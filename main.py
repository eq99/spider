import csv
import json
import requests
from collections import deque
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_proxy(proxy_server='http://118.24.52.95/get/'):
    proxy = json.loads(requests.get(proxy_server).text)['proxy']
    print(f'{datetime.now()} Proxy {proxy}')
    return proxy



def get_book_infos(url):
    options = Options()
    options.headless = True
    options.add_argument('--window-size=1920,1200')
    # options.add_argument(f'--proxy-server={get_proxy()}')
    driver = webdriver.Chrome(options=options, executable_path=r'/usr/local/bin/chromedriver')
    driver.get(url)
    print(f'{datetime.now()} Get {url}')

    name = driver.find_element_by_xpath('//*[@id="wrapper"]/h1/span').text
    rate = driver.find_element_by_xpath('//*[@id="interest_sectl"]/div/div[2]/strong').text or 0
    
    try:
        num_rate_people = driver.find_element_by_xpath('//*[@id="interest_sectl"]/div/div[2]/div/div[2]/span/a/span').text 
    except:
        num_rate_people = 0
    
    try:
        num_comment = driver.find_element_by_xpath('//*[@id="comments-section"]/div[1]/h2/span[2]/a').text.split(' ')[1] 
    except:
        num_comment = 0
    
    try:
        num_read_people = driver.find_element_by_xpath('//*[@id="collector"]/p[2]/a').text[:-3]
    except:
        num_read_people = 0
    
    # extract links
    link_elements = driver.find_elements_by_xpath('//*[@id="db-rec-section"]/div/dl/dd/a')
    links=[]
    for link in link_elements:
        links.append(link.get_attribute('href'))

    driver.quit()

    return {
        'name': name,
        'rate': rate,
        'num_rate_people': num_rate_people,
        'num_comment': num_comment,
        'num_read_people': num_read_people,
        'links': links
    }



def store_book_infos(link, infos):
    with open('./book_infos.csv', mode='a') as csv_file:
        fieldnames = ['Rate', 'Num_Rate_People', 'Num_Comment', 'Num_Read_People', 'Link', 'Name']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        #writer.writeheader()
        writer.writerow({
            'Rate': infos['rate'],
            'Num_Rate_People': infos['num_rate_people'],
            'Num_Comment': infos['num_comment'],
            'Num_Read_People': infos['num_read_people'],
            'Link': link,
            'Name': infos['name']
        })



def spider(link_maxsize=1000, seed_link='https://book.douban.com/subject/25779298/'):
    closed_links = set()
    open_links = deque([seed_link])
    
    while open_links:
        # pick one link from links_list
        current_link = open_links.popleft()
        if current_link in closed_links:
            continue
        # get info for link
        infos = get_book_infos(current_link)
        # store link info for link
        store_book_infos(current_link, infos)
        # update link.links in link_list and links_set: list_maxsize:1000
        for link in infos['links']:
            if (link not in closed_links) and (len(open_links) <= link_maxsize):
                open_links.append(link)
        # add cuurent link to closed links
        closed_links.update({current_link})
        print(f'list_size: {len(open_links)}')
        print(f'set_size: {len(closed_links)}')

if __name__ == '__main__':
    spider()
