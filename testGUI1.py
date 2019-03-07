from PyQt5 import QtCore, QtWidgets, QtGui, Qt, uic
import sys
import time
from os import path
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import threading
from PyQt5.QtCore import QThread, pyqtSignal, QPropertyAnimation
#import RPi.GPIO as GPIO

qtCreatorFile = "RocketGUI1.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

HOST = "192.168.0.10"
port = 1883
TOPIC_1 = "RELAY"
TOPIC_2 = "DATA"
TOPIC_3 = "STATE" 
counter = 1

mqtt_client = mqtt.Client()
mqtt_client.connect(HOST, port=port, keepalive=60)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN)
GPIO.setup(16, GPIO.IN)
GPIO.setup(18, GPIO.IN)
GPIO.setup(36, GPIO.IN)

def lox_mpv(channel):
    if GPIO.input(36):
        mqtt_client.publish(TOPIC_1,b'LOX_MPV_OPEN')
    else:
        mqtt_client.publish(TOPIC_1,b'LOX_MPV_CLOSE')

def ch4_mpv(channel):
    if GPIO.input(18):
        mqtt_client.publish(TOPIC_1,b'CH4_MPV_OPEN')
    else:
        mqtt_client.publish(TOPIC_1,b'CH4_MPV_CLOSE')

def ignitor(channel):
    if GPIO.input(16):
        mqtt_client.publish(TOPIC_1,b'IGNITOR_ON')
    else:
        mqtt_client.publish(TOPIC_1,b'IGNITOR_OFF')

def launch(channel):
    if GPIO.input(12):
        mqtt_client.publish(TOPIC_1,b'LAUNCH')
    else:
        mqtt_client.publish(TOPIC_1,b'ABORT')

GPIO.add_event_detect(12, GPIO.BOTH, callback=launch)
GPIO.add_event_detect(16, GPIO.BOTH, callback=ignitor)
GPIO.add_event_detect(18, GPIO.BOTH, callback=ch4_mpv)
GPIO.add_event_detect(36, GPIO.BOTH, callback=lox_mpv)

class mainthread(QThread):
    STATEsignal = pyqtSignal('PyQt_PyObject')
    DATAsignal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        QThread.__init__(self)
        self.connect1()

    def connect1(self):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_message = self.subscrib1
        self.mqtt_client.connect(HOST, port=port, keepalive=60)
        self.mqtt_client.subscribe(TOPIC_2)
        self.mqtt_client.subscribe(TOPIC_3)
        self.mqtt_client.loop_start()
        print("connected")

    def subscrib1(self, mqtt_client, userdata, msg):
        if msg.topic == "DATA":
            D = str(msg.payload)[2:-1]
            C = (D.split(',')[0], D.split(',')[1], D.split(',')[2], D.split(',')[3])
            C = ('%4s' % C[0], '%4s' % C[1], '%4s' % C[2], '%4s' % C[3])
            self.DATAsignal.emit(C)
            print(C)
        if msg.topic == "STATE":
            B = str(msg.payload)[2:-1]
            A = (B.split(',')[0], B.split(',')[1], B.split(',')[2], B.split(',')[3], B.split(',')[4], B.split(',')[5], B.split(',')[6])
            A = ('%4s' % A[0], '%4s' % A[1], '%4s' % A[2], '%4s' % A[3], '%4s' % A[4], '%4s' % A[5], '%4s' % A[6],)
            self.STATEsignal.emit(A)

class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.mythread1 = mainthread()
        self.init_ui()
        self.mythread1.STATEsignal.connect(self.progress1)
        self.mythread1.DATAsignal.connect(self.progress2)        
        self.radioButton1.toggled.connect(self.radio1)
        self.radioButton2.toggled.connect(self.radio2)
        self.radioButton3.toggled.connect(self.radio3)
        self.checkBox.toggled.connect(self.radio4)

    def init_ui(self):
        self.mythread1.start()

    def progress1(self, A):
        self.Pressure_Key.setAutoFillBackground(True)
        self.Ign_Safety.setAutoFillBackground(True)
        self.MPV_Safety.setAutoFillBackground(True)
        self.MPV_Key.setAutoFillBackground(True)
        self.Ign_Key.setAutoFillBackground(True)
        try:
            if int(A[1]) == 1:
                p1 = self.Pressure_Key.palette()
                p1.setColor(self.Pressure_Key.backgroundRole(), Qt.red)
                self.Pressure_Key.setPalette(p1)
            if int(A[1]) == 0:
                p2 = self.Pressure_Key.palette()
                p2.setColor(self.Pressure_Key.backgroundRole(), Qt.white)
                self.Pressure_Key.setPalette(p2)
            if int(A[0]) == 1:
                p1 = self.Ign_Safety.palette()
                p1.setColor(self.Ign_Safety.backgroundRole(), Qt.red)
                self.Ign_Safety.setPalette(p1)
            if int(A[0]) == 0:
                p2 = self.Ign_Safety.palette()
                p2.setColor(self.Ign_Safety.backgroundRole(), Qt.white)
                self.Ign_Safety.setPalette(p2)
            if int(A[3]) == 1:
                p1 = self.MPV_Safety.palette()
                p1.setColor(self.MPV_Safety.backgroundRole(), Qt.red)
                self.MPV_Safety.setPalette(p1)
            if int(A[3]) == 0:
                p2 = self.MPV_Safety.palette()
                p2.setColor(self.MPV_Safety.backgroundRole(), Qt.white)
                self.MPV_Safety.setPalette(p2)
            if int(A[4]) == 1:
                p1 = self.MPV_Key.palette()
                p1.setColor(self.MPV_Key.backgroundRole(), Qt.red)
                self.MPV_Key.setPalette(p1)
            if int(A[4]) == 0:
                p2 = self.MPV_Key.palette()
                p2.setColor(self.MPV_Key.backgroundRole(), Qt.white)
                self.MPV_Key.setPalette(p2)
            if int(A[6]) == 1:
                p1 = self.Ign_Key.palette()
                p1.setColor(self.Ign_Key.backgroundRole(), Qt.red)
                self.Ign_Key.setPalette(p1)
            if int(A[6]) == 0:
                p2 = self.Ign_Key.palette()
                p2.setColor(self.Key.backgroundRole(), Qt.white)
                self.Ign_Key.setPalette(p2)
        except:
            pass

    def progress2(self, C):
        try:
            self.Readout0.display(C[0])
            self.Readout1.display(C[1])
            self.Readout2.display(C[2])
            self.Readout3.display(C[3])
            self.progressBar0.setValue(float(C[0]))
            self.progressBar1.setValue(float(C[1]))
            self.progressBar2.setValue(float(C[2]))
            self.progressBar3.setValue(float(C[3]))
            if float(C[0]) >= 4500:
                self.Readout0.setAutoFillBackground(True)
                p = self.Readout0.palette()
                p.setColor(self.Readout0.backgroundRole(), Qt.red)
                self.Readout0.setPalette(p)
                self.progressBar0.setValue(4500)
            if float(C[1]) >= 4500:
                self.Readout1.setAutoFillBackground(True)
                c = self.Readout1.palette()
                c.setColor(self.Readout1.backgroundRole(), Qt.red)
                self.Readout1.setPalette(c)
                self.progressBar1.setValue(150)
            if float(C[2]) >= 4500:
                self.Readout2.setAutoFillBackground(True)
                h = self.Readout2.palette()
                h.setColor(self.Readout2.backgroundRole(), Qt.red)
                self.Readout2.setPalette(h)
                self.progressBar2.setValue(150)
            if float(C[3]) >= 4500:
                self.Readout3.setAutoFillBackground(True)
                k = self.Readout3.palette()
                k.setColor(self.Readout3.backgroundRole(), Qt.red)
                self.Readout3.setPalette(k)
                self.progressBar3.setValue(150)
        except:
            pass

    def radio1(self):
        self.HE_Range.move(241,284)
        self.HE_Target.move(263,284)
        self.HE_T_Label.move(224,325)
        self.radioButton2.setChecked(False)
        self.radioButton3.setChecked(False)

    def radio2(self):
        self.HE_Range.move(747,284)
        self.HE_Target.move(769,284)
        self.HE_T_Label.move(713,325)
        self.radioButton1.setChecked(False)
        self.radioButton3.setChecked(False)

    def radio3(self):
        self.HE_Range.move(200,284)
        self.radioButton1.setChecked(False)
        self.radioButton2.setChecked(False)

    def radio4(self):
        self.progressBar3.hide()
        self.pstate_label_5.hide()
        self.Readout3.hide()
        self.label_5.hide()
        self.progressBar2.move(130, 365)
        self.Readout2.move(20, 350)
        self.label_4.move(130, 345)
        self.pstate_label_4.move(350, 330)
        self.pstate_label_3.move(350, 225)
        self.progressBar1.move(130, 265)
        self.label_3.move(130, 245)
        self.Readout1.move(20, 250)
        if self.checkBox.isChecked() == False:
            self.radio5()

    def radio5(self):
        self.progressBar3.show()
        self.pstate_label_5.show()
        self.Readout3.show()
        self.label_5.show()
        self.progressBar2.move(130, 325)
        self.Readout2.move(20, 310)
        self.label_4.move(130, 305)
        self.pstate_label_4.move(350, 290)
        self.pstate_label_3.move(350, 205)
        self.progressBar1.move(130, 245)
        self.label_3.move(130, 225)
        self.Readout1.move(20, 230)

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    '''t1 = threading.Thread(target=MainApp.switch_loop, args=(window, ))
    t1.start()'''
    app.exec_()

if __name__ == '__main__':
    main()
