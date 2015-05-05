'''
Created on May 3, 2015

@author: puneeth
'''

from web import web
from flask.templating import render_template
from flask import request

#Route create the mapping URLs to their respective functions
@web.route('/')
@web.route('/index')
def index():      
    return render_template('index.html',
                           title='Yelp Dataset Challenge')
    
@web.route('/suggestions', methods=['POST'])
def suggestions():
    userid = request.form['userid']
    print(userid)
    fpath = '/home/ubuntu/datamining/SLP/src/web/templates/'
    
    if(userid == 'emily'):
        fname = 'prediction_output_Emily.txt'
    elif(userid == 'norm'):
        fname = 'prediction_output_Norm.txt'
    elif(userid == 'gabi'):
        fname = 'prediction_output_Gabi.txt'
    elif(userid == 'j'):
        fname = 'prediction_output_J.txt'
    elif(userid == 'karen'):
        fname = 'prediction_output_Karen.txt'
    elif(userid == 'jennifer'):
        fname = 'prediction_output_Jennifer.txt'
    elif(userid == 'ken'):
        fname = 'prediction_output_Ken.txt'
    elif(userid == 'felicia'):
        fname = 'prediction_output_Felicia.txt'
    elif(userid == 'mike'):
        fname = 'prediction_output_Mike.txt'
    elif(userid == 'jessica'):
        fname = 'prediction_output_Jessica.txt'
    
    f = open(fpath+fname, mode='r')
    j = {}
    for line in f:
        key, lat, long = line.split(',')
        j[key] = (lat + ',' + long).replace('\n', ' ').strip()

    return render_template('suggestions.html', obj=j)
