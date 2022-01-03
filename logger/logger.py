import logging
import logging.handlers
import pika, sys, os, json

from pika.spec import Queue

#Creating Custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#formatting
formatter = logging.Formatter('%(asctime)s : %(name)s : %(message)s')

file_handler = logging.FileHandler('NewLog.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.info("New msg")
data = []
#making connection 
def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='hostname'))
    channel = connection.channel()

    # channel.queue_declare(queue='log')
    #declaring exchange
    channel.exchange_declare(exchange='logs', exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='logs', queue=queue_name)

    def callback(ch, method, properties, body):
        email = json.loads(body)
        logger.info(email)
        data.append(email)
        print("record logged")
        
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

logger.info(data)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
