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
    '''
    '''
    def __init__(self):
        path = os.sep.join(['blackbox', 'blackbox.sdb'])
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()
        self._createTables()

    def dtStamp(self):
        now = datetime.utcnow()
        now = [str(now.year), str(now.month),
               str(now.day), str(now.hour),
               str(now.minute), str(now.second),
               str(now.microsecond)]
        now = ':'.join(now)
        return now

    def randomString(self, length=64):
        choices = string.ascii_letters + string.digits + '!@#$%&<>=[]?'
        x = random.choices(choices, k=length)
        return ''.join(x)

    def hash(self, data):
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
        now = self.dtStamp()
        # Metadata table
        sql_metadata_create = '''
        create table if not exists metadata (
            key text primary key,
            value text not null);'''
        sql_metadata_insert1 = '''
        insert into metadata (key, value) values ('creation_timestamp', '%s');
        ''' % (now)
        sql_metadata_insert2 = '''
        insert into metadata (key, value) values ('blackboxID', '%s');
        ''' % (self.randomString(512))
        # Data log table
        sql_datalog_create = '''
        create table if not exists datalog (
            ID integer primary key autoincrement,
            dtstamp text not null,
            hash text not null,
            data blob);'''
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
            fID text not null,
            key text not null,
            value text not null);'''
        # SQL execution
        sqlstmt = [sql_metadata_create, 
                   sql_metadata_insert1,
                   sql_metadata_insert2,
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
