#!/usr/bin/python3
import sys
import time
from PyQt5 import QtCore, QtWidgets, QtGui, Qt, uic
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from PyQt5.QtGui import QTextCursor

piAddress = "192.168.0.10"

HOST = piAddress
TOPIC_1 = "RELAY"
TOPIC_2 = "DATA"
TOPIC_2 = "STATE"

print('Imported Packages and Starting Launch VI')

qtCreatorFile = "RocketGUI.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.connection_status = False
        self.initUI()

    def initUI(self):
        print('initUI')
        self.p3_zero.clicked.connect(self.testP4T)

    def testP4T(self):
        self.Readout0.display(v0)
        self.Readout1.display(v1)
        self.Readout2.display(v2)
        self.Readout3.display(v3)
        self.Readout4.display(v4)
        self.Readout5.display(v5)
        self.Readout6.display(v6)
        self.Readout7.display(v7)
        self.Readout8.display(v8)
        self.Readout9.display(v9)

    def on_message(client, userdata, msg):
        calldata(str(msg.payload))

    def calldata(data):
        A = data.split(',')
        v0 = A[0]
        v1 = A[1]
        v2 = A[2]
        v3 = A[3]
        v4 = A[4]
        v5 = A[5]
        v6 = A[6]
        v7 = A[7]
        v8 = A[8]
        v9 = A[9]

    def on_connect(client,userdata,flags,rc):

        print("Connected with result code "+str(rc))
        client.subscribe(TOPIC_3)
        client.subscribe(TOPIC_2)
        error = rc
        return error

    def on_disconnect(client, userdata,rc=0):
        print("Connection Lost.")
        client.loop_stop()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.connect(HOST, 3300, 60)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()