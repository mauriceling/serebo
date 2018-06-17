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
'''

from . import serebo_api
from .serebo_api import connectDB
