import mysql.connector

cnx = mysql.connector.MySQLConnection(
    user="mongouhd_evernorth",
    password="U*dgQkKRuEHe",
    host="cp-15.webhostbox.net",
    database="mongouhd_evernorth",
    port=3306,
)
if cnx.is_connected():
    print("Connected")
cursor = cnx.cursor()
cursor.close()
cnx.close()
