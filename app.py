import os
from flask import Flask, render_template, request, Response
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont
import tempfile
import io

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scribble", methods=["POST"])
def scribble():
    file = request.files["file"]
    temp = tempfile.mktemp()
    os.mkdir(temp)
    file_path = os.path.join(temp, file.name)

    file.stream.seek(0)
    file.save(file_path)
    file.close()

    img = Image.open(file_path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(r"static/fonts/sauce_code_pro.ttf", 50)
    draw.text((5, 5), "Peter Sux", font=font, align="left", fill="black")
    buf = io.BytesIO()
    img.save(buf, format="PNG")

    if os.path.exists(file_path):
        os.remove(file_path)

    return Response(buf.getvalue(), mimetype="image/png")


if __name__ == "__main__":
    app.run()
