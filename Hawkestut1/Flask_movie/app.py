from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, redirect, url_for



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Admin@localhost/Beer++'
app.debug=True
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    Amount_owed = db.Column(db.Integer) #can't modify table once created in sqlalchemy!
    beers_outstanding = db.Column(db.Integer) #can't modify table once created in sqlalchemy!

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.beers_outstanding = 0
    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/')
def index():
    myUser = User.query.all() #links to display of list of all users under login
    #oneItem = User.query.filter_by(username="test")
    return render_template('index.html', myUser=myUser)##myUser feeds variable into html code - which prints list of users. changed 'add_user.html' to 'index.html' to incorporate bootstrap index.

@app.route('/post_user', methods=['POST'])
def post_user():
    user = User(request.form['username'], request.form['email'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/buy_beer', methods=['POST'])
def buy_beer():
    user = User.query.get(request.form["id"])
    user.beers_outstanding += 1
    db.session.commit()
    #print (u.beers_outstanding)
    # user = User(request.form['username'], request.form['email'])
    # db.session.add(user)
    # db.session.commit()
    return redirect(url_for('index'))

@app.route('/clear_debt', methods=['POST'])
def clear_debt():
    user = User.query.get(request.form["id"])
    user.beers_outstanding = 0
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='0.0.0.0') #inserted ip details to get it running on other devices - didn't work (was blank in brackets before)
    #iptables -I INPUT -p tcp --dport 5000 -j ACCEPT #trying to get external page working
