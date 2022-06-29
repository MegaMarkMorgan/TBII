from flask import Flask, request, url_for, redirect, render_template
from PIL import Image
from unsplash.api import Api
from unsplash.auth import Auth
import urllib.request

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('stage1'))
    return render_template('index.html')

@app.route("/stage1", methods=['GET', 'POST'])
def stage1():
    if request.method == 'POST':
        client_id = "bUzkAUmMw9KUjv-V5jsaWWXnWyZLwonnRLIQVi0hMZA"
        client_secret = ""
        redirect_uri = ""
        code = ""

        auth = Auth(client_id, client_secret, redirect_uri, code=code)
        api = Api(auth)

        pic = request.form.get("pic")

        img = str(api.photo.random(orientation = "squarish", query = "{} landscape".format(pic)))
        id = img.rstrip("')]").lstrip("[Photo(id='")

        urllib.request.urlretrieve("https://unsplash.com/photos/{}/download?force=true".format(id), "static/background.png")

        background = Image.open('static/background.png')
        new_image = background.resize((2048, 2048)).convert('RGBA')
        new_image.save('static/background.png')
        return redirect(url_for('stage2'))
    return render_template('stage1.html')

@app.route('/stage2', methods=['GET', 'POST'])
def stage2():
    if request.method == 'POST':
        return redirect(url_for('stage3'))
    return render_template('stage2.html')

@app.route('/stage3', methods=['GET', 'POST'])
def stage3():
    if request.method == 'POST':
        #avatar_name = request.form.get("name")
        skin = Image.open("static/{}.png".format(request.form.get("skin")))
        Image.alpha_composite(Image.open("static/background.png"), skin).save("static/Avatar_{}.png".format("avatar_name"))
        return redirect(url_for('stage4'))
    return render_template('stage3.html')

@app.route('/stage4', methods=['GET', 'POST'])
def stage4():
    if request.method == 'POST':
        clothes = Image.open("static/{}.png".format(request.form.get("clothes")))
        Image.alpha_composite(Image.open("static/Avatar_{}.png".format("avatar_name")), clothes).save("static/Avatar_{}.png".format("avatar_name"))
        return redirect(url_for('stage5'))
    return render_template('stage4.html')

@app.route('/stage5', methods=['GET', 'POST'])
def stage5():
    if request.method == 'POST':
        hair = Image.open("static/{}.png".format(request.form.get("hair")))
        Image.alpha_composite(Image.open("static/Avatar_{}.png".format("avatar_name")), hair).save("static/Avatar_{}.png".format("avatar_name"))
        return redirect(url_for('stage6'))
    return render_template('stage5.html')

@app.route('/stage6', methods=['GET', 'POST'])
def stage6():
    if request.method == 'POST':
        eyes = Image.open("static/{}.png".format(request.form.get("eyes")))
        Image.alpha_composite(Image.open("static/Avatar_{}.png".format("avatar_name")), eyes).save("static/Avatar_{}.png".format("avatar_name"))
        return redirect(url_for('stage7'))
    return render_template('stage6.html')

@app.route('/stage7', methods=['GET', 'POST'])
def stage7():
    if request.method == 'POST':
        mouth = Image.open("static/{}.png".format(request.form.get("mouth")))
        Image.alpha_composite(Image.open("static/Avatar_{}.png".format("avatar_name")), mouth).save("static/Avatar_{}.png".format("avatar_name"))
        return redirect(url_for('stage8'))
    return render_template('stage7.html')

@app.route('/stage8', methods=['GET', 'POST'])
def stage8():
    if request.method == 'POST':
        acc = Image.open("static/{}.png".format(request.form.get("acc")))
        Image.alpha_composite(Image.open("static/Avatar_{}.png".format("avatar_name")), acc).save("static/Avatar_{}.png".format("avatar_name"))
        return redirect(url_for('stage9'))
    return render_template('stage8.html')

@app.route('/stage9', methods=['GET', 'POST'])
def stage9():
    return render_template('stage9.html')




if __name__ == '__main__':
    app.run()
