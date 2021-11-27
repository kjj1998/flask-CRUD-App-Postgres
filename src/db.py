import sqlite3
import click

from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
	if 'db' not in g:
		# establish connection to the database file
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db.execute("PRAGMA foreign_keys = 1")

		# return rows that behave like dicts
		g.db.row_factory = sqlite3.Row
	
	return g.db

def close_db(e=None):
	db = g.pop('db', None)

	# close connection if it exists
	if db is not None:
		db.close()

def init_db():
	db = get_db()

	# opens a connection to the db and execute the script in schema.sq1
	with current_app.open_resource('schema.sql') as f:
		db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
	# clear the existing data and create new tables
	init_db()
	click.echo('Initialized the database.')

def init_app(app):
	# close the db when cleaning up after returning the response
	app.teardown_appcontext(close_db)
	# adds a new command that can be called with the flask command
	app.cli.add_command(init_db_command)