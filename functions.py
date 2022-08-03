from encodings import utf_8
from datetime import datetime, timedelta
from operator import index
import zipfile
import time
import os, shutil
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
import  urllib.request
import pandas as pd

def wait_until_download(path_for_download):
    while not os.path.exists(path_for_download):
        time.sleep(1)
    if os.path.isfile(path_for_download):
        return

def usom_search(isDefault, date1_i, date2_i, keywords_a):
    
    if isDefault == "interface": #replace with input if it gets interface parameter
        isDefault = input("Do you want usom's paramteters as deafult?(y/n)")

    if isDefault == "n":

        date1_i = input("From Date: (YYYY-MM-DD): ")
        date1_data = date1_i.split("-")

        date2_i = input("To Date (YYYY-MM-DD) [t: for today]: ")
        dates2_data = date2_i.split("-")

        date1_using = datetime(int(date1_data[0]), int(date1_data[1]), int(date1_data[2]))

        if(date2_i == "t"):
            date2_using = datetime.today() + timedelta(days=1)
        else:
            date2_using = datetime(int(dates2_data[0]), int(dates2_data[1]), int(dates2_data[2])) + timedelta(days=1)

    elif isDefault == "y":
        date1_using = datetime.today() - timedelta(days=1)
        date2_using = datetime.today() + timedelta(days=1)
    
    elif isDefault == "nn":
        date1_data = date1_i.split("-")
        dates2_data = date2_i.split("-")

        date1_using = datetime(int(date1_data[0]), int(date1_data[1]), int(date1_data[2]))

        if(date2_i == "t"):
            date2_using = datetime.today() + timedelta(days=1)
        else:
            date2_using = datetime(int(dates2_data[0]), int(dates2_data[1]), int(dates2_data[2])) + timedelta(days=1)
    
    elif isDefault == "yy":
        date1_using = date1_i
        date2_using = date2_i
    
    else:
        print("Wrong Enterence.")
        
    URL = "https://www.usom.gov.tr/url-list.xml"

    response = requests.get(URL)

    with open('./temp/url-list.xml', 'wb') as usom_f:
        usom_f.write(response.content)
    usom_f.close()
    
    wait_until_download("./temp/url-list.xml")

    tree = ET.parse("./temp/url-list.xml")
    root = tree.getroot()

    date_rage = pandas.date_range(date1_using,date2_using,freq='d')

    print("\nDates for Usom: ")
    for a in date_rage[:-1]: print(str(a).split(" ")[0])

    df_usom = pd.DataFrame(columns=['Date', 'Domain', 'Keyword', 'Source'])

    for keyword in keywords_a:
        for index_of_date in range(len(date_rage)-1):
            index_of_usom = 0
            for index_of_usom in range(len(root[1])-1):
                date_urllist = root[1][index_of_usom][4].text.split(" ")[0]
                date_for = str(date_rage[index_of_date]).split(" ")[0]
                if date_urllist == date_for:
                    domain = root[1][index_of_usom][1].text
                    date = date_urllist
                    if keyword in domain:
                        df_usom = pd.concat([df_usom, pd.DataFrame.from_records([{'Date': date, 'Domain': domain, 'Keyword': keyword, 'Source': 'Usom'}])])
                index_of_usom+=1
            index_of_date+=1
    
    df_usom = df_usom.drop_duplicates(subset='Domain', keep="first")

    return df_usom

def whoisds_search(keywords_a):

    whoisds_source_code = urllib.request.urlopen("https://www.whoisds.com/newly-registered-domains")
    soup = BeautifulSoup(whoisds_source_code, features="lxml")

    whoisds_links = []
    for link in soup.findAll('a'):
        if 'whois-database/newly-registered-domains' in link.get('href'):
            whoisds_links.append(link.get('href'))
    
    whoisds_dates = []
    for date in soup.findAll('td'):
        if "Only Domains" in str(date):
            whoisds_dates.append(str(date)[4:14])
    whoisds_date = whoisds_dates[0]

    whoisds_last_data_link = str(whoisds_links[0])
    r_wds = requests.get(whoisds_last_data_link, allow_redirects=True)
    open('./temp/whoisds.zip', 'wb').write(r_wds.content)

    wait_until_download("./temp/whoisds.zip")

    with zipfile.ZipFile("./temp/whoisds.zip", 'r') as zip_ref:
        zip_ref.extractall("./temp/")

    whoisds_domains_f = open('./temp/domain-names.txt', 'r')
    whoisds_domains_l = whoisds_domains_f.readlines()
    whoisds_domains_f.close()

    df_whoisds = pd.DataFrame(columns=['Date', 'Domain', 'Keyword', 'Source'])

    for keyword in keywords_a:
        for whoisds_domain in whoisds_domains_l:
            whoisds_domain = whoisds_domain[:-1]
            if keyword in whoisds_domain:
                df_whoisds = pd.concat([df_whoisds, pd.DataFrame.from_records([{'Date': whoisds_date, 'Domain': whoisds_domain, 'Keyword': keyword, 'Source': 'Whoisds'}])])
    
    df_whoisds = df_whoisds.drop_duplicates(subset='Domain', keep="first")

    return df_whoisds
   
def formatter(whoisds_domains_df, usom_domains_df):
    frames = [whoisds_domains_df, usom_domains_df]
    result = pd.concat(frames)
    print(result)
    result.to_excel("results.xlsx", index = False)  

def file_to_str(file_path):
    file_f = open(file_path, "r", encoding="utf8")
    file_l = file_f.readlines()
    file_str =""

    for file in file_l:
        file_str += file
    
    file_f.close()
    return file_str

def welcome_page():
    welcome = (""" 

    ███╗░░██╗██████╗░██████╗░░░░░░░░██████╗███████╗░█████╗░██████╗░░█████╗░██╗░░██╗
    ████╗░██║██╔══██╗██╔══██╗░░░░░░██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██║░░██║
    ██╔██╗██║██████╔╝██║░░██║█████╗╚█████╗░█████╗░░███████║██████╔╝██║░░╚═╝███████║
    ██║╚████║██╔══██╗██║░░██║╚════╝░╚═══██╗██╔══╝░░██╔══██║██╔══██╗██║░░██╗██╔══██║
    ██║░╚███║██║░░██║██████╔╝░░░░░░██████╔╝███████╗██║░░██║██║░░██║╚█████╔╝██║░░██║
    ╚═╝░░╚══╝╚═╝░░╚═╝╚═════╝░░░░░░░╚═════╝░╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝


    [1] USOM Search Active
    [2] WHOISDS Search Active 
    [3] Typo (maintenance)
    [4] Show Selected
    [5] Continue

    - to remove selection

    """)
    print(welcome)

def chose_platform(isDevam, isUsom, isWhoisds, isTypo):

    def show_selected():
        if(isUsom): print("Usom has selected")
        if(isWhoisds): print("Whoisds has selected")
        if(isTypo): print("Typo is turned on")

    while not isDevam:
        s1 = input("Chose: ")
        if(s1 == "1"):
            isUsom = True
            os.system('CLS')
            welcome_page()
            print("Usom is selected, select 5 to continue.")
        elif(s1 == "-1"): 
            isUsom = False
            os.system('CLS')
            welcome_page()
            print("Usom is unselected, select 5 to continue.")
        elif(s1 == "2"): 
            isWhoisds = True
            os.system('CLS')
            welcome_page()
            print("Whoisds is selected, select 5 to continue.")
        elif(s1 == "-2"): 
            isWhoisds = False
            os.system('CLS')
            welcome_page()
            print("Whoisds is unselected, select 5 to continue.")
        elif(s1 == "3"): 
            isTypo = True
            os.system('CLS')
            welcome_page()
            print("Typo is selected, select 5 to continue.")
        elif(s1 == "-3"): 
            isTypo = False
            os.system('CLS')
            welcome_page()
            print("Typo is unselected, select 5 to continue.")
        elif(s1 == "4"): show_selected()
        elif(s1 == "5"): isDevam = True
        else: print("Wrong Chose")
        
    return isUsom, isWhoisds, isTypo

def chose_typo():
    print("""
    Select typo types:

    [1] insertedKey
    [2] skipLetter
    [3] doubleLetter
    [4] reverseLetter
    [5] wrongVowel
    [6] wrongKey

    [7] Seçimler
    [8] Devam

    - ile seçimi silebilirsiniz.
    
    """)
    isInsertedKey = False
    isSkipLetter = False
    isDoubleLetter = False
    isReverseLetter = False
    isWrongVovel = False
    isWrongKey = False

    isDevam = False

    def show_selected():
        if(isInsertedKey): print("insertedKey Seçildi")
        if(isSkipLetter): print("skipLetter Seçildi")
        if(isDoubleLetter): print("doubleLetter Açık")
        if(isReverseLetter): print("reverseLetter Seçildi")
        if(isWrongVovel): print("wrongVowel Seçildi")
        if(isWrongKey): print("wrongKey Açık")

    while not isDevam:
        s1 = input("\nSeçim: ")
        if(s1 == "1"): isInsertedKey = True
        elif(s1 == "-1"): isInsertedKey = False
        elif(s1 == "2"): isSkipLetter = True
        elif(s1 == "-2"): isSkipLetter = False
        elif(s1 == "3"): isDoubleLetter = True
        elif(s1 == "-3"): isDoubleLetter = False
        elif(s1 == "4"): isReverseLetter = True
        elif(s1 == "-4"): isReverseLetter = False
        elif(s1 == "5"): isWrongVovel = True
        elif(s1 == "-5"): isWrongVovel = False
        elif(s1 == "6"): isWrongKey = True
        elif(s1 == "-6"): isWrongKey = False

        elif(s1 == "7"): show_selected()
        elif(s1 == "8"): isDevam = True
        else: print("Yanlış Seçim")
        
    return isInsertedKey, isSkipLetter, isDoubleLetter, isReverseLetter, isWrongVovel, isWrongKey

class TypoGenerator:

    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    vowels = "aeıioöuü"

    def insertedKey(k):
        kwds = []
        alphabet = TypoGenerator.alphabet

        for s in k:
            for i in range(0, len(s)):
                for char in alphabet:
                    kwds.append(s[:i+1] + char + s[i+1:])

        return kwds

    def skipLetter(k):
        kwds = []

        for s in k:
            for i in range(1, len(s)+1):
                kwds.append(s[:i-1] + s[i:])

        return kwds

    def doubleLetter(k):
        kwds = []
        for s in k:
            for i in range(0, len(s)+1):
                kwds.append(s[:i] + s[i-1] + s[i:])

        return kwds

    def reverseLetter(k):
        kwds = []
        for s in k:
            for i in range(0, len(s)):
                letters = s[i-1:i+1:1]
                if len(letters) != 2:
                    continue
            
                reverse_letters = letters[1] + letters[0]
                kwds.append(s[:i-1] + reverse_letters + s[i+1:])

        return kwds

    def wrongVowel(k):
        kwds = []
        vowels = TypoGenerator.vowels

        for s in k:
            for i in range(0, len(s)):
                for letter in vowels:
                    if s[i] in vowels:
                        for vowel in vowels:
                            s_list = list(s)
                            s_list[i] = vowel
                            kwd = "".join(s_list)
                            kwds.append(kwd)

        return kwds

    def wrongKey(k):
        kwds = []
        alphabet = TypoGenerator.alphabet

        for s in k:
            for i in range(0, len(s)):
                for letter in alphabet:
                    kwd = s[:i] + letter + s[i+1:]
                    kwds.append(kwd)
                
        return kwds

def makeTypo(keywords_a):
    isInsertedKey, isSkipLetter, isDoubleLetter, isReverseLetter, isWrongVovel, isWrongKey = chose_typo()
    keywords_ac = keywords_a

    if(isInsertedKey):
        a = input("devam")
        insertedkeys = TypoGenerator.insertedKey(keywords_ac)
        #keywords_a.append("\nINSERTED\n")
        for i in range(len(insertedkeys)):
            keywords_a.append(insertedkeys[i])

    if(isSkipLetter):
        a = input("devam")
        skipLetter = TypoGenerator.skipLetter(keywords_ac)
        #keywords_a.append("\nSKIPLETTER\n")
        for i in range(len(skipLetter)):
            keywords_a.append(skipLetter[i])

    if(isDoubleLetter):
        a = input("devam")
        doubleLetter = TypoGenerator.doubleLetter(keywords_ac)
        #keywords_a.append("\nDOUBLE\n")
        for i in range(len(doubleLetter)):
            keywords_a.append(doubleLetter[i])

    if(isReverseLetter):
        a = input("devam")
        reverseLetter = TypoGenerator.reverseLetter(keywords_ac)
        #keywords_a.append("\nREVERSE\n")
        for i in range(len(reverseLetter)):
            keywords_a.append(reverseLetter[i])
        
    if(isWrongVovel):
        a = input("devam")
        wrongVowel = TypoGenerator.wrongVowel(keywords_ac)
        #keywords_a.append("\nVowel\n")
        for i in range(len(wrongVowel)):
            keywords_a.append(wrongVowel[i])

    if(isWrongKey):
        a = input("devam")
        wrongKey = TypoGenerator.wrongKey(keywords_ac)
        #keywords_a.append("\nWRONGKEY\n")
        for i in range(len(wrongKey)):
            keywords_a.append(wrongKey[i])
    
    keywords_a = list(set(keywords_a))

    f = open("newkeywords.txt", "a", encoding="utf8")
    for i in range(len(keywords_a)):
        f.write(str(keywords_a[i]) + "\n")
    
    return keywords_a

def list_keywords(keywords_a):
    print("\nAranan Keywordler: ")
    for b in keywords_a:
        print(str(b).split(" ")[0])
        if b == '':
            keywords_a.pop()
    print()

def temp_cleaner():
    folder = './temp'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    
    open("./temp/temp","w")