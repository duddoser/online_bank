from flask import Flask, render_template, redirect, session
from db import DB
from operationsmodel import OperationsModel
from usersmodel import UsersModel
from signin_form import SigninForm
from signup_form import SignupForm
from transfer_form import TransferForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'online_bank_secret_key'

o_db = DB('operations.db')
u_db = DB('users.db')
OperationsModel(o_db.get_connection()).init_table()
UsersModel(u_db.get_connection()).init_table()


@app.route('/home')
def home():
    return render_template('main.html', title='Главная')


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
        return redirect('/home')
    return render_template('sign_in.html', title='Авторизация', form=form)


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = SignupForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        card_number = form.card_number.data
        expiry_date = form.expiry_date.data
        name = form.name.data
        safe_number = form.safe_number.data
        money = form.money.data
        user_model = UsersModel(u_db.get_connection())
        user_model.insert(user_name, password, card_number, expiry_date, name, safe_number, money)
        session['username'] = user_name
        session['user_id'] = user_model.exists(user_name, password)[1]
        return redirect('/home')
    return render_template('sign_up.html', title='Регистрация', form=form)


@app.route('/personal', methods=['GET'])
def personal():
    user_model = UsersModel(u_db.get_connection())
    row = list(user_model.get(session['user_id']))
    snippet = {
        'Логин': '',
        'Пароль': '',
        'Номер карты': '',
        'Дата истечения': '',
        'Имя': '',
        'Трехзначный код': '',
        'Баланс': ''
    }
    i = 1
    for el in snippet:
        snippet[el] = str(row[i])
        i += 1
    tuple_s = []
    for el in snippet:
        tuple_s.append((el, snippet[el]))
    return render_template('personal.html', lists=tuple_s)


@app.route('/history', methods=['GET'])
def history():
    o_model = OperationsModel(o_db.get_connection())
    row = o_model.get_all(session['user_id'])
    operations = []
    for el in row:
        operations.append(el)
    return render_template('history.html', title='История операций', lists=operations)


@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    u_model = UsersModel(u_db.get_connection())
    o_model = OperationsModel(o_db.get_connection())
    form = TransferForm()
    money1 = o_model.get_money(session['user_id'])
    if 0 < int(money1) <= int(form.money.data):
        if u_model.exist_card_number(form.card_number.data):
            id = u_model.get_id(form.card_number.data)
            money2 = u_model.get_money()

    return render_template('transfer.html', title='Перевод денег')


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/sign_in')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
