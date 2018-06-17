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
        choices = string.ascii_letters + string.digits
        x = random.choices(choices, k=length)
        return ''.join(x)

    def _createTables(self):
        now = self.dtStamp()
        # Metadata table
        sql_metadata_create = '''
        create table if not exists metadata (
            key text not null,
            value text not null);'''
        sql_metadata_insert1 = '''
        insert into metadata values ('creation_timestamp', '%s');
        ''' % (now)
        sql_metadata_insert2 = '''
        insert into metadata values ('blackboxID', '%s');
        ''' % (self.randomString(1024))
        sqlstmt = [sql_metadata_create, 
                   sql_metadata_insert1,
                   sql_metadata_insert2]
        for statement in sqlstmt:
            self.cur.execute(statement)
            self.conn.commit()
