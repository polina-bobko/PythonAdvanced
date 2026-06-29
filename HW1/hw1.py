# task1


# task2
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_flask():
    return "Hello, Flask!"

@app.route('/user/<username>')
def hello_flask_user(username):
    return f"Hello, {username}!"

if __name__ == "__main__":
    app.run()