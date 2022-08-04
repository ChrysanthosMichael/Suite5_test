
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.views.writers_view import writers_view_blueprint
from app.views.blogs_view import blogs_view_blueprint
from app.views.articles_view import articles_view_blueprint

app.register_blueprint(
    blogs_view_blueprint,
    url_prefix=f"/{blogs_view_blueprint.name}"
)
app.register_blueprint(
    writers_view_blueprint,
    url_prefix=f"/{writers_view_blueprint.name}"
)
app.register_blueprint(
    articles_view_blueprint,
    url_prefix=f"/{articles_view_blueprint.name}"
)

@app.route('/')
def home():
    return 'Home'
