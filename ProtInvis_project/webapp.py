from flask import Flask, render_template, url_for
from forms import AAForm
from create_plot import ploter
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)

@app.route('/', methods=['GET', 'POST']) 
def index():
	form = AAForm()
	
	if form.validate_on_submit():
		graphJSON = ploter(form.uniprot_ids.data, form.the_dye.data)
		return render_template('result.html', graphJSON=graphJSON)

	return render_template('index.html', form=form)

@app.route('/about', methods=['GET']) 
def about():
	return render_template('about.html')

@app.route('/references', methods=['GET']) 
def references():
	return render_template('references.html')

if __name__ == '__main__':
	app.run(debug=True)
