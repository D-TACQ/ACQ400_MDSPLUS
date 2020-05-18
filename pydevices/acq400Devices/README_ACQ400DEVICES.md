# ACQ400DEVICES: MDSplus support for ACQ400

ACQ400 is a range of [DAQ Appliances](http://www.d-tacq.com/modproducts.shtml) comprising an networked [Carrier](http://www.d-tacq.com/modcarriers.shtml) and a pyload of one or more analog [Modules](http://www.d-tacq.com/modproducts_modules.shtml). The device support allows any carrier/payload combination to be used in number of **Operating Modes**.

For support and comment please contact: info@d-tacq.co.uk

## Supported Carriers
 * [ACQ1001](http://www.d-tacq.com/acq1001Q.shtml) : single site
 * [ACQ1002](http://d-tacq.com/acq1002R.shtml) : dual site
 * [ACQ2106](http://www.d-tacq.com/acq2106.shtml) : up to 6 sites

## Supported Modules
 * [ACQ435ELF](http://www.d-tacq.com/acq435elf.shtml) : 32 simultaneous 24 bit ADC, 128kSPS/channel
 * [ACQ423ELF](http://www.d-tacq.com/acq423elf.shtml) : 32 simultaneous 16 bit ADC, 200kSPS/channel
 * [ACQ424ELF](http://www.d-tacq.com/acq424elf.shtml) : 32 simultaneous 16 bit ADC, 1MSPS/channel
 * [ACQ425ELF](http://www.d-tacq.com/acq425elf.shtml) : 16 simultaneous 16 bit ADC, 2MSPS/channel
 * [ACQ480ELF](http://www.d-tacq.com/acq482elf.shtml) :  8 simultaneous 14 bit ADC, to 80MSPS/channel
 * [ACQ482ELF](http://www.d-tacq.com/acq482elf.shtml) : 16 simultaneous 14 bit oversampling ADC, to 80MSPS/channel

## Operating Modes
 * **TR** Transient: store a shot at up to full rate to limit of onboard memory, post-shot upload to MDSplus.
 * **MG** Transient, but with extended, 8GByte memory (acq2106 only)
 * **MR** MultiRate Transient, with RUN/JOG/SPRINT variable rates to extend use of memory
 * **ST** Streaming: streaming capture, perhaps at reduced rate, segmented store to MDSplus
 * **MV** Streaming capture with multiple event captures at full rate.

## Implementation

### Core Code: acq400_base.py
* base_parts[] : array of nodes, to be customised
* assemble() : adds payload specific nodes, essentially a group of nodes per channel.
* methods:
  * INIT()
  * ARM()
  * STORE()
* DO NOT call acq400_base.py functions directly!

### Generator classes
Leaf modules generate a custom class for each carrier/mode/payload combination
eg
* ACQ2106_MR_128
  * ACQ2106 : Carrier
  * MR : Operating Mode: Multi Rate
  * 128 : Payload, 128 channels.
* Create devices from the appropriate specific combination

```
[pgm@hoy5 acq400Devices]$ for file in acq[21]*.py; do echo " * $file";grep '^# ACQ[12]' $file | sed -e 's/# /  * /'; done
```
 * acq1001_st.py
  * ACQ1001_ST_8
  * ACQ1001_ST_16
  * ACQ1001_ST_24
  * ACQ1001_ST_32
  * ACQ1001_ST_40
  * ACQ1001_ST_48
  * ACQ1001_ST_64
 * acq1001_tr.py
  * ACQ1001_TR_8
  * ACQ1001_TR_16
  * ACQ1001_TR_24
  * ACQ1001_TR_32
  * ACQ1001_TR_40
  * ACQ1001_TR_48
  * ACQ1001_TR_64
 * acq2106_mr.py
  * ACQ2106_MR_8
  * ACQ2106_MR_16
  * ACQ2106_MR_24
  * ACQ2106_MR_32
  * ACQ2106_MR_40
  * ACQ2106_MR_48
  * ACQ2106_MR_64
  * ACQ2106_MR_80
  * ACQ2106_MR_96
  * ACQ2106_MR_128
  * ACQ2106_MR_160
  * ACQ2106_MR_192
 * acq2106_st.py
  * ACQ2106_ST_8
  * ACQ2106_ST_16
  * ACQ2106_ST_24
  * ACQ2106_ST_32
  * ACQ2106_ST_40
  * ACQ2106_ST_48
  * ACQ2106_ST_64
  * ACQ2106_ST_80
  * ACQ2106_ST_96
  * ACQ2106_ST_128
  * ACQ2106_ST_160
  * ACQ2106_ST_192
 * acq2106_tr.py
  * ACQ2106_TR_8
  * ACQ2106_TR_16
  * ACQ2106_TR_24
  * ACQ2106_TR_32
  * ACQ2106_TR_40
  * ACQ2106_TR_48
  * ACQ2106_TR_64
  * ACQ2106_TR_80
  * ACQ2106_TR_96
  * ACQ2106_TR_128
  * ACQ2106_TR_160
  * ACQ2106_TR_192

