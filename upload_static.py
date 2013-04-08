#!/usr/bin/env python

# Copyright 2013 Globo.com. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os
import re

import flask_s3
from boto.s3.connection import S3Connection

import app

location = None
endpoint = os.environ.get("TSURU_S3_ENDPOINT")
if endpoint:
    location_regexp = re.compile("^https://([a-z0-9-]+)\.amazonaws\.com$")
    m = location_regexp.match(endpoint)
    if m:
        location = m.groups()[0]

all_files = flask_s3._gather_files(app.app, False)
conn = S3Connection(os.environ.get("TSURU_S3_ACCESS_KEY_ID"),
                    os.environ.get("TSURU_S3_SECRET_KEY"))
bucket = conn.get_bucket(os.environ.get("TSURU_S3_BUCKET"))
print "Uploading static files to S3... ",
flask_s3._upload_files(app.app, all_files, bucket)
print "ok"
