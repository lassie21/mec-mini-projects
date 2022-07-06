To run this app, open an anaconda cmd terminal if on windows:
1. Paste the following:
    cd PycharmProjects/mec-mini-projects/flask_deploy
    set FLASK_APP=flask_deploy/request_rfr
    set FLASK_ENV=development
    flask run
1a. if on linux system, replace "set" in the previous commands with "export"
2. input sequencing output array from Roche Sequencing Solutions HTP run
2a. Try uploading sample_run_data.csv to test the app
3. app will output expected read length, MT score, and accuracy
