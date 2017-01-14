from os import path

# App details
BASE_DIRECTORY = path.abspath(path.dirname(__file__))
# DEBUG = True
SECRET_KEY = 'keep_it_like_a_secret'

#Debug
LOG_PATH = '/tmp/fblogin.log'

# Database details
SQLALCHEMY_DATABASE_URI = 'mysql://research:chuenen@localhost/research'

#Upload file
UPLOAD_FOLDER = path.join(BASE_DIRECTORY, 'app/uploads')
ALLOWED_EXTENSIONS = set(['apk', 'png', 'jpg', 'jpeg'])
MAX_CONTENT_LENGTH = 100 * 1024 * 1024
