import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

url = "https://companies-market-cap-copy.vercel.app/index.html"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

tables = soup.find_all("table")

if tables:
    table = tables[0]  
    rows = table.find_all("tr")

    data_list = []
    for row in rows:
        cols = row.find_all("td")
        cols = [col.text.strip() for col in cols]
        if cols:
            data_list.append(cols)

df = pd.DataFrame(data_list, columns = ["Year", "Revenue" ,"Change"])
df["Revenue"] = df["Revenue"].str.replace('[$B]', '', regex = True)
df["Change"] = df["Change"].str.replace('[%]', '', regex = True)
df = df.sort_values("Year")
df.to_csv("tesla_data.csv", index = False)

print(df)

#           #
#   SQL     #
#           #

conn = sqlite3.connect('tesla_data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS revenue (
               year TEXT,
               revenue REAL,
               change REAL
               )
''')

for num, row in df.iterrows():
    cursor.execute("INSERT INTO revenue (year, revenue, change) VALUES (?, ?, ?)", (row["Year"], row["Revenue"], row["Change"]))

conn.commit()
conn.close()

plt.figure(figsize=(10, 6))
plt.plot(df["Year"], df["Revenue"], marker = "o", label = "Revenue")
plt.title("Tesla annual revenue")
plt.xlabel("Date")
plt.ylabel("Revenue in billions (USD)")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)

plt.savefig("revenue_plot.png")
plt.show()
