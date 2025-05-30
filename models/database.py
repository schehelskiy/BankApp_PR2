import json
import os
from datetime import datetime
from models.core import User, Account, Transaction, UserRole
from models.utils import generate_id

class Database:
    def __init__(self, file_path="data.json"):
        self.file_path = file_path
        self.log_file = "log.txt"
        self.users = {}
        self.accounts = {}
        self.transactions = {}
        self.load_from_json()

    def load_from_json(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                    for user_data in data.get("users", []):
                        self.users[user_data["user_id"]] = User(
                            user_data["user_id"],
                            user_data["username"],
                            user_data["password"],
                            UserRole(user_data["role"])
                        )
                    for account_data in data.get("accounts", []):
                        self.accounts[account_data["account_id"]] = Account(
                            account_data["account_id"],
                            account_data["user_id"],
                            account_data["balance"],
                        )
                        self.accounts[account_data["account_id"]].is_blocked = account_data["is_blocked"]
                    for transaction_data in data.get("transactions", []):
                        self.transactions[transaction_data["transaction_id"]] = Transaction(
                            transaction_data["transaction_id"],
                            transaction_data["account_id"],
                            transaction_data["amount"],
                            transaction_data["transaction_type"],
                            datetime.fromisoformat(transaction_data["timestamp"])
                        )
            else:
                self._init_sample_data()
                self.save_to_json()
        except Exception as e:
            self.log_action(f"Помилка завантаження JSON: {str(e)}")

    def save_to_json(self):
        try:
            data = {
                "users": [
                    {
                        "user_id": user.user_id,
                        "username": user.username,
                        "password": user.password,
                        "role": user.role.value
                    } for user in self.users.values()
                ],
                "accounts": [
                    {
                        "account_id": account.account_id,
                        "user_id": account.user_id,
                        "balance": account.balance,
                        "is_blocked": account.is_blocked
                    } for account in self.accounts.values()
                ],
                "transactions": [
                    {
                        "transaction_id": transaction.transaction_id,
                        "account_id": transaction.account_id,
                        "amount": transaction.amount,
                        "transaction_type": transaction.transaction_type,
                        "timestamp": transaction.timestamp.isoformat()
                    } for transaction in self.transactions.values()
                ]
            }
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            self.log_action(f"Помилка збереження JSON: {str(e)}")

    def _init_sample_data(self):
        self.users["u1"] = User("u1", "client1", "pass123", UserRole.CLIENT)
        self.users["u2"] = User("u2", "employee1", "pass456", UserRole.EMPLOYEE)
        self.accounts["a1"] = Account("a1", "u1", 1000.0)
        self.transactions["t1"] = Transaction("t1", "a1", 100.0, "deposit")

    def register_user(self, username, password, role):
        for user in self.users.values():
            if user.username == username:
                return False, "Ім'я користувача вже існує"
        user_id = generate_id()
        self.users[user_id] = User(user_id, username, password, role)
        if role == UserRole.CLIENT:
            account_id = generate_id()
            self.accounts[account_id] = Account(account_id, user_id, 0.0)
        self.save_to_json()
        return True, "Реєстрація успішна"

    def get_user(self, username, password):
        for user in self.users.values():
            if user.username == username and user.password == password:
                return user
        return None

    def get_user_by_username(self, username):
        for user in self.users.values():
            if user.username == username:
                return user
        return None

    def get_account(self, account_id):
        return self.accounts.get(account_id)

    def get_user_accounts(self, user_id):
        return [account for account in self.accounts.values() if account.user_id == user_id]

    def create_account(self, user_id, account_id):
        self.accounts[account_id] = Account(account_id, user_id, 0.0)
        self.save_to_json()

    def add_transaction(self, transaction):
        self.transactions[transaction.transaction_id] = transaction
        self.save_to_json()

    def get_account_transactions(self, account_id):
        return [t for t in self.transactions.values() if t.account_id == account_id]

    def block_account(self, account_id):
        if account_id in self.accounts:
            self.accounts[account_id].is_blocked = True
            self.save_to_json()

    def unblock_account(self, account_id):
        if account_id in self.accounts:
            self.accounts[account_id].is_blocked = False
            self.save_to_json()

    def get_all_transactions(self):
        return list(self.transactions.values())

    def add_deposit(self, account, amount):
        user_id = account.user_id
        today = datetime.now().date()
        daily_deposits = sum(
            t.amount for t in self.transactions.values()
            if t.transaction_type == "deposit" and t.account_id in [a.account_id for a in self.get_user_accounts(user_id)]
            and t.timestamp.date() == today
        )
        if daily_deposits + amount > 100000:
            return False, "Перевищено денний ліміт депозиту 100,000"
        account.balance += amount
        self.save_to_json()
        return True, "Депозит дозволено"

    def export_report(self, total_deposits, total_transfers, total_payments):
        try:
            with open("report.txt", "w") as f:
                f.write(f"Звіт про транзакції ({datetime.now()})\n")
                f.write("-" * 40 + "\n")
                f.write(f"Загальні депозити: ${total_deposits:.2f}\n")
                f.write(f"Загальні перекази: ${total_transfers:.2f}\n")
                f.write(f"Загальні оплати рахунків: ${total_payments:.2f}\n")
        except Exception as e:
            self.log_action(f"Помилка експорту звіту: {str(e)}")

    def log_action(self, action):
        try:
            with open(self.log_file, "a") as f:
                f.write(f"[{datetime.now()}] {action}\n")
        except Exception as e:
            pass