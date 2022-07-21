from warnings import catch_warnings
from functions import *
import sys

def main():

    keywords_str = file_to_str("./keywords.txt")
    keywords_a = keywords_str.split("\n")
    whoisds_date = ""
    usom_domains_a = []
    whoisds_domains_a = []

    if(len(sys.argv) == 1):

        welcome_page()
        isUsom, isWhoisds, isTypo = chose_platform(False, False, False, False)
        if(isTypo): keywords_a = makeTypo(keywords_a)

        if(isUsom): usom_domains_a = usom_search("interface", "interface", "interface") #veriler arayüzden değişecek
            
        if(isWhoisds): whoisds_domains_a, whoisds_date = whoisds_search() 
    
    else:
        if "-u" in sys.argv: isUsom = True #usom açılsın parametresi
        else: isUsom = False

        if "-w" in sys.argv: isWhoisds = True #whoisds açılsın parametresi
        else: isWhoisds = False

        if "-t" in sys.argv: isTypo = True #typo açılsın parametresi
        else: isTypo = False

        if(isUsom):
            if "-udd" in sys.argv: #tarihler varsayılan kalsın
                innum = sys.argv.index("-udd")
                usom_domains_a = usom_search("yy", datetime.today() - timedelta(days=1), datetime.today() + timedelta(days=1))
            elif "-udnd" in sys.argv: #tarihler varsayalın değilse
                innum = sys.argv.index("-udnd")
                date1_innum = innum + 1
                date2_innum = innum + 2

                print(date1_innum)
                print(sys.argv[date1_innum])
                print(sys.argv[date2_innum])
                try:
                    usom_domains_a = usom_search("nn", sys.argv[date1_innum], sys.argv[date2_innum])
                
                except:
                    print("udnd parametresi kullandığınız için tarih aralığı bekleniyor. Format: YIL-AY-GÜN")
                    return 
            else:
                print("Usom araması için tercih yapınız. -udd varsayılan tarihlerde arama yapmak için, -udnd tarih1 tarih2 belli tarih aralığında arama yapmak için")
                return

        if(isWhoisds): whoisds_domains_a, whoisds_date = whoisds_search() 
                      
        
    
    list_keywords(keywords_a)

    formatter(keywords_a, isWhoisds, isUsom, whoisds_domains_a, usom_domains_a, whoisds_date)

    temp_cleaner()

main()
