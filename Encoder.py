# Different way to encode images to strings

import base64 # package to encode the images
import io
from io import BytesIO # more image encoding
import matplotlib.pyplot as plt # image showing
from PIL import Image # image decoding
import sqlite3 as sq # image database



'''
READ FILE, ENCODE FILE, AND INSERT INTO DATABASE
'''
# Function for encoding the image to a string
def encoder(user_choice):
    with open(user_choice,"rb") as image_file: # perform the image encoding
        blobData = base64.b64encode(image_file.read())
    return blobData # pass encoded string

# Function for inserting into SQL database
def insertBlob(id, chapter, user_choice):
    try: # establish connection
        sqliteConnection = sq.connect('Delta.db')
        cursor = sqliteConnection.cursor() # make cursor object
        print("Connection to database successful")
        # establish proper query for database
        sq_query = """INSERT INTO chapter""" + chapter + """ (id, photoData) VALUES (?, ?)"""

        # make contact with encoder
        photoData = encoder(user_choice)
        data_tuple = (id,photoData) # arrange into a tuple for SQL query
        cursor.execute(sq_query,data_tuple) # execute SQL query
        sqliteConnection.commit() # commit to the change
        print("Successfully inserted into database")
        cursor.close() # close cursor

    except sq.Error as error: # if something happened with database connection
        print("Failed to insert blob", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close() # close the connection
            print("Connection closed.")

'''
RETRIEVE FROM DATABASE, DECODE, AND DISPLAY IMAGE
'''

# Function to retrieve database by chapter and id
def imageRetrieve(chapter,id):
    # connect to the database
    try:
        sqliteConnection = sq.connect('Delta.db')
        cursor = sqliteConnection.cursor() # make cursor object
        print("Successfully connected to database")

        # establish query
        fetch_query = """SELECT * FROM chapter""" + chapter + """ WHERE id = ?"""
        cursor.execute(fetch_query, (id,)) # execute query
        record = cursor.fetchall() # retrieve the data
        for row in record:
            print("Chapter" + chapter + " Id: " , row[0])
            photoData = row[1] # assign photo data

        # decode it and display
        photoData = base64.b64decode(photoData) # currently here
        image = Image.open(io.BytesIO(photoData)) # decode from base64 string
        plt.imshow(image) # display it, REMEMBER THAT IT'S MATPLOTLIB.PYPLOT
        plt.axis('off')
        plt.show()
        cursor.close() # close cursor

    except sq.Error as error: # if there is a problem reading from the table
        print("Failed to read blob data from table")
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("Database connection has closed!")

'''
DRIVER CODE
'''
# Driver code:
# Make it user input, driver code.
user_choice = input("Photo name: ")
user_id = int(input("id: "))
user_chapter = input("chapter: ")

# inserting into database
#insertBlob(user_id,user_chapter,user_choice)

# retrieving from database
imageRetrieve(user_chapter, user_id)







