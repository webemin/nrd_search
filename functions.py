from encodings import utf_8
from datetime import datetime, timedelta
import zipfile
import time
import os, shutil
import xml.etree.ElementTree as ET
import pandas
import requests
from bs4 import BeautifulSoup
import  urllib.request

def wait_until_download(path_for_download):
    while not os.path.exists(path_for_download):
        time.sleep(1)
    if os.path.isfile(path_for_download):
        return

def usom_search(isDefault, date1_i, date2_i):
    
    if isDefault == "interface": #eğer interfaceden alacaksak input ile değiştiriyoruz
        isDefault = input("Usomun tarih değerleri varsayılan (dün ve bugün) olarak kalsın mı?(y/n)")

    if isDefault == "n":

        date1_i = input("Başlangıç Tarihini Giriniz (YIL-AY-GÜN): ")
        date1_data = date1_i.split("-")

        date2_i = input("Bitiş Tarihini Giriniz (YIL-AY-GÜN) (t: bugünün tarihi): ")
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
        print("Yanlış Giriş")
        
    URL = "https://www.usom.gov.tr/url-list.xml"

    response = requests.get(URL)

    with open('./temp/url-list.xml', 'wb') as usom_f:
        usom_f.write(response.content)
    usom_f.close()
    
    wait_until_download("./temp/url-list.xml")

    tree = ET.parse("./temp/url-list.xml")
    root = tree.getroot()

    date_rage = pandas.date_range(date1_using,date2_using,freq='d')

    print("\nBakılan Usom Tarihleri: ")
    for a in date_rage[:-1]: print(str(a).split(" ")[0])

    usom_domains_str = ""

    for index_of_date in range(len(date_rage)-1):
        index_of_usom = 0
        for index_of_usom in range(len(root[1])-1):
            if (root[1][index_of_usom][4].text).split(" ")[0] == str(date_rage[index_of_date]).split(" ")[0]:
                usom_domains_str += root[1][index_of_usom][4].text.split(" ")[0] + "=" + (root[1][index_of_usom][1].text + "\n")
            index_of_usom+=1
        index_of_date+=1

    usom_domains_a = usom_domains_str.split("\n")
    return usom_domains_a

def whoisds_search():

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

    whoisds_domains_str = ""

    for whoisds_domain in whoisds_domains_l:
        whoisds_domains_str+=whoisds_domain

    whoisds_domains_a = whoisds_domains_str.split("\n")

    whoisds_domains_f.close()
    return whoisds_domains_a, whoisds_date
   
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


    [1] USOM
    [2] WHOISDS
    [3] Typo (bakımda)
    [4] Show Selected
    [5] Devam

    - ile seçimi silebilirsiniz.

    """)
    print(welcome)

def chose_platform(isDevam, isUsom, isWhoisds, isTypo):

    def show_selected():
        if(isUsom): print("Usom Seçildi")
        if(isWhoisds): print("Whoisds Seçildi")
        if(isTypo): print("Typo Açık")

    while not isDevam:
        s1 = input("\nSeçim: ")
        if(s1 == "1"):
            isUsom = True
            print("Usom Seçildi, devam etmek için Devam'ı seçiniz.")
        elif(s1 == "-1"): 
            isUsom = False
            print("Usom Devredışı, devam etmek için Devam'ı seçiniz.")
        elif(s1 == "2"): 
            isWhoisds = True
            print("Whoisds Seçildi, devam etmek için Devam'ı seçiniz.")
        elif(s1 == "-2"): 
            isWhoisds = False
            print("Whoisds Devredışı, devam etmek için Devam'ı seçiniz.")
        elif(s1 == "3"): 
            isTypo = True
            print("Typo Seçildi, devam etmek için Devam'ı seçiniz.")
        elif(s1 == "-3"): 
            isTypo = False
            print("Typo Devredışı, devam etmek için Devam'ı seçiniz.")
        elif(s1 == "4"): show_selected()
        elif(s1 == "5"): isDevam = True
        else: print("Yanlış Seçim")
        
    return isUsom, isWhoisds, isTypo

def chose_typo():
    print("""
    Uygulanmasını İstediğiniz Typoları Seçiniz:

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

def formatter(keywords_a, isWhoisds, isUsom, whoisds_domains_a, usom_domains_a, whoisds_date):
    
    whoisds_domain_dd = []
    usom_domain_dd = []
    final_text = ""

    for keyword in keywords_a:
        if(isWhoisds):
            for whoisds_domain in whoisds_domains_a:
                if keyword in whoisds_domain and whoisds_domain not in whoisds_domain_dd:
                    final_text += "Tarih: {:15} Domain: {:60} Keyword: {:15} Kaynak: Whoisds\n".format(whoisds_date, whoisds_domain, keyword)
                    whoisds_domain_dd.append(whoisds_domain)
        if(isUsom):
            for usom_domain in usom_domains_a:
                if keyword in usom_domain and usom_domain not in usom_domain_dd: 
                    final_text += "Tarih: {:15} Domain: {:60} Keyword: {:15} Kaynak: Usom\n".format(str(usom_domain).split("=")[0], str(usom_domain).split("=")[1], keyword)
                    usom_domain_dd.append(usom_domain)

    final_text_a = final_text.split("\n")
    final_text_a.sort()

    final_text_s = ""
    for i in final_text_a:
        final_text_s += i + "\n"

    print(final_text_s)

    final_text_f = open("result.txt", "w", encoding="utf-8")
    final_text_f.write(final_text_s)
    final_text_f.close()

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