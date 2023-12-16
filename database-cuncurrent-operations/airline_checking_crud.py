import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
def convertToDict(tuples):
    d = dict()
    for tup in tuples:
        if(tup[0] in d.keys()):
            d[tup[0]] = 'x'
        else:
            d[tup[0]] = str(tup[1])
    
    return d

def show_all_occupied_seats(seatsDict : dict):
    count = 1
    current_seat = 0
    for seat in range(1,1201):
        if (count - 1) % 3 == 0:
            print(' ', end = ' ') 
        if (count-1) % 12 == 0:
            print()
            count = 1
        count += 1
        if(seat in seatsDict.keys()):
            if(seatsDict[seat] ==  None):
                print('.',end = ' ')     
            else:
                print(seatsDict[seat],end = ' ')
                
        else :
            print('.',end = ' ')


def get_all_seats_allocated_for_airplane(id):
    connection = mysql.connector.connect(**database_config)
    cursor = connection.cursor() 
    sql_query = "select seat_id,passenger_id FROM `seats_user_connection` where plane_id = " + str(id)
    cursor.execute(sql_query)
    seats_allocated = cursor.fetchall()
    seats_allocated = [i for i in seats_allocated if i[1] != None]
    connection.close()
        
    show_all_occupied_seats(convertToDict( seats_allocated))

def delete_all_allocated_seats_from_airplane(id):
    connection = mysql.connector.connect(**database_config)
    cursor = connection.cursor()  
    sql_query = "UPDATE `seats_user_connection` SET passenger_id = null where plane_id = " + str(id)
    cursor.execute(sql_query)
    connection.commit()
    connection.close()

def allocate_seats(user_id, plane_id, seat_id):
    connection = mysql.connector.connect(**database_config)
    cursor = connection.cursor()  
    sql_query = "insert into  seats_user_connection(seat_id,plane_id,passenger_id) values("+seat_id+","+plane_id+","+user_id+")"
    cursor.execute(sql_query)
    connection.commit()
    connection.close()

def insert_names_from_file(cursor,connection):
    with open("names.txt", "r") as f:
        names = [line.strip() for line in f]

    sql_query = "INSERT INTO `user` (name) VALUES (%s)"
    names_tuples = [(name,) for name in names]
    cursor.executemany(sql_query, names_tuples)
    connection.commit()

def get_all_users(cursor,connection):
    sql_query = "SELECT * FROM `user`"
    cursor.execute(sql_query)
    user = cursor.fetchall()
    print(user)
    connection.commit()


def delete_user_table(cursor,connection):
    sql_query = "DELETE FROM `user`"
    cursor.execute(sql_query)
    connection.commit()

def create_seats(cursor, connection):
    seats  = []
    for i in range(1,201):
        for j in range (ord('A'), ord('F')+1):
            seat_name = str(i) + '-' + chr(j)
            seats.append((seat_name,))
    print(seats)
    sql_query = "INSERT INTO `airplane_seats` (name) VALUES (%s)"
    cursor.executemany(sql_query,seats)
    connection.commit()

def make_seats_for_plane(conn,cursor,plane_id):
    sql_query = "SELECT id FROM airplane_seats"
    cursor.execute(sql_query)
    seat_ids = cursor.fetchall()
    seat_ids  = [i[0] for i in seat_ids ]
    for i in seat_ids:
        sql_query = "insert into  seats_user_connection(seat_id,plane_id) values("+str(i)+","+str(plane_id)+");"
        cursor.execute(sql_query)
    conn.commit()

def get_all_user_ids():
    connection = mysql.connector.connect(**database_config)
    cursor = connection.cursor()    
    sql_query = "SELECT id FROM `user` order by id"
    cursor.execute (sql_query)
    user_ids = cursor.fetchall()
    connection.close()
    return [i[0] for i in user_ids]

database_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME")
}

connection = mysql.connector.connect(**database_config)
# cursor = connection.cursor()
# insert_names_from_file(cursor,connection)
# get_all_users(cursor,connection)
# delete_user_table(cursor,connection)
# create_seats(cursor, connection)
# allocate_seats(cursor,connection,str(1),str(1),str(12))
# get_all_seats_allocated_for_airplane(cursor,connection,1)  
# delete_all_allocated_seats_from_airplane(cursor,connection,1)

# print("user ids")
# # print(get_all_user_ids(cursor, connection))
# # make_seats_for_plane(connection,cursor,1)
# # delete_all_allocated_seats_from_airplane(cursor,connection,str(1))
# print('ssuccess')
# connection.close()