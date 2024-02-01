from flask import Blueprint, render_template, request, redirect
from flask import current_app
from werkzeug.utils import secure_filename
import os, subprocess

views = Blueprint(__name__, "views")

@views.route("/", methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        print(request.files)
        image = request.files['file']

        if image.filename == '':
            print("no file selected")
            return redirect(request.url)
        
        # find directory where you want to save image
        filename = secure_filename(image.filename)
        basedir = os.path.abspath(os.path.dirname(__file__))
        image.save(os.path.join(basedir, current_app.config["IMAGE_UPLOAD"], filename))

        # if there is an issue running read_text.py, exit program
        try:
            subprocess.run(['python', 'notionapi.py'], check=True, text=True)

        except subprocess.CalledProcessError as e:
            print(e)
            print("error running notionapi.py")

    return render_template("index.html")