# RPi &amp; IR  [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/etfovac/rpi_ir/blob/master/LICENSE) [![GitHub (pre-)release](https://img.shields.io/badge/releases--yellow.svg)](https://github.com/etfovac/rpi_ir/releases/)
RPi &amp; IR: Raspberry Pi GPIO &amp; Infrared remote controls (No LIRC)  

### Keywords  
> Raspberry Pi GPIO  
> Infrared remote, Infrared sensor, Infrared remote control protocol  
> Python callback

### Overview  
- [x] Monitor GPIO pin (no blocking)
- [x] Capture edges (GPIO callbacks)
- [x] Decode frame (bin, hex)
- [ ] Data field recovery (redundancy, 8 + 8)
- [ ] Address field recovery (redundancy, 8 + 8)
- [ ] Log to config file and map hex codes to buttons
- [ ] GUI (link code to button and save in config file, confirm/test by button highlighting)
- [ ] Handle repeat codes, button debouncing, etc.
- [ ] Re-transmit IR codes
- [ ] Transmit custom IR codes

### IR Protocols  

NEC (now Renesas) IR code format:  
- bit 1:  0.5625 ms pulse, 1.6875 ms space (total duration 2.250 ms)  
- bit 0:  0.5625 ms pulse, 0.5625 ms space (total duration 1.125 ms) 

> The NEC code operates with a carrier frequency of 38 kHz and uses pulse position modulation (PPM).  

Header:  
> Transmission begins with a 9 ms long start bit, followed by a 4.5 ms space.  

The message  has 32  bits:  
- 16 bit manufacturer (adress) field (8 + 8) 
- 16 bit command field (8 + 8)   
> Address and Command are transmitted twice.  
> The second time all bits are inverted and can be used for verification of the received message.  
> The total transmission time is constant because every bit is repeated with its inverted length.  

> The 8 bit wide data is sent twice, the second time inverted.  
> A complete message is 67.5 ms long.  

A new message can be sent every ~108 ms. There is a 40ms gap between a message code and repeat code.  

Repeat code:  
> A special current saving feature is implemented if a key is held down on the controller.  
> In this case the message consists of a 9 ms start bit followed by a 2.25 ms space and a 0.56 ms pulse.  
> Sanyo supply ICs that generate codes using this format but have a 13 bit manufacturers code.  

Taken from [winlirc](http://winlirc.sourceforge.net/technicaldetails.html) (duration in microseconds, us):
``` 
Yamaha

Typical Header:

 bits           16
 flags SPACE_ENC|REVERSE

 header       9067  4393
 one           642   470
 zero          642  1600
 ptrail        642
 repeat       9065  2139
 pre_data_bits   16
 gap          39597

``` 
<b> Note </b>: If you had used LIRC, then you had to uncomment a line in ``` /boot/config.txt```  to reserve Rx/Tx GPIO pin. Even after uninstalling LIRC that line still reserves the pin, so you'll need to comment it out again and reboot. After a reboot that pin is available for registering event detection and callback.  
Rx pin is 11 (Board), i.e. 17 (BCM).  
``` 
# Uncomment this to enable infrared communication.
#dtoverlay=gpio-ir,gpio_pin=17
#dtoverlay=gpio-ir-tx,gpio_pin=18
```  
### References  
RPi GPIO, IR:  
<a href="https://github.com/Lime-Parallelogram/IR-Code-Referencer">Lime-Parallelogram</a> (github with link to youtube)  
<a href="https://fishandwhistle.net/post/2016/raspberry-pi-pure-python-infrared-remote-control/">fishandwhistle (2016 blog)</a>  
<a href="https://blog.bschwind.com/2016/05/29/sending-infrared-commands-from-a-raspberry-pi-without-lirc/">bschwind (2016 blog)</a>  
IR frame format info:  
<a href="http://winlirc.sourceforge.net/technicaldetails.html">winlirc - technical details</a>   
<a href="https://techdocs.altium.com/display/FPGA/NEC+Infrared+Transmission+Protocol">NEC Infrared Transmission Protocol</a>  
<a href="http://read.pudn.com/downloads157/sourcecode/embed/701593/docs/IR%20Formats%202.PDF">IR Formats 2nd part (PDF)</a>  
<a href="https://www.sbprojects.net/knowledge/ir/nec.php">SB-Projects - IR - NEC Protocol</a>  
<a href="https://www.youtube.com/watch?v=BUvFGTxZBG8">EEVblog #506 - IR Remote Control Arduino Protocol Tutorial</a>  
