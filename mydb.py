import mysql.connector

database=mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='root',
)
cursorobject=database.cursor()
cursorobject.execute('CREATE DATABASE custom')

print("all done")