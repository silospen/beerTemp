import os
import logging

class TempProvider():
    PARENT_SENSOR_PATH = "/sys/bus/w1/devices/"
    SENSOR_PATH = PARENT_SENSOR_PATH + "{0}/w1_slave"
    LOG = logging.getLogger('TempProvider')

    def getId(self):
        return self._sensorId

    def getTemp(self):
        with TempProvider._rawTempHandle(self.SENSOR_PATH.format(self._sensorId)) as sensorInput:
            return self._parseRawTemp(sensorInput.read())

    def _parseRawTemp(self, sensorInput):
        return int(sensorInput.split("t=")[1]) / 1000.

    @staticmethod
    def _rawTempHandle(sensorPath):
        return open(sensorPath)

    #noinspection PyBroadException
    @classmethod
    def create(cls):
        sensors = []
        try:
            sensorList = cls._listSensors()
        except Exception as ex:
            cls.LOG.error(ex)
            return []

        for sensor in sensorList:
            sensors.append(TempProvider(sensor))
        return sensors
    @classmethod
    def _listSensors(cls):
        return os.listdir(cls.PARENT_SENSOR_PATH)

    def __init__(self, sensorId):
        self._sensorId = sensorId

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
