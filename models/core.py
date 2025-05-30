from datetime import datetime
from enum import Enum

class UserRole(Enum):
    CLIENT = "client"
    EMPLOYEE = "employee"

class User:
    def __init__(self, user_id, username, password, role: UserRole):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role

class Account:
    def __init__(self, account_id, user_id, balance=0.0):
        self.account_id = account_id
        self.user_id = user_id
        self.balance = balance
        self.is_blocked = False

class Transaction:
    def __init__(self, transaction_id, account_id, amount, transaction_type, timestamp=None):
        self.transaction_id = transaction_id
        self.account_id = account_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.timestamp = timestamp or datetime.now()