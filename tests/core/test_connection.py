from ...core.databr import get_connection

con = get_connection()
print("Connection successful")
con.close()