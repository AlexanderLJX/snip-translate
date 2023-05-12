import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def save_proxies_to_file(proxies):
    with open("proxies.txt", "w") as f:
        for i, proxy in enumerate(proxies):
            if i == len(proxies) - 1:  # check if it's the last proxy in the list
                f.write(f"{proxy['IP']}:{proxy['Port']}")
            else:
                f.write(f"{proxy['IP']}:{proxy['Port']}\n")
        # for proxy in proxies:
        #     # time_delta = convert_to_timedelta(proxy['Last Checked'])
        #     # if time_delta < timedelta(minutes=9):
        #     #     print(proxy)
        #     #     f.write(f"{proxy['IP']}:{proxy['Port']}\n")
        #     f.write(f"{proxy['IP']}:{proxy['Port']}\n")

def convert_to_timedelta(value: str) -> timedelta:
    units = {'secs': 'seconds', 'sec': 'seconds', 'mins': 'minutes', 'min': 'minutes', 'hours': 'hours', 'hour': 'hours'}
    amount, unit, ago = value.split()
    return timedelta(**{units[unit]: int(amount)})

url = "https://free-proxy-list.net/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find the table containing the proxies
table = soup.find("table", {"class": "table"})

# Extract the rows with the 'Yes' column
rows = table.find_all("tr")[1:]  # Skip the header row

# Extract the proxy details and the 'Yes' column
proxies = []
for row in rows:
    columns = row.find_all("td")
    # print(columns)
    if len(columns) > 2:
        proxy = {
            "IP": columns[0].text,
            "Port": columns[1].text,
            "code": columns[2].text,
            "Country": columns[3].text,
            "Anonymity": columns[4].text,
            "Google": columns[5].text,
            "HTTPS": columns[6].text,
            "Last Checked": columns[7].text
        }
        proxies.append(proxy)

save_proxies_to_file(proxies)
