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
        new_user = Person(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        flash(f"Thank you {new_user.username} for signing up!", "success")
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
    flash("You have logged out", "success")
    return redirect(url_for('index'))


@app.route('/addinfo', methods=["GET", "POST"])
@login_required
def addinfo():
    form = AddInfo()
    if form.validate_on_submit():
        print('All Information Submitted')
        first = form.first_name.data
        last = form.last_name.data
        number = form.number.data
        address = form.address.data

        print(first, last, number, address)
        #checks to see if address is already in the phonebook
        check_address =  User.query.filter(( User.number == number) | ( User.address == address)).all()
        if check_address:
            flash("Your information has already been added to the Address Book!", "warning")
            return redirect(url_for('addinfo'))
        new_info = User(first=first, last=last, number=number, address=address, person_id=current_user.id)
        flash(f"Thank you {first} {last} for adding your information to our Address Book!", "success")
        return redirect(url_for('index'))
    return render_template('add_info.html', form=form)

@app.route('/edit/<information_id>', methods=["GET", "POST"])
@login_required
def edit(information_id):
    form=AddInfo()
    info_to_edit = User.query.get_or_404(information_id)

    if form.validate_on_submit():
        info_to_edit.first = form.first_name.data
        info_to_edit.last = form.last_name.data
        info_to_edit.number = form.number.data
        info_to_edit.address = form.address.data
        db.session.commit()
        flash(f"{info_to_edit.first} {info_to_edit.last} | {info_to_edit.number} | {info_to_edit.address} has been edited!", "success")
        return redirect(url_for('index'))
    form.first_name.data = info_to_edit.first
    form.last_name.data = info_to_edit.last
    form.number.data = info_to_edit.number
    form.address.data = info_to_edit.address
    return render_template('edit.html', form=form, information=info_to_edit)


@app.route('/delete/<information_id>', methods=["GET", "POST"])
@login_required
def delete(information_id):
    post_to_delete = User.query.get_or_404(information_id)
    if post_to_delete.person_id != current_user.id:
        flash("You do not have permission to delete this information!", "danger")
        return redirect(url_for('index'))
    db.session.delete(post_to_delete)
    db.session.commit()
    flash(f"{post_to_delete.first} {post_to_delete.last} | {post_to_delete.number} | {post_to_delete.address} has been deleted!", "success")
    return redirect(url_for('index'))
