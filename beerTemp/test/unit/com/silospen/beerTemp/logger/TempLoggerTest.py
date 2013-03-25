import unittest
from unittest import mock
from src.com.silospen.beerTemp.logger.TempLogger import TempLogger

class TempLoggerTest(unittest.TestCase):
    def testLog(self):
        tempLogger = TempLogger()
        TempLogger._write = mock.Mock()
        tempLogger.log(1234, "sensorID", 22.123, True)
        TempLogger._write.assert_called_once_with("1234\tsensorID\t22.123\t1\n")