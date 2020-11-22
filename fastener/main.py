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
project = 'labs-209320'

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


# redirect elsewhere
@app.route('/')
def main():
    redirect("https://lucidworks.com/labs")


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


@app.route('/api/instance/<instance_id>/console', method='GET')
def console(instance_id):
    # token
    try:
        if request.query['token'] != token:
            return dumps({'error': "need token"})
    except:
        return dumps({'error': "need token"})

    regionint = instance_id[-2]
    zonealpha = instance_id[-1]

    try:
        result = compute.instances().getSerialPortOutput(
            project=project,
            zone='%s-%s' % (regions[int(regionint)], zonealpha),
            instance=instance_id
        ).execute()
    except Exception as ex:
        result = {}
        print "console probably not ready, but here's the actual error: %s" % ex
    return dumps(result)


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

# requires ssh_key (encoded) and username parameters
@app.route('/api/instance/<instance_id>/addkey', method='GET')
def addkey(instance_id):
    # ssh key
    try:
        if not request.query['ssh_key']:
            return dumps({'error': "need ssh_key"})
        if not request.query['username']:
            return dumps({'error': "need username"})


        ssh_key = urllib.unquote(request.query['ssh_key'])
        username = request.query['username']
    except:
        return dumps({'error': "ssh_key, username required to add keys"})

    regionint = instance_id[-2]
    zonealpha = instance_id[-1]

    status = "FAIL"

    # write ssh_key to file
    try:
        # this be juju
        # convert to use 'compute.instances.setmetadata'
        # for adding metadata to an instance
        f = open("keys/%s_rsa.pub" % username, "w")
        f.write("%s:%s" % (username, ssh_key))
        f.close()

        # likely attack vector through not scrubing github username?
        command = "gcloud compute instances add-metadata %s --metadata-from-file ssh-keys=keys/%s_rsa.pub --zone=%s-%s" % (
            instance_id,
            username,
            regions[int(regionint)],
            zonealpha
        )
        print "executing `%s`" % command

        # sigh (at least it doesn't block)
        commands = command.split()
        p = subprocess.Popen(commands)

        # os.system(command)

        status = "SUCCESS"

    except Exception as ex:
        print ex
        pass

    result = {
        'project': project,
        'zone': '%s-%s' % (regions[int(regionint)], zonealpha),
        'instance': instance_id,
        'ssh_key': ssh_key,
        'status': status
    }

    return dumps(result)


@app.route('/api/instance/<instance_id>/stop', method='GET')
def stop(instance_id):
    # token
    try:
        if request.query['token'] != token:
            return dumps({'error': "need token"})
    except:
        return dumps({'error': "need token"})


@app.route('/api/instance/<instance_id>/delete', method='GET')
def delete(instance_id):
    # token
    try:
        if request.query['token'] != token:
            return dumps({'error': "need token"})
    except:
        return dumps({'error': "need token"})

    regionint = instance_id[-2]
    zonealpha = instance_id[-1]

    try:
        result = compute.instances().delete(
            project=project,
            zone='%s-%s' % (regions[int(regionint)], zonealpha),
            instance=instance_id
        ).execute()
        return dumps(result)

    except Exception as ex:
        print "error: %s" % ex
        return dumps({"response": "%s" % ex})


@app.route('/api/instance/<instance_id>/restart', method='GET')
def reset(instance_id):
    # token
    try:
        if request.query['token'] != token:
            return dumps({'error': "need token"})
    except:
        return dumps({'error': "need token"})
    regionint = instance_id[-2]
    zonealpha = instance_id[-1]
    result = compute.instances().reset(
        project=project,
        zone='%s-%s' % (regions[int(regionint)], zonealpha),
        instance=instance_id
    ).execute()
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


@app.route('/api/stream/<stream_slug>', method='POST')
def create(stream_slug='lou'):
    # token
    try:
        if request.query['token'] != token:
            return dumps({'error': "need token"})
    except:
        return dumps({'error': "need token"})

    try:
        user = request.query['user']
    except:
        user = "prod-unknown"

    try:
        sizeint = request.query['size']
        try:
            size = sizes[int(sizeint)]
        except:
            size = sizes[0]
    except:
        size = sizes[0]

   #F5 hack attack

    #try:
    if stream_slug == "fusion5":
        # name and machine type
        name = id_generator()
        # generate a good password
        subprocess.Popen(["/streams/projects/buttons/fastener/install_fusion5.sh", name])
        response.content_type = 'Application/json'
        return dumps({'instance': name, 'password': 'createapassword'})
    else:
        print "not Fusion 5 placeholder"
       # except:
       #    print "foobar!"

    #End F5 hack attack

    try:
        regionint = request.query['region']
        try:
            region = regions[int(regionint)]

            try:
                # query for region prefered zone
                zonealpha = random.choice('abc')
            except:
                zonealpha = random.choice('abc')

        except:
            region = "any"
    except Exception as ex:
        region = "any"

    try:
        preemptible = request.query['preemptible']
        if int(preemptible) == 0:
            preemptible = False
        else:
            preemptible = True
    except:
        preemptible = True


    while region == "any":
        # trips
        trip = 0

        # random region/zone from regions/zones arrays above
        zonealpha = random.choice(zones)
        regionint = random.randint(0,len(regions)-1)
        region = '%s' % (regions[int(regionint)])

        # patch us-east1 until we can write better code for it
        if region == "us-east1" and zonealpha == "a":
            zonealpha = "d"

        # check to see which zone we can use
        region_check = compute.regions().get(project=project,region=region).execute()

        for quota in region_check['quotas']:
            try:
                if quota['metric'] == "CPUS":
                    usage = quota['usage']
                    limit = quota['limit']
            except:
                # guess we don't have that zone
                print "%s-%s doesn't work" % (region, zonealpha)

        # we start 4 cpu instances
        if (usage+4) <= limit:
            trip = trip + 1
            break

        # otherwise wait a bit
        time.sleep(3)

        # if we've made more than so many requests, we give up
        if trip > 20:
            name = "failed"
            password = "failed"
            response.content_type = 'application/json'
            return dumps({'instance': name, 'password': password})

    # # name and machine type
    iid = id_generator()
    name = 'button-%s-%s%s%s' % (stream_slug, iid, regionint, zonealpha) # use the int, not the name of region
    password = ""

    # generate a good password
    while not bool(re.search(r'\d', password)):
        password = password_generator()

    config = {
        'name': name,
        'scheduling':
        {
            'preemptible': preemptible
        }
    }

    # boot disk and type
    config['disks'] = [{
        'boot': True,
        'type': "PERSISTENT",
        'autoDelete': True,
        'initializeParams': {
            "sourceImage": "projects/ubuntu-os-cloud/global/images/ubuntu-1604-xenial-v20190212",
            "diskType": "projects/%s/zones/%s-%s/diskTypes/pd-ssd" % (project, regions[int(regionint)], zonealpha),
            "diskSizeGb": "100"
        }
    }]

    # service account
    config["serviceAccounts"] = [{
        "email": "%s@appspot.gserviceaccount.com" % project,
        "scopes": [
            "https://www.googleapis.com/auth/devstorage.read_only",
            # remove to increase lockdown for individual boxes (for SSH access for some users)
            # "https://www.googleapis.com/auth/servicecontrol",
            "https://www.googleapis.com/auth/service.management.readonly",
        ]
    }]
    # tags ad labels
    config['tags'] = { 'items': ["fusion"] }
    config['labels'] = { 'type': "button", 'sid': stream_slug, 'iid': iid, 'password': password, 'user': user}
    # network interface
    config['networkInterfaces'] = [{
        'network': 'global/networks/default',
        'accessConfigs': [
            {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
        ]
    }]
    # metadata
    config["metadata"] = {
        "items": [
        {
            "key": "startup-script-url",
            "value": "https://raw.githubusercontent.com/lucidworks/streams/master/projects/buttons/fastener/scripts/start-button.sh"
        },
        {
            "key": "password",
            "value": password
        }]
    }
    # execute the query
    try:
        config['machineType'] = "zones/%s-%s/machineTypes/%s" % (regions[int(regionint)], zonealpha, size)
        operation = compute.instances().insert(
            project=project,
            zone='%s-%s' % (regions[int(regionint)], zonealpha),
            body=config
        ).execute()
    except Exception as ex:
        print ex
        name = "failed"
        password = "failed"
    response.content_type = 'application/json'
    return dumps({'instance': name, 'password': password})

# start off
app.run(server='paste', host='0.0.0.0', port=80, debug=True)
