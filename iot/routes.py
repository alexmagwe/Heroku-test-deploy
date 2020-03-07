from iot import app, db, bcrypt
from flask import Flask, render_template, url_for, redirect, flash
from flask_login import login_user, current_user, logout_user, login_required
from iot.forms import LoginForm, RegisterationForm
from iot.models import Users, Devices

@app.route('/')
@app.route('/main')
@login_required
def main():
    device = Devices.query.all()
    return render_template('main.html', device=device ,title = 'Smart Street Lights/Main')

@app.route('/login', methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main'))
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else  redirect(url_for('main'))
		else:
			flash('login was unsuccessful. Please check your Email and Password','danger')
	return render_template('login.html', form=form ,title = 'Smart Street Lights/Sign In')


@app.route('/register', methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main'))
	form = RegisterationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = Users(username=form.username.data,email=form.email.data,password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Registered succesfully', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Smart Street Lights/Sign Up', form=form)

@app.route('/logout')
def logout():
    login_user()
    return redirect(url_for('login'))
