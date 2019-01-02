from flask import *
from Problem import *
from Create import *

import functools

app = Flask(__name__)
app.secret_key = 'secret_123'



@app.route('/report', methods=('GET', 'POST'))
def register():
    form = RequestForm(request.form)
    if request.method == 'POST':

        problem = form.problem.data
        description = form.description.data
        location = form.location.data
        date     = form.date.data
        error = ""
        if problem == "":
            error = 'Username is required.'
        if description == "":
            error = 'Description is required.'
        if location == "":
            error = 'Location is required'
        if date == "":
            error = 'Date is required'

        if error == "":

            User.create_request(problem, description, location,date)
            return redirect(url_for('Userpage'))
        flash(error)
    return render_template('Userpage.html', form=form)


@app.route('/Adminpage')
def viewpublications():

    db_read = shelve.open("problems.bak", "r")

    problems = db_read["problems"]

    print(problems)

    list = []

    for pubid in problems:
        list.append(problems.get(pubid))

    return render_template('Adminpage.html', publications=list)




if __name__ == '__main__':
    app.run()
