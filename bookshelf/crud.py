# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from bookshelf import get_model, storage
from flask import Blueprint, current_app, redirect, render_template, request, \
    url_for
import cloud_vision

crud = Blueprint('crud', __name__)


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
# [END upload_image_file]


@crud.route("/")
def list():
    current_app.logger.info("enter crud.list")
    token = request.args.get('page_token', None)
    books, next_page_token = get_model().list(cursor=token)

    return render_template(
        "list.html",
        books=books,
        next_page_token=next_page_token)


@crud.route('/<id>')
def view(id):
    book = get_model().read(id)
    return render_template("view.html", book=book)


@crud.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        # If an image was uploaded, update the data to point to the new image.
        # [START image_url]
        image_url = upload_image_file(request.files.get('image'))
        # [END image_url]
        current_app.logger.info("############Image url : %s" %image_url)

        uri = image_url
        _url = uri.split( "/")
        print len(_url)
        gcfile =  _url[len(_url) - 1]
        gcbucket = _url[len(_url) - 2]
        print (gcbucket + " " + gcfile)
        
        current_app.logger.info("############starting cloud vision gcfile : {} : gcbucket : {}".format(gcfile, gcbucket))
        cv_response = cloud_vision.identify_image_attributes_gcs(gcfile, gcbucket)
        current_app.logger.info("############end cloud vision gcfile :   %s: " %cv_response )

        # [START image_url2]
        if image_url:
            data['imageUrl'] = image_url
        # [END image_url2]

        book = get_model().create(data)
        if cv_response:
            book['cv_response'] = cv_response
        return redirect(url_for('.view', id=book['id']))

    return render_template("form.html", action="Add", book={})


@crud.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    book = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        image_url = upload_image_file(request.files.get('image'))

        if image_url:
            data['imageUrl'] = image_url

        book = get_model().update(data, id)

        return redirect(url_for('.view', id=book['id']))

    return render_template("form.html", action="Edit", book=book)


@crud.route('/<id>/delete')
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.list'))
