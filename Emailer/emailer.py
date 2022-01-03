import smtplib, pika,json,sys, os 
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='hostname'))
    channel = connection.channel()

    #Declaring exchange
    channel.exchange_declare(exchange='logs', exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='logs', queue=queue_name)


    def callback(ch, method, properties, body):
        datadict = json.loads(body)
        # print(datadict)
        
        #Initailizing Variables for email
        fromaddr = "desired email address"
        toaddr = datadict[0]["toaddr"]
        sub = datadict[0]["subject"]

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = str(toaddr)
        msg['Subject'] = str(sub)

        body = datadict[0]["body"]
        msg.attach(MIMEText(body, 'plain'))

        #Connection to SMTP server 
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        #getting login details 
        server.login(fromaddr, "google app hashkey")
        text = msg.as_string()
        #sending email
        server.sendmail(fromaddr, toaddr, text)
        #SMPT connect terminated
        print("Email sent")
        server.quit()
        
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
