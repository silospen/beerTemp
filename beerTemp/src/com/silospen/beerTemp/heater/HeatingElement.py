class HeatingElement():

    def __init__(self):
        self.active = False

    def isActive(self):
        return self.active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False