# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# 爬 TaiBIF 的物種出現資料
# =====================
# 
# 目標：
# -----
# 
# 1. 取得物種出現的點位座標
# 2. 整理成 database format (sqlite/postgresql)
# 
# http://www.taibif.tw/zh/catalogue_of_life/page/68f1-445a-9d08-41b0-95dc-1fed-d1ae-74da-namecode-204881
#         

# <codecell>

from IPython.core.display import Image
# 物種名錄的結構
Image(filename='img/taibif_occ_rec.png', height=200, width=600) 

# <codecell>

# 物種記錄的表格
Image(filename='img/occ_records.png', width=600)

# <markdowncell>

# 流程：
# -----
# 
# 1. 研究物種搜尋的 search POST 如何運作
# 2. 使用 lxml 來 parse
#     1. 取得個別物種的頁面
#     2. 取得所有頁面

# <codecell>

# use lxml to parse html
from lxml import *
from numpy import array,reshape,vstack
import csv
import time
import sys


# define variables
site_base = 'http://www.taibif.tw'
catalog_path = '/zh/catalogue_of_life/page'

# 取得物種編碼及座標
def get_spcoord(url, site_base='http://www.taibif.tw'):
    parsed_html = html.parse(url)
    # 取得物種個別記錄的 url
    record_url = []
    global record_list
    record_list = []
    global coor_out
    for row in parsed_html.xpath('//table[@class="views-table cols-7"]//tr//td//a[@href]'):
        record_url.append(row.attrib['href'])
        #print('Parsing ' + site_base + row.attrib['href'])
        rpg = html.parse(site_base + row.attrib['href'])
        
        # get coordinate
        code = 'div[@class="views-field views-field-solr-document-1"]'
        lon_div = 'div[@class="views-field views-field-Longitude-t"]'
        span_con = 'span[@class="field-content"]'
        lon_tag = '//'+lon_div+'//'+span_con
        lat_div = 'div[@class="views-field views-field-Latitude-t"]'
        lat_tag = '//'+lat_div+'//'+span_con
        code_tag = '//'+code+'//'+span_con
        for row in rpg.xpath(code_tag)+rpg.xpath(lon_tag)+rpg.xpath(lat_tag):
            record_list.append(row.text)
    coor_out = reshape(record_list, (len(record_list)/3,3))
            
# 取得最後一頁的頁數
def get_lastpage(url):
    parsed_html = html.parse(url)
    for row in parsed_html.xpath('//li[@class="pager-last last"]//a'):
        last_pg_num = row.attrib['href'].split('?page=')[1]
        print('The last page number is ' + last_pg_num)
        return(int(last_pg_num))
    
# 輸出資料為 csv 檔案
def export_csv(filename, output):
    with open(filename, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerows(output)

# <codecell>

# Trema orientalis
lpg_num = int(get_lastpage(url))
foutput = array(['biocode','longitude','latitude'])
for i in xrange(0, lpg_num):
    num = i+1
    url_str = url+'?page='+str(num)
    get_spcoord(url_str)
    foutput = vstack((foutput, coor_out))
print('Finished!')
export_csv("Trema_orientalis.csv", foutput)

# <codecell>

# Cinnamomum kanehirae
url = 'http://www.taibif.tw/zh/catalogue_of_life/page/dbd4-aa5a-4949-397e-fb99-478e-6c5b-0985-namecode-203595'
lpg_num = int(get_lastpage(url))
foutput = array(['biocode','longitude','latitude'])
for i in xrange(0, lpg_num):
    num = i+1
    url_str = url+'?page='+str(num)
    get_spcoord(url_str)
    foutput = vstack((foutput, coor_out))
print('Finished!')
export_csv("Cinnamomum_kanehirae.csv", foutput)

# <codecell>

# Taiwania cryptomerioides
url = 'http://www.taibif.tw/zh/catalogue_of_life/page/62da-3460-4adb-eb13-8280-7284-947b-ecb8-namecode-201121'
lpg_num = int(get_lastpage(url))
foutput = array(['biocode','longitude','latitude'])
for i in xrange(0, lpg_num):
    num = i+1
    url_str = url+'?page='+str(num)
    get_spcoord(url_str)
    foutput = vstack((foutput, coor_out))
print('Finished!')
export_csv("Taiwania_cryptomerioides.csv", foutput)

# <codecell>

# Trochodendron aralioides
url = 'http://www.taibif.tw/zh/catalogue_of_life/page/88fa-6d78-3fab-ce7c-0568-85af-969d-4d1f-namecode-204821'
lpg_num = int(get_lastpage(url))
foutput = array(['biocode','longitude','latitude'])
pbar = ProgressBar(maxval=lpg_num).start()
for i in xrange(0, lpg_num):
    num = i+1
    url_str = url+'?page='+str(num)
    get_spcoord(url_str)
    foutput = vstack((foutput, coor_out))
    pbar.update(i+1)
pbar.finish()
print('Finished!')
export_csv("Trochodendron_aralioides.csv", foutput)

# <codecell>

# Alnus formosana
url = 'http://www.taibif.tw/zh/catalogue_of_life/page/a0eb-662c-f01a-ee07-3d7e-833c-7096-513f-namecode-203257'
lpg_num = int(get_lastpage(url))
foutput = array(['biocode','longitude','latitude'])
pbar = ProgressBar(maxval=lpg_num).start()
for i in xrange(0, lpg_num):
    num = i+1
    url_str = url+'?page='+str(num)
    get_spcoord(url_str)
    foutput = vstack((foutput, coor_out))
    pbar.update(i+1)
pbar.finish()
print('Finished!')
export_csv("Alnus_formosana.csv", foutput)

# <codecell>

#
search_api_url = 'http://www.taibif.tw/zh/taxonomy_fts?search_api_views_fulltext='


# <markdowncell>

# 資料待處理
# 1. 空白的座標
# 2. 重複的資料

