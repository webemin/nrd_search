from encodings import utf_8
import string
from selenium import webdriver
from datetime import datetime, timedelta
import zipfile
import time
import os
import xml.etree.ElementTree as ET
import pandas
import pyautogui


def whoisds_domain_date_format(finded_date):
    whoisds_domains_discovered = finded_date
    y = int(whoisds_domains_discovered.split("-")[0])
    m = int(whoisds_domains_discovered.split("-")[1].replace("0", ""))
    d = int(whoisds_domains_discovered.split("-")[2])
    the_time = datetime(y, m, d)
    d = the_time - timedelta(days=1)
    return str(d).split(" ")[0]

def wait_until_download(path_for_download):
    while not os.path.exists(path_for_download):
        time.sleep(1)
    if os.path.isfile(path_for_download):
        return

def usom_search():
    giris = input("Usomun tarih değerleri varsayılan (dün ve bugün) olarak kalsın mı?(y/n)")
    if giris == "n":

        date1_i = input("Başlangıç Tarihini Giriniz (YIL-AY-GÜN): ")
        date1_data = date1_i.split("-")

        date2_i = input("Bitiş Tarihini Giriniz (YIL-AY-GÜN): ")
        dates2_data = date2_i.split("-")

        date1_using = datetime(int(date1_data[0]), int(date1_data[1]), int(date1_data[2]))
        date2_using = datetime(int(dates2_data[0]), int(dates2_data[1]), int(dates2_data[2]))
    else:
        date1_using = datetime.today() - timedelta(days=1)
        date2_using = datetime.today()

    conf_usom_asking = conf_str.split("\n")[1].split("=")[1]

    if conf_usom_asking == "y": usom_asking = True
    else: usom_asking = False

    browser = webdriver.Chrome(executable_path="./chromedriver.exe")
    browser.maximize_window()

    browser.get("https://www.usom.gov.tr/")

    browser.find_element_by_xpath("/html/body/app-root/app-layout/div/div/app-header/header/div/div[1]/div/div/nav[1]/ul/li[2]/a").click()

    time.sleep(2)

    if usom_asking:
        print("\nUsomdan dosya indirilirken uyarı veriyor olarak ayarlandı. Değiştirmek için conf dosyasını düzenleyiniz.")
        pyautogui.keyDown("shift")
        for i in range(14) :pyautogui.press("tab")
        pyautogui.keyUp("shift")
        pyautogui.press("enter")

    wait_until_download(conf_default_download_dir + "url-list.xml")

    tree = ET.parse(conf_default_download_dir + "url-list.xml")
    root = tree.getroot()

    date_rage = pandas.date_range(date1_using,date2_using,freq='d')

    print("\nBakılan Usom Tarihleri: ")
    for a in date_rage: print(str(a).split(" ")[0])
    print("\nAranan Keywordler: ")
    for b in keywords_a: print(str(b).split(" ")[0])
    print()

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

    browser = webdriver.Chrome(executable_path="./chromedriver.exe")
    browser.maximize_window()
    
    browser.get("https://www.whoisds.com/newly-registered-domains")

    whoisds_formated_date = whoisds_domain_date_format(browser.find_element_by_xpath("/html/body/div[2]/div/div/div/div/div[1]/div[2]/div/table/tbody/tr[1]/td[3]").text)
    path_to_zip_file = conf_default_download_dir+ "newly-registered-domains-" + whoisds_formated_date + ".zip"

    browser.find_element_by_xpath("/html/body/div[2]/div/div/div/div/div[1]/div[2]/div/table/tbody/tr[1]/td[4]/a/button").click()
    wait_until_download(path_to_zip_file)

    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall("./")

    whoisds_domains_f = open('domain-names.txt', 'r')
    whoisds_domains_l = whoisds_domains_f.readlines()

    whoisds_domains_str = ""

    for whoisds_domain in whoisds_domains_l:
        whoisds_domains_str+=whoisds_domain

    whoisds_domains_a = whoisds_domains_str.split("\n")
    
    if(not isUsom):
        print("\nAranan Keywordler: ")
        for b in keywords_a: print(str(b).split(" ")[0])
    print()

    whoisds_domains_f.close()
    return whoisds_domains_a
   
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

def chose_platform():
    isDevam = False
    isUsom = False
    isWhoisds = False
    isTypo = False

    def show_selected():
        if(isUsom): print("Usom Seçildi")
        if(isWhoisds): print("Whoisds Seçildi")
        if(isTypo): print("Typo Açık")

    while not isDevam:
        s1 = input("\nSeçim: ")
        if(s1 == "1"): isUsom = True
        elif(s1 == "-1"): isUsom = False
        elif(s1 == "2"): isWhoisds = True
        elif(s1 == "-2"): isWhoisds = False
        elif(s1 == "3"): isTypo = True
        elif(s1 == "-3"): isTypo = False
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


conf_str = file_to_str("./conf.txt")

keywords_str = file_to_str("./keywords.txt")
keywords_a = keywords_str.split("\n")

final_text = ""

conf_default_download_dir = conf_str.split("\n")[0].split("=")[1]

welcome_page()

isUsom, isWhoisds, isTypo = chose_platform()

print("\nİndirilenler Dizini: " + conf_default_download_dir)

if(isTypo):
    keywords_a = makeTypo(keywords_a)

if(isUsom):
    usom_domains_a = usom_search()
    usom_domains_a = list(set(usom_domains_a))
    
if(isWhoisds):
    whoisds_domains_a = whoisds_search()
    whoisds_domains_a = list(set(whoisds_domains_a))

for keyword in keywords_a:
    if(isWhoisds):
        for whoisds_domain in whoisds_domains_a:
            if keyword in whoisds_domain: 
                final_text += "Tarih: {:15} Domain: {:60} Keyword: {:15} Kaynak: Whoisds\n".format("Tarih Yok",whoisds_domain, keyword)
                print("Tarih: {:15} Domain: {:60} Keyword: {:15} Kaynak: Whoisds".format("Tarih Yok",whoisds_domain, keyword))
    if(isUsom):
        for usom_domain in usom_domains_a:
            if keyword in usom_domain: 
                final_text += "Tarih: {:15} Domain: {:60} Keyword: {:15} Kaynak: Usom\n".format(str(usom_domain).split("=")[0], str(usom_domain).split("=")[1], keyword)
                print("Tarih: {:15} Domain: {:60} Keyword: {:15} Kaynak: Usom".format(str(usom_domain).split("=")[0], str(usom_domain).split("=")[1], keyword))

final_text_f = open("result.txt", "w", encoding="utf-8")
final_text_f.write(final_text)
final_text_f.close()