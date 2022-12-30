import mysql.connector

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="mysql123"
)
print(mydb)