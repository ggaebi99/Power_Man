# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 21:56:24 2023

@author: ggaeb
"""

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import uic
import threading
import socket
import struct
import win32api

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))

form_class = uic.loadUiType("main.ui")[0]


mac = list()
f = open("Mac_Add.txt", 'r')
while(True):
    line = f.readline()
    if not line: break
    line = line.split(':')

    
    line[-1] = line[-1].replace("\n", "")
    mac.append(line[1:])
f.close()

def Shut_Down(num):
    num = num + 151
    print(num)
    ip = 'yourPC_IP.{0}'.format(num)
    message = "shutdown -s -f -t 0 -m "+ip+"\n"
    print(message)
    os.system(message)
    print("ip : "+ ip + "종료완료")

def Power_On(num):
    macAddr = "".join(mac[num])
    data = b'ffffffffffff' + (macAddr * 16).encode()
    send_data = b''
    for i in range(0, len(data), 2):
        send_data += struct.pack('B', int(data[i: i + 2], 16))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(send_data, ('YourBoardcastIP', 9))

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_SA.clicked.connect(self.toggle_checkboxes)
        self.btn_SD.clicked.connect(self.perform_action)
        self.CB_list = [getattr(self, f"CB_{i}") for i in range(1, 41)]

    def toggle_checkboxes(self):
        for cb in self.CB_list:
            cb.toggle()

    def perform_action(self):
        checked_boxes = [i for i, cb in enumerate(self.CB_list) if cb.isChecked()]

        if not checked_boxes:
            win32api.MessageBox(0, "체크를 하셔야 합니다.", "error", 16)
            return

        for num in checked_boxes:
            try:
                if self.btn_Off.isChecked():
                    t = threading.Thread(target=Shut_Down, args=(num,))
                elif self.btn_On.isChecked():
                    t = threading.Thread(target=Power_On, args=(num,))
                else:
                    win32api.MessageBox(0, "동작체크오류", "error", 16)
                    break
                t.start()
                t.join(1)
            except:
                win32api.MessageBox(0, f"{num+1}번 오류", "error", 16)
           
if __name__ == "__main__" :
    if s.getsockname()[0] == "MainPCIP":
        while(True):
            win32api.MessageBox(0, "MainPC가 아닙니다.", "MainPC가 아닙니다.", 16)
    app = QApplication(sys.argv)

    myWindow = WindowClass()

    myWindow.show()

    app.exec_()