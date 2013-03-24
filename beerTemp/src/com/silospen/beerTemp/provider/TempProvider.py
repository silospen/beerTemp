class TempProvider():
    PATH_SKELETON = "/sys/bus/w1/devices/{0}/w1_slave"

    def __init__(self, sensorId):
        self.sensorId = sensorId

    def getTemp(self):
        with TempProvider._rawTempHandle(self.PATH_SKELETON.format(self.sensorId)) as sensorInput:
            return self._parseRawTemp(sensorInput.read())

    def _parseRawTemp(self, sensorInput):
        return int(sensorInput.split("t=")[1]) / 1000.

    @staticmethod
    def _rawTempHandle(sensorPath):
        return open(sensorPath)
