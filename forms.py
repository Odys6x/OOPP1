from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators






class PublicationForm(Form):
    problem = RadioField('Type Of Problems', choices=[('smrt', 'Mrt'), ('sbus', 'Bus')])

    description = TextAreaField('description')

    location = StringField('location', [
        validators.Length(min=1, max=100),
        validators.DataRequired()])
    status = SelectField('Status', [validators.DataRequired()],
                         choices=[('', 'Select'), ('P', 'Pending'), ('A', 'Available For Borrowing'),
                                  ])