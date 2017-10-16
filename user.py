import random


class User:
    def registration(self, email, username, password):
        return

    def login(self, email, password):
        return

    def token(self, n, characters):
        out = ''.join([random.choice(characters) for i in range(n)])
        return out

    def forgot_password(self, email):
        return

    def change_password(self, token, user_id, old_password, new_password):
        return

    def logged_in(self, token, user_id):
        return

    def log_out(self, token, user_id):
        return