from flask import Flask, render_template
from flask_wtf import FlaskForm
import json
import csv
import logging as log 
import itertools
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

app = Flask(__name__,template_folder='template')

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'input' 

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])  
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET',"POST"])  
@app.route('/home', methods=['GET',"POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data 
        log.info("Grabbing the file from the server")
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        log.info("Saving the file to the directory")
        filestream = form.file.data
        filestream.seek(0)
        new_data = convert_data(filestream.filename)
        return new_data
    #return render_template('data.html', datas=datas)

    return render_template('index.html', form=form)

def convert_data(filestream):
    filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],filestream)
    with open(filepath, newline='') as s:
        rows = list(csv.reader(s))
        r = cluster(rows) 
        data = json.dumps(r, indent=1)
    return data


def cluster(rows):
    result = []
    for key, group in itertools.groupby(rows, key=lambda rows: rows[0]):
        group_rows = [row[1:] for row in group]
        if len(group_rows[0]) == 2:
            result.append({key: dict(group_rows)})
        else:
            result.append({key: cluster(group_rows)})
    return result




if __name__ == '__main__':
    app.run(debug=True)