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


import numpy as np
import MDSplus
import threading
# import Queue
from Queue import Queue, Empty
import socket
import time
import inspect
import os


try:
    acq400_hapi = __import__('acq400_hapi', globals(), level=1)
except:
    acq400_hapi = __import__('acq400_hapi', globals())


print("pgmwashere {} {} HAPI {}".format("acq400_base", __file__, acq400_hapi.__file__))


class _ACQ400_BASE(MDSplus.Device):
    """
    D-Tacq ACQ400 Base parts and methods.

    All other carrier/function combinations use this class as a parent class.
    """

    base_parts=[
        # The user will need to change the hostname to the relevant hostname/IP.
        {'path':':NODE','type':'text','value':'acq2106_999', 'options':('no_write_shot',)},
        {'path':':SITE','type':'numeric', 'value': 1, 'options':('no_write_shot',)},
        {'path':':TRIG_MODE','type':'text', 'value': 'role_default', 'options':('no_write_shot',)},
        {'path':':ROLE','type':'text', 'value': 'fpmaster', 'options':('no_write_shot',)},
        {'path':':FREQ','type':'numeric', 'value': int(1e6), 'options':('no_write_shot',)},
        {'path':':SAMPLES','type':'numeric', 'value': int(1e5), 'options':('no_write_shot',)},
        {'path':':INIT_ACTION', 'type':'action', 'valueExpr':"Action(Dispatch('CAMAC_SERVER','INIT',50,None),Method(None,'INIT',head))",'options':('no_write_shot',)},
        {'path':':ARM_ACTION', 'type':'action', 'valueExpr':"Action(Dispatch('CAMAC_SERVER','INIT',51,None),Method(None,'ARM',head))",'options':('no_write_shot',)},
        {'path':':STORE_ACTION', 'type':'action', 'valueExpr':"Action(Dispatch('CAMAC_SERVER','INIT',52,None),Method(None,'STORE',head))",'options':('no_write_shot',)},
    ]

    trig_types=[ 'hard', 'soft', 'automatic']


    def setChanScale(self,num):
        chan=self.__getattr__('INPUT_%3.3d' % num)
        print("pgmwashere. BOGUS alert. computed but going nowhere:{}".format(chan))


    def init(self):

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

        uut.s0.transient = "POST={}".format(self.samples.data())

    INIT = init


class _ACQ400_ST_BASE(_ACQ400_BASE):

    """
    A sub-class of _ACQ400_BASE that includes classes for streaming data
    and the extra nodes for streaming devices.
    """

    st_base_parts = [
        {'path':':RUNNING',     'type':'numeric',                  'options':('no_write_model',)},
        {'path':':SEG_LENGTH',  'type':'numeric', 'value': 8000,   'options':('no_write_shot',)},
        {'path':':MAX_SEGMENTS','type':'numeric', 'value': 1000,   'options':('no_write_shot',)},
        {'path':':SEG_EVENT',   'type':'text',   'value': 'STREAM','options':('no_write_shot',)},
        {'path':':TRIG_TIME',   'type':'numeric',                  'options':('write_shot',)}
    ]


    def arm(self):
        self.running.on=True
        thread = self.MDSWorker(self)
        thread.start()
    ARM=arm

    def stop(self):
        self.running.on = False
    STOP = stop

    class MDSWorker(threading.Thread):
        NUM_BUFFERS = 20

        def __init__(self,dev):
            super(_ACQ400_ST_BASE.MDSWorker,self).__init__(name=dev.path)
            threading.Thread.__init__(self)

            self.dev = dev.copy()

            self.chans = []
            self.decim = []
            # self.nchans = self.dev.sites*32
            uut = acq400_hapi.Acq400(self.dev.node.data())
            self.nchans = uut.nchan()

            for i in range(self.nchans):
                self.chans.append(getattr(self.dev, 'INPUT_%3.3d'%(i+1)))
                self.decim.append(getattr(self.dev, 'INPUT_%3.3d:DECIMATE' %(i+1)).data())
            self.seg_length = self.dev.seg_length.data()
            self.segment_bytes = self.seg_length*self.nchans*np.int16(0).nbytes

            self.empty_buffers = Queue()
            self.full_buffers  = Queue()

            for i in range(self.NUM_BUFFERS):
                self.empty_buffers.put(bytearray(self.segment_bytes))
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

            event_name = self.dev.seg_event.data()

            dt = 1./self.dev.freq.data()

            decimator = lcma(self.decim)

            if self.seg_length % decimator:
                self.seg_length = (self.seg_length // decimator + 1) * decimator

            self.device_thread.start()

            segment = 0
            running = self.dev.running
            max_segments = self.dev.max_segments.data()
            while running.on and segment < max_segments:
                try:
                    buf = self.full_buffers.get(block=True, timeout=1)
                except Empty:
                    continue

                buffer = np.frombuffer(buf, dtype='int16')
                i = 0
                for c in self.chans:
                    slength = self.seg_length/self.decim[i]
                    deltat  = dt * self.decim[i]
                    if c.on:
                        b = buffer[i::self.nchans*self.decim[i]]
                        begin = segment * slength * deltat
                        end   = begin + (slength - 1) * deltat
                        dim   = MDSplus.Range(begin, end, deltat)
                        c.makeSegment(begin, end, dim, b)
                    i += 1
                segment += 1
                MDSplus.Event.setevent(event_name)

                self.empty_buffers.put(buf)

            self.dev.trig_time.record = self.device_thread.trig_time - ((self.device_thread.io_buffer_size / np.int16(0).nbytes) * dt)
            self.device_thread.stop()

        class DeviceWorker(threading.Thread):
            running = False

            def __init__(self,mds):
                threading.Thread.__init__(self)
                self.debug = mds.dev.debug
                self.node_addr = mds.dev.node.data()
                self.seg_length = mds.dev.seg_length.data()
                self.segment_bytes = mds.segment_bytes
                self.freq = mds.dev.freq.data()
                self.nchans = mds.nchans
                self.empty_buffers = mds.empty_buffers
                self.full_buffers = mds.full_buffers
                self.trig_time = 0
                self.io_buffer_size = 4096

            def stop(self):
                self.running = False

            def run(self):
                if self.debug:
                    print("DeviceWorker running")

                self.running = True

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.node_addr,4210))
                s.settimeout(6)

                # trigger time out count initialization:
                first = True
                while self.running:
                    try:
                        buf = self.empty_buffers.get(block=False)
                    except Empty:
                        buf = bytearray(self.segment_bytes)

                    toread =self.segment_bytes
                    try:
                        view = memoryview(buf)
                        while toread:
                            nbytes = s.recv_into(view, min(self.io_buffer_size,toread))
                            if first:
                                self.trig_time = time.time()
                                first = False
                            view = view[nbytes:] # slicing views is cheap
                            toread -= nbytes

                    except socket.timeout as e:
                        print("Got a timeout.")
                        err = e.args[0]
                        # this next if/else is a bit redundant, but illustrates how the
                        # timeout exception is setup

                        if err == 'timed out':
                            time.sleep(1)
                            print (' recv timed out, retry later')
                            continue
                        else:
                            print (e)
                            break
                    except socket.error as e:
                        # Something else happened, handle error, exit, etc.
                        print("socket error", e)
                        self.full_buffers.put(buf[:self.segment_bytes-toread])
                        break
                    else:
                        if toread != 0:
                            print ('orderly shutdown on server end')
                            break
                        else:
                            self.full_buffers.put(buf)


class _ACQ400_TR_BASE(_ACQ400_BASE):
    """
    A child class of _ACQ400_BASE that contains the specific methods for
    taking a transient capture.
    """


    def _arm(self):
        uut = acq400_hapi.Acq400(self.node.data())
        shot_controller = acq400_hapi.ShotController([uut])
        shot_controller.run_shot()
        return None


    def arm(self):
        thread = threading.Thread(target = self._arm)
        thread.start()
    ARM=arm


    def store(self):
        thread = threading.Thread(target = self._store)
        thread.start()
        return None


    def _store(self):

        uut = acq400_hapi.Acq400(self.node.data())
        while uut.statmon.get_state() != 0: continue
        self.chans = []
        nchans = uut.nchan()
        for ii in range(nchans):
            self.chans.append(getattr(self, 'INPUT_%3.3d'%(ii+1)))

        uut.fetch_all_calibration()
        eslo = uut.cal_eslo[1:]
        eoff = uut.cal_eoff[1:]
        channel_data = uut.read_channels()

        DT=1/float(self.FREQ.data())
        nsam = len(channel_data[0])
        print("self.FREQ.data() nsam:{} {} DT {}".format(nsam, self.FREQ.data(), DT))

        for ic, ch in enumerate(self.chans):
            if ch.on:
                ch.RAW.putData(channel_data[ic])  # store raw for easy access
                ch.EOFF.putData(float(eoff[ic]))
                ch.ESLO.putData(float(eslo[ic]))
                ch.CAL.putData(MDSplus.Data.compile('BUILD_WITH_UNITS($3*$1+$2, "V")', ch.ESLO, ch.EOFF, ch.RAW))  # does this make a COPY of ch.RAW?
# from mdsPutCh, recipe by B.Blackwell C(2007)
                win = MDSplus.Data.compile('BUILD_WINDOW(0, $1, BUILD_WITH_UNITS(0, "s"))', nsam)
                axis = MDSplus.Data.compile('BUILD_WITH_UNITS(BUILD_RANGE($1, $2, $3), "s")', 0, nsam*DT, DT)
                ch.TB.putData(MDSplus.Dimension(win, axis))
                ch.CAL_INPUT.putData(MDSplus.Data.compile('BUILD_SIGNAL($1, $2, $3)', ch.CAL, ch.RAW, ch.TB))
                ch.putData(ch.CAL_INPUT)


    STORE=store

    pass


class _ACQ400_MR_BASE(_ACQ400_TR_BASE):
    """
    A sub-class of _ACQ400_TR_BASE that includes functions for MR data
    and the extra nodes for MR processing.
    """

    mr_base_parts = [
        {'path':':DT',       'type':'numeric','options':('write_shot',)},
        {'path':':TB_NS',    'type':'signal', 'options':('no_write_model','write_once',)},
        {'path':':DECIMS',   'type':'signal','options':('no_write_model','write_once',)},
        {'path':':Fclk',     'type':'numeric','value':40000000,'options':('write_shot',)},
        {'path':':trg0_src', 'type':'text',   'value':'EXT','options':('write_model',)},
        {'path':':evsel0',   'type':'numeric','value':4,'options':('write_model',)},
        {'path':':MR10DEC',  'type':'numeric','value':32,'options':('write_model',)},
        {'path':':STL',      'type':'text',   'options':('write_model',)}
    ]


    def _create_time_base(self, decims, dt):
        tb = np.zeros(decims.shape[-1])
        ttime = 0
        for ix, dec in enumerate(decims):
            tb[ix] = ttime
            ttime += float(dec) * dt

        return tb

    def create_time_base(self, uut):
        decims = uut.read_decims()
        try:
            dt = 1 / ((round(float(uut.s0.SIG_CLK_MB_FREQ.split(" ")[1]), -4)) * 1e-9)
        except:
            dt = 25
        tb_ns = self._create_time_base(decims, dt)

        self.DECIMS.putData(decims)
        self.DT.putData(dt)
        self.TB_NS.putData(tb_ns)

    def store(self):
        uut = acq400_hapi.Acq400(self.node.data())
        self.chans = []
        nchans = uut.nchan()
        for ii in range(nchans):
            self.chans.append(getattr(self, 'INPUT_%3.3d'%(ii+1)))

        uut.fetch_all_calibration()
        eslo = uut.cal_eslo[1:]
        eoff = uut.cal_eoff[1:]
        channel_data = uut.read_channels()

        for ic, ch in enumerate(self.chans):
            if ch.on:
                ch.putData(channel_data[ic])
                ch.EOFF.putData(float(eoff[ic]))
                ch.ESLO.putData(float(eslo[ic]))
                expr = "{} * {} + {}".format(ch, ch.ESLO, ch.EOFF)
                ch.CAL_INPUT.putData(MDSplus.Data.compile(expr))

        self.create_time_base(uut)
        # return None
    STORE=store


    def arm():
        # A customised ARM function for the acq2106_MR setup.
        uut = acq400_hapi.Acq400(self.node.data())
        shot_controller = acq400_hapi.ShotController([uut])
        shot_controller.run_shot(remote_trigger=self.selects_trg_src(uut, self.trg0_src.data()))
        return None
    ARM = arm


    def selects_trg_src(self, uut, src):
        def select_trg_src():
            uut.s0.SIG_SRC_TRG_0 = src
        return select_trg_src


    def denormalise_stl(self, stl):

        # lines = args.stl.splitlines()
        lines = stl.splitlines()
        stl_literal_lines = []
        for line in lines:
            if line.startswith('#') or len(line) < 2:
                # if args.verbose:
                #     print(line)
                continue
            else:
                action = line.split('#')[0]

                if action.startswith('+'): # support relative increments
                    delayp = '+'
                    action  = action[1:]
                else:
                    delayp = ''

                delay, state = [int(x) for x in action.split(',')]
                # delayk = int(delay * self.Fclk.data() / 1000000)
                delayk = int(delay * 40000000 / 1000000)
                delaym = delayk - delayk % self.MR10DEC.data()
                state = state << self.evsel0.data()
                elem = "{}{:d},{:02x}".format(delayp, delaym, state)
                stl_literal_lines.append(elem)
                # if args.verbose:
                #     print(line)

        return "\n".join(stl_literal_lines)


    def init(self):
        # args.uuts = [ acq400_hapi.Acq2106(u, has_comms=False) for u in args.uut ]
        uut = acq400_hapi.Acq2106(self.node.data())
        # master = args.uuts[0]
        self.STL.putData("/home/dt100/PROJECTS/acq400_hapi/user_apps/STL/acq2106_test10.stl")
        with open(self.STL.data(), 'r') as fp:
            stl = fp.read()

        lit_stl = self.denormalise_stl(stl)

        uut.s0.SIG_SRC_TRG_0 = 'NONE'

        # for u in args.uuts:
        # acq400_hapi.Acq400UI.exec_args(uut, args)
        uut.s0.gpg_trg = '1,0,1'
        uut.s0.gpg_clk = '1,1,1'
        uut.s0.GPG_ENABLE = '0'
        uut.load_gpg(lit_stl, 2) # TODO: Change to MDSplus debug.
        uut.set_MR(True, evsel0=self.evsel0.data(), evsel1=self.evsel0.data()+1, MR10DEC=self.MR10DEC.data())
        uut.s0.set_knob('SIG_EVENT_SRC_{}'.format(self.evsel0.data()), 'GPG')
        uut.s0.set_knob('SIG_EVENT_SRC_{}'.format(self.evsel0.data()+1), 'GPG')
        uut.s0.GPG_ENABLE = '1'
    INIT = init

    pass


class _ACQ400_M8_BASE(_ACQ400_BASE):
    """
    A child class of _ACQ400_BASE that contains the specific methods for
    taking a transient capture from MGTDRAM8.
    """


    def _arm(self):
        uut = acq400_hapi.Acq400(self.node.data())
        print("WORKTODO")
        return None


    def arm(self):
        thread = threading.Thread(target = self._arm)
        thread.start()
    ARM=arm


    def store(self):
        thread = threading.Thread(target = self._store)
        thread.start()
        return None


    def _store(self):

        uut = acq400_hapi.Acq400(self.node.data())
        while uut.statmon.get_state() != 0: continue
        self.chans = []
        nchans = uut.nchan()
        for ii in range(nchans):
            self.chans.append(getattr(self, 'INPUT_%3.3d'%(ii+1)))

        uut.fetch_all_calibration()
        eslo = uut.cal_eslo[1:]
        eoff = uut.cal_eoff[1:]
        channel_data = uut.read_channels()

        DT=1/float(self.FREQ.data())
        nsam = len(channel_data[0])
        print("self.FREQ.data() nsam:{} {} DT {}".format(nsam, self.FREQ.data(), DT))

        for ic, ch in enumerate(self.chans):
            if ch.on:
                ch.RAW.putData(channel_data[ic])  # store raw for easy access
                ch.EOFF.putData(float(eoff[ic]))
                ch.ESLO.putData(float(eslo[ic]))
                ch.CAL.putData(MDSplus.Data.compile('BUILD_WITH_UNITS($3*$1+$2, "V")', ch.ESLO, ch.EOFF, ch.RAW))  # does this make a COPY of ch.RAW?
# from mdsPutCh, recipe by B.Blackwell C(2007)
                win = MDSplus.Data.compile('BUILD_WINDOW(0, $1, BUILD_WITH_UNITS(0, "s"))', nsam)
                axis = MDSplus.Data.compile('BUILD_WITH_UNITS(BUILD_RANGE($1, $2, $3), "s")', 0, nsam*DT, DT)
                ch.TB.putData(MDSplus.Dimension(win, axis))
                ch.CAL_INPUT.putData(MDSplus.Data.compile('BUILD_SIGNAL($1, $2, $3)', ch.CAL, ch.RAW, ch.TB))
                ch.putData(ch.CAL_INPUT)


    STORE=store

    pass


def int_key_chan(elem):
    return int(elem.split('_')[2])

def print_generated_classes(class_dict):
    print("# public classes created in this module")
    key1 = None
    for key in sorted(class_dict.keys(), key=int_key_chan):
        if key1 is None:
            key1 = key
        print("# {}".format(key))
    print("{}".format(key1))
    for p in class_dict[key1].parts:
        print("{}".format(p))


INPFMT3 = ':INPUT_%3.3d'
#INPFMT2 = ':INPUT_%2.2d'

ACQ2106_CHANNEL_CHOICES = [8, 16, 24, 32, 40, 48, 64, 80, 96, 128, 160, 192]
ACQ1001_CHANNEL_CHOICES = [8, 16, 24, 32, 40, 48, 64]

def assemble(cls):
    inpfmt = INPFMT3
# probably easier for analysis code if ALWAYS INPUT_001
#    inpfmt = INPFMT2 if cls.nchan < 100 else INPFMT3
    for ch in range(1, cls.nchan+1):
        # expr =
        node = inpfmt%(ch,)
        cls.parts.append({'path': node, 'type':'signal','options':('no_write_model','write_once',)})
#                          'valueExpr':'head.setChanScale(%d)' %(ch,)})
        cls.parts.append({'path': node+':RAW', 'type':'signal','options':('no_write_model','write_once',)})
        cls.parts.append({'path': node+':CAL', 'type':'signal'})
        cls.parts.append({'path': node+':TB', 'type':'signal'})
        cls.parts.append({'path': node+':DECIMATE', 'type':'NUMERIC', 'value':1, 'options':('no_write_shot')})
        cls.parts.append({'path': node+':COEFFICIENT','type':'NUMERIC', 'value':1, 'options':('no_write_shot')})
        cls.parts.append({'path': node+':OFFSET', 'type':'NUMERIC', 'value':1, 'options':('no_write_shot')})
        cls.parts.append({'path': node+':EOFF','type':'NUMERIC', 'value':1, 'options':('no_write_shot')})
        cls.parts.append({'path': node+':ESLO', 'type':'NUMERIC', 'value':1, 'options':('no_write_shot')})
        cls.parts.append({'path': node+':CAL_INPUT', 'type':'signal'})
    return cls


def create_classes(base_class, root_name, parts, channel_choices):
    my_classes = {}
    for nchan in channel_choices:
        class_name = "{}_{}".format(root_name, str(nchan))
        my_parts = list(parts)
        my_classes[class_name] = assemble(
            type(class_name, (base_class,), {"nchan": nchan, "parts": my_parts}))
        # needed because of lockout in mdsplus code file
        # python/MDSplus/tree.py function findPyDevices
        my_classes[class_name].__module__ = base_class.__module__
        # exec("{} = {}".format(class_name, "my_classes[class_name]"))
    return my_classes
