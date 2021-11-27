import os

from flask import Flask
from . import db, application
UPLOAD_FOLDER = '.\\static\\uploads'
DOWNLOAD_FOLDER = '.\\static\\downloads'

# application factory function
def create_app(test_config=None):
	# create and confiure app
	app = Flask(__name__, instance_relative_config=True)
	
	# sets some default configuration used by the app
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'src.sqlite'),
	)
	app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
	app.config['DOWNLOAD_FOLDER'] =  DOWNLOAD_FOLDER

	# overrides the default configuration
	if test_config is None:
		# Load the instance config when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		# Load the test config
		app.config.from_mapping(test_config)

	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	# simple page to test that Flask is working
	@app.route('/hello')
	def hello():
		return 'Hello, World!'
	
	db.init_app(app)
	
	# register the blueprint from application
	app.register_blueprint(application.bp)
	app.add_url_rule('/', endpoint='index')

	return app