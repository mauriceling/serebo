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
import random
import secrets

from . import sereboDB
from .sereboDB import SereboDB

def connectDB():
    '''!
    Function to connect to SEREBO database - the recorder box.

    @return: SEREBO database object
    '''
    db = SereboDB()
    return db

def insertText(sdb_object, text, description='NA'):
    '''!
    Function to insert text string into SEREBO database.

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

    @param sdb_object Object: SEREBO database object.
    @param text String: Text string to be inserted.
    @param description String: Explanation string for this entry 
    event. Default = NA.
    @return: Dictionary of data generated from this event.
    '''
    rdata = sdb_object.insertData(data, description)
    return rdata
