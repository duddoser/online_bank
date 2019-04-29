import datetime


def check_data(data_m, data_y):
    year, month = datetime.datetime.now().year, datetime.datetime.now().month
    if data_m.isdigit() and data_y.isdigit():
        if int('20' + data_y) > year:
            return True
        elif int('20' + data_y) == year and int(data_m) >= month:
            return True
    return False


def check_money(money):
    if money.isdigit():
        return True
    return False


def card_check(card):
    if len(card) == 16 and card.isdigit():
        return True
    return False


def cvv_check(cvv):
    if len(cvv) == 3 and cvv.isdigit():
        return True
    return False


def name_check(name):
    if ' ' in name:
        s = name.split()
        if s[0].isalpha() and s[1].isalpha():
            for el in s[0]:
                if el.lower() not in 'qwertyuiopasdfghjklzxcvbnm':
                    return False
            for el in s[1]:
                if el.lower() not in 'qwertyuiopasdfghjklzxcvbnm':
                    return False
            return True
    return False


def double(x):
    res = x * 2
    if res > 9:
        res = res - 9
    return res


def luhn_algorithm(card):
    odd = map(lambda x: double(int(x)), card[::2])
    even = map(int, card[1::2])
    return (sum(odd) + sum(even)) % 10 == 0
