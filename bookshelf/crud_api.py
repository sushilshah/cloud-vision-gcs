from flask import Blueprint, current_app
from bookshelf import storage
import cloud_vision, json

response = { "imageUrl" : ""}

def foo():
    return "FOO"
    
def identify_image_attributes(files):
    current_app.logger.info("############files : %s" %files)
    image_url = upload_image_file(files)
    response['imageUrl'] = image_url
    _url = image_url.split( "/")
    gcfile =  _url[len(_url) - 1]
    gcbucket = _url[len(_url) - 2]

    cv_response = cloud_vision.identify_image_attributes_gcs(gcfile, gcbucket)
    cv_response_pretty = json.dumps(cv_response, indent=4, sort_keys=True)
    response['cv_response'] = str(cv_response_pretty)
    return response

    
# [START upload_image_file]
def upload_image_file(file):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    print("********************upload file name %s" %file)
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
   
#    return {"identify_image_attributes" : "ok"}
# [END upload_image_file]
    # if request.method == 'POST':
    #     data = request.form.to_dict(flat=True)

    #     # If an image was uploaded, update the data to point to the new image.
    #     # [START image_url]
    #     image_url = upload_image_file(request.files.get('image'))
    #     # [END image_url]
    #     current_app.logger.info("############Image url : %s" %image_url)

    #     _url = image_url.split( "/")
    #     gcfile =  _url[len(_url) - 1]
    #     gcbucket = _url[len(_url) - 2]
        
        
    #     current_app.logger.info("############starting cloud vision gcfile : {} : gcbucket : {}".format(gcfile, gcbucket))
    #     cv_response = cloud_vision.identify_image_attributes_gcsifilesle, gcbucket)
    #     current_app.logger.info("############end cloud vision gcfile :   %s: " %cv_response )
    #     cv_response_pretty = json.dumps(cv_response, indent=4, sort_keys=True)
    #     # [START image_url2]
    #     if image_url:
    #         data['imageUrl'] = image_url
    #         #data['cv_response'] ="cv_response FOOBAR"
    #     # [END image_url2]
    #     if cv_response:
    #         data['cv_response'] = str(cv_response_pretty)

    #     book = get_model().create(data)
        
        #_book = dict(book)

        #current_app.logger.info("############BOOK OBJECT TYPE : " +  str(_book))
        #_book['cv_response'] ="cv_response FOOBAR"
        
        # if cv_response:
        #     book['cv_response'] = cv_response
        # book['cv_response1'] = "cv_response FOOBAR"
        #current_app.logger.info("############BOOK OBJECT :   %s: " %_book )

        #return redirect(url_for('.view', id=book['id']))
        
