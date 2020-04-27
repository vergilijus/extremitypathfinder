import os
import re
import sys
from os import listdir
from os.path import abspath, isfile, join, pardir

"""
required packages
numpy
(numba)


these packages have to be installed in virtual environment in use:

right python version! (will influence the tox environments!)
for testing:
conda install pytest
conda install isort
conda install twine

pip install rstcheck pip-tools

rstcheck>=3.3.1
twine for uploading securely

documentation generation:
conda install sphinx
https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html

Use the Makefile to build the docs, like so:
make html


--cov-config=tox.ini

pip-tools package:
TODO write bash script for this
its important to pin requirements to get reproducible errors!
compile a new requirements file (with the latest versions)

source activate tzEnv
pip-compile --upgrade
same as?!:
pip-compile --output-file requirements_tests.txt requirements_tests.in
only update the flask package:
pip-compile --upgrade-package flask
compile a new requirements file (with versions currently used in the virtual env )
pip-compile --generate-hashes requirements_numba.in

do NOT sync. will install ONLY the packages specified! (tox etc. would not be installed any more!)
pip-sync

commands
tox -r to rebuild your tox virtualenvs when you've made changes to requirements setup
# rstcheck will complain about non referenced hyperlinks in doc .rst files! (cannot detect cross file references!)
rstcheck *.rst
tox -r -e codestyle
tox -r -e py37
tox -r -e py37-numba

automatically update imports: isort -rc .
dont use for example.py


Use the Makefile to build the docs, like so:
cd ./docs
make html
# for online build of docs, release tag must be created!

use bandit to check for vulnerabilities:

conda install bandit
bandit ./timezonefinder/*.py

"""

PACKAGE = 'extremitypathfinder'
VERSION_FILE = 'VERSION'

# print('Enter virtual env name:')
# virtual env has to be given!
# VIRT_ENV_NAME = input()
VIRT_ENV_NAME = 'pathEnv'


def get_version():
    return open(VERSION_FILE, 'r').read().strip()


def parse_version(new_version_input='', old_version_str='1.0.0'):
    new_version_input = re.search(r'\d\.\d\.\d+', new_version_input)

    if new_version_input is None:
        raise ValueError  # will cause new input request
    else:
        new_version_input = new_version_input.group()

    # print(new_version_input)

    split_new_version = [int(x) for x in new_version_input.split('.')]
    # print(split_new_version)
    split_old_version = [int(x) for x in old_version_str.split('.')]
    # print(split_old_version)

    for i in range(3):
        if split_new_version[i] > split_old_version[i]:
            break
        if split_new_version[i] < split_old_version[i]:
            raise ValueError  # will cause new input request

    return new_version_input


def set_version(new_version_str):
    with open(VERSION_FILE, 'w') as version_file:
        version_file.write(new_version_str)


def routine(command=None, message='', option1='next', option2='exit'):
    while 1:
        print(message)

        if command:
            print('running command:', command)
            os.system(command)

        print('__________\nDone. Options:')
        print('1)', option1)
        print('2)', option2)
        print('anything else to repeat this step.')
        try:
            inp = int(input())

            if inp == 1:
                print('==============')
                break
            if inp == 2:
                sys.exit()

        except ValueError:
            pass
        print('================')


if __name__ == "__main__":

    print('Do you want to switch to the "dev" branch? Commit before switching branch!')
    print('1) yes, change now.')
    print('2) no, exit')
    print('anything else skip.')
    try:
        inp = int(input())
        if inp == 1:
            os.system('git checkout dev')
            print('==============')
        if inp == 2:
            sys.exit()
    except ValueError:
        pass

    old_version = get_version()

    print('The actual version number is:', old_version)
    print('Enter new version number:')
    version_input = None
    while 1:
        try:
            version_input = input()
            version_str = parse_version(version_input, old_version)
            set_version(version_str)
            break
        except ValueError:
            print(
                f'Invalid version input. Should be of format "x.x.xxx" and higher than the old version {old_version}.')
            pass  # try again

    version = get_version()
    print('the version number has been set to:', version)
    print('=====================')

    routine(None,
            'Maybe re-pin the test dependencies (requirements.txt) with pip-compile!'
            ' Commands are written in the beginning of this script',
            'Done.', 'Exit')
    routine(None,
            'Are all pinned dependencies written in setup.py and the Documentation?',
            'OK. Continue',
            'Exit')
    routine(None, 'Are all (new) features documented?', 'OK. Continue', 'Exit')
    routine(None, 'Remember to write a changelog now for version %s' % version, 'Done. Continue', 'Exit')

    print('___________')
    print('Running TESTS:')

    virt_env_act_command = f'source activate {VIRT_ENV_NAME}; '

    # routine(virt_env_act_command + "pip-compile requirements_tests.in;pip-sync",
    #         'pinning the requirements.txt and bringing virtualEnv to exactly the specified state:', 'next: build check')

    routine(virt_env_act_command + "rstcheck *.rst", 'checking syntax of all .rst files:', 'next: build check')

    # TODO
    # print('generating documentation now...')
    # os.system('(cd ./docs && exec make html)')
    # print('done.')

    # IMPORTANT: -r flag to rebuild tox virtual env
    # only when dependencies have changed!
    rebuild_flag = ''
    print('when the dependencies (in requirements.txt) have changed enter 1 (-> rebuild tox)')
    try:
        inp = int(input())
        if inp == 1:
            rebuild_flag = ' -r'
    except ValueError:
        pass

    # routine(virt_env_act_command + "tox" + rebuild_flag, 'checking syntax, codestyle and imports', 'continue')
    routine(virt_env_act_command + "tox" + rebuild_flag + " -e codestyle",
            'checking syntax, codestyle and imports', 'continue')
    routine(virt_env_act_command + "tox" + rebuild_flag + " -e py37", 'build tests py3', 'continue')

    print('Tests finished.')

    routine(None,
            'Please commit your changes, push and wait if Travis tests build successfully. '
            'Only then merge them into the master.',
            'Build successful. Publish and upload now.', 'Exit.')

    # TODO do this automatically, problem are the commit messages (often the same as changelog)
    # git commit --message
    # git push dev

    # TODO wait for Travis to finish positively

    # if not in master

    # TODO ask to push in master
    # git merge ...

    # TODO switching to master

    print('=================')
    print('PUBLISHING:')

    # routine("python3 setup.py sdist bdist_wheel upload", 'Uploading the package now.') # deprecated
    # new twine publishing routine:
    # https://packaging.python.org/tutorials/packaging-projects/
    routine("python3 setup.py sdist bdist_wheel", 'building the package now.')

    path = abspath(join(__file__, pardir, 'dist'))
    all_archives_this_version = [f for f in os.listdir(path) if isfile(join(path, f)) and version_str in f]
    paths2archives = [abspath(join(path, f)) for f in all_archives_this_version]
    command = "twine upload --repository-url https://test.pypi.org/legacy/ " + ' '.join(paths2archives)

    # upload all archives of this version
    routine(virt_env_act_command + command, 'testing if upload works.')

    command = "twine upload " + ' '.join(paths2archives)
    routine(virt_env_act_command + command, 'real upload to PyPI.')

    # tag erstellen
    routine(None, 'Do you want to create a git release tag?', 'Yes', 'No')

    routine(f"git tag -a v{version} -m 'Version {version}'", 'Creating tag', 'Continue')

    routine(None, 'Do you want to push the git release tag?', 'Yes', 'No')
    # in den master pushen
    os.system("git push --tags")

    print('______________')
    print('Publishing Done.')
    print("only when the upload didn't work: python3 setup.py bdist_wheel upload")
    print('now run:')
    print(f'sudo -H pip install {PACKAGE} --upgrade')
