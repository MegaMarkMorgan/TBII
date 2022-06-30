from flask import Flask, request, url_for, redirect, render_template
from PIL import Image
from unsplash.api import Api
from unsplash.auth import Auth
import urllib.request
import sqlite3
import random

app = Flask(__name__)

#Start Page
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('stage1'))
    return render_template('index.html')

#stage1: Background image using unsplash API
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

        #blacklist check
        conn = sqlite3.connect('background_blacklist.db')
        cur = conn.cursor()
        cur.execute("SELECT rowid FROM ids WHERE unsplash_id = ?", (id,))
        data=cur.fetchall()

        while len(data)==1:
            img = str(api.photo.random(orientation = "squarish", query = "{} landscape".format(pic)))
            id = img.rstrip("')]").lstrip("[Photo(id='")

        else:
            urllib.request.urlretrieve("https://unsplash.com/photos/{}/download?force=true".format(id), "static/background.png")
            background = Image.open('static/background.png')
            new_image = background.resize((2048, 2048)).convert('RGBA')
            new_image.save('static/background.png')

            cur.execute("INSERT INTO ids (unsplash_id) VALUES (?)",(id,))
            conn.commit()
            conn.close()
            return redirect(url_for('stage1_idcheck'))
    return render_template('stage1.html')

#ask for user feedback regarding background image
@app.route('/stage1_idcheck', methods=['GET', 'POST'])
def stage1_idcheck():
    if request.method == 'POST':
        if request.form.get('start') == 'start':
            conn = sqlite3.connect('background_blacklist.db')
            cur = conn.cursor()
            cur.execute("DELETE FROM ids WHERE rowid = (SELECT MAX(rowid) FROM ids)")
            conn.commit()
            conn.close()
            return redirect(url_for('stage2'))
        elif  request.form.get('block') == 'block':
            return redirect(url_for('stage1'))
    return render_template('stage1_idcheck.html')

#stage2: Optional Randomizer
@app.route('/stage2', methods=['GET', 'POST'])
def stage2():
    if request.method == 'POST':
        if request.form.get('create') == 'create':
            return redirect(url_for('stage3'))
        elif  request.form.get('random') == 'random':
            conn = sqlite3.connect('assets_database.db')
            cur = conn.cursor()

            cur.execute("SELECT * FROM skin ORDER BY RANDOM() LIMIT 1")
            rand_skin = cur.fetchone()
            skin = Image.open("{}".format(rand_skin[0]))
            Image.alpha_composite(Image.open("static/background.png"), skin).save("static/Avatar.png")

            cur.execute("SELECT * FROM clothes ORDER BY RANDOM() LIMIT 1")
            rand_clothes = cur.fetchone()
            clothes = Image.open("{}".format(rand_clothes[0]))
            Image.alpha_composite(Image.open("static/Avatar.png"), clothes).save("static/Avatar.png")

            cur.execute("SELECT * FROM hair ORDER BY RANDOM() LIMIT 1")
            rand_hair = cur.fetchone()
            hair = Image.open("{}".format(rand_hair[0]))
            Image.alpha_composite(Image.open("static/Avatar.png"), hair).save("static/Avatar.png")

            cur.execute("SELECT * FROM eyes ORDER BY RANDOM() LIMIT 1")
            rand_eyes = cur.fetchone()
            eyes = Image.open("{}".format(rand_eyes[0]))
            Image.alpha_composite(Image.open("static/Avatar.png"), eyes).save("static/Avatar.png")

            cur.execute("SELECT * FROM mouth ORDER BY RANDOM() LIMIT 1")
            rand_mouth = cur.fetchone()
            mouth = Image.open("{}".format(rand_mouth[0]))
            Image.alpha_composite(Image.open("static/Avatar.png"), mouth).save("static/Avatar.png")

            cur.execute("SELECT * FROM acc ORDER BY RANDOM() LIMIT 1")
            rand_acc = cur.fetchone()
            acc = Image.open("{}".format(rand_acc[0]))
            Image.alpha_composite(Image.open("static/Avatar.png"), acc).save("static/Avatar.png")

            conn.commit()
            conn.close()
            return redirect(url_for('stage9'))
    return render_template('stage2.html')

#Stage3: Choose skin
@app.route('/stage3', methods=['GET', 'POST'])
def stage3():
    if request.method == 'POST':
        skin = Image.open("static/{}.png".format(request.form.get("skin")))
        Image.alpha_composite(Image.open("static/background.png"), skin).save("static/Avatar.png")
        return redirect(url_for('stage4'))
    return render_template('stage3.html')

#Stage4: Choose clothes
@app.route('/stage4', methods=['GET', 'POST'])
def stage4():
    if request.method == 'POST':
        clothes = Image.open("static/{}.png".format(request.form.get("clothes")))
        Image.alpha_composite(Image.open("static/Avatar.png"), clothes).save("static/Avatar.png")
        return redirect(url_for('stage5'))
    return render_template('stage4.html')

#Stage5: Choose hair color or Hijab
@app.route('/stage5', methods=['GET', 'POST'])
def stage5():
    if request.method == 'POST':
        hair_color = request.form.get("hair_color")
        if hair_color == 'hijab':
            Image.alpha_composite(Image.open("static/Avatar.png"), Image.open("static/hijab.png")).save("static/Avatar.png")
            return redirect(url_for('stage6'))
        elif hair_color == 'black':
            return redirect(url_for('stage5_black'))
        elif hair_color == 'blond':
            return redirect(url_for('stage5_blond'))
        elif hair_color == 'brown':
            return redirect(url_for('stage5_brown'))
        elif hair_color == 'red':
            return redirect(url_for('stage5_red'))
    return render_template('stage5.html')

#Stage5 black: Choose black hair style
@app.route('/stage5_black', methods=['GET', 'POST'])
def stage5_black():
    if request.method == 'POST':
        hair_style_black = Image.open("static/{}.png".format(request.form.get("hair_style_black")))
        Image.alpha_composite(Image.open("static/Avatar.png"), hair_style_black).save("static/Avatar.png")
        return redirect(url_for('stage6'))
    return render_template('stage5_black.html')

#Stage5 blond: Choose blond hair style
@app.route('/stage5_blond', methods=['GET', 'POST'])
def stage5_blond():
    if request.method == 'POST':
        hair_style_blond = Image.open("static/{}.png".format(request.form.get("hair_style_blond")))
        Image.alpha_composite(Image.open("static/Avatar.png"), hair_style_blond).save("static/Avatar.png")
        return redirect(url_for('stage6'))
    return render_template('stage5_blond.html')

#Stage5 brown: Choose brown hair style
@app.route('/stage5_brown', methods=['GET', 'POST'])
def stage5_brown():
    if request.method == 'POST':
        hair_style_brown = Image.open("static/{}.png".format(request.form.get("hair_style_brown")))
        Image.alpha_composite(Image.open("static/Avatar.png"), hair_style_brown).save("static/Avatar.png")
        return redirect(url_for('stage6'))
    return render_template('stage5_brown.html')

#Stage5 red: Choose red hair style
@app.route('/stage5_red', methods=['GET', 'POST'])
def stage5_red():
    if request.method == 'POST':
        hair_style_red = Image.open("static/{}.png".format(request.form.get("hair_style_red")))
        Image.alpha_composite(Image.open("static/Avatar.png"), hair_style_red).save("static/Avatar.png")
        return redirect(url_for('stage6'))
    return render_template('stage5_red.html')

#stage 6: Choose eyes
@app.route('/stage6', methods=['GET', 'POST'])
def stage6():
    if request.method == 'POST':
        eyes = Image.open("static/{}.png".format(request.form.get("eyes")))
        Image.alpha_composite(Image.open("static/Avatar.png"), eyes).save("static/Avatar.png")
        return redirect(url_for('stage7'))
    return render_template('stage6.html')

#stage 7: Choose mouth
@app.route('/stage7', methods=['GET', 'POST'])
def stage7():
    if request.method == 'POST':
        mouth = Image.open("static/{}.png".format(request.form.get("mouth")))
        Image.alpha_composite(Image.open("static/Avatar.png"), mouth).save("static/Avatar.png")
        return redirect(url_for('stage8'))
    return render_template('stage7.html')

#stage 8: Choose accessories
@app.route('/stage8', methods=['GET', 'POST'])
def stage8():
    if request.method == 'POST':
        acc = Image.open("static/{}.png".format(request.form.get("acc")))
        Image.alpha_composite(Image.open("static/Avatar.png"), acc).save("static/Avatar.png")
        return redirect(url_for('stage9'))
    return render_template('stage8.html')

#stage 9: Final image + download
@app.route('/stage9', methods=['GET', 'POST'])
def stage9():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('stage9.html')

if __name__ == '__main__':
    app.run()
