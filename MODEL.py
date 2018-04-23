from flask import Flask, jsonify, request
from Models.Customer import Customer
from Models.Task import Task
from Models.Work import Work
from Models.Performance import Performance
from Models.Stats import Stats
from datetime import datetime, timedelta

app = Flask(__name__)
Perform = Performance()
Customers = list()
Tasks = list()


@app.route('/')
def home():
    return "Welcome to MODEL!"


@app.route('/check_in', methods=['POST', 'PUT', 'OPTIONS'])
def check_in():
    try:
        if request.method == 'PUT':
            for x in Tasks:
                if x.ID == request.args.get('task_id'):
                    for y in x.work:
                        if request.args.get('work_id') == y.work_id:
                            y.end_time = datetime.now()
                            response = jsonify(y.serialize())
                            response.headers.add('Access-Control-Allow-Origin', '*')
                            response.headers.add('Access-Control-Allow-Methods', 'PUT,OPTIONS')
                            return response
        if request.method == 'POST':
            work = Work()
            work.work_id = request.args.get('work_id')
            work.task_id = request.args.get('task_id')
            work.employee = request.args.get('employee')
            work.start_time = datetime.now()
            for x in Tasks:
                if x.ID == work.task_id:
                    x.work.append(work)
            response = jsonify(work.serialize())
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Methods', 'PUT,OPTIONS,POST')
            return response
        else:
            response = jsonify([])
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Methods', 'PUT,OPTIONS,POST')
            return response
    finally:
        Perform.end("check_in")


@app.route('/prioritize', methods=['PUT', 'OPTIONS'])
def prioritize():
    Perform.start()
    try:
        for x in Tasks:
            if x.ID == request.args.get('task_id'):
                x.rank = int(request.args.get('rank'))
                response = jsonify(x.serialize())
                response.headers.add('Access-Control-Allow-Origin', '*')
                response.headers.add('Access-Control-Allow-Methods', 'PUT,OPTIONS')
                return response
        response = jsonify(None)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    finally:
        Perform.end("Prioritize")


@app.route('/tasks')
def list_tasks():
    Perform.start()
    try:
        tasks = []
        for x in Tasks:
            if x.rank == 1:
                tasks.append((x.serialize()))

        for x in Tasks:
            if x.rank == 2:
                tasks.append((x.serialize()))

        for x in Tasks:
            if x.rank == 3:
                tasks.append((x.serialize()))

        response = jsonify(tasks)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    finally:
        Perform.end("get_tasks")


@app.route('/companies')
def list_companies():
    Perform.start()
    try:
        companies = []
        for derp in Customers:
            companies.append(derp.serialize())
        response = jsonify(companies)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    finally:
        Perform.end("list_companies")


@app.route('/task', methods=['POST', 'GET'])
def task():
    Perform.start()
    try:
        if request.method == 'POST':
            ID = request.args.get('id')
            derp = Task()
            derp.ID = ID
            derp.est_hrs = request.args.get('est-hrs')
            for x in Customers:
                if request.args.get('company') == x.name:
                    x.add_task()
                    derp.set_company(x)
            if derp.company is None:
                c = Customer(request.args.get('company'))
                c.add_task()
                Customers.append(c)
                derp.set_company(c)
            derp.posted = datetime.now()
            Tasks.append(derp)
            response = jsonify(derp.serialize())
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        else:
            ID = request.args.get('id')
            for derp in Tasks:
                if derp.ID == ID:
                    response = jsonify(derp.serialize())
                    response.headers.add('Access-Control-Allow-Origin', '*')
                    return response
        response = jsonify([])
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    finally:
        Perform.end("task")


@app.route('/company', methods=['POST', 'GET'])
def company():
    Perform.start()
    try:
        if request.method == 'POST':
            new_cust = Customer(request.args.get('name'))
            Customers.append(new_cust)
            response = jsonify(new_cust.serialize())
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        else:
            for derp in Customers:
                if derp.name == request.args.get('name'):
                    response = jsonify(derp.serialize())
                    response.headers.add('Access-Control-Allow-Origin', '*')
                    return response
        response = jsonify([])
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    finally:
        Perform.end("company")


@app.route('/performance', methods=['GET'])
def perform():
    response = jsonify(Perform.serialize_stats())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/month', methods=['GET'])
def stats():
    Perform.start()
    try:
        work = list()
        for x in Tasks:
            for y in x.work:
                work.append(y)
        response = jsonify(Stats.get_stats(Tasks, work))
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    finally:
        Perform.end("month")


@app.route('/fake_me')
def fake_me():
    derp_comp = Customer(name="Mike LLC")
    Customers.append(derp_comp)

    for x in range(1, 6):
        task_one = Task()
        task_one.ID = x
        task_one.company = derp_comp
        task_one.posted = datetime.now()
        task_one.est_hrs = 7

        w1 = Work()
        w1.task_id = x
        w1.work_id = 1
        w1.start_time = datetime.now()
        w1.end_time = datetime.now() + timedelta(hours=-4)

        w2 = Work()
        w2.task_id = x
        w2.work_id = 2
        w2.start_time = datetime.now()
        w2.end_time = datetime.now() + timedelta(hours=-4)

        w3 = Work()
        w3.task_id = x
        w3.work_id = 3
        w3.start_time = datetime.now()
        w3.end_time = datetime.now() + timedelta(hours=-4)

        task_one.work.append(w1)
        task_one.work.append(w2)
        task_one.work.append(w3)
        Tasks.append(task_one)

        derp_comp.add_task()

    return "Fake Data Added"




if __name__ == '__main__':
    app.run()
