import threading
import serial
import time
import struct
'''
以下变量是标注按键状态, l前缀表示左边的手柄, r前缀表示右边的手柄
后缀为x, y的取值-1, 0, 1表示左, 不动, 右 / 上, 不动, 下
u(up)
d(down)
l(left)
r(right)
后缀取值0, 1表示按下/不按

实例化一个Joypad, 传入"COM3"或"COM4"表示microbit接的usb口
'''
lx = 0
ly = 0
rx = 0
ry = 0
ls = 0
lu = 0
ld = 0
ll = 0
lr = 0
rs = 0
ru = 0
rd = 0
rl = 0
rr = 0

# class event:
#     pass

ser = None

def readf():
    global ser
    global lx
    global ly
    global rx
    global ry
    global ls
    global lu
    global ld
    global ll
    global lr
    global rs
    global ru
    global rd
    global rl
    global rr
    print("game starts!")
    if ser.isOpen():
        # while True:
        st = ser.readline().decode("ascii")
        print(len(st))
        try:
            lx = int(st[0]) - 1
            ly = int(st[1]) - 1
            rx = int(st[2]) - 1
            ry = int(st[3]) - 1
            ls = int(st[4])
            lu = int(st[5])
            ld = int(st[6])
            ll = int(st[7])
            lr = int(st[8])
            rs = int(st[9])
            ru = int(st[10])
            rd = int(st[11])
            rl = int(st[12])
            rr = int(st[13])
        except ValueError as e:
            print(e)
            print(st)

class Joystick:
    '''
    port is something like 'COM3' or 'COM4'
    '''
    def __init__(self, port):
        global ser
        ser = serial.Serial(port, 115200)
        assert ser.isOpen()
        # self.thread = threading.Thread(target = readf)
        # self.thread.start()