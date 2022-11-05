import mysql.connector
import sys

# Connect MySQL
try:
    cnx = mysql.connector.connect(user='admin', password='********',
        host='database-1.c8tsrocn0rc8.eu-west-2.rds.amazonaws.com', port = 3306)
    cursor = cnx.cursor()
    print("Connected.")
except:
    print("Failed to connected.")
    _ = input("Press any key to continue: ")
    sys.exit()

# Create database
db = "books" # database name
table = "inventory"
try:
    cursor.execute(f"CREATE DATABASE {db}")
except:
    cursor.execute(f"DROP DATABASE {db}")
    cursor.execute(f"CREATE DATABASE {db}")

# Connect to database
cnx = mysql.connector.connect(user='admin', password='a1234567',
        host='database-1.c8tsrocn0rc8.eu-west-2.rds.amazonaws.com', port = 3306,
        database = db)
cursor = cnx.cursor()

# Create table
try:
    cursor.execute(f"CREATE TABLE {table} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), unit INT)")
    sql = f"INSERT INTO inventory (name, unit) VALUES (%s, %s)"
    val = [("Harry Potter", 1), ("Game of Thrones", 2)]
    for x in val:
        cursor.execute(sql, x)
    cnx.commit()
except:
    pass

condition = 0
while condition != 4:
    message = """\nWellcome to the main menu
    \t 1-Show all books available
    \t 2-Add book
    \t 3-Remove book
    \t 4-Exit
    """
    print(message)
    condition = int(input(""))

    if condition == 1:
        # Show all books
        cursor.execute(f"SELECT * FROM {table};")
        print("(ID, Name, Unit)")
        result = cursor.fetchall()
        for x in result:
            print(x)
        _ = input("\nPress any key to go back to the main menu: ")
    elif condition == 2:
        # Add book
        book_name = input("Enter the book name: ")
        
        # Find if the book exists in the table
        flag_exist = False
        index = -1
        unit = 1
        id = 0
        cursor.execute(f"SELECT * FROM {table};")
        result = cursor.fetchall()
        for i in range(len(result)):
            if result[i][1] == book_name:
                index = i
                unit = result[i][2]
                id = result[i][0]
                flag_exist = True
                break
        
        if (flag_exist):
            sql = f"UPDATE {table} SET unit = {unit + 1} where id = {id}"
            cursor.execute(sql)
        else:
            sql = f"INSERT INTO {table} (name, unit) VALUES (%s, %s)"
            val = (book_name, 1)
            cursor.execute(sql, val)
        cnx.commit()
        print(f"\nYou have added the book '{book_name}'.")
        _ = input("\nPress any key to go back to the main menu: ")
    elif condition == 3:
        # Remove book
        book_name = input("Enter the book name: ")
        
        # Find if the book exists in the table
        flag_exist = False
        index = -1
        unit = 1
        id = 0
        cursor.execute(f"SELECT * FROM {table};")
        result = cursor.fetchall()
        for i in range(len(result)):
            if result[i][1] == book_name:
                index = i
                unit = result[i][2]
                id = result[i][0]
                flag_exist = True
                break
        
        if (flag_exist):
            if (unit > 1):
                sql = f"UPDATE {table} SET unit = {unit - 1} where id = {id}"
            else:
                sql = f"DELETE FROM {table} WHERE id = {id}"
            print(f"\nUpdate completed.")
            cursor.execute(sql)
            cnx.commit()
        else:
            print(f"\nThere is no such book named '{book_name}'.")
        _ = input("\nPress any key to go back to the main menu: ")
# Drop the database before exit
print("Good bye!")
cursor.execute(f"Drop DATABASE {db}")
cursor.close()
cnx.close()
