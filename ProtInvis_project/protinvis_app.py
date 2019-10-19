from flask import Flask, render_template, redirect, url_for, session
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
            session['graphJSON'] = graphJSON
            return redirect(url_for('result'))
        else:
            if len(graphJSON) > 15:
                graphJSON = f"{graphJSON[:12]}..."
            form.uniprot_id.errors.append(f"«{graphJSON}» не найдено")

    return render_template('index.html', form=form)

@app.route('/result', methods=['GET', 'POST'])
def result():
    graphJSON = session.get('graphJSON', None)
    if graphJSON is None:
        return redirect(url_for('index'))
    return render_template('result.html', graphJSON=graphJSON)

if __name__ == '__main__':
	app.run(debug=False)
