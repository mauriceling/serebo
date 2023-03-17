"""!
Secured Recorder Box (SEREBO) Command Line Interface (CLI)

Date created: 17th May 2018

License: GNU General Public License version 3 for academic or 
not-for-profit use only


SEREBO is free software: you can redistribute it and/or modify it 
under the messages of the GNU General Public License as published by the 
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

    @param bbpath String: Path to SEREBO black box. Default = "serebo_blackbox\\blackbox.sdb".
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
    @param description String: Explanation string for this entry event. Default = NA.
    @param bbpath String: Path to SEREBO black box. Default = "serebo_blackbox\\blackbox.sdb".
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
    @param description String: Explanation string for this entry event. Default = NA.
    @param bbpath String: Path to SEREBO black box. Default = "serebo_blackbox\\blackbox.sdb".
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
    Function to print out data and test hashes of current platform - This does not insert a record into SEREBO Black Box.

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

def systemRecord(bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to record data and test hashes of current platform.

    Usage:

        python serebo.py sysrecord --bbpath=<path to SEREBO black box>

    For example:

        python serebo.py sysrecord --bbpath="serebo_blackbox\\blackbox.sdb"

    @param bbpath String: Path to SEREBO black box. Default = "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    data = bb.systemData()
    dtstamp = bb.dateTime(db)
    sqlstmt = """insert into systemdata (dtstamp, key, value) values 
        ("%s", "%s", "%s");"""
    print("")
    print("System Data ...")
    for k in data:
        if k != "hashdata":
            db.cur.execute(sqlstmt % (str(dtstamp), str(k), 
                                      str(data[k])))
    db.conn.commit()
    rdat = {"SEREBO Black Box": db,
            "Black Box Path": str(db.path),
            "architecture": str(data["architecture"]),
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

def fileHash(filepath):
    """!
    Function to generate and print out hash of a file.

    Usage:

        python serebo.py fhash --filepath=<path of file to hash>

    For example:

        python serebo.py fhash --filepath=doxygen_serebo

    @param fileapth String: Path of file to process.
    """
    fHash = bb.fileHash(filepath)
    print("")
    rdat = {"File Path": str(filepath),
            "File Hash": str(fHash)}
    return rdat

def localCode(length, description=None, 
              bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to generate a random string, and log this generation into SEREBO Black Box.

    Usage:

        python serebo.py localcode --length=<length of random string> --description=<explanatory description for this insertion> --bbpath=<path to SEREBO black box> 

    For example:

        python serebo.py localcode --length=10 --description="Notarizing certificate ABC123" --bbpath="serebo_blackbox\\blackbox.sdb"

    @param length Integer: Length of random string to generate
    @param description String: Explanation string for this entry event. Default = None.
    @param bbpath String: Path to SEREBO black box. Default = "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    rstring = bb.randomString(db, length)
    description = ["Local random string generation"] + [description]
    description = " | ".join(description)
    rdata = bb.insertFText(db, rstring, description)
    print("")
    print("Generate Random String (Local) ...")
    rdat = {"SEREBO Black Box": db,
            "Black Box Path": str(db.path),
            "Date Time Stamp": str(rdata["DateTimeStamp"]),
            "Random String": str(rstring)}
    return rdat

def localDTS(bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to get date time string. This event is not logged.

    Usage:

        python serebo.py localdts --bbpath=<path to SEREBO black box> 

    For example:

        python serebo.py localdts --bbpath="serebo_blackbox\\blackbox.sdb"

    @param bbpath String: Path to SEREBO black box. Default = "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    dts = bb.dateTime(db)
    print("")
    rdat = {"SEREBO Black Box": db,
            "Black Box Path": str(db.path),
            "Date Time Stamp": str(dts)}
    return rdat

def stringHash(message, bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to generate hash for a data string. This event is not logged.

    Usage:

        python serebo.py shash --message=<string to hash> --bbpath=<path to SEREBO black box> 

    For example:

        python serebo.py shash --message="SEREBO is hosted at https://github.com/mauriceling/serebo" --bbpath="serebo_blackbox\\blackbox.sdb"

    @param message String: Message to generate hash.
    @param bbpath String: Path to SEREBO black box. Default = "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    x = bb.stringHash(db, message)
    print("")
    rdat = {"SEREBO Black Box": db,
            "Black Box Path": str(db.path),
            "Data String": str(message),
            "Data Hash": str(x)}
    return rdat

def selfSign(bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to self-sign (self-notarization) SEREBO Black Box.

    Usage:

        python serebo.py selfsign --bbpath=<path to SEREBO black box> 

    For example:

        python serebo.py selfsign --bbpath="serebo_blackbox\\blackbox.sdb"

    @param bbpath String: Path to SEREBO black box. Default = "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    rstring = bb.randomString(db, 32) 
    rdata = bb.insertFText(db, rstring, "Self notarization")
    print("")
    print("Self-Signing / Self-Notarization ...")
    rdat = {"SEREBO Black Box": db,
            "Black Box Path": str(db.path),
            "Date Time Stamp": str(rdata["DateTimeStamp"]),
            "Random String": str(rstring)}
    return rdat

def searchMessage(message, mode="like",
                  bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to search SEREBO Black Box for a message - This does not insert a record into SEREBO Black Box.

    Usage: 

        python serebo.py searchmsg --mode=<search mode> --message=<search message> --bbpath=<path to SEREBO black box>

    For example:

        python serebo.py searchmsg --mode="like" --message="Self%" --bbpath="serebo_blackbox\\blackbox.sdb"

    @param message String: Case sensitive search message.
    @param mode String: Mode of search. Allowable modes are "like" and "exact". If mode is "like", wildcards such as "_" (matches any single character) and "%" (matches any number of characters). Default = "like".
    @param bbpath String: Path to SEREBO black box. Default = "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    mode = str(mode)
    message = str(message)
    result = bb.searchDatalog(db, message, "data", mode)
    rdat = []
    for row in result:
        tempD = {"Date Time Stamp": str(row[1]),
                 "Message": str(row[3]),
                 "Description": str(row[4])}
        rdat.append(tempD)
    return rdat

def searchDescription(message, mode="like",
                      bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to search SEREBO Black Box for a description - This does not insert a record into SEREBO Black Box.

    Usage: 

        python serebo.py searchdesc --mode=<search mode> --message=<search term> --bbpath=<path to SEREBO black box>

    For example:

        python serebo.py searchdesc --mode="like" --message="%NA%" --bbpath="serebo_blackbox\\blackbox.sdb"

    @param message String: Case sensitive search term.
    @param mode String: Mode of search. Allowable modes are "like" and "exact". If mode is "like", wildcards such as "_" (matches any single character) and "%" (matches any number of characters). Default = "like".
    @param bbpath String: Path to SEREBO black box. Default = "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    mode = str(mode)
    message = str(message)
    result = bb.searchDatalog(db, message, "description", mode)
    rdat = []
    for row in result:
        tempD = {"Date Time Stamp": str(row[1]),
                 "Message": str(row[3]),
                 "Description": str(row[4])}
        rdat.append(tempD)
    return rdat

def searchFile(filepath, bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to search SEREBO Black Box for a file logging event - This does not insert a record into SEREBO Black Box.

    Usage: 

        python serebo.py searchfile --filepath=<path to file for searching> --bbpath=<path to SEREBO black box>

    For example:

        python serebo.py searchfile --filepath=doxygen_serebo --bbpath="serebo_blackbox\\blackbox.sdb"

    @param fileapth String: Path of file to search in SEREBO black box.
    @param bbpath String: Path to SEREBO black box. Default = "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    filepath = str(filepath)
    absPath = bb.absolutePath(filepath)
    fHash = bb.fileHash(absPath)
    result = bb.searchDatalog(db, fHash, "data", "exact")
    rdat = []
    for row in result:
        tempD = {"File Path": filepath,
                 "Absolute File Path": absPath,
                 "Date Time Stamp": str(row[1]),
                 "Message": str(row[3]),
                 "Description": str(row[4])}
        rdat.append(tempD)
    return rdat

def auditCount(bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to check for equal numbers of records in data log and blockchain in SEREBO Black Box - should have the same number of records. This does not insert a record into SEREBO Black Box.

    Usage: 

        python serebo.py audit_count --bbpath=<path to SEREBO black box>

    For example:

        python serebo.py audit_count --bbpath="serebo_blackbox\\blackbox.sdb"

    @param bbpath String: Path to SEREBO black box. Default = 
    "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    sqlstmtA = "select ID, dtstamp from datalog"
    sqlresultA = {}
    for row in db.cur.execute(sqlstmtA):
        sqlresultA[row[0]] = row[1]
    sqlstmtB = "select c_ID, c_dtstamp from blockchain"
    sqlresultB = {}
    for row in db.cur.execute(sqlstmtB):
        sqlresultB[row[0]] = row[1]
    print("")
    print("Audit SEREBO Black Box Data Count ...")
    print("")
    if len(sqlresultA) == len(sqlresultB):
        for k in sqlresultA:
            if sqlresultA[k] != sqlresultB[k]:
                print("Date time stamp mismatch")
                print("Datalog record number %s" % str(k))
                print("Datalog date time stamp: %s" % \
                    str(sqlresultA[k]))
                print("Blockchain date time stamp: %s" % \
                    str(sqlresultB[k]))
            else:
                print("Date time stamp match - Record %s" % str(k))
        print("Number of records in datalog matches the number of records in blockchain")
    else:
        if len(sqlresultA) > len(sqlresultB):
            print("Number of records in datalog MORE than the number of records in blockchain")
        elif len(sqlresultA) < len(sqlresultB):
            print("Number of records in datalog LESS than the number of records in blockchain")
    return {}

def auditDatahash(bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to check for accuracy of hash generations in data log within SEREBO Black Box - recorded hash in data log and computed hash should be identical. This does not insert a record into SEREBO Black Box.

    Usage: 

        python serebo.py audit_datahash --bbpath=<path to SEREBO black box>

    For example:

        python serebo.py audit_datahash --bbpath="serebo_blackbox\\blackbox.sdb"

    @param bbpath String: Path to SEREBO black box. Default = 
    "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    sqlstmt = """select ID, dtstamp, data, description, hash from datalog"""
    print("")
    print("Audit SEREBO Black Box Data Log Records ...")
    print("")
    for row in db.cur.execute(sqlstmt):
        ID = str(row[0])
        dtstamp = str(row[1])
        data = str(row[2])
        description = str(row[3])
        rHash = str(row[4])
        dhash = bytes(dtstamp, "utf-8") + bytes(data, "utf-8") + bytes(description, "utf-8")
        tHash = db.hash(dhash)
        if tHash == rHash:
            print("Verified record %s in data log" % ID)
        else:
            print("ERROR in record %s in data log" % ID)
            print("Hash in record: %s" % rHash)
            print("Computed hash: %s" % tHash)
    return {}

def auditDataBlockchain(bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to check for accuracy in data log and blockchain mapping in SEREBO Black Box - recorded hash in data log and data in 
    blockchain should be identical. This does not insert a record into SEREBO Black Box.

    Usage: 

        python serebo.py audit_data_blockchain --bbpath=<path to SEREBO black box>

    For example:

        python serebo.py audit_data_blockchain --bbpath="serebo_blackbox\\blackbox.sdb"

    @param bbpath String: Path to SEREBO black box. Default = "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    sqlstmt = """select datalog.ID, datalog.dtstamp, datalog.hash, blockchain.c_dtstamp, blockchain.data from datalog inner join blockchain where datalog.ID=blockchain.c_ID and datalog.dtstamp=blockchain.c_dtstamp"""
    print("")
    print("Audit SEREBO Black Box - Accuracy in Data Log to Blockchain Mapping...")
    print("")
    for row in db.cur.execute(sqlstmt):
        dID = str(row[0])
        ddtstamp = str(row[1])
        dhash = str(row[2])
        bdtstamp = str(row[3])
        bhash = str(row[4])
        if dhash == bhash:
            print("Verified record %s mapping" % dID)
        else:
            print("ERROR in record %s mapping" % dID)
            print("Hash in Data Log: %s" % dHash)
            print("Data in Blockchain: %s" % bHash)
    return {}

def auditBlockchainHash(bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to check for accuracy in blockchain hash generation within SEREBO Black Box - recorded hash in blockchain and computed hash should be identical. This does not insert a record into SEREBO Black Box.

    Usage: 

        python serebo.py audit_blockchainhash --bbpath=<path to SEREBO black box>

    For example:

        python serebo.py audit_blockchainhash --bbpath="serebo_blackbox\\blackbox.sdb"

    @param bbpath String: Path to SEREBO black box. Default = "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    sqlstmt = """select c_ID, p_dtstamp, p_randomstring, p_hash, data, c_hash from blockchain"""
    print("")
    print("Audit SEREBO Black Box Blockchain hashes ...")
    print("")
    for row in db.cur.execute(sqlstmt):
        ID = str(row[0])
        p_dtstamp = str(row[1])
        p_randomstring = str(row[2])
        p_hash = str(row[3])
        data = str(row[4])
        c_hash = str(row[5])
        dhash = "".join([str(p_dtstamp), str(p_randomstring), str(p_hash), str(data)])
        dhash = bytes(dhash, "utf-8")
        tHash = db.hash(dhash)
        if tHash == c_hash:
            print("Verified record %s in Blockchain" % ID)
        else:
            print("ERROR in record %s in Blockchain" % ID)
            print("Hash in record: %s" % c_hash)
            print("Computed hash: %s" % tHash)
    return {}

def auditBlockchainFlow(bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to trace the decendancy of blockchain records (also known as blocks) within SEREBO Black Box - decandency from first block should be traceable to the last / latest block. This does not insert a record into SEREBO Black Box.

    Usage: 

        python serebo.py audit_blockchainflow --bbpath=<path to SEREBO black box>

    For example:

        python serebo.py audit_blockchainflow --bbpath="serebo_blackbox\\blackbox.sdb"

    @param bbpath String: Path to SEREBO black box. Default = "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    sqlstmt = """select max(c_ID) from blockchain"""
    print("")
    print("Trace SEREBO Black Box Blockchain's block decendancy ...")
    print("")
    maxID = [row for row in db.cur.execute(sqlstmt)][0][0]
    maxID = int(maxID)
    for i in range(1, maxID, 1):
        # Get parent data from parent block
        sqlstmt = """select c_ID, c_dtstamp, c_randomstring, c_hash from blockchain where c_ID=%s""" % str(i)
        #print(sqlstmt)
        p_data = [row for row in db.cur.execute(sqlstmt)][0]
        pc_ID = str(p_data[0])
        pc_dtstamp = str(p_data[1])
        pc_randomstring = str(p_data[2])
        pc_hash = str(p_data[3])
        # Get parent data from current / child block
        sqlstmt = """select p_ID, p_dtstamp, p_randomstring, p_hash from blockchain where c_ID=%s""" % str(i+1)
        #print(sqlstmt)
        c_data = [row for row in db.cur.execute(sqlstmt)][0]
        p_ID = str(c_data[0])
        p_dtstamp = str(c_data[1])
        p_randomstring = str(c_data[2])
        p_hash = str(c_data[3])
        # Compare parental block record and parent data in current record
        if (p_ID == pc_ID) and \
            (p_dtstamp == pc_dtstamp) and \
            (p_randomstring == pc_randomstring) and \
            (p_hash == pc_hash):
            print("Verified - Record %s was used as parent record in record %s" % (str(i), str(i+1)))
        else:
            print("ERROR in record %s" % str(i+1))
            print("Parent ID in record %s: %s" % (str(i+1), str(i)))
            print("Parent date time stamp in record %s: %s" % (str(i+1), p_dtstamp))
            print("Actual date time stamp in record %s: %s" % (str(i), pc_dtstamp))
            print("Parent random string in record %s: %s" % (str(i+1), p_randomstring))
            print("Actual random string in record %s: %s" % (str(i), pc_randomstring))
            print("Parent hash in record %s: %s" % (str(i+1), p_hash))
            print("Actual hash in record %s: %s" % (str(i), pc_hash))
    return {}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("command", type=str, help="SEREBO command")
    parser.add_argument("-bb", "--bbpath", type=str, default="serebo_blackbox\\blackbox.sdb", help="Path to SEREBO blackbox")
    parser.add_argument("-d", "--description", type=str, default="NA", help="Explanation string for this entry")
    parser.add_argument("-f", "--filepath", type=str, default=None, help="Path of file")
    parser.add_argument("-l", "--length", type=int, default=10, help="Length of item to generate")
    parser.add_argument("-m", "--message", type=str, help="Text string to be processed")
    parser.add_argument("-mo", "--mode", type=str, default="like", help="Type of processing mode")

    args = parser.parse_args()

    if args.command.lower() == "audit_blockchainflow": result = auditBlockchainFlow(args.bbpath)
    elif args.command.lower() == "audit_blockchainhash": result = auditBlockchainHash(args.bbpath)
    elif args.command.lower() == "audit_count": result = auditCount(args.bbpath)
    elif args.command.lower() == "audit_data_blockchain": result = auditDataBlockchain(args.bbpath)
    elif args.command.lower() == "audit_datahash": result = auditDatahash(args.bbpath)
    elif args.command.lower() == "fhash": result = fileHash(args.filepath)
    elif args.command.lower() == "init": result = initialize(args.bbpath)
    elif args.command.lower() == "intext": result = insertText(args.message, args.description, args.bbpath)
    elif args.command.lower() == "localcode": result = localCode(args.length, args.description, args.bbpath)
    elif args.command.lower() == "localdts": result = localDTS(args.bbpath)
    elif args.command.lower() == "logfile": result = logFile(args.filepath, args.description, args.bbpath)
    elif args.command.lower() == "searchdesc": result = searchDescription(args.message, args.mode, args.bbpath)
    elif args.command.lower() == "searchfile": result = searchFile(args.filepath, args.bbpath)
    elif args.command.lower() == "searchmsg": result = searchMessage(args.message, args.mode, args.bbpath)
    elif args.command.lower() == "selfsign": result = selfSign(args.bbpath)
    elif args.command.lower() == "shash": result = stringHash(args.message, args.bbpath)
    elif args.command.lower() == "sysdata": result = systemData()
    elif args.command.lower() == "sysrecord": result = systemRecord(args.bbpath)

    for key in result: 
        try:
            print("%s: %s" % (str(key), str(result[key])))
        except TypeError:
            for row in result:
                for k2 in row:
                    print("%s: %s" % (str(k2), str(row[k2])))
            print("")
    """
"audit_notarizebb": auditNotarizeBB,
"audit_register": auditRegister,
"backup": backup,
"changealias": changeAlias,
"checkhash": checkHash,
"dump": dump,
"dumphash": dumpHash,
"notarizebb": notarizeBlackbox,
"ntpsign": NTPSign,
"register": registerBlackbox,
"viewntpnote": viewNTPNotarizations,
"viewselfnote": viewSelfNotarizations,
"viewsnnote": viewNotaryNotarizations,
"viewreg": viewRegistration
    """
