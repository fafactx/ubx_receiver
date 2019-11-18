#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 
Marcus Voß (m.voss@laposte.net)

Description:
Library for communication with the ublox F9T receiver
Example for storing received messages in json format
"""


from ubx_receiver import UBX_receiver, UBX_message, NMEA_message
import time
import json
import itertools
import os 


msgID = itertools.count()
dir_path = os.path.dirname(os.path.realpath(__file__))

receiver = UBX_receiver("COM3", 115200)
receiver.ubx_config_disable_all()
receiver.ubx_config_enable("GGA_UART1","SFRBX_UART1", "RAWX_UART1")
with open(os.path.join(dir_path,"output.o"), "w") as file:
    try:
        while True:
            try:
                msg = receiver.parse()
                if (isinstance(msg, str)):
                    print(f"error: {msg}")
                elif (isinstance(msg, UBX_message)):
                    print(msg)
                    constructed_message = {
                                "msgID": next(msgID),
                                "type": "GNSS",
                                "protocol": "UBX",
                                "timestamp": time.time(),
                                "class": msg.cl,
                                "id": msg.id,
                                "payload": list(msg.payload),
                                "raw": list(msg.raw_data)
                            }
                    file.write(json.dumps(constructed_message)+"\n")
                    file.flush()
                elif (isinstance(msg, NMEA_message)):
                    print(msg)
                    constructed_message = {
                                "msgID": next(msgID),
                                "type": "GNSS",
                                "protocol": "NMEA",
                                "timestamp": time.time(),
                                "talker": msg.talker_id+msg.msg_type,
                                "data": msg.data,
                                "raw": msg.raw_data
                            }
                    file.write(json.dumps(constructed_message)+"\n")
                    file.flush()
            except (ValueError, IOError) as err:
                print(err)

    finally:
        del receiver #clean up serial connection