from functions import *

def main():

    keywords_str = file_to_str("./keywords.txt")
    keywords_a = keywords_str.split("\n")
    whoisds_date = ""

    welcome_page()

    isUsom, isWhoisds, isTypo = chose_platform()

    if(isTypo): keywords_a = makeTypo(keywords_a)

    if(isUsom): usom_domains_a = usom_search() 
    else: usom_domains_a = []
        
    if(isWhoisds): whoisds_domains_a, whoisds_date = whoisds_search() 
    else: whoisds_domains_a = []
    
    list_keywords(keywords_a)

    formatter(keywords_a, isWhoisds, isUsom, whoisds_domains_a, usom_domains_a, whoisds_date)

    temp_cleaner()

main()
