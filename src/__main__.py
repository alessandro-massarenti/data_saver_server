import argparse
import time
from threading import Thread
import _thread

import mysql.connector
import requests


class Database:
    def __init__(self, host: str):
        self.__server = mysql.connector.connect(
            host=host,
            user="sensingstation",
            passwd="8mUdOIU9I8Ws5Kc6",
            database="sensingstation"
        )
        self.__cursor = self.__server.cursor(prepared=True)

    def __saveData(self, signature, value: float):
        sql = "INSERT INTO data (sensorsignature, value) VALUES (%s, %s)"
        val = (signature, value)
        self.__cursor.execute(sql, val)
        self.__server.commit()

    def saveTemperature(self, temperature: float):
        self.__saveData("T1", temperature)

    def saveHumidity(self, humidity: float):
        self.__saveData("H1", humidity)


class Satellite:
    def __init__(self, url: str):
        self.url = url

    def getTemperature(self):
        return requests.get(self.url).json()['data']['temperature']

    def getHumidity(self):
        return requests.get(self.url).json()['data']['humidity']


def data_grappler(server, sensor,num):
    while True:
        try:
            server.saveTemperature(sensor.getTemperature())
            server.saveHumidity(sensor.getHumidity())
            print("Dato letto")
            print(num)
        except:
            print("Sensor not found")
        time.sleep(3)


def main():
    parser = argparse.ArgumentParser(description='A tutorial of argparse!')
    parser.add_argument("-db", default="db", help="This is the 'a' variable")
    parser.add_argument("-sensor")

    args = parser.parse_args()

    server = Database(str(args.db))
    roof_sensor = Satellite(str(args.sensor))

    _thread.start_new_thread(data_grappler, (server, roof_sensor, 1))

    # Keep program alive
    while True:
        time.sleep(5)


if __name__ == "__main__":
    main()
