from datetime import datetime
from flask import Flask, request ,render_template, url_for, flash, redirect, session
from forms import RegistrationForm, LoginForm
 
from flask_bcrypt import bcrypt 
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_login import LoginManager,login_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

'''
login = SimpleLogin(app)

app.config['SIMPLELOGIN_LOGIN_URL'] = '/login/'
app.config['SIMPLELOGIN_LOGOUT_URL'] = '/logout/'
app.config['SIMPLELOGIN_HOME_URL'] = '/home/'''


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'rstore'

mysql = MySQL(app)

'''
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)'''



posts = [
    {
        'author': 'Dead',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2022'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2022'
    }
]



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)



@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    '''
    if validate_on_submit():
        return redirect(url_for('home'))
    '''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = form.email.data
        password = form.password.data
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM accounts WHERE email = % s AND password = % s', (email, password )) 
        account = cur.fetchone()
        if account: 
            session['loggedin'] = True
            session['email'] = account['email'] 
            session['password'] = account['password']

            #user = form.username.data
            #login_user(UserName,remember = form.remember.data)

        #if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout') 
def logout(): 
    session.pop('loggedin', None) 
    session.pop('id', None) 
    session.pop('username', None) 
    return redirect(url_for('login')) 




@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if validate_on_submit():
        return redirect(url_for('home'))
    form = RegistrationForm()
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:       
        if form.validate_on_submit():
                username=form.username.data
                email=form.email.data 
                password=form.password.data
                #db.session.add(user)
                #db.session.commit()
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("INSERT INTO accounts(UserName, email, password) VALUES (%s, %s,%s)", (username,email,password))
                mysql.connection.commit()
                cur.close()
                flash('Your account has been created! You are now able to log in', 'success')
                return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


        




if __name__ == '__main__':
    app.run(debug=True)
