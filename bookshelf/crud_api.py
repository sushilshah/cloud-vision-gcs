from flask import Blueprint, current_app
from bookshelf import storage
import cloud_vision, json

response = { "imageUrl" : ""}

#[START identify_image_attributes]
def identify_image_attributes(files, max_results=4):
    image_url = upload_image_file(files)
    response['imageUrl'] = image_url
    _url = image_url.split( "/")
    gcfile =  _url[len(_url) - 1]
    gcbucket = _url[len(_url) - 2]
    cv_response = cloud_vision.identify_image_attributes_gcs(gcfile, gcbucket, max_results)
    if cv_response:
        response['cv_response'] = cv_response
        attrib_info = cloud_vision.get_attributes_info(cv_response, "BIRD", True)
    if attrib_info:
        response["birdInfo"] = attrib_info
    return response
#[END identify_image_attributes]

    
# [START upload_image_file]
def upload_image_file(file):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    
    if not file:
        return None

    public_url = storage.upload_file(
        file.read(),
        file.filename,
        file.content_type
    )

    current_app.logger.info(
        "Uploaded file %s as %s content type %s.", file.filename, public_url, file.content_type)

    return public_url