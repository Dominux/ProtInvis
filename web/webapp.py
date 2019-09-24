from flask import Flask, render_template, send_file
from forms import AAForm
from create_plot import ploter
import os

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/', methods=['GET', 'POST']) 
def index():
	form = AAForm()
	if form.validate_on_submit():
		bytes_obj = ploter(form.uniprot_ids.data, form.the_dye.data)
		return send_file(bytes_obj, 
						 attachment_filename='plot.png', 
						 mimetype='image/png')
	return render_template('index.html', form=form)

if __name__ == '__main__':
	app.run(debug=True)
