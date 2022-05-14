class Bank():
  def get_balance(self, account):
    raise NotImplementedError()
  
  def withdraw(self, account, amount):
    raise NotImplementedError()
  
  def deposit(self, account, amount):
    raise NotImplementedError()
  
  def verify_pin(self, card_id, pin):
    raise NotImplementedError()

  def get_account(self, card_id):
    raise NotImplementedError()
  
  def check_amount(self, account, amount):
    raise NotImplementedError()