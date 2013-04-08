import json
import unittest
import time
from unittest import mock
from unittest.mock import call
from src.com.silospen.beerTemp.BeerTemp import BeerTemp
from src.com.silospen.beerTemp.heater.HeatingElement import HeatingElement
from src.com.silospen.beerTemp.logger.TempLogger import TempLogger
from src.com.silospen.beerTemp.provider.TempProvider import TempProvider

class BeerTempTest(unittest.TestCase):
    def testTestTempAndLog_withSingleProvider(self):
        tempProvider = TempProvider("sensorid")
        tempProvider.getTemp = mock.Mock(return_value=18.0)
        heatingElement = HeatingElement()
        tempLogger = TempLogger()
        tempLogger._write = mock.Mock()
        time.time = mock.Mock(return_value=1234)

        beerTemp = BeerTemp([tempProvider], heatingElement, tempLogger)
        beerTemp.testTempAndLog()
        self.assertTrue(heatingElement.isActive())
        tempLogger._write.assert_called_with(
            json.dumps({"active": True, "sensorId": "sensorid", "temp": 18.0, "time": 1234}))

        tempProvider.getTemp = mock.Mock(return_value=22.0)
        time.time = mock.Mock(return_value=5678)
        beerTemp.testTempAndLog()
        self.assertFalse(heatingElement.isActive())
        tempLogger._write.assert_called_with(
            json.dumps({"active": False, "sensorId": "sensorid", "temp": 22.0, "time": 5678}))

    def testTestTempAndLog_withSingleProvider_withNoneReturns(self):
        tempProvider = TempProvider("sensorid")
        tempProvider.getTemp = mock.Mock(return_value=None)
        heatingElement = HeatingElement()
        tempLogger = TempLogger()
        tempLogger._write = mock.Mock()
        time.time = mock.Mock(return_value=1234)

        beerTemp = BeerTemp([tempProvider], heatingElement, tempLogger)
        beerTemp.testTempAndLog()
        self.assertFalse(heatingElement.isActive())
        self.assertNotIn(call(json.dumps({"active": True, "sensorId": "sensorid", "temp": 18.0, "time": 5678})),
            tempLogger._write.mock_calls)

        tempProvider.getTemp = mock.Mock(return_value=22.0)
        time.time = mock.Mock(return_value=5678)
        beerTemp.testTempAndLog()
        self.assertFalse(heatingElement.isActive())
        tempLogger._write.assert_called_with(
            json.dumps({"active": False, "sensorId": "sensorid", "temp": 22.0, "time": 5678}))

    def testTestTempAndLog_withMultipleProviders(self):
        tempProvider1 = TempProvider("sensorid1")
        tempProvider1.getTemp = mock.Mock(return_value=18.0)
        tempProvider2 = TempProvider("sensorid2")
        tempProvider2.getTemp = mock.Mock(return_value=22.0)
        tempProvider3 = TempProvider("sensorid3")
        tempProvider3.getTemp = mock.Mock(return_value=21.0)

        heatingElement = HeatingElement()
        tempLogger = TempLogger()
        tempLogger._write = mock.Mock()
        time.time = mock.Mock(return_value=1234)

        beerTemp = BeerTemp([tempProvider1, tempProvider2, tempProvider3], heatingElement, tempLogger)
        beerTemp.testTempAndLog()
        self.assertFalse(heatingElement.isActive())
        calls = [call.write(json.dumps({"active": False, "sensorId": "sensorid1", "temp": 18.0, "time": 1234})),
                 call.write(json.dumps({"active": False, "sensorId": "sensorid2", "temp": 22.0, "time": 1234})),
                 call.write(json.dumps({"active": False, "sensorId": "sensorid3", "temp": 21.0, "time": 1234}))]
        tempLogger._write.assert_has_calls(calls)

        tempProvider3.getTemp = mock.Mock(return_value=19.8)
        time.time = mock.Mock(return_value=5678)
        beerTemp.testTempAndLog()
        self.assertTrue(heatingElement.isActive())
        calls = [call.write(json.dumps({"active": True, "sensorId": "sensorid1", "temp": 18.0, "time": 5678})),
                 call.write(json.dumps({"active": True, "sensorId": "sensorid2", "temp": 22.0, "time": 5678})),
                 call.write(json.dumps({"active": True, "sensorId": "sensorid3", "temp": 19.8, "time": 5678}))]
        tempLogger._write.assert_has_calls(calls)


    def testTempAndLog_withMultipleProviders_oneAmbient(self):
        tempProvider1 = TempProvider("28-000004a2bb68")
        tempProvider1.getTemp = mock.Mock(return_value=18.0)
        tempProvider2 = TempProvider("sensorid2")
        tempProvider2.getTemp = mock.Mock(return_value=180.0)
        tempProvider3 = TempProvider("sensorid3")
        tempProvider3.getTemp = mock.Mock(return_value=18.0)

        heatingElement = HeatingElement()
        tempLogger = TempLogger()
        tempLogger._write = mock.Mock()
        time.time = mock.Mock(return_value=1234)

        beerTemp = BeerTemp([tempProvider1, tempProvider2, tempProvider3], heatingElement, tempLogger)
        beerTemp.testTempAndLog()
        self.assertFalse(heatingElement.isActive())