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
import hashlib as h
import random
import string

from gluon.tools import Service

service = Service()

def call():
    '''!
    Function to enable web services in Web2Py.
    '''
    session.forget()
    return service()

@service.xmlrpc
def now():
    '''!
    Function to generate a UTC date time stamp string in the format 
    of <year>:<month>:<day>:<hour>:<minute>:<second>:<microsecond>

    @return: UTC date time stamp string
    '''
    dt = datetime.utcnow()
    x = [str(dt.year), str(dt.month),
         str(dt.day), str(dt.hour),
         str(dt.minute), str(dt.second),
         str(dt.microsecond)]
    return ':'.join(x)

@service.xmlrpc
def randomString(length=16):
    '''!
    Function to generate a random string, which can contain 80 
    possible characters - abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNO
    PQRSTUVWXYZ0123456789~!@#$%^&*()<>=+[]?. Hence, the possible 
    number of strings is 80**length.

    @param length Integer: Length of random string to generate. 
    Default = 16.
    @return: Random string
    '''
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
    '''!
    Function to register SEREBO Black Box with SEREBO Notary.

    @param blackboxID String: ID of SEREBO black box - found in 
    metadata table in SEREBO black box database.
    @param owner String: Owner's or administrator's name.
    @param email String: Owner's or administrator's email.
    @param architecture String: Architecture of machine - from 
    platform library in Python Standard Library.
    @param machine String: Machine description - from platform 
    library in Python Standard Library.
    @param node String: Machine's node description - from 
    platform library in Python Standard Library.
    @param platform String: Platform description - from platform 
    library in Python Standard Library.
    @param processor String: Machine's processor description - from 
    platform library in Python Standard Library.
    @returns: (Notary authorization code, Date time stamp from 
    SEREBO Notary)
    '''
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
    eventText = ['SEREBO Black Box Registration',
                 'Date Time Stamp: %s' % dtstamp,
                 'Black Box ID: %s' % blackboxID,
                 'Owner: %s' % owner,
                 'Email: %s' % email,
                 'Notary Authorization: %s' % notaryAuthorization]
    eventText = ' | '.join(eventText)
    notabase.eventlog.insert(datetimestamp=dtstamp,
                             event=eventText)
    return (notaryAuthorization, dtstamp)

@service.xmlrpc
def hash(dstring):
    '''!
    Function to generate a series of 6 hashes for a given data 
    string, in the format of <MD5>:<SHA1>:<SHA224>:<SHA256>:
    <SHA384>:<SHA512>.

    @param dstring String: String to generate hash.
    @return: Hash
    '''
    dstring = str(dstring)
    x = [h.md5(dstring).hexdigest(),
         h.sha1(dstring).hexdigest(), 
         h.sha224(dstring).hexdigest(),
         h.sha256(dstring).hexdigest(), 
         h.sha384(dstring).hexdigest(),
         h.sha512(dstring).hexdigest()]
    return ':'.join(x)
    
@service.xmlrpc
def checkBlackBoxRegistration(blackboxID, notaryAuthorization):
    '''!
    Function to check for SEREBO Black Box registration.
    
    @param blackboxID String: ID of SEREBO black box - found in 
    metadata table in SEREBO black box database.
    @param notaryAuthorization String: Notary authorization code 
    of SEREBO black box (generated during black box registration 
    - found in metadata table in SEREBO black box database.
    @return: True is SEREBO Black Box is registered; False if SEREBO 
    Black Box is not registered
    '''
    if notabase(notabase.notarize_blackbox.blackboxID == blackboxID) \
        (notabase.notarize_blackbox.notaryAuthorization == notaryAuthorization).count():
        return True
    else:
        return False
    
@service.xmlrpc
def notarizeSereboBB(blackboxID, notaryAuthorization, 
                     dtstampBB, codeBB):
    '''!
    Function to notarize SEREBO Black Box with SEREBO Notary.

    @param blackboxID String: ID of SEREBO black box - found in 
    metadata table in SEREBO black box database.
    @param notaryAuthorization String: Notary authorization code 
    of SEREBO black box (generated during black box registration 
    - found in metadata table in SEREBO black box database.
    @param dtstampBB String: Date time stamp from SEREBO black box.
    @param codeBB String: Notarization code from SEREBO black box.
    @returns: (Date time stamp from SEREBO Notary, Notarization code 
    from SEREBO Notary, Cross-Signing code from SEREBO Notary)
    '''
    blackboxID = str(blackboxID)
    notaryAuthorization = str(notaryAuthorization)
    dtstampBB = str(dtstampBB)
    codeBB = str(codeBB)
    dtstampNS = now()
    if not checkBlackBoxRegistration(blackboxID, 
                                     notaryAuthorization):
        eventText = ['SEREBO Black Box Notarization',
                     'Failed - Registration not found',
                     'Date Time Stamp: %s' % dtstampNS,
                     'Black Box ID: %s' % blackboxID,
                     'Notary Authorization: %s' % notaryAuthorization]
        eventText = ' | '.join(eventText)
        notabase.eventlog.insert(datetimestamp=dtstampNS,
                                 event=eventText)
        return ('not registered', 
                'not registered', 
                'not registered')
    codeNS = str(randomString(32))
    codeCommon = hash(codeBB + codeNS)
    notabase.notarize_blackbox.insert(blackboxID=blackboxID,
                                      notaryAuthorization=notaryAuthorization,
                                      dtstampBB=dtstampBB,
                                      dtstampNS=dtstampNS,
                                      codeBB=codeBB,
                                      codeNS=codeNS,
                                      codeCommon=codeCommon)
    eventText = ['SEREBO Black Box Notarization',
                 'Success',
                 'Date Time Stamp: %s' % dtstampNS,
                 'Black Box ID: %s' % blackboxID,
                 'Notary Authorization: %s' % notaryAuthorization,
                 'Black Box Code: %s' % codeBB,
                 'Notary Code: %s' % codeNS,
                 'Cross-Signing Code: %s' % codeCommon]
    eventText = ' | '.join(eventText)
    notabase.eventlog.insert(datetimestamp=dtstampNS,
                             event=eventText)
    return (dtstampNS, codeNS, codeCommon)
