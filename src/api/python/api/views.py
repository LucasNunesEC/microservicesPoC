from api import app
from flask import jsonify, abort, request, make_response
from api import models, db, auth

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    tasks = models.Task.query.all()
    tmp = []
    for task in tasks:
        tmp.append(task.serialize())
    return jsonify({'tasks': tmp})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    tasks = models.Task.query.all()
    task = [task for task in tasks if task.id == task_id]

    if len(task) == 0:
        abort(404)
    return jsonify({'task':task[0].serialize()})

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    tasks = models.Task.query.all()
    if not request.json or not 'title' in request.json:
        abort(400)
    if request.json['done'] == 'True':
        task = models.Task(title=request.json['title'], 
                           description=request.json.get('description', ""), 
                           done=True)
    if request.json['done'] == 'False':
        task = models.Task(title=request.json['title'], 
                           description=request.json.get('description', ""), 
                           done=False)
    db.session.add(task)
    db.session.commit()
    return jsonify({'task': task.serialize()}), 201

'''
    ------------------------------FIX----------------------------

        Autor: Diogo Dantas
        Data: 28/06/2017
        Hora: 15:57 PM

        Comentário:
            - Corrigir a atualização do campo "Done" para salvar valores booleanos
            para que seja possivel atualizar esse campo normalmente com o método PUT.abort
            No momento o PUT está salvando uma string no campo "Done", que é booleano", o que pode
            causar problemas futuramente.
'''
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    tasks = models.Task.query.all()
    task = [task for task in tasks if task.id == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        print("Aqui2")
        abort(400)
    # if 'title' in request.json and type(request.json['title']) != unicode:
    #     abort(400)
    # if 'description' in request.json and type(request.json['description']) is not unicode:
    #     abort(400)

    task[0].title = request.json.get('title', task[0].title)
    task[0].description = request.json.get('description', task[0].description)
    task[0].done = request.json.get(bool('done'), task[0].done)
    db.session.commit()
    return jsonify({'task': task[0].serialize()})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = models.Task.query.all()
    task = [task for task in tasks if task.id == task_id]
    if len(task) == 0:
        abort(404)
    db.session.delete(task[0])
    db.session.commit()
    return jsonify({'result': True})

@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'admin'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

