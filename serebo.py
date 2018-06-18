'''!
Secured Recorder Box (SEREBO) Command Line Interface (CLI)

Date created: 17th May 2018

License: GNU General Public License version 3 for academic or 
not-for-profit use only


SEREBO is free software: you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by the 
Free Software Foundation, either version 3 of the License, or (at your 
option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
import random
import secrets

import fire

import serebo_blackbox as bb


def initialize():
    '''!
    Function to initialize SEREBO blackbox.

    Usage:

        python serebo.py init
    '''
    db = bb.connectDB()

def insertText(message, description='NA'):
    '''!
    Function to insert a text string into SEREBO blackbox.

    Usage:

        python serebo.py intext --message=<text message to be inserted> --description=<explanatory description for this insertion>

    For example:

        python serebo.py intext --message="This is a text message for insertion" --description="Texting 1"

    @param message String: Text string to be inserted.
    @param description String: Explanation string for this entry 
    event. Default = NA.
    '''
    db = bb.connectDB()
    rdata = bb.insertText(db, message, description)
    print('')
    print('Insert Text Status ...')
    print('Message: %s' % rdata['Data'])
    print('Description: %s' % rdata['UserDescription'])
    print('Data Hash: %s' % rdata['DataHash'])
    print('Date Time Stamp: %s' % rdata['DateTimeStamp'])
    print('Number of Pre-existing Blocks in Blockchain: %s' % \
          rdata['ParentBlockID'])
    print('Current Block Hash: %s' % rdata['BlockHash'])
    print('------ Insert Text Successful ------')
    print('')


if __name__ == '__main__':
    exposed_functions = {'init': initialize,
                         'intext': insertText}
    fire.Fire(exposed_functions)