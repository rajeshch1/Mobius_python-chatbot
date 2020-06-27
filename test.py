from flask import Flask,render_template,request,redirect,url_for,jsonify
from twilio.rest import Client
import MySQLdb
import os
import aiml

username =" "

app = Flask(__name__)

conn = MySQLdb.connect("localhost","root","hokage","mobius" )

@app.route("/")
def index():
	return render_template("signup.html", title="signup")
@app.route("/signup",methods=["POST"])
def signup():
	name = str(request.form["name"])
	email = str(request.form["Email"])
	password = str(request.form["pass"])
	enroll = str(request.form["Enroll"])
	contact = str(request.form["Contact"])
	slct1 = str(request.form.get('slct1'))
	slct2 = str(request.form.get('slct2'))
	slct3 = str(request.form.get('slct3'))
	cursor = conn.cursor()
	
	cursor.execute("INSERT INTO user_details (uname,email,password,enroll,contact,slct1,slct2,slct3)VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(name,email,password,enroll,contact,slct1,slct2,slct3))
	conn.commit()
	return redirect(url_for("login")) 

#@app.route("/hello")
#def hello():
#    return render_template('chat.html')




@app.route("/login")
def login():
	return render_template("login.html",title="data")

@app.route("/checkUser",methods=["POST"])
def check():
	global username 
	username = str(request.form["username"])
	password = str(request.form["password"])
	cursor = conn.cursor()
	cursor.execute("SELECT EXISTS(SELECT uname FROM user_details WHERE email ='" + username + "' AND password = '"+password+"')")
	user = cursor.fetchone()
	
	if user[0]==1:
	  return render_template("chat.html")
    	
	else:
		return "Please enter a valid password"
@app.route("/home")
def home():
	return render_template("chat.html")
	
@app.route("/ask", methods=['POST'])
def ask():
	message = str(request.form['messageText'])

	kernel = aiml.Kernel()

	if os.path.isfile("bot_brain.brn"):
	    kernel.bootstrap(brainFile = "bot_brain.brn")
	else:
	    kernel.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands = "load aiml b")
	    kernel.saveBrain("bot_brain.brn")

	# kernel now ready for use
	while True:
	    if message == "quit":
	        exit()
	    elif message == "save":
	        kernel.saveBrain("bot_brain.brn")
	    else:
	        bot_response = kernel.respond(message)
	        # print bot_response
	        return jsonify({'status':'OK','answer':bot_response})	

@app.route("/feedback")
def feedback():
	return render_template("feedback.html",title="feedback")

@app.route("/admin",methods=['POST'])
def admin():
	subject = str(request.form["subject"])
	cursor = conn.cursor()		
	cursor.execute("INSERT INTO feedback(name,subject) VALUES('" + username +" ','" + subject + "')")
	conn.commit()
	accountSid = "ACed8110a2b4abb60d54a4c6c9255da8b5"
	authToken = "4ad309b44f0955efdf42dc7a911f2362"
	twilioClient = Client(accountSid, authToken)
	myTwilioNumber = "+15103984745"
	destCellPhone = "+919030719650"
	myMessage = twilioClient.messages.create(body = "Hey you have recieved a suggestion from  " + username + " ", from_=myTwilioNumber, to=destCellPhone)
	return render_template("chat.html")

@app.route("/logout")
def logout():
	return render_template("signup.html", title="signup")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/contact")
def contact():
	return render_template("contact.html")	

			

if __name__ == "__main__":
	app.run(debug=True)
