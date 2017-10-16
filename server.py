from flask import Flask, request, redirect, url_for, send_from_directory

# Set up flask app
# Define a custom static directory
naomi = Flask(__name__, static_folder='designs/UI')
naomi.debug = True


# Routes
@naomi.route('/')
def root():
    return naomi.send_static_file('index.html')


# serve files from root url instead of static directory
@naomi.route('/<path:path>')
def static_proxy(path):
    return naomi.send_static_file(path)


if __name__ == '__main__':
    naomi.run()

