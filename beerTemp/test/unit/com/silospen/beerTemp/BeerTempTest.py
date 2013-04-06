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
        tempLogger._write.assert_called_with("1234\tsensorid\t18.0\t1\n")

        tempProvider.getTemp = mock.Mock(return_value=22.0)
        time.time = mock.Mock(return_value=5678)
        beerTemp.testTempAndLog()
        self.assertFalse(heatingElement.isActive())
        tempLogger._write.assert_called_with("5678\tsensorid\t22.0\t0\n")

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
        calls = [call._write("1234\tsensorid1\t18.0\t0\n"), call._write("1234\tsensorid2\t22.0\t0\n"),
                 call._write("1234\tsensorid3\t21.0\t0\n")]
        tempLogger._write.assert_has_calls(calls)

        tempProvider3.getTemp = mock.Mock(return_value=18.8)
        time.time = mock.Mock(return_value=5678)
        beerTemp.testTempAndLog()
        self.assertTrue(heatingElement.isActive())
        calls = [call._write("5678\tsensorid1\t18.0\t1\n"), call._write("5678\tsensorid2\t22.0\t1\n"),
                 call._write("5678\tsensorid3\t18.8\t1\n")]
        tempLogger._write.assert_has_calls(calls)