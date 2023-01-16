#!/usr/bin/python3
# -- coding: utf-8 --
from bluepy import btle
import paho.mqtt.client as mqtt
import struct

_BLE_ADDRESS     = "C0:49:EF:D3:8E:16"
_SERVICE_UART      = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
_CHARACTERISTIC_RX = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
_CHARACTERISTIC_TX = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
cliente = mqtt.Client("ricardo")
cliente.connect("192.168.100.204",1883)

class data_driver(btle.DefaultDelegate):
    def _init_(self):
        btle.DefaultDelegate._init_(self)
    #
    def handleNotification(self, cHandle, data):
        data = struct.unpack("ff",data)
        cliente.publish('pizq',data[0])
        cliente.publish('pder',data[1])
        print(data[0],data[1])

def main():
    print("Conectando...")
    dev = btle.Peripheral(_BLE_ADDRESS)
    dev.setDelegate(data_driver())
    #
    service_uuid = btle.UUID(_SERVICE_UART)
    ble_service  = dev.getServiceByUUID(service_uuid)
    #
    uuidConfig = btle.UUID(_CHARACTERISTIC_RX)
    data_rx = ble_service.getCharacteristics(uuidConfig)[0]
    #
    
    #     
    while True:
        if dev.waitForNotifications(0.5):
            continue
        else:
            print("No hay datos nuevos")
#
if _name_ == '_main_':
    main()