from unittest import TestCase
from unittest.mock import patch

from app.controller import Controller
from app.errors.invalid_pin_number import InvalidPinNumber
from app.errors.not_enough_amount import NotEnoughAmount
from app.errors.not_found_account import NotFoundAccount

class TestController(TestCase):
  @patch('app.interface.bank.Bank')
  @patch('app.interface.cash_bin.CashBin')
  @patch('app.interface.card_reader.CardReader')
  @patch('app.interface.atm_ui.AtmUi')
  def setUp(self, mock_bank, mock_cash_bin, mock_card_reader, mock_atm_ui):
    self.bank = mock_bank
    self.cash_bin = mock_cash_bin
    self.card_reader = mock_card_reader
    self.atm_ui = mock_atm_ui

    self.controller = Controller(mock_bank, mock_cash_bin, mock_card_reader, mock_atm_ui)

  def tearDown(self):
    super().tearDown()

  def test_see_balance(self):
    self.bank.get_balance.return_value = 12

    balance = self.controller.see_balance()

    self.assertEqual(balance, 12)

  def test_deposit(self):
    self.bank.get_account.return_value = "fakeaccount"

    self.controller.deposit(50)
    
    self.bank.deposit.assert_called_with("fakeaccount", 50)
    self.cash_bin.deposit.assert_called_with(50)

  def test_withdraw(self):
    self.bank.get_account.return_value = "fakeaccount"

    self.controller.withdraw(35)
    
    self.bank.withdraw.assert_called_with("fakeaccount", 35)
    self.cash_bin.withdraw.assert_called_with(35)

  def test_see_balance_when_invalid_pin(self):
    error = InvalidPinNumber("invalid_pin_number")
    self.bank.verify_pin.side_effect = error

    self.assertRaises(type(error), lambda: self.controller.withdraw(50))

    self.atm_ui.print_error.assert_called_with(str(error))
    
  def test_see_balance_account_not_found(self):
    error = NotFoundAccount("invalid_account")
    self.bank.get_account.side_effect = error
    
    self.assertRaises(type(error), lambda: self.controller.see_balance())

    self.atm_ui.print_error.assert_called_with(str(error))

  def test_withdraw_when_not_enough_amount_in_atm(self):
    error = NotEnoughAmount()
    self.cash_bin.check_amount.side_effect = error

    self.assertRaises(type(error), lambda: self.controller.withdraw(50))

    self.atm_ui.print_error.assert_called_with(str(error))

  def test_withdraw_when_not_enough_amount_in_account(self):
    error = NotEnoughAmount("fakeaccount")
    self.cash_bin.check_amount.side_effect = error
    
    self.assertRaises(type(error), lambda: self.controller.withdraw(50))

    self.atm_ui.print_error.assert_called_with(str(error))
