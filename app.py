
from pathlib import Path
from uuid import uuid4

from flask import Flask, jsonify, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = Path(app.root_path) / "static" / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

students = []

BRANCH_NAMES = {
    "MECH": "Mechanical Engineering",
    "COMPS": "Computer Engineering",
    "IT": "Information Technology",
    "EXTC": "Electronics and Telecommunication",
}

CATEGORIES = [
    {
        "name": "Studies",
        "description": "Subject help, notes, coding, exams, and project guidance.",
    },
    {
        "name": "Sports",
        "description": "Training, team selection, fitness, and tournament support.",
    },
    {
        "name": "Cultural",
        "description": "Dance, music, drama, debate, anchoring, and event guidance.",
    },
    {
        "name": "Projects",
        "description": "Mini projects, final year projects, reports, and presentations.",
    },
    {
        "name": "Placements",
        "description": "Resume building, interviews, aptitude, and career guidance.",
    },
]

MENTORS = {
    branch: {category["name"]: [] for category in CATEGORIES}
    for branch in BRANCH_NAMES
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/choose-role")
def choose_role():
    return render_template("role.html")


@app.route("/form")
def student_form():
    return render_template("form.html", branches=BRANCH_NAMES)


@app.route("/submit_student", methods=["POST"])
def submit_student():
    name = request.form.get("student_name", "").strip()
    branch = request.form.get("branch", "").strip()

    if not name or branch not in BRANCH_NAMES:
        error = "Please enter your name and select a valid branch."
        return render_template("form.html", branches=BRANCH_NAMES, error=error)

    students.append({
        "name": name,
        "branch": branch,
    })

    return redirect(url_for("department", name=name, branch=branch))


@app.route("/department")
def department():
    name = request.args.get("name", "")
    branch = request.args.get("branch", "")

    if branch not in BRANCH_NAMES:
        return redirect(url_for("student_form"))

    return render_template(
        "department.html",
        student_name=name,
        branch=branch,
        branch_name=BRANCH_NAMES[branch],
        categories=CATEGORIES,
    )


@app.route("/mentors")
def mentors():
    name = request.args.get("name", "")
    branch = request.args.get("branch", "")
    category = request.args.get("category", "")

    if branch not in BRANCH_NAMES or category not in MENTORS[branch]:
        return redirect(url_for("student_form"))

    return render_template(
        "mentors.html",
        student_name=name,
        branch=branch,
        branch_name=BRANCH_NAMES[branch],
        category=category,
    )


@app.route("/mentor-register")
def mentor_register():
    return render_template(
        "mentor_form.html",
        branches=BRANCH_NAMES,
        categories=CATEGORIES,
    )


@app.route("/submit_mentor", methods=["POST"])
def submit_mentor():
    name = request.form.get("mentor_name", "").strip()
    branch = request.form.get("branch", "").strip()
    category = request.form.get("category", "").strip()
    expertise = request.form.get("expertise", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    photo = request.files.get("photo")

    valid_categories = [category_item["name"] for category_item in CATEGORIES]

    if (
        not name
        or branch not in BRANCH_NAMES
        or category not in valid_categories
        or not expertise
        or not email
        or not phone
        or not photo
        or photo.filename == ""
    ):
        error = "Please fill all mentor details and upload a photo."
        return render_template(
            "mentor_form.html",
            branches=BRANCH_NAMES,
            categories=CATEGORIES,
            error=error,
        )

    filename = secure_filename(photo.filename)
    unique_filename = f"{uuid4().hex}_{filename}"
    photo_path = UPLOAD_FOLDER / unique_filename
    photo.save(photo_path)

    new_mentor = {
        "name": name,
        "photo": url_for("static", filename=f"uploads/{unique_filename}"),
        "email": email,
        "phone": phone,
        "expertise": expertise,
    }

    MENTORS[branch][category].append(new_mentor)

    return render_template(
        "mentor_success.html",
        mentor_name=name,
        branch=branch,
        branch_name=BRANCH_NAMES[branch],
        category=category,
    )


@app.route("/get_mentors")
def get_mentors():
    branch = request.args.get("branch", "")
    category = request.args.get("category", "")

    mentors_list = MENTORS.get(branch, {}).get(category, [])
    return jsonify(mentors_list)


if __name__ == "__main__":
    app.run(debug=True)
