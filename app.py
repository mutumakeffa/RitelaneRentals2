import os
from os.path import join, dirname, realpath
import pymysql as pymysql
from flask import Flask, render_template, request, redirect

#we want to upload the image
from werkzeug.utils import secure_filename


app = Flask(__name__)

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/')  # create path where the image file will be saved
# specify allowed extensions
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# configure upload folder in the app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024


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

        connection = pymysql.connect("localhost", "root", "", "ritelane_db")

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

            # check if file is present and allowed
            if file1 and allowed_file(file1.filename):
                filename = secure_filename(file1.filename)
                # save the file with its filename
                file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                # once the file is saved, save the link to the db

            # now we want to save this data in the database hence we have to import pymysql as the connector to the sql
            connection = pymysql.connect("localhost", "root", "", "ritelane_db")

            # connection has true or false connection
            # create a cursor and use it to execute SQL --- Cursor helps to execute sql

            cursor = connection.cursor()

            sql = """SELECT * FROM tbl_carcollection"""

            cursor.execute(sql)

            cursor.fetchall()

            if cursor.rowcount == 0:
                sql = """INSERT INTO tbl_carcollection( car_name, car_desc, image) VALUES (%s,%s,%s)"""
                cursor.execute(sql, (car_name1, car_desc1, filename))

                # commit/rollback -if the connection crashes before it commits, it should render back
                connection.commit()
                return redirect('/admin')
                # return render_template('add.html', msg="CONGRATS! SUCCESSFULLY SAVED")
            elif cursor.rowcount == 1:
                sql = """UPDATE tbl_carcollection SET car_name = [%s], car_desc = [%s], image = [%s] WHERE user_id = 1 """
                cursor.execute(sql, (car_name1, car_desc1, filename))

                connection.commit()
                return redirect('/admin')
            else:
                return redirect('admin')

        elif request.method == 'POST':
            car_name2 = request.form['car_name2']
            car_desc2 = request.form['car_desc2']
            file2 = request.files['file2']  # receive file

            # check if file is present and allowed
            if file2 and allowed_file(file2.filename):
                filename = secure_filename(file2.filename)
                # save the file with its filename
                file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                # once the file is saved, save the link to the db

            # now we want to save this data in the database hence we have to import pymysql as the connector to the sql
            connection = pymysql.connect("localhost", "root", "", "ritelane_db")

            # connection has true or false connection
            # create a cursor and use it to execute SQL --- Cursor helps to execute sql

            cursor = connection.cursor()

            sql = """SELECT * FROM tbl_carcollection2"""

            cursor.execute(sql)

            cursor.fetchall()

            if cursor.rowcount == 0:
                sql = """INSERT INTO tbl_carcollection2( car_name, car_desc, image) VALUES (%s,%s,%s)"""
                cursor.execute(sql, (car_name2, car_desc2, filename))

                # commit/rollback -if the connection crashes before it commits, it should render back
                connection.commit()
                return redirect('/update')
                # return render_template('add.html', msg="CONGRATS! SUCCESSFULLY SAVED")
            elif cursor.rowcount == 1:
                sql = """UPDATE tbl_carcollection2 SET car_name = [%s], car_desc = [%s], image = [%s] WHERE user_id = 1 """
                cursor.execute(sql, (car_name2, car_desc2, filename))

                connection.commit()
                return redirect('/admin')
            else:
                return redirect('admin')

        elif request.method == 'POST':
            car_name3 = request.form['car_name3']
            car_desc3 = request.form['car_desc3']
            file3 = request.files['file3']  # receive file

            # check if file is present and allowed
            if file3 and allowed_file(file3.filename):
                filename = secure_filename(file3.filename)
                # save the file with its filename
                file3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                # once the file is saved, save the link to the db

            # now we want to save this data in the database hence we have to import pymysql as the connector to the sql
            connection = pymysql.connect("localhost", "root", "", "ritelane_db")

            # connection has true or false connection
            # create a cursor and use it to execute SQL --- Cursor helps to execute sql

            cursor = connection.cursor()

            sql = """ SELECT * FROM tbl_carcollection3"""

            cursor.execute(sql)

            cursor.fetchall()

            if cursor.rowcount == 0:
                sql = """INSERT INTO tbl_carcollection3( car_name, car_desc, image) VALUES (%s,%s,%s)"""
                cursor.execute(sql, (car_name3, car_desc3, filename))

                # commit/rollback -if the connection crashes before it commits, it should render back
                connection.commit()
                return redirect('/update')
                # return render_template('add.html', msg="CONGRATS! SUCCESSFULLY SAVED")
            elif cursor.rowcount == 1:
                sql = """UPDATE tbl_carcollection3 SET car_name = [%s], car_desc = [%s], image = [%s] WHERE user_id = 1"""
                cursor.execute(sql, (car_name3, car_desc3, filename))

                connection.commit()
                return redirect('/admin')
            else:
                return redirect('admin')

        else:
            return render_template('admin2.html')


@app.route('/view', methods=['POST', 'GET'])
def view():
    connection = pymysql.connect("localhost", "root", "", "ritelane_db")

    cursor = connection.cursor()

    sql1 = """SELECT * FROM tbl_carcollection"""
    sql2 = """SELECT * FROM tbl_carcollection2"""
    sql3 = """SELECT * FROM tbl_carcollection3"""

    cursor.execute(sql1, sql2, sql3)

    # fetch rows
    rows = cursor.fetchall()  # rows can contain 0,1 or more rows

    # perform a row count
    if cursor.rowcount == 0:
        return render_template('admin2.html', msg='No records')
    else:
        return render_template('admin2.html', data=rows)


if __name__ == '__main__':
    app.run()
