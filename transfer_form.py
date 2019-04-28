from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class TransferForm(FlaskForm):
        card_number = StringField('Номер карты (лица, которому переводим)', validators=[DataRequired()])
        money = StringField('Сумма перевода', validators=[DataRequired()])
        submit = SubmitField('Перевести')
