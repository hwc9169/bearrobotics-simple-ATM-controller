class NotFoundAccount(Exception):
  def __init__(self, card_id):
    self.card_id = card_id

  def __str__(self):
    return "error: not found account for card ID({})".format(self.card_id)