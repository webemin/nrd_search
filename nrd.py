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

conf_f = open("./conf.txt", "r", encoding="utf8")
conf_l = conf_f.readlines()
conf_str = ""

for conf in conf_l:
    conf_str+=conf

conf_default_download_dir = conf_str.split("\n")[0].split("=")[1]

print(conf_default_download_dir)

#kullanıcıdan tarih girişi alınsın mı sorgusu
if input("Tarih varsayılan (dün ve bugün) olarak kalsın mı?(y/n)") == "n":

    date1_i = input("Başlangıç Tarihini Giriniz (YIL-AY-GÜN): ")
    date1_data = date1_i.split("-")

    date2_i = input("Bitiş Tarihini Giriniz (YIL-AY-GÜN): ")
    dates2_data = date2_i.split("-")

    date1_using = datetime(int(date1_data[0]), int(date1_data[1]), int(date1_data[2]))
    date2_using = datetime(int(dates2_data[0]), int(dates2_data[1]), int(dates2_data[2]))
else:
    date1_using = datetime.today() - timedelta(days=1)
    date2_using = datetime.today()

#kullanıcıdan oto enter sorgusu
conf_usom_asking = conf_str.split("\n")[1].split("=")[1]

if conf_usom_asking == "y": usom_asking = True
else: usom_asking = False

#webdriver ayarlama
browser = webdriver.Chrome(executable_path="./chromedriver.exe")
browser.maximize_window()

#whoisds işlemleri
browser.get("https://www.whoisds.com/newly-registered-domains")
whoisds_formated_date = whoisds_domain_date_format(browser.find_element_by_xpath("/html/body/div[2]/div/div/div/div/div[1]/div[2]/div/table/tbody/tr[1]/td[3]").text)
path_to_zip_file = conf_default_download_dir+ "newly-registered-domains-" + whoisds_formated_date + ".zip"

browser.find_element_by_xpath("/html/body/div[2]/div/div/div/div/div[1]/div[2]/div/table/tbody/tr[1]/td[4]/a/button").click()
wait_until_download(path_to_zip_file)

#usom işlemleri
browser.get("https://www.usom.gov.tr/")

#xml dosyasını indire basıp 10 saniye bekliyor
browser.find_element_by_xpath("/html/body/app-root/app-layout/div/div/app-header/header/div/div[1]/div/div/nav[1]/ul/li[2]/a").click()

time.sleep(2)

if usom_asking:
    print("\nUsomdan dosya indirilirken uyarı veriyor olarak ayarlandı. Değiştirmek için conf dosyasını düzenleyiniz.")
    pyautogui.keyDown("shift")
    for i in range(14) :pyautogui.press("tab")
    pyautogui.keyUp("shift")
    pyautogui.press("enter")

wait_until_download(conf_default_download_dir + "url-list.xml")

#whoisds zip dosyasını çıkarma
with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
    zip_ref.extractall("./")

#keyword listesini içeri alma
keywords_f = open('./keywords.txt', 'r')
keywords_l = keywords_f.readlines()

keywords_str = ""

for keyword in keywords_l:
    keywords_str+=keyword

#keywordler dizi haline getiriliyor 
keywords_a = keywords_str.split("\n")
keywords_a.pop()

#whoisds domainlerini okuma
whoisds_domains_f = open('domain-names.txt', 'r')
whoisds_domains_l = whoisds_domains_f.readlines()

whoisds_domains_str = ""

for whoisds_domain in whoisds_domains_l:
    whoisds_domains_str+=whoisds_domain

#whoisds domainleri dizi haline getiriliyor
whoisds_domains_a = whoisds_domains_str.split("\n")

#usom domainlerini okuma
tree = ET.parse(conf_default_download_dir + "url-list.xml")
root = tree.getroot()

date_rage = pandas.date_range(date1_using,date2_using,freq='d')

print("\nBakılan Tarihler: ")
for a in date_rage: print(str(a).split(" ")[0])
print("\nAranan Keywordler: ")
for b in keywords_a: print(str(b).split(" ")[0])

usom_domains_str = ""

index_of_date = 0
for index_of_date in range(len(date_rage)-1):
    index_of_usom = 0
    for index_of_usom in range(len(root[1])-1):
        if (root[1][index_of_usom][4].text).split(" ")[0] == str(date_rage[index_of_date]).split(" ")[0]:
            usom_domains_str += (root[1][index_of_usom][1].text + "\n")
        index_of_usom+=1
    index_of_date+=1

#usom domainleri dizi haline getiriliyor
usom_domains_a = usom_domains_str.split("\n")

final_text = ""

for keyword in keywords_a:
    final_text +="\n " +  "*"*10 + keyword + " keywordu " + "*"*10 + "\n\n"
    final_text +="\n " +  "-"*10 + "whoisds domain" + "-"*10 + "\n"
    for whoisds_domain in whoisds_domains_a:
        if keyword in whoisds_domain: final_text += whoisds_domain + "\n"
    final_text +="\n " +  "-"*10 + "usom domain" + "-"*10 + "\n"
    for usom_domain in usom_domains_a:
        if keyword in usom_domain: final_text += usom_domain + "\n"

final_text_f = open("result.txt", "a")

final_text_f.write(final_text)

final_text_f.close()
whoisds_domains_f.close()
keywords_f.close()