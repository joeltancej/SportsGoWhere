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
  
5. Download and install MySQL Workbench (take note of host, user, password, database name)
(preferably host="localhost", database = 'sportsgowhere',user="root", passwd="password")
6. Set up local database and connection in MySQL Workbench
7. On your local database, import the 3 csv files with their respective names (e.g. sportsfacilities.csv as sportsfacilities Table)
8. On Visual Studio Code, open up the terminal and change directory to Flask_Learn (cd Flask_Learn)
9. Type the following commands:
with app.app_context():
  db.create_all()
10. Open up MySQL Workbench and check that there are 3 new tables: accounts, recentsearches, favorites
11. Open up Visual Studio code and run run.py
12. Open the IP address in your browser 
13. Enjoy our website
