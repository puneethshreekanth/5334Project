'''
Created on May 3, 2015

@author: puneeth
'''

import json

big_dict = {}

def cols(userid):
    f = open('user_reviews_att.csv', 'r')
    for line in f:    
    #     print(line)
        line = line.replace("u'", "'")
        line = line.replace("\"{", "{")
        line = line.replace("}\"", "}")
        line = line.replace("'", "\"")
        line = line.replace("False", "\"False\"")
        line = line.replace("True", "\"True\"")
        print(line)
        
        d = json.JSONDecoder(object_pairs_hook=dict).decode(line)
#         print(type(d), d)
        
        for key, val in d.items():
            try:
                big_dict[key] = []
                
            except KeyError:
                pass
        
        break
    
    return d