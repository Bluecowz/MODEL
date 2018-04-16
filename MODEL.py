from flask import Flask, jsonify, request
from Models.Customer import Customer
from Models.Task import Task
from Models.Work import Work
from datetime import datetime

app = Flask(__name__)

Customers = list()
Tasks = list()


@app.route('/')
def home():
    return "Welcome to MODEL!"


@app.route('/check_in', methods=['POST', 'PUT'])
def check_in():
    if request.method == 'PUT':
        for x in Tasks:
            if x.ID == request.args.get('task_id'):
                for y in x.work:
                    if y.request.args.get('work_id'):
                        y.end_time = datetime.now()
                        return jsonify(y.serialize())
    if request.method == 'POST':
        work = Work()
        work.work_id = request.args.get('work_id')
        work.task_id = request.args.get('task_id')
        work.employee = request.args.get('employee')
        work.start_time = datetime.now()
        for x in Tasks:
            if x.ID == work.task_id:
                x.work.append(work)
        return jsonify(work.serialize())
    else:
        return jsonify([])


@app.route('/prioritize', method=['PUT'])
def prioritize():
    for x in Tasks:
        if x.ID == request.args.get('task_id'):
            x.rank = request.args.get('rank')
            return jsonify(x.serialize())
    return jsonify(None)


@app.route('/tasks')
def list_tasks():
    tasks = []
    for derp in Tasks:
        tasks.append(derp.serialize())
    return jsonify(tasks)


@app.route('/companies')
def list_companies():
    companies = []
    for derp in Customers:
        companies.append(derp.serialize())
    return jsonify(companies)


@app.route('/task', methods=['POST', 'GET'])
def task():
    ID = request.args.get('id')
    if request.method == 'POST':
        derp = Task()
        derp.ID = ID
        for x in Customers:
            if request.args.get('company') == x.name:
                x.task_count = x.task_count + 1
                derp.company = x
        if derp.company is None:
            company(request.args.get('company'))
            for x in Customers:
                if request.args.get('company') == x.name:
                    x.task_count = x.task_count + 1
                    derp.company = x
        derp.posted = datetime.now()
        Tasks.append(derp)
        return jsonify(derp.serialize())
    else:
        for derp in Tasks:
            if derp.name == ID:
                return jsonify(derp.serialize())
    return None


@app.route('/company/<name>', methods=['POST', 'GET'])
def company(name):
    if request.method == 'POST':
        new_cust = Customer(name=name)
        Customers.append(new_cust)
        return jsonify(new_cust.serialize())
    else:
        for derp in Customers:
            if derp.name == name:
                return jsonify(derp.serialize())
    return jsonify([])


if __name__ == '__main__':
    app.run()
