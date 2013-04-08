import unittest
import io
from unittest import mock
from unittest.mock import patch
from src.com.silospen.beerTemp.provider.TempProvider import TempProvider

class TempProviderTest(unittest.TestCase):
    def testGetTemp(self):
        self._setupRawTempExpectation("29 00 4b 46 ff ff 08 10 eb : crc=eb YES\n29 00 4b 46 ff ff 08 10 eb t=20250")
        tempProvider = TempProvider("test_serial")
        self.assertEqual(20.25, tempProvider.getTemp())
        TempProvider._rawTempHandle.assert_called_once_with("/sys/bus/w1/devices/test_serial/w1_slave")

    def testSetAmbient(self):
        self.assertFalse(TempProvider("test_serial").isAmbient())
        self.assertTrue(TempProvider("28-000004a2bb68").isAmbient())

    def testGetTemp_withMissingTempString(self):
        self._setupRawTempExpectation("29 00 4b 46 ff ff 08 10 eb : crc=eb YES\n29 00 4b 46 ff ff 08 10 eb t=")
        tempProvider = TempProvider("test_serial")
        self.assertRaises(Exception, tempProvider.getTemp)
        TempProvider._rawTempHandle.assert_called_once_with("/sys/bus/w1/devices/test_serial/w1_slave")

    def testGetTemp_withInvalidReading(self):
        self._setupRawTempExpectation("29 00 4b 46 ff ff 08 10 eb : crc=eb NO\n29 00 4b 46 ff ff 08 10 eb t=20250")
        tempProvider = TempProvider("test_serial")
        self.assertEqual(None, tempProvider.getTemp())
        TempProvider._rawTempHandle.assert_called_once_with("/sys/bus/w1/devices/test_serial/w1_slave")

    def testGetTemp_withBustedTempString(self):
        self._setupRawTempExpectation("29 00 4b 46 ff ff 08 10 eb : crc=eb YES")
        tempProvider = TempProvider("test_serial")
        self.assertRaises(Exception, tempProvider.getTemp)
        TempProvider._rawTempHandle.assert_called_once_with("/sys/bus/w1/devices/test_serial/w1_slave")

    def _setupRawTempExpectation(self, expectedTempString):
        TempProvider._rawTempHandle = mock.Mock(return_value=io.StringIO(expectedTempString))

    @patch('src.com.silospen.beerTemp.provider.TempProvider.TempProvider._listSensors',
        mock.Mock(return_value=["test_serial"]))
    def testCreate_singleProvider(self):
        self.assertEqual([TempProvider("test_serial")], TempProvider.create())

    @patch('src.com.silospen.beerTemp.provider.TempProvider.TempProvider._listSensors',
        mock.Mock(return_value=["test_serial", "w1_bus_master_1"]))
    def testCreate_singleProvider_excludes_busMaster(self):
        self.assertEqual([TempProvider("test_serial")], TempProvider.create())

    @patch('src.com.silospen.beerTemp.provider.TempProvider.TempProvider._listSensors',
        mock.Mock(return_value=["test_serial1", "test_serial2", "test_serial3"]))
    def testCreate_multipleProviders(self):
        self.assertEqual([TempProvider("test_serial1"), TempProvider("test_serial2"), TempProvider("test_serial3")],
            TempProvider.create())

    @patch('src.com.silospen.beerTemp.provider.TempProvider.TempProvider._listSensors', mock.Mock(return_value=[]))
    def testCreate_emptyList(self):
        self.assertEqual([], TempProvider.create())

    @patch('src.com.silospen.beerTemp.provider.TempProvider.TempProvider._listSensors',
        mock.Mock(side_effect=FileNotFoundError))
    def testCreate_withException(self):
        self.assertEqual([], TempProvider.create())