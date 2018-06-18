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
from datetime import datetime
import hashlib
import random
import os
import secrets
import sqlite3
import string

class SereboDB(object):
    '''!
    Class representing SEREBO database - the recorder black box.
    '''
    def __init__(self):
        '''!
        Initiation method - connects to SEREBO database. If SEREBO 
        database does not exist, this function will create the 
        database with the necessary data tables.
        '''
        path = os.sep.join(['serebo_blackbox', 'blackbox.sdb'])
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()
        self._createTables()

    def dtStamp(self):
        '''!
        Method to generate a UTC date time stamp string in the format 
        of <year>:<month>:<day>:<hour>:<minute>:<second>:<microsecond>

        @return: UTC date time stamp string
        '''
        now = datetime.utcnow()
        now = [str(now.year), str(now.month),
               str(now.day), str(now.hour),
               str(now.minute), str(now.second),
               str(now.microsecond)]
        now = ':'.join(now)
        return now

    def randomString(self, length=64):
        '''!
        Method to generate a random string, which can contain 80 
        possible characters - abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNO
        PQRSTUVWXYZ0123456789~!@#$%^&*()<>=+[]?. Hence, the possible 
        number of strings is 80**length.

        @param length Integer: Length of random string to generate. 
        Default = 64.
        @return: Random string
        '''
        choices = string.ascii_letters + \
                  string.digits + \
                  '~!@#$%^&*()<>=+[]?'
        x = random.choices(choices, k=int(length))
        return ''.join(x)

    def hash(self, data):
        '''!
        Method to generate a series of 12 hashes for a given data 
        string, in the format of <MD5>:<SHA1>:<SHA224>:<SHA3 
        244>:<SHA256>:<SHA3 256>:<SHA384>:<SHA3 384>:<SHA512>:<SHA3 
        215>:<Blake 2b>:<Blake 2s>.

        @param data String: Data string to generate hash.
        @return: Hash
        '''
        data = str(data)
        data = bytes(data, 'utf-8')
        x = [hashlib.md5(data).hexdigest(),
             hashlib.sha1(data).hexdigest(), 
             hashlib.sha224(data).hexdigest(),
             hashlib.sha3_224(data).hexdigest(),
             hashlib.sha256(data).hexdigest(), 
             hashlib.sha3_256(data).hexdigest(),
             hashlib.sha384(data).hexdigest(),
             hashlib.sha3_384(data).hexdigest(), 
             hashlib.sha512(data).hexdigest(), 
             hashlib.sha3_512(data).hexdigest(), 
             hashlib.blake2b(data).hexdigest(), 
             hashlib.blake2s(data).hexdigest()]
        return ':'.join(x)

    def _createTables(self):
        '''!
        Private method - used by initialization method to generate 
        data tables. 
        '''
        now = self.dtStamp()
        # Metadata table
        sql_metadata_create = '''
        create table if not exists metadata (
            key text primary key,
            value text not null);'''
        sql_metadata_insert1 = '''
        insert into metadata (key, value) values 
            ('creation_timestamp', '%s');''' % (now)
        sql_metadata_insert2 = '''
        insert into metadata (key, value) values ('blackboxID', '%s');''' % (self.randomString(512))
        # System data table
        sql_systemdata_create = '''
        create table if not exists systemdata (
            ID integer primary key autoincrement,
            dtstamp text not null,
            key text not null,
            value text not null);'''
        # Data log table
        sql_datalog_create = '''
        create table if not exists datalog (
            ID integer primary key autoincrement,
            dtstamp text not null,
            hash text not null,
            data blob,
            description not null);'''
        sql_datalog_unique = '''
        create unique index if not exists datalog_unique on datalog (
            dtstamp, hash);'''
        # Blockchain table
        sql_blockchain_create = '''
        create table if not exists blockchain (
            c_ID integer primary key autoincrement,
            c_dtstamp text not null,
            c_randomstring text not null,
            c_hash text not null,
            p_ID integer not null,
            p_dtstamp text not null,
            p_randomstring text not null,
            p_hash text not null,
            data text not null);'''
        # Event log table
        sql_eventlog_create1 = '''
        create table if not exists eventlog (
            ID integer primary key autoincrement,
            dtstamp text not null,
            fID text not null,
            description text not null);'''
        sql_eventlog_create2 = '''
        create table if not exists eventlog_datamap (
            dtstamp text not null,
            fID text not null,
            key text not null,
            value text not null);'''
        # SQL execution
        sqlstmt = [sql_metadata_create, 
                   sql_metadata_insert1,
                   sql_metadata_insert2,
                   sql_systemdata_create,
                   sql_datalog_create,
                   sql_datalog_unique,
                   sql_blockchain_create,
                   sql_eventlog_create1,
                   sql_eventlog_create2]
        for statement in sqlstmt:
            try:
                self.cur.execute(statement)
                self.conn.commit()
            except sqlite3.IntegrityError:
                pass

    def _insertData1(self, data, description, debug):
        '''!
        Private method - Step 1 of insert data into CEREBO black box. 
        Called by insertData method. Step 1 (1) gets a UTC date time 
        stamp; (2) formats the description by suffixing the 
        description with a 10-character random string (80**10 = 1e19 
        possibility); and (3) generates a hash using the UTC date time 
        stamp, data and formatted description. 
        '''
        dtstamp = self.dtStamp()
        DL_data = str(data)
        if description == 'NA' or description == None:
            description = 'NA:' + self.randomString(10)
        else:
            description = str(description) + ':' + \
                          self.randomString(10)
        DL_hash = self.hash(bytes(dtstamp, 'utf-8') + \
                            bytes(DL_data, 'utf-8') + \
                            bytes(description, 'utf-8'))
        return (dtstamp, DL_data, description, DL_hash)

    def _insertFile1(self, data, description, debug):
        '''!
        Private method - Step 1 of insert data into CEREBO black box. 
        Called by insertData method. Step 1 (1) gets a UTC date time 
        stamp; and (2) generates a hash using the UTC date time stamp, 
        data and description containing the absolute and relative path 
        to the file. 
        '''
        dtstamp = self.dtStamp()
        DL_data = str(data)
        description = str(description)
        DL_hash = self.hash(bytes(dtstamp, 'utf-8') + \
                            bytes(DL_data, 'utf-8') + \
                            bytes(description, 'utf-8'))
        return (dtstamp, DL_data, description, DL_hash)

    def _insertData2(self, dtstamp, DL_data, description, 
                     DL_hash, debug):
        '''!
        Private method - Step 2 of insert data into CEREBO black box. 
        Called by insertData method. Step 2 inserts the results from 
        Step 1 into datalog table.
        '''
        sqlstmt = '''insert into datalog (dtstamp, hash, data, 
            description) values (?,?,?,?)'''
        sqldata = (str(dtstamp), str(DL_hash), str(DL_data), 
                   str(description))
        self.cur.execute(sqlstmt, sqldata)
        if debug:
            print('Step 1&2: Inserted Data into Data Log ...')
            print('Date Time Stamp: %s' % dtstamp)
            print('Inserted Data: %s' % data)
            print('Generated Hash: %s' % DL_hash)

    def _insertData3(self, debug):
        '''!
        Private method - Step 3 of insert data into CEREBO black box. 
        Called by insertData method. Step 3 gets data (ID, dtstamp, 
        randomstring, and hash) the latest pre-existing block in 
        blockchain table, to be used as parent in the next block.
        '''
        sqlstmt = '''select max(c_ID) from blockchain'''
        max_cID = [row for row in self.cur.execute(sqlstmt)][0][0]
        if max_cID == None:
            p_ID = 0 
            p_dtstamp = '0'
            p_randomstring = 'GenesisBlock:SEREBO_MauriceHTLing'
            p_hash = 'TheWord:OmAhHum'
        else:
            sqlstmt = '''select c_ID, c_dtstamp, c_randomstring, 
                c_hash from blockchain where c_ID = %s''' % \
                str(max_cID)
            data3 = [row for row in self.cur.execute(sqlstmt)]
            p_ID = data3[0][0]
            p_dtstamp = data3[0][1]
            p_randomstring = data3[0][2]
            p_hash = data3[0][3]
        if debug:
            print('Step 3: Getting Latest Block from Blockchain ...')
            print('Parent ID: %s' % p_ID)
            print('Parent Date Time Stamp: %s' % p_dtstamp)
            print('Parent Random String: %s' % p_randomstring)
            print('Parent Hash: %s' % p_hash)
        return (p_ID, p_dtstamp, p_randomstring, p_hash)

    def _insertData4(self, p_dtstamp, p_randomstring, p_hash, DL_hash):
        '''!
        Private method - Step 4 of insert data into CEREBO black box. 
        Called by insertData method. Step 4 (1) generates a hash from 
        the parent date time stamp, parent random string, parent hash, 
        and current data hash (from Step 1) as current block hash; (2) 
        and generates a 32-character random string (80**32 = 8e60 
        possibilities) for the current block.
        '''
        BC_rstr = self.randomString(32)
        hashdata = ''.join([str(p_dtstamp), str(p_randomstring),
                            str(p_hash), str(DL_hash)])
        BC_hash = self.hash(bytes(hashdata, 'utf-8'))
        return (BC_rstr, BC_hash)

    def _insertData5(self, dtstamp, BC_rstr, BC_hash, p_ID,
                   p_dtstamp, p_randomstring, p_hash, 
                   DL_hash, debug):
        '''!
        Private method - Step 5 of insert data into CEREBO black box. 
        Called by insertData method. Step 5 inserts data of the 
        current block into blockchain table.  
        '''
        sqldata = (str(dtstamp), str(BC_rstr), str(BC_hash), str(p_ID),
                   str(p_dtstamp), str(p_randomstring), str(p_hash), 
                   str(DL_hash))
        sqlstmt = '''insert into blockchain (c_dtstamp, 
            c_randomstring, c_hash, p_ID, p_dtstamp, p_randomstring, 
            p_hash, data) values (?,?,?,?,?,?,?,?)'''
        self.cur.execute(sqlstmt, sqldata)
        if debug:
            print('Step 5: Insert Data into Blockchain (New Block) ...')
            print('Random String: %s' % BC_rstr)
            print('New Block Hash: %s' % BC_hash)
            print('')

    def _insertData6(self, dtstamp, description, 
                     DL_hash, p_hash, BC_hash):
        '''!
        Private method - Step 6 of insert data into CEREBO black box. 
        Called by insertData method. Step 6 records the current data 
        insertion event into eventlog tables by recording the date 
        time stamp, parent block hash, data hash, and current block 
        hash.
        '''
        fID = self.randomString(10)
        sqlstmt = '''insert into eventlog (dtstamp, fID, description) 
        values (?,?,?)'''
        sqldata = (str(dtstamp), str(fID), str(description))
        self.cur.execute(sqlstmt, sqldata)
        sqlstmt = '''insert into eventlog_datamap (dtstamp, fID, key, 
            value) values (?,?,?,?)'''
        sqldata = [(str(dtstamp), str(fID), 'DataHash', str(DL_hash)),
                   (str(dtstamp), str(fID), 'ParentHash', str(p_hash)),
                   (str(dtstamp), str(fID), 'BlockHash', str(BC_hash))]
        self.cur.executemany(sqlstmt, sqldata)

    def insertData(self, data, description='NA', mode='text', 
                   debug=False):
        '''!
        Method to insert data into SEREBO database. Data will be 
        recorded in datalog table together with the hash of the data. 
        The hash of the data will be logged into blockchain table. 
        This data insertion event will be logged into eventlog tables.
        
        A dictionary of items generated will be returned with the 
        following keys: (1) DateTimeStamp is the UTC date time stamp 
        of this event, (2) Data is the given data string to be 
        inserted, (3) UserDescription is the user given explanation 
        string for this event suffixed with a 64-character random 
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

        @param data String: Data to be inserted.
        @param description String: Explanation string for this entry 
        event. Default = NA.
        @param mode String: Type of data to insert. Allowable modes 
        are 'text' and 'file'. Default = 'text'.
        @param debug Boolean: Flag to print out debugging statements.
        @return: Dictionary of data generated from this event.
        '''
        # Step 1: Preparing data
        if mode.lower() == 'text':
            (dtstamp, DL_data, description, DL_hash) = \
                self._insertData1(data, description, debug)
        elif mode.lower() == 'file':
            (dtstamp, DL_data, description, DL_hash) = \
                self._insertFile1(data, description, debug)
        # Step 2: Insert data into datalog
        self._insertData2(dtstamp, DL_data, description, 
                          DL_hash, debug)
        # Step 3: Get latest block in blockchain
        (p_ID, p_dtstamp, p_randomstring, p_hash) = \
            self._insertData3(debug)
        # Step 4: Prepare data for blockchain insertion
        (BC_rstr, BC_hash) = self._insertData4(p_dtstamp, 
                                               p_randomstring, 
                                               p_hash, 
                                               DL_hash)
        # Step 5: Insert data into blockchain
        self._insertData5(dtstamp, BC_rstr, BC_hash, p_ID,
                          p_dtstamp, p_randomstring, p_hash, 
                          DL_hash, debug)
        # Step 6: Insert event into eventlog
        self._insertData6(dtstamp, description, 
                          DL_hash, p_hash, BC_hash)
        # Step 7: Commit 
        self.conn.commit()
        # Step 8: Return data
        return {'DateTimeStamp': dtstamp,
                'Data': data,
                'UserDescription': description,
                'DataHash': DL_hash,
                'ParentBlockID': p_ID,
                'ParentDateTimeStamp': p_dtstamp,
                'ParentRandomString': p_randomstring,
                'ParentHash': p_hash,
                'BlockRandomString': BC_rstr,
                'BlockHash': BC_hash}
