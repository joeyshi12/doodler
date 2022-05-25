import os
import io
import tempfile
from flask import Flask, render_template, request, Response, jsonify
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont

from werkzeug.datastructures import FileStorage

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scribble", methods=["POST"])
def scribble():
    if "image" not in request.files:
        return jsonify({"message": "image not found in files"}), 500
    try:
        buffer = __process_image(request.files["image"])
        return Response(buffer.getvalue(), mimetype="image/png")
    except:
        return jsonify({"message": "error in processing image"}), 500


def __process_image(file: FileStorage) -> io.BytesIO:
    tempdir_name = tempfile.mkdtemp()
    file_path = os.path.join(tempdir_name, file.name)
    file.stream.seek(0)
    file.save(file_path)
    file.close()

    image = Image.open(file_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(r"static/fonts/sauce_code_pro.ttf", 50)
    draw.text((5, 5), "Peter Sux", font=font, align="left", fill="black")

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")

    if os.path.exists(file_path):
        os.remove(file_path)
        os.rmdir(tempdir_name)

    return buffer


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
