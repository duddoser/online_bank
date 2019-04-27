from random import shuffle
from flask import Flask, render_template, redirect, session
from db import DB
from operationsmodel import OperationsModel
from usersmodel import UsersModel
from signin_form import SigninForm
from sugnup_form import SignupForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'online_bank_secret_key'

o_db = DB('operations.db')
u_db = DB('users.db')
OperationsModel(o_db.get_connection()).init_table()
UsersModel(u_db.get_connection()).init_table()


@app.route('/home')
def home():
    return render_template('main.html')


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = SigninForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_model = UsersModel(u_db.get_connection())
        exists = user_model.exists(user_name, password)
        if exists[0]:
            session['username'] = user_name
            session['user_id'] = exists[1]
        return redirect('/main')
    return render_template('sign_in.html', title='Авторизация', form=form)


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = SignupForm()
    user_name = form.username.data
    password = form.password.data
    card_number = form.card_number.data
    expiry_date = form.expiry_date.data
    name = form.name.data
    safe_number = form.safe_number.data
    money = form.money.data
    user_model = UsersModel(u_db.get_connection())
    id = shuffle('012345')
    session['username'] = user_name
    session['user_id'] = id
    user_model.insert(user_name, password, card_number, expiry_date, name, safe_number, money)
    if form.validate_on_submit:
        return redirect('/home')
    return render_template('sign_up.html', title='Регистрация', form=form)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
