'''
Created on May 3, 2015

@author: puneeth
'''

from web import web
from flask.templating import render_template
from flask import request
from dm import jsontotable

@web.route('/')
@web.route('/index')
def index():
#     return "Hello, World!"
    user = {'nickname':'Puneeth',
            'friend': 'Nishanth'}  # fake user
      
    return render_template('index.html',
                           title='Yelp Dataset Challenge',
                           user=user)
    
@web.route('/suggestions', methods=['POST'])
def suggestions():
    userid = request.form['userid']
    print(userid)
    fpath = '/home/puneeth/workspace/SLP/src/web/templates/'
    
    if(userid == 'volvo'):
        fname = 'prediction_output_1.txt'
    elif(userid == 'saab'):
        fname = 'prediction_output_2.txt'
    elif(userid == 'mercedes'):
        fname = 'prediction_output_3.txt'
    elif(userid == 'audi'):
        fname = 'prediction_output_4.txt'
    
    f = open(fpath+fname, mode='r', encoding='utf-8')
    j = {}
    for line in f:
        key, lat, long = line.split(',')
        j[key] = (lat + ',' + long).replace('\n', ' ').strip()

    return render_template('suggestions.html', obj=j)
