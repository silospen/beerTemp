import logging
from subprocess import Popen
import tempfile
import time
from src.com.silospen.beerTemp.heater.HeatingElement import HeatingElement
from src.com.silospen.beerTemp.logger.TempLogger import TempLogger
from src.com.silospen.beerTemp.provider.TempProvider import TempProvider

class BeerTemp():
    THRESHOLD = 20.5
    LOG = logging.getLogger("BeerTemp")

    def __init__(self, tempProviders, heatingElement, tempLogger):
        self._tempProviders = tempProviders
        self._heatingElement = heatingElement
        self._tempLogger = tempLogger

    def testTempAndLog(self):
        temps = []
        for tempProvider in self._tempProviders:
            temp = tempProvider.getTemp()
            if temp is not None:
                temps.append((tempProvider.getId(), temp, tempProvider.isAmbient()))

        if sum(temp[1] < self.THRESHOLD for temp in temps if not temp[2]) > len(temps) // 2:
            self._heatingElement.activate()
        else:
            self._heatingElement.deactivate()

        currentTime = int(time.time())

        for temps in temps:
            self._tempLogger.log(currentTime, temps[0], temps[1], self._heatingElement.isActive())

    def publishLog(self):
        #noinspection PyStatementEffect
        Popen(["sh", "/root/publishLog.sh"]).pid

    def schedule(self):
        while True:
            try:
                self.testTempAndLog()
                self.publishLog()
            except Exception as e:
                self.LOG.error(e)
            time.sleep(60)


if __name__ == '__main__':
    logging.basicConfig(filename=tempfile.gettempdir() + "/" + 'beerTemp.log', level=logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    logging.getLogger().addHandler(ch)

    BeerTemp(TempProvider.create(), HeatingElement(), TempLogger()).schedule()
