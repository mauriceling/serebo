# -*- coding: utf-8 -*-
'''!
Secured Recorder Box (SEREBO) Notary Services

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

from datetime import datetime
import random
import string

from gluon.tools import Service

service = Service()

def call():
    session.forget()
    return service()

@service.xmlrpc
def now():
    dt = datetime.utcnow()
    x = [str(dt.year), str(dt.month),
         str(dt.day), str(dt.hour),
         str(dt.minute), str(dt.second),
         str(dt.microsecond)]
    return ':'.join(x)

@service.xmlrpc
def randomString(length=16):
    choices = string.ascii_letters + \
              string.digits + \
              '~!@#$%^&*()<>=+[]?'
    x = [random.choice(choices) 
         for i in range(int(length))]
    return ''.join(x)

@service.xmlrpc
def register_blackbox(blackboxID, owner, email, 
             architecture, machine, node, 
             platform, processor):
    dtstamp = now()
    notaryAuthorization = str(randomString(256))
    notabase.registered_blackbox.insert(datetimestamp=dtstamp,
                                        blackboxID=str(blackboxID), 
                                        owner=str(owner), 
                                        email=str(email), 
                                        architecture=str(architecture), 
                                        machine=str(machine), 
                                        node=str(node), 
                                        platform=str(platform), 
                                        processor=str(processor), 
                                        notaryAuthorization=notaryAuthorization)
    return (notaryAuthorization, dtstamp)
