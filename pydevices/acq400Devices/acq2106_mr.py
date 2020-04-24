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


import acq400_base


class _ACQ2106_MR(acq400_base._ACQ400_MR_BASE):
    """
    D-Tacq ACQ2106 MR transient support.
    """
    pass


class_ch_dict = acq400_base.create_classes(
    _ACQ2106_MR, "ACQ2106_MR",
    list(_ACQ2106_MR.base_parts) + list(_ACQ2106_MR.mr_base_parts),
    acq400_base.ACQ2106_CHANNEL_CHOICES
)

for key,val in class_ch_dict.items():
    exec("{} = {}".format(key, "val"))

if __name__ == '__main__':
    acq400_base.print_generated_classes(class_ch_dict)

# public classes created in this module
# ACQ2106_MR_8
# ACQ2106_MR_16
# ACQ2106_MR_24
# ACQ2106_MR_32
# ACQ2106_MR_40
# ACQ2106_MR_48
# ACQ2106_MR_64
# ACQ2106_MR_80
# ACQ2106_MR_96
# ACQ2106_MR_128
# ACQ2106_MR_160
# ACQ2106_MR_192
