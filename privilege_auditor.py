import requests
from bs4 import BeautifulSoup
import subprocess


url = "https://gtfobins.github.io/"


response = requests.get(url)
if response.status_code != 200:
    print(f"Error: Unable to fetch data from {url}. Status code: {response.status_code}")
    exit()


soup = BeautifulSoup(response.text, "html.parser")


binary_elements = soup.select("li a")  


binary_names = set()  
for element in binary_elements:
    href = element.get("href")  
    if href and href.startswith("/gtfobins/") and (href.endswith("/#suid") or href.endswith("/#limited-suid")): 
        parts = href.split("/")
        if len(parts) > 2:  
            binary_name = parts[2]  
            binary_names.add(binary_name)  
            
binary_names = list(binary_names)

command = [
    "find", "/", "-type", "f", "-perm", "-04000", "-exec", "basename", "{}", ";"
]

result = subprocess.run(command, capture_output=True, text=True)

suid_files = []

output = result.stdout.splitlines()
for line in output:
    suid_files.append(line)
    
common_values = set(binary_names) & set(suid_files)

print("\n".join(map(str, common_values)))
