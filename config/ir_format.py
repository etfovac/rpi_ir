#!/usr/bin/env python3
# Monitor, capture and decode InfraRed signal (of an IR remote controller) 
# Version:  v1.0
# Author: Nikola Jovanovic
# Date: 13.09.2020.
# Repo: https://github.com/etfovac/rpi_ir
# SW: Python 3.7.3
# HW: Pi Model 3B  V1.2, IR kit: Rx sensor module HX1838, Tx = IR remote(s)

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
    'repeat' : repeat[ir_remote],
    'data_len': 32
     }
# Notes: IR signal is valid only if Last was 0, and num of edges >34
# Header: (NEC)
#        Edge 0 diff_ts_us > 9 ms (pulse)
#        Edge 1 diff_ts_us > 4.5 ms (gap)
# Bits: (NEC)
#       Logical 0: 0.5625 (pulse) +  0.5625 (gap) = 1.125 ms
#       Logical 1: 0.5625 (pulse) +  3*0.5625 (gap) = 2*1.125 = 2.250 ms