from flask import Flask,render_template,redirect,url_for,request
from pymongo import MongoClient
import urllib.parse
from flask_mail import Mail,Message
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL')   # Your Gmail address
app.config['MAIL_PASSWORD'] = os.getenv('PASSWORD')  # Your Gmail app password


mail = Mail(app)




try:
    username = urllib.parse.quote_plus(os.getenv('DATABASE_USERNAME'))
    password = urllib.parse.quote_plus(os.getenv('DATABASE_PASSWORD'))
    DB_URI = f"mongodb+srv://{username}:{password}@cluster0.2iatqsb.mongodb.net/Food"
    client = MongoClient(DB_URI)
    db = client.Food
    user_collection = db.food_details
    print('Connection successfully')
except Exception as e:
    print(f'Please follow the error {e}')
    




@app.route('/result',methods=['GET','POST'])
def home():
    cursor = user_collection.find({})
    return render_template('results.html',cursor=cursor)

@app.route('/donation',methods=['POST','GET'])
def donations():
    if request.method == "POST":
        name = request.form['name']
        age = request.form['age']
        area = request.form['area']
        food_type = request.form['food_type']
        quantity = request.form['quantity']
        gmail = request.form['gmail']
        # data = [name,age,area,food_type,quantity]
        user_collection.insert_one({'name':name,'age':age,'area':area,'food_type':food_type,'quantity':quantity})
        # print(name,age,area,food_type,quantity)
        # return redirect(url_for('home',name=name,age=age,area=area,food_type=food_type,quantity=quantity))
        msg = Message(subject='New Donation Received',
                      sender=gmail,
                      recipients=['cheguakash001@gmail.com'])  # Replace with recipient email
        msg.body = f"New donation received:\nName: {name}\nAge: {age}\nArea: {area}\nFood Type: {food_type}\nQuantity: {quantity}"
        mail.send(msg)
        return redirect(url_for('home'))
    return render_template('index.html')   
   
   
     

if __name__ == '__main__':
    app.run(debug=True)