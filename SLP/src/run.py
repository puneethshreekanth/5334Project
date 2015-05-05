'''
Created on May 3, 2015

@author: puneeth
'''
'''
The script simply imports the web variable from our web package and invokes its
run method to start the server. Remember that the web variable holds the Flask
instance that we created it above.
'''

from web import web

web.run(debug=True, host='0.0.0.0', port=5000)
