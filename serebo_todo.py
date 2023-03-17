def registerBlackbox(owner, email, alias, 
                     notaryURL="https://mauricelab.pythonanywhere.com/serebo_notary/services/call/xmlrpc",
                     bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to register SEREBO Black Box with SEREBO Notary.

    Usage:

        python serebo.py register --alias=<alias for this SEREBO Notary> --notaryURL="https://mauricelab.pythonanywhere.com/serebo_notary/services/call/xmlrpc" --owner=<owner"s name> --email=<owner"s email> --bbpath=<path to SEREBO black box> 

    For example:

        python serebo.py register --alias="NotaryPythonAnywhere" --notaryURL="https://mauricelab.pythonanywhere.com/serebo_notary/services/call/xmlrpc" --owner="Maurice HT Ling" --email="mauriceling@acm.org" --bbpath="serebo_blackbox\\blackbox.sdb"

    @param owner String: Owner"s or administrator"s name.
    @param email String: Owner"s or administrator"s email.
    @param alias String: Alias for this SEREBO Notary.
    @param notaryURL String: URL for SEREBO Notary web service. 
    Default="https://mauricelab.pythonanywhere.com/serebo_notary/services/call/xmlrpc"
    @param bbpath String: Path to SEREBO black box. Default = 
    "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    owner = str(owner)
    email = str(email)
    sqlstmt = "select value from metadata where key="blackboxID""
    blackboxID = [row for row in db.cur.execute(sqlstmt)][0][0]
    data = bb.systemData() 
    architecture = data["architecture"]
    machine = data["machine"]
    node = data["node"] 
    platform = data["platform"] 
    processor = data["processor"]
    try:
        (notaryURL, notaryAuthorization, dtstamp) = \
            notary.registerBlackbox(blackboxID, owner, email, 
                                    architecture, machine, node, 
                                    platform, processor, notaryURL)
        sqlstmt = """insert into notary (dtstamp, alias, owner, email, notaryDTS, notaryAuthorization, notaryURL) values (?,?,?,?,?,?,?)"""
        sqldata = (db.dtStamp(), alias, owner, email, 
                   dtstamp, notaryAuthorization, notaryURL)
        db.cur.execute(sqlstmt, sqldata)
        db.conn.commit()
        rstring = "Register SEREBO Black Box with SEREBO Notary"
        description = ["Notary URL: %s" % str(notaryURL),
                       "Notary Authorization: %s" % \
                            str(notaryAuthorization),
                        "Notary Date Time Stamp %s" % str(dtstamp)]
        description = " | ".join(description)
        rdata = bb.insertFText(db, rstring, description)
        print("")
        print("Registering SEREBO Black Box with SEREBO Notary...")
        rdat = {"SEREBO Black Box": db,
                "Black Box Path": str(db.path),
                "Black Box ID": str(blackboxID),
                "Notary URL": str(notaryURL),
                "Notary Authorization": str(notaryAuthorization),
                "Notary Date Time Stamp": str(dtstamp)}
        return rdat
    except:
        print("Registration failed - likely to be SEREBO Notary error or XMLRPC error.")
        rdat = {"SEREBO Black Box": db,
                "Black Box Path": str(db.path),
                "Black Box ID": str(blackboxID),
                "Notary URL": str(notaryURL)}
        return rdat

def notarizeBlackbox(alias, bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to notarize SEREBO Black Box with SEREBO Notary.

    Usage:

        python serebo.py notarizebb --alias=<alias for SEREBO Notary> --bbpath=<path to SEREBO black box> 

    For example:

        python serebo.py notarizebb --alias="NotaryPythonAnywhere" --bbpath="serebo_blackbox\\blackbox.sdb"

    @param alias String: Alias for this SEREBO Notary.
    @param bbpath String: Path to SEREBO black box. Default = 
    "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    sqlstmt = "select value from metadata where key="blackboxID""
    blackboxID = [row for row in db.cur.execute(sqlstmt)][0][0]
    try:
        sqlstmt = "select notaryAuthorization, notaryURL from notary where alias="%s"" % str(alias)
        sqlresult = [row for row in db.cur.execute(sqlstmt)][0]
        notaryAuthorization = sqlresult[0]
        notaryURL = sqlresult[1]
    except IndexError:
        print("Notary authorization or Notary URL not found for the given alias")
        return {"SEREBO Black Box": db,
                "Black Box Path": str(db.path),
                "Notary Alias": str(alias)}
    dtstampBB = bb.dateTime(db)
    codeBB = bb.randomString(db, 32)
    try:
        (notaryURL, dtstampNS, codeNS, codeCommon) = \
            notary.notarizeBB(blackboxID, notaryAuthorization, 
                              dtstampBB, codeBB, notaryURL)
        description = ["Notarization with SEREBO Notary",
                       "Black Box Code: %s" % codeBB,
                       "Black Box Date Time: %s" % dtstampBB,
                       "Notary Code: %s" % codeNS,
                       "Notary Date Time: %s" % dtstampNS,
                       "Notary URL: %s" % notaryURL]
        description = " | ".join(description)
        rdata = bb.insertFText(db, codeCommon, description)
        print("")
        print("Notarizing SEREBO Black Box with SEREBO Notary...")
        rdat = {"SEREBO Black Box": db,
                "Black Box Path": str(db.path),
                "Notary Alias": str(alias),
                "Notary URL": str(notaryURL),
                "Notary Authorization": str(notaryAuthorization),
                "Notary Date Time Stamp": str(dtstampNS),
                "Date Time Stamp": str(dtstampBB),
                "Black Box Code": str(codeBB),
                "Notary Code": str(codeNS),
                "Cross-Signing Code": str(codeCommon)}
        return rdat
    except:
        print("Failed in attempt to notarize SEREBO Black Box with SEREBO Notary")
        rdat = {"SEREBO Black Box": db,
                "Black Box Path": str(db.path),
                "Notary Alias": str(alias),
                "Notary URL": str(notaryURL),
                "Notary Authorization": str(notaryAuthorization)}
        return rdat

def viewRegistration(bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to view all SEREBO Notary registration for this SEREBO 
    Black Box - This does not insert a record into SEREBO Black Box.

    Usage:

        python serebo.py viewreg --bbpath=<path to SEREBO black box> 

    For example:

        python serebo.py viewreg --bbpath="serebo_blackbox\\blackbox.sdb"

    @param bbpath String: Path to SEREBO black box. Default = 
    "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    print("")
    print("Black Box Path: %s" % str(bbpath))
    sqlstmt = """select dtstamp, alias, owner, email, notaryDTS, notaryAuthorization, notaryURL from notary"""
    print("")
    print("Notary Registration(s) ...")
    for row in db.cur.execute(sqlstmt):     
        print("")
        print("Date Time Stamp: %s" % str(row[0]))
        print("Notary Alias: %s" % str(row[1]))
        print("Owner: %s" % str(row[2]))
        print("Email: %s" % str(row[3]))
        print("Notary Date Time Stamp: %s" % str(row[4]))
        print("Notary Authorization: %s" % str(row[5]))
        print("Notary URL: %s" % str(row[6]))

def viewRegistrationReturn(bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to view all SEREBO Notary registration for this SEREBO 
    Black Box - This does not insert a record into SEREBO Black Box. 
    This is identical to viewRegistration() but used when results 
    needs to be returned to the calling function.

    @param bbpath String: Path to SEREBO black box. Default = 
    "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    print("")
    print("Black Box Path: %s" % str(bbpath))
    sqlstmt = """select dtstamp, alias, owner, email, notaryDTS, notaryAuthorization, notaryURL from notary"""
    rdat = []
    for row in db.cur.execute(sqlstmt):
        tempD = {"Date Time Stamp": str(row[0]),
                 "Notary Alias": str(row[1]),
                 "Owner": str(row[2]),
                 "Email": str(row[3]),
                 "Notary Date Time Stamp": str(row[4]),
                 "Notary Authorization": str(row[5]),
                 "Notary URL": str(row[6])}
        rdat.append(tempD)
    return rdat

def changeAlias(alias, newalias, 
                bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to change alias for a specific SEREBO Notary registration.

    Usage:

        python serebo.py changealias --alias=<current alias to be changed> --newalias=<new alias to change into> --bbpath=<path to SEREBO black box>

    For example:

        python serebo.py changealias --alias="NotaryPythonAnywhere" --newalias="testAlias" --bbpath="serebo_blackbox\\blackbox.sdb"

    @param alias String: Current alias for the SEREBO Notary to change.
    @param newalias String: New alias for the SEREBO Notary.
    @param bbpath String: Path to SEREBO black box. Default = 
    "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    alias = str(alias)
    newalias = str(newalias)
    sqlstmt = """update notary set alias=? where alias=?"""
    db.cur.execute(sqlstmt, (newalias, alias))
    db.conn.commit()
    message = "Change notary alias from %s to %s" % \
        (alias, newalias)
    rdata = bb.insertFText(db, message, "NA")
    print("")
    rdat - {"SEREBO Black Box": db,
            "Black Box Path": str(db.path),
            "Alias": alias,
            "New Alias": newalias}
    return rdat

def dumpHash(outputf, bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to write out record hash from SEREBO Black Box into a 
    file - This does not insert a record into SEREBO Black Box.

    Usage: 

        python serebo.py dumphash --outputf=<output file path> --bbpath=<path to SEREBO black box>

    For example:

        python serebo.py dumphash --outputf=sereboBB_hash --bbpath="serebo_blackbox\\blackbox.sdb"

    @param outputf String: Output file path. Default = sereboBB_hash
    @param bbpath String: Path to SEREBO black box. Default = 
    "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    outputf = str(outputf)
    outputf = bb.absolutePath(outputf)
    outf = open(outputf, "w")
    sqlstmt = "select ID, dtstamp, hash from datalog"
    count = 0
    for row in db.cur.execute(sqlstmt):
        data = [str(row[0]), str(row[1]), str(row[2])]
        data = " | ".join(data)
        outf.write(data + "\n")
        count = count + 1
    outf.close()
    print("")
    print("Dump SEREBO Black Box Data Log Hashes ...")
    print("")
    rdat = {"SEREBO Black Box": db,
            "Black Box Path": str(db.path),
            "Output File Path": outputf,
            "Number of Records": str(count)}
    return rdat

def auditBlockchainHash(bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to check for accuracy in blockchain hash generation 
    within SEREBO Black Box - recorded hash in blockchain and computed 
    hash should be identical. This does not insert a record into 
    SEREBO Black Box.

    Usage: 

        python serebo.py audit_blockchainhash --bbpath=<path to SEREBO black box>

    For example:

        python serebo.py audit_blockchainhash --bbpath="serebo_blackbox\\blackbox.sdb"

    @param bbpath String: Path to SEREBO black box. Default = 
    "serebo_blackbox\\blackbox.sdb".
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
        dhash = "".join([str(p_dtstamp), str(p_randomstring),
                         str(p_hash), str(data)])
        dhash = bytes(dhash, "utf-8")
        tHash = db.hash(dhash)
        if tHash == c_hash:
            print("Verified record %s in Blockchain" % ID)
        else:
            print("ERROR in record %s in Blockchain" % ID)
            print("Hash in record: %s" % c_hash)
            print("Computed hash: %s" % tHash)

def checkHash(hashfile, bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to compare record hash from SEREBO Black Box with that in 
    a hash file. This does not insert a record into SEREBO Black Box.

    Usage: 

        python serebo.py checkhash --hashfile=<path to hash file> --bbpath=<path to SEREBO black box>

    For example:

        python serebo.py checkhash --hashfile=sereboBB_hash --bbpath="serebo_blackbox\\blackbox.sdb"

    @param hashfile String: File path to hash file.
    @param bbpath String: Path to SEREBO black box. Default = 
    "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    hashfile= str(hashfile)
    hashfile = bb.absolutePath(hashfile)
    print("")
    print("Compare record hash from SEREBO Black Box with that in a hash file...")
    print("")
    hf = open(hashfile, "r")
    for record in hf:
        record = [str(d.strip()) for d in record[:-1].split("|")]
        ID = record[0]
        dtstamp = record[1]
        thash = record[2]
        sqlstmt = """select hash from datalog where ID="%s" and dtstamp="%s"""" % (ID, dtstamp)"""
        dhash = [row for row in db.cur.execute(sqlstmt)][0][0]
        dhash = str(dhash)
        if thash == dhash:
            print("Verified record %s hash between Data Log and Hash file" % ID)
        else:
            print("ERROR in record %s" % ID)
            print("Hash in Hash File: %s" % thash)
            print("Hash in Data Log: %s" % dhash)

def auditBlockchainFlow(bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to trace the decendancy of blockchain records (also known 
    as blocks) within SEREBO Black Box - decandency from first block 
    should be traceable to the last / latest block. This does not 
    insert a record into SEREBO Black Box.

    Usage: 

        python serebo.py audit_blockchainflow --bbpath=<path to SEREBO black box>

    For example:

        python serebo.py audit_blockchainflow --bbpath="serebo_blackbox\\blackbox.sdb"

    @param bbpath String: Path to SEREBO black box. Default = 
    "serebo_blackbox\\blackbox.sdb".
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
        # Compare parental block record and parent data in current 
        # record
        if (p_ID == pc_ID) and \
            (p_dtstamp == pc_dtstamp) and \
            (p_randomstring == pc_randomstring) and \
            (p_hash == pc_hash):
            print("Verified - Record %s was used as parent record in record %s" % \
                (str(i), str(i+1)))
        else:
            print("ERROR in record %s" % str(i+1))
            print("Parent ID in record %s: %s" % (str(i+1), str(i)))
            print("Parent date time stamp in record %s: %s" % \
                (str(i+1), p_dtstamp))
            print("Actual date time stamp in record %s: %s" % \
                (str(i), pc_dtstamp))
            print("Parent random string in record %s: %s" % \
                (str(i+1), p_randomstring))
            print("Actual random string in record %s: %s" % \
                (str(i), pc_randomstring))
            print("Parent hash in record %s: %s" % \
                (str(i+1), p_hash))
            print("Actual hash in record %s: %s" % \
                (str(i), pc_hash))

def NTPSign(bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to self-sign (self notarization) SEREBO Black Box using 
    NTP (Network Time Protocol) server.

    Usage:

        python serebo.py ntpsign --bbpath=<path to SEREBO black box> 

    For example:

        python serebo.py ntpsign --bbpath="serebo_blackbox\\blackbox.sdb"

    @param bbpath String: Path to SEREBO black box. Default = 
    "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    ntp = bb.ntplib.NTPClient()
    rstring = bb.randomString(db, 32)
    response = ntp.request("pool.ntp.org", version=3)
    dtstamp = bb.gmtime(response.tx_time)
    ntp_ip = bb.ntplib.ref_id_to_text(response.ref_id)
    description = ["NTP server (self) notarization",
                   "Seconds Since Epoch: %s" % str(response.tx_time),
                   "NTP Date Time: %s" % str(dtstamp),
                   "NTP Server IP: %s" % str(ntp_ip)]
    description = " | ".join(description)
    rdata = bb.insertFText(db, rstring, description)
    print("")
    print("Self-Signing / Self-Notarization ...")
    print("")
    rdat = {"SEREBO Black Box": db,
            "Black Box Path": str(db.path),
            "Date Time Stamp": str(rdata["DateTimeStamp"]),
            "Random String": str(rstring),
            "Seconds Since Epoch": str(response.tx_time),
            "NTP Date Time": str(dtstamp),
            "NTP Server IP": str(ntp_ip)}
    return rdat

def backup(backuppath="blackbox_backup.sdb",
           bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to backup SEREBO Black Box - This does not insert a 
    record into SEREBO Black Box.

    Usage:

        python serebo.py backup --backuppath=<path for backed-up SEREBO black box> --bbpath=<path to SEREBO black box> 

    For example:

        python serebo.py backup --backuppath="blackbox_backup.sdb" --bbpath="serebo_blackbox\\blackbox.sdb"

    @param backuppath String: Path for backed-up SEREBO black box. Default = "blackbox_backup.sdb"
    @param bbpath String: Path to SEREBO black box. Default = 
    "serebo_blackbox\\blackbox.sdb".
    """
    print("")
    print("Backup SEREBO Black Box ...")
    print("")
    if backuppath != bbpath:
        (bbpath, backuppath) = bb.backup(bbpath, backuppath)
        rdat = {"Black Box Path": bbpath,
                "Backup Path": backuppath}
        return rdat
    else:
        print("Backup path cannot be the same as SEREBO Black Box path")
        bbpath = bb.absolutePath(bbpath)
        backuppath = bb.absolutePath(backuppath)
        rdat = {"Black Box Path": bbpath,
                "Backup Path": backuppath}
        return rdat

def dump(dumpfolder=".", fileprefix="dumpBB", 
         bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to dump individual data tables from SEREBO Black Box into 
    text files - This does not insert a record into SEREBO Black Box.

    Usage:

        python serebo.py dump --dumpfolder=<folder to save dump files> --fileprefix=<prefix for individual dump files> --bbpath=<path to SEREBO black box>

    For example:

        python serebo.py dump --dumpfolder="." --fileprefix="dumpBB" --bbpath="serebo_blackbox\\blackbox.sdb"

    @param dumpfolder String: Folder to save dump files. Default = "." 
    (current working directory).
    @param fileprefix String: Prefix for individual dump files. 
    Default = "dumpBB".
    @param bbpath String: Path to SEREBO black box. Default = 
    "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    tableSet = {"metadata": ["key", "value"],
                "notary": ["dtstamp", 
                           "alias",
                           "owner",
                           "email",
                           "notaryDTS",
                           "notaryAuthorization",
                           "notaryURL"],
                "systemdata": ["dtstamp", "key", "value"],
                "datalog": ["dtstamp",
                            "hash",
                            "data",
                            "description"],
                "blockchain": ["c_ID", "c_dtstamp",
                               "c_randomstring", "c_hash",
                               "p_ID", "p_dtstamp",
                               "p_randomstring", "p_hash", "data"],
                "eventlog": ["dtstamp", "fID", "description"],
                "eventlog_datamap": ["dtstamp", "fID", 
                                     "key", "value"]}
    print("")
    print("Dump out data (text backup) from SEREBO Black Box ...")
    print("")
    for tableName in tableSet:
        outputfile = [dumpfolder, 
                      fileprefix + "_" + tableName + ".csv"]
        outputfile = os.sep.join(outputfile)
        (outputfile, count) = bb.dumpTable(db, tableName, 
                                           tableSet[tableName], 
                                           outputfile)
        print("%s table dumped into %s" % (tableName, outputfile))
        print("Number of records dumped: %s" % count)
        print("")
    
def auditRegister(alias, bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to check for SEREBO Black Box registration with SEREBO 
    Notary - This does not insert a record into SEREBO Black Box.

    Usage:

        python serebo.py audit_register --alias=<alias for SEREBO Notary> --bbpath=<path to SEREBO black box> 

    For example:

        python serebo.py audit_register --alias="NotaryPythonAnywhere" --bbpath="serebo_blackbox\\blackbox.sdb"

    @param alias String: Alias for this SEREBO Notary.
    @param bbpath String: Path to SEREBO black box. Default = 
    "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    sqlstmt = "select value from metadata where key="blackboxID""
    blackboxID = [row for row in db.cur.execute(sqlstmt)][0][0]
    try:
        sqlstmt = "select notaryAuthorization, notaryURL from notary where alias="%s"" % str(alias)
        sqlresult = [row for row in db.cur.execute(sqlstmt)][0]
        notaryAuthorization = sqlresult[0]
        notaryURL = sqlresult[1]
    except IndexError:
        print("Notary authorization or Notary URL not found for the given alias")
        return {"SEREBO Black Box": db,
                "Black Box Path": str(db.path),
                "Notary Alias": str(alias)}
    try:
        presence = notary.checkRegistration(blackboxID, notaryAuthorization, 
                                            notaryURL)
        if presence:
            message = "Registration found in SEREBO Notary"
        else:
            message = "Registration NOT found in SEREBO Notary"
        print("")
        print("Checking SEREBO Black Box registration in SEREBO Notary...")
        rdat = {"SEREBO Black Box": db,
                "Black Box Path": str(db.path),
                "Notary Alias": str(alias),
                "Notary URL": str(notaryURL),
                "Notary Authorization": str(notaryAuthorization),
                "Status": message}
        return rdat
    except:
        print("Failed in checking SEREBO Black Box registration in SEREBO Notary")
        rdat = {"SEREBO Black Box": db,
                "Black Box Path": str(db.path),
                "Notary Alias": str(alias),
                "Notary URL": str(notaryURL),
                "Notary Authorization": str(notaryAuthorization)}
        return rdat

def viewSelfNotarizations(bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to view all self notarizations for this SEREBO Black 
    Box - This does not insert a record into SEREBO Black Box.

    Usage:

        python serebo.py viewselfnote --bbpath=<path to SEREBO black box> 

    For example:

        python serebo.py viewselfnote --bbpath="serebo_blackbox\\blackbox.sdb"

    @param bbpath String: Path to SEREBO black box. Default = 
    "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    print("")
    print("Black Box Path: %s" % str(bbpath))
    sqlstmt = """select dtstamp, data from datalog where description like 'Self notarization'"""
    print("")
    print("Self Notarization(s) ...")
    for row in db.cur.execute(sqlstmt):
        print("")
        print("Date Time Stamp: %s" % str(row[0]))
        print("Hash: %s" % str(row[1]))

def viewNTPNotarizations(bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to view all self-notarization(s) by NTP time server for 
    this SEREBO Black Box - This does not insert a record into SEREBO 
    Black Box.

    Usage:

        python serebo.py viewntpnote --bbpath=<path to SEREBO black box> 

    For example:

        python serebo.py viewntpnote --bbpath="serebo_blackbox\\blackbox.sdb"

    @param bbpath String: Path to SEREBO black box. Default = 
    "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    print("")
    print("Black Box Path: %s" % str(bbpath))
    sqlstmt = """select dtstamp, data, description from datalog where description like 'NTP server (self) notarization%'"""
    print("")
    print("Self-Notarization(s) by NTP Time Server(s) ...")
    for row in db.cur.execute(sqlstmt):
        description = [x.strip() for x in str(row[2]).split("|")]
        print("")
        print("Date Time Stamp: %s" % str(row[0]))
        print("Random Code: %s" % str(row[1]))
        print("NTP Seconds Since Epoch: %s" % description[1])
        print("NTP Date Time: %s" % description[2])
        print("NTP Server IP: %s" % description[3])

def viewNotaryNotarizations(bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to view all notarizations by SEREBO Notary for this SEREBO 
    Black Box - This does not insert a record into SEREBO Black Box.

    Usage:

        python serebo.py viewsnnote --bbpath=<path to SEREBO black box> 

    For example:

        python serebo.py viewsnnote --bbpath="serebo_blackbox\\blackbox.sdb"

    @param bbpath String: Path to SEREBO black box. Default = 
    "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    print("")
    print("Black Box Path: %s" % str(bbpath))
    sqlstmt = """select dtstamp, data, description from datalog where description like 'Notarization with SEREBO Notary%'"""
    print("")
    print("Notarization(s) by SEREBO Notary(ies) ...")
    for row in db.cur.execute(sqlstmt):
        description = [x.strip() for x in str(row[2]).split("|")]
        print("")
        print("Date Time Stamp: %s" % str(row[0]))
        print("Common Code: %s" % str(row[1]))
        print(description[1]) # Black Box Code
        print(description[2]) # Black Box Date Time
        print(description[3]) # Notary Code
        print(description[4]) # Notary Date Time
        print(description[5]) # Notary URL

def _auditSingleNotarizeBB(blackboxID, notaryAuthorization, notaryURL,
                           BBCode, NCode, CommonCode):
    """!
    Private function - communicate with SEREBO Notary to check for 
    SEREBO Black Box notarization record.

    @param blackboxID String: ID of SEREBO black box - found in 
    metadata table in SEREBO black box database.
    @param notaryAuthorization String: Notary authorization code of 
    SEREBO black box (generated during black box registration - found 
    in metadata table in SEREBO black box database.
     @param notaryURL String: URL for SEREBO Notary web service.
    @param BBCode String: Notarization code from SEREBO Black Box.
    @param NCode String: Notarization code from SEREBO Notary.
    @param CommonCode String: Cross-Signing code from SEREBO Notary.
    @returns: "True" if SEREBO Black Box notarization is found in 
    SEREBO Notary. "False" if SEREBO Black Box notarization is not 
    found in SEREBO Notary. "Failed" if there is any errors, such as 
    network error.
    """
    try:
        presence = notary.checkNotarization(blackboxID, 
                                            notaryAuthorization, 
                                            BBCode, 
                                            NCode, 
                                            CommonCode, 
                                            notaryURL)
        return presence
    except:
        return "Failed"

def auditNotarizeBB(bbpath="serebo_blackbox\\blackbox.sdb"):
    """!
    Function to view all notarizations by SEREBO Notary for this SEREBO 
    Black Box - This does not insert a record into SEREBO Black Box.

    Usage:

        python serebo.py audit_notarizebb --bbpath=<path to SEREBO black box> 

    For example:

        python serebo.py audit_notarizebb --bbpath="serebo_blackbox\\blackbox.sdb"

    @param bbpath String: Path to SEREBO black box. Default = 
    "serebo_blackbox\\blackbox.sdb".
    """
    db = bb.connectDB(bbpath)
    sqlstmt = "select value from metadata where key="blackboxID""
    blackboxID = [row for row in db.cur.execute(sqlstmt)][0][0]
    print("")
    print("Black Box Path: %s" % str(bbpath))
    sqlstmtA = """select dtstamp, data, description from datalog where description like "Notarization with SEREBO Notary%""""
    dataA = [row for row in db.cur.execute(sqlstmtA)]
    print("")
    print("Notarization(s) by SEREBO Notary(ies) ...")
    for row in dataA:
        description = [x.strip() for x in str(row[2]).split("|")]
        try:
            notaryURL = description[5].split(": ")[1].strip()
            sqlstmt = "select notaryAuthorization from notary where notaryURL="%s"" % str(notaryURL)
            sqlresult = [row for row in db.cur.execute(sqlstmt)][0]
            notaryAuthorization = sqlresult[0]
        except IndexError:
            print("Notary authorization not found for the given Notary URL")
            return {"SEREBO Black Box": db,
                    "Black Box Path": str(db.path),
                    "Notary URL": str(notaryURL)}
        presence = _auditSingleNotarizeBB(blackboxID, 
                                          notaryAuthorization,
                                          notaryURL,
                                          description[1].split(": ")[1].strip(), 
                                          description[3].split(": ")[1].strip(), 
                                          str(row[1]))
        if presence == "True":
            message = "Notarization record is found in SEREBO Notary"
        elif presence == "False":
            message = "Notarization record is NOT found in SEREBO Notary"
        elif presence == "Failed":
            message = "Unspecified error - does not mean that notarization record is not found. It may mean network error."
        print("")
        print("Date Time Stamp: %s" % str(row[0]))
        print("Common Code: %s" % str(row[1]))
        print(description[1]) # Black Box Code
        print(description[2]) # Black Box Date Time
        print(description[3]) # Notary Code
        print(description[4]) # Notary Date Time
        print(description[5]) # Notary URL
        print("Status: %s" % message)
        
