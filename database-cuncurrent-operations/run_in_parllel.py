import asyncio
import aiomysql
import os 
from dotenv import load_dotenv

load_dotenv()

async def run_query(conn, user_id):
    # Execute the query
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT * FROM airplane_seats WHERE id = %s", (user_id,))
        rows = await cursor.fetchall()
    return rows

async def main(loop):
    user_ids = [1,2]# [i for i in range(2,50)]

    
    # Create a connection pool
    pool = await aiomysql.create_pool(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        db=os.getenv("DB_NAME"),
       loop=loop
    )

    # Create tasks for each user ID
    tasks = []
    for user_id in user_ids:
        async with pool.acquire() as conn:
            tasks.append(asyncio.create_task(run_query(conn, user_id)))
    pool.close()
    await pool.wait_closed()

    # Wait for all tasks to finish and collect results
    results = await asyncio.gather(*tasks)
    print(results)
    # Print the results
    for user_data in results:
        for row in user_data:
            print(f"User ID: {row[0]}")
            print(f"User data: {row[1]}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))