from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import werkzeug
import crud_api
from werkzeug.exceptions import BadRequest

parser = reqparse.RequestParser()
parser.add_argument('task')
parser.add_argument('maxResults',  type=int)
# From file uploads
parser.add_argument('picture', type=werkzeug.datastructures.FileStorage, location='files')

# [START upload file]
# UploadFile
# lets you post files
class UploadFile(Resource):
    def get(self):
        raise BadRequest("Get request is not supported. Try POST request")
    def post(self):
        args = parser.parse_args()
        file = args['picture']
        max_results = args['maxResults']
        kGraph = args['maxResults']
        if file:
            response = crud_api.identify_image_attributes(file, max_results)
        else:
            abort(404, message="No file ('picture' attribute) attached with the request")
        return response, 201
# [END upload file]

##
## Actually setup the Api resource routing here
##
def register_apis(app):
    api = Api(app)
    api.add_resource(UploadFile, '/uploadfile')
