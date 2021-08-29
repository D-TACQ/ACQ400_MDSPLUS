'''
ACQ2106_M8 : Support for ACQ2106 with MGTDRAM8
Created on 29 Aug 2021

@author: pgm
'''

import acq400_base


class _ACQ2106_M8(acq400_base._ACQ400_M8_BASE):
    """
    D-Tacq ACQ2106 MR transient support.
    """
    pass


class_ch_dict = acq400_base.create_classes(
    _ACQ2106_M8, "ACQ2106_MR",
    list(_ACQ2106_M8.base_parts),
    acq400_base.ACQ2106_CHANNEL_CHOICES
)

for key,val in class_ch_dict.items():
    exec("{} = {}".format(key, "val"))

if __name__ == '__main__':
    acq400_base.print_generated_classes(class_ch_dict)
