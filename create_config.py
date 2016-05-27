
import ConfigParser
import sys
from os.path import expanduser
from os.path import join
from os.path import isfile

if __name__ == '__main__':

    filename = join(expanduser("~"),'.ec2-aws.cfg')
    if isfile(filename):
        print "%s already exist. Delete it first if necessary, and run again." % (filename)
        sys.exit(0)

    try:
        config = ConfigParser.RawConfigParser()
        config.add_section('AWS-CHILES')
        config.set('AWS-CHILES', 'region_name', 'us-west-2')
        config.set('AWS-CHILES', 'aws_access_key_id', '<Insert you aws_access_key_id here>')
        config.set('AWS-CHILES', 'aws_secret_access_key', '<Insert you aws_secret_access_key here>')
        config.set('AWS-CHILES', 'vis_instanceID', '<Insert instance ID for visualisation serive here>')

        with open(filename, 'wb') as configfile:
            config.write(configfile)
        print "Config file's been created %s. Please modify!" % (filename)

    except ImportError:
        print "Error: Unable to create a config file."
