from app import app, db
from flask import render_template, redirect, url_for, flash
from app.forms import AddInfo
from app.models import User

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/addinfo', methods=["GET", "POST"])
def addinfo():
    forms = AddInfo()
    if forms.validate_on_submit():
        print('All Information Submitted')
        first = forms.first_name.data
        last = forms.last_name.data
        number = forms.number.data
        address = forms.address.data

        print(first, last, number, address)
        #checks to see if address is already in the phonebook
        check_address =  User.query.filter(( User.number == number) | ( User.address == address)).all()
        if check_address:
            # Flash a message saying that user with email/username already exists
            flash("Your information has already been added to the Address Book!", "warning")
            return redirect(url_for('addinfo'))
        # If check_user is empty, create a new record in the user table
        new_user = User(first=first, last=last, number=number, address=address)
        flash(f"Thank you {first} {last} for adding your information to our Address Book!", "success")
        return redirect(url_for('index'))
    return render_template('add_info.html', forms=forms)
