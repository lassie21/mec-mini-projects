import numpy as np
from flask import Flask, request, jsonify, render_template, session
import pickle
import os
import pandas as pd

app = Flask(__name__, static_folder='staticFiles')
path = 'C:/Users/Nai/PycharmProjects/mec-mini-projects/'
model = pickle.load(open(path + '/flask_deploy/finalized_seq_model.sav', 'rb'))
# Define folder to save uploaded files to process further
UPLOAD_FOLDER = os.path.join('flask_deploy', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'

# Define allowed files (for this example I want only csv file)
ALLOWED_EXTENSIONS = {'csv'}

@app.route('/')
def index():
    return render_template('upload_and_show_page.html')

@app.route('/', methods=("POST", "GET"))
def uploadFile():
    if request.method == 'POST':
        # upload file flask
        uploaded_df = request.files['uploaded-file']

        # Extracting uploaded data file name
        data_filename = uploaded_df.filename

        # flask upload file to database (defined uploaded folder in static path)
        uploaded_df.save(os.path.join(app.config['UPLOAD_FOLDER'], data_filename))

        # Storing uploaded file path in flask session
        session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], data_filename)

        return render_template('upload_and_show_page2.html')


@app.route('/show_data')
def showData():
    # Retrieving uploaded file path from session
    data_file_path = session.get('uploaded_data_file_path', None)

    # read csv file in python flask (reading uploaded csv file from uploaded server location)
    uploaded_df = pd.read_csv(data_file_path)

    # pandas dataframe to html table flask
    pred = model.predict(uploaded_df[model.feature_names])
    #denormalize values
    pred[0][0] = pred[0][0] * 33520362.0
    pred[0][1] = pred[0][1] * 1527.0
    pred[0][2] = pred[0][2] * (100.0 - 60.31745910644531) + 60.31745910644531
    uploaded_df_html = pd.DataFrame(pred, columns=['Num Align Hqmt','Mode Mt Base Call Read Length Align Hqmt','Avg Mt Align Edit Percent Identical']).to_html()
    return render_template('show_csv_data.html', data_var=uploaded_df_html)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
