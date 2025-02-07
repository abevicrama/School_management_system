import mysql.connector


mydb = mysql.connector.connect(
    host = "localhost",
    user ="root",
    password = "",
    database = "school_management_system"
)

mycurser = mydb.cursor()
print("connected")
