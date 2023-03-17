"""!
Secured Recorder Box (SEREBO) Command Line Interface (CLI)

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
"""
import argparse
import random
import os
import sqlite3

import serebo_blackbox as bb
import serebo_notary_api as notary


def initialize(bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to initialize SEREBO blackbox.

    Usage:

        python serebo.py init --bbpath=<path to SEREBO black box>

    For example:

        python serebo.py init --bbpath="serebo_blackbox\\blackbox.sdb"

    @param bbpath String: Path to SEREBO black box. Default = 
    "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    try:
        sqlstmt = """insert into metadata (key, value) values ("serebo_blackbox_path", "%s");""" % (str(db.path))
        db.cur.execute(sqlstmt)
        db.conn.commit()
    except sqlite3.IntegrityError: pass
    print("")
    rdat = {"SEREBO Black Box": db,
            "Black Box Path": str(db.path)}
    return rdat

def insertText(message, description="NA", 
               bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to insert a text string into SEREBO blackbox.

    Usage:

        python serebo.py intext --message=<text message to be inserted> --description=<explanatory description for this insertion> --bbpath=<path to SEREBO black box>

    For example:

        python serebo.py intext --message="This is a text message for insertion" --description="Texting 1" --bbpath="serebo_blackbox\\blackbox.sdb"

    @param message String: Text string to be inserted.
    @param description String: Explanation string for this entry 
    event. Default = NA.
    @param bbpath String: Path to SEREBO black box. Default = 
    "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    rdata = bb.insertText(db, message, description)
    print("")
    print("Insert Text Status ...")
    rdat = {"SEREBO Black Box": db,
            "Black Box Path": str(db.path),
            "Date Time Stamp": str(rdata["DateTimeStamp"]),
            "Message": str(rdata["Data"]),
            "Description": str(rdata["UserDescription"]),
            "Data Hash": str(rdata["DataHash"])}
    return rdat

def logFile(filepath, description="NA",
            bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to log a file into SEREBO blackbox.

    Usage:

        python serebo.py logfile --filepath=<path of file to log> --description=<explanatory description for this insertion> --bbpath=<path to SEREBO black box>

    For example:

        python serebo.py logfile --filepath=doxygen_serebo  --description="Doxygen file for SEREBO" --bbpath="serebo_blackbox\\blackbox.sdb"

    @param fileapth String: Path of file to log in SEREBO black box.
    @param description String: Explanation string for this entry 
    event. Default = NA.
    @param bbpath String: Path to SEREBO black box. Default = 
    "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    rdata = bb.logFile(db, filepath, description)
    print("")
    print("File Logging Status ...")
    rdat = {"SEREBO Black Box": db,
            "Black Box Path": str(db.path),
            "Date Time Stamp": str(rdata["DateTimeStamp"]),
            "File Hash": str(rdata["Data"]),
            "Description": str(rdata["UserDescription"]),
            "Data Hash": str(rdata["DataHash"])}
    return rdat

def systemData():
    
    """!
    Function to print out data and test hashes of current platform - 
    This does not insert a record into SEREBO Black Box.

    Usage:

        python serebo.py sysdata
    """
    data = bb.systemData()
    print("")
    print("System Data ...")
    rdat = {"architecture": str(data["architecture"]),
            "machine": str(data["machine"]),
            "node": str(data["node"]),
            "platform": str(data["platform"]),
            "processor": str(data["processor"]),
            "python_build": str(data["python_build"]),
            "python_compiler": str(data["python_compiler"]),
            "python_implementation": str(data["python_implementation"]),
            "python_branch": str(data["python_branch"]),
            "python_revision": str(data["python_revision"]),
            "python_version": str(data["python_version"]),
            "release": str(data["release"]),
            "system": str(data["system"]),
            "version": str(data["version"]),
            "hashdata": str(data["hashdata"]),
            "hash_md5": str(data["hash_md5"]),
            "hash_sha1": str(data["hash_sha1"]),
            "hash_sha224": str(data["hash_sha224"]),
            "hash_sha3_224": str(data["hash_sha3_224"]),
            "hash_sha256": str(data["hash_sha256"]),
            "hash_sha3_256": str(data["hash_sha3_256"]),
            "hash_sha384": str(data["hash_sha384"]),
            "hash_sha3_384": str(data["hash_sha3_384"]),
            "hash_sha512": str(data["hash_sha512"]),
            "hash_sha3_512": str(data["hash_sha3_512"]),
            "hash_blake2b": str(data["hash_blake2b"]),
            "hash_blake2s": str(data["hash_blake2s"])}
    return rdat


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("command", type=str, help="SEREBO command")
    parser.add_argument("-bb", "--bbpath", type=str, help="Path to SEREBO blackbox")
    parser.add_argument("-d", "--description", type=str, default="NA", help="Explanation string for this entry")
    parser.add_argument("-f", "--filepath", type=str, default=None, help="Path of file")
    parser.add_argument("-m", "--message", type=str, help="Text string to be inserted")

    args = parser.parse_args()

    if args.command.lower() == "init": result = initialize(args.bbpath)
    elif args.command.lower() == "intext": result = insertText(args.message, args.description, args.bbpath)
    elif args.command.lower() == "logfile": result = logFile(args.filepath,  args.description, args.bbpath)
    elif args.command.lower() == "sysdata": result = systemData()

    for key in result: print("%s: %s" % (str(key), str(result[key])))
    """
     exposed_functions = {\
         "audit_blockchainflow": auditBlockchainFlow,
         "audit_blockchainhash": auditBlockchainHash,
         "audit_count": auditCount,
         "audit_data_blockchain": auditDataBlockchain,
         "audit_datahash": auditDatahash,
         "audit_notarizebb": auditNotarizeBB,
         "audit_register": auditRegister,
         "backup": backup,
         "changealias": changeAlias,
         "checkhash": checkHash,
         "dump": dump,
         "dumphash": dumpHash,
         "fhash": fileHash,
         "localcode": localCode,
         "localdts": localDTS,
         "notarizebb": notarizeBlackbox,
         "ntpsign": NTPSign,
         "register": registerBlackbox,
         "searchmsg": searchMessage,
         "searchdesc": searchDescription,
         "searchfile": searchFile,
         "selfsign": selfSign,
         "shash": stringHash,
         "sysrecord": systemRecord,
         "viewntpnote": viewNTPNotarizations,
         "viewselfnote": viewSelfNotarizations,
         "viewsnnote": viewNotaryNotarizations,
         "viewreg": viewRegistration}
    """
