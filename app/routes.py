from app import app
from flask import render_template, redirect, url_for, flash
from fake_data import info
from app.forms import AddInfo

@app.route('/')
def index():
    return render_template('index.html', posts=info)


@app.route('/addinfo', methods=["GET", "POST"])
def addinfo():
    forms = AddInfo()
    if forms.validate_on_submit():
        print('All Information Submitted')
        first = forms.first_name.data
        last = forms.last_name.data
        number = forms.number.data
        address = forms.address.data
        city = forms.city.data
        state = forms.state.data
        zip_code = forms.zip_code.data

        print(first, last, number, address, city, state, zip_code)
        flash(f"Thank you {first} {last} for adding your information to our Address Book!", "success")
        return redirect(url_for('index'))
    return render_template('add_info.html', forms=forms)
