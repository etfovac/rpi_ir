# RPi &amp; IR  [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/etfovac/rpi_ir/blob/master/LICENSE) [![GitHub (pre-)release](https://img.shields.io/badge/releases--yellow.svg)](https://github.com/etfovac/rpi_ir/releases/)
RPi &amp; IR: Raspberry Pi GPIO &amp; Infrared remote controls (No LIRC)  

### Keywords  
> Raspberry Pi GPIO  
> Infrared remote, Infrared sensor, Infrared remote control protocol  
> Python callback

### Table of Contents (Wiki)
[Wiki Home](https://github.com/etfovac/rpi_ir/wiki)  
[Overview](https://github.com/etfovac/rpi_ir/wiki/Overview)  
[Notes](https://github.com/etfovac/rpi_ir/wiki/Notes)  
[IR Protocols](https://github.com/etfovac/rpi_ir/wiki/IR-Protocols)  
[Examples: IR Capture](https://github.com/etfovac/rpi_ir/wiki/Examples:-IR-Capture)  
[References](https://github.com/etfovac/rpi_ir/wiki/References)  

### IR Recorder
Fully operational and reliable IR recorder is implemented in file ```ir-rec_main.py```: 
```py
def ir_rx_callback(ir_decoded, ir_hex, valid):
        print("ir_decoded={} len={}".format(ir_decoded, len(ir_decoded)))
        print("ir_dec_hex={}".format(ir_hex))
        if valid:
            print("Valid IR code! Pressed button was: ")
            key = input()
            button_map[key] = {ir_decoded, ir_hex}
            print(button_map)
pi = pigpio.pi()
ir_rec = infrared.rx(pi, IR_PIN, ir_rx_callback, 5)
```  
It relies on 2 imported modules ```pigpio``` and custom ```infrared```.

[rpi_ir](https://github.com/etfovac/rpi_ir) is maintained by [etfovac](https://github.com/etfovac).
