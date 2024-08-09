from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired




class AccountForm(FlaskForm):
    account = StringField('Account handle?', validators=[DataRequired()])
    submit = SubmitField('Classify')

