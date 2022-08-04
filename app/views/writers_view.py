from flask import Blueprint, render_template, request, Response
from app.app import db
import json


writers_view_blueprint = Blueprint("writer", __name__)

class Writer(db.Model):
    __tablename__ = "writer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Integer)
    email = db.Column(db.String(128), nullable=False)

    def to_json(self):
        return {"id": self.id, "name": self.name, "age": self.age, "email":self.email} 
    
def query_to_json(writer):
    return {"id": writer.id, "name": writer.name, "age": writer.age, "email":writer.email} 

@writers_view_blueprint.route('/create', methods=["POST"])
def create():
    data = request.get_json()
    try:
        writer = Writer(
            name=data.get("name"), 
            age=data.get("age"), 
            email=data.get("email")
        )
        db.session.add(writer)
        db.session.commit()
        return Response(json.dumps(writer.to_json()), status=200, mimetype="application/json")
    except Exception as e:
        return Response(e, status=501)

@writers_view_blueprint.route('/update', methods=["POST"])
def update():
    data = request.get_json()
    writer = Writer.query.filter_by(id=data.get("id")).update(data)
    db.session.commit()
    return Response(json.dumps({"updated_rows": writer}), status=200)

@writers_view_blueprint.route('/get/<int:id>', methods=["GET"])
def get_writer(id):
    writer = Writer.query.filter_by(id=id).first()
    if writer:
        return Response(json.dumps(query_to_json(writer)), status=200, mimetype="application/json")
    else:
        return Response(json.dumps(f"Writer {id} not found"), status=404)

@writers_view_blueprint.route('/delete', methods=["POST"])
def delete():
    data = request.get_json()
    writer = Writer.query.filter_by(id=data.get("id")).delete()
    db.session.commit()
    return Response(json.dumps({"deleted_rows": writer}), status=200)
