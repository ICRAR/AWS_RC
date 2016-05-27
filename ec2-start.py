#!/usr/bin/python

import sys, getopt
from os.path import expanduser
from os.path import join

try:
    import boto.ec2
    import ConfigParser
except ImportError:
    print('Please run: python setup.py install')

help_line = "ec2-start.py or [-v or --vis] or [-i <ec2_instanceID> or --instanceid=<ec2_instanceID>"

def read_conf(config):
    try:
        region_name = config.get('AWS-CHILES', 'region_name')
        aws_access_key_id = config.get('AWS-CHILES', 'aws_access_key_id')
        aws_secret_access_key = config.get('AWS-CHILES', 'aws_secret_access_key')

    except ImportError:
        print "Error: could not read configuration file %s!" % filename
        sys.exit(2)

    return region_name, aws_access_key_id, aws_secret_access_key

#starts an instance in AWS EC2
def start(region_name, aws_access_key_id, aws_secret_access_key, instanceID, message):
    try:
        conn = boto.ec2.connect_to_region(region_name = region_name,
                    aws_access_key_id = aws_access_key_id,
                    aws_secret_access_key = aws_secret_access_key)
        status = conn.get_all_instance_status(instance_ids = instanceID)
        if len(status) == 0:
            try:
                conn.start_instances(instanceID)
                print message
            except ImportError:
                print 'Error: could not start %s' % (instanceID)
        else:
            print 'The instance is already running! Nothing to do.'

    except ImportError:
        assert False, 'Error: could not authenticate with AWS.'

# this starts an instance based on instanceID
def start_inst(region_name, aws_access_key_id, aws_secret_access_key, instanceID):
    start(region_name, aws_access_key_id, aws_secret_access_key, instanceID,
                'Instance %s is starting...\n' % instanceID)

# this starts SkuareView visualisation server
def start_vis(config, region_name, aws_access_key_id, aws_secret_access_key):
    try:
        instanceID = config.get('AWS-CHILES', 'vis_instanceID')
    except ImportError:
        assert False, 'Error: vis_instanceID not found in config file.'

    start(region_name, aws_access_key_id, aws_secret_access_key, instanceID,
                "Visualisation service is starting...\n"
                "Please wait about 3 to 4 minutes before trying to connect the client.\n"
                "The service will shutdown automatically if not used for 100 minutes.\n")

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hvi:",["help","vis","instanceid="])
    except getopt.GetoptError:
        print 'For help: ec2-start.py [-h or --help]'
        sys.exit(2)

    filename = join(expanduser("~"),'.ec2-aws.cfg')
    config = ConfigParser.RawConfigParser()
    config.read(filename)
    region_name, aws_access_key_id, aws_secret_access_key = read_conf(config)

    for opt, arg in opts:
        if opt in ('--help', '-h'):
            print 'Use: %s' % help_line
        elif opt in ('--vis', '-v'):
            start_vis(config, region_name, aws_access_key_id, aws_secret_access_key)
        elif opt in ('--instanceid', '-i'):
            start_inst(region_name, aws_access_key_id, aws_secret_access_key, arg)
        else:
            assert False, "unhandled option"

if __name__ == '__main__':
    main(sys.argv[1:])
