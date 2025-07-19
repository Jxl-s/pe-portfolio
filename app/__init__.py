import datetime
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from peewee import *
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    myDb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    myDb = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=int(os.getenv("MYSQL_PORT", 3306)),
)


class TimelinePost(Model):
    id = AutoField()
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = myDb


myDb.connect()
myDb.create_tables([TimelinePost])

experience = [
    {
        "title": "Production Engineering Fellow",
        "company": "Meta & Major League Hacking",
        "date": "June 2025 - Present",
        "location": "Remote",
        "description": [
            "Deploying scalable infrastructure with Docker and Linux, and automating CI/CD pipelines with GitHub Actions."
        ],
    },
    {
        "title": "Software Development Intern",
        "company": "NDT Technologies Inc.",
        "date": "January 2024 - August 2024",
        "location": "Montreal, Canada",
        "description": [
            "Cut page loading times from 30s to 0.15s by optimizing database queries, significantly enhancing user experience.",
            "Reduced administration workload by 40% by developing a 4-level authentication flow, hardening system security.",
        ],
    },
]

education = [
    {
        "degree": "Bachelor of Computer Science",
        "school": "Concordia University",
        "date": "Expected: June 2027",
        "location": "Montreal, Canada",
    },
    {
        "degree": "Technical DCS in Computer Science",
        "school": "Vanier College",
        "date": "May 2024",
        "location": "Montreal, Canada",
    },
]

hobbies = [
    {
        "title": "3D Modeling",
        "description": "I like to create 3D models for fun using Blender. I enjoy modeling low-poly items and environments as a simple way to express my creativity.",
        "image": "hobbies/3d-modeling.png",
    },
    {
        "title": "Doing LeetCode",
        "description": "I like to solve LeetCode problems in my free time as well, although it might seem weird. I find solving problems to be fun, and I've been getting into competitive programming lately.",
        "image": "hobbies/leetcode.png",
    },
    {
        "title": "Watching TV Series",
        "description": "I enjoy TV series, especially Korean and Chinese dramas, since I find the longer stories interesting. I also enjoy the cultural aspects they portray.",
        "image": "hobbies/tv-series.png",
    },
    {
        "title": "Scrolling TikTok/Reels",
        "description": "I like to scroll TikTok and Reels in my free time for the dopamine, although I know it's not the best use of my time. It's a good way to give a break to my brain.",
        "image": "hobbies/scrolling.jpg",
    },
]


@app.route("/")
def index():
    return render_template(
        "index.html",
        title="Jia Xuan Li",
        url=os.getenv("URL"),
        experience=experience,
        education=education,
    )


@app.route("/hobbies")
def hobbies_page():
    return render_template(
        "hobbies.html",
        title="Hobbies",
        url=os.getenv("URL", "http://localhost:5000") + "/hobbies",
        hobbies=hobbies,
    )


@app.route("/timeline")
def timeline():
    timeline_posts = [
        model_to_dict(p)
        for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
    ]

    return render_template(
        "timeline.html",
        title="Timeline",
        url=os.getenv("URL", "http://localhost:5000") + "/timeline",
        timeline_posts=timeline_posts,
    )


@app.route("/api/timeline_post", methods=["POST"])
def post_time_line_post():
    name = request.form["name"]
    email = request.form["email"]
    content = request.form["content"]
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)


@app.route("/api/timeline_post", methods=["GET"])
def get_time_line_posts():
    return {
        "timeline_posts": [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


@app.route("/api/timeline_post/<int:post_id>", methods=["DELETE"])
def delete_time_line_posts(post_id):
    deleted = TimelinePost.delete().where(TimelinePost.id == post_id).execute()
    if deleted:
        return jsonify({"message": f"Post {post_id} deleted"}), 200
    else:
        return jsonify({"error": "Post not found"}), 404
