from flask import Flask, render_template, redirect, url_for, request
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkE'    
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ad.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Ad(db.Model):
  uid = db.Column(db.Integer, primary_key = True)
  subject = db.Column(db.String(50), nullable = False)
  body = db.Column(db.String(50), nullable = False)
  price = db.Column(db.Integer, nullable = False)
  email = db.Column(db.String(50), nullable = False)
  rank = db.Column(db.Integer, nullable = False)


@app.route("/")
def home():
  all_ads = Ad.query.order_by(Ad.uid).all()
  return render_template('index.html', ads = all_ads)


@app.route("/sorted")
def sorted():
  all_ads = Ad.query.order_by(Ad.price.desc()).all()
  for i in range(len(all_ads)):
    all_ads[i].rank = i+1  
  db.session.commit()
  return render_template('rank.html', ads = all_ads)


@app.route("/search", methods = ['GET','POST'])
def search():
  subject = request.form['subject']
  search_results = Ad.query.filter_by(subject = subject.title())
  return render_template('index.html', ads = search_results)


@app.route("/insert", methods = ['POST'])
def insert():
  fuid = int(request.form['uid'])
  fsubject = request.form['subject']
  fbody = request.form['body']
  fprice = int(request.form['price'])
  femail = request.form['email']

  new_record = Ad(
    uid = fuid,
    subject = fsubject.title(),
    body = fbody,
    price = fprice,
    email = femail,
    
    rank = 0
  )
  db.session.add(new_record)
  db.session.commit()
  flash('Advertisement added successfully')
  #print(uid,subject,body,price,email)
  return redirect(url_for('home'))


@app.route('/delete/<id>', methods = ['GET','POST'])
def delete(id):
  tAd = Ad.query.get(id)
  db.session.delete(tAd)
  db.session.commit()
  flash("Ad deleted successfully")
  return redirect(url_for('home'))


@app.route('/update/<id>', methods = ['GET', 'POST'])
def update(id):
  if request.method == 'POST':
    tAd = Ad.query.get(id)
    subject = request.form['subject']
    body = request.form['body']
    price = int(request.form['price'])
    email = request.form['email'] 
    tAd.subject = subject.title()
    tAd.body = body
    tAd.price = price
    tAd.email = email
  
    db.session.commit()
    flash("Ad details updated successfully")
    return redirect(url_for('home'))
  
if __name__ == "__main__":
  app.run(debug=True, port=8001)