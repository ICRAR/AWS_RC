#!/usr/bin/python

import sys, getopt
from os.path import expanduser
from os.path import join

try:
    import boto.ec2
    import ConfigParser
except ImportError:
    print('Please run: python setup.py install')

def start_vis():
    try:
        filename = join(expanduser("~"),'.ec2-aws.cfg')
        config = ConfigParser.RawConfigParser()
        config.read(filename)
        region_name = config.get('AWS-CHILES', 'region_name')
        aws_access_key_id = config.get('AWS-CHILES', 'aws_access_key_id')
        aws_secret_access_key = config.get('AWS-CHILES', 'aws_secret_access_key')
        instanceID = config.get('AWS-CHILES', 'vis_instanceID')

    except ImportError:
        print "Error: could not read configuration file %s!" % filename

    try:
        conn = boto.ec2.connect_to_region(region_name = region_name, aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key)
        status = conn.get_all_instance_status(instance_ids = instanceID)
        if len(status) == 0:
            try:
                conn.start_instances(instanceID)
                print 'Visualisation service is starting...\nPlease wait about 3 to 4 minutes before trying to connect the client.\nThe service will shutdown automatically if not used for 100 minutes.\n'
            except ImportError:
                print 'Error: could not start'
        else:
            print 'Visualisation service is already running! Try connecting the client.'

    except ImportError:
        print 'Error: could not authenticate with AWS.'

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hv",["help","vis"])
    except getopt.GetoptError:
        print 'Use: ec2-start.py --vis'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '--help' or opt == '-h':
            print 'Help: ec2-start.py --vis'
            sys.exit()
        elif opt == '--vis' or opt == '-v':
            start_vis()
            sys.exit()

    print 'Use: ec2-start.py --vis'
    sys.exit()

if __name__ == '__main__':
    main(sys.argv[1:])
