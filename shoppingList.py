"""
class shoppingList and shoppingList_items methods
"""
from user import User


class ShoppingList:

    def __init__(self, user: User):  # expects a data type of the class user
        self.user = user

    def add_list(self, list_name: str, user_id, token):
        success = False
        try:
            if self.user.logged_in(token, user_id):
                if list_name is not None and list_name.strip() is not "":
                    self.user.users[int(user_id)]["lists"].append(str(list_name))
                    self.user.users[int(user_id)]["list_items"].append([])
                    success = True
                    message = "Shopping list created successfully"
                else:
                    message = "list name is required"
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
                for list_id in range(len(lst)):
                    message.append({"list_id": list_id, "list_name": lst[list_id]})
                success = True
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
                if list_name is not None:
                    self.user.users[int(user_id)]["lists"][int(list_id)] = list_name
                    success = True
                    message = "list name changed successfully"
                else:
                    message = "list name is required"
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
        success = False
        try:
            if self.user.logged_in(token, user_id):
                if item_name is not None and item_name.strip() is not "":
                    if quantity.isdigit():
                        if cost.isdigit():
                            self.user.users[int(user_id)]["list_items"][int(list_id)].append({
                                "item_name": item_name, "quantity": quantity, "units": units, "cost": cost
                            })
                            success = True
                            message = "items added successfully"
                        else:
                            message = "cost can only be a digit"
                    else:
                        message = "quantity can only contain digits"
                else:
                    message = "provide the list name"
            else:
                message = "user must be logged in to add items to the list"
        except Exception:
            message = "An error occurred"

        return{
            "success": success,
            "message": message
        }

    def read_items(self, user_id, token, list_id):
        success = False
        try:
            if self.user.logged_in(token, user_id):
                lst_items = self.user.users[int(user_id)]["list_items"][int(list_id)]
                success = True
                message = []
                for item_id in range(len(lst_items)):
                    item = lst_items[item_id]
                    item["item_id"] = item_id
                    message.append(item)
            else:
                message = "must be logged in to view items"
        except Exception:
            message = "An error occurred"
        return{
            "success": success,
            "message": message
        }

    def edit_item(self, item_id, list_id, user_id, token, attribute, value):
        success = False
        try:
            if self.user.logged_in(token, user_id):
                if attribute and value is not None:
                    message = attribute + " updated successfully"
                    success = True
                    if attribute == "item_name":
                        if value is not None and value.strip() is not "":
                            self.user.users[int(user_id)]["list_items"][int(list_id)][int(item_id)]["item_name"] = str(value)
                        else:
                            success = False
                            message = "list name cannot be empty"
                    elif attribute == "quantity":
                        if value.isdigit():
                            self.user.users[int(user_id)]["list_items"][int(list_id)][int(item_id)]["quantity"] = value
                        else:
                            success = False
                            message = "quantity must be a digit"
                    elif attribute == "cost":
                        if value.isdigit():
                            self.user.users[int(user_id)]["list_items"][int(list_id)][int(item_id)]["cost"] = value
                        else:
                            success = False
                            message = "cost must be a digit"
                    elif attribute == "units":
                        self.user.users[int(user_id)]["list_items"][int(list_id)][int(item_id)]["units"] = value
                    else:
                        success = False
                        message = attribute + " not allowed"
                else:
                    message = attribute + "and" + value + " can not be empty"
            else:
                message = "user must be logged in"
        except Exception:
            message = "An error occurred"

        return{
            "success": success,
            "message": message
        }

    def delete_item(self, item_id, user_id, token, list_id):
        success = False
        try:
            if self.user.logged_in(token, user_id):
                self.user.users[int(user_id)]["list_items"][int(list_id)].pop(int(item_id))
                success = True
                message = "item successfully deleted"
            else:
                message = "user must be logged in to perform a delete action"
        except Exception:
            message = "An error occurred"
        return{
            "success": success,
            "message": message
        }




