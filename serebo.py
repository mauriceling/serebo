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
import sqlite3

import fire

import serebo_blackbox as bb
import serebo_notary_api as notary


def initialize(bbpath='serebo_blackbox\\blackbox.sdb'):
    '''!
    Function to initialize SEREBO blackbox.

    Usage:

        python serebo.py init --bbpath=<path to SEREBO black box>

    For example:

        python serebo.py init --bbpath='serebo_blackbox\\blackbox.sdb'

    @param bbpath String: Path to SEREBO black box. Default = 
    'serebo_blackbox\\blackbox.sdb'.
    '''
    db = bb.connectDB(bbpath)
    try:
        sqlstmt = '''insert into metadata (key, value) values ('serebo_blackbox_path', '%s');''' % (str(db.path))
        db.cur.execute(sqlstmt)
        db.conn.commit()
    except sqlite3.IntegrityError: pass
    print('')
    return {'SEREBO Black Box': db,
            'Black Box Path': str(db.path)}

def insertText(message, description='NA', 
               bbpath='serebo_blackbox\\blackbox.sdb'):
    '''!
    Function to insert a text string into SEREBO blackbox.

    Usage:

        python serebo.py intext --message=<text message to be inserted> --description=<explanatory description for this insertion> --bbpath=<path to SEREBO black box>

    For example:

        python serebo.py intext --message="This is a text message for insertion" --description="Texting 1" --bbpath='serebo_blackbox\\blackbox.sdb'

    @param message String: Text string to be inserted.
    @param description String: Explanation string for this entry 
    event. Default = NA.
    @param bbpath String: Path to SEREBO black box. Default = 
    'serebo_blackbox\\blackbox.sdb'.
    '''
    db = bb.connectDB(bbpath)
    rdata = bb.insertText(db, message, description)
    print('')
    print('Insert Text Status ...')
    return {'SEREBO Black Box': db,
            'Black Box Path': str(db.path),
            'Date Time Stamp': str(rdata['DateTimeStamp']),
            'Message': str(rdata['Data']),
            'Description': str(rdata['UserDescription']),
            'Data Hash': str(rdata['DataHash'])}

def logFile(filepath, description='NA',
            bbpath='serebo_blackbox\\blackbox.sdb'):
    '''!
    Function to log a file into SEREBO blackbox.

    Usage:

        python serebo.py logfile --filepath=<path of file to log> --description=<explanatory description for this insertion> --bbpath=<path to SEREBO black box>

    For example:

        python serebo.py logfile --filepath=doxygen_serebo  --description="Doxygen file for SEREBO" --bbpath='serebo_blackbox\\blackbox.sdb'

    @param fileapth String: Path of file to log in SEREBO black box.
    @param description String: Explanation string for this entry 
    event. Default = NA.
    @param bbpath String: Path to SEREBO black box. Default = 
    'serebo_blackbox\\blackbox.sdb'.
    '''
    db = bb.connectDB(bbpath)
    rdata = bb.logFile(db, filepath, description)
    print('')
    print('File Logging Status ...')
    return {'SEREBO Black Box': db,
            'Black Box Path': str(db.path),
            'Date Time Stamp': str(rdata['DateTimeStamp']),
            'File Hash': str(rdata['Data']),
            'Description': str(rdata['UserDescription']),
            'Data Hash': str(rdata['DataHash'])}

def systemData():
    
    '''!
    Function to print out data and test hashes of current platform.

    Usage:

        python serebo.py sysdata
    '''
    data = bb.systemData()
    print('')
    print('System Data ...')
    return {'architecture': str(data['architecture']),
            'machine': str(data['machine']),
            'node': str(data['node']),
            'platform': str(data['platform']),
            'processor': str(data['processor']),
            'python_build': str(data['python_build']),
            'python_compiler': str(data['python_compiler']),
            'python_implementation': str(data['python_implementation']),
            'python_branch': str(data['python_branch']),
            'python_revision': str(data['python_revision']),
            'python_version': str(data['python_version']),
            'release': str(data['release']),
            'system': str(data['system']),
            'version': str(data['version']),
            'hashdata': str(data['hashdata']),
            'hash_md5': str(data['hash_md5']),
            'hash_sha1': str(data['hash_sha1']),
            'hash_sha224': str(data['hash_sha224']),
            'hash_sha3_224': str(data['hash_sha3_224']),
            'hash_sha256': str(data['hash_sha256']),
            'hash_sha3_256': str(data['hash_sha3_256']),
            'hash_sha384': str(data['hash_sha384']),
            'hash_sha3_384': str(data['hash_sha3_384']),
            'hash_sha512': str(data['hash_sha512']),
            'hash_sha3_512': str(data['hash_sha3_512']),
            'hash_blake2b': str(data['hash_blake2b']),
            'hash_blake2s': str(data['hash_blake2s'])}

def systemRecord(bbpath='serebo_blackbox\\blackbox.sdb'):
    '''!
    Function to record data and test hashes of current platform.

    Usage:

        python serebo.py sysrecord --bbpath=<path to SEREBO black box>

    For example:

        python serebo.py sysrecord --bbpath='serebo_blackbox\\blackbox.sdb'

    @param bbpath String: Path to SEREBO black box. Default = 
    'serebo_blackbox\\blackbox.sdb'.
    '''
    db = bb.connectDB(bbpath)
    data = bb.systemData()
    dtstamp = bb.dateTime(db)
    sqlstmt = '''insert into systemdata (dtstamp, key, value) values 
        ('%s', '%s', '%s');'''
    print('')
    print('System Data ...')
    for k in data:
        if k != 'hashdata':
            db.cur.execute(sqlstmt % (str(dtstamp), str(k), 
                                      str(data[k])))
    db.conn.commit()
    return {'SEREBO Black Box': db,
            'Black Box Path': str(db.path),
            'architecture': str(data['architecture']),
            'machine': str(data['machine']),
            'node': str(data['node']),
            'platform': str(data['platform']),
            'processor': str(data['processor']),
            'python_build': str(data['python_build']),
            'python_compiler': str(data['python_compiler']),
            'python_implementation': str(data['python_implementation']),
            'python_branch': str(data['python_branch']),
            'python_revision': str(data['python_revision']),
            'python_version': str(data['python_version']),
            'release': str(data['release']),
            'system': str(data['system']),
            'version': str(data['version']),
            'hashdata': str(data['hashdata']),
            'hash_md5': str(data['hash_md5']),
            'hash_sha1': str(data['hash_sha1']),
            'hash_sha224': str(data['hash_sha224']),
            'hash_sha3_224': str(data['hash_sha3_224']),
            'hash_sha256': str(data['hash_sha256']),
            'hash_sha3_256': str(data['hash_sha3_256']),
            'hash_sha384': str(data['hash_sha384']),
            'hash_sha3_384': str(data['hash_sha3_384']),
            'hash_sha512': str(data['hash_sha512']),
            'hash_sha3_512': str(data['hash_sha3_512']),
            'hash_blake2b': str(data['hash_blake2b']),
            'hash_blake2s': str(data['hash_blake2s'])}

def fileHash(filepath):
    '''!
    Function to generate and print out hash of a file.

    Usage:

        python serebo.py fhash --filepath=<path of file to hash>

    For example:

        python serebo.py fhash --filepath=doxygen_serebo
    '''
    fHash = bb.fileHash(filepath)
    print('')
    return {'File Path': str(filepath),
            'File Hash': str(fHash)}

def localCode(length, description=None, 
              bbpath='serebo_blackbox\\blackbox.sdb'):
    '''!
    Function to generate a random string, and log this generation into 
    SEREBO blackbox.

    Usage:

        python serebo.py localcode --length=<length of random string> --description=<explanatory description for this insertion> --bbpath=<path to SEREBO black box> 

    For example:

        python serebo.py localcode --length=10 --description="Notarizing certificate ABC123" --bbpath='serebo_blackbox\\blackbox.sdb'

    @param length Integer: Length of random string to generate
    @param description String: Explanation string for this entry 
    event. Default = None.
    @param bbpath String: Path to SEREBO black box. Default = 
    'serebo_blackbox\\blackbox.sdb'.
    '''
    db = bb.connectDB(bbpath)
    rstring = bb.randomString(db, length)
    description = ['Local random string generation'] + [description]
    description = ' | '.join(description)
    rdata = bb.insertFText(db, rstring, description)
    print('')
    print('Generate Random String (Local) ...')
    return {'SEREBO Black Box': db,
            'Black Box Path': str(db.path),
            'Date Time Stamp': str(rdata['DateTimeStamp']),
            'Random String': str(rstring)}

def localDTS(bbpath='serebo_blackbox\\blackbox.sdb'):
    '''!
    Function to get date time string. This event is not logged.

    Usage:

        python serebo.py localdts --bbpath=<path to SEREBO black box> 

    For example:

        python serebo.py localdts --bbpath='serebo_blackbox\\blackbox.sdb'

    @param bbpath String: Path to SEREBO black box. Default = 
    'serebo_blackbox\\blackbox.sdb'.
    '''
    db = bb.connectDB(bbpath)
    dts = bb.dateTime(db)
    print('')
    return {'SEREBO Black Box': db,
            'Black Box Path': str(db.path),
            'Date Time Stamp': str(dts)}

def stringHash(dstring, bbpath='serebo_blackbox\\blackbox.sdb'):
    '''!
    Function to generate hash for a data string. This event is not 
    logged.

    Usage:

        python serebo.py shash --dstring=<string to hash> --bbpath=<path to SEREBO black box> 

    For example:

        python serebo.py shash --dstring="SEREBO is hosted at https://github.com/mauriceling/serebo" --bbpath='serebo_blackbox\\blackbox.sdb'

    @param dstring String: String to generate hash.
    @param bbpath String: Path to SEREBO black box. Default = 
    'serebo_blackbox\\blackbox.sdb'.
    '''
    db = bb.connectDB(bbpath)
    x = bb.stringHash(db, dstring)
    print('')
    return {'SEREBO Black Box': db,
            'Black Box Path': str(db.path),
            'Data String': str(dstring),
            'Data Hash': str(x)}

def registerBlackbox(owner, email, alias, 
                     notaryURL='https://mauricelab.pythonanywhere.com/serebo_notary/services/call/xmlrpc',
                     bbpath='serebo_blackbox\\blackbox.sdb'):
    '''!
    Function to register SEREBO Black Box with SEREBO Notary.

    Usage:

        python serebo.py register --alias=<alias for this SEREBO Notary> --notaryURL="https://mauricelab.pythonanywhere.com/serebo_notary/services/call/xmlrpc" --owner=<owner's name> --email=<owner's email> --bbpath=<path to SEREBO black box> 

    For example:

        python serebo.py register --alias="NotaryPythonAnywhere" --notaryURL="https://mauricelab.pythonanywhere.com/serebo_notary/services/call/xmlrpc" --owner="Maurice HT Ling" --email="mauriceling@acm.org" --bbpath='serebo_blackbox\\blackbox.sdb'

    @param owner String: Owner's or administrator's name.
    @param email String: Owner's or administrator's email.
    @param alias String: Alias for this SEREBO Notary.
    @param notaryURL String: URL for SEREBO Notary web service. 
    Default="https://mauricelab.pythonanywhere.com/serebo_notary/services/call/xmlrpc"
    @param bbpath String: Path to SEREBO black box. Default = 
    'serebo_blackbox\\blackbox.sdb'.
    '''
    db = bb.connectDB(bbpath)
    owner = str(owner)
    email = str(email)
    sqlstmt = "select value from metadata where key='blackboxID'"
    blackboxID = [row for row in db.cur.execute(sqlstmt)][0][0]
    data = bb.systemData() 
    architecture = data['architecture']
    machine = data['machine']
    node = data['node'] 
    platform = data['platform'] 
    processor = data['processor']
    try:
        (notaryURL, notaryAuthorization, dtstamp) = \
            notary.registerBlackbox(blackboxID, owner, email, 
                                    architecture, machine, node, 
                                    platform, processor, notaryURL)
        sqlstmt = '''insert into notary (dtstamp, alias, owner, email, notaryDTS, notaryAuthorization, notaryURL) values (?,?,?,?,?,?,?)'''
        sqldata = (db.dtStamp(), alias, owner, email, 
                   dtstamp, notaryAuthorization, notaryURL)
        db.cur.execute(sqlstmt, sqldata)
        db.conn.commit()
        rstring = 'Register SEREBO Black Box with SEREBO Notary'
        description = ['Notary URL: %s' % str(notaryURL),
                       'Notary Authorization: %s' % \
                            str(notaryAuthorization),
                        'Notary Date Time Stamp %s' % str(dtstamp)]
        description = ' | '.join(description)
        rdata = bb.insertFText(db, rstring, description)
        print('')
        print('Registering SEREBO Black Box with SEREBO Notary...')
        return {'SEREBO Black Box': db,
                'Black Box Path': str(db.path),
                'Black Box ID': str(blackboxID),
                'Notary URL': str(notaryURL),
                'Notary Authorization': str(notaryAuthorization),
                'Notary Date Time Stamp': str(dtstamp)}
    except:
        print('Registration failed - likely to be SEREBO Notary error or XMLRPC error.')
        return {'SEREBO Black Box': db,
                'Black Box Path': str(db.path),
                'Black Box ID': str(blackboxID),
                'Notary URL': str(notaryURL)}

def selfSign(bbpath='serebo_blackbox\\blackbox.sdb'):
    '''!
    Function to self-sign (self notarization) SEREBO Black Box.

    Usage:

        python serebo.py selfsign --bbpath=<path to SEREBO black box> 

    For example:

        python serebo.py selfsign --bbpath='serebo_blackbox\\blackbox.sdb'

    @param bbpath String: Path to SEREBO black box. Default = 
    'serebo_blackbox\\blackbox.sdb'.
    '''
    db = bb.connectDB(bbpath)
    rstring = bb.randomString(db, 32) 
    rdata = bb.insertFText(db, rstring, 'Self notarization')
    print('')
    print('Self-Signing / Self-Notarization ...')
    return {'SEREBO Black Box': db,
            'Black Box Path': str(db.path),
            'Date Time Stamp': str(rdata['DateTimeStamp']),
            'Random String': str(rstring)}

def notarizeBlackbox(alias, bbpath='serebo_blackbox\\blackbox.sdb'):
    '''!
    Function to notarize SEREBO Black Box with SEREBO Notary.

    Usage:

        python serebo.py notarizebb --alias=<alias for SEREBO Notary> --bbpath=<path to SEREBO black box> 

    For example:

        python serebo.py notarizebb --alias="NotaryPythonAnywhere" --bbpath='serebo_blackbox\\blackbox.sdb'

    @param alias String: Alias for this SEREBO Notary.
    @param bbpath String: Path to SEREBO black box. Default = 
    'serebo_blackbox\\blackbox.sdb'.
    '''
    db = bb.connectDB(bbpath)
    sqlstmt = "select value from metadata where key='blackboxID'"
    blackboxID = [row for row in db.cur.execute(sqlstmt)][0][0]
    try:
        sqlstmt = "select notaryAuthorization, notaryURL from notary where alias='%s'" % str(alias)
        sqlresult = [row for row in db.cur.execute(sqlstmt)][0]
        notaryAuthorization = sqlresult[0]
        notaryURL = sqlresult[1]
    except IndexError:
        print('Notary authorization or Notary URL not found for the given alias')
        return {'SEREBO Black Box': db,
                'Black Box Path': str(db.path),
                'Notary Alias': str(alias)}
    dtstampBB = bb.dateTime(db)
    codeBB = bb.randomString(db, 32)
    try:
        (notaryURL, dtstampNS, codeNS, codeCommon) = \
            notary.notarizeBB(blackboxID, notaryAuthorization, 
                              dtstampBB, codeBB, notaryURL)
        description = ['Notarization with SEREBO Notary',
                       'Black Box Code: %s' % codeBB,
                       'Black Box Date Time: %s' % dtstampBB,
                       'Notary Code: %s' % codeNS,
                       'Notary Date Time: %s' % dtstampNS,
                       'Notary URL: %s' % notaryURL]
        description = ' | '.join(description)
        rdata = bb.insertFText(db, codeCommon, description)
        print('')
        print('Notarizing SEREBO Black Box with SEREBO Notary...')
        return {'SEREBO Black Box': db,
                'Black Box Path': str(db.path),
                'Notary Alias': str(alias),
                'Notary URL': str(notaryURL),
                'Notary Authorization': str(notaryAuthorization),
                'Notary Date Time Stamp': str(dtstampNS),
                'Date Time Stamp': str(dtstampBB),
                'Black Box Code': str(codeBB),
                'Notary Code': str(codeNS),
                'Cross-Signing Code': str(codeCommon)}
    except:
        print('Failed in attempt to notarize SEREBO Black Box with SEREBO Notary')
        return {'SEREBO Black Box': db,
                'Black Box Path': str(db.path),
                'Notary Alias': str(alias),
                'Notary URL': str(notaryURL),
                'Notary Authorization': str(notaryAuthorization)}

def viewRegistration(bbpath='serebo_blackbox\\blackbox.sdb'):
    '''!
    Function to view all SEREBO Notary registration for this SEREBO 
    Black Box - This does not insert a record into SEREBO Black Box.

    Usage:

        python serebo.py viewreg --bbpath=<path to SEREBO black box> 

    For example:

        python serebo.py viewreg --bbpath='serebo_blackbox\\blackbox.sdb'

    @param bbpath String: Path to SEREBO black box. Default = 
    'serebo_blackbox\\blackbox.sdb'.
    '''
    db = bb.connectDB(bbpath)
    sqlstmt = '''select ID, dtstamp, alias, owner, email, notaryDTS, notaryAuthorization, notaryURL from notary'''
    sqlresult = {}
    for row in db.cur.execute(sqlstmt):
        ID = row[0]
        reg = {'Date Time Stamp': str(row[1]),
               'Notary Alias': str(row[2]),
               'Owner': str(row[3]),
               'Email': str(row[4]),
               'Notary Date Time Stamp': str(row[5]),
               'Notary Authorization': str(row[6]),
               'Notary URL': str(row[7])}
        sqlresult[str(ID)] = reg
    return {'SEREBO Black Box': db,
            'Black Box Path': str(db.path),
            'Notary Registrations': sqlresult}


if __name__ == '__main__':
    exposed_functions = {\
         #'audit_blockchain': auditBlockchain,
         #'audit_count': auditCount,
         #'audit_data_blockchain': auditDataBlockchain,
         #'audit_datahash': auditDatahash,
         #'audit_notarizebb': auditNotarizeBB,
         #'audit_register': auditRegister,
         #'backup': backup,
         #'changealias': changeAlias,
         #'dump': dump,
         'fhash': fileHash,
         'init': initialize,
         'intext': insertText,
         'localcode': localCode,
         'localdts': localDTS,
         'logfile': logFile,
         'notarizebb': notarizeBlackbox,
         #'notarizesn': notarizeNotary,
         'register': registerBlackbox,
         #'searchmsg': searchMessage,
         #'searchdesc': searchDescription,
         #'searchfile': searchFile,
         'selfsign': selfSign,
         'shash': stringHash,
         'sysdata': systemData,
         'sysrecord': systemRecord,
         'viewreg': viewRegistration}
    fire.Fire(exposed_functions)
