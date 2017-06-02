from flask import Flask, render_template, redirect
from app.api.users import api_bp as user_api_bp
from app.api.memories import api_bp as memory_api_bp
from app.api.auth import api_bp as auth_api_bp


app = Flask(__name__)
app.config.from_object('config')

app.register_blueprint(user_api_bp)
app.register_blueprint(memory_api_bp)
app.register_blueprint(auth_api_bp)


@app.route('/')
def index():
    return redirect('/login')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/memories')
def memory():
    return render_template('memory_list.html')

@app.after_request
def accept(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
