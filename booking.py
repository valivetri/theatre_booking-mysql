# This project is a simple theatre booking app
# I used XAMPP for local use without internet for several features

import mysql.connector
import random
import time
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bookings"
)

    if connection.is_connected():
        print("Connected to MySQL database")
        cursor = connection.cursor()
except Error:
    print("\n\tUnable to connect to Mysql. \n\tPlease take action!\n")
    time.sleep(3)
    exit(1)

while True:
    while True:
        print("Here are the movies:\n\t")
        movies = [
            "1) jailer @ 05|09|2023",
            "2) vikram @ 07|09|2023",
            "3) varisu @ 11|09|2023",
            "4) thunivu @ 14|09|2023",
            "5) master @ 17|09|2023",
            "6) catch @ 19|09|2023"
        ]
        for movie in movies:
            print(movie.title())

        while True:
            x = input("\nEnter a movie no. which you'd like to book? (1 to 6) or type 0 to exit: ").strip()

            if x == '0':
                print("Exiting the program.")
                cursor.close()
                connection.close()
                exit(0)
            elif not x.isdigit():
                print("Please enter a valid movie number.")
            else:
                movie_number = int(x)

                if movie_number < 1 or movie_number > len(movies):
                    print("\nThe movie number you entered is not available.")
                else:
                    print("\nYou've chosen the movie, {}".format(movies[movie_number - 1]), "\n")
                    time.sleep(1.5)
                    break

        blocks_list = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        userName = input("Enter your name: ").strip()
        time.sleep(1.5)

        i = 0
        while i < 9:
            row_index = random.randint(0, len(blocks_list) - 1)
            col_index = random.randint(0, len(blocks_list[0]) - 1)

            blocks_list[row_index][col_index] = 1
            i += 1

        check_query = "SELECT id FROM bookings WHERE username = %s AND movie = %s"
        duplicate_data = (userName, movies[movie_number - 1])

        cursor.execute(check_query, duplicate_data)
        existing_booking = cursor.fetchone()

        if existing_booking:
            print("\nWarning: Username '{}' has already booked '{}' movie.".format(userName, movies[movie_number - 1]))
            time.sleep(3)
            break
        else:
            print("\n\tYour ticket amount is Rs.200 (Your pin must be a 6-digit number!)")

        while True:
            payment = input("\nEnter your account pin to pay (6-digit number): ")

            if len(payment) != 6 or not payment.isdigit():
                print("Please enter a valid 6-digit pin.")
            else:
                payment = int(payment)
                time.sleep(1.5)
                break

        blocks_list[row_index][col_index] = userName
        for row in blocks_list:
            print(row)

        insert_query = "INSERT INTO bookings (username, movie, row, seat, amount_paid) VALUES (%s, %s, %s, %s, %s)"
        booking_data = (userName, movies[movie_number - 1], row_index + 1, col_index + 1, 200)

        cursor.execute(insert_query, booking_data)
        connection.commit()

        print("\n\tCongratulations! ", userName.title(), ", You've successfully booked a ticket for {}".format(
            movies[movie_number - 1]), "\n\n\tYour seat number is: Row {}, Seat {}".format(row_index + 1, col_index + 1))
        print("\tThank you!...\n")

        time.sleep(3)
