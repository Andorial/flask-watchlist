from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange

#Login
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


#Registration
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", 
                                     validators=[DataRequired(), EqualTo("password", message="Passwords must match")])
    submit = SubmitField("Register")


#Add movie/series
class AddItemForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=200)])
    genre = StringField("Genre", validators=[Length(max=100)])
    rating = StringField("Rating (e.g. IMDb)", validators=[Length(max=50)])
    comment = TextAreaField("Comment")
    submit = SubmitField("Add")


#Update watched
class UpdateWatchedForm(FlaskForm):
    comment = TextAreaField("Comment")
    my_rating = IntegerField("My Rating (1-10)", validators=[NumberRange(min=1, max=10)])
    submit = SubmitField("Update")
