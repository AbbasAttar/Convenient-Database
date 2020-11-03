from flask import Flask, request, jsonify, redirect
from flask_pymongo import PyMongo
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb+srv://Abbas:alohomora@cluster0.4cqiz.mongodb.net/Users?retryWrites=true&w=majority"

mongo = PyMongo(app)

db_operations = mongo.db.user

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    sender_number = request.form.get('From').split(":")
    print(sender_number)

    msg = request.form.get('Body')

    resp = MessagingResponse() 
    
    #Guide message
    if msg.upper() == "HI":
        resp.message("""
Hi there

This message is sent for guiding you how you can update your data in our database.
        
You can update your company detail or job title detail by messageing us like the following:
        
Company: <new Company name>
or
Job: <new Job title>
""")
        return str(resp)
    else:
        li = msg.split(":");
        if (li[0].upper().find("COMPANY") != -1):
            
            updated_user = {"$set": {'Company' : li[1].strip()}}
            filt = {'Phone' : sender_number[1]}
            db_operations.update_one(filt, updated_user)

            resp.message("Your company: {}".format(li[1].strip()))

        elif (li[0].upper().find("JOB") != -1):

            updated_user = {"$set": {'Job Title' : li[1].strip()}}
            filt = {'Phone' : sender_number[1]}
            db_operations.update_one(filt, updated_user)
            
            resp.message("Your Job Title: {}".format(li[1].strip()))
        else:
            
            resp.message("Invalid Update")
        
        return str(resp)
    

if __name__ == "__main__":
    app.run(debug=True)