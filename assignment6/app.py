import json
import logging
from flask import Flask, request, make_response, jsonify
import mysql.connector


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
        user="tee",
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


def show_data(dbname):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tee191",
        database=dbname
    )
    jsonbody = {
        "users": [],
    }
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Scoreboard")
    for x in mycursor:
        xjson = {
            "name": x[0],
            "score": x[1],
        }
        jsonbody["users"].append(xjson)

    return jsonbody


app = Flask(__name__)


@app.route('/')
def hello():
    app.logger.info("A User entered")
    q = request.args.get('q')
    print(q)
    return "Hello"


@app.route('/users', methods=['GET'])
def display_data():
    app.logger.info("A User request for all users")
    return show_data("teedb")


@app.route("/add/<name>/<score>")
def add(name, score):
    app.logger.info("A User add a data")
    add_data("teedb", name, score)
    jsonbody = {
        "name": name,
        "score": score,
    }
    return jsonify(jsonbody)


if __name__ == '__main__':
    # create_db("teedb")
    # create_table("teedb")
    app.run(port=8080, debug=False)
