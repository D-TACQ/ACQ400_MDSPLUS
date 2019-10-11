#
# Copyright (c) 2017, Massachusetts Institute of Technology All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice, this
# list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
import numpy as np
import MDSplus
import threading
import Queue
import socket
import time
import inspect


try:
    acq400_hapi = __import__('acq400_hapi', globals(), level=1)
except:
    acq400_hapi = __import__('acq400_hapi', globals())

class TRANSIENT(MDSplus.Device):
    """
    D-Tacq ACQ2106_MGT support.

    """

    parts=[
        # The user will need to change the hostname to the relevant hostname/IP.
        {'path':':NODE','type':'text','value':'acq2106_085', 'options':('no_write_shot',)},
        {'path':':SITE','type':'numeric', 'value': 1, 'options':('no_write_shot',)},
        {'path':':TRIG_MODE','type':'text', 'value': 'role_default', 'options':('no_write_shot',)},
        {'path':':ROLE','type':'text', 'value': 'master', 'options':('no_write_shot',)},
        {'path':':FREQ','type':'numeric', 'value': int(1e7), 'options':('no_write_shot',)},
        {'path':':TRIG_TIME','type':'numeric', 'options':('write_shot',)},
        {'path':':TRIG_STR','type':'text', 'options':('nowrite_shot',),'valueExpr':"EXT_FUNCTION(None,'ctime',head.TRIG_TIME)"},
        {'path':':RUNNING','type':'any', 'options':('no_write_model',)},
        ]

    uut = acq400_hapi.Acq400(parts[0]["value"], monitor=False)
    nchans = uut.nchan()
    for i in range(nchans):
        parts.append({'path':':INPUT_%3.3d'%(i+1,),'type':'signal','options':('no_write_model','write_once',),
                      'valueExpr':'head.setChanScale(%d)' %(i+1,)})
        parts.append({'path':':INPUT_%3.3d:DECIMATE'%(i+1,),'type':'NUMERIC', 'value':1, 'options':('no_write_shot')})
        parts.append({'path':':INPUT_%3.3d:COEFFICIENT'%(i+1,),'type':'NUMERIC', 'value':1, 'options':('no_write_shot')})
        parts.append({'path':':INPUT_%3.3d:OFFSET'%(i+1,),'type':'NUMERIC', 'value':1, 'options':('no_write_shot')})
    del i

    debug=None

    trig_types=[ 'hard', 'soft', 'automatic']


    class MDSWorker(threading.Thread):
        NUM_BUFFERS = 20

        def __init__(self,dev):
            super(TRANSIENT.MDSWorker,self).__init__(name=dev.path)
            threading.Thread.__init__(self)

            self.dev = dev.copy()

            self.chans = []
            self.decim = []

            self.uut = acq400_hapi.Acq400(self.dev.node.data(), monitor=False)
            self.nchans = self.uut.nchan()

            for i in range(self.nchans):
                self.chans.append(getattr(self.dev, 'INPUT_%3.3d'%(i+1)))

            self.device_thread = self.DeviceWorker(self)

        def run(self):
            def lcm(a,b):
                from fractions import gcd
                return (a * b / gcd(int(a), int(b)))

            def lcma(arr):
                ans = 1.
                for e in arr:
                    ans = lcm(ans, e)
                return int(ans)

            if self.dev.debug:
                print("MDSWorker running")

            self.device_thread.start()

            self.device_thread.join()

        class DeviceWorker(threading.Thread):
            running = False

            def __init__(self,mds):
                threading.Thread.__init__(self)
                self.debug = mds.dev.debug
                self.node_addr = mds.dev.node.data()
                self.freq = mds.dev.freq.data()
                self.nchans = mds.nchans
                self.chans = mds.chans

            def stop(self):
                print "Setting running to false 1"
                self.running = False

            def run(self):
                if self.debug:
                    print("DeviceWorker running")

                self.running = True

                uut = acq400_hapi.Acq400(self.node_addr, monitor=False)

                # Get all data
                data = uut.pull_data()

                # Put data in node
                for pos, c in enumerate(self.chans):
                    if c.on:
                        print "DEBUG: ", pos, c
                        c.putData(data[pos])
                print "Finished storing data"



    def setChanScale(self,num):
        chan=self.__getattr__('INPUT_%3.3d' % num)
        chan.setSegmentScale(MDSplus.ADD(MDSplus.MULTIPLY(chan.COEFFICIENT,MDSplus.dVALUE()),chan.OFFSET))

    def init(self):
        print('Running init')

        uut = acq400_hapi.Acq400(self.node.data(), monitor=False)

        trig_types=[ 'hard', 'soft', 'automatic']
        trg = self.trig_mode.data()

        if trg == 'hard':
            trg_dx = 0
        elif trg == 'automatic':
            trg_dx = 1
        elif trg == 'soft':
            trg_dx = 1

        # The default case is to use the trigger set by sync_role.
        if self.trig_mode.data() == 'role_default':
            uut.s0.sync_role = "{} {}".format(self.role.data(), self.freq.data())
        else:
            # If the user has specified a trigger.
            uut.s0.sync_role = '{} {} TRG:DX={}'.format(self.role.data(), self.freq.data(), trg_dx)

        # Now we set the trigger to be soft when desired.
        if trg == 'soft':
            uut.s0.transient = 'SOFT_TRIGGER=0'
        if trg == 'automatic':
            uut.s0.transient = 'SOFT_TRIGGER=1'

        print('Finished init')


    def arm(self):
        print("Capturing now.")
        uut = acq400_hapi.Acq400(self.node.data())
        # uut.s0.set_arm
        shot_controller = acq400_hapi.ShotController([uuts])
        shot_controller.run_shot()
        print("Finished capture.")
    ARM=arm


    def soft_trigger(self):
        uut = acq400_hapi.Acq400(self.node.data(), monitor=False)
        uut.s0.soft_trigger = 1


    def pull(self):
        print("Starting data collection now.")
        import os
        import sys
        from threading import Thread
        import tempfile
        import subprocess

        uut = acq400_hapi.Acq400(self.node.data(), monitor=False)
        uut.s0.set_knob('set_abort', '1')
        self.running.on=True
        thread = self.MDSWorker(self)
        thread.start()
    PULL=pull


    def stop(self):
        print "Setting running to false 2"
        self.running.on = False
    STOP=stop

