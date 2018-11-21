import json
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.pool import ThreadPool
import time
# Read file and return list
def read_file(file_name):
    path = file_name
    vul_file=open(path, 'r')
    content =vul_file.readlines()
    item=dict()
    list_vul =list()

    # Oupt is list_items, item: {item['sub']:'/svn/tags/Mars_v2.3/Changelog', item['id_verity']: 3, item['name_vul]:'Log file', item['id_name_vul']:480}
    length = len(content)
    for i in range(length):
        list_items = list(content[i].split(','))
        #print(list_items)
        # cut 'https:' or 'http:' from url
        if 'https://' in list_items[0]:
            domain =list_items[0].replace('https://','')
        else:
            domain = list_items[0].replace('http://','')
        index =domain.find('/')
        directory =domain[index:]
        item['url']=list_items[0]
        item['sub_url']=directory
        item['method'] =list_items[1].strip()
        item['id_verity']=int(list_items[4][0])
        item['vul_name'] =list_items[3]
        item['param']=list_items[2].strip()
        item_tem=item.copy()
        #print(item_tem)
        list_vul.append(item_tem)
    return list_vul

def compare_vul(list_vul_4web, list_vul_acunetix):
    # compare critical_vul:
    lenth_2=len(list_vul_acunetix)
    list_items_is_duplication=list()
    for vul_4web in list_vul_4web:
        number = 0
        for vul_acu in list_vul_acunetix:
            if vul_4web['sub_url'] not in vul_acu['sub_url']:
                number+=1
            else:
                if vul_4web['param'] == vul_acu['param'] and vul_4web['method'] == vul_acu['method']:
                    # Write file to vul_not_in_4web:
                    list_items_is_duplication.append(vul_4web)
                else:
                    number+=1
        if number == lenth_2:
            data = vul_4web['vul_name'] + "\t" + vul_4web['url'] + "\t" +vul_4web['method']+"\t"+ vul_4web[
                'param'] + "\t" + str(vul_4web['id_verity']) + '\n'
            print('STRART WRITE FILE: vul_not_in_acunetix')
            print(data)
            write_file('vul_not_in_acunetix', data)
        time.sleep(2)

    # Write file to vul_not_in_acunetix:
    for vul_acu in list_vul_acunetix:
        if vul_acu not in list_items_is_duplication:
            data = vul_acu['vul_name'] + "\t" + vul_acu['url'] + "\t" + vul_acu['method']+"\t"+ vul_acu[
            'param'] + "\t" + str(vul_acu['id_verity']) + '\n'
            print('STRART WRITE FILE: vul_not_in_4web')
            print(data)
            write_file('vul_not_in_4web', data)
        time.sleep(2)

def write_file(file_name, data):
    f= open(file_name+'.txt', 'a')
    f.write(data)
    f.close()
if __name__ == '__main__':
    list_vul_4web=read_file('./report/vul_4web.txt')
    list_vul_acunetix=read_file('./report/vul_acunetix.txt')
    compare_vul(list_vul_4web, list_vul_acunetix)