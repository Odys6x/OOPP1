from flask import Flask, render_template, request, flash, redirect, url_for
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators
from Mrt import problemReq
from Bus import ProblemReq
import shelve

app = Flask(__name__)


@app.route('/')
def default():
    return render_template('Userpage.html')




@app.route('/viewproblems')
def viewproblems():

    db_read = shelve.open("storage.db", "r")

    problems = db_read["problems"]

    print(problems)

    list = []

    for pubid in problems:
        list.append(problems.get(pubid))

    return render_template('Adminpage.html', problems=list)

class RequiredIf(object):

    def __init__(self, *args, **kwargs):
        self.conditions = kwargs

    def __call__(self, form, field):
        for name, data in self.conditions.items():
            if name not in form._fields:
                validators.Optional()(field)
            else:
                condition_field = form._fields.get(name)
                if condition_field.data == data:
                    validators.DataRequired().__call__(form, field)
                else:
                    validators.Optional().__call__(form, field)


@app.route('/delete_problem/<int:id>', methods=['POST'])
def delete_problem(id):
    db_read = shelve.open("storage.db")

    try:
        pList = db_read["problems"]
        print("id, ", id)
        print("pList before: ", pList)

        ##del pList[id]
        pList.pop(id)

        print(pList)
        db_read["problems"] = pList
        db_read.close()

        flash('Problem Deleted', 'success')

        return redirect(url_for('Adminpage'))

    except:
        flash('Problem Not Deleted', 'danger')
        return redirect(url_for('Adminpage'))


    # mag_db = root.child('publications/' + id)
    # mag_db.delete()
    # flash('Article Deleted', 'success')
    #
    # return redirect(url_for('viewpublications'))
#this one u copy from lib portal? i delete first ahh^ cuz not needed or u alr implemented some stuff i implemented some stuff okk


@app.route('/Adminpage')


class PublicationForm(Form):
    problem = RadioField('Type Of Problems', choices=[('smrt', 'Mrt'), ('sbus', 'Bus')], default='')

    description = TextAreaField('description', [
        RequiredIf(pubtype='smrt' or 'sbus')])

    location = StringField('location', [
        validators.Length(min=1, max=100),
        validators.DataRequired()])
    status = SelectField('Status', [validators.DataRequired()],
                         choices=[('', 'Select'), ('P', 'Pending'), ('A', 'Available For Borrowing'),
                                  ], default='')



@app.route('/Userpage', methods=['GET', 'POST'])
def new():
    form = PublicationForm(request.form)

    db_read = shelve.open("storage.db")

    try:
        pubList = db_read["problems"]
    except:
        pubList = {}

    if request.method == 'POST' and form.validate():
        if form.problem.data == 'smrt':
            problem = form.problem.data
            description = form.description.data
            status = form.status.data
            location = form.location.data
            datereported = form.datereported.data

            mrt = problemReq(problem,description,location,datereported,status)

            id = len(pubList) + 1

            pubList[id] = mrt

            db_read["problems"] = pubList

            db_read.close()

            flash('Problem has been sent sucessfully.', 'success')

        elif form.problem.data == 'sbus':
            problem = form.problem.data
            description = form.description.data
            status = form.status.data
            location = form.location.data
            datereported = form.datereported.data

            bus = ProblemReq(problem,description,location,datereported,status)
            id = len(pubList) + 1


            pubList[id] = bus

            db_read["problems"] = pubList

            db_read.close()


            flash('Problem has been sent sucessfully.', 'success')

        return redirect(url_for('Adminpage'))


    return render_template('Userpage.html', form= form)

@app.route('/resolved/<int:id>/', methods=['GET', 'POST'])
def resolved_problem(id):

    form = PublicationForm(request.form)
    db_read = shelve.open("storage.db")
    try:
        pList = db_read["problems"]
        if request.method == 'POST' and form.validate():
            if form.problem.data == 'smrt':
                problem = form.problem.data
                description = form.description.data
                status = form.status.data
                location = form.location.data
                datereported = form.datereported.data

                mrt = problemReq(problem, description, location, datereported, status)

                pList[id] = mrt

                db_read["problems"] = pList
                db_read.close()
                flash('Problem Resolved.', 'success')
            elif form.problem.data == 'sbus':
                print("resolved ")
                problem = form.problem.data
                description = form.description.data
                status = form.status.data
                location = form.location.data
                datereported = form.datereported.data
                bus = ProblemReq(problem, description, location, datereported, status)


                pList[id] = bus
                db_read["problems"] = pList
                db_read.close()

                flash('Problem resolved.', 'success')
            return redirect(url_for('Adminpage'))


            return render_template('Userpage.html', form=form)
    except:
        print("in ")
        pass



    #
    # if request.method == 'POST' and form.validate():
    #     if form.pubtype.data == 'smag':
    #         title = form.title.data
    #         type = form.pubtype.data
    #         category = form.category.data
    #         status = form.status.data
    #         frequency = form.frequency.data
    #         publisher = form.publisher.data
    #         created_by = "U0001"  # hardcoded value
    #
    #         mag = Magazine(title, publisher, status, created_by, category, type, frequency)
    #
    #         # create the magazine object
    #         mag_db = root.child('publications/' + id)
    #         mag_db.set({
    #                 'title': mag.get_title(),
    #                 'type': mag.get_type(),
    #                 'category': mag.get_category(),
    #                 'status': mag.get_status(),
    #                 'frequency': mag.get_frequency(),
    #                 'publisher': mag.get_publisher(),
    #                 'created_by': mag.get_created_by(),
    #                 'create_date': mag.get_created_date()
    #         })
    #
    #         flash('Magazine Updated Sucessfully.', 'success')
    #
    #     elif form.pubtype.data == 'sbook':
    #         title = form.title.data
    #         type = form.pubtype.data
    #         category = form.category.data
    #         status = form.status.data
    #         isbn = form.isbn.data
    #         author = form.author.data
    #         synopsis = form.synopsis.data
    #         publisher = form.publisher.data
    #         created_by = "U0001"  # hardcoded value
    #
    #         book = Book(title, publisher, status, created_by, category, type, synopsis, author, isbn)
    #         mag_db = root.child('publications/' + id)
    #         mag_db.set({
    #             'title': book.get_title(),
    #             'type': book.get_type(),
    #             'category': book.get_category(),
    #             'status': book.get_status(),
    #             'author': book.get_author(),
    #             'publisher': book.get_publisher(),
    #             'isbn': book.get_isbnno(),
    #             'synopsis': book.get_synopsis(),
    #             'created_by': book.get_created_by(),
    #             'create_date': book.get_created_date()
    #         })
    #
    #         flash('Book Updated Successfully.', 'success')
    #
    #     return redirect(url_for('viewpublications'))
    #
    # else:
    #     url = 'publications/' + id
    #     eachpub = root.child(url).get()
    #
    #     if eachpub['type'] == 'smag':
    #         magazine = Magazine(eachpub['title'], eachpub['publisher'], eachpub['status'],
    #                             eachpub['created_by'], eachpub['category'], eachpub['type'],
    #                             eachpub['frequency'])
    #
    #         magazine.set_pubid(id)
    #         form.title.data = magazine.get_title()
    #         form.pubtype.data = magazine.get_type()
    #         form.category.data = magazine.get_category()
    #         form.publisher.data =  magazine.get_publisher()
    #         form.status.data =  magazine.get_status()
    #         form.frequency.data = magazine.get_frequency()
    #     elif eachpub['type'] == 'sbook':
    #         book = Book(eachpub['title'], eachpub['publisher'], eachpub['status'],
    #                     eachpub['created_by'], eachpub['category'], eachpub['type'],
    #                     eachpub['synopsis'], eachpub['author'], eachpub['isbn'])
    #         book.set_pubid(id)
    #         form.title.data = book.get_title()
    #         form.pubtype.data = book.get_type()
    #         form.category.data = book.get_category()
    #         form.publisher.data = book.get_publisher()
    #         form.status.data = book.get_status()
    #         form.synopsis.data = book.get_synopsis()
    #         form.author.data = book.get_author()
    #         form.isbn.data = book.get_isbnno()
    #
    #     return render_template('update_publication.html', form=form)

if __name__ == '__main__':

    app.run()
# i show u sthplplokok