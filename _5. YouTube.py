import re
import csv
from selenium import webdriver

filename = '5. Redactado.csv'

def get_first_video_id(keyword):
    base_url = "https://www.youtube.com/results?search_query="
    search_url = base_url + keyword
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.get(search_url)
    driver.implicitly_wait(10)
    html = driver.page_source
    driver.quit()
    video_id_match = re.search(r'/watch\?v=([^\&]+)', html)
    if video_id_match:
        return video_id_match.group(1)
    else:
        return None

with open(filename, mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    rows = list(reader)
    fieldnames = reader.fieldnames + ['Video']

for row in rows:
    keyword = row['Keywords'].split('\n')[0]
    video_id = get_first_video_id(keyword)
    print(video_id)
    if video_id:
        iframe_code = f'<center><iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></center>'
        row['Video'] = iframe_code
    else:
        row['Video'] = ''

with open(filename, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
