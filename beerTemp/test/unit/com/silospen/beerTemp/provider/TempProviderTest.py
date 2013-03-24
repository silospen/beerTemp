import unittest
import io
from unittest import mock
from src.com.silospen.beerTemp.provider.TempProvider import TempProvider

class TempProviderTest(unittest.TestCase):
    def testGetTemp(self):
        self._setupExpectation("29 00 4b 46 ff ff 08 10 eb : crc=eb YES\n29 00 4b 46 ff ff 08 10 eb t=20250")
        tempProvider = TempProvider("test_serial")
        self.assertEqual(20.25, tempProvider.getTemp())
        TempProvider._rawTempHandle.assert_called_once_with("/sys/bus/w1/devices/test_serial/w1_slave")

    def testGetTemp_withEmptyTempString(self):
        self._setupExpectation("")
        tempProvider = TempProvider("test_serial")
        self.assertRaises(Exception, tempProvider.getTemp)
        TempProvider._rawTempHandle.assert_called_once_with("/sys/bus/w1/devices/test_serial/w1_slave")

    def testGetTemp_withMissingTempString(self):
        self._setupExpectation("29 00 4b 46 ff ff 08 10 eb : crc=eb YES\n29 00 4b 46 ff ff 08 10 eb t=")
        tempProvider = TempProvider("test_serial")
        self.assertRaises(Exception, tempProvider.getTemp)
        TempProvider._rawTempHandle.assert_called_once_with("/sys/bus/w1/devices/test_serial/w1_slave")

    def testGetTemp_withBustedTempString(self):
        self._setupExpectation("29 00 4b 46 ff ff 08 10 eb : crc=eb Y")
        tempProvider = TempProvider("test_serial")
        self.assertRaises(Exception, tempProvider.getTemp)
        TempProvider._rawTempHandle.assert_called_once_with("/sys/bus/w1/devices/test_serial/w1_slave")

    def _setupExpectation(self, expectedTempString):
        TempProvider._rawTempHandle = mock.Mock(return_value=io.StringIO(expectedTempString))

