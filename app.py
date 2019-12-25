import os
import zipfile

from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
root = os.getcwd() + "/storage"
os.chdir(root)


@app.route("/")
def index():
    return render_template('file.html')


@app.route("/<string:username>/<int:product_id>", methods=["GET", "POST"])
def upload_image(username, product_id):
    username_cwd = root + "/" + username
    if username not in os.listdir(root):
        os.mkdir(username_cwd)

    os.chdir(username_cwd)
    product_cwd = username_cwd + "/" + str(product_id)
    if str(product_id) not in os.listdir(username_cwd):
        os.mkdir(product_cwd)

    os.chdir(product_cwd)

    try:
        if request.method == "POST":
            for f in request.files.getlist("images"):
                f.save(secure_filename(f.filename))
            return jsonify({"message": "Upload images successfully"}), 201
        elif request.method == "GET":
            with zipfile.ZipFile("images.zip", "w") as images_zip:
                for image in os.listdir(product_cwd):
                    if os.path.isfile(image) and image.endswith(".jpg"):
                        images_zip.write(image)
            return send_file(product_cwd + "/images.zip", attachment_filename="images.zip", as_attachment=True)
    except Exception as e:
        print(e)
        return jsonify({"message": "An internal error has occurred"}), 500
    finally:
        os.chdir(root)


@app.route("/<string:username>/avatar")
def avatar(username):
    username_cwd = root + "/" + username
    if username not in os.listdir(root):
        os.mkdir(username_cwd)

    os.chdir(username_cwd)
    avatar_cwd = username_cwd + "/avatar"
    if "avatar" not in os.listdir(username_cwd):
        os.mkdir(avatar_cwd)

    os.chdir(avatar_cwd)
    try:
        if request.method == "POST":
            for f in request.files["avatar"]:
                f.save(secure_filename(f.filename))
            return jsonify({"message": "Upload images successfully"}), 201
        elif request.method == "GET":
            return send_file(avatar_cwd + "/avatar.jpg", attachment_filename="avatar.jpg", as_attachment=True)
    except Exception as e:
        print(e)
        return jsonify({"message": "An internal error has occurred"}), 500
    finally:
        os.chdir(root)


if __name__ == '__main__':
    app.run(host="192.168.2.107", port=5000)
