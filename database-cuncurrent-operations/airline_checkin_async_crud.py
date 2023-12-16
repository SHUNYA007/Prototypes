import asyncio
import mysql.connector
import aiomysql
import os 
from dotenv import load_dotenv
import airline_checking_crud as aircrud

load_dotenv()

database_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME")
}
connection = mysql.connector.connect(**database_config)


async def allocate_seats(conn,available_id,passenger_id):
    async with conn.cursor() as cur:
        await cur.execute("update seats_user_connection set passenger_id = "+str (passenger_id)+" where id = "+available_id+";")
        await conn.commit()


async def run_query(conn):
    async with conn.cursor() as cur:
        await cur.execute("SELECT id from `seats_user_connection` where passenger_id is null order by id limit 1")
        r = await cur.fetchall()
        return r[0][0]



async def insertValues(u): 
    available_id = await run_query(connection)
    allocate_seats(connection,available_id, u)

async def call_insert_values():
    user_ids = aircrud.get_all_user_ids()
    await asyncio.gather(*(insertValues(u) for u in user_ids))

asyncio.run(call_insert_values())
# print(len(user_ids))
# print(user_ids)
# async def test_example(loop):
#     pool = await aiomysql.create_pool(host=os.getenv("DB_HOST"),
#         user=os.getenv("DB_USER"),
#         password=os.getenv("DB_PASS"),
#         db=os.getenv("DB_NAME"), loop=loop)
    
    
#     async with pool.acquire() as conn:
#         for u in user_ids:
#            await asyncio.gather(available_seat  = await run_query(conn),await allocate_seats(conn,str(available_seat),str(u)))
            
            
#     pool.close()
#     await pool.wait_closed()



# aircrud.delete_all_allocated_seats_from_airplane(1)
# loop = asyncio.get_event_loop()
# loop.run_until_complete(test_example(loop))


aircrud.get_all_seats_allocated_for_airplane(1)

