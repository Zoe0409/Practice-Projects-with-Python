import sqlite3
from urllib.parse import urlparse
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

db_path = '/Users/Zoe/Library/Application Support/Google/Chrome/Default/History'
conn = sqlite3.connect(db_path)

sql = '''
select url 
from  urls where 
datetime(last_visit_time/1000000-11644473600,'unixepoch') 
> '2019-01-01'
'''
cursor = conn.execute(sql)

parser = lambda u: urlparse(u).netloc
history_dict = {}
for row in cursor:
    print(row[0])
    url = parser(row[0])
    history_dict.setdefault(url, 0)
    history_dict[url] += 1
    
    
history_lst = [(url, count) for url, count in history_dict.items()]
history_lst.sort(key=lambda item: item[1], reverse=True)

top_20_url = history_lst[:20]

pie_data = [item[1] for item in top_20_url]

pie_labels = [item[0] for item in top_20_url]

plt.figure(1, figsize=(10, 10))
plt.title('Top 20 most frequent browsing website')
plt.pie(pie_data, autopct='%1.1f%%', labels=pie_labels)
plt.savefig('./Top 20 most frequent browsing website.jpg')