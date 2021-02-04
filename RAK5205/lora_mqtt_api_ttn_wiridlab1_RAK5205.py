#!/usr/bin/python

# This shows a simple example of an MQTT subscriber.


import paho.mqtt.client as mqtt
import base64, json
import os
import datetime
import requests

#Please Complete te next information for WiridLab Platform API connection
TOKEN_API_WIRIDLAB='<YOUR_AUTHENTICATION_WIRIDLAB_TOKEN>'
NODE_NAME_WIRIDLAB= '<NODE_NAME_WIRIDLAB_PLATFORM>'

#Please complete the next information for MQTT connection
SERVER_TTN='<DNS_TTN_SERVER>' # EJ: us-west.thethings.network
ACCESS_KEY_TTN= '<TTN_APPLICATION_ACCESS_KEY>'
APPLICATION_ID='<APPLICATION_ID_TTN>'


def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

def on_message(mqttc, obj, msg):
    #print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    print('Mensaje --> Topic: {} \n'.format(msg.topic))
    x = msg.payload.decode("utf-8")
    y = json.loads(x)
    lora = y["metadata"]
    fields = y['payload_fields']
    gatew = y['metadata']['gateways']
    altit = fields.get('altitude', 'NA')
    barom = fields.get('barometer', 'NA')#['barometer']
    batte = fields.get('battery', 'NA')#['battery']
    gasre = fields.get('gasResistance', 'NA')#['gasResistance']
    humid = fields.get('humidity', 'NA')#['humidity']
    latit = fields.get('latitude', 'NA')#['latitude']
    longi = fields.get('longitude', 'NA')#['longitude']
    tempe = fields.get('temperature', 'NA')#['temperature']
    acelx = fields.get('acceleration_x', 'NA')#['acceleration_x']
    acely = fields.get('acceleration_y', 'NA')#['acceleration_y']
    acelz = fields.get('acceleration_z', 'NA')#['acceleration_z']
    frequ = lora['frequency']
    modul = lora['modulation']
    datar = lora['data_rate']
    airti = lora['airtime']
    codin = lora['coding_rate']
    grssi = gatew[0]['rssi']
    gsnr = gatew[0]['snr']
    gchan = gatew[0]['channel']


#    print("\nAcelerometro: \n\tX : {} \n\tY: {} \n\tZ: {} ".format(acele['x'],acele['y'],acele['z']))
#    print("\nTime : {} \n Temp : {} \n\tlatitud:{} \n\tlongitud: {} \n\taltitud: {}".format(time,temp,lat,lon,alt))

    #z = base64.b64decode(z).decode("utf-8")
    #print ('datos: {}'.format(z))
    print("Enviando datos a la API.....")
    jsonData = [{}]
    nodeName="test-panel-01"
    jsonData[0]["altitude_s"] = altit
    jsonData[0]["barometer_s"] = barom
    jsonData[0]["battery_s"] = batte
    jsonData[0]["gasResistance_s"] = gasre
    jsonData[0]["humidity_s"] = humid
    jsonData[0]["latitude_s"] = latit
    jsonData[0]["longitude_s"] = longi
    jsonData[0]["temperature_s"] = tempe
    jsonData[0]["acceleration_x_s"] = acelx
    jsonData[0]["acceleration_y_s"] = acely
    jsonData[0]["acceleration_z_s"] = acelz
    jsonData[0]['frequency_s'] = frequ
    jsonData[0]['modulation_s'] = modul
    jsonData[0]['data_rate_s'] = datar
    jsonData[0]['airtime_s'] = airti
    jsonData[0]['coding_rate_s'] = codin
    jsonData[0]['rssi_s'] = grssi
    jsonData[0]['snr_s'] = gsnr
    jsonData[0]['channel_s'] = gchan

    print (jsonData)
    jsonData = json.dumps(jsonData, indent=4)
    headers = {"WIRID-LAB-AUTH-TOKEN": TOKEN_API_WIRIDLAB, "Content-Type": "application/json"}
    info = requests.post("https://api.wiridlab.site/api/iot/devices/"+ NODE_NAME_WIRIDLAB.lower(), headers=headers, data=jsonData, timeout=None)
    data = info.json()

    if (info.status_code == 200):
        print ("  Request API")
        print(json.dumps(data, indent=4, sort_keys=True))
    else:
        print ("error enviando comunicacion")
        print(json.dumps(data, indent=4, sort_keys=True))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)


# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log
mqttc.username_pw_set(APPLICATION_ID, ACCESS_KEY_TTN)
mqttc.connect(SERVER_TTN, 1883, 30)
mqttc.subscribe("+/devices/+/up", 0)

mqttc.loop_forever()
