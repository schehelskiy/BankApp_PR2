from models.core import UserRole

class AuthManager:
    def __init__(self, database):
        self.database = database
        self.current_user = None

    def login(self, username, password):
        user = self.database.get_user(username, password)
        if user:
            self.current_user = user
            return True
        return False

    def logout(self):
        self.current_user = None

    def has_access(self, required_role):
        if not self.current_user:
            return False
        return self.current_user.role == required_role