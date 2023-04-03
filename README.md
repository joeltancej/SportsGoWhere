# SportsGoWhere

Steps to install and run project:
1. Clone github repository
2. Open repository in Visual Studio Code
3. Open up the terminal on Visual Studio Code
4. Check requirements:
  Flask==2.2.2
  Flask_Bcrypt==1.0.1
  Flask_Login==0.6.2
  flask_sqlalchemy==3.0.3
  Flask_WTF==1.1.1
  itsdangerous==2.1.2
  mysql_connector_repackaged==0.3.1
  pandas==1.3.5
  python_bcrypt==0.3.2
  pytz==2021.3
  requests==2.25.1
  SQLAlchemy==2.0.4
  WTForms==3.0.1

5. Download and install MySQL Workbench (preferably host="localhost", database = 'sportsgowhere',user="root", password="password")
6. Open up Visual Studio Code and edit the following files with the correct values for host, user, password, database:

  (1) app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:password@localhost/sportsgowhere" 
  (line 13 in __init__.py)

  (2) mydb = mysql.connector.connect(host="localhost", user="root", password="password", database="sportsgowhere") 
  (line 70 in routes.py)

  (3) mydb = connection.connect(host="localhost", database = 'sportsgowhere',user="root", passwd="password",use_pure=True) 
  (line 12 in nearestCarparks.py)

  (4) mydb = connection.connect(host="localhost", database = 'sportsgowhere',user="root", passwd="password",use_pure=True) 
  (line 11 in nearestEateries.py)

7. Set up local database and connection in MySQL Workbench
8. On your local database, import the 3 csv files with their respective names (e.g. sportsfacilities.csv as sportsfacilities Table)
9. On Visual Studio Code, open up the terminal and change directory to Flask_Learn (cd Flask_Learn)
10. Type the following commands:
with app.app_context():
  db.create_all()
11. Open up MySQL Workbench and check that there are 3 new tables: accounts, recentsearches, favorites
12. Open up Visual Studio code and run run.py
13. Open the IP address in your browser 
14. Enjoy our website
---
### File and Logic Organisation
- SportsGoWhere/Flask_Learn/run.py: runs the application
- Datasets directory: csv files for carparks, eateries, and sports facilities
- Flask_Learn/NearestFinder: Python logic files to find nearest carparks, eateries, and implement geolocation.
- Flask_Learn/flaskblog/routes.py: Contol functions to respond to user inputs and render required html file. 
- Flask_Learn/flaskblog/apimanagers.py: Python code to provide interface for carpark, PSI, datetime, and weather APIs. 
- Flask_Learn/flaskblog/models.py: Creates the tables for the entities and establishes relation between datasets.
- SportsGoWhere/Flask_Learn/flaskblog/templates: directory contains all html files which each correspond to a view. 

