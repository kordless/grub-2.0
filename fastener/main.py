from google.auth import compute_engine
from googleapiclient import discovery
from bottle import Bottle, route, run, template, response, request, redirect, error
from json import dumps
import urllib
import random
import string
import sys
import os
import subprocess
import time
import re

# generators
def id_generator(size=4, chars=string.ascii_lowercase + "labs"):return ''.join(random.choice(chars) for _ in range(size))
def password_generator(size=12, chars=string.ascii_lowercase + string.digits):return ''.join(random.choice(chars) for _ in range(size))

# get the token from gcp tag on instance
import httplib2
http = httplib2.Http()
url = 'http://metadata.google.internal/computeMetadata/v1/instance/tags'
headers = {'Metadata-Flavor': 'Google'}
response, content = http.request(url, 'GET', headers=headers)
evalcontent = eval(content)
for item in evalcontent:
        if 'token' in item:
            key,token = item.split('-')

# google creds
credentials = compute_engine.Credentials()
compute = discovery.build('compute', 'v1', credentials=credentials)
compute_beta = discovery.build('compute', 'beta', credentials=credentials)
project = 'mitta-us'

# regions, zones & sizes (NOTE: us-east1 does not have an 'a' zone and has a 'd' zone)
regions = ['us-central1', 'us-west1', 'us-west2', 'us-east4', 'us-east1', 'europe-west2', 'asia-east2'] # numbered 0, 1, 2, etc. in name
zones = ['a', 'b', 'c']
sizes = ['n1-standard-4', 'n1-standard-8', 'n1-standard-16']

app = Bottle(__name__)

# let's not screw around with other requests
@app.error(404)
def error404(error):
    # client_ip = request.environ.get('REMOTE_ADDR')
    client_ip = "foo"
    return dumps({'error': "illegal scan reported from %s" % client_ip, 'response': "fyuta"})


@app.route('/api/instance/list', method='GET')
def list():
    # token
    try:
        if request.query['token'] != token:
            return dumps({'error': "need token"})
    except:
        return dumps({'error': "need token"})

    try:
        items = []
        for r in regions:
            for z in zones:
                for x in range(3):
                    try:
                        # patch us-east1 until we can write better code for it (mirrored below in create)
                        zonealpha = z
                        if r == "us-east1" and z == "a":
                            zonealpha = "d"

                        # query
                        result = compute.instances().list(
                            project=project,
                            zone='%s-%s' % (r, zonealpha)
                        ).execute()
                        break
                    except Exception as ex:
                        print ex
                        print "sleeping..."
                        time.sleep(3)
                        print "waking..."

                try:
                    for item in result['items']:
                        items.append(item)
                except:
                    print "%s-%s has no instances or does not exist" % (r, z)
        return dumps(items)
    except:
        # except Exception as ex:
        print "error: %s" % ex
        return dumps([])


@app.route('/api/instance/<instance_id>/status', method='GET')
def status(instance_id):
    # token
    try:
        if request.query['token'] != token:
            return dumps({'error': "need token"})
    except:
        return dumps({'error': "need token"})

    regionint = instance_id[-2]
    zonealpha = instance_id[-1]

    try:
        result = compute.instances().get(
            project=project,
            zone='%s-%s' % (regions[int(regionint)], zonealpha),
            instance=instance_id
        ).execute()

    except Exception as ex:
        if "HttpError" in str(ex):
            result = {'error': "NOTFOUND"}

        else:
            print "here's an actual error: %s" % ex
            print "trying again"
            try:
                result = compute.instances().get(
                    project=project,
                    zone='%s-%s' % (regions[int(regionint)], zonealpha),
                    instance=instance_id
                ).execute()
            except:
                result = {}
                print "here's an actual error: %s" % ex

    return dumps(result)


@app.route('/api/instance/<instance_id>/start', method='GET')
def start(instance_id):
    # token
    try:
        if request.query['token'] != token:
            return dumps({'error': "need token"})
    except:
        return dumps({'error': "need token"})
    regionint = instance_id[-2]
    zonealpha = instance_id[-1]
    try:
        result = compute.instances().start(
            project=project,
            zone='%s-%s' % (regions[int(regionint)], zonealpha),
            instance=instance_id
        ).execute()
    except Exception as ex:
        print "error: %s" % ex
    return dumps(result)


# start off
app.run(server='paste', host='0.0.0.0', port=80, debug=True)
