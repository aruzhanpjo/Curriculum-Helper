import os
import mysql.connector
import pandas as pd


db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

cursor = connection.cursor(dictionary=True)

while True:
    findVal = int(input("How many goal areas do you want to cover? Out of 3. (You can include W and L as well)\n"))
    if findVal <= 3:
        break
    print("Invalid input. Please try again.")


goalArea = set()
for i in range(findVal):
    val = input(f"Enter goal area {i + 1}: ")
    goalArea.add(val)


goalArea_conditions = []
contains_w_condition = ""


if 'W' in goalArea:
    contains_w_condition = "contains_W = 1"


for area in goalArea:
    if area != 'W':  
        goalArea_conditions.append(f"area LIKE '%{area}%'")

if contains_w_condition:

    query_conditions = " AND ".join(goalArea_conditions + [contains_w_condition])
else:

    query_conditions = " OR ".join(goalArea_conditions)


if query_conditions:
    query = f"""
    SELECT short_name, name, credits, area
    FROM goalAreasDataBase
    WHERE {query_conditions};
    """
else:
    query = "SELECT short_name, name, credits, area FROM goalAreasDataBase;"

cursor.execute(query)


filtered_data = cursor.fetchall()


df = pd.DataFrame(filtered_data)


if not df.empty:
    print(df)  
else:
    print("No classes found. Try different goal areas.")


cursor.close()
connection.close()