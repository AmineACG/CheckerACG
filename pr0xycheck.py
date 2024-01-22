import requests
from concurrent.futures import ThreadPoolExecutor
#THIS IS AMAZING TO CHECK IF PROXIES FROM THE INTERNET ARE WORKING AND TO SEPERATE THEM BEFORE MAKING A DOS
def test_proxy(proxy):
    url = 'http://www.example.com'
    #it uses thread also
    try:
        response = requests.get(url, proxies={'http': proxy, 'https': proxy}, timeout=10)
        if response.status_code == 200:
            print(f"Proxy {proxy} is working.")
            with open("working_proxies.txt", "a") as file:
                file.write(proxy + '\n')  
            return True
        else:
            print(f"Proxy {proxy} returned status code {response.status_code}.")
    except Exception as e:
        print(f"Failed with proxy {proxy}")

    return False

def test_proxies_from_file(file_path):
    with open(file_path, 'r') as file:
        proxies = file.read().splitlines()

    with ThreadPoolExecutor(max_workers=10) as executor:  
        executor.map(test_proxy, proxies)

file_path = 'http_proxies.txt'
test_proxies_from_file(file_path)
