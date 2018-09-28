from flask import Flask, render_template, flash, url_for, redirect
from flask_wtf import FlaskForm
# see some new ones... + ValidationError
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import Required, Length, Regexp

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
# Can be whatever for us, for now; this is what 'seeds' the CSRF protection
app.config['SECRET_KEY'] = 'hard to guess string'
app.debug = True

####################
###### FORMS #######
####################


class SecretClubForm(FlaskForm):
    name = StringField("Enter the name of your secret club:", validators=[
                       Required(), Length(3, 64)])  # Must be at least 3 and no more than 64 chars
    number_members = StringField("How many people may be in this secret club (must enter an integer):", validators=[
                                 Required(), Regexp('^\d+$')])  # Validated with a regular expression: only digits
    # Required, plus the below validator...
    passcode = StringField(
        "What is the secret code to enter the secret society? Must not have any vowels.", validators=[Required()])
    submit = SubmitField('Submit')

    def validate_passcode(self, field):
        # Replace comments w code here...
        # With code here -- I had 2 lines above the code already provided to make it so that this validator would reject anything with vowels.
        # Could also do it in 1 line.
        vowels = ['a', 'e', 'i', 'o', 'u']
        for ch in field.data:
            if ch in vowels:
                raise ValidationError(
                    "Your passcode was not valid because there was at least 1 vowel in it.")

####################
###### ROUTES ######
####################


@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/form')
def form_entry():
    form = SecretClubForm()
    return render_template('form.html', form=form)


@app.route('/answers', methods=['GET', 'POST'])
def show_answers():
    form = SecretClubForm()
    if form.validate_on_submit():
        name = form.name.data
        passcode = form.passcode.data
        capacity = form.number_members.data
        return render_template('results.html', name=name, passcode=passcode, capacity=capacity)
    flash(form.errors)
    return redirect(url_for('form_entry'))


if __name__ == "__main__":
    app.run(use_reloader=True, debug=True)
