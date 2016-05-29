from flask import request
from app import app

from app.form import mailNinja


@app.route('/api/sendForm/<string:query>/', methods=['POST'])
def sendForm(query):
    if request.method == 'POST':
        try:
            # request.referrer can be None for the time being
            # will be deprecated in the future
            if request.referrer is None:
                ref = "NO-REFERRER"
            else:
                ref = request.referrer

            # sender_name and sender_email are not required fields
            # if they are not set, default to anonymous/empty
            sender_name = request.form["senderName"] if request.form.get("senderName") else "Anonymous"
            sender_email = request.form["senderEmail"] if request.form.get("senderEmail") else "DO-NOT-REPLY"
            # Create the subject, and the text_body from POST params
            subject = "[{}] New msg from: {} ".format(ref, sender_name)
            text_body = "New form submission from " + ref + "\n"
            for k,v in request.form.items():
                text_body += "{:20}: {}\n".format(k.upper(),v)
            # Send the email
            mailNinja.send_email(subject, sender_name, query, text_body, sender_email, 0)
            return "PEW PEW! Email has been dispatched by our trained ninja monkeys!"
        except Exception as e:
            print(e)
            return e
    else:
        return "Method not allowed. You cheeky sneaky ninja!", 405

@app.errorhandler(500)
def internal_error():
    return "You have broken our servers! Don't worry though, our specialized monkey ninja team has been deployed to fix them!", 500
