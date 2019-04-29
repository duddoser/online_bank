from flask import Flask, render_template, redirect, session, request, make_response, jsonify
from db import DB
from operationsmodel import OperationsModel
from usersmodel import UsersModel
from signin_form import SigninForm
from transfer_form import TransferForm
from data_check import check_data, card_check, cvv_check, name_check, double, luhn_algorithm, check_money


app = Flask(__name__)
app.config['SECRET_KEY'] = 'online_bank_secret_key'

OPERATIONS = {}
o_db = DB('operations.db')
u_db = DB('users.db')
OperationsModel(o_db.get_connection()).init_table()
UsersModel(u_db.get_connection()).init_table()


@app.route('/home')
def home():
    return render_template('main.html', title='Главная')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


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
    if request.method == 'POST':
        user_name = request.form['login']
        password = request.form['password']
        card_number = request.form['card_number']
        expiry_m = request.form['expiry_m']
        expiry_y = request.form['expiry_y']
        name = request.form['name']
        safe_number = request.form['ccv']
        money = request.form['money']
        user_model = UsersModel(u_db.get_connection())
        if not user_model.exists(user_name)[0] and card_check(card_number) and check_data(expiry_m, expiry_y) and\
            name_check(name) and cvv_check(safe_number) and check_money(money):
            if not user_model.exist_card_number(card_number)[0]:
                user_model.insert(user_name, password, card_number, expiry_m, expiry_y, name, safe_number, money)
                session['username'] = user_name
                session['user_id'] = user_model.exists(user_name, password)[1]
                return redirect('/home')
        else:
            return render_template('sign_up2.html', title='Регистрация')
    return render_template('sign_up.html', title='Регистрация')


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
        if i == 4:
            snippet[el] = str(row[i]) + '/' + str(row[i+1])
            i += 2
        else:
            snippet[el] = str(row[i])
            i += 1
    tuple_s = []
    for el in snippet:
        tuple_s.append((el, snippet[el]))
    return render_template('personal.html', lists=tuple_s)


@app.route('/history')
def history():
    o_model = OperationsModel(o_db.get_connection())
    row = o_model.get_all(session['user_id'])
    operations = []
    if row is not None:
        for el in row:
            operations.append(el[0])
        return render_template('history.html', title='История операций', lists=operations)


@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    u_model = UsersModel(u_db.get_connection())
    o_model = OperationsModel(o_db.get_connection())
    form = TransferForm()
    money1 = u_model.get_money(session['user_id'])[0]
    if form.validate_on_submit():
        if 0 < int(form.money.data) <= int(money1):
            if u_model.exist_card_number(form.card_number.data)[0]:
                id = u_model.get_id(form.card_number.data)[0]
                money2 = u_model.get_money(id)[0]
                u_model.update_money(form.card_number.data, int(money2) + int(form.money.data))
                u_model.update_money(u_model.get_card_number(session['user_id'])[0], int(money1) - int(form.money.data))
                string = 'Перевод держателю карты {}'.format(form.card_number.data)
                o_model.insert(string, id)
                return redirect('/success')
            else:
                return render_template('transfer2.html', title='Перевод денег', form=form)
        else:
            return render_template('transfer2.html', title='Перевод денег', form=form)
    return render_template('transfer.html', title='Перевод денег', form=form)


@app.route('/success')
def success():
    return render_template('success.html', title='Успешно завершено')


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/sign_in')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
