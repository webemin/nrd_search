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
                usom_domains_str += "Tarih: " + root[1][index_of_usom][4].text.split(" ")[0] + "  Domain: " + (root[1][index_of_usom][1].text + "\n")
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
    [3] DEVAM

    - ile seçimi silebilirsiniz.

    """)
    print(welcome)

def chose_platform():
    isDevam = False
    isUsom = False
    isWhoisds = False

    def show_selected():
        if(isUsom): print("Usom Seçildi\n")
        if(isWhoisds): print("Whoisds Seçildi\n")

    while not isDevam:
        s1 = input("Seçim: ")
        print()
        if(s1 == "1"):
            isUsom = True
            show_selected()
        elif(s1 == "2"):
            isWhoisds = True
            show_selected()
        elif(s1 == "-1"):
            isUsom = False
            show_selected()
        elif(s1 == "-2"):
            isWhoisds = False
            show_selected()
        elif(s1 == "3"):
            isDevam = True
            show_selected()
        else:
            print("Yanlış Seçim")
        
    return isDevam, isUsom, isWhoisds


conf_str = file_to_str("./conf.txt")

keywords_str = file_to_str("./keywords.txt")
keywords_a = keywords_str.split("\n")

final_text = ""

conf_default_download_dir = conf_str.split("\n")[0].split("=")[1]

welcome_page()

isDevam ,isUsom, isWhoisds = chose_platform()

print("İndirilenler Dizini: " + conf_default_download_dir)

if(isUsom):
    usom_domains_a = usom_search()
    
if(isWhoisds):
    whoisds_domains_a = whoisds_search()

for keyword in keywords_a:
    final_text +="\n " +  "*"*10 + keyword + " keywordu " + "*"*10 + "\n\n"
    print("\n " +  "*"*10 + keyword + " keywordu " + "*"*10 + "\n\n")
    if(isWhoisds):
        final_text +="\n " +  "-"*10 + "whoisds domain" + "-"*10 + "\n"
        print("\n " +  "-"*10 + "whoisds domain" + "-"*10 + "\n")
        for whoisds_domain in whoisds_domains_a:
            if keyword in whoisds_domain: 
                final_text += whoisds_domain + "\n"
                print(whoisds_domain)
    if(isUsom):
        final_text +="\n " +  "-"*10 + "usom domain" + "-"*10 + "\n"
        print("\n " +  "-"*10 + "usom domain" + "-"*10 + "\n")
        for usom_domain in usom_domains_a:
            if keyword in usom_domain: 
                final_text += usom_domain + "\n"
                print(usom_domain)

final_text_f = open("result.txt", "w")
final_text_f.write(final_text)
final_text_f.close()