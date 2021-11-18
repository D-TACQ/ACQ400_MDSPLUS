## MDSPLUS Support for D-TACQ ACQ400 series

Pydevices provided for every combination of ACQ1001, ACQ2106
Operating Modes
1. TR : Transient Recorder to ZYNQ DRAM (max 512MB)
2. M8 : Transient Recorder to MGTDRAM8 (max 8GB)
3. MR : Transient Recorder, multirate (ACQ480-specific)
4. ST : Streaming device.

```
git clone https://github.com/D-TACQ/ACQ400_MDSPLUS
cp -a ACQ400_MDSPLUS/pydevices/acq400Devices /usr/local/mdsplus/pydevices
```

For scripts to create trees, jscope configs and store data, please see:
https://github.com/D-TACQ/ACQ400_MDSplus_TREESUPPORT



