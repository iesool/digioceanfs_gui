#!/usr/bin/env python

import sys
import serial
import time
import string

cmd_dict = { 'Q'   : "%c%c"%(0x51,0x0D),
             'Q1'  : "%c%c%c"%(0x51,0x31,0x0D),
             'Q4'  : "%c%c%c"%(0x51,0x34,0x0D),
             'Q6'  : "%c%c%c"%(0x51,0x36,0x0D),
             'S2'  : "%c%c%c"%(0x53,0x32,0x0D) }

#cmd_fnp  = { 'Q'  : None,
#             'Q1' : format_Q1,
#             'Q4' : '',
#             'Q6' : '',
#             'S2' : ''}

UPS_STATUS = {  0 : ["Reserved", "Reserved"],
                2 : ["", "Shutdown Active"],
                4 : ["", "Test in Progress"], 
                8 : ["UPS On-line", "UPS is Standby"],
               16 : ["", "UPS Failed"],
               32 : ["Boost Active", "Bypass Active"],
               64 : ["", "Battery Low"],
              128 : ["","Utility Fail"]}

def shutdown_active(status):
    if (status & 2) == 0 :
        return 0
    else:
        return 1

def test_in_progress(status):
    if (status & 4) == 0 :
        return 0
    else:
        return 1

def ups_type_standby(status):
    if (status & 8) == 0 :
        return 0
    else:
        return 1

def ups_failed(status):
    if (status & 16) == 0 :
        return 0
    else:
        return 1

def ups_bypass_active(status):
    if (status & 32) == 0 :
        return 0
    else:
        return 1

def battery_low(status):
    if (status & 64) == 0 :
        return 0
    else:
        return 1

def utility_fail(status):    
    if (status & 128) == 0 :
        return 0
    else:
        return 1
    
def ups_float(st):
    try:
        st = float(st)
    except:
        st = st
    finally:
        return st

def ups_int(st, sys = 10):
    try:
        st = int(st, sys)
    except:
        st = st
    finally:
        return st

def need_power_off(Q1_rt):
    try:
        if Q1_rt["UPS Status"][6] == "Utility Fail":
            if Q1_rt["UPS Status"][5] == "Battery Low":
                return True
    except:
        return
    
    return False

def format_Q1(st):
    try: 
        st  = st.split("(")
        arr = st[1].split(" ")
        Q1_rt = {}
        
        Q1_rt["I/P voltage(V)"]       = ups_float(arr[0])
        Q1_rt["I/P fault voltage(V)"] = ups_float(arr[1])
        Q1_rt["O/P voltage(V)"]       = ups_float(arr[2])
        if (type(ups_float(arr[3])) == str):
            Q1_rt["O/P load(%)"] = arr[3]
        else:
            Q1_rt["O/P load(%)"] = float(arr[3])/100
        Q1_rt["I/P frequency(Hz)"]    = ups_float(arr[4])
        Q1_rt["Battery voltage(V)"]   = ups_float(arr[5])
        Q1_rt["Temperature(C)"]       = ups_float(arr[6])
        Q1_rt["UPS Status"]           = ["","","","","","",""]

        status                         = ups_int(arr[7],2)
        if type(status) == int:
            Q1_rt["UPS Status"][0] = UPS_STATUS[2][shutdown_active(status)]
            Q1_rt["UPS Status"][1] = UPS_STATUS[4][test_in_progress(status)]
            Q1_rt["UPS Status"][2] = UPS_STATUS[8][ups_type_standby(status)]
            Q1_rt["UPS Status"][3] = UPS_STATUS[16][ups_failed(status)]
            Q1_rt["UPS Status"][4] = UPS_STATUS[32][ups_bypass_active(status)]
            Q1_rt["UPS Status"][5] = UPS_STATUS[64][battery_low(status)]
            Q1_rt["UPS Status"][6] = UPS_STATUS[128][utility_fail(status)]

        #print Q1_rt # Debug
        return Q1_rt
    except:
        print "Invalid data received!"
        return

def format_Q4(st):
    try: 
        st    = st.split("(")
#        print st # Debug
        arr   = st[1].split(" ")
#        print arr # Debug
        Q4_rt = {}
        
        Q4_rt["I/P voltage(V)"]         = ups_float(arr[0])
        Q4_rt["MAX I/P voltage(V)"]     = ups_float(arr[1])
        Q4_rt["MIN I/P voltage(V)"]     = ups_float(arr[2])
        Q4_rt["PREV switch voltage(V)"] = ups_float(arr[3])
        Q4_rt["O/P voltage(V)"]         = ups_float(arr[4])
        
        if (type(ups_float(arr[5])) == str):
            Q4_rt["O/P current(%)"] = arr[5]
        else:
            Q4_rt["O/P current(%)"] = float(arr[5])/100

        if (type(ups_float(arr[6])) == str):
            Q4_rt["O/P load(%)"] = arr[6]
        else:
            Q4_rt["O/P load(%)"] = float(arr[6])/100
            
        Q4_rt["O/P frequency(Hz)"]      = ups_float(arr[7])
        Q4_rt["+BUS voltage(V)"]        = ups_float(arr[8])
        Q4_rt["-BUS voltage(V)"]        = ups_float(arr[9])
        Q4_rt["Battery voltage"]        = ups_float(arr[10])
        Q4_rt["Temperature(C)"]         = ups_float(arr[11])
        Q4_rt["UPS Status"]             = arr[12]
        
        #print Q4_rt # Debug
        return Q4_rt
    except:
        print "Invalid data received!"
        return

def format_Q6(st):
    try: 
        st    = st.split("(")
#        print st # Debug
        arr   = st[1].split(" ")
 #       print arr # Debug
        Q6_rt = {}
        
        Q6_rt["Main I/P voltage(V)"]            = ups_float(arr[0])
        Q6_rt["Main I/P voltage(V)"]            = ups_float(arr[1])
        Q6_rt["Main I/P voltage(V)"]            = ups_float(arr[2])
        Q6_rt["Main I/P frequency(Hz)"]         = ups_float(arr[3])
        Q6_rt["O/P voltage(V)"]                 = ups_float(arr[4])
        Q6_rt["O/P voltage(V)"]                 = ups_float(arr[5])
        Q6_rt["O/P voltage(V)"]                 = ups_float(arr[6])
        Q6_rt["O/P frequency(Hz)"]              = ups_float(arr[7])

        if (type(ups_float(arr[8])) == str):
            Q6_rt["Output Current(%)"] = arr[8]
        else:
            Q6_rt["Output Current(%)"] = float(arr[8])/100

        if (type(ups_float(arr[9])) == str):
            Q6_rt["Output Current(%)"] = arr[9]
        else:
            Q6_rt["Output Current(%)"] = float(arr[9])/100

        if (type(ups_float(arr[10])) == str):
            Q6_rt["Output Current(%)"] = arr[10]
        else:
            Q6_rt["Output Current(%)"] = float(arr[10])/100

        Q6_rt["Positive Battery voltage(V)"] = ups_float(arr[11])
        Q6_rt["Negative Battery voltage(V)"] = ups_float(arr[12])
        Q6_rt["Temperature(C)"]              = ups_float(arr[13])
        Q6_rt["Estimated Runtime(s)"]        = ups_int(arr[14])

        if (type(ups_float(arr[15])) == str):
            Q6_rt["Battery Capacity Percentage(%)"] = arr[15]
        else:
            Q6_rt["Battery Capacity Percentage(%)"] = float(arr[15])/100

        Q6_rt["System Mode"]                    = ups_int(arr[16][:7], 2)
        Q6_rt["Status of Battery Test"]         = ups_int(arr[16][8:], 2)
        Q6_rt["Fault Code"]                     = arr[17]
        Q6_rt["Warnings"]                       = arr[18]

        #print Q6_rt # Debug
        return Q6_rt
    except Exception,e:
        print "Invalid data received!"
        print e
        return

def read_serial_data(ser, cmd = 'Q1'):
    ser.write(cmd_dict[cmd])
#    newstr = ser.read()

    newstr = []
    i      = 0
    while True:
        newchar           = ser.read()
        newstr.append(newchar)
        i = i + 1
        if len(newchar) == 0:
            print >> sys.stderr, "Read data Timeout!"
            break

        if newchar == '\r':
            break
    return ''.join(newstr)

def open_serial(port, timeout = 5):
    baudrate = 2400
    bytesize = serial.EIGHTBITS
    parity   = serial.PARITY_NONE
    stopbits = serial.STOPBITS_ONE
    
    ser      = serial.Serial(port, baudrate, bytesize, parity, stopbits, timeout)
#    time.sleep(1)
    return ser

def close_serial(ser):
    ser.close()
        
