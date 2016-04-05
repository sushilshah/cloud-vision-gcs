

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

uri = "https://storage.googleapis.com/cloud-vision/demo-peacock1-2016-04-04-174206.jpg"
_url = uri.split( "/")
print len(_url)
gcfile =  _url[len(_url) - 1]
gcbucket = _url[len(_url) - 2]
print (gcbucket + " " + gcfile)