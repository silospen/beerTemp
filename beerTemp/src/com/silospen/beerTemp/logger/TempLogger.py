import json
from os.path import expanduser

class TempLogger():
    LOG_FILE = expanduser("~") + "/tempLog"

    def log(self, timeInS, sensorId, temp, heaterOn):
        self._write(json.dumps({'time': timeInS, 'sensorId': sensorId, 'temp': float(temp), 'active': heaterOn}))

    def _write(self, line):
        with open(self.LOG_FILE, 'a+') as log:
            log.write(line)



