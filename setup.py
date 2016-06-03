import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages

import os, sys
from distutils.core import setup
from distutils.command.install import install as _install


def _post_install(dir):
    from subprocess import call
    call([sys.executable, 'create_config.py'])
#    ,
#         cwd=os.path.join(dir, 'awsremote'))


class install(_install):
    def run(self):
        _install.run(self)
        self.execute(_post_install, (self.install_lib,),
                     msg="Creating a default config file...")

setup(
    name = "Remote AWS environment control",
    version = "0.1",
    packages = find_packages(),
    scripts = ['ec2-start.py'],
    setup_requires =['ConfigParser', 'boto'],
    install_requires = ['ConfigParser', 'boto'],

    # metadata for upload to PyPI
    author = "Slava Kitaeff",
    author_email = "slava.kitaeff@icrar.org",
    description = "Set of tools to remotely control AWS EC2 envoronment",
    license = "PSF",
    keywords = "AWS-EC2 remote control",
    url = "https://github.com/ICRAR/AWS_RC",

    cmdclass={'install': install},
    )
