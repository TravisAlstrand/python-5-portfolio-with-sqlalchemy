from flask import render_template, url_for, request, redirect
from model import db, Project, app
from os.path import exists
import data_to_db


@app.route('/')
def index():
  projects = Project.query.all()
  return render_template('index.html', projects=projects)


@app.route('/projects/new', methods=['GET', 'POST'])
def create_project():
  projects = Project.query.all()
  if request.form:
    new_product = Project(title=request.form['title'],
                          date=data_to_db.clean_date(request.form['date']),
                          description=request.form['desc'],
                          skills=request.form['skills'],
                          gh_link=request.form['github'])
    db.session.add(new_product)
    db.session.commit()
    return redirect(url_for('index'))
  return render_template('projectform.html', projects=projects)


@app.route('/projects/<id>')
def project_detail(id):
  projects = Project.query.all()
  project = Project.query.get_or_404(id)
  project.date = project.date.strftime('%m/%d/%Y')
  project.skills = project.skills.split(', ')
  return render_template('detail.html', project=project, projects=projects)


@app.route('/projects/<id>/edit', methods=['GET', 'POST'])
def edit_project(id):
  projects = Project.query.all()
  project = Project.query.get_or_404(id)
  if request.form:
    project.title = request.form['title']
    project.date = data_to_db.clean_date(request.form['date'])
    project.description = request.form['desc']
    project.skills = request.form['skills']
    project.gh_link = request.form['github']
    db.session.commit()
    return redirect(url_for('project_detail', id=id))
  project.date = project.date.strftime('%Y-%m-%d')
  return render_template('editform.html', project=project, projects=projects)


@app.route('/projects/<id>/delete')
def delete_project(id):
  project = Project.query.get_or_404(id)
  db.session.delete(project)
  db.session.commit()
  return redirect(url_for('index'))


@app.route('/about')
def about():
  projects = Project.query.all()
  return render_template('about.html', projects=projects)


@app.errorhandler(404)
def not_found(error):
  projects = Project.query.all()
  return render_template('404.html', msg=error, projects=projects), 404


if __name__ == "__main__":
  db_exists = exists('./instance/projects.db')
  if db_exists == False:
    with app.app_context():
      db.create_all()
    data_to_db.populate_db()
    
  app.run(debug=True, port=8000, host='127.0.0.1')