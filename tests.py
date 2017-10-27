import unittest
from user import User
from shoppingList import ShoppingList


class Tests(unittest.TestCase):
    user = User()  # initiating class user
    shoppingList = ShoppingList(user)  # initiating class

    registered_mail = user.token(10, "abcdefghijklmnopqrstuvwxyz") + "@example.com"
    registered_password = "correct1234"

    token = None
    user_id = None
    lst = None
    items_list = None

    def test_01_all_functions_returns_dictionary(self):
        message = " is supposed to return a dictionary"
        self.assertIsInstance(self.user.registration(None, None, None), dict, "registration" + message)
        self.assertIsInstance(self.user.login(None, None), dict, "login" + message)
        self.assertIsInstance(self.user.forgot_password(None), dict, "forgot_password" + message)
        self.assertIsInstance(self.user.logged_in(None, None), bool, "logged_in should return true or false")
        self.assertIsInstance(self.user.change_password(None, None, None, None), dict, "change_password" + message)
        self.assertIsInstance(self.shoppingList.add_list(None, None, None), dict, "add_list" + message)
        self.assertIsInstance(self.shoppingList.update_list(None, None, None, None), dict, "update_list" + message)
        self.assertIsInstance(self.shoppingList.read_lists(None, None), dict, "read_lists" + message)
        self.assertIsInstance(self.shoppingList.delete_list(None, None, None), dict, "delete_lists" + message)
        self.assertIsInstance(self.shoppingList.add_item(None, None, None, None, None, None, None), dict, " add_item" + message)
        self.assertIsInstance(self.shoppingList.read_items(None, None, None), dict, "read_items" + message)
        self.assertIsInstance(self.shoppingList.edit_item(None, None, None, None, None, None), dict, "edit_item" + message)
        self.assertIsInstance(self.shoppingList.delete_item(None, None, None, None), dict, "delete_item" + message)

    def test_02_registration_accepts_valid_variables(self):
        result1 = self.user.registration("testmail", "tester", "Password")
        result2 = self.user.registration("testmail@email.com", "$%^&", "Password")
        result3 = self.user.registration("testmail@email.com", "tester", "Pass")
        result4 = self.user.registration(self.registered_mail, "tester", self.registered_password)
        self.assertFalse(result1["success"], "Registration accepts a valid email")
        self.assertFalse(result2["success"], "Registration accepts a alphanumeric username")
        self.assertFalse(result3["success"], "Registration accepts a valid password length")
        self.assertTrue(result4["success"], "Registration supposed to be successful")

    def test_03_login_accepts_valid_variables(self):
        result1 = self.user.login("testmail", "password")
        result2 = self.user.login("testmail@email.com", "pass")
        self.assertFalse(result1["success"], "Login supposed to accepts a valid email")
        self.assertFalse(result2["success"], "login supposed to accepts a valid password")

    def test_04_login_accepts_registered_credentials_only(self):
        result1 = self.user.login("unregisteredmail@example.com", "wrong_password")
        result2 = self.user.login(self.registered_mail, "wrong_password")
        result3 = self.user.login(self.registered_mail, self.registered_password)
        self.assertFalse(result1["success"], "email does not exist in our records")
        self.assertFalse(result2["success"], "wrong email and password combination")
        self.assertTrue(result3["success"], "Login supposed to be successful")
        self.__class__.token = result3["message"]["token"]
        self.__class__.user_id = result3["message"]["user_id"]
        self.__class__.user_name = result3["message"]["user_name"]

    def test_05_if_provided_token_and_user_id_are_working(self):
        result1 = self.user.logged_in("token", "user_id")
        result2 = self.user.logged_in(self.token, self.user_id)
        self.assertFalse(result1, "invalid user-id and token combination for this session")
        self.assertTrue(result2, "The system should accept the token and user_id it provided")

    def test_06_shopping_list_addition(self):
        result1 = self.shoppingList.add_list("list_name", None, None)
        result2 = self.shoppingList.add_list("list_name", self.user_id, self.token)
        self.assertFalse(result1["success"], "invalid user_id and token issued")
        self.assertTrue(result2["success"], "Should add list_name, user_id, and token")

    def test_07_read_shopping_list(self):
        result1 = self.shoppingList.read_lists(self.user_id, self.token)
        self.assertTrue(result1["success"], "success supposed to be true when provided with correct user_id and token")
        self.assertIsInstance(result1["message"], list, "supposed to be a list of lists")
        self.__class__.lst = result1["message"][0]
        self.assertIsInstance(self.lst, dict, "expected at least one item return as a dictionary")

    def test_08_edit_shopping_list(self):
        result1 = self.shoppingList.update_list(self.lst["list_id"], self.token, self.user_id, "new_name")
        result2 = self.shoppingList.update_list(None, self.token, self.user_id, "new_name")
        self.assertTrue(result1["success"], "supposed to change the 'list_name' to 'new_name'")
        self.assertFalse(result2["success"], "list_id must exist in the system")

    def test_09_add_items_to_the_list(self):
        result1 = self.shoppingList.add_item("item_name", "2", "", "400", self.lst["list_id"], self.token, self.user_id)
        result2 = self.shoppingList.add_item("item_name", "", "kg", "", None, self.token, self.user_id)
        result3 = self.shoppingList.add_item(None, "", "", "", self.lst["list_id"], self.token, self.user_id)
        self.assertTrue(result1["success"], "supposed to add item")
        self.assertFalse(result2["success"], "supposed to have a list_id")
        self.assertFalse(result3["success"], "supposed to have a list_name")

    def test_10_read_items(self):
        result1 = self.shoppingList.read_items(self.user_id, self.token, self.lst["list_id"])
        self.assertTrue(result1["success"], "supposed to return true when all the right details are provided")
        self.assertIsInstance(result1["message"], list, "supposed to return a list of items")
        self.__class__.items_list = result1["message"][0]
        self.assertIsInstance(self.items_list, dict, "expected at least one item returned as a dictionary")

    def test_11_edit_item(self):
        result1 = self.shoppingList.edit_item(
            self.items_list["item_id"], self.lst["list_id"], self.user_id, self.token, "item_name", "new_item_name")
        result2 = self.shoppingList.edit_item(None, None, None, None, None, "")
        self.assertTrue(result1["success"], "expected to change the 'item_name' to 'new_item_name'")
        self.assertFalse(result2["success"], "expected to return false")

    def test_12_delete_item(self):
        result1 = self.shoppingList.delete_item(self.items_list["item_id"], self.user_id, self.token, self.lst["list_id"])
        result2 = self.shoppingList.delete_item(None, None, None, None)
        self.assertTrue(result1["success"], "expected to remove item and return success as true")
        self.assertFalse(result2["success"], "expected to return false since removing the item fail")

    def test_13_delete_shopping_list(self):
        result1 = self.shoppingList.delete_list(self.lst["list_id"], self.user_id, self.token)
        result2 = self.shoppingList.delete_list(None, None, None)
        self.assertTrue(result1["success"], "should return success as true since the list was deleted")
        self.assertFalse(result2["success"], "should return success as false since the list ")

        
if __name__ == '__main__':
    unittest.main()
