#!/bin/bash
#Start up script
#* activate the virtual env
#* set up credential file variable
#* invoke the start up program

. venv/bin/activate
export GOOGLE_APPLICATION_CREDENTIAL=/home/ubuntu/cloud-vision-file/cloud-vision-2ba51fb06cbf.json
python main.py
