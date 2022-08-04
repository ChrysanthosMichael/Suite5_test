from flask import Blueprint, request, Response
from app.app import db
from app.views.articles_view import Article
import json

blogs_view_blueprint = Blueprint("blog", __name__)

class Blog(db.Model):
    __tablename__ = "blog"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)

    def to_json(self):
        return {"id": self.id, "title": self.title}

def query_to_json(blog, articles=None):
    return {
        "id": blog.id, 
        "title": blog.title,
        "articles" : [{
            "id": article.id,
            "title": article.title,
            "excerpt": article.excerpt,
            "text": article.text,
            "date_created": str(article.date_created),
            "date_updated": str(article.date_updated),
            "writer": article.writer
        } for article in articles] if articles else []
    } 

@blogs_view_blueprint.route('/create', methods=["POST"])
def create():
    data = json.loads(request.get_json())
    try:
        blog = Blog(
            title=data.get("title"), 
        )
        db.session.add(blog)
        db.session.commit()
        return Response(json.dumps(blog.to_json()), status=200, mimetype="application/json")
    except Exception as e:
        return Response(e, status=501)

@blogs_view_blueprint.route('/update', methods=["POST"])
def update():
    data = json.loads(request.get_json())
    writer = Blog.query.filter_by(id=data.get("id")).update(data)
    db.session.commit()
    return Response(json.dumps({"updated_rows": writer}), status=200)

@blogs_view_blueprint.route('/get/<int:id>', methods=["GET"])
def get_blog_articles(id):
    blog = Blog.query.filter_by(id=id).first()
    articles = Article.query.filter_by(blog_id = blog.id).all()
    if blog:
        return Response(json.dumps(query_to_json(blog, articles)), status=200, mimetype="application/json")
    else:
        return Response(json.dumps(f"Blog {id} not found"), status=404)

@blogs_view_blueprint.route('/delete', methods=["POST"])
def delete():
    data = json.loads(request.get_json())
    blog = Blog.query.filter_by(id=data.get("id")).delete()
    db.session.commit()
    return Response(json.dumps({"deleted_rows": blog}), status=200)
