import pika
from flask import Flask, request, make_response, jsonify
import mysql.connector

queue_name = 'name-queue'

def create_db(dbname):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tee191",
    )

    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE " + dbname)
    print("Database created!")


def create_table(dbname):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tee191",
        database=dbname
    )
    mycursor = mydb.cursor()
    mycursor.execute(
        "CREATE TABLE Scoreboard (name VARCHAR(50), score smallint UNSIGNED)")
    print("Table created!")


def add_data(dbname, name, score):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tee191",
        database=dbname
    )

    mycursor = mydb.cursor()
    sql = "INSERT INTO Scoreboard (name, score) VALUES (%s, %s)"
    val = (name, score)
    mycursor.execute(sql, val)
    mydb.commit()
    print("Data Added!")
    # for x in mycursor:
    #     print(x)
    mycursor.close()
    mydb.close()

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body), end="")
    add_data("teedb",body,0)



if __name__ == '__main__':
    parameters = pika.ConnectionParameters(host='localhost')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.basic_consume(on_message_callback=callback, queue=queue_name , auto_ack=True)
    channel.start_consuming()
    
