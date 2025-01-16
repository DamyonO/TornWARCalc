import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")

url = f"https://api.torn.com/v2/faction/chainreport?key={api_key}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
else:
    print(f"Failed to fetch data, status code: {response.status_code}")
    exit()

attackers_data = data.get('chainreport', {}).get('attackers', [])

if not attackers_data:
    print("No attackers data found.")
    exit()

attackers_stats = []
for attacker in attackers_data:
    attacker_id = attacker['id']
    response = requests.get(f'https://api.torn.com/user/{attacker_id}?selections=&key=64CGm7xYesFaRmHR')
    if response.status_code == 200:
        data = response.json()
    attacker_name = data.get('name', 'N/A')
    attacker_info = {
        'ID': attacker['id'],
        'Name': attacker_name,
        'Total Respect': attacker['respect']['total'],
        'Average Respect': attacker['respect']['average'],
        'Best Respect': attacker['respect']['best'],
        'Total Attacks': attacker['attacks']['total'],
        'Leave': attacker['attacks']['leave'],
        'Mug': attacker['attacks']['mug'],
        'Hospitalize': attacker['attacks']['hospitalize'],
        'Assists': attacker['attacks']['assists'],
        'Retaliations': attacker['attacks']['retaliations'],
        'Overseas': attacker['attacks']['overseas'],
        'Draws': attacker['attacks']['draws'],
        'Escapes': attacker['attacks']['escapes'],
        'Losses': attacker['attacks']['losses'],
        'War': attacker['attacks']['war'],
        'Bonuses': attacker['attacks']['bonuses']
    }
    attackers_stats.append(attacker_info)

df = pd.DataFrame(attackers_stats)

df.to_excel('attackers_stats.xlsx', index=False)

print("Data has been written to 'attackers_stats.xlsx'")
