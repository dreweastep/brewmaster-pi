import time
import board
import adafruit_dht
import paho.mqtt.client as mqtt
import subprocess
import signal
import json
import os
from datetime import datetime as dt


# check to see if process that produced play back bug is in the process list
# then kills that process
process_name = "libgpiod_pulsei"
proc = subprocess.Popen(["pgrep", process_name], stdout = subprocess.PIPE)

# Kill
for pid in proc.stdout:
    os.kill(int(pid), signal.SIGKILL)
    # Check if the process that we killed is alive.    

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D18)

# creating client instance of mqtt
mqttc = mqtt.Client()


while True:
    try:
        mqttc.connect("127.0.0.1", 1883, 60)
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(temperature_f, temperature_c, humidity))
        
        t = {
            "temperature": str(temperature_f),
            "timestamp": str(dt.now())
        }
        
        h = {
            "humidity": str(humidity),
            "timestamp": str(dt.now())
        }
        
        temp_json = json.dumps(t)
        humi_json = json.dumps(t)
        
        mqttc.publish("temp", temp_json);
        mqttc.publish("humid", humi_json);


    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])

    time.sleep(10)

