import mysql.connector
import requests
import argparse
import time


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


def main():
    parser = argparse.ArgumentParser(description='A tutorial of argparse!')
    parser.add_argument("-db", default="db", help="This is the 'a' variable")
    parser.add_argument("-sensor")

    args = parser.parse_args()

    roof_sensor = Satellite(str(args.sensor))
    server = Database(str(args.db))

    while True:
        try:
            server.saveTemperature(roof_sensor.getTemperature())
            server.saveHumidity(roof_sensor.getHumidity())
        except:
            print("Sensor not found")
        time.sleep(5)


if __name__ == "__main__":
    main()
