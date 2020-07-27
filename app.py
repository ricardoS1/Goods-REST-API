import os
from flask import Flask, redirect, url_for, request, render_template, jsonify, json
from pymongo import MongoClient
app = Flask(__name__)

client = MongoClient(os.environ['RESTENDPOINT_DB_1_PORT_27017_TCP_ADDR'], 27017)
database = client.restdatabase

@app.route('/')
def homepage():
    return render_template('index.html')


@app.route ('/new', methods=['POST'])
def insert():
    goods = {
        'name': request.form['name'],
        'description': request.form['description'],
        'price': request.form['price'],
        'rating': request.form['rating'],
        'last_purchased': request.form['last_purchased'],
        'total_days_last_purchased': request.form['total_days_last_purchased'],
    }
    database.restdb.insert_one(goods)
    return redirect(url_for('homepage'))

@app.route ('/getGood/<name>', methods=['GET'])
def getAGood(name):
    data = database.restdb
    result = []
    i = data.find_one({'name': name})
    result.append({'name': i['name'],
                   'description': i['description'],
                   'rating': i['rating'],
                   'price': i['price'],
                   'last_purchased': i['last_purchased'],
                   'total_days_last_purchased': i['total_days_last_purchased']})

    return jsonify(result)

@app.route ('/getAll', methods=['GET'])
def getAllGoods():
    data = database.restdb
    result=[]
    for i in data.find():
        result.append({'name': i['name'],
                       'description': i['description'],
                       'rating': i['rating'],
                       'price': i['price'],
                       'last_purchased': i['last_purchased'],
                       'total_days_last_purchased': i['total_days_last_purchased']})
    return jsonify(result)


@app.route ('/getRange/<pageno>', methods=['GET'])
def getPaginatedGoods(pageno):
    if not wholeNum(pageno):
        return jsonify({'Error': 'The page you requested cannot be found'})  # Checking for whole number
    pageno = int(pageno)
    if pageno <= 0:
        return jsonify({'Error': 'The page you requested cannot be found'})  # Checking for positive number
    if pageno > 1:
        skipno = (10 * pageno) - 10
    else:
        skipno = 0
    data = database.restdb
    result = []
    for i in data.find().skip(skipno).limit(10):
        result.append({'name': i['name'],
                       'description': i['description'],
                       'rating': i['rating'],
                       'price': i['price'],
                       'last_purchased': i['last_purchased'],
                       'total_days_last_purchased': i['total_days_last_purchased']})
    return jsonify(result)


def wholeNum(n):
    n = float(n)
    if n % 2 == 0 or (n + 1) % 2 == 0:
        return True
    else:
        return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


