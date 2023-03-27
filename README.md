# SportsGoWhere

Steps to install and run project:
1. Clone github repository
2. Open repository in Visual Studio Code
3. Open up the terminal on Visual Studio Code
4. install these packages\
&emsp;&emsp; pip install flask\
&emsp;&emsp; pip install mysqlclient\
&emsp;&emsp; pip install image\
&emsp;&emsp; pip install flask-wtf\
&emsp;&emsp; pip install email_validator\
&emsp;&emsp; pip install flask-mysqldb\
&emsp;&emsp; pip install requests\
&emsp;&emsp; pip install pandas
  
5. Download and install MySQL Workbench (preferably host="localhost", database = 'sportsgowhere',user="root", password="password")
6. Open up Visual Studio Code and edit the following files with the correct values for host, user, password, database:
&emsp;&emsp; app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:password@localhost/sportsgowhere" (line 13 in __init__.py)
&emsp;&emsp; mydb = mysql.connector.connect(host="localhost", user="root", password="password", database="sportsgowhere") (line 70 in routes.py)
&emsp;&emsp; mydb = connection.connect(host="localhost", database = 'sportsgowhere',user="root", passwd="password",use_pure=True) (line 12 in nearestCarparks.py)
&emsp;&emsp; mydb = connection.connect(host="localhost", database = 'sportsgowhere',user="root", passwd="password",use_pure=True) (line 11 in nearestEateries.py)
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
