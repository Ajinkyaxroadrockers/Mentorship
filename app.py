from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)

students = []

BRANCH_NAMES = {
    "MECH": "Mechanical Engineering",
    "COMPS": "Computer Engineering",
    "IT": "Information Technology",
    "EXTC": "Electronics and Telecommunication",
}

CATEGORIES = [
    {"name": "Studies", "description": "Subject help, notes, exams, and academic guidance."},
    {"name": "Sports", "description": "Training, fitness, team selection, and tournament support."},
    {"name": "Cultural", "description": "Dance, music, drama, debate, anchoring, and events."},
    {"name": "Projects", "description": "Mini projects, final year projects, reports, and presentations."},
    {"name": "Placements", "description": "Resume, interviews, aptitude, and career guidance."},
]

MENTORS = {
    "COMPS": {
        "Studies": [
            {
                "name": "Kabir Khan",
                "photo": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=500&q=80",
                "email": "kabir.comps@college.edu",
                "phone": "+91 91234 56789",
            },
            {
                "name": "Priya Nair",
                "photo": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=500&q=80",
                "email": "priya.comps@college.edu",
                "phone": "+91 90123 45678",
            },
        ],
        "Sports": [
            {
                "name": "Aarav Sharma",
                "photo": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=500&q=80",
                "email": "aarav.sports@college.edu",
                "phone": "+91 98765 43210",
            }
        ],
        "Cultural": [
            {
                "name": "Meera Joshi",
                "photo": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=crop&w=500&q=80",
                "email": "meera.cultural@college.edu",
                "phone": "+91 99887 76655",
            }
        ],
        "Projects": [
            {
                "name": "Dev Shah",
                "photo": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=500&q=80",
                "email": "dev.projects@college.edu",
                "phone": "+91 93210 45678",
            }
        ],
        "Placements": [
            {
                "name": "Riya Mehta",
                "photo": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=500&q=80",
                "email": "riya.place@college.edu",
                "phone": "+91 97654 32109",
            }
        ],
    },

    "IT": {
        "Studies": [
            {
                "name": "Ananya Desai",
                "photo": "https://images.unsplash.com/photo-1531123897727-8f129e1688ce?auto=format&fit=crop&w=500&q=80",
                "email": "ananya.it@college.edu",
                "phone": "+91 93456 78901",
            }
        ],
        "Sports": [
            {
                "name": "Rohan Patil",
                "photo": "https://images.unsplash.com/photo-1507591064344-4c6ce005b128?auto=format&fit=crop&w=500&q=80",
                "email": "rohan.it@college.edu",
                "phone": "+91 97654 32109",
            }
        ],
        "Cultural": [
            {
                "name": "Sneha Rao",
                "photo": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=500&q=80",
                "email": "sneha.it@college.edu",
                "phone": "+91 95555 44332",
            }
        ],
        "Projects": [
            {
                "name": "Nikhil Verma",
                "photo": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=500&q=80",
                "email": "nikhil.it@college.edu",
                "phone": "+91 94444 33221",
            }
        ],
        "Placements": [
            {
                "name": "Tanvi Kulkarni",
                "photo": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=500&q=80",
                "email": "tanvi.it@college.edu",
                "phone": "+91 93333 22110",
            }
        ],
    },

    "MECH": {
        "Studies": [
            {
                "name": "Sahil Jadhav",
                "photo": "https://images.unsplash.com/photo-1504257432389-52343af06ae3?auto=format&fit=crop&w=500&q=80",
                "email": "sahil.mech@college.edu",
                "phone": "+91 92222 11009",
            }
        ],
        "Sports": [
            {
                "name": "Omkar More",
                "photo": "https://images.unsplash.com/photo-1531891437562-4301cf35b7e4?auto=format&fit=crop&w=500&q=80",
                "email": "omkar.mech@college.edu",
                "phone": "+91 91111 00998",
            }
        ],
        "Cultural": [
            {
                "name": "Kavya Iyer",
                "photo": "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=500&q=80",
                "email": "kavya.mech@college.edu",
                "phone": "+91 90000 99887",
            }
        ],
        "Projects": [
            {
                "name": "Harsh Pawar",
                "photo": "https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=500&q=80",
                "email": "harsh.mech@college.edu",
                "phone": "+91 98989 87876",
            }
        ],
        "Placements": [
            {
                "name": "Neha Singh",
                "photo": "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=500&q=80",
                "email": "neha.mech@college.edu",
                "phone": "+91 97878 76765",
            }
        ],
    },

    "EXTC": {
        "Studies": [
            {
                "name": "Yash Bhide",
                "photo": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=500&q=80",
                "email": "yash.extc@college.edu",
                "phone": "+91 96767 65654",
            }
        ],
        "Sports": [
            {
                "name": "Aditya Rao",
                "photo": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=500&q=80",
                "email": "aditya.extc@college.edu",
                "phone": "+91 95656 54543",
            }
        ],
        "Cultural": [
            {
                "name": "Isha Menon",
                "photo": "https://images.unsplash.com/photo-1544723795-3fb6469f5b39?auto=format&fit=crop&w=500&q=80",
                "email": "isha.extc@college.edu",
                "phone": "+91 94545 43432",
            }
        ],
        "Projects": [
            {
                "name": "Manav Shetty",
                "photo": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=500&q=80",
                "email": "manav.extc@college.edu",
                "phone": "+91 93434 32321",
            }
        ],
        "Placements": [
            {
                "name": "Pooja Shah",
                "photo": "https://images.unsplash.com/photo-1531123897727-8f129e1688ce?auto=format&fit=crop&w=500&q=80",
                "email": "pooja.extc@college.edu",
                "phone": "+91 92323 21210",
            }
        ],
    },
}


@app.route("/")
def home():
    return render_template("index.html")


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

    students.append({"name": name, "branch": branch})
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

    if branch not in BRANCH_NAMES or not category:
        return redirect(url_for("student_form"))

    return render_template(
        "mentors.html",
        student_name=name,
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
