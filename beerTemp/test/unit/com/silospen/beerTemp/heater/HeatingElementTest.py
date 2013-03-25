import unittest
from src.com.silospen.beerTemp.heater.HeatingElement import HeatingElement

class HeatingElementTest(unittest.TestCase):
    def testActivate(self):
        heatingElement = HeatingElement()
        self.assertFalse(heatingElement.isActive())
        heatingElement.activate()
        self.assertTrue(heatingElement.isActive())
        heatingElement.deactivate()
        self.assertFalse(heatingElement.isActive())