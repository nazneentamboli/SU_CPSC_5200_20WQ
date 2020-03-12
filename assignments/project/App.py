import os
import time
from flask import Flask,request, send_from_directory, render_template, abort
from PIL import Image

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/imageProcessor', methods=['POST'])
def imageProcessor():
    requests = request.form['requests']
    #upload file
    target = os.path.join(UPLOAD_FOLDER, 'static/db')

    # create image directory if not found
    if not os.path.isdir(target):
        os.mkdir(target)

    # retrieve file from html file-picker
    upload = request.files['file']
    print("File name: {}".format(upload.filename))
    filename = upload.filename

    # file support verification
    ext = os.path.splitext(filename)[1]
    if (ext == ".jpg") or (ext == ".png") or (ext == ".jpeg"):
        print("File accepted")
    else:
        abort(400)

    # save original file 
    sourceFile = "/".join([target, filename])
    if os.path.isfile(sourceFile):
        filename = str(time.time()) + " " + filename
        sourceFile = "/".join([target, filename])
    print("File saved to to:", sourceFile)
    upload.save(sourceFile)

     # open and process image
    requestList = requests.split(",")
    print(requestList)
    img = Image.open(sourceFile)

    # modify image
    for operation in requestList: 
        print(operation)
        each = operation.split("_")
        if each[0] == 'flip':
            img = flip(each[1], img, sourceFile)
        elif each[0] == 'rotate':
            img = rotate(each[1],img, sourceFile)
        elif each[0] == 'grayscale':
            img = color(img, sourceFile) 
        elif each[0] == 'thumbnail':
            img = thumbnail(img, sourceFile)
        elif each[0] == 'w':
            img = resize_w(each[1], img, sourceFile)
        elif each[0] == 'h':
            img = resize_h(each[1], img, sourceFile)
        else:
            abort(400)

    # save modified file 
    filename = "new " + filename
    print(filename)
    destination = "/".join([target, filename])
    img.save(destination)
    return send_from_directory("static/db", filename)

def flip(mode, img, sourceFile):
    if mode == 'h':
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
        print("flip ho succeed")
    elif mode == 'v':
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        print("flip ve succeed")
    else:
        abort(400)
    return img

def rotate(angle, img, sourceFile):
    print(angle)
    #img = img.rotate(-1*int(angle),resample=0, expand=True)
    if(angle=="left"):
        img = img.rotate(90,resample=0, expand=True)
    elif (angle == "right"):
        img = img.rotate(-1*90,resample=0, expand=True)
    else:
        img = img.rotate(int(angle),resample=0, expand=True)
    print("rotate succeed")

    return img

def color(img, sourceFile):
    img = img.convert(mode="L")
    print("grey succeed")
    return img

def thumbnail(img,sourceFile):
    img = img.resize((200, 200))  
    print("thumbnail succeed")
    return img

def resize_w(width, img, sourceFile):
    if int(width) > 0:
        w, h = img.size
        img = img.resize((int(width), int(h)))
        print("resize succeed")
    else:
        abort(400)
    return img

def resize_h(height, img, sourceFile):
    if int(height) > 0:
        w, h = img.size
        img = img.resize((int(w), int(height)))
        print("resize succeed")
    else:
        abort(400)
    return img

if __name__ == '__main__':
	app.run(debug=True)
