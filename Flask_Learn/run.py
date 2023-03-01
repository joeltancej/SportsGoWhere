# save this as run.py
# For anyone who is facing the error of 'outside application context', try this :
#  -   in your terminal: from <your_app> import app, db
#  -   with app.app_context():
#               db.create_all()
#
# Note: You can use this also when you will want to add data to the database. GoodLuck!
# from markupsafe import escape
from flaskblog import app


if __name__ == '__main__':
    app.run(debug=True)
