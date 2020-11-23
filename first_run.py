import sqlite3
import flask
from cosmicdepth import db
from cosmicdepth import create_app

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)
conn = sqlite3.connect('site.db')
conn.close()
with app.app_context():
    db.create_all()

print("""
Your sqlite database has been created.

You may now launch app.py
""")