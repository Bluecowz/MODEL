from flask import Flask, jsonify, request
from Models.Customer import Customer
from Models.Task import Task
from Models.Work import Work
from Models.Performance import Performance
from Models.Stats import Stats
from datetime import datetime

app = Flask(__name__)


Perform = Performance()
Customers = list()
Tasks = list()



@app.route('/')
def home():
    return "Welcome to MODEL!"


@app.route('/check_in', methods=['POST', 'PUT'])
def check_in():
    try:
        if request.method == 'PUT':
            for x in Tasks:
                if x.ID == request.args.get('task_id'):
                    for y in x.work:
                        if request.args.get('work_id') == y.work_id:
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
    finally:
        Perform.end("check_in")


@app.route('/prioritize', methods=['PUT'])
def prioritize():
    Perform.start()
    try:
        for x in Tasks:
            if x.ID == request.args.get('task_id'):
                x.rank = int(request.args.get('rank'))
                return jsonify(x.serialize())
        return jsonify(None)
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

        return jsonify(tasks)
    finally:
        Perform.end("get_tasks")


@app.route('/companies')
def list_companies():
    Perform.start()
    try:
        companies = []
        for derp in Customers:
            companies.append(derp.serialize())
        return jsonify(companies)
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
            return jsonify(derp.serialize())
        else:
            ID = request.args.get('id')
            for derp in Tasks:
                if derp.name == ID:
                    return jsonify(derp.serialize())
        return jsonify([])
    finally:
        Perform.end("task")


@app.route('/company', methods=['POST', 'GET'])
def company():
    Perform.start()
    try:
        if request.method == 'POST':
            new_cust = Customer(request.args.get('name'))
            Customers.append(new_cust)
            return jsonify(new_cust.serialize())
        else:
            for derp in Customers:
                if derp.name == request.args.get('name'):
                    return jsonify(derp.serialize())
        return jsonify([])
    finally:
        Perform.end("company")


@app.route('/performance', methods=['GET'])
def perform():
    return jsonify(Perform.serialize_stats())


@app.route('/month', methods=['GET'])
def stats():
    Perform.start()
    try:
        work = list()
        for x in Tasks:
            for y in x.work:
                work.append(y)
        return jsonify(Stats.get_stats(Tasks, work))
    finally:
        Perform.end("month")


if __name__ == '__main__':
    app.run()
