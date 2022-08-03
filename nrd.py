from functions import *
import sys

def main():

    keywords_str = file_to_str("./keywords.txt")
    keywords_a = keywords_str.split("\n")
    df_s = pd.DataFrame(columns=['Date', 'Domain', 'Keyword', 'Source'])
    whoisds_domains_df, usom_domains_df = df_s,df_s

    if(len(sys.argv) == 1):

        welcome_page()
        isUsom, isWhoisds, isTypo = chose_platform(False, False, False, False)
        if(isTypo): print("In progress")#keywords_a = makeTypo(keywords_a)

        if(isUsom): usom_domains_df = usom_search("interface", "interface", "interface", keywords_a) #data will change from interface
            
        if(isWhoisds): whoisds_domains_df = whoisds_search(keywords_a)
    
    if(len(sys.argv) == 2 and sys.argv[2] == '-h'):
        print("""
        -u searches given keywords in the public database from www.usom.gov.tr

        [--dates] [YYYY-MM-DD] [YYYY-MM-DD or -t(it is the shortcut for today's date)] After -u parameter to search between specific 
        dates in usom's database. By default it searches from yesterday to today.
        
        -w searches given keywords in the public database from www.whoisds.com
        
        -t applies typo to given keywords.
        """)
    
    elif(len(sys.argv) >= 2 and len(sys.argv) <= 6):
        if "-u" in sys.argv: isUsom = True #turn on usom parameter
        else: isUsom = False

        if "-w" in sys.argv: isWhoisds = True #turn on whoisds parameter
        else: isWhoisds = False

        if "-t" in sys.argv: isTypo = True #turn on typo parameter
        else: isTypo = False

        if(isUsom):
            if "--dates" in sys.argv: #if user want to enter specific dates
                innum = sys.argv.index("--dates")
                date1_innum = innum + 1
                date2_innum = innum + 2

                print(date1_innum)
                print(sys.argv[date1_innum])
                print(sys.argv[date2_innum])
                try:
                    usom_domains_df = usom_search("nn", sys.argv[date1_innum], sys.argv[date2_innum], keywords_a)
                
                except:
                    print("2 dates are expected due to --dates parameter. Format: YYY-MM-DD")
                    return 
            
            else:
                usom_domains_df = usom_search("yy", datetime.today() - timedelta(days=1), datetime.today() + timedelta(days=1), keywords_a)

        if(isWhoisds): whoisds_domains_df = whoisds_search(keywords_a)

        else: print("Parameters are expected. -h to see help")
    
    else: print("Too many arguments. -h to see help")                  
            
    list_keywords(keywords_a)

    formatter(whoisds_domains_df, usom_domains_df)

    #temp_cleaner()

if __name__ == '__main__':
    main()