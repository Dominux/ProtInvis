from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired
from constants import dyes_for_form

class AAForm(FlaskForm):
	uniprot_id = StringField('Uniprot id', validators=[DataRequired()])
	the_dye = SelectField('Краситель', choices=dyes_for_form)
	