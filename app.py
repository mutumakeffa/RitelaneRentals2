import os
from os.path import join, dirname, realpath
import pymysql as pymysql
from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

#we want to upload the image
from werkzeug.utils import secure_filename


app = Flask(__name__)

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/')  # create path where the image file will be saved
# specify allowed extensions
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# configure upload folder in the app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

connection = pymysql.connect("207.148.17.93", "root", os.getenv("DB_PASSWORD"), "ritelane_db")

# this function is used to check if the allowed image extensions has been met
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/admin')
def admin():
    return render_template('admin2.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email_add = request.form['email_add']

        cursor = connection.cursor()

        sql = """INSERT INTO tbl_emails(emails) VALUES(%s)"""

        try:
            cursor.execute(sql, email_add)
            connection.commit()
            return redirect('https://turo.com/c/kenm356')
        except:
            connection.commit()
            return render_template('index.html')


# make route aware of methods to be received
@app.route('/post', methods=['POST', 'GET'])
def post():

        # we first have to check the methods sent either POST or Get so that we can extract the data sent. We do this by importing a module called request
        if request.method == 'POST':
            car_name1 = request.form['car_name1']
            car_desc1 = request.form['car_desc1']
            file1 = request.files['file1']  # receive file
            turo_link = request.form['turo_link']

            # check if file is present and allowed
            if file1 and allowed_file(file1.filename):
                filename = secure_filename(file1.filename)
                # save the file with its filename
                file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                # once the file is saved, save the link to the db

            # now we want to save this data in the database hence we have to import pymysql as the connector to the sql
            # connection = pymysql.connect("localhost", "root", "", "ritelane_db")

            # connection has true or false connection
            # create a cursor and use it to execute SQL --- Cursor helps to execute sql

            cursor = connection.cursor()

            sql = """INSERT INTO tbl_carcollection( car_name, car_desc, image, turo_link) VALUES (%s,%s,%s,%s)"""

            try:
                cursor.execute(sql, (car_name1, car_desc1, filename, turo_link))
                connection.commit()
                return render_template('admin2.html', msg="Car added successfully, add another")
            except:
                connection.commit()
                return redirect('/view')

        else:
            return render_template('admin2.html', msg2="No data entered yet")


@app.route('/view')
def view():

    cursor = connection.cursor()

    sql = """SELECT * FROM tbl_carcollection"""

    cursor.execute(sql)

    # fetch rows
    rows = cursor.fetchall()  # rows can contain 0,1 or more rows

    # perform a row count
    if cursor.rowcount == 0:
        return render_template('view_collection.html', msg='No records')
    else:
        return render_template('view_collection.html', data=rows)

@app.route('/emails')
def emails():

    cursor = connection.cursor()

    sql = """SELECT * FROM tbl_emails"""

    cursor.execute(sql)

    # fetch rows
    rows = cursor.fetchall()  # rows can contain 0,1 or more rows

    # perform a row count
    if cursor.rowcount == 0:
        return render_template('admin2.html', msg='No records')
    else:
        return render_template('admin2.html', data=rows)


if __name__ == '__main__':
    app.debug == True
    app.run()
