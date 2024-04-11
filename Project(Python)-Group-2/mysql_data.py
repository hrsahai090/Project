import mysql.connector

def sql_data(self):
    self.conn = mysql.connector.connect(host="localhost",  user="root",password="123456", database="new_Parking_project")
    