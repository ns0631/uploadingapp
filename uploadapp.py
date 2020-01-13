from flask import Flask, render_template, request
import requests, json, os, datetime, sys, flask, flask_uploads
from flask_uploads import UploadSet, configure_uploads, IMAGES, TEXT

#Instance is made
app = Flask(__name__)

#Upload setting is set
type_of_upload = UploadSet('text', TEXT)

#Upload configuration and destination are set
app.config['UPLOADED_TEXT_DEST'] = 'your_text_uploads'
configure_uploads(app, type_of_upload)

@app.route('/')
def home():
    #Home page is displayed
    return render_template('uploadhome.html')

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        try:
            #File is retrieved by key and saved
            filename = type_of_upload.save(request.files['user_text_file'])
        except flask_uploads.UploadNotAllowed:
            #If the file's format is not plain text, the user will be told
            return render_template('uploadforbidden.html')
        else:
            #All uploads are listed
            all_uploads = os.listdir('your_text_uploads')
            upload_dict = dict()

            #The list of uploads is passed as a parameter for the uploads page
            for upload_index, each_upload in enumerate(all_uploads):
                upload_dict[upload_index] = each_upload
            return render_template('uploads.html', result=upload_dict)

@app.route('/open_upload', methods=['POST', 'GET'])
def open_upload():
    if request.method == 'POST':
        #Gets the file path to the user's file
        file_path = 'your_text_uploads/' + request.form['requestedfile'][:-1]

        #Reads the file
        text_file = open(file_path, 'r')
        file_contents = text_file.read()
        text_file.close()

        #Opens a html page that displays the text file's contents
        return render_template('displayfile.html', result={request.form['requestedfile'][:-1]: file_contents})

if __name__ == '__main__':
    #App is run
    app.run(debug=True)
