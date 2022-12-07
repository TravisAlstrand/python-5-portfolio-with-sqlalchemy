from flask import render_template, url_for, request, redirect

from model import db, Project, app


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/projects/new')
def create_project():
  return render_template('projectform.html')


@app.route('/projects/<id>')
def project_detail(id):
  return render_template('detail.html')


@app.route('/projects/<id>/edit')
def edit_project(id):
  return render_template('projectform.html')


@app.route('/projects/<id>/delete')
def delete_project(id):
  return redirect(url_for('index.html'))


@app.route('/about')
def about():
  return render_template('about.html')


@app.errorhandler(404)
def not_found(error):
  return render_template('404.html', msg=error), 404


def add_products_to_db():
  pass


if __name__ == "__main__":
  with app.app_context():
    db.create_all()
  app.run(debug=True, port=8000, host='127.0.0.1')