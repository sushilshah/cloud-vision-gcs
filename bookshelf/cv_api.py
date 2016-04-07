from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import werkzeug
import crud_api


# TODOS = {
#     'todo1': {'task': 'build an API'},
#     'todo2': {'task': '?????'},
#     'todo3': {'task': 'profit!'},
# }


# def abort_if_todo_doesnt_exist(todo_id):
#     if todo_id not in TODOS:
#         abort(404, message="Todo {} doesn't exist".format(todo_id))


parser = reqparse.RequestParser()
parser.add_argument('task')
# From file uploads
parser.add_argument('picture', type=werkzeug.datastructures.FileStorage, location='files')


# Todo
# shows a single todo item and lets you delete a todo item
# class Todo(Resource):
#     def get(self, todo_id):
#         abort_if_todo_doesnt_exist(todo_id)
#         return TODOS[todo_id]

#     def delete(self, todo_id):
#         abort_if_todo_doesnt_exist(todo_id)
#         del TODOS[todo_id]
#         return '', 204

#     def put(self, todo_id):
#         args = parser.parse_args()
#         task = {'task': args['task']}
#         TODOS[todo_id] = task
#         return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
# class TodoList(Resource):
#     def get(self):
#         return TODOS

#     def post(self):
#         args = parser.parse_args()
#         print args
#         print "**ARGS"
#         todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
#         todo_id = 'todo%i' % todo_id
#         TODOS[todo_id] = {'task': args['task']}
#         return TODOS[todo_id], 201

# UploadFile
# lets you post files
class UploadFile(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        file = args['picture']
        if file:
            response = crud_api.identify_image_attributes(file)
        else:
            abort(404, message="No file ('picture' attribute) attached with the request")
        return response, 201

##
## Actually setup the Api resource routing here
##
def register_apis(app):
    #app = Flask(__name__)
    api = Api(app)
    # api.add_resource(TodoList, '/todos/')
    # api.add_resource(Todo, '/todos/<todo_id>')
    api.add_resource(UploadFile, '/uploadfile')



# if __name__ == '__main__':
#     app.run(debug=True)

# Example usage

# $ python api.py
#  * Running on http://127.0.0.1:5000/
#  * Restarting with reloader

# GET the list

# $ curl http://localhost:5000/todos
# {"todo1": {"task": "build an API"}, "todo3": {"task": "profit!"}, "todo2": {"task": "?????"}}

# GET a single task

# $ curl http://localhost:5000/todos/todo3
# {"task": "profit!"}

# DELETE a task

# $ curl http://localhost:5000/todos/todo2 -X DELETE -v

# > DELETE /todos/todo2 HTTP/1.1
# > User-Agent: curl/7.19.7 (universal-apple-darwin10.0) libcurl/7.19.7 OpenSSL/0.9.8l zlib/1.2.3
# > Host: localhost:5000
# > Accept: */*
# >
# * HTTP 1.0, assume close after body
# < HTTP/1.0 204 NO CONTENT
# < Content-Type: application/json
# < Content-Length: 0
# < Server: Werkzeug/0.8.3 Python/2.7.2
# < Date: Mon, 01 Oct 2012 22:10:32 GMT

# Add a new task

# $ curl http://localhost:5000/todos -d "task=something new" -X POST -v

# > User-Agent: curl/7.19.7 (universal-appl
#> POST /todos HTTP/1.1