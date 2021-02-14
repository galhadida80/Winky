# Copyright 2019 Google LLC
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

import logging
import firestore
from flask import current_app, flash, Flask, Markup, redirect, render_template
from flask import request, url_for
from google.cloud import error_reporting
import google.cloud.logging
import storage
import os

from src import datamovie

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/Hadida/PycharmProjects/Winky/src/Winky.json"

from google.cloud import storage

# # Instantiates a client
# storage_client = storage.Client()
#
# # The name for the new bucket
# bucket_name = "my-new-bucket"
#
# # Creates the new bucket
# bucket = storage_client.create_bucket(bucket_name)
#
# print("Bucket {} created.".format(bucket.name))

# [START upload_image_file]
def upload_image_file(img):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    if not img:
        return None

    public_url = storage.upload_file(
        img.read(),
        img.filename,
        img.content_type
    )

    current_app.logger.info(
        'Uploaded file %s as %s.', img.filename, public_url)

    return public_url
# # [END upload_image_file]


app = Flask(__name__)
app.config.update(
    SECRET_KEY='secret',
    MAX_CONTENT_LENGTH=8 * 1024 * 1024,
    ALLOWED_EXTENSIONS=set(['png', 'jpg', 'jpeg', 'gif'])
)

app.debug = False
app.testing = False

# @app.route('/')
# def index():
#     return "Hello World!"

# Configure logging
if not app.testing:
    logging.basicConfig(level=logging.INFO)
    client = google.cloud.logging.Client()
    # Attaches a Google Stackdriver logging handler to the root logger
    client.setup_logging()
    print(client)



@app.route('/')
def index():
    t=datamovie.listmovie()
    return render_template('Movielist.html', movies=t)
# def list():
#     return 0
#     start_after = request.args.get('start_after', None)
    # books, last_title = firestore.next_page(start_after=start_after)
    #
    # return render_template('list.html', books=books, last_title=last_title)


@app.route('/books/<book_id>')
def view(book_id):
    book = firestore.read(book_id)
    return render_template('view.html', book=book)






# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)
