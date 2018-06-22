'''!
Secured Recorder Box (SEREBO) Black Box

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

# Metadata
__version__ = '1.0'
__author__ = 'Maurice H.T. Ling <mauriceling@acm.org>'
__maintainer__ = 'Maurice H.T. Ling <mauriceling@acm.org>'
__email__ = 'mauriceling@acm.org'
__copyright__ = '(c) 2018-%s, Maurice H.T. Ling.' % (datetime.now().year)
__description__ = '''
SEREBO (SEcured REcorder BOx) Black Box is inspired by the black boxes (cockpit voice recorder and flight data recorder) in airliners. The intended purpose is to track and audit research records under the following premise - Given a set of data files, is there a system to log and verify that these files had not been changed or edited since its supposed creation?

SEREBO Black Box aims to address this issue using several approaches. Firstly, the data files can be used to generate a file hash. It is very likely that an edit in the file will result in a different hash. Hence, if a file generates the same hash across two different points in time, it can be safely assumed that the file had not been edited during this time span. Secondly, the file hash has to be securely recorded with amendment protected. SEREBO records the hash and registers the hash into a blockchain. The main concept of blockchain is that the hash of previous (parent) block is concatenated with the data (file hash in this case) of the current block to generate a hash for the current block. Hence, as the blockchain grows, any amendments in earlier blocks can be easily detected - only amendments to the latest block cannot be detected. Therefore, the value of SEREBO lies in its use.'''

from . import ntplib
from . import serebo_api
from .serebo_api import absolutePath
from .serebo_api import backup
from .serebo_api import connectDB
from .serebo_api import dateTime
from .serebo_api import fileHash
from .serebo_api import gmtime
from .serebo_api import insertFText
from .serebo_api import insertText
from .serebo_api import logFile
from .serebo_api import randomString
from .serebo_api import searchDatalog
from .serebo_api import stringHash
from .serebo_api import systemData
