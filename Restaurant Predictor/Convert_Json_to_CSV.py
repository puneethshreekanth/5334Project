'''
Created on May 2015

@author: Shreekanth

References
http://blog.cloudera.com/blog/2013/04/demo-analyzing-data-with-hue-and-hive/
https://raw.githubusercontent.com/romainr/yelp-data-analysis/master/convert.py

File to preprocess the data, convert data from json to csv
'''

#!/usr/bin/env python
import json

'''Covert Business data from json to csv'''
business_clean = open('C:\Shree\Study\Data Mining\Course_Project\CSV_Files\yelp_academic_dataset_business_clean.json', 'w+')

for line in open('C:\Shree\Study\Data Mining\Course_Project\Data_Files\yelp_academic_dataset_business.json'):
    business_json = json.loads(line)
    business = map(unicode, business_json.values())
    business_clean.write(u'\t'.join(business).replace('\n', ' ').encode('utf-8') + '\n')

print json.dumps(business_json.keys())

'''Covert Review data from json to csv'''
review_clean = open('C:\Shree\Study\Data Mining\Course_Project\CSV_Files\yelp_academic_dataset_review_clean.json', 'w+')

for line in open('C:\Shree\Study\Data Mining\Course_Project\Data_Files\yelp_academic_dataset_review.json'):
	review_json = json.loads(line)
	review_json_votes = review_json['votes']
	review_json['votes'] = '\t'.join(map(unicode, review_json_votes.values()))  
	review = map(unicode, review_json.values())  
	review_clean.write(u'\t'.join(review).replace('\n', ' ').encode('utf-8') + '\n')

print json.dumps(review_json_votes.keys() + review_json.keys()[1:])

'''Covert User data from json to csv'''
user_clean = open('C:\Shree\Study\Data Mining\Course_Project\CSV_Files\yelp_academic_dataset_user_clean.json', 'w+')

for line in open('C:\Shree\Study\Data Mining\Course_Project\Data_Files\yelp_academic_dataset_user.json'):
    user_json = json.loads(line)
    user_json_votes = user_json['votes']
    user_json['votes'] = '\t'.join(map(unicode, user_json_votes.values()))  
    user = map(unicode, user_json.values())  
    user_clean.write(u'\t'.join(user).replace('\n', ' ').encode('utf-8') + '\n')

print json.dumps(user_json_votes.keys() + user_json.keys()[1:])