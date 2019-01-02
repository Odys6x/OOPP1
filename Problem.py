from wtforms import StringField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, Form, PasswordField,DateField
from wtforms import validators, ValidationError


class RequestForm(Form):
    problem = StringField('Problem', [validators.DataRequired('Please enter your problems.')])
    description = StringField('Description', [validators.DataRequired('Please enter description.')])
    location = StringField('Where is your location', [validators.DataRequired('Please enter your location.')])
    date    = DateField('Enter your date here', [validators.DataRequired('Please enter description.')])
    submit = SubmitField('Submit')

