from app.errors.invalid_pin_number import InvalidPinNumber
from app.errors.not_enough_amount import NotEnoughAmount
from app.errors.not_found_account import NotFoundAccount
from app.interface.bank import Bank 
from app.interface.cash_bin import CashBin 
from app.interface.card_reader import CardReader 
from app.interface.atm_ui import AtmUi

class Controller():
  def __init__(self, bank: Bank, cash_bin: CashBin, card_reader: CardReader, atm_ui: AtmUi):
    self.bank = bank
    self.card_reader = card_reader
    self.cash_bin = cash_bin
    self.atm_ui = atm_ui

  def see_balance(self):
    account = self._get_account()
    return self.bank.get_balance(account)


  def withdraw(self, amount):
    account = self._get_account()
    self._withdraw(account, amount)

  def _withdraw(self, account, amount):
    try:
      self.bank.check_amount(account, amount)
      self.cash_bin.check_amount(amount)
    except NotEnoughAmount as e:
      self.atm_ui.print_error(str(e))
      raise(e)
    
    self.bank.withdraw(account, amount)
    self.cash_bin.withdraw(amount)

  def deposit(self, amount):
    account = self._get_account()
    self._deposit(account, amount)

  def _deposit(self, account, amount):
    self.cash_bin.deposit(amount)
    self.bank.deposit(account, amount)

  def _get_account(self):
    card_id = self.card_reader.read()
    pin = self.atm_ui.get_pin()

    try:
      self.bank.verify_pin(card_id, pin)
    except InvalidPinNumber as e :
      self.atm_ui.print_error(str(e))
      raise(e)

    try:
      return self.bank.get_account(card_id)
    except NotFoundAccount as e:
      self.atm_ui.print_error(str(e))
      raise(e)
