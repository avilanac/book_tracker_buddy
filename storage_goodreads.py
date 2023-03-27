import os
import psycopg2
import pandas as pd
import logging

# Setting the logging level to INFO.
logging.basicConfig(level=logging.INFO)

try:
    dbname = os.getenv("DB_NAME")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")   
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    connect = psycopg2.connect(
        database=dbname,
        host=host, 
        port=port,  
        user=user, 
        password=password
    )
    cursor = connect.cursor()
    
    data = r"E:\Practicas\Proyects\book_tracker_buddy\data\goodreads_process.csv"
    df = pd.read_csv(data)

    # Iterating over the rows of the dataframe and inserting the values into the database.
    for index, row in df.iterrows():
        title = row["Title"]
        author = row["Author"]
        stars = row["Stars"]
        n_ratings = row["N.Ratings"]
        score = row["Score"]
        people_voted = row["People voted"]

        query = """INSERT INTO goodreads (title, author, stars, n_ratings, score, people_voted)
        VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (title, author, stars, n_ratings, score, people_voted)

        cursor.execute(query, values)

except psycopg2.OperationalError as err:
    logging.error("Error connecting to the database: %s", err)
else:
    # Checking if the variable connect is in the local scope. If it is, it commits the changes.
    if 'connect' in locals() and 'cursor' in locals():
        connect.commit()  
        cursor.close()
        connect.close()
        
    logging.info("Data inserted successfully.")
