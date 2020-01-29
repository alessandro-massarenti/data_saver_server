import mysql.connector
import requests
import argparse


class Database:
    def __init__(self, host):
        self.__server = mysql.connector.connect(
            host=host,
            user="sensingStation",
            passwd="8mUdOIU9I8Ws5Kc6",
            database="sensingStation"
        )

    def __getCursor(self):
        self.__cursor = self.__server.cursor(prepared=True)

    def __saveData(self, signature, value: float):
        sql = "INSERT INTO data (sensor_signature, value) VALUES (%s, %s)"
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

    roof_sensor = Satellite(args.sensor)
    server = Database(args.db)

    server.saveTemperature(roof_sensor.getTemperature())
    server.saveHumidity(roof_sensor.getHumidity())


if __name__ == "__main__":
    main()
