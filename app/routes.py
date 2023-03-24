from app import app, db
from flask import render_template, redirect, url_for, flash
from app.forms import SignUpForm, LoginForm, AddInfo
from app.models import User, Person
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
def index():
    info = User.query.all()
    return render_template('index.html', info=info)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('Hooray our form was validated!!')
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(first_name, last_name, email, username, password)
        check_user = db.session.execute(db.select(Person).filter((Person.username == username) | (Person.email == email))).scalars().all()
        if check_user:
            flash("That username already exists!", "warning")
            return redirect(url_for('signup'))
        # If check_user is empty, create a new record in the user table
        new_user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        flash(f"Thank you {new_user.username} for signing up for our Address Book!", "success")
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('Form Validated :)')
        username = form.username.data
        password = form.password.data
        print(username, password)
        person = Person.query.filter_by(username=username).first()
        if person is not None and person.check_password(password):
            login_user(person)
            flash(f'You have logged in as {username}', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username and/or password!', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have logged out", "info")
    return redirect(url_for('index'))


@app.route('/addinfo', methods=["GET", "POST"])
def addinfo():
    forms = AddInfo()
    if forms.validate_on_submit():
        print('All Information Submitted')
        first_name = forms.first_name.data
        last_name = forms.last_name.data
        number = forms.number.data
        address = forms.address.data

        print(first_name, last_name, number, address)
        #checks to see if address is already in the phonebook
        check_address =  User.query.filter(( User.number == number) | ( User.address == address)).all()
        if check_address:
            flash("Your information has already been added to the Address Book!", "warning")
            return redirect(url_for('addinfo'))
        new_user = User(first_name=first_name, last_name=last_name, number=number, address=address)
        flash(f"Thank you {first_name} {last_name} for adding your information to our Address Book!", "success")
        return redirect(url_for('index'))
    return render_template('add_info.html', forms=forms)
