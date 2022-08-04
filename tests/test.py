import json
import uuid

def test_add_writer(client):
    fake_data = str(uuid.uuid4())
    resp = client.post(
        '/writer/create',
        json={
            "name": fake_data,
            "age": 10,
            "email": fake_data
        }
    )

    assert resp.status_code == 200
    assert resp.json["name"] == fake_data
    assert resp.json["email"] == fake_data
    assert resp.json["age"] == 10

def test_get_writer(client):
    fake_data = str(uuid.uuid4())
    resp = client.post(
        '/writer/create',
        json={
            "name": fake_data,
            "age": 10,
            "email": fake_data
        }
    )

    get_resp = client.get(
        f'/writer/get/{resp.json["id"]}',
    )
    assert get_resp.status_code == 200
    assert get_resp.json["name"] == fake_data
    assert get_resp.json["email"] == fake_data
    assert get_resp.json["age"] == 10
    

def test_update_writer(client):
    fake_data = str(uuid.uuid4())
    resp = client.post(
        '/writer/create',
        json={
            "name": fake_data,
            "age": 10,
            "email": fake_data
        }
    )

    assert resp.status_code == 200
    assert resp.json["name"] == fake_data
    assert resp.json["email"] == fake_data
    assert resp.json["age"] == 10

    new_data = str(uuid.uuid4())

    up_resp = client.post(
        '/writer/update',
        json={
            "id": resp.json["id"],
            "name": new_data,
            "age": 11,
            "email": new_data
        }
    )

    assert up_resp.status_code == 200

def test_delete_writer(client):
    fake_data = str(uuid.uuid4())
    resp = client.post(
        '/writer/create',
        json={
            "name": fake_data,
            "age": 10,
            "email": fake_data
        }
    )

    assert resp.status_code == 200
    assert resp.json["name"] == fake_data
    assert resp.json["email"] == fake_data
    assert resp.json["age"] == 10

    del_resp = client.post(
        f'/writer/delete',
        json={
            "id": resp.json["id"]
        }
    )

    assert del_resp.status_code == 200
    
def test_blog_creation(client):
    fake_data = str(uuid.uuid4())
    resp = client.post(
        '/blog/create',
        json={
            "title": fake_data
        }
    )

    assert resp.json["title"] == fake_data

def test_blog_update(client):
    fake_data = str(uuid.uuid4())
    resp = client.post(
        '/blog/create',
        json={
            "title": fake_data
        }
    )
    assert resp.json["title"] == fake_data
    new_data = str(uuid.uuid4())
    up_resp = client.post(
        '/blog/update',
        json={
            "id": resp.json["id"],
            "title": new_data
        }
    )

    assert up_resp.status == "200 OK"

def test_blog_delete(client):
    fake_data = str(uuid.uuid4())
    resp = client.post(
        '/blog/create',
        json={
            "title": fake_data
        }
    )

    del_resp = client.post(
        f'/blog/delete',
        json={
            "id": resp.json["id"]
        }
    )

    assert del_resp.status=="200 OK"

def test_blog_get(client):
    fake_data = str(uuid.uuid4())
    resp = client.post(
        '/blog/create',
        json={
            "title": fake_data
        }
    )

    get_resp = client.get(
        f'/blog/get/{resp.json["id"]}'
    )

    assert get_resp.json =={
        "id": resp.json["id"],
        "title": fake_data,
        "articles": []
    }

def test_article_create(client):
    writer_data = str(uuid.uuid4())
    blog_data = str(uuid.uuid4())
    article_data = str(uuid.uuid4())
    writer = client.post(
        '/writer/create',
        json={
            "name": writer_data,
            "age": 10,
            "email": writer_data
        }
    )
    blog = client.post(
        '/blog/create',
        json={
            "title": blog_data
        }
    )
    article = client.post(
        '/article/create',
        json={
            "title": article_data,
            "excerpt" : article_data,
            "text": article_data,
            "writer": writer.json["id"],
            "blog_ids": [blog.json["id"]]
        }
    )

    assert article.json["result"] == f"Article created on blogs [{blog.json['id']}]"

def test_article_delete(client):
    writer_data = str(uuid.uuid4())
    blog_data = str(uuid.uuid4())
    article_data = str(uuid.uuid4())
    writer = client.post(
        '/writer/create',
        json={
            "name": writer_data,
            "age": 10,
            "email": writer_data
        }
    )
    blog = client.post(
        '/blog/create',
        json={
            "title": blog_data
        }
    )
    article = client.post(
        '/article/create',
        json={
            "title": article_data,
            "excerpt" : article_data,
            "text": article_data,
            "writer": writer.json["id"],
            "blog_ids": [blog.json["id"]]
        }
    )

    assert len(article.json["instances"]) == 1
    art = article.json["instances"][0]
    up_resp = client.post(
        '/article/delete',
        json=art
    )

    assert up_resp.json["deleted_rows"] == 1

def test_article_delete_all(client):
    writer_data = str(uuid.uuid4())
    blog_data = str(uuid.uuid4())
    article_data = str(uuid.uuid4())
    writer = client.post(
        '/writer/create',
        json={
            "name": writer_data,
            "age": 10,
            "email": writer_data
        }
    )
    blog = client.post(
        '/blog/create',
        json={
            "title": blog_data
        }
    )
    
    blog2 = client.post(
        '/blog/create',
        json={
            "title": blog_data
        }
    )

    article = client.post(
        '/article/create',
        json={
            "title": article_data,
            "excerpt" : article_data,
            "text": article_data,
            "writer": writer.json["id"],
            "blog_ids": [blog.json["id"], blog2.json["id"]]
        }
    )

    assert len(article.json["instances"]) == 2
    art = article.json["instances"][0]
    up_resp = client.post(
        '/article/delete_all',
        json=art
    )

    assert up_resp.json["deleted_rows"] == 2

def test_article_update(client):
    writer_data = str(uuid.uuid4())
    blog_data = str(uuid.uuid4())
    article_data = str(uuid.uuid4())
    writer = client.post(
        '/writer/create',
        json={
            "name": writer_data,
            "age": 10,
            "email": writer_data
        }
    )
    blog = client.post(
        '/blog/create',
        json={
            "title": blog_data
        }
    )
    article = client.post(
        '/article/create',
        json={
            "title": article_data,
            "excerpt" : article_data,
            "text": article_data,
            "writer": writer.json["id"],
            "blog_ids": [blog.json["id"]]
        }
    )

    assert article.json["result"] == f"Article created on blogs [{blog.json['id']}]"
    assert len(article.json["instances"]) == 1
    art = article.json["instances"][0]
    art["title"] == "New title"
    up_resp = client.post(
        '/article/update',
        json=art
    )

    assert up_resp.json["updated_rows"] == 1

def test_all_article_update_all(client):
    writer_data = str(uuid.uuid4())
    blog_data = str(uuid.uuid4())
    article_data = str(uuid.uuid4())
    writer = client.post(
        '/writer/create',
        json={
            "name": writer_data,
            "age": 10,
            "email": writer_data
        }
    )
    blog = client.post(
        '/blog/create',
        json={
            "title": blog_data
        }
    )
    
    blog2 = client.post(
        '/blog/create',
        json={
            "title": blog_data
        }
    )

    article = client.post(
        '/article/create',
        json={
            "title": article_data,
            "excerpt" : article_data,
            "text": article_data,
            "writer": writer.json["id"],
            "blog_ids": [blog.json["id"], blog2.json["id"]]
        }
    )

    assert article.json["result"] == f"Article created on blogs {[blog.json['id'], blog2.json['id']]}"
    assert len(article.json["instances"]) == 2
    art = article.json["instances"][0]
    art["title"] == "New title"
    up_resp = client.post(
        '/article/update_all',
        json=art
    )

    assert up_resp.json["updated_rows"] == 2

def test_article_create_multiple(client):
    writer_data = str(uuid.uuid4())
    blog_data = str(uuid.uuid4())
    article_data = str(uuid.uuid4())
    writer = client.post(
        '/writer/create',
        json={
            "name": writer_data,
            "age": 10,
            "email": writer_data
        }
    )
    blog = client.post(
        '/blog/create',
        json={
            "title": blog_data
        }
    )

    blog2 = client.post(
        '/blog/create',
        json={
            "title": blog_data
        }
    )

    article = client.post(
        '/article/create',
        json={
            "title": article_data,
            "excerpt" : article_data,
            "text": article_data,
            "writer": writer.json["id"],
            "blog_ids": [blog.json["id"], blog2.json["id"]]
        }
    )

    article2 = client.post(
        '/article/create',
        json={
            "title": article_data,
            "excerpt" : article_data,
            "text": article_data,
            "writer": writer.json["id"],
            "blog_ids": [blog.json["id"]]
        }
    )

    assert article.json["result"] == f"Article created on blogs {[blog.json['id'], blog2.json['id']]}"

def test_get_blog_with_articles(client):
    writer_data = str(uuid.uuid4())
    blog_data = str(uuid.uuid4())
    article_data = str(uuid.uuid4())
    article2_data = str(uuid.uuid4())
    writer = client.post(
        '/writer/create',
        json={
            "name": writer_data,
            "age": 10,
            "email": writer_data
        }
    )
    blog = client.post(
        '/blog/create',
        json={
            "title": blog_data
        }
    )

    article = client.post(
        '/article/create',
        json={
            "title": article_data,
            "excerpt" : article_data,
            "text": article_data,
            "writer": writer.json["id"],
            "blog_ids": [blog.json["id"]]
        }
    )

    article2 = client.post(
        '/article/create',
        json={
            "title": article2_data,
            "excerpt" : article2_data,
            "text": article2_data,
            "writer": writer.json["id"],
            "blog_ids": [blog.json["id"]]
        }
    )

    get_resp = client.get(
        f'/blog/get/{blog.json["id"]}'
    )

    assert len(get_resp.json["articles"]) == 2


