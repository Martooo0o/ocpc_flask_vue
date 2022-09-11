#!/bin/bash

source myenv/bin/activate

export FLASK_ENV=development

export FLASK_APP=manage_dev.py

flask run --host=localhost
