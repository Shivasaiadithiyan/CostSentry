import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

_YOURMAILID = 'enteryourmail@gmail.com'

def sendNotification(receiverEmail, items):
    message = MIMEMultipart()
    message['From'] = _YOURMAILID
    message['To'] = receiverEmail
    message['Subject'] = 'Offers available'

    body = ""
    for item, price in items:
        body += f"The {item} price has decreased to {price}.\n\n"
    
    body+="----END----"

    message.attach(MIMEText(body))

    session = smtplib.SMTP('smtp.gmail.com', 587) 
    session.starttls()  
    session.login(_YOURMAILID, 'enteryourmailpassword')  
    text = message.as_string()
    session.sendmail(_YOURMAILID, receiverEmail, text)
    session.quit()
