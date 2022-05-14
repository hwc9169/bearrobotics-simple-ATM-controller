class NotEnoughAmount(Exception):
  def __init__(self, account=None):
    self.account = account

  def __str__(self):
    if self.account:
      return "error: not enough amount in account({})".format(self.account)
    return "error: not enough amount in ATM cash bin"