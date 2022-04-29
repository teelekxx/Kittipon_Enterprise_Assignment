import pika

queue_name = 'name-queue'
max_priority = 10

parameters = pika.ConnectionParameters(host = 'localhost')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(
    queue=queue_name, arguments={"x-max-priority": max_priority}
)
def publish(name, priority):
    name = name
    channel.basic_publish(
        properties=pika.BasicProperties(priority=priority),
        exchange='',
        routing_key=queue_name,
        body=name
    )
    print("publish!")

publish("test", 2)
    