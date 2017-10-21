"""
running application methods
"""
from user import User
import json
from flask import Flask, request, Response
from shoppingList import ShoppingList

user = User()
shoppingList = ShoppingList(user)

# Set up flask app
# Define a custom static directory
app = Flask(__name__, static_folder='designs/UI')


# Covert Dictionary to JSON
def dict_to_json(dct):
    return json.dumps(dct, sort_keys=True, indent=4, separators=(',', ': '))


# Routes
@app.route('/')
def root():
    return app.send_static_file('index.html')


# serve files from root url instead of static directory
@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)


@app.route('/register', methods=['POST', 'GET'])
def registration_submit():

    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        out = user.registration(email, username, password)
    else:
        out = {
            "success": False,
            "message": "Use POST to send your request with variables:"
                       " 'email', 'username', 'password'"
        }

    return Response(dict_to_json(out), mimetype="text/json")


@app.route('/login', methods=['POST'])
def login_submit():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        out = user.login(email, password)
    else:
        out = {
            "success": False,
            "message": "use POST to send your request with variables: 'email', 'password'"
        }

    return Response(dict_to_json(out), mimetype="text/json")


@app.route('/reset_password', methods=['POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        out = user.forgot_password(email)
    else:
        out = {
            "success": False,
            "message": "use POST to send your request with variable 'email'"
        }

    return Response(dict_to_json(out), mimetype="text/json")


@app.route('/change_password', methods=['POST'])
def change_password():
    out = {
        "success": False,
        "message": "use POST send your request and required are new_password and old_password"
    }
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        token = request.form.get('token')
        user_id = request.form.get('user_id')
        old_password = request.form.get('old_password')
        if new_password is not None and old_password is not None and user_id is not None and token is not None:
            out = user.change_password(token, user_id, old_password, new_password)

    return Response(dict_to_json(out), mimetype="text/json")


@app.route('/shoppingList_create', methods=['POST'])
def create_new_list():
    if request.method == 'POST':
        shoppinglist_name = request.form.get('list_name')
        token = request.form.get('token')
        user_id = request.form.get('user_id')
        out = shoppingList.add_list(shoppinglist_name, user_id, token)
    else:
        out = {
            "success": False,
            "message": "list creation failed"
        }
    return Response(dict_to_json(out), mimetype="text/json")


@app.route('/read_lists', methods=['POST'])
def read_lists():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        token = request.form.get('token')
        out = shoppingList.read_lists(user_id, token)
    else:
        out = {
            "success": False,
            "message": "use the POST method to provide user_id and token"
        }
    return Response(dict_to_json(out), mimetype="text/json")


@app.route('/edit_lists', methods=['POST'])
def edit_lists():
    if request.method == 'POST':
        list_id = request.form.get('list_id')
        token = request.form.get('token')
        user_id = request.form.get('user_id')
        list_name = request.form.get('list_name')
        out = shoppingList.update_list(list_id, token, user_id, list_name)
    else:
        out = {
            "success": False,
            "message": "use POST and required variables are list_id, token, user_id and list_name"
        }
    return Response(dict_to_json(out), mimetype= "text/json")


@app.route("/logout", methods=['POST'])
def logout():
    if request.method == 'POST':
        token = request.form.get('token')
        user_id = request.form.get('user_id')
        out = user.log_out(token, user_id)

    else:
        out = {
            "success": False,
            "message": "unsuccessful logout"
        }
    return Response(dict_to_json(out), mimetype="text/json")


@app.route('/delete_lists', methods=['POST'])
def delete_lists():
    if request.method == 'POST':
        list_id = request.form.get('list_id')
        user_id = request.form.get('user_id')
        token = request.form.get('token')
        out = shoppingList.delete_list(list_id, user_id, token)
    else:
        out = {
            "success": False,
            "message": "use POST to get required variables: list_id, user_id, token"
        }
    return Response(dict_to_json(out), mimetype="text/json")


@app.route('/add_items', methods=['POST'])
def add_items():
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        quantity = request.form.get('quantity')
        units = request.form.get('units')
        cost = request.form.get('cost')
        list_id = request.form.get('list_id')
        token = request.form.get('token')
        user_id = request.form.get('user_id')
        out = shoppingList.add_item(item_name, quantity, units, cost, list_id, token, user_id)
    else:
        out = {
            "success": False,
            "message": "use POST to get the required variables: item_name, quantity,units, cost, list_id,"
                       "token, user_id"
        }
    return Response(dict_to_json(out), mimetype="text/json")


@app.route('/read_items', methods=['POST'])
def read_items():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        token = request.form.get('token')
        list_id = request.form.get("list_id")
        out = shoppingList.read_items(user_id, token, list_id)
    else:
        out = {
            "success": False,
            "message": "Use POST to get required variables: user_id, token and list_id"
        }
    return Response(dict_to_json(out), mimetype="text/json")


@app.route('/edit_items', methods=['POST'])
def edit_items():
    if request.method == 'POST':
        item_id = request.form.get('item_id')
        user_id = request.form.get('user_id')
        token = request.form.get('token')
        list_id = request.form.get('list_id')
        attribute = request.form.get('attribute')
        value = request.form.get('value')
        out = shoppingList.edit_item(item_id, list_id, user_id, token, attribute, value)
    else:
        out = {
            "success": False,
            "message" : "Use POST to get required variables item_id, user_id, token and list_id"
        }
    return Response(dict_to_json(out), mimetype="text\json")


@app.route('/delete_items', methods=['POST'])
def delete_items():
    if request.method == 'POST':
        item_id = request.form.get('item_id')
        user_id = request.form.get('user_id')
        token = request.form.get('token')
        list_id = request.form.get('list_id')
        out = shoppingList.delete_item(item_id, user_id, token, list_id)
    else:
        out = {
            "success": False,
            "message": "use POST tp get required variables:item_id, user_id, token and list_id"
        }
    return Response(dict_to_json(out), mimetype="text/json")


if __name__ == '__main__':
    app.run("0.0.0.0", 8080)
