import unittest
import os 
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
    
    def test_home(self):
        response = self.client.get("/")
        mapIn = self.client.get("/static/img/map.png")
        photo = self.client.get("/static/img/photo.webp")
        logo = self.client.get("/static/img/logo.svg")
        cssI= self.client.get("/static/styles/index.css")
        cssM = self.client.get("/static/styles/main.css")

        assert mapIn.status_code == 200
        assert response.status_code == 200
        assert photo.status_code == 200
        assert logo.status_code == 200
        assert cssI.status_code == 200
        assert cssM.status_code == 200

        html = response.get_data(as_text=True)
        assert "<title>Jia Xuan Li</title>" in html
        assert "<h2>About Me</h2>" in html
        assert "<h2>Experience</h2>" in html
        assert "<h2>Education</h2>" in html
        assert "<h2>Places I traveled to</h2>" in html
        assert "<a href=\"/hobbies\">Hobbies</a>" in html
        assert "<a href=\"/timeline\">Timeline</a>" in html

        html = response.get_data(as_text=True)

        expAndEducation = html.count('<div class="card"')
        self.assertGreaterEqual(expAndEducation, 4, "There are at least 4 or more cards representing current experience and education as of 2025")
        

    
    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert len(json["timeline_posts"]) == 0  

        postResponse = self.client.post("/api/timeline_post", data={
            "name":"John Doe",
            "email":"john@example.com",
            "content":"Hello World, I'm John!"
        })

        assert postResponse.status_code == 200
        assert postResponse.is_json
        json = postResponse.get_json()
        assert json["name"] == "John Doe"
        assert json["email"] == "john@example.com"
        assert json["content"] == "Hello World, I'm John!"

        getResponse = self.client.get("/api/timeline_post")
        assert getResponse.status_code == 200
        assert getResponse.is_json
        json = getResponse.get_json()
        assert len(json["timeline_posts"]) == 1
        assert json["timeline_posts"][0]["name"] == "John Doe"
        assert json["timeline_posts"][0]["email"] == "john@example.com"
        assert json["timeline_posts"][0]["content"] == "Hello World, I'm John!"
        assert json["timeline_posts"][0]["id"] == 1

        postResponse1 = self.client.post("/api/timeline_post", data={
            "name": "Jane Doe",
            "email": "jane@example.com",
            "content": "Hello World, I'm Jane!"
        })

        assert postResponse1.status_code == 200
        assert postResponse1.is_json
        json = postResponse1.get_json()
        assert json["name"] == "Jane Doe"
        assert json["email"] == "jane@example.com"
        assert json["content"] == "Hello World, I'm Jane!"
        assert json["id"] == 2
        assert json["created_at"] is not None

        getResponse1 = self.client.get("/api/timeline_post")
        assert getResponse1.status_code == 200
        assert getResponse1.is_json
        json = getResponse1.get_json()
        assert len(json["timeline_posts"]) == 2
        assert json["timeline_posts"][0]["name"] == "Jane Doe"
        assert json["timeline_posts"][0]["email"] == "jane@example.com"
        assert json["timeline_posts"][0]["content"] == "Hello World, I'm Jane!"

        
        cssM = self.client.get("/static/styles/main.css")
        logo = self.client.get("/static/img/logo.svg")
        photo = self.client.get("/static/img/photo.webp")

        assert cssM.status_code == 200
        assert logo.status_code == 200
        assert photo.status_code == 200

        html = self.client.get("/timeline").get_data(as_text=True)
        assert "<title>Timeline</title>" in html
        assert "<h2>Timeline</h2>" in html

    def test_malformed_timeline_post(self):
        response = self.client.post("/api/timeline_post", data={
            "email": "john@example.com",
            "content": "Hello World, I'm John!"
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert 'Invalid name' in html

        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe",
            "email": "john@example.com",
            "content": ""
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe",
            "email": "not-an-email",
            "content": "Hello World, I'm John!"
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html