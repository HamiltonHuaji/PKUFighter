from microbit import *
import joypad
import struct
addr = [0x16,0x17]

stickxy_base_lx, stickxy_base_ly = joypad.stickxy(addr[0])
stickxy_base_rx, stickxy_base_ry = joypad.stickxy(addr[1])

max_diff = 500

# [lx, ly, rx, ry, lu, ld, ll, lr, ru, rd, rl, rr]

def diff(var, base):
    if var - base > max_diff:
        print("2", end="")
    elif var - base < -max_diff:
        print("0", end="")
    else:
        print("1", end="")

def raw_in():
    global stickxy_base_lx, stickxy_base_ly, stickxy_base_rx, stickxy_base_ry
    lx, ly, rx, ry = joypad.stickxy(addr[0]) + joypad.stickxy(addr[1])
    diff(lx, stickxy_base_lx)
    diff(ly, stickxy_base_ly)
    diff(rx, stickxy_base_rx)
    diff(ry, stickxy_base_ry)
    keys = [ls, lu, ld, ll, lr, rs, ru, rd, rl, rr] = joypad.keys(addr[0]) + joypad.keys(addr[1])
    for k in keys:
        print(k,end="")
    print("",end="\n")

display.scroll("PKU FIGHTER")

def wait_for_cmd():
    pass

while True:
    raw_in()
    sleep(50)
