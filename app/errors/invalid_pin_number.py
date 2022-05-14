class InvalidPinNumber(Exception):
  def __init__(self, pin):
    self.pin = pin

  def __str__(self):
    return "error: invalid pin number({})".format(self.pin)