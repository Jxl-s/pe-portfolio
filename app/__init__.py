import os

from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()
app = Flask(__name__)

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
    }
]

hobbies = [
    {
        "title": "3D Modeling",
        "description": "Creating basic 3D models for fun using Blender.",
    }
]


@app.route("/")
def index():
    return render_template(
        "index.html",
        title="Jia Xuan Li",
        url=os.getenv("URL"),
        experience=experience,
        education=education,
        hobbies=hobbies,
    )
