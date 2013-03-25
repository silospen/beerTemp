from os.path import expanduser

class TempLogger():
    LOG_FILE = expanduser("~") + "/tempLog"

    def log(self, timeInMs, temp, heaterOn):
        self._write(str(timeInMs) + '\t' + str(temp) + '\t' + ('1' if heaterOn else '0') + '\n')

    def _write(self, line):
        with open(self.LOG_FILE, 'a+') as log:
            log.write(line)



