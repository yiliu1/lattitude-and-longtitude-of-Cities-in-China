
# coding: utf-8

# In[259]:

import urllib, urllib2
import json
 
 
class GeoCoding(object):
    def __init__(self, key = ' '):
        self.url_para = {'address': '', 
                 'sensor': 'false',
                 'language': 'zh-CN'}
        self.url = 'http://maps.googleapis.com/maps/api/geocode/json'
        self.geo_info_list = []
         
    def get_latlng_by_name(self, geo_name):
        self.url_para['address'] = geo_name.encode('utf-8')
        arguments = urllib.urlencode(self.url_para)
        url_get_geo = self.url + '?' + arguments
        handler = urllib2.urlopen(url_get_geo)
        resp_data = handler.read()
        handler.close()
        st = self.parse_ret_json(resp_data)
        return self.geo_info_list
 
    def parse_ret_json(self, ret_str):
        parse_st = False
        ret_json = json.loads(ret_str)
        if ret_json['status'] == 'OK':
            #get lat lng and addr
            for geo_info in ret_json['results']:
                #print(geo_info)
                geo_dict = {'lat': geo_info['geometry']['location']['lat'],
                            'lng': geo_info['geometry']['location']['lng'],
                            'addr': geo_info['formatted_address'],
                            'city':'',
                            'state_province':'',
                            'country':'',
                            'types': geo_info['types']}
                #get city state_provine country
                for addr_comp in geo_info['address_components']:
                    if 'country' in addr_comp['types']: 
                        geo_dict['country'] = addr_comp['long_name']
                    elif 'administrative_area_level_1' in addr_comp['types']:
                        geo_dict['state_province'] = addr_comp['long_name']
                    elif 'sublocality' in addr_comp['types'] or                          'locality' in addr_comp['types'] or                          'administrative_area_level_2' in addr_comp['types'] or                          'administrative_area_level_3' in addr_comp['types']:
                        geo_dict['city'] = addr_comp['long_name']
                self.geo_info_list.append(geo_dict) 
            parse_st = True
            print(self.geo_info_list)
        else:
            parse_st = False
            print(ret_json['status']) 
        return parse_st


# In[260]:

import sys
reload(sys)
sys.setdefaultencoding('utf8')


# In[261]:

import pandas as pd
import numpy as np


# In[262]:

# For .read_csv, always use header=0 when you know row 0 is the header row
df = pd.read_csv('/Users/yi/Desktop/map.csv', header=0)


# In[338]:

import time

for k in range(65):
    p=10*k
    q=p+10
    for i in range (p,q):
        s=GeoCoding()
        a=df['站点名'][i]
    #b=df['Unnamed: 2'][i]
        n=s.get_latlng_by_name(a)
    #m=s.get_latlng_by_name(b)
    #if len(m)==len(n) :
        if n!=[]:
            n=n[0]
            df['Unnamed: 3'][i]=n['lat']
            df['Unnamed: 4'][i]=n['lng']
        

        
    if i%9==0 :
        time.sleep(0.5)
        
        
    
        
     #time.sleep(1)
    
   # print k
    
        
    


    

    


# In[340]:

df.to_csv('/Users/yi/Desktop/baobao.csv')

