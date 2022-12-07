from model import db, Project, app
import datetime
import json


def clean_date(date_str):
  split_date = date_str.split('/')
  month = int(split_date[0])
  day = int(split_date[1])
  year = int(split_date[2])
  date_obj = datetime.date(year, month, day)
  return date_obj

def clean_skills(skill_list):
  skill_str = ', '.join(skill_list)
  return skill_str


def populate_db():
  with app.app_context():
    with open('data.json') as datafile:
      data = json.load(datafile)
      i = 1
      while i <= len(data):
        new_product = Project(title=data['project' + str(i)]['title'],
                              date=clean_date(data['project' + str(i)]['date']),
                              description=data['project' + str(i)]['description'],
                              skills=clean_skills(data['project' + str(i)]['skills']),
                              gh_link=data['project' + str(i)]['gh_link'])
        db.session.add(new_product)
        db.session.commit()
        i += 1
