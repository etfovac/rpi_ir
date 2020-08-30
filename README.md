# rpi_ir
RPi &amp; IR: Raspberry Pi GPIO &amp; Infrared remote controls (No LIRC)


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

### References  
https://github.com/Lime-Parallelogram/IR-Code-Referencer  
https://fishandwhistle.net/post/2016/raspberry-pi-pure-python-infrared-remote-control/  
https://blog.bschwind.com/2016/05/29/sending-infrared-commands-from-a-raspberry-pi-without-lirc/  
header & repeat info http://winlirc.sourceforge.net/technicaldetails.html  
