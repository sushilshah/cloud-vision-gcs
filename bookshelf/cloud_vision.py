#!/usr/bin/python

# Copyright 2016 Google, Inc
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

"""Identifies the landmark for the given image."""

import argparse

from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials
from flask import current_app
import chirping

# [START get_vision_service]
# The url template to retrieve the discovery document for trusted testers.
DISCOVERY_URL='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'


def get_vision_service():
    credentials = GoogleCredentials.get_application_default()
    return discovery.build('vision', 'v1', credentials=credentials,
                           discoveryServiceUrl=DISCOVERY_URL)
# [END get_vision_service]


# [START identify_landmark]
def identify_image_attributes(gcs_uri, max_results=4):
    """Uses the Vision API to identify the landmark in the given image.

    Args:
        gcs_uri: A uri of the form: gs://bucket/object

    Returns:
        An array of dicts with information about the landmarks in the picture.
    """
    print ("**** Got max_results %s " %max_results)
    batch_request = [{
        'image': {
            'source': {
                'gcs_image_uri': gcs_uri
            }
        },
        'features': [{
            'type': 'LANDMARK_DETECTION',
            'maxResults': max_results,
            },
            {
            "type": "LABEL_DETECTION",
            'maxResults': max_results
            },
            {
            "type": "SAFE_SEARCH_DETECTION",
            'maxResults': max_results
        }]
    }]

    service = get_vision_service()
    request = service.images().annotate(body={
        'requests': batch_request,
        })
    response = request.execute()

    #return response['responses'][0].get('landmarkAnnotations', None)
    return response
# [END identify_landmark]

# [START identify_image_attributes_gcs]
def identify_image_attributes_gcs(gcs_file, gcs_bucket, max_results=4):
    gcs_uri = "gs://" + str(gcs_bucket) + "/" + str(gcs_file)
    return identify_image_attributes(gcs_uri, max_results)
# [END identify_image_attributes_gcs]

# [START get_attributes_info]
def get_attributes_info(response_json, attribute_identifier, get_kg=False):
    attribute = current_app.config['ATTRIBUTE_' + attribute_identifier]
    
    if attribute == 'bird':
        attribute = ""
        chirping_response = chirping.start_chirping(response_json, get_kg)
        print "CV chirping_response"
        print chirping_response
    else:
        raise ValueError(
            "No appropriate attribute found in the config file for the attribute: " + attribute_identifier +" . "
            "Please configure the values in config file.")
    return chirping_response
# [END get_attributes_info]