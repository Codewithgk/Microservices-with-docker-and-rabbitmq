from flask import Flask, render_template, request, jsonify 
import pika, json
# from flask_restful import Resource, Api    

app = Flask(__name__)

#Establishing Connection
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='172.17.0.2'))
channel = connection.channel()

#Declaring exchange
channel.exchange_declare(exchange='logs', exchange_type='fanout')
    

@app.route('/')
def home():
    return "Hey, Hello Welcome to Flask Api!"

Data=[]
@app.route('/send',methods= ['POST'])
def send():
    
    request_data = request.get_json()
    email = {
        'toaddr': request_data['toaddr'],
        'subject' : request_data['subject'],
        'body': request_data['body'],
    }
    Data.append(email) 
    #Sending the data to Queue.
    channel.basic_publish(exchange='logs', routing_key='', body = json.dumps(Data))
    return jsonify(Data)



if __name__== "__main__":
    app.run(host ='0.0.0.0', port = 5001, debug=True)

