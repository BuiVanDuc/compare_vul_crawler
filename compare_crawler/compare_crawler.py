import time
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
from random import randint
from pip._vendor import requests

list_items_is_duplication = list()
# Read file
def read_file(file_name):
    path = file_name
    vul_file=open(path, 'r')
    content =vul_file.readlines()
    return content

# Get link not in acunetix
def get_link_not_in_acu(list_4web_crawler, list_acu_crawler, index_start, index_end,file_name):
    length=len(list_acu_crawler)
    for i in range(index_start, index_end):
        count=0
        link_4web= list_4web_crawler[i].strip()
        for acu_crawler in list_acu_crawler:
            link_acu = acu_crawler.strip()
            if link_4web== link_acu:
                list_items_is_duplication.append(link_acu)
                break
            else:
                count +=1
        if count ==length:
            url = link_4web
            status= get_link_status(url)
            data= url + '\t' + status +'\n'
            print('start write file: link_not_in_acunetix')
            write_file(file_name,data)
        time.sleep(1)

# Get link not in 4web:
def get_link_not_in_4web(list_items_is_duplication, list_acu_crawler):
    for acu_crawler in list_acu_crawler:
        link=acu_crawler.strip()
        if link not in list_items_is_duplication:
            url=link
            status = get_link_status(url)
            data =url + '\t' + status +'\n'
            print('start write file: link_not_in_4web')
            write_file('link_not_in_4web',data)
        time.sleep(1)

# Check status link:
def get_link_status(link):
    cnt = 0
    link_status = "N/A"
    while cnt <= 3:
        try:
            r = requests.get(link)
            return str(r.status_code)
        except Exception as ex:
            link_status = "Exception"
            pass
        cnt += 1
        time.sleep(randint(3, 9))
    return link_status
# read file:
def write_file(file_name, data):
    f= open(file_name+'.txt', 'a')
    f.write(data)
    f.close()

if __name__ == '__main__':
    list_4web_crawler= read_file('./report_crawler/4web_crawler.txt')
    list_acu_crawler = read_file('./report_crawler/acu_crawler.txt')
    length=len(list_4web_crawler)
    length_1=len(list_acu_crawler)
    with ThreadPoolExecutor(max_workers=3) as executor:
        task1= executor.submit(get_link_not_in_acu, list_4web_crawler, list_acu_crawler,0, length//2, 'lin_not_in_acu_1')
        task2 = executor.submit(get_link_not_in_acu, list_4web_crawler, list_acu_crawler,length//2, length, 'lin_not_in_acu_2')
    for i in as_completed([task1, task2]):
        pass
    get_link_not_in_4web(list_items_is_duplication,list_acu_crawler)
    #get_link_not_in_4web(list_acu_crawler, list_items_is_duplication)