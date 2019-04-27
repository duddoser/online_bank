from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class Signuporm(FlaskForm):
        username = StringField('Логин', validators=[DataRequired()])
        password = PasswordField('Пароль', validators=[DataRequired()])
        card_number = StringField('Номер карты', validators=[DataRequired()])
        expiry_date = StringField('Срок истечения карты', validators=[DataRequired()])
        name = StringField('Указаннвые имя и фамилия на карте (на латинице)', validators=[DataRequired()])
        safe_number = StringField('Код на обратной стороне карты', validators=[DataRequired()])
        money = StringField('Количество денег на счету', validators=[DataRequired()])
        submit = SubmitField('Зарегестрироваться')
