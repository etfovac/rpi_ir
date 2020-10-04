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
import os
from load_ir_file import parse_ir_to_dict, find_key

IR_PIN = 17 # Board=11, BCM=17

def main():
    
    def interrupt_signal_handler(signum, frame):
        print('Interrupt signal ' + str(signum) +
                      ' on line ' + str(frame.f_lineno) +
                      ' in ' + frame.f_code.co_filename)
        pi.stop()
        sys.exit(0)

    def ir_rx_callback(ir_decoded, ir_hex, model, valid, track, log):
        print("ir_decoded={} len={}".format(ir_decoded, len(ir_decoded)))
        print("ir_dec_hex={}".format(ir_hex))
        if valid:
            print("Valid IR code (remote model \"{}\") captured @ {} \n".format(model,datetime.datetime.now()))
            filepath = "ir_code_"+str(model)+".txt"
            if track:
                key = input("Enter key ID for this code: [\"skip\" to skip] ")
                if key != "skip":
                    if model in ir_dict:
                        btn_dict = ir_dict[model]
                    else:
                        btn_dict = {}
                    btn_dict[key] = {ir_decoded, ir_hex}
                    ir_dict[model] = btn_dict
                    print(ir_dict)
                    if log:
                        f = open(filepath, "w")
                        f.write(str(ir_dict[model]))
                        f.close()
                        print("IR code dictionary written to file: {}\n".format(filepath))
            else:
                if os.path.exists(filepath):
                    f = open(filepath, "r")
                    ir_model_rd = f.read()
                    f.close()
                    btn_dict = parse_ir_to_dict(ir_model_rd)
                    print("Key decoded: {}".format(find_key(btn_dict, ir_hex)))
                else: print("IR code dictionary file not found. Turn on logging to create it.")
        idle()
 
    def idle():
        print("\nIR Rx @ {}: Idle... (Ctrl+C to exit) \n".format(IR_PIN))
    
    # Setup tracking and logging
    print("IR Rx @ {}: Setup Started".format(IR_PIN))
    track = (lambda x: x == 'y' or x == 'Y')(input("IR Rx @ {}: Turn tracking on? [y/n] ".format(IR_PIN)))
    #print("IR Rx @ {}: Tracking on: {}".format(IR_PIN, track))
    log = False
    if track:
        log = (lambda x: x == 'y' or x == 'Y')(input("IR Rx @ {}: Turn logging on? [y/n] ".format(IR_PIN)))
        #print("IR Rx @ {}: Logging on: {}".format(IR_PIN, log))
        ir_dict = {}
    
    # Setup IR Receiver Callback
    pi = pigpio.pi()
    ir_rec = infrared.rx(pi, IR_PIN, ir_rx_callback, track, log) #timeout=5ms, see infrared.py
    print("IR Rx @ {}: Setup Done @ {}".format(IR_PIN, datetime.datetime.now()))
    idle()
    
    # Setup Terminal interrupt signal SIGINT for Ctrl+C
    signal.signal(signal.SIGINT, interrupt_signal_handler)
    signal.pause()
    
# main END
       
if __name__ == "__main__":
    main()