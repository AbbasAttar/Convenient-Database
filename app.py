from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
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
            resp.message("Your company: {}".format(li[1].strip()))
        elif (li[0].upper().find("JOB") != -1):
            resp.message("Your Job Title: {}".format(li[1].strip()))
        else:
            resp.message("Invalid Update")
        return str(resp)
    

if __name__ == "__main__":
    app.run(debug=True)