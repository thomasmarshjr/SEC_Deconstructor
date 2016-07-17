import os, sys, os.path, re, csv
from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.rtf15.writer import Rtf15Writer
from pyth.plugins.plaintext.writer import PlaintextWriter
from PyRTF import *

def removeNonAscii(s):
    return "".join(filter(lambda x: ord(x) < 128, s))

def getName(sec_txt):
    if(sec_txt.find("Inc.", 0, 1000) != -1 or sec_txt.find("INC.", 0, 1000) != -1):
        return getNameInc(sec_txt)
    elif(sec_txt.find("Company", 0, 1000) != -1 or sec_txt.find("COMPANY", 0, 1000) != -1):
        return getNameCompany(sec_txt)
    else:
        return getNameCorp(sec_txt)

def getNameInc(sec_txt):
    loc_name1 = sec_txt.find("Inc.", 0, 1000)
    if loc_name1 == -1:
        loc_name1 = sec_txt.find("INC.", 0, 1000)
    loc_name2 = 0
    x = loc_name1
    while loc_name1 - x < 17:
        if sec_txt[x] == "\n":
            loc_name2 = x
            x = x - 50
        x -= 1
    name = sec_txt[loc_name2 + 1:loc_name1 + 3]
    if name.rfind("\n") != -1:
        name = name[name.rfind("\n")+1: len(name)]
    return getTicker(name)

def getNameCorp(sec_txt):
    loc_name1 = sec_txt.find("Corporation", 0, 1000)
    if loc_name1 == -1:
        loc_name1 = sec_txt.find("CORPORATION", 0, 1000)
    loc_name2 = 0
    x = loc_name1
    while loc_name1 - x < 20:
        if sec_txt[x] == "\n":
            loc_name2 = x
            x = x - 50
        x -= 1
    name = sec_txt[loc_name2 + 1:loc_name1 + 11]
    if len(name)>40:
        name = name[name.rfind("\n")+1:len(name)]
    return getTicker(name)

def getNameCompany(sec_txt):
    loc_name1 = sec_txt.find("COMPANY", 0, 1000)
    if loc_name1 == -1:
        loc_name1 = sec_txt.find("Company", 0, 1000)
    loc_name2 = 0
    x = loc_name1
    while loc_name1 - x < 20:
        if sec_txt[x] == "\n":
            loc_name2 = x
            x = x - 50
        x -= 1
    name = sec_txt[loc_name2 + 1:loc_name1 + 7]
    return getTicker(name)

def getTicker(name):
    if (name == "MICROSOFT CORPORATION" or name == "Microsoft Corporation"):
        return "MSFT"
    elif (name == "APPLE INC" or name == "Apple Inc" or name == "APPLE COMPUTER, INC"):
        return "AAPL"
    elif (name == "Facebook, Inc" or name == "FACEBOOK, INC"):
        return "FB"
    elif (name == "Twitter, Inc" or name == "TWITTER, INC"):
        return "TWTR"
    elif (name == "NETFLIX INC." or name == "Netflix, Inc" or name == "NETFLIX, INC"):
        return "NFLX"
    elif (name == "Google, Inc" or name == "GOOGLE INC."):
        return "GOOGL"
    elif (name == "LOCKHEED MARTIN CORPORATION"):
        return "LMT"
    elif (name == "THE BOEING COMPANY" or name == "~THE BOEING COMPANY" or name == "The Boeing Company" or name == "~The Boeing Company"):
        return "BA"
    elif (name == "NORTHROP GRUMMAN CORPORATION"):
        return "NOC"
    elif (name == "Ball Corporation" or name == "BALL CORPORATION"):
        return "BLL"
    elif (name == "EMCORE Corporation" or name == "Emcore Corporation" or name == "EMCORE CORPORATION"):
        return "EMKR"
    elif (name == "UNITED TECHNOLOGIES CORPORATION"):
        return "UTX"
    else:
        print "Wrong Ticker"

def typeDoc(sec_txt):
    if (sec_txt.find("10-K/A", 0, 200  ) == -1 and (sec_txt.find("FORM 10-K", 0, 400) != -1 or sec_txt.find("10-K", 0, 300) != -1)):
        return "10K"
    elif (sec_txt.find("8-K/A", 0, 400) != -1):
        return "8KA"
    elif (sec_txt.find("FORM 10-K/A", 0, 400) != -1 or sec_txt.find("K/A", 0, 400) != -1):
        return "10KA"
    elif (sec_txt.find("10-Q/A", 0, 400) != -1):
        return "10QA"
    elif (sec_txt.find("10-Q", 0, 200) == -1 and (sec_txt.find("8-K", 0, 300) != -1 or sec_txt.find("8-K", 0, 300) != -1 or sec_txt.find("Form 8-K", 0, 300))):
        return "8K"
    elif (sec_txt.find("FORM 10-Q", 0, 300) != -1 or sec_txt.find("Form 10-Q", 0, 300) != -1 or sec_txt.find("FORM 10-Q", 0, 300)):
        return "10Q"
    else:
        return "10K"


adfadfasfasdfasdfasdfsdafasdfasdfasdfasdfasdfdsfasdfasdfadfadsfadfasdfdsfasdfasdfadsfasd4i36463iaz
def docDate(sec_txt, type_doc):
    date_end = ""
    if (type_doc == "10Q"):
        loc_date1 = sec_txt.find("For the quarterly period ended")
        if loc_date1 == -1:
            loc_date1 = sec_txt.find("For the Quarterly Period Ended")
        if loc_date1 == -1:
            loc_date1 = sec_txt.find("FOR THE QUARTERLY PERIOD ENDED")
        loc_date2 = sec_txt.find("\n", loc_date1)
        date_end = removeNonAscii(sec_txt[loc_date1 + 31:loc_date2])
    elif (type_doc == "10K" or type_doc == "10KA"):
        loc_date1 = sec_txt.find("For the fiscal year ended")
        if loc_date1 == -1:
            loc_date1 = sec_txt.find("For the Fiscal Year Ended")
        if loc_date1 == -1:
            loc_date1 = sec_txt.find("FOR THE FISCAL YEAR ENDED")
        loc_date2 = sec_txt.find("\n", loc_date1)
        date_end = removeNonAscii(sec_txt[loc_date1 + 26:loc_date2])
    elif (type_doc == "8K" or type_doc == "8KA"):
        loc_date1 = sec_txt.find("Date of Report (Date of Earliest Event Reported): ")
        loc_date2 = sec_txt.find("\n", loc_date1)
        date_end = removeNonAscii(sec_txt[loc_date1 + 50:loc_date2])
        if (loc_date1 == -1):
            loc_date1 = sec_txt.find("Date of Report (Date of earliest event reported):")
            loc_date2 = sec_txt.find("\n", loc_date1+56)
            date_end = removeNonAscii(sec_txt[loc_date1 + 51:loc_date2])
        if (loc_date1 == -1):
            loc_date1 = sec_txt.find("Date of report (Date of earliest event reported):")
            loc_date2 = sec_txt.find("\n", loc_date1)
            date_end = removeNonAscii(sec_txt[loc_date1 + 50:loc_date2])
        if (loc_date1 == -1):
            loc_date1 = sec_txt.find("Date of report (Date of earliest event reported) ")
            loc_date2 = sec_txt.find("\n", loc_date1+53)
            date_end = removeNonAscii(sec_txt[loc_date1 + 49:loc_date2])
        if (loc_date1 == -1):
            loc_date1 = sec_txt.find("Date of Report (date of earliest event reported): ")
            loc_date2 = sec_txt.find("\n", loc_date1)
            date_end = removeNonAscii(sec_txt[loc_date1 + 50:loc_date2])
        if (loc_date1 == -1):
            loc_date1 = sec_txt.find("Date of Report (Date of earliest event reported):")
            loc_date2 = sec_txt.find("\n", loc_date1+4)
            date_end = removeNonAscii(sec_txt[loc_date1 + 50:loc_date2])
            date_end = date_end.replace("/", " ")
        if (loc_date1 == -1):
            loc_date1 = sec_txt.find("Date of Report (Date of earliest event reported)")
            loc_date2 = sec_txt.find("\n", loc_date1+52)
            date_end = removeNonAscii(sec_txt[loc_date1 + 50:loc_date2])
        if (loc_date1 == -1 and getName(sec_txt)=="EMKR"):
            loc_date1 = sec_txt.rfind("Date of Report (Date of earliest event reported)")
            loc_date2 = sec_txt.rfind("\n", loc_date1+53)
            date_end = removeNonAscii(sec_txt[loc_date1+50:loc_date2])
        if (loc_date1 == -1 and getName(sec_txt) == "AAPL"):
            loc_date1 = sec_txt.find("1934")
            loc_date2 = sec_txt.rfind("Date of Report (Date of earliest event reported)", loc_date1)
            date_end = removeNonAscii(sec_txt[loc_date1 + 6:loc_date2 - 2])
        if (date_end.find("\n")!=-1):
            loc_date1 = sec_txt.find("THE SECURITIES EXCHANGE ACTOF 1934")
            loc_date2 = sec_txt.find("\n", loc_date1 + 40)
            date_end = removeNonAscii(sec_txt[loc_date1 + 36:loc_date2])
            if loc_date1 == -1:
                loc_date1 = sec_txt.find("THE SECURITIES EXCHANGE ACT OF 1934")
                loc_date2 = sec_txt.find("\n", loc_date1+40)
                date_end = removeNonAscii(sec_txt[loc_date1+37:loc_date2])
                if loc_date1 == -1:
                    loc_date1 = sec_txt.find("The Securities Exchange Act of 1934")
                    loc_date2 = sec_txt.find("\n", loc_date1 + 40)
                    date_end = removeNonAscii(sec_txt[loc_date1 + 37:loc_date2])
    date_end = date_end.replace("\n", "")
    if date_end.find(", ")!=-1:
        loc_date = date_end.find(", ") - 2
        date_end = date_end[0:loc_date] + " " + date_end[loc_date:len(date_end)]
        date_end = date_end[0:date_end.find(",")] + date_end[date_end.find(",") + 1:len(date_end)]
    #m = re.search("\d", date_end)
    #if date_end[m.start()-2:m.start()-1]!=" ":
        #date_end = date_end[0:date_end.find(" ")]+" "+date_end[date_end.find(" ")+1: date_end.find(" ")+2]+" "+date_end[date_end.find(" ")+3:]
        #print "hi"
    if date_end.find("Ma y")!=-1:
        loc1 = date_end.find("Ma y")
        date_end = date_end[0:loc1]+"May "+date_end[loc1+4:]
    if date_end.find("Jun e") != -1:
        loc1 = date_end.find("Jun e")
        date_end = date_end[0:loc1] + "June " + date_end[loc1 + 5:]
    if date_end.find("Novembe r") != -1:
        loc1 = date_end.find("Novembe r")
        date_end = date_end[0:loc1] + "November " + date_end[loc1 + 9:]
    if date_end.find("Februar y") != -1:
        loc1 = date_end.find("Februar y")
        date_end = date_end[0:loc1] + "February " + date_end[loc1 + 9:]
    if date_end.find("Octobe r") != -1:
        loc1 = date_end.find("Octobe r")
        date_end = date_end[0:loc1] + "October " + date_end[loc1 + 8:]
    if date_end.find("Decembe r") != -1:
        loc1 = date_end.find("Decembe r")
        date_end = date_end[0:loc1] + "December " + date_end[loc1 + 9:]
    if date_end.find("Januar y") != -1:
        loc1 = date_end.find("Januar y")
        date_end = date_end[0:loc1] + "January " + date_end[loc1 + 8:]
    if date_end.find("Augus t") != -1:
        loc1 = date_end.find("Augus t")
        date_end = date_end[0:loc1] + "August " + date_end[loc1 + 7:]
    if date_end.find("Jul y") != -1:
        loc1 = date_end.find("Jul y")
        date_end = date_end[0:loc1] + "July " + date_end[loc1 + 5:]
    if date_end.find("(")!=-1:
        loc1 = date_end.find("(")
        date1 = date_end[loc1:]
        m = re.search("\d", date1)
        loc_int = m.start()
        date1 = date1[0:loc_int]+" "+date1[loc_int:]
        print date1
        date_end = date_end[:loc1]+date1
    if date_end.find(" OR") != -1:
        date_end = date_end[0:len(date_end) - 3]
    date_end = date_end.replace("  ", " ")
    if len(date_end)>40:
        date_end = date_end[0:14]
        date_end = date_end[0:8]+" "+date_end[8:10]+" "+date_end[10:]
    if len(date_end)>40:
        print "DATE ERROR"
        return "DATE ERROR"
    date_end = date_end.replace("~", " ")
    date_end = date_end.replace(",", " ")
    date_end = date_end.replace("/", " ")
    locMonth = date_end.find(" ")
    date_end = date_end.replace(date_end[:locMonth], monthToNum(date_end[:locMonth]))
    return date_end

def getMD(sec_txt):
    txt_file = removeNonAscii(sec_txt)
    loc_m1 = txt_file.find("Item7. MANAGEMENTS DISCUSSION AND ANALYSIS", 40000)
    if (loc_m1 == -1):
        loc_m1 = txt_file.find("Item 7.Management's Discussion and Analysis of Financial Condition")
    if (loc_m1 == -1):
        loc_m1 = txt_file.find("Item7. Managements Discussion")
    if (loc_m1 == -1):
        loc_m1 = txt_file.find("Item7.Managements Discussion and Analysis", 40000)
    if (loc_m1 == -1):
        loc_m1 = txt_file.find("Item 2.Managements Discussion and Analysis", 40000)
    if (loc_m1 == -1):
        loc_m1 = txt_file.find("Item2. Managements Discussion", 40000)
    if (loc_m1 == -1):
        loc_m1 = txt_file.find("It em7. MANAGEMENTS DISCUSSION AND ANALYSIS")
    if (loc_m1 == -1):
        loc_m1 = txt_file.find("Item 7.Management's Discussion and Analysis")
    if (loc_m1 == -1):
        loc_m1 = txt_file.find("ITEM 7.Managements Discussion and Analysis of Financial")
    if (loc_m1 == -1):
        loc_m1 = txt_file.find("S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESU", 40000)
    if (loc_m1 == -1):
        loc_m1 = txt_file.find("Management's Discussion and Analysis of Financial Condition", 40000)
    if (loc_m1 == -1):
        loc_m1 = txt_file.find("Managements Discussion and Analysis",40000)
    if (loc_m1 == -1):
        loc_m1 = txt_file.find("DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION", 40000)
    if (loc_m1 == -1):
        loc_m1 = txt_file.find("Discussion and Analysis of Financial Condition", 40000)
    if (loc_m1 == -1):
        loc_m1 = txt_file.find("DISCUSSION AND ANALYSIS OF", 40000)
    if (loc_m1 == -1):
        loc_m1 = txt_file.find("FINANCIAL CONDITION AND RESULTS OF OPERATIONS", 40000)
    if (loc_m1 == -1):
        loc_m1 = txt_file.find("MANAGEMENTS DISCUSSION", 40000)
    if (loc_m1 == -1):
        loc_m1 = txt_file.find("S DISCUSSION AND ANALYSIS", 40000)
    if (loc_m1 == -1):
        loc_m1 = txt_file.find(". Management", 6000)
    if (loc_m1 == -1):
        loc_m1 = txt_file.find(".Management", 6000)
    if (loc_m1 == -1):
        loc_m1 = txt_file.find("Management's Discussion and Analysis", 6000)
    loc_m2 = txt_file.find("ITEM 3. QUANTITATIVE AND QUALITATIVE DISCLOSURES ", loc_m1)
    if (loc_m2 == -1):
        loc_m2 = txt_file.find("Item 7A. Quantitative and Qualitative", loc_m1)
    if (loc_m2 == -1):
        loc_m2 = txt_file.find("Item7A. Quantitative and Qualitative Disclosures", loc_m1)
    if (loc_m2 == -1):
        loc_m2 = txt_file.find("Item 7A.  Quantitative and Qualitative", loc_m1)
    if (loc_m2 == -1):
        loc_m2 = txt_file.find("ITEM 7A.Quantitative and Qualitative", loc_m1)
    if (loc_m2 == -1):
        loc_m2 = txt_file.find("Notes to Consolidated Financial Statements\n", loc_m1)
    if (loc_m2 == -1):
        loc_m2 = txt_file.find("NOTES TO CONSOLIDATED FINANCIAL STATEMENTS\n", loc_m1)
    if (loc_m2 == -1):
        loc_m2 = txt_file.find("Item8.Financial Statements and Supplementary Data", loc_m1)
    if (loc_m2 == -1):
        loc_m2 = txt_file.find("Controls and Procedures", loc_m1)
    if (loc_m2 == -1):
        loc_m2 = txt_file.find("CRITICAL AND SIGNIFICANT ACCOUNTING POLICIES", loc_m1)
    if (loc_m2 == -1):
        loc_m2 = txt_file.find("FORWARD-LOOKING STATEMENTS", loc_m1)
    if (loc_m2 == -1):
        loc_m2 = txt_file.find("QUANTITATIVE AND QUALITATIVE ", loc_m1+1000)
    if (loc_m2 == -1):
        loc_m2 = txt_file.find(". QUANTITATIVE", loc_m1+1000)
    if (loc_m2 == -1):
        loc_m2 = txt_file.find("STATEMENT OF MANAGEMENTS", loc_m1+1000)
    if (loc_m2 == -1):
        loc_m2 = txt_file.find("STATEMENT OF MANAGEMENTS RESPONSIBILITY FOR FINANCIAL STATEMENTS")
    if (loc_m2 == -1):
        loc_m2 = txt_file.find("Disclosures", loc_m1)
    if (loc_m2 == -1):
        loc_m2 = txt_file.find("We have operations both")
    if loc_m2-loc_m1<20000:
        loc_m1 = txt_file.find("Managements Discussion", loc_m1)
        if (loc_m1 == -1):
            loc_m1 = txt_file.find(". Management", loc_m1)
        if (loc_m1 == -1):
            loc_m1 = txt_file.find("MANAGEMENTS DISCUSSION", loc_m1)
        loc_m2 = txt_file.find(".Quantitative", loc_m1)
        if (loc_m2 == -1):
            loc_m2 = txt_file.find("ITEM 1A.  Risk Factors", loc_m1 + 1000)
        if (loc_m2 == -1):
            loc_m2 = txt_file.find("Disclosures", loc_m1)
        if (loc_m2 == -1):
            loc_m2 = txt_file.find(". QUANTITATIVE", loc_m1)
        if (loc_m2 == -1):
            loc_m2 = txt_file.find("STATEMENT OF MANAGEMENTS", loc_m1)
        if (loc_m2 == -1):
            loc_m2 = txt_file.find("STATEMENT OF MANAGEMENTS RESPONSIBILITY FOR FINANCIAL STATEMENTS")
    if txt_file.find("UNITED TECHNOLOGIES CORPORATION")!=-1 and str(typeDoc(sec_txt))=="10K":
        loc_m1 = txt_file.find("Management's Discussion and Analysis of Financial Condition and Results of Operations", 140000)
        loc_m2 = txt_file.find("Management's Report on Internal Control", loc_m1)
    mgmt_txt = txt_file[loc_m1:loc_m2]
    return mgmt_txt

def getNtF(sec_txt):
    loc1 = sec_txt.find("Notes to Consolidated Financial Statements\n")
    loc2 = sec_txt.find("Changes in and Disagreements with Accountants",loc1)
    if loc1 == -1:
        loc1 = sec_txt.find("Notes to Condensed Consolidated Financial Statements (Unaudited)\n")
        loc2 = sec_txt.find("Quantitative and Qualitative Disclosures", loc1)
    if loc1 == -1:
        loc1 = sec_txt.find("NOTES TO CONSOLIDATED FINANCIAL STATEMENTS\n")
        loc2 = sec_txt.find("SIGNATURES\n", loc1)
    if loc1 == -1:
        loc1 = sec_txt.find("NOTES TO CONDENSED CONSOLIDATED FINANCIAL STATEMENTS\n")
        loc2 = sec_txt.find("Discussion and Analysis of Financial Condition ", loc1)
    if loc1 == -1:
        loc1 = sec_txt.find("Notes to Consolidated Financial Statements\n")
        loc2 = sec_txt.find("Item 2.Management", loc1)
    if loc1 == -1:
        loc1 = sec_txt.find("NOTES TO FINANCIAL STATEMENTS\n")
        loc2 = sec_txt.find("DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION.", loc1)
    txt_file = sec_txt[loc1:loc2]
    return txt_file

def getRF(sec_txt):
    loc1 = sec_txt.find("1A.Risk Factors", 6000)
    if loc1 == -1:
        loc1 = sec_txt.find("RISK FACTORS\n")
    loc2 = sec_txt.find("1B.Unresolved Staff Comments", loc1)
    if loc2 == -1:
        loc2 = sec_txt.find("2.Unregistered Sales of Equity", loc1)
    if loc2 == -1:
        loc2 = sec_txt.find("UNRESOLVED STAFF COMMENTS", loc1)
    if loc2 == -1:
        loc2 = sec_txt.find("2.Unregistered Sales of Equity", loc1)
    if loc2 == -1:
        loc2 = sec_txt.find("UNREGISTERED SALES OF EQUITY", loc1)
    txt_file = sec_txt[loc1:loc2]
    return txt_file

def getBusiness(sec_txt):
    loc1 = sec_txt.find("1. BUSINESS", 4500)
    if loc1 == -1:
        loc1 = sec_txt.find("1.BusinessOverview", 4500)
    if loc1 == -1:
        loc1 = sec_txt.find("1. Business", 4500)
    if loc1 == -1:
        loc1 = sec_txt.find("1.BusinessCompany", 4500)
    if loc1 == -1:
        loc1 = sec_txt.find("Item 1.Business", 4500)
    if loc1 == -1:
        loc1 = sec_txt.find("1. BUSINESS", 4500)
    loc2 = sec_txt.find("1A.Risk Factors", loc1)
    if loc2 == -1:
        loc2 = sec_txt.find("RISK FACTORS")
    txt_file = sec_txt[loc1:loc2]
    return txt_file

def monthToNum(Month):
    return{
            'January': '1',
            'February': '2',
            'March': '3',
            'April': '4',
            'May': '5',
            'June': '6',
            'July': '7',
            'August': '8',
            'September': '9',
            'October': '10',
            'Ocbtober': '10',
            'November': '11',
            'December': '12',
            '05': '5'
    }[Month]

directory_test = 'F:\Dropbox\SEC Pipeline\SEC Filings Input'
directory_completed = 'F:\Dropbox\SEC Pipeline\SEC Filings Output'
problem = ""

def getTextOutput():  
    with open(directory_completed + '/SEC_metadata.csv', 'wb') as csv_file:
        field_names = ['doc_name', 'doc_title', 'doc_url', 'doc_date', 'date_adj', 'doc_source',
                       'doc_author_one', 'doc_org_one', 'doc_author_two', 'symbol', 'doc_city', 'doc_state', 'doc_country',
                       'doc_zipcode',
                       'doc_media_type', 'doc_date_fingerprinted', 'company_name']
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        def addCompInfo(name):
            if name == "AAPL":
                writer.writerow({'doc_city':'Cupertino', 'doc_state': 'CA', 'doc_country': 'USA', 'doc_zipcode': '95014',
                                 'doc_media_type': 'document', 'doc_date_fingerprinted': '7/12/2016', 'company_name':
                                     'APPLE INC'})
            elif name == "FB":
                writer.writerow(
                    {'doc_city': 'Menlo Park', 'doc_state': 'CA', 'doc_country': 'USA', 'doc_zipcode': '94025',
                     'doc_media_type': 'document', 'doc_date_fingerprinted': '7/12/2016', 'company_name':
                         'FACEBOOK INC'})
            elif name == "MSFT":
                writer.writerow(
                    {'doc_city': 'Redmond', 'doc_state': 'WA', 'doc_country': 'USA', 'doc_zipcode': '98052',
                     'doc_media_type': 'document', 'doc_date_fingerprinted': '7/12/2016', 'company_name':
                         'MICROSOFT CORP'})
            elif name == "GOOGL":
                writer.writerow(
                    {'doc_city': 'Mountain View', 'doc_state': 'CA', 'doc_country': 'USA', 'doc_zipcode': '94035',
                     'doc_media_type': 'document', 'doc_date_fingerprinted': '7/12/2016', 'company_name':
                         'ALPHABET INC.'})
            elif name == "NFLX":
                writer.writerow(
                    {'doc_city': 'Los Gatos', 'doc_state': 'CA', 'doc_country': 'USA', 'doc_zipcode': '95032',
                     'doc_media_type': 'document', 'doc_date_fingerprinted': '7/12/2016', 'company_name':
                         'NETFLIX INC'})
            elif name == "TWTR":
                writer.writerow(
                    {'doc_city': 'San Francisco', 'doc_state': 'CA', 'doc_country': 'USA', 'doc_zipcode': '94103',
                     'doc_media_type': 'document', 'doc_date_fingerprinted': '7/12/2016', 'company_name':
                         'TWITTER, INC.'})
        for idx,fn in enumerate(os.listdir(directory_test)):
            print idx
            print fn
            doc = Rtf15Reader.read(open(directory_test+"/"+fn))
            sec_txt = PlaintextWriter.write(doc).getvalue()
            type_doc = str(typeDoc(sec_txt))
            date_end = str(docDate(sec_txt, type_doc))
            date_end = date_end.replace("  ", " ")
            name = str(getName(sec_txt))
            sec_txt = sec_txt.replace("~", " ")
            doc_name = ""
            doc_name1 = ""
            doc_name2 = ""
            doc_name3 = ""
            if type_doc == "10K" or type_doc == "10Q":
                doc_name = directory_completed + "/" + name + " " + type_doc + " " + date_end + " MDA.txt"
                doc_name = doc_name.replace(" eptember", " September")
                doc_name = doc_name.replace("SSeptember", "September")
                doc_name = doc_name.replace("arch", "March")
                doc_name = doc_name.replace("MMarch", "March")
                doc_name1 = directory_completed + "/" + name + " " + type_doc + " " + date_end + " NTF.txt"
                doc_name1 = doc_name1.replace(" eptember", " September")
                doc_name1 = doc_name1.replace("SSeptember", "September")
                doc_name1 = doc_name1.replace("arch", "March")
                doc_name1 = doc_name1.replace("MMarch", "March")
                doc_name2 = directory_completed + "/" + name + " " + type_doc + " " + date_end + " RF.txt"
                doc_name2 = doc_name2.replace(" eptember", " September")
                doc_name2 = doc_name2.replace("SSeptember", "September")
                doc_name2 = doc_name2.replace("arch", "March")
                doc_name2 = doc_name2.replace("MMarch", "March")
                if os.path.isfile(doc_name):
                    doc_name = doc_name[:len(doc_name) - 4] + " 2nd.txt"
                if os.path.isfile(doc_name1):
                    doc_name1 = doc_name1[:len(doc_name1) - 4] + " 2nd.txt"
                if os.path.isfile(doc_name2):
                    doc_name2 = doc_name2[:len(doc_name2) - 4] + " 2nd.txt"
                sec_doc_MDA = open(doc_name, 'w+')
                sec_doc_NtF = open(doc_name1, 'w+')
                sec_doc_RF = open(doc_name2, 'w+')
                sec_doc_MDA.write(getMD(sec_txt))
                sec_doc_NtF.write(getNtF(sec_txt))
                sec_doc_RF.write(getRF(sec_txt))
                sec_doc_RF.close()
                sec_doc_MDA.close()
                sec_doc_NtF.close()
                if type_doc == "10K":
                    doc_name3 = directory_completed + "/" + name + " " + type_doc + " " + date_end + " BD.txt"
                    doc_name3 = doc_name3.replace(" eptember", " September")
                    doc_name3 = doc_name3.replace("SSeptember", "September")
                    doc_name3 = doc_name3.replace("arch", "March")
                    doc_name3 = doc_name3.replace("MMarch", "March")
                    if os.path.isfile(doc_name3):
                        doc_name3 = doc_name3[:len(doc_name3) - 4] + " 2nd.txt"
                    sec_doc_BD = open(doc_name3, 'w+')
                    sec_doc_BD.write(getBusiness(sec_txt))
                    sec_doc_BD.close()
                    writer.writerow(
                        {'doc_title': doc_name3[42:len(doc_name3) - 4], 'doc_date': date_end.replace(" ","-"), 'doc_source': 'SEC',
                         'doc_author_one': 'CFO', 'doc_org_one': name, 'doc_author_two': 'CEO', 'symbol': name})
                writer.writerow({'doc_title': doc_name[42:len(doc_name) - 4], 'doc_date': date_end.replace(" ","-"), 'doc_source': 'SEC',
                                     'doc_author_one': 'CFO', 'doc_org_one': name, 'doc_author_two': 'CEO', 'symbol': name})
                writer.writerow({'doc_title': doc_name1[42:len(doc_name1) - 4], 'doc_date': date_end.replace(" ","-"), 'doc_source': 'SEC',
                             'doc_author_one': 'CFO', 'doc_org_one': name, 'doc_author_two': 'CEO', 'symbol': name})
                writer.writerow({'doc_title': doc_name2[42:len(doc_name2) - 4], 'doc_date': date_end.replace(" ","-"), 'doc_source': 'SEC',
                                 'doc_author_one': 'CFO', 'doc_org_one': name, 'doc_author_two': 'CEO', 'symbol': name})
            elif type_doc == "10KA":
                doc_name = directory_completed + "/" + name + " " + type_doc + " " + date_end + ".txt"
                doc_name = doc_name.replace(" eptember", " September")
                doc_name = doc_name.replace("SSeptember", "September")
                doc_name = doc_name.replace("arch", "March")
                doc_name = doc_name.replace("MMarch", "March")
                if os.path.isfile(doc_name):
                    doc_name = doc_name[:len(doc_name) - 4] + " 2nd.txt"
                sec_doc = open(doc_name, 'w+')
                sec_doc.write(sec_txt)
                sec_doc.close()
                writer.writerow({'doc_title': doc_name[42:len(doc_name) - 4], 'doc_date': date_end.replace(" ","-"), 'doc_source': 'SEC',
                                 'doc_author_one': 'CFO', 'doc_org_one': name, 'doc_author_two': 'CEO', 'symbol': name})
            elif type_doc == "10QA":
                doc_name = directory_completed + "/" + name + " " + type_doc + " " + date_end + ".txt"
                doc_name = doc_name.replace(" eptember", " September")
                doc_name = doc_name.replace("SSeptember", "September")
                doc_name = doc_name.replace("arch", "March")
                doc_name = doc_name.replace("MMarch", "March")
                if os.path.isfile(doc_name):
                    doc_name = doc_name[:len(doc_name) - 4] + " 2nd.txt"
                sec_doc = open(doc_name, 'w+')
                sec_doc.write(sec_txt)
                sec_doc.close()
                writer.writerow({'doc_title': doc_name[42:len(doc_name) - 4], 'doc_date': date_end.replace(" ","-"), 'doc_source': 'SEC',
                                 'doc_author_one': 'CFO', 'doc_org_one': name, 'doc_author_two': 'CEO', 'symbol': name})
            elif type_doc == "8K" or type_doc == "8KA":

                doc_name = directory_completed + "/" + name + " " + type_doc + " " + date_end + ".txt"
                doc_name = doc_name.replace(" eptember", " September")
                doc_name = doc_name.replace("SSeptember", "September")
                doc_name = doc_name.replace("arch", "March")
                doc_name = doc_name.replace("MMarch", "March")
                if os.path.isfile(doc_name):
                    doc_name = doc_name[:len(doc_name) - 4] + " 2nd.txt"
                sec_doc = open(doc_name, 'w+')
                sec_doc.write(sec_txt)
                sec_doc.close()
                writer.writerow({'doc_title': doc_name[42:len(doc_name) - 4], 'doc_date': date_end.replace(" ","-"), 'doc_source': 'SEC',
                                 'doc_author_one': 'CFO', 'doc_org_one': name, 'doc_author_two': 'CEO', 'symbol': name})
        csv_file.close()
    print problem

getTextOutput()