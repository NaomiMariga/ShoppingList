from user import User


class ShoppingList:

    def __init__(self, user: User):  # expects a data type of the class user
        self.user = user

    def add_list(self, list_name: str, user_id, token):
        success = False
        try:
            if self.user.logged_in(token, user_id):
                self.user.users[int(user_id)]["lists"].append(str(list_name))
                self.user.users[int(user_id)]["list_items"].append([])
                success = True
                message = "Shopping list created successfully"
            else:
                message = "user must be logged in to create am list"
        except Exception:
            message = "An error occurred. Please retry."

        return{
            "success": success,
            "message": message
        }

    def read_lists(self, user_id, token):
        success = False
        try:
            if self.user.logged_in(token, user_id):
                lst = self.user.users[int(user_id)]["lists"]
                message = []
                success = True
                for list_id in range(len(lst)):
                    message.append({"list_id": list_id, "list_name": lst[list_id]})
            else:
                message = "user must be logged in to read lists"
        except Exception:
            message = "An error occurred"

        return{
            "success": success,
            "message": message
        }

    def update_list(self, list_id, token, user_id, list_name):
        success = False
        try:
            if self.user.logged_in(token, user_id):
                self.user.users[int(user_id)]["lists"][int(list_id)] = list_name
                success = True
                message = "list name changed successfully"
            else:
                message = "user must be logged in to change the list name"
        except Exception:
            message = "An error occurred"
        return {
            "success": success,
            "message": message
        }

    def delete_list(self, list_id, user_id, token):
        success = False
        try:
            if self.user.logged_in(token, user_id):
                self.user.users[int(user_id)]["lists"].pop(int(list_id))
                self.user.users[int(user_id)]["list_items"].pop(int(list_id))
                success = True
                message = "list was successfully deleted"
            else:
                message = "user must be logged in"
        except Exception:
            message = "An error occurred"

        return{
            "success": success,
            "message": message
        }

    def add_item(self, item_name, quantity, units, cost, list_id, token, user_id):
        return

    def delete_item(self, item_id, user_id, token, list_id):
        return

    def edit_item(self, item_id, list_id, user_id, token, item_name, quantity, cost, units):
        return

    def read_items(self, user_id, token, list_id):
        return


