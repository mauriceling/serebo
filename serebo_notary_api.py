'''!
Secured Recorder Box (SEREBO) Notary Communicator

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

from xmlrpc.client import ServerProxy

def registerBlackbox(blackboxID, owner, email, 
                     architecture, machine, node, 
                     platform, processor, 
                     notaryURL='https://mauricelab.pythonanywhere.com/serebo_notary/services/call/xmlrpc'):
    '''!
    Function to communicate with SEREBO Notary to register SEREBO 
    Black Box with SEREBO Notary.

    @param blackboxID String: ID of SEREBO black box - found in 
    metadata table in SEREBO black box database.
    @param owner String: Owner's or administrator's name.
    @param email String: Owner's or administrator's email.
    @param architecture String: Architecture of this machine - from 
    platform library in Python Standard Library.
    @param machine String: This machine description - from platform 
    library in Python Standard Library.
    @param node String: This machine's node description - from 
    platform library in Python Standard Library.
    @param platform String: This platform description - from platform 
    library in Python Standard Library.
    @param processor String: Machine's processor description - from 
    platform library in Python Standard Library
    @param notaryURL String: URL for SEREBO Notary web service. 
    Default="https://mauricelab.pythonanywhere.com/serebo_notary/services/call/xmlrpc"
    @returns: (URL of SEREBO Notary, Notary authorization code, Date 
    time stamp from SEREBO Notary)
    '''
    serv = ServerProxy(notaryURL)
    (notaryAuthorization, dtstamp) = \
        serv.register_blackbox(blackboxID, owner, email, 
                               architecture, machine, node, 
                               platform, processor)
    return (notaryURL, str(notaryAuthorization), str(dtstamp))

def notarizeBB(blackboxID, notaryAuthorization, dtstampBB, codeBB,
              notaryURL='https://mauricelab.pythonanywhere.com/serebo_notary/services/call/xmlrpc'):
    '''!
    Function to communicate with SEREBO Notary to notarize SEREBO 
    Black Box with SEREBO Notary.

    @param blackboxID String: ID of SEREBO black box - found in 
    metadata table in SEREBO black box database.
    @param notaryAuthorization String: Notary authorization code of 
    SEREBO black box (generated during black box registration - found 
    in metadata table in SEREBO black box database.
    @param dtstampBB String: Date time stamp from SEREBO black box.
    @param codeBB String: Notarization code from SEREBO black box.
    @param notaryURL String: URL for SEREBO Notary web service. 
    Default="https://mauricelab.pythonanywhere.com/serebo_notary/services/call/xmlrpc"
    @returns: (URL of SEREBO Notary, Date time stamp from SEREBO 
    Notary, Notarization code from SEREBO Notary, Cross-Signing code 
    from SEREBO Notary)
    '''
    serv = ServerProxy(notaryURL)
    (dtstampNS, codeNS, codeCommon) = \
        serv.notarizeSereboBB(blackboxID, notaryAuthorization, 
                              dtstampBB, codeBB)
    return (notaryURL, str(dtstampNS), str(codeNS), str(codeCommon))

def checkRegistration(blackboxID, notaryAuthorization, 
                      notaryURL='https://mauricelab.pythonanywhere.com/serebo_notary/services/call/xmlrpc'):
    '''!

    @param blackboxID String: ID of SEREBO black box - found in 
    metadata table in SEREBO black box database.
    @param notaryAuthorization String: Notary authorization code of 
    SEREBO black box (generated during black box registration - found 
    in metadata table in SEREBO black box database.
    @param notaryURL String: URL for SEREBO Notary web service. 
    Default="https://mauricelab.pythonanywhere.com/serebo_notary/services/call/xmlrpc"
    @returns: Boolean flag - True if SEREBO black box registration 
    is found in SEREBO Notary. False if SEREBO black box registration 
    is not found in SEREBO Notary.
    '''
    serv = ServerProxy(notaryURL)
    value = serv.checkBlackBoxRegistration(blackboxID, 
                                           notaryAuthorization)
    if value or value == 'True':
        return True
    elif not value or value == 'False':
        return False
