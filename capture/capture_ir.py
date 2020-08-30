# Monitor, capture and decode InfraRed signal (of an IR remote controller) 
# Version:  v1.0
# Author: Nikola Jovanovic
# Date: 30.08.2020.
# Repo: https://github.com/etfovac/rpi_ir
# SW: Python 3.7.3
# HW: Pi Model 3B  V1.2, IR kit:Rx sensor module HX1838, IR Tx = IR remote(s)

import RPi.GPIO as GPIO
# import multiprocessing
import datetime
import signal                   
import sys
# import matplotlib.pyplot as pplot

# Globals
IR_PIN = 11 # Board=11, BCM=17
cntr = 0
ts = datetime.datetime.timestamp(datetime.datetime.now())
ir_signal = []
ir_decoded = ""
ir_data_duration = 0
# Header pulse and gap durations [us]
header = {'NEC':[9000,4500], 'Yamaha':[9067,4393]}
# End of message gap duration [us]
stop = {'NEC':40000,'Yamaha':39597}
bit0 = {'NEC':[562.5,562.5], 'Yamaha':[642,1600]}
bit1 = {'NEC':[562.5,1687.5], 'Yamaha':[642,470]}
# Repeat codes pulse, gap and pulse [us]
repeat = {'NEC':[9000,2250,562.5], 'Yamaha':[9065,2139]}
tolerance = {'down':0.9, 'up':1.1, 'no':1} # custom tweak
ir_remote = 'NEC'
ir_format = {
    'header' : header[ir_remote],
    'bit0' : bit0[ir_remote],
    'bit1' : bit1[ir_remote],
    'stop' : stop[ir_remote],
    'repeat' : repeat[ir_remote]
     }
# Notes: IR signal is valid only if Last was 0, and num of edges >34
# Header: (NEC)
#        Edge 0 diff_ts_us > 9 ms (pulse)
#        Edge 1 diff_ts_us > 4.5 ms (gap)
# Bits: (NEC)
#       Logical 0: 0.5625 (pulse) +  0.5625 (gap) = 1.125 ms
#       Logical 1: 0.5625 (pulse) +  3*0.5625 (gap) = 2*1.125 = 2.250 ms
        
def IR_event_Callback(pin): # IR_PIN is not used, but the callback requires a param
    global cntr, ts, ir_signal, ir_decoded, ir_data_duration
    # Readout last timestamp
    new_ts = datetime.datetime.timestamp(datetime.datetime.now())
    diff_ts_us =  (new_ts - ts)*1e6 # to microseconds, us
    ts = new_ts
    if diff_ts_us < 72000*tolerance['up']: # 9+4.5+32*2.25+40 = 125.5, 32*2.25=72 (longest case)
        # TODO: improve condition to log repeat codes and handle button debouncing better
        ir_signal.append(diff_ts_us)
        if diff_ts_us > ir_format['stop']*tolerance['down']:
            #print(ir_decoded)
            if len(ir_decoded) > 0:
                print(ir_decoded+" bit num: "+str(len(ir_decoded))+" hex: "+str(hex(int(ir_decoded,2)))+" dt="+str(ir_data_duration)+"us")
            else:
                print("IR Rx @ {}: Empty command.".format(IR_PIN))
        else:
            if len(ir_signal)>2:
                #print(ir_signal)
                decode(diff_ts_us)
                print(" Edge {} | {}".format(cntr,diff_ts_us)) 
            cntr=cntr+1
            ir_data_duration += diff_ts_us
    else:
        last(diff_ts_us)
        reset()
        
def decode(diff_ts_us):
    global ir_decoded, ir_signal 
    if ir_signal[0] > ir_format['header'][0]*tolerance['down'] and ir_signal[0] < ir_format['header'][0]*tolerance['up']:
        if ir_signal[1] > ir_format['header'][1]*tolerance['down'] and ir_signal[1] < ir_format['header'][1]*tolerance['up']:
            if diff_ts_us > sum(ir_format['bit0'])*tolerance['down']:
                if diff_ts_us > sum(ir_format['bit1'])*tolerance['down']:
                    ir_decoded+="1"
                else:
                    ir_decoded+="0"
                    # > 1.125*0.8 and < 2*1.125*0.8, ie > 0.9 and < 1.8
            else:
                ir_decoded+="0" # < 1.125*0.8
    
def last(diff_ts_us):
    print("IR Rx @ {}: State {} after {} s".format(IR_PIN,GPIO.input(IR_PIN),diff_ts_us/1e6))
    print("IR Rx @ {}: Edges detected:".format(IR_PIN))    

def reset():
    global cntr, ts, ir_signal, ir_decoded, ir_data_duration
    # Reset counter and count new edges
    cntr = 0
    ir_signal = []
    ir_decoded = ""
    ir_data_duration = 0
#             # plot ir_signal for benchmarking against piscope (terminal: 'piscope &')
#             # TODO: move plotting to other thread
#             # TODO: log to file
#             pplot.plot(ir_signal[0,2:], ones([1,64-2])) # no all 1
#             #remove first edge (pause between succ signals)
#             pplot.xlabel('Time [ms]')
#             pplot.ylabel('Edges')
#             pplot.title('Captured IR signal')
#             pplot.show()

def setup():
    print("IR Rx @ {}: Setup Started".format(IR_PIN))
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(IR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.remove_event_detect(IR_PIN)
    GPIO.add_event_detect(IR_PIN, GPIO.BOTH, bouncetime=1)
    GPIO.add_event_callback(IR_PIN,  IR_event_Callback)
    print("IR Rx @ {}: Setup Done".format(IR_PIN))
    print("IR Rx @ {}: Waits for IR signal".format(IR_PIN))

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

if __name__ == "__main__":
    
    setup()
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
