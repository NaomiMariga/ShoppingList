from flask import Flask, request, Response, redirect, url_for, send_from_directory
from user import User
from shoppingList import ShoppingList
import json

user = User()
shoppingList = ShoppingList(user)

# Set up flask app
# Define a custom static directory
naomi = Flask(__name__, static_folder='designs/UI')
naomi.debug = True


# Covert Dictionary to JSON
def dict_to_json(dct):
    return json.dumps(dct, sort_keys=True, indent=4, separators=(',', ': '))


# Routes
@naomi.route('/')
def root():
    return naomi.send_static_file('index.html')


# serve files from root url instead of static directory
@naomi.route('/<path:path>')
def static_proxy(path):
    return naomi.send_static_file(path)


@naomi.route('/register', methods=['POST', 'GET'])
def registration_submit():

    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        out = user.registration(email, username, password)
    else:
        out = {
            "success": False,
            "message": "Use POST to send your request with variables: 'email', 'username', 'password'"
        }

    return Response(dict_to_json(out), mimetype="text/json")


@naomi.route('/login', methods=['POST'])
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


@naomi.route('/reset_password', methods=['POST'])
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




if __name__ == '__main__':
    naomi.run()

