# Tercino
Specific conversion of xlsx files to csv

You can run only the script locally, then you need to set the variables directly inside data_transform.py.
Variables: source, target, config file to be used (there are examples).

Easier way is to run flask application (my_flask.py). After starting it you open http://127.0.0.1:5000/, you will see windows to upload the files, after you select files, press "Do toho!" and the transformation process starts. In case of big files it takes a few minutes, up to cca 30, so just wait. When finished, the new csv is automatically downloaded. You will find it in your "Downloads" folder under the same name as the source (just the extension is different - .csv).

Requrements:
flask
pandas
datetime
csv
xlrd
