from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os
import uuid
from datetime import datetime,date
from flask_mail import Mail, Message
import random
app = Flask(__name__)
app.secret_key = "smartgov_secret"
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'uploads/job_pdfs'
app.config["AD_UPLOAD_FOLDER"] = "static/ad_posts"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'iamniranjanxyz27@gmail.com'
app.config['MAIL_PASSWORD'] = 'wdyl fcpt vtku uxqp'
import re
mail = Mail(app)

db = SQLAlchemy(app)

# -----------------------------
# Database Models
# -----------------------------

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))



class Academy(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    academy_name = db.Column(db.String(200))

    email = db.Column(db.String(200), unique=True)

    password = db.Column(db.String(200))

    phone = db.Column(db.String(20))

    address = db.Column(db.String(300))

    district = db.Column(db.String(100))

    state = db.Column(db.String(100))

    pincode = db.Column(db.String(20))

    specialization = db.Column(db.String(200))   # UPSC / SSC / Banking / TNPSC

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
class AcademyCourse(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    academy_id = db.Column(db.Integer)

    course_name = db.Column(db.String(200))

    exam_type = db.Column(db.String(100))   # SSC / UPSC / Banking

    duration = db.Column(db.String(50))

    fees = db.Column(db.String(50))

    mode = db.Column(db.String(50))   # Online / Offline

    description = db.Column(db.Text)

    location = db.Column(db.String(200))
class AcademyAd(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    academy_id = db.Column(db.Integer)

    title = db.Column(db.String(200))

    file = db.Column(db.String(200))   # pdf / image

    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)



class GovernmentJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(200))
    department = db.Column(db.String(200))
    qualification = db.Column(db.String(200))
    age_limit = db.Column(db.String(100))
    location = db.Column(db.String(200))
    last_date = db.Column(db.String(100))
    description = db.Column(db.Text)
    pdf_file = db.Column(db.String(200))
    posted_date = db.Column(db.DateTime, default=datetime.utcnow)


class ChatMessage(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer)

    sender = db.Column(db.String(20))   # admin / student

    message = db.Column(db.Text)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    is_read = db.Column(db.Boolean, default=False)
class Student(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # ---------------------------
    # ACCOUNT INFORMATION
    # ---------------------------

    user_id = db.Column(db.String(20), unique=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(200))
    email = db.Column(db.String(120))
    mobile = db.Column(db.String(20))
    account_created = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    otp_status = db.Column(db.Boolean, default=False)

    # ---------------------------
    # PERSONAL DETAILS
    # ---------------------------

    full_name = db.Column(db.String(150))
    father_name = db.Column(db.String(150))
    mother_name = db.Column(db.String(150))
    dob = db.Column(db.Date)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    marital_status = db.Column(db.String(50))
    nationality = db.Column(db.String(100))
    religion = db.Column(db.String(100))
    aadhaar = db.Column(db.String(20))

    # ---------------------------
    # ADDRESS
    # ---------------------------

    permanent_address = db.Column(db.Text)
    current_address = db.Column(db.Text)
    village = db.Column(db.String(100))
    district = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(10))

    # ---------------------------
    # CATEGORY
    # ---------------------------

    category = db.Column(db.String(50))
    sub_category = db.Column(db.String(100))
    caste_certificate = db.Column(db.String(100))
    creamy_layer = db.Column(db.String(50))
    ews_certificate = db.Column(db.String(100))

    # ---------------------------
    # SPECIAL RESERVATION
    # ---------------------------

    pwd = db.Column(db.String(20))
    disability_type = db.Column(db.String(100))
    disability_percentage = db.Column(db.String(50))
    ex_serviceman = db.Column(db.String(20))
    defence_ward = db.Column(db.String(20))
    freedom_fighter = db.Column(db.String(20))
    sports_quota = db.Column(db.String(20))

    # ---------------------------
    # EDUCATION – 10th
    # ---------------------------

    tenth_board = db.Column(db.String(100))
    tenth_school = db.Column(db.String(200))
    tenth_year = db.Column(db.String(10))
    tenth_percentage = db.Column(db.String(10))
    tenth_subjects = db.Column(db.String(200))

    # ---------------------------
    # EDUCATION – 12th
    # ---------------------------

    twelfth_board = db.Column(db.String(100))
    twelfth_stream = db.Column(db.String(50))
    twelfth_school = db.Column(db.String(200))
    twelfth_year = db.Column(db.String(10))
    twelfth_percentage = db.Column(db.String(10))
    twelfth_subjects = db.Column(db.String(200))

    # ---------------------------
    # DIPLOMA
    # ---------------------------

    diploma_course = db.Column(db.String(150))
    diploma_branch = db.Column(db.String(150))
    diploma_institute = db.Column(db.String(200))
    diploma_university = db.Column(db.String(200))
    diploma_year = db.Column(db.String(10))
    diploma_percentage = db.Column(db.String(10))

    # ---------------------------
    # UG DEGREE
    # ---------------------------

    ug_degree = db.Column(db.String(100))
    ug_branch = db.Column(db.String(150))
    ug_college = db.Column(db.String(200))
    ug_university = db.Column(db.String(200))
    ug_mode = db.Column(db.String(50))
    ug_year = db.Column(db.String(10))
    ug_percentage = db.Column(db.String(10))

    # ---------------------------
    # PG DEGREE
    # ---------------------------

    pg_degree = db.Column(db.String(100))
    pg_specialization = db.Column(db.String(150))
    pg_college = db.Column(db.String(200))
    pg_university = db.Column(db.String(200))
    pg_year = db.Column(db.String(10))
    pg_percentage = db.Column(db.String(10))

    # ---------------------------
    # ADDITIONAL QUALIFICATIONS
    # ---------------------------

    phd = db.Column(db.String(100))
    professional_courses = db.Column(db.String(200))
    certifications = db.Column(db.String(200))

    # ---------------------------
    # NCC / DEFENCE
    # ---------------------------

    ncc_certificate = db.Column(db.String(20))
    ncc_division = db.Column(db.String(50))
    ncc_grade = db.Column(db.String(10))
    service_preference = db.Column(db.String(50))
def calculate_age(dob):

    today = date.today()

    return today.year - dob.year - (
        (today.month, today.day) < (dob.month, dob.day)
    )

def generate_otp():
    return str(random.randint(100000,999999))
import re
education_levels = {
    "10th pass": 1,
    "sslc": 1,

    "12th pass": 2,
    "+2": 2,
    "hsc": 2,

    "diploma": 3,

    "any degree": 4,
    "b.e": 4,
    "b.tech": 4,
    "b.sc": 4,
    "b.com": 4,
    "b.a": 4,

    "post graduate": 5,
    "m.e": 5,
    "m.tech": 5,
    "m.sc": 5,
    "mba": 5
}
def get_student_level(student):

    if student.pg_degree:
        return 5

    if student.ug_degree:
        return 4

    if student.diploma_course:
        return 3

    if student.twelfth_board:
        return 2

    if student.tenth_board:
        return 1

    return 0
def get_job_level(job):

    job_q = job.qualification.lower()

    for key, value in education_levels.items():

        if key in job_q:
            return value

    return 0
def check_age(student, job):

    if not job.age_limit:
        return True

    try:

        parts = job.age_limit.split("-")

        min_age = int(parts[0])
        max_age = int(parts[1])

        return min_age <= student.age <= max_age

    except:
        return True
def match_job(student, job):

    score = 0

    student_level = get_student_level(student)
    job_level = get_job_level(job)

    # Qualification eligibility
    if student_level >= job_level:

        score += 60

        # exact qualification match
        if student_level == job_level:
            score += 20

        # branch relevance
        if student.ug_branch:

            branch = student.ug_branch.lower()

            if branch in (job.description or "").lower():
                score += 20

    # Age eligibility
    if check_age(student, job):
        score += 10
    else:
        return 0

    return min(score,100)

def recommend_jobs(student):

    jobs = GovernmentJob.query.all()

    recommendations = []

    for job in jobs:

        score = match_job(student, job)

        if score >= 50:

            recommendations.append({
                "job": job,
                "score": score
            })

    recommendations.sort(key=lambda x: x["score"], reverse=True)

    return recommendations[:5]
def recommend_academies(student):

    recommended_jobs = recommend_jobs(student)

    exam_types = set()

    # Detect exam types from recommended jobs
    for item in recommended_jobs:

        job = item["job"]
        title = (job.job_title or "").lower()

        if "ssc" in title:
            exam_types.add("SSC")

        if "upsc" in title:
            exam_types.add("UPSC")

        if "bank" in title:
            exam_types.add("Banking")

        if "tnpsc" in title:
            exam_types.add("TNPSC")

        if "railway" in title:
            exam_types.add("Railway")

        if "defence" in title or "army" in title:
            exam_types.add("Defence")

    courses = AcademyCourse.query.all()

    recommendations = []

    for c in courses:

        score = 0

        course_exam = (c.exam_type or "").lower()

        for exam in exam_types:

            if exam.lower() in course_exam:

                score += 60

        # additional scoring
        if student.ug_degree:
            score += 20

        if student.twelfth_board:
            score += 10

        if student.category:
            score += 10

        if score >= 60:

            # get advertisement for academy
            ad = AcademyAd.query.filter_by(
                academy_id=c.academy_id
            ).first()

            recommendations.append({
                "course": c,
                "score": score,
                "ad": ad
            })

    recommendations.sort(key=lambda x: x["score"], reverse=True)

    return recommendations[:5]
# -----------------------------
# HOME PAGE
# -----------------------------

@app.route("/")
def home():

    jobs = GovernmentJob.query.order_by(GovernmentJob.posted_date.desc()).limit(5).all()

    return render_template("home.html", jobs=jobs)


# -----------------------------
# ADMIN LOGIN
# -----------------------------

@app.route("/admin", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        admin = Admin.query.filter_by(username=username, password=password).first()

        if admin:
            session["admin"] = username
            return redirect(url_for("admin_dashboard"))

        else:
            flash("Invalid login")

    return render_template("admin_login.html")


# -----------------------------
# ADMIN DASHBOARD
# -----------------------------

@app.route("/admin/dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect(url_for("admin_login"))

    student_count = Student.query.count()
    academy_count = Academy.query.count()
    job_count = GovernmentJob.query.count()

    recent_jobs = GovernmentJob.query.order_by(
        GovernmentJob.posted_date.desc()
    ).limit(5).all()

    return render_template(
        "admin_dashboard.html",
        students=student_count,
        academies=academy_count,
        jobs=job_count,
        recent_jobs=recent_jobs
    )


# -----------------------------
# UPLOAD GOVERNMENT JOB
# -----------------------------

@app.route("/admin/upload_job", methods=["GET", "POST"])
def upload_job():

    if "admin" not in session:
        return redirect(url_for("admin_login"))

    if request.method == "POST":

        job_title = request.form["job_title"]
        department = request.form["department"]
        qualification = request.form["qualification"]
        age_limit = request.form["age_limit"]
        location = request.form["location"]
        last_date = request.form["last_date"]
        description = request.form["description"]

        pdf = request.files["pdf_file"]

        filename = pdf.filename
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        pdf.save(path)

        # Create job object
        new_job = GovernmentJob(
            job_title=job_title,
            department=department,
            qualification=qualification,
            age_limit=age_limit,
            location=location,
            last_date=last_date,
            description=description,
            pdf_file=filename
        )

        db.session.add(new_job)
        db.session.commit()

        # -------------------------------
        # Send email notifications
        # -------------------------------

        students = Student.query.all()

        for student in students:

            score = match_job(student, new_job)

            if score >= 60:

                msg = Message(
                    "New Government Job Matching Your Profile",
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[student.email]
                )

                msg.body = f"""
Hello {student.full_name},

A new government job matches your profile.

Job Title: {new_job.job_title}
Department: {new_job.department}

Match Score: {score}%

Login to SmartGov portal to view details.

Regards,
SmartGov System
"""

                mail.send(msg)

        flash("Job uploaded successfully")

        return redirect(url_for("view_jobs"))

    return render_template("upload_job.html")


# -----------------------------
# VIEW JOBS
# -----------------------------

@app.route("/admin/jobs")
def view_jobs():

    if "admin" not in session:
        return redirect(url_for("admin_login"))

    jobs = GovernmentJob.query.order_by(GovernmentJob.posted_date.desc()).all()

    return render_template("view_jobs.html", jobs=jobs)


# -----------------------------
# FILTER JOBS
# -----------------------------

@app.route("/admin/filter_jobs", methods=["POST"])
def filter_jobs():

    qualification = request.form["qualification"]

    jobs = GovernmentJob.query.filter_by(qualification=qualification).all()

    return render_template("view_jobs.html", jobs=jobs)


# -----------------------------
# DOWNLOAD JOB PDF
# -----------------------------

@app.route("/download/<filename>")
def download_pdf(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/admin/delete_job/<int:id>")
def delete_job(id):

    job = GovernmentJob.query.get(id)

    db.session.delete(job)
    db.session.commit()

    flash("Job deleted successfully")

    return redirect(url_for("view_jobs"))
# -----------------------------
# ADMIN CHAT
# -----------------------------

@app.route("/admin/chat")
def admin_chat():

    if "admin" not in session:
        return redirect(url_for("admin_login"))

    students = db.session.query(Student).join(
        ChatMessage,
        Student.id == ChatMessage.student_id
    ).distinct().all()

    student_data = []

    for s in students:

        unread = ChatMessage.query.filter_by(
            student_id=s.id,
            sender="student",
            is_read=False
        ).count()

        student_data.append({
            "student": s,
            "unread": unread
        })

    return render_template(
        "admin_chat_dashboard.html",
        students=student_data
    )
@app.route("/admin/chat/<int:student_id>")
def admin_chat_user(student_id):

    if "admin" not in session:
        return redirect(url_for("admin_login"))

    student = Student.query.get(student_id)

    messages = ChatMessage.query.filter_by(
        student_id=student_id
    ).order_by(ChatMessage.timestamp.asc()).all()

    # mark messages as read
    ChatMessage.query.filter_by(
        student_id=student_id,
        sender="student"
    ).update({"is_read": True})

    db.session.commit()

    return render_template(
        "admin_chat.html",
        student=student,
        messages=messages
    )
@app.route("/admin/send_message/<int:student_id>", methods=["POST"])
def admin_send_message(student_id):

    if "admin" not in session:
        return redirect(url_for("admin_login"))

    message = request.form["message"]

    chat = ChatMessage(
        student_id=student_id,
        sender="admin",
        message=message
    )

    db.session.add(chat)
    db.session.commit()

    return "OK"
@app.route("/get_messages/<int:student_id>")
def get_messages(student_id):

    messages = ChatMessage.query.filter_by(
        student_id=student_id
    ).order_by(ChatMessage.timestamp.asc()).all()

    data = []

    for m in messages:

        data.append({
            "sender": m.sender,
            "message": m.message
        })

    return {"messages": data}

@app.route("/student/register", methods=["GET", "POST"])
def student_register():

    if request.method == "POST":

        # OTP verification check
        if not session.get("otp_verified"):
            flash("Please verify your email OTP first")
            return redirect(url_for("student_register"))

        # Handle DOB safely
        dob_str = request.form.get("dob")

        if dob_str:
            dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
            age = calculate_age(dob)
        else:
            dob = None
            age = None

        # Generate Student ID
        user_id = "STU" + str(uuid.uuid4().hex[:6]).upper()

        student = Student(

            user_id=user_id,
            username=request.form.get("username"),
            password=request.form.get("password"),
            email=request.form.get("email"),
            mobile=request.form.get("mobile"),

            full_name=request.form.get("full_name"),
            father_name=request.form.get("father_name"),
            mother_name=request.form.get("mother_name"),
            dob=dob,
            age=age,
            gender=request.form.get("gender"),
            marital_status=request.form.get("marital_status"),
            nationality=request.form.get("nationality"),
            religion=request.form.get("religion"),
            aadhaar=request.form.get("aadhaar"),

            permanent_address=request.form.get("permanent_address"),
            current_address=request.form.get("current_address"),
            village=request.form.get("village"),
            district=request.form.get("district"),
            state=request.form.get("state"),
            pincode=request.form.get("pincode"),

            category=request.form.get("category"),
            sub_category=request.form.get("sub_category"),
            caste_certificate=request.form.get("caste_certificate"),
            creamy_layer=request.form.get("creamy_layer"),
            ews_certificate=request.form.get("ews_certificate"),

            pwd=request.form.get("pwd"),
            disability_type=request.form.get("disability_type"),
            disability_percentage=request.form.get("disability_percentage"),
            ex_serviceman=request.form.get("ex_serviceman"),
            defence_ward=request.form.get("defence_ward"),
            freedom_fighter=request.form.get("freedom_fighter"),
            sports_quota=request.form.get("sports_quota"),

            tenth_board=request.form.get("tenth_board"),
            tenth_school=request.form.get("tenth_school"),
            tenth_year=request.form.get("tenth_year"),
            tenth_percentage=request.form.get("tenth_percentage"),
            tenth_subjects=request.form.get("tenth_subjects"),

            twelfth_board=request.form.get("twelfth_board"),
            twelfth_stream=request.form.get("twelfth_stream"),
            twelfth_school=request.form.get("twelfth_school"),
            twelfth_year=request.form.get("twelfth_year"),
            twelfth_percentage=request.form.get("twelfth_percentage"),
            twelfth_subjects=request.form.get("twelfth_subjects"),

            diploma_course=request.form.get("diploma_course"),
            diploma_branch=request.form.get("diploma_branch"),
            diploma_institute=request.form.get("diploma_institute"),
            diploma_university=request.form.get("diploma_university"),
            diploma_year=request.form.get("diploma_year"),
            diploma_percentage=request.form.get("diploma_percentage"),

            ug_degree=request.form.get("ug_degree"),
            ug_branch=request.form.get("ug_branch"),
            ug_college=request.form.get("ug_college"),
            ug_university=request.form.get("ug_university"),
            ug_mode=request.form.get("ug_mode"),
            ug_year=request.form.get("ug_year"),
            ug_percentage=request.form.get("ug_percentage"),

            pg_degree=request.form.get("pg_degree"),
            pg_specialization=request.form.get("pg_specialization"),
            pg_college=request.form.get("pg_college"),
            pg_university=request.form.get("pg_university"),
            pg_year=request.form.get("pg_year"),
            pg_percentage=request.form.get("pg_percentage"),

            phd=request.form.get("phd"),
            professional_courses=request.form.get("professional_courses"),
            certifications=request.form.get("certifications"),

            ncc_certificate=request.form.get("ncc_certificate"),
            ncc_division=request.form.get("ncc_division"),
            ncc_grade=request.form.get("ncc_grade"),
            service_preference=request.form.get("service_preference")
        )

        db.session.add(student)
        db.session.commit()

        flash("Registration Successful")

        session.pop("otp_verified", None)

        return redirect(url_for("student_login"))

    return render_template("student_register.html")
@app.route("/send_otp", methods=["POST"])
def send_otp():

    email = request.form["email"]

    otp = generate_otp()

    session["email_otp"] = otp
    session["otp_email"] = email

    # DEBUG: Print OTP to console for local testing
    print(f"\n{'='*20}")
    print(f"DEBUG - OTP Sent: {otp}")
    print(f"Target Email: {email}")
    print(f"{'='*20}\n")

    msg = Message(
        "SmartGov Email Verification OTP",
        sender='iamniranjanxyz27@gmail.com',  # ✅ your verified email
        recipients=[email]
    )

    msg.body = f"""
    SmartGov Career Portal

    Your Email Verification OTP is: {otp}

    Do not share this OTP with anyone.
    """

    try:
        mail.send(msg)
        print("OTP sent successfully")   # helpful for Render logs
    except Exception as e:
        print("Mail error:", e)          # VERY IMPORTANT for debugging

    return {"status": "OTP Sent"}
@app.route("/verify_otp", methods=["POST"])
def verify_otp():

    otp = request.form["otp"]

    if otp == session.get("email_otp"):

        session["otp_verified"] = True
        return {"status":"verified"}

    return {"status":"invalid"}
@app.route("/academy/register", methods=["GET","POST"])
def academy_register():

    if request.method == "POST":

        academy = Academy(

            academy_name=request.form["academy_name"],
            email=request.form["email"],
            password=request.form["password"],
            phone=request.form["phone"],
            address=request.form["address"],
            district=request.form["district"],
            state=request.form["state"],
            pincode=request.form["pincode"],
            specialization=request.form["specialization"]
        )

        db.session.add(academy)
        db.session.commit()

        flash("Academy registered successfully")

        return redirect(url_for("academy_login"))

    return render_template("academy_register.html")
@app.route("/academy/login", methods=["GET","POST"])
def academy_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        academy = Academy.query.filter_by(
            email=email,
            password=password
        ).first()

        if academy:

            session["academy_id"] = academy.id
            session["academy_name"] = academy.academy_name

            return redirect(url_for("academy_dashboard"))

        else:
            flash("Invalid login")

    return render_template("academy_login.html")
@app.route("/academy/dashboard")
def academy_dashboard():

    if "academy_id" not in session:
        return redirect(url_for("academy_login"))

    academy_id = session["academy_id"]

    courses = AcademyCourse.query.filter_by(
        academy_id=academy_id
    ).all()

    ads = AcademyAd.query.filter_by(
        academy_id=academy_id
    ).all()

    return render_template(
        "academy_dashboard.html",
        courses=courses,
        ads=ads
    )
@app.route("/academy/upload_course", methods=["GET","POST"])
def upload_course():

    if "academy_id" not in session:
        return redirect(url_for("academy_login"))

    if request.method == "POST":

        course = AcademyCourse(

            academy_id=session["academy_id"],

            course_name=request.form["course_name"],

            exam_type=request.form["exam_type"],

            duration=request.form["duration"],

            fees=request.form["fees"],

            mode=request.form["mode"],

            description=request.form["description"],

            location=request.form["location"]
        )

        db.session.add(course)
        db.session.commit()

        flash("Course uploaded successfully")

        return redirect(url_for("academy_dashboard"))

    return render_template("upload_course.html")
@app.route("/academy/upload_ad", methods=["GET","POST"])
def upload_ad():

    if "academy_id" not in session:
        return redirect(url_for("academy_login"))

    if request.method == "POST":

        file = request.files["file"]

        if file:

            filename = secure_filename(file.filename)

            save_path = os.path.join(
                app.config["AD_UPLOAD_FOLDER"],
                filename
            )

            file.save(save_path)

            ad = AcademyAd(

                academy_id=session["academy_id"],

                title=request.form["title"],

                file=filename
            )

            db.session.add(ad)
            db.session.commit()

            flash("Advertisement uploaded successfully")

            return redirect(url_for("academy_dashboard"))

    return render_template("upload_ad.html")
@app.route("/academy/logout")
def academy_logout():

    session.pop("academy_id", None)

    return redirect(url_for("academy_login"))
@app.route("/academy/delete_course/<int:id>")
def delete_course(id):

    course = AcademyCourse.query.get(id)

    db.session.delete(course)

    db.session.commit()

    flash("Course deleted successfully")

    return redirect(url_for("academy_dashboard"))
@app.route("/academy/delete_ad/<int:id>")
def delete_ad(id):

    ad = AcademyAd.query.get(id)

    db.session.delete(ad)

    db.session.commit()

    flash("Advertisement deleted")

    return redirect(url_for("academy_dashboard"))

@app.route("/student/login", methods=["GET","POST"])
def student_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        student = Student.query.filter_by(
            username=username,
            password=password
        ).first()

        if student:

            session["student_id"] = student.id
            session["student_name"] = student.full_name

            student.last_login = datetime.utcnow()

            db.session.commit()

            flash("Login Successful")

            return redirect(url_for("student_dashboard"))

        else:

            flash("Invalid Username or Password")

            return redirect(url_for("student_login"))

    return render_template("student_login.html")
@app.route("/student/dashboard")
def student_dashboard():

    if "student_id" not in session:
        return redirect(url_for("student_login"))

    student = Student.query.get(session["student_id"])

    # AI recommended jobs
    recommended_jobs = recommend_jobs(student)

    # Latest matched jobs only
    all_jobs = GovernmentJob.query.order_by(
        GovernmentJob.id.desc()
    ).limit(10).all()

    latest_jobs = []

    for job in all_jobs:

        score = match_job(student, job)

        if score >= 60:   # same condition used for email
            latest_jobs.append({
                "job": job,
                "score": score
            })

    academies = recommend_academies(student)

    return render_template(
        "student_dashboard.html",
        student=student,
        recommended_jobs=recommended_jobs,
        latest_jobs=latest_jobs,
        academies=academies
    )
@app.route("/student/delete_profile")
def delete_student():

    if "student_id" not in session:
        return redirect(url_for("student_login"))

    student = Student.query.get(session["student_id"])

    db.session.delete(student)
    db.session.commit()

    session.clear()

    flash("Your profile has been deleted")

    return redirect(url_for("home"))
@app.route("/student/chat", methods=["GET","POST"])
def student_chat():

    if "student_id" not in session:
        return redirect(url_for("student_login"))

    student_id = session["student_id"]

    if request.method == "POST":

        msg = ChatMessage(
            student_id=student_id,
            sender="student",
            message=request.form["message"]
        )

        db.session.add(msg)
        db.session.commit()

        return "OK"

    return render_template("student_chat.html")
# @app.route("/get_messages")
# def get_messages():

#     messages = ChatMessage.query.order_by(
#         ChatMessage.timestamp.asc()
#     ).all()

#     data = []

#     for m in messages:

#         data.append({
#             "sender": m.sender,
#             "message": m.message
#         })

#     return {"messages": data}

@app.route("/student/logout")
def student_logout():

    session.pop("student_id", None)
    session.pop("student_name", None)

    flash("Logged Out Successfully")

    return redirect(url_for("student_login"))
        # Continue registration process
# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect(url_for("home"))
@app.route("/admin/logout")
def logout1():

    session.pop("admin", None)

    return redirect(url_for("home"))

with app.app_context():

    db.create_all()

    admin = Admin.query.filter_by(username="admin").first()

    if not admin:
        new_admin = Admin(username="admin", password="admin123")
        db.session.add(new_admin)
        db.session.commit()
# -----------------------------
# RUN APP
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)