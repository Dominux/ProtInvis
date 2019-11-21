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
        graphJSON = ploter(form.uniprot_id.data, form.the_dye.data)

        if graphJSON.startswith('{'):
            return render_template('result.html', graphJSON=graphJSON, form=form)
        
        else:
            if len(graphJSON) > 15:
                graphJSON = f"{graphJSON[:12]}..."
            form.uniprot_id.errors.append(f"«{graphJSON}» не найдено")

    return render_template('index.html', form=form)

if __name__ == '__main__':
	app.run(debug=False)
