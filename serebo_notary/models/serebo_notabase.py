# -*- coding: utf-8 -*-
'''!
Secured Recorder Box (SEREBO) Notary Database

Date created: 19th May 2018

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

notabase = SQLDB('sqlite://serebo_notabase.sqlite')

'''
Table registered_blackbox is to store registration data 
of SEREBO Black Box.
'''
notabase.define_table('registered_blackbox',
    SQLField('datetimestamp', 'text'),
    SQLField('blackboxID', 'text', unique=True),
    SQLField('owner', 'text'),
    SQLField('email', 'text'),
    SQLField('architecture', 'text'),
    SQLField('machine', 'text'),
    SQLField('node', 'text'),
    SQLField('platform', 'text'),
    SQLField('processor', 'text'),
    SQLField('notaryAuthorization', 'text'))
