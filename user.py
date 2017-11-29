"""
class user methods
"""
import random
from validate_email import validate_email


class User:
    users = []
    user_emails = []
    token = None
    username = None
    users_tokens = []
    out = None

    def registration(self, email, username: str, password: str):
        success = False
        try:
            if validate_email(email):
                if email not in self.user_emails:
                    if (username.isalnum() or username.isalpha()) and len(username) >= 5:
                        if len(password) >= 6:
                            if any(letter.isdigit() for letter in password) and any(letter.isalpha() for letter in password):
                                if password == password.replace(" ", ""):
                                    self.users.append({
                                        "email": email, "username": username, "password": password,
                                        "lists": [], "list_items": []
                                    })
                                    self.user_emails.append(email)
                                    success = True
                                    message = "User added successfully"
                                else:
                                    message = "Password cannot contain spaces"
                            else:
                                message = " Password must contain both numbers and letters"
                        else:
                            message = "password must be at least 6 characters"
                    else:
                        message = "username should only be alphanumeric and must be at least 5 characters long"
                else:
                    message = "Email already exists"
            else:
                message = "use a valid email address"
        except Exception:
            message = "An exception occurred"
        return {
            "success": success,
            "message": message
        }

    def login(self, email, password):
        success = False
        try:
            if validate_email(email):
                if email in self.user_emails:
                    user_id = self.user_emails.index(email)
                    if password == self.users[user_id]['password']:
                        success = True
                        token = self.token(16, "abcdefghijklmnopqrstuvwxyz")
                        self.users_tokens.append({"user_id": user_id, "token": token})
                        username = self.users[user_id]["username"]
                        message = {
                            "message": "Login successful, Welcome " + username,
                            "user_id": user_id,
                            "username": username,
                            "token": token
                        }
                    else:
                        message = "wrong password or email"
                else:
                    message = "email does not exist"
            else:
                message = "invalid email, please use a valid email"

        except Exception:
            message = "An error occurred"

        return{
            "success": success,
            "message": message
        }

    def token(self, length, characters):
        out = ''.join([random.choice(characters) for i in range(length)])
        return out

    def send_email(self, receiver, subject, message):
        import smtplib
        try:
            smtp = smtplib.SMTP("smtp.gmail.com", 587)  # initialize smtp class
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login("prettynoms@gmail.com", "shoppinglist1")
            header = 'To:' + receiver + '\nFrom: shopping list<prettynoms@gmail.com>\nSubject: ' + subject + '\n'
            msg = header + '\n' + message + '\n\n'
            smtp.sendmail("prettynoms@gmail.com", receiver, msg)
            smtp.close()
            return True
        except Exception:
            return False

    def forgot_password(self, email):
        success = False
        try:
            if validate_email(email):
                if email in self.user_emails:
                    user_id = self.user_emails.index(email)
                    username = self.users[user_id]["username"]
                    temporary_password = self.token(10, "abcdefghijklmnopqrstuvwxyz")
                    email_message = "Hello " + username + \
                                    "\nuse this new password to log in to you " \
                                    "shopping list account \nPassword: " + temporary_password
                    if self.send_email(email, "ShoppingList Password Reset", email_message):
                        self.users[user_id]["password"] = temporary_password
                        success = True
                        message = "Password sent to your email"
                    else:
                        message = "An error occurred, your password was not changed"
                else:
                    message = "Email is not registered with us"
            else:
                message = "invalid email"
        except Exception:
            message = "Error occurred"

        return {
            "success": success,
            "message": message
        }

    def logged_in(self, token, user_id):
        try:
            return {"user_id": int(user_id), "token": token} in self.users_tokens
        except Exception:
            return False

    def change_password(self, token, user_id, old_password, new_password):
        success = False
        try:
            if self.logged_in(token, user_id):
                if old_password == self.users[int(user_id)]["password"]:
                    if len(new_password) >= 6 and new_password.isalnum():
                        self.users[int(user_id)]["password"] = new_password
                        success = True
                        message = "your password was successfully changed"
                    else:
                        message = "password must be at least 8 characters and" \
                                  " must contain both numbers and letters"
                else:
                    message = "password did not match your stored password"
            else:
                message = "user must be logged in to change password"
        except Exception:
            message = "An error occurred. Password was not changed"
        return {
            "success": success,
            "message": message
        }

    def log_out(self, token, user_id):
        message = "Token was not logged in the system"
        if self.logged_in(token, user_id):
            self.users_tokens.remove({"user_id": int(user_id), "token": token})
            message = "User was logged out successfully"

        return {
            "success": True,
            "message": message
        }
