﻿#!/usr/bin/env/ python
################################################################################
#    Copyright 2016 Brecht Baeten
#    This file is part of python-git-package.
#
#    python-git-package is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    python-git-package is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with python-git-package.  If not, see <http://www.gnu.org/licenses/>.
################################################################################

import sys
import os
import datetime
import re
import subprocess

from utils import setup_file,readme_file,gitignore_file,test_file,file_header,license_text,raw_input_validated

def init():

    # default package data
    package_data = {}
    package_data['packagename'] = os.path.split(os.getcwd())[-1]
    package_data['description'] = ''
    package_data['url'] = ''
    package_data['author'] = 'me'
    package_data['author_email'] = ''
    package_data['license'] = 'GPLv3'

    # current year
    now = datetime.datetime.now()
    package_data['year'] = now.year



    # check for existing files
    createsetup = True
    if os.path.isfile('setup.py'):
        response = raw_input_validated('A setup.py file was found, keep this file? (y)','y',['y','n','yes','no'],'Error: {} is not a valid response','Valid responses are:')
        if response in ['y','yes']:
            createsetup = False

    createmanifest = True        
    if os.path.isfile('manifest.in'):
        response = raw_input_validated('A manifest.in file was found, keep this file? (y)','y',['y','n','yes','no'],'Error: {} is not a valid response','Valid responses are:')
        if response in ['y','yes']:
            createmanifest = False
            
    createlicense = True
    if os.path.isfile('LICENSE') or os.path.isfile('license') or os.path.isfile('LICENSE.txt') or os.path.isfile('license.txt') or os.path.isfile('LICENSE.md') or os.path.isfile('license.md'):
        response = raw_input_validated('A license file was found, keep this file? (y)','y',['y','n','yes','no'],'Error: {} is not a valid response','Valid responses are:')
        if response in ['y','yes']:
            createlicense = False

    createreadme = True
    if os.path.isfile('README') or os.path.isfile('readme') or os.path.isfile('README.rst') or os.path.isfile('readme.rst') or os.path.isfile('README.md') or os.path.isfile('readme.md'):
        response = raw_input_validated('A readme file was found, keep this file? (y)','y',['y','n','yes','no'],'Error: {} is not a valid response','Valid responses are:')
        if response in ['y','yes']:
            createreadme = False

    creategitignore = True
    if os.path.isfile('.gitignore'):
        response = raw_input_validated('A .gitignore file was found, keep this file? (y)','y',['y','n','yes','no'],'Error: {} is not a valid response','Valid responses are:')
        if response in ['y','yes']:
            creategitignore = False


    # check existing files for package data
    if not createsetup:
        package_data.update(get_data_from_setup())



    # ask for the package data
    package_data['packagename'] = raw_input('Package name ({}): '.format(package_data['packagename'])) or package_data['packagename']
    package_data['packagename_file'] = package_data['packagename'].replace('-','_')
    package_data['packagename_caps'] = package_data['packagename_file'].title()
    package_data['description'] = raw_input('Package description ({}): '.format(package_data['description'])) or package_data['description']
    package_data['url'] = raw_input('Package url ({}): '.format(package_data['url'])) or package_data['url']
    package_data['author'] = raw_input('Author ({}): '.format(package_data['author'])) or package_data['author']
    package_data['author_email'] = raw_input('Author email ({}): '.format(package_data['author_email'])) or package_data['author_email']
    package_data['license'] = raw_input_validated('License ({}): '.format(package_data['license']),package_data['license'],license_text.keys(),'Error: {} is not a valid license name','Valid licence names are:')




    # create folders
    if not os.path.exists(package_data['packagename_file']):
        os.makedirs(package_data['packagename_file'])
    if not os.path.exists('tests'):
        os.makedirs('tests')
    if not os.path.exists('examples'):
        os.makedirs('examples')


    # create files if they are not present
    if createsetup:
        file = open('setup.py', 'w+')
        file.write(setup_file.format(**package_data))
        file.close()
        
    if createmanifest:
        file = open('manifest.in', 'w+')
        file.write('include README.md\ninclude LICENSE\ninclude examples/example.py')
        file.close()

    if createreadme:
        file = open('README.rst', 'w+')
        file.write(readme_file.format(**package_data))
        file.close()

    if createlicense:
        file = open('LICENSE', 'w+')
        file.write(license_text[package_data['license']])
        file.close()

    if creategitignore:
        file = open('.gitignore', 'w+')
        file.write(gitignore_file)
        file.close()

    filename = os.path.join(package_data['packagename_file'],'__init__.py')
    if not os.path.isfile(filename):
        file = open(filename, 'w+')
        file.write('from __version__ import version as __version__\n')
        file.write('from {} import *\n'.format(package_data['packagename_file']))
        file.close()

    filename = os.path.join(package_data['packagename_file'],'__version__.py')
    if not os.path.isfile(filename):
        file = open(filename, 'w+')
        file.write('version = \'0.0.0\'')
        file.close()

    filename = os.path.join(package_data['packagename_file'],'{}.py'.format(package_data['packagename_file']))
    if not os.path.isfile(filename):
        file = open(filename, 'w+')
        file.write(file_header[package_data['license']].format(**package_data))
        file.close()

    filename = os.path.join('examples','example.py')
    if not os.path.isfile(filename):
        file = open(filename, 'w+')
        file.write(file_header[package_data['license']].format(**package_data))
        file.close()

    filename = os.path.join('tests','test_{}.py'.format(package_data['packagename_file']))
    if not os.path.isfile(filename):
        file = open(filename, 'w+')
        file.write(file_header[package_data['license']].format(**package_data))
        file.write(test_file.format(**package_data))
        file.close()

    filename = os.path.join('tests','all.py')
    if not os.path.isfile(filename):
        file = open(filename, 'w+')
        file.write(file_header[package_data['license']].format(**package_data))
        file.write('import unittest\n\n')
        file.write('from test_{packagename_file} import *\n\n'.format(**package_data))
        file.write('if __name__ == \'__main__\':\n    unittest.main()')
        file.close()


    # initialise a git repository
    output = subprocess.check_output(['git', 'init'])[:-1]


def release():
    """
    Creates a new release
    """

    # search for a version file
    versionfilename = ''
    for d in os.walk('.'):
        filename = os.path.join(d[0],'__version__.py')
        if os.path.isfile(filename):
            versionfilename = filename
            break

    if filename == '':
        print('Could not find __version__.py')

    branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD' ])[:-1]
    
    #if not branch=='master':
    #    raise ValueError('the current branch ({}) is not master.'.format(branch))
    
    # get the previous version number from git
    output = subprocess.check_output(['git', 'tag'])[:-1]
    if not output == '':
        splitoutput = output.split('\n')
        oldversion = splitoutput[-1]

    else:
        # try to get the old version number from __version__.py
        try:
            with open( versionfilename, 'r') as f:
                content = f.readline()
                splitcontent = content.split('\'')
                oldversion = splitcontent[1]
        except:
            print('Error while checking the version number. Check __version__.py')
            return

    splitoldversion = oldversion.split('.')

    print('previous version: {}'.format(oldversion))


    # ask for a new version number
    version = raw_input('new version number: ') 

    # check if the new version is higher than the old version
    splitversion = version.split('.')
    if sum([int(v)*1000**i for i,v in enumerate(splitversion[::-1])]) <= sum([int(v)*1000**i for i,v in enumerate(splitoldversion[::-1])]):
        print('The new version ({}) is not higher than the old version ({})'.format(version,oldversion))
        return

    # ask if you've updated the changelog
    changelog = ''
    response = raw_input_validated('Did you update the changelog? ','',['y','n','yes','no'],'Error: {} is not a valid response','Valid responses are:')
    if response in ['n','no']:
        print('Update the changelog before issuing a release')
        return
        

    print('')
    print('GIT branch: {}'.format(branch) )
    print('Version: {}'.format(version) )

    response = raw_input_validated('Is this ok? ','',['y','n','yes','no'],'Error: {} is not a valid response','Valid responses are:')
    if response in ['n','no']:
        print('Exit')
        return



    # write the new version number to version.py
    with open( versionfilename, 'w') as f:
        f.write( 'version = \'{}\''.format(version) )


    # create a commit message
    message = 'Created new version\nVersion: {}'.format(version)

    if not changelog == '':
        # add the changelog to the commit message
        message = message + '\nChangelog:\\n{}'.format(changelog)

    message = message + '\nThis is an automated commit.'

    # create the commit
    output = subprocess.check_output(['git', 'commit', '-a', '-m', message])[:-1]


    # merge the branch with master
    output = subprocess.check_output(['git', 'checkout', 'master'])[:-1]
    output = subprocess.check_output(['git', 'merge', branch])[:-1]

    # add a git tag
    output = subprocess.check_output(['git', 'tag' ,'{}'.format(version)])[:-1]

    # checkout the old branch
    output = subprocess.check_output(['git', 'checkout', branch])[:-1]



def get_data_from_setup():
    package_data = {}

    with open('setup.py', 'r') as f:
        for line in f:

            matchObj = re.match('.*name=\'(.*)\'',line)
            if matchObj:
                package_data['name'] = matchObj.group(1)

            matchObj = re.match('.*description=\'(.*)\'',line)
            if matchObj:
                package_data['description'] = matchObj.group(1)

            matchObj = re.match('.*author=\'(.*)\'',line)
            if matchObj:
                package_data['author'] = matchObj.group(1)

            matchObj = re.match('.*author_email=\'(.*)\'',line)
            if matchObj:
                package_data['author_email'] = matchObj.group(1)

    return package_data



def execute_from_command_line():
    #print(sys.argv)

    command = sys.argv[1]

    if command == 'init':
        init()
    elif command == 'release':
        release()
    else:
        print('not a valid command')
        print('usage:')




