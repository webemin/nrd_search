# nrd_search
This script searches input keywords in new registered domains downloaded from usom and whoisds domains.
------
# Usage
- cd nrd_search
- Append keywords to keywords.txt file
- pip install -r requirements.txt
- ptyhon nrd.py
------
# Parameters
- -u searches given keywords in the public database from www.usom.gov.tr

- [--dates] [YYYY-MM-DD] [YYYY-MM-DD or -t(it is the shortcut for today's date)] After -u parameter to search between specific 
dates in usom's database. By default it searches from yesterday to today.
        
- -w searches given keywords in the public database from www.whoisds.com
        
- -t applies typo to given keywords.
------ 

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

------
note: Typo is not available for now
