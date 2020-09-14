#!/usr/bin/env python3
# Monitor, capture and decode InfraRed signal (of an IR remote controller) 
# Version:  v1.0
# Author: Nikola Jovanovic
# Date: 13.09.2020.
# Repo: https://github.com/etfovac/rpi_ir
# SW: Python 3.7.3
# HW: Pi Model 3B  V1.2, IR kit: Rx sensor module HX1838, Tx = IR remote(s)
import sys
import datetime
import signal
import pigpio
import infrared

IR_PIN = 17 # Board=11, BCM=17

def main():
    print("IR Rx @ {}: Setup Started".format(IR_PIN))

    model_map = {}
    
    def interrupt_signal_handler(signum, frame):
        print('Interrupt signal ' + str(signum) +
                      ' on line ' + str(frame.f_lineno) +
                      ' in ' + frame.f_code.co_filename)
        pi.stop()
        sys.exit(0)

    def ir_rx_callback(ir_decoded, ir_hex, model, valid):
        print("ir_decoded={} len={}".format(ir_decoded, len(ir_decoded)))
        print("ir_dec_hex={}".format(ir_hex))
        if valid:
            print("Valid IR code! Pressed button was of IR remote model {}: ".format(model))
            key = input()
            if model in model_map:
                btn_map = model_map[model]
            else:
                btn_map = {}
            btn_map[key] = {ir_decoded, ir_hex}
            model_map[model] = btn_map
            print(model_map)

    pi = pigpio.pi()
    ir_rec = infrared.rx(pi, IR_PIN, ir_rx_callback, 5)
    print("IR Rx @ {}: Setup Done ({})".format(IR_PIN, datetime.datetime.now()))
    print("IR Rx @ {}: Waits for IR signal... (Ctrl+C to exit)".format(IR_PIN))

    signal.signal(signal.SIGINT, interrupt_signal_handler) #Terminal interrupt signal
    signal.pause()
       
if __name__ == "__main__":
    main()