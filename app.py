from flask import Flask, render_template, request, redirect, url_for
from models.user import Db, User
from modules.userform import UserForm
from modules.deluserform import DelUserForm
from modules.upduserform import UpdUserForm
from random import randrange

from flask_heroku import Heroku

# Also after you initialize your app, configure and connect the db:
app = Flask(__name__)
heroku = Heroku(app)

# Necessary to connect to app
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/usersdb'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/usersdb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fadi:fadi123@localhost:5432/usersdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "s14a-key"
Db.init_app(app)

#
# List all Users
#
# Create a '/' route with some logic (READ):
@app.route('/')
def index():
    # Query all
    users = User.query.all()

    # Iterate and print
    for user in users:
        User.toString(user)
    
    h1 = 'Lab: 3 HW2 - List of Users'
    return render_template("index.html", header1 = h1, user_result = users)

#
# Add User
#
# Create a '/adduser' route with GET and POST methods (CREATE):
# @route /adduser - GET, POST
@app.route('/adduser', methods=['GET', 'POST'])
def addUser():
    form = UserForm()
    # If GET
    if request.method == 'GET':
        return render_template('adduser.html', form=form)
    # If POST
    else:
        if form.validate_on_submit():
            first_name = request.form['first_name']
            age = request.form['age']
            new_user = User()
            new_user.first_name = first_name
            new_user.age = age
            Db.session.add(new_user)
            Db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('adduser.html', form=form)

# Expand route, '/adduser/<first_name>/', to add users based on url parameters":
# @route /adduser/<first_name>/<age>
@app.route('/adduser/<first_name>/<age>')
def addUserFromUrl(first_name, age):
    Db.session.add(User(first_name=first_name, age=age))
    Db.session.commit()
    return redirect(url_for('index'))
#
# Delete User
#
@app.route('/deluser', methods=['GET', 'POST'])
def delUser():
    form = DelUserForm()
    # If GET
    if request.method == 'GET':
        return render_template('deluser.html', form=form)
    # If POST
    else:
        if form.validate_on_submit():
            id = request.form['user_id']
            print('Del User ID >>>>>> ', id)
            Db.session.query(User).filter(User.user_id==id).delete()
            # Or you may select the obj; than delete it:
            # obj = session.query(User).filter(User.id==id).first()
            # session.delete(obj)
            Db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('deluser.html', form=form)
#
# Update User
#
@app.route('/upduser', methods=['GET', 'POST'])
def updUser():
    form = UpdUserForm()
    # If GET
    if request.method == 'GET':
        return render_template('upduser.html', form=form)
    # If POST
    else:
        if form.validate_on_submit():
            id = request.form['user_id']
            print('Upd User ID >>>>>> ', id)
            first_name = request.form['first_name']
            age = request.form['age']           
            Db.session.query(User).filter(User.user_id==id).update({"first_name": first_name, "age": age}, synchronize_session='evaluate')
            # Or you may select the obj; than delete it:
            # obj = session.query(User).filter(User.id==id).first()
            # session.delete(obj)
            Db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('deluser.html', form=form)

#
# Generate mock data of any amount (names can be nonsense) and List them
#
@app.route('/mockuser')
def mockUser():
    mock_users = []
    idrange = 1000
    random_num_of_users = 5
    for i in range(random_num_of_users):
        rand_new_user = User()
        rand_new_user.user_id = randrange(idrange)
        User.toString(rand_new_user)
        mock_users.append(rand_new_user)
    
    h1 = 'List of Mocked Users'
    return render_template("index.html", header1 = h1, user_result = mock_users)

#
# No caching at all for API endpoints.
#
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response