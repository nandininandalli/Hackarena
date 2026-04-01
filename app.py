from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# Initialize app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret123'

# Initialize database
db = SQLAlchemy(app)

# ---------------- MODELS ---------------- #

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.String(200), nullable=False)
    interest = db.Column(db.String(200), nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)

# ---------------- HELPER FUNCTION ---------------- #

def get_role(skills):
    skills = skills.lower()
    if "python" in skills or "java" in skills:
        return "Developer"
    elif "marketing" in skills or "business" in skills:
        return "Business"
    elif "design" in skills or "ui" in skills:
        return "Designer"
    return "Other"

# ---------------- ROUTES ---------------- #

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        skills = request.form.get('skills')
        interest = request.form.get('interest')

        if name and skills and interest:
            user = User(name=name, skills=skills, interest=interest)
            db.session.add(user)
            db.session.commit()

            return redirect('/dashboard')

    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    users = User.query.all()
    teams = []

    for i in range(len(users)):
        for j in range(i + 1, len(users)):
            u1 = users[i]
            u2 = users[j]

            if u1.interest == u2.interest:
                if get_role(u1.skills) != get_role(u2.skills):
                    teams.append((u1, u2))

    return render_template('dashboard.html', teams=teams)
@app.route('/create_project', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')

        if name and description:
            project = Project(name=name, description=description)
            db.session.add(project)
            db.session.commit()

            return redirect('/projects')

    return render_template('create_project.html')


@app.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)
@app.route('/project/<int:id>')
def project_detail(id):
    project = Project.query.get(id)
    return render_template('project_detail.html', project=project)


# ---------------- MAIN ---------------- #

if __name__ == '__main__':
    with app.app_context():
        db.create_all()   # Creates database tables
    app.run(debug=True)