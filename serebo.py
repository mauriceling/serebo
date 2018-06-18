'''!
Secured Recorder Box (SEREBO) Black Box Command Line Interface (CLI)

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

def logFile(filepath, description='NA'):
    '''!
    Function to log a file into SEREBO blackbox.

    Usage:

        python serebo.py logfile --filepath=<path of file to log> --description=<explanatory description for this insertion>

    For example:

        python serebo.py logfile --filepath=doxygen_serebo  --description="Doxygen file for SEREBO"

    @param fileapth String: Path of file to log in SEREBO black box.
    @param description String: Explanation string for this entry 
    event. Default = NA.
    '''
    db = bb.connectDB()
    rdata = bb.logFile(db, filepath, description)
    print('')
    print('File Logging Status ...')
    print('File Hash: %s' % rdata['Data'])
    print('Description: %s' % rdata['UserDescription'])
    print('Data Hash: %s' % rdata['DataHash'])
    print('Date Time Stamp: %s' % rdata['DateTimeStamp'])
    print('Number of Pre-existing Blocks in Blockchain: %s' % \
          rdata['ParentBlockID'])
    print('Current Block Hash: %s' % rdata['BlockHash'])
    print('------ File Logging Successful ------')
    print('')

def systemData():
    
    '''!
    Function to print out data and test hashes of current platform.

    Usage:

        python serebo.py sysdata
    '''
    data = bb.systemData()
    print('')
    print('System Data ...')
    for k in data:
        print('    %s: %s' % (k, data[k]))
    print('------ End of System Data ------')
    print('')

def systemRecord():
    '''!
    Function to record data and test hashes of current platform.

    Usage:

        python serebo.py sysrecord
    '''
    db = bb.connectDB()
    data = bb.systemData()
    dtstamp = db.dtStamp()
    sqlstmt = '''insert into systemdata (dtstamp, key, value) values 
        ('%s', '%s', '%s');'''
    print('')
    print('System Data ...')
    for k in data:
        if k != 'hashdata':
            db.cur.execute(sqlstmt % (str(dtstamp), str(k), 
                                      str(data[k])))
        print('    %s: %s' % (k, data[k]))
    db.conn.commit()
    print('------ End of System Data ------')
    print('')

def fileHash(filepath):
    '''!
    Function to generate and print out hash of a file.

    Usage:

        python serebo.py fhash --filepath=<path of file to hash>
    '''
    fHash = bb.fileHash(filepath)
    print('')
    print('File Path: %s' % str(filepath))
    print('File Hash: %s' % str(fHash))
    print('')


if __name__ == '__main__':
    exposed_functions = {'fhash': fileHash,
                         'init': initialize,
                         'intext': insertText,
                         'logfile': logFile,
                         'sysdata': systemData,
                         'sysrecord': systemRecord}
    fire.Fire(exposed_functions)
