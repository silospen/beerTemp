try:
    import RPi.GPIO as GPIO
except RuntimeError as e:
    GPIO = None

class HeatingElement():
    ELEMENT_GPIO = 11

    def __init__(self):
        if GPIO:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.ELEMENT_GPIO, GPIO.OUT, initial=GPIO.HIGH)
        self.active = False

    def isActive(self):
        return self.active

    def activate(self):
        if GPIO:
            GPIO.output(self.ELEMENT_GPIO, GPIO.LOW)
        self.active = True

    def deactivate(self):
        if GPIO:
            GPIO.output(self.ELEMENT_GPIO, GPIO.HIGH)
        self.active = False