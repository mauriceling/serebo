'''!
Secured Recorder Box (SEREBO) Application Programming Interface (API)

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
import hashlib
import random
import secrets
import os.path
import time

from . import sereboDB
from .sereboDB import SereboDB

def connectDB(bbpath='serebo_blackbox\\blackbox.sdb'):
    '''!
    Function to connect to SEREBO database - the recorder box.

    @param bbpath String: Path to SEREBO black box. Default = 
    'serebo_blackbox\\blackbox.sdb'.
    @return: SEREBO database object
    '''
    bbpath = os.path.abspath(bbpath)
    db = SereboDB(bbpath)
    return db

def systemData():
    '''!
    Function to extract data and test hashes of current platform.

    @return: Dictionary of system data and test hashs 
    '''
    import platform
    data = {\
        'architecture': ':'.join(platform.architecture()),
        'machine': platform.machine(),
        'node': platform.node(),
        'platform': platform.platform(),
        'processor': platform.processor(),
        'python_build': ' > '.join(platform.python_build()),
        'python_compiler': platform.python_compiler(),
        'python_implementation': platform.python_implementation(),
        'python_branch': platform.python_branch(),
        'python_revision': platform.python_revision(),
        'python_version': platform.python_version(),
        'release': platform.release(),
        'system': platform.system(),
        'version': platform.version()
        }
    data['hashdata'] = \
    bytes('''yd6jwAYeqHmzSyxkNOVXTGtDr8dgZIE9LoL9jxRUbqOEuODCysfeJkLJHy3LuQX3Rp4f1Ms5HcfTDAyjdLSpNVJx2vbksBKAAi5VVkhW7MJ9CtlfZBlBvCYbX8Qk8Jw27fsglmaPmbR9BZQoFpuSQxCDF77dmCcbqw5WiKfuTQiUl9PeyHemnMVtsRGKfN2c0x0BA54HjOyN30Dy86fJhitrhLsW3wIY9PtzFEcXd1rq36cFKfrNp7lRjJzDJ4W8ZCuQY6P3HUM8Eu4fsGytH9WlVmJ1aJGiyPVf1ZAa42yKUnfBUwhFNU1aEtplVeHrQqQvO7tLxyE5Oc8TjRF7sAzQozjVbNyhVlxOmhI45pX4qtBA9y9XrHfYJP9RJaprTsnR24g1pOjxVypzEjSGVEh7EKYWXk7fLllwWRkAb7rG5HSEH5gmcsvbpTNNEsXfcmmyrvvh6i7cfQGPap2XmxjO6VRZg1hkf7yUarltZ1kTdD3pMJRBoPpPijuqB1uA''', 'utf-8')
    data['hash_md5'] = hashlib.md5(data['hashdata']).hexdigest()
    data['hash_sha1'] = hashlib.sha1(data['hashdata']).hexdigest()
    data['hash_sha224'] = hashlib.sha224(data['hashdata']).hexdigest()
    data['hash_sha3_224'] = \
        hashlib.sha3_224(data['hashdata']).hexdigest()
    data['hash_sha256'] = hashlib.sha256(data['hashdata']).hexdigest()
    data['hash_sha3_256'] = \
        hashlib.sha3_256(data['hashdata']).hexdigest()
    data['hash_sha384'] = hashlib.sha384(data['hashdata']).hexdigest()
    data['hash_sha3_384'] = \
        hashlib.sha3_384(data['hashdata']).hexdigest() 
    data['hash_sha512'] = hashlib.sha512(data['hashdata']).hexdigest()
    data['hash_sha3_512'] = \
        hashlib.sha3_512(data['hashdata']).hexdigest() 
    data['hash_blake2b'] = \
        hashlib.blake2b(data['hashdata']).hexdigest() 
    data['hash_blake2s'] = \
        hashlib.blake2s(data['hashdata']).hexdigest()
    return data

def insertText(sdb_object, text, description='NA'):
    '''!
    Function to insert text string into SEREBO database, with 
    10-random character string suffixing the description.

    A dictionary of items generated will be returned with the 
    following keys: (1) DateTimeStamp is the UTC date time stamp 
    of this event, (2) Data is the given data string to be 
    inserted, (3) UserDescription is the user given explanation 
    string for this event suffixed with a 10-character random 
    string, (4) DataHash is the hash string of Data, (5) 
    ParentBlockID is the ID of the parent block in blockchain, (6) 
    ParentDateTimeStamp is the UTC date time stamp of the parent 
    block in blockchain (which is also the parent insertion 
    event), (7) ParentRandomString is the random string generated 
    in parent block in blockchain, (8) ParentHash is the hash of 
    parent block in blockchain, (9) BlockRandomString is the 
    random string generated for current insertion event, and (10) 
    BlockHash is the block hash of current insertion event in 
    blockchain.

    @param sdb_object Object: SEREBO database object.
    @param text String: Text string to be inserted.
    @param description String: Explanation string for this entry 
    event. Default = NA.
    @return: Dictionary of data generated from this event.
    '''
    rdata = sdb_object.insertData(text, description, 'text')
    return rdata

def insertFText(sdb_object, text, description='NA'):
    '''!
    Function to insert text string into SEREBO database, without 
    10-random character string suffixing the description.

    A dictionary of items generated will be returned with the 
    following keys: (1) DateTimeStamp is the UTC date time stamp 
    of this event, (2) Data is the given data string to be 
    inserted, (3) UserDescription is the user given explanation 
    string for this event, (4) DataHash is the hash string of Data, 
    (5) ParentBlockID is the ID of the parent block in blockchain, (6) 
    ParentDateTimeStamp is the UTC date time stamp of the parent 
    block in blockchain (which is also the parent insertion 
    event), (7) ParentRandomString is the random string generated 
    in parent block in blockchain, (8) ParentHash is the hash of 
    parent block in blockchain, (9) BlockRandomString is the 
    random string generated for current insertion event, and (10) 
    BlockHash is the block hash of current insertion event in 
    blockchain.

    @param sdb_object Object: SEREBO database object.
    @param text String: Text string to be inserted.
    @param description String: Explanation string for this entry 
    event. Default = NA.
    @return: Dictionary of data generated from this event.
    '''
    rdata = sdb_object.insertData(text, description, 'ftext')
    return rdata

def absolutePath(filepath):
    '''!
    Function to convert file path (absolute or relative file path) 
    into absolute file path.

    @param filepath String: File path to be converted.
    @return: Absolute file path.
    '''
    return os.path.abspath(filepath)

def fileHash(filepath):
    '''!
    Function to generate a series of 12 hashes for a given file, in 
    the format of <MD5>:<SHA1>:<SHA224>:<SHA3 244>:<SHA256>:<SHA3 
    256>:<SHA384>:<SHA3 384>:<SHA512>:<SHA3 215>:<Blake 2b>:<Blake 
    2s>.

    @param filepath String: Path of file for hash generation.
    @return: Hash
    '''
    absPath = absolutePath(filepath)
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha224 = hashlib.sha224()
    sha3_224 = hashlib.sha3_224()
    sha256 = hashlib.sha256()
    sha3_256 = hashlib.sha3_256()
    sha384 = hashlib.sha384()
    sha3_384 = hashlib.sha3_384()
    sha512 = hashlib.sha512()
    sha3_512 =  hashlib.sha3_512() 
    blake2b = hashlib.blake2b()
    blake2s = hashlib.blake2s()
    with open(absPath, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            md5.update(data)
            sha1.update(data)
            sha224.update(data)
            sha3_224.update(data)
            sha256.update(data)
            sha3_256.update(data)
            sha384.update(data)
            sha3_384.update(data)
            sha512.update(data)
            sha3_512.update(data)
            blake2b.update(data)
            blake2s.update(data)
    x = [md5.hexdigest(),
         sha1.hexdigest(), 
         sha224.hexdigest(),
         sha3_224.hexdigest(),
         sha256.hexdigest(), 
         sha3_256.hexdigest(),
         sha384.hexdigest(),
         sha3_384.hexdigest(), 
         sha512.hexdigest(), 
         sha3_512.hexdigest(), 
         blake2b.hexdigest(), 
         blake2s.hexdigest()]
    return ':'.join(x)

def logFile(sdb_object, filepath, description='NA'):
    '''!
    Function to logging a file into SEREBO database.

    A dictionary of items generated will be returned with the 
    following keys: (1) DateTimeStamp is the UTC date time stamp 
    of this event, (2) Data is the given data string to be 
    inserted, (3) UserDescription is the user given explanation 
    string for this event, (4) DataHash is the hash string of Data, 
    (5) ParentBlockID is the ID of the parent block in blockchain, (6) 
    ParentDateTimeStamp is the UTC date time stamp of the parent 
    block in blockchain (which is also the parent insertion 
    event), (7) ParentRandomString is the random string generated 
    in parent block in blockchain, (8) ParentHash is the hash of 
    parent block in blockchain, (9) BlockRandomString is the 
    random string generated for current insertion event, and (10) 
    BlockHash is the block hash of current insertion event in 
    blockchain.

    @param sdb_object Object: SEREBO database object.
    @param fileapth String: Path of file to log in SEREBO black box.
    @param description String: Explanation string for this entry 
    event. Default = NA.
    @return: Dictionary of data generated from this event.
    '''
    absPath = absolutePath(filepath)
    if description == 'NA':
        description = ['UserGivenPath:>%s' % str(filepath),
                       'AbsolutePath:>%s' % str(absPath)]
    else:
        description = ['UserGivenPath :> %s' % str(filepath),
                       'AbsolutePath :> %s' % str(absPath),
                       'UserDescription :> %s' % str(description)]
    description = ' >> '.join(description)
    fHash = fileHash(absPath)
    rdata = sdb_object.insertData(fHash, description, 'file')
    return rdata

def searchDatalog(sdb_object, term, field, mode='like'):
    '''!
    Function to search datalog table.

    @param sdb_object Object: SEREBO database object.
    @param term String: Case sensitive search term.
    @param field String: Field name to search.
    @param mode String: Mode of search. Allowable modes are 'like' and 
    'exact'. If mode is 'like', wildcards such as '_' (matches any 
    single character) and '%' (matches any number of characters). 
    Default = 'like'.
    @return: List of datalog rows: [ID, dtstamp, hash, data, 
    description]
    '''
    term = str(term)
    field = str(field)
    if mode.lower() == 'exact':
        sqlstmt = """select ID, dtstamp, hash, data, description from datalog where %s='%s'""" % (field, term)
    if mode.lower() == 'like':
        sqlstmt = """select ID, dtstamp, hash, data, description from datalog where %s like '%s'""" % (field, term)
    result = [row for row in sdb_object.cur.execute(sqlstmt)]
    return result

def dateTime(sdb_object):
    '''!
    Function to get a date time string.

    @param sdb_object Object: SEREBO database object.
    @return: Date time string
    '''
    return sdb_object.dtStamp()

def randomString(sdb_object, length):
    '''!
    Function to get a random string.

    @param sdb_object Object: SEREBO database object.
    @param length Integer: Length of random string to generate.
    @return: Random string
    '''
    length = int(length)
    return sdb_object.randomString(length)

def stringHash(sdb_object, dstring):
    '''!
    Function to generate hash for a data string.

    @param dstring String: Data string for hash generation.
    @param sdb_object Object: SEREBO database object.
    @return: Hash
    '''
    return sdb_object.hash(str(dstring))

def gmtime(seconds_since_epoch):
    '''!
    Function to generate a UTC date time stamp string in the format 
    of <year>:<month>:<day>:<hour>:<minute>:<second>:<microsecond> 
    from seconds since epoch. However, microseconds cannot be 
    converted; hence, it is given as 00000.

    @param seconds_since_epoch Float: Seconds since epoch.
    @return: UTC date time stamp string
    '''
    seconds_since_epoch = float(seconds_since_epoch)
    now = time.gmtime(seconds_since_epoch)
    now = [str(now.tm_year), str(now.tm_mon),
           str(now.tm_mday), str(now.tm_hour),
           str(now.tm_min), str(now.tm_sec),
           '00000']
    return ':'.join(now)

def backup(bbpath, backuppath):
    '''!
    Function to backup SEREBO Black Box.

    @param backuppath String: Path for backed-up SEREBO black box. 
    @param bbpath String: Path to SEREBO black box.
    @return: (absolute bbpath, absolute backuppath)
    '''
    import shutil
    bbpath = absolutePath(bbpath)
    backuppath = absolutePath(backuppath)
    db = connectDB(bbpath)
    db.cur.execute('begin immediate')
    shutil.copyfile(bbpath, backuppath)
    db.conn.rollback()
    return (str(bbpath), str(backuppath))
