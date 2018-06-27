from app import app
from flask import render_template, url_for, flash, redirect
from app.models import User, Post
from app.forms import RegistrationForm, LoginForm




posts = [
    {
        'author': 'Leo Igane',
        'title': 'Minute Pitch 1',
        'content': 'First pitch content',
        'date_posted': 'April 20, 20018'
    },
    {
    'author': 'Njeri Igane',
    'title': 'Minute Pitch 2',
    'content': 'Second pitch content',
    'date_posted': 'April 21, 20018'
    }
    ]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts = posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)
