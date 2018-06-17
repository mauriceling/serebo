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
    db = SereboDB()
    return db


