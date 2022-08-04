import uuid
from flask import Blueprint, render_template, request, Response
from app.app import db
from app.views.writers_view import Writer
import datetime
import json


articles_view_blueprint = Blueprint("article", __name__)


class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article_code = db.Column(db.Text)
    title = db.Column(db.String(128), nullable=False)
    excerpt = db.Column(db.Integer)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.Date, default=datetime.datetime.now())
    date_updated = db.Column(db.Date, default=datetime.datetime.now())
    writer = db.Column(db.String(128), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey("blog.id"))

    def to_json(self):
        return {
            "id": self.id,
            "article_code": self.article_code,
            "title": self.title,
            "excerpt": self.excerpt,
            "text": self.text,
            "date_created": self.date_created,
            "date_updated": self.date_updated,
            "writer": self.writer,
            "blog_id": self.blog_id
        }

def query_to_json(article):
    return {
        "id": article.id,
        "article_code": article.article_code,
        "title": article.title,
        "excerpt": article.excerpt,
        "text": article.text,
        "date_created": article.date_created,
        "date_updated": article.date_updated,
        "writer": article.writer,
        "blog_id": article.blog_id
    }


@articles_view_blueprint.route('/create', methods=["POST"])
def create():
    data = request.form
    writer = Writer.query.filter_by(id=id).first()
    art_code = str(uuid.uuid4())
    if writer:
        for blog_id in request.form.get("blog_ids"):
            article = Article(
                title=data.get("title"),
                article_code=art_code,
                excerpt = data.get("excerpt"),
                text = data.get("text"),
                date_created = str(datetime.datetime.now()),
                date_updated = str(datetime.datetime.now()),
                writer = data.get("writer"),
                blog_id = blog_id,
            )
            db.session.add(article)
        db.session.commit()
        return Response(json.dumps(f"Article created on blogs {data.get('blog_ids')}"), status=200)
    else:
        return Response(json.dumps(f"Writer {id} not found"), status=404)


@articles_view_blueprint.route('/update', methods=["POST"])
def update():
    data = request.form
    rows = Article.query.filter_by(article_code=data.get("article_code")).update(data)
    db.session.commit()
    return Response(json.dumps({"updated_rows": rows}), status=200)

@articles_view_blueprint.route('/get/<int:id>', methods=["GET"])
def get_article(id):
    article = Article.query.filter_by(id=id).first()
    if article:
        return Response(json.dumps(query_to_json(article)), status=200, mimetype="application/json")
    else:
        return Response(json.dumps(f"Article {id} not found"), status=404)

@articles_view_blueprint.route('/delete/<int:id>', methods=["POST"])
def delete(id):
    rows = Article.query.filter_by(id=id).delete()
    db.session.commit()
    return Response(json.dumps({"deleted_rows": rows}), status=200)

@articles_view_blueprint.route('/delete/<code>', methods=["POST"])
def delete_all(code):
    rows = Article.query.filter_by(article_code=code).delete()
    db.session.commit()
    return Response(json.dumps({"deleted_rows": rows}), status=200)