

PROJECT_ID = 'cloud-vision-1266'

def _get_storage_client():
	return PROJECT_ID
    # return storage.Client(
    #     project=current_app.config['PROJECT_ID'])

def upload_file(file_stream, filename, content_type):
    """
    Uploads a file to a given Cloud Storage bucket and returns the public url
    to the new object.
    """
    #_check_extension(filename, current_app.config['ALLOWED_EXTENSIONS'])
    #filename = _safe_filename(filename)

    client = _get_storage_client()
    #bucket = client.get_bucket(current_app.config['CLOUD_STORAGE_BUCKET'])
    bucket = client.get_bucket('cloud-vision')
    blob = bucket.blob(filename)

    blob.upload_from_string(
        file_stream,
        content_type=content_type)

    url = blob.public_url
    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')

    return url



# file = open('d:/sushil2.jpg', 'r')
# print file
# print file.read()

#foo = storage.upload_file()
# public_url = upload_file(
#         file.read(),
#         "myname",
#         "image/jpeg"
#     )
#image_url = crud.upload_image_file()

# uri = "https://storage.googleapis.com/cloud-vision/demo-peacock1-2016-04-04-174206.jpg"
# _url = uri.split( "/")
# print len(_url)
# gcfile =  _url[len(_url) - 1]
# gcbucket = _url[len(_url) - 2]
# print (gcbucket + " " + gcfile)

# from flask import Flask, url_for
# app = Flask(__name__)
# @app.route('/')
# def index(): pass

# @app.route('/login')
# def login(): pass

# @app.route('/user/<username>')
# def profile(username): pass

# with app.test_request_context():
#  print url_for('index')
#  print url_for('login')
#  print url_for('login', next='/')
#  print url_for('.view', username='John Doe')

import json

myJson = """{"
"responses": "[""{"
    "safeSearchAnnotation":
    "{"
    "medical": "VERY_UNLIKELY", "spoof": "VERY_UNLIKELY", "violence": "VERY_UNLIKELY", "adult": "VERY_UNLIKELY"
    "}",
    "labelAnnotations": "[""{"
        "score": "0.98018545", "mid": "/m/0h29c", "description": "peafowl"
        "}",
        "{"
        "score": "0.94620532", "mid": "/m/015p6", "description": "bird"
        "}",
        "{"
        "score": "0.88552451", "mid": "/m/0jbk", "description": "animal"
        "}",
        "{"
        "score": "0.84765267", "mid": "/m/02cqfm", "description": "close up"
        "}"
    "]"
    "}"
"]"
"}"""



jsonData = """{"responses": [{"safeSearchAnnotation": {"spoof": "VERY_UNLIKELY", "adult": "VERY_UNLIKELY"}, "labelAnnotations": [{"score": "0.98018545", "mid": "/m/0h29c", "description": "peafowl"},{"score": "0.94620532", "mid": "/m/015p6", "description": "bird"}]}]}"""
#workingjsonData = """{"responses": [{"safeSearchAnnotation": {"spoof": "VERY_UNLIKELY", "adult": "VERY_UNLIKELY"}, "labelAnnotations": [{"score": "0.98018545", "mid": "/m/0h29c", "description": "peafowl"},{"score": "0.94620532", "mid": "/m/015p6", "description": "bird"}]}]}"""


#{"data": [{"id": "1543", "name": "Honey Pinter"}]},


def getTargetIds(jsonData):
    data = json.loads(jsonData)

    if 'responses' in data:
        _results = data["responses"][0]
        for attribute in _results:
            if attribute == 'safeSearchAnnotation':
                safe_search_result  = validate_safe_search_annotation(_results[attribute])
            if attribute == 'labelAnnotations': 
                validate_label_result = validate_label_annotations(_results[attribute])
                if validate_label_result:
                    #bird found. chirping....
                    ##Search birdName and 
                    search_bird_results = search_bird(_results[attribute])
                    #bird_mid = get_bird(_results[attribute])
                    if search_bird_results:
                        chirping_bird = search_bird_results[0] #As of now pick at index 0
                        #knowledge search 
                    ##Add to response bird info

#expects input format as [{u'score': u'0.98018545', u'mid': u'/m/0h29c', u'description': u'peafowl'}, {u'score': u'0.94620532', u'mid': u'/m/015p6', u'description': u'bird'}]
bird_name_list = ['hummingbird', 'owl', 'penguin', 'kingfisher', 'peafowl']
def search_bird(input):
    response = []
    i = 0
    for label_annotations in input:
        if label_annotations['description'] in bird_name_list:
            response.append(label_annotations)
            i=+1
    return response



ADULT_PASS_CRITERIA = ['LIKELY', 'UNLIKELY']
VIOLENCE_PASS_CRITERIA = ['VERY_UNLIKELY', 'UNLIKELY']
#expects input format as {"spoof": "VERY_UNLIKELY", "adult": "VERY_UNLIKELY"}
def validate_safe_search_annotation(input):
    pass_flag = False

    for attribute in input:
        if attribute == 'adult':
            if input[attribute] in ADULT_PASS_CRITERIA:
                pass_flag = True 
                #false
            if input[attribute] in VIOLENCE_PASS_CRITERIA and pass_flag:
                pass_flag = True
            else:
                pass_flag = False
    return pass_flag




#expects input format as [{u'score': u'0.98018545', u'mid': u'/m/0h29c', u'description': u'peafowl'}, {u'score': u'0.94620532', u'mid': u'/m/015p6', u'description': u'bird'}]
def validate_label_annotations(input):
    response = {"bird" : "", "score" : ""}
    for label_annotation in input:
        if label_annotation['description'] == 'bird':
            print "Yay! Bird found."
            return True
    return False


import chirping
chirping.start_chirping(jsonData)

#getTargetIds(jsonData)

# https://www.googleapis.com/freebase/v1/search?query=cardiff&lang=en&type=university

# https://www.googleapis.com/freebase/v1/m/0h29c

# import requests
# #url = 'https://www.googleapis.com/freebase/v1/search?query=cardiff&lang=en&type=university'
# url = 'https://www.googleapis.com/freebase/v1/search?query=m/0h29c'
# data = '{"query":{"bool":{"must":[{"text":{"record.document":"SOME_JOURNAL"}},{"text":{"record.articleTitle":"farmers"}}],"must_not":[],"should":[]}},"from":0,"size":50,"sort":[],"facets":{}}'
# print "Calling url"
# response = requests.get(url)
# print response.json()
# print type(response)

# import json
# import urllib

#api_key = open(".freebase_api_key").read()
#service_url = 'https://www.googleapis.com/freebase/v1/search?query=cardiff&lang=en&type=university'
# service_url = 'https://www.googleapis.com/freebase/v1/topic'
# topic_id = '/m/0d6lp'
# params = {
#    'filter': 'suggest'
# }
# url = service_url + topic_id #+ '?' + urllib.urlencode(params)
# topic = json.loads(urllib.urlopen(url).read())
# print topic
# for property in topic['property']:
#   print property + ':'
#   for value in topic['property'][property]['values']:
#     print ' - ' + value['text']