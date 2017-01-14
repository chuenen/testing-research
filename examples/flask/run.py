'''
#!/usr/bin/env python
from os import environ

from app import app, db

db.create_all()
app.run(host='chuen.com', port=8000, debug=True)
'''

import logging
from config import LOG_PATH

logging.basicConfig(filename=LOG_PATH, filemode='w', level=logging.DEBUG,
		    format='%(asctime)s %(levelname)-6s %(name)s - %(message)s')

from app import app as application
