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
    sqlstmtA = """select dtstamp, data, description from datalog where description like 'Notarization with SEREBO Notary%'"""
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
        
