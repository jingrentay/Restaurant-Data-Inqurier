import json
import psycopg2
from datetime import datetime
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap


def cleanStr4SQL(s):
    return s.replace("'", "`").replace("\n", " ")


def int2BoolStr(value):
    if value == 0:
        return 'False'
    else:
        return 'True'


def insert2BusinessTable():
    # reading the JSON file
    with open('../Project Milestone 2/yelp_business.JSON', 'r') as f:  # TODO: update path for the input file
        # outfile = open('../Project Milestone 2/yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        # TODO: update the database name, username, and password
        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='durian123'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            # Generate the INSERT statement for the current business
            # TODO: The below INSERT statement is based on a simple (and incomplete) businesstable schema. Update the statement based on your own table schema and
            # include values for all businessTable attributes
            sql_str = "INSERT INTO businessTable (business_id, name, address, state, city, zipcode, latitude, longitude, stars, reviewcount, numcheckins, is_open, reviewrating) " \
                      "VALUES ('" + data['business_id'] + "','" + cleanStr4SQL(data["name"]) + "','" + cleanStr4SQL(
                data["address"]) + "','" + \
                      cleanStr4SQL(data["state"]) + "','" + cleanStr4SQL(data["city"]) + "','" + data[
                          "postal_code"] + "'," + str(data["latitude"]) + "," + \
                      str(data["longitude"]) + "," + str(data["stars"]) + "," + str(
                data["review_count"]) + ", 0 ," + str(data["is_open"]) + ", 0" + ");"

            try:
                cur.execute(sql_str)
            except:
                print("Insert to businessTable failed!" + str(data["review_count"]))
            conn.commit()
            # optionally you might write the INSERT statement to a file.
            # outfile.write(sql_str)

            line = f.readline()
            count_line += 1

        cur.close()
        conn.close()

    print(count_line)
    # outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()


def insert2UsersTable():
    # reading the JSON file
    with open('../Project Milestone 2/yelp_user.JSON', 'r') as f:  # TODO: update path for the input file
        # outfile = open('../Project Milestone 2/yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        # TODO: update the database name, username, and password
        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='durian123'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            # Generate the INSERT statement for the current business
            # TODO: The below INSERT statement is based on a simple (and incomplete) businesstable schema. Update the statement based on your own table schema and
            # include values for all businessTable attributes
            sql_str = "INSERT INTO users (user_id, name, review_count, yelping_since, funny, useful, cool, num_fans, avg_stars) " \
                      "VALUES ('" + data['user_id'] + "','" + cleanStr4SQL(data["name"]) + "','" + str(
                data["review_count"]) + "','" + \
                      cleanStr4SQL(data["yelping_since"]) + "','" + str(data["funny"]) + "','" + str(
                data["useful"]) + "'," + str(data["cool"]) + "," + \
                      str(data["fans"]) + "," + str(data["average_stars"]) + ");"

            try:
                cur.execute(sql_str)
            except:
                print("Insert to userTable failed!" + str(data["user_id"]))
            conn.commit()
            # optionally you might write the INSERT statement to a file.
            # outfile.write(sql_str)

            line = f.readline()
            count_line += 1

        cur.close()
        conn.close()

    print(count_line)
    # outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()


def parseCheckinTimes(Times):
    result = {}
    Week = []
    sixAM = datetime.strptime("06:00", "%M:%S")
    twelvePM = datetime.strptime("12:00", "%M:%S")
    fivePM = datetime.strptime("17:00", "%M:%S")
    ninePM = datetime.strptime("21:00", "%M:%S")

    for day in Times.keys():
        Morning = 0
        Afternoon = 0
        Evening = 0
        Night = 0

        for time in Times.get(day):
            actualtime = datetime.strptime(time, "%M:%S")

            if (actualtime >= sixAM and actualtime < twelvePM):
                Morning += int(Times.get(day).get(time))
            elif (actualtime >= twelvePM and actualtime < fivePM):
                Afternoon += int(Times.get(day).get(time))
            elif (actualtime >= fivePM and actualtime < ninePM):
                Evening += int(Times.get(day).get(time))
            elif (actualtime >= ninePM and actualtime < sixAM):
                Night += int(Times.get(day).get(time))

        Week = [str(Morning), str(Afternoon), str(Evening), str(Night)]
        result[day] = Week

    return result


def insert2CheckinsTable():
    # reading the JSON file
    with open('../Project Milestone 2/yelp_checkin.JSON', 'r') as f:  # TODO: update path for the input file
        # outfile = open('../Project Milestone 2/yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        # TODO: update the database name, username, and password
        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='durian123'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            # Generate the INSERT statement for the current business
            # TODO: The below INSERT statement is based on a simple (and incomplete) businesstable schema. Update the statement based on your own table schema and
            # include values for all businessTable attributes
            checkins = parseCheckinTimes(data['time'])

            for day in checkins.keys():
                val = checkins.get(day)
                sql_str = "INSERT INTO checkins (business_id, day, morning, afternoon, evening, night) " \
                          "VALUES ('" + data['business_id'] + "', '" + str(day) + "', '" + str(val[0]) + "', '" \
                          + str(val[1]) + "', '" + str(val[2]) + "', '" + str(val[3]) + "');"

            try:
                cur.execute(sql_str)
            except:
                print("Insert to checkinsTable failed!")
            conn.commit()
            # optionally you might write the INSERT statement to a file.
            # outfile.write(sql_str)

            line = f.readline()
            count_line += 1

        cur.close()
        conn.close()

    print(count_line)
    # outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()


def insert2ReviewsTable():
    # reading the JSON file
    with open('../Project Milestone 2/yelp_review.JSON', 'r') as f:  # TODO: update path for the input file
        # outfile = open('../Project Milestone 2/yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        # TODO: update the database name, username, and password
        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='durian123'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            # Generate the INSERT statement for the current business
            # TODO: The below INSERT statement is based on a simple (and incomplete) businesstable schema. Update the statement based on your own table schema and
            # include values for all businessTable attributes
            sql_str = "INSERT INTO reviews (review_id, user_id, business_id, stars, date, text, useful, funny, cool) " \
                      "VALUES ('" + data['review_id'] + "','" + data['user_id'] + "','" + data["business_id"] + "','" + \
                      str(data["stars"]) + "','" + cleanStr4SQL(data['date']) + "','" + cleanStr4SQL(
                data['text']) + "'," \
                      + str(data["useful"]) + "," + str(data["funny"]) + "," + str(data["cool"]) + ");"

            try:
                cur.execute(sql_str)
            except:
                print("Insert to reviewTable failed!" + str(data["review_id"]))
            conn.commit()
            # optionally you might write the INSERT statement to a file.
            # outfile.write(sql_str)

            line = f.readline()
            count_line += 1

        cur.close()
        conn.close()

    print(count_line)
    # outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()


def insert2CategoryTable():
    # reading the JSON file
    with open('../Project Milestone 2/yelp_business.JSON', 'r') as f:  # TODO: update path for the input file
        # outfile = open('../Project Milestone 2/yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        # TODO: update the database name, username, and password
        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='durian123'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            # Generate the INSERT statement for the current business
            # TODO: The below INSERT statement is based on a simple (and incomplete) businesstable schema. Update the statement based on your own table schema and
            # include values for all businessTable attributes
            for val in data['categories']:
                sql_str = "INSERT INTO category (c_name, business_id) " \
                          "VALUES ('" + cleanStr4SQL(val) + "', '" + data['business_id'] + "');"

            try:
                cur.execute(sql_str)
            except:
                print("Insert to categoryTable failed!")
            conn.commit()
            # optionally you might write the INSERT statement to a file.
            # outfile.write(sql_str)

            line = f.readline()
            count_line += 1

        cur.close()
        conn.close()

    print(count_line)
    # outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()


def insert2FriendsTable():
    # reading the JSON file
    with open('../Project Milestone 2/yelp_user.JSON', 'r') as f:  # TODO: update path for the input file
        # outfile = open('../Project Milestone 2/yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        # TODO: update the database name, username, and password
        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='durian123'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            # Generate the INSERT statement for the current business
            # TODO: The below INSERT statement is based on a simple (and incomplete) businesstable schema. Update the statement based on your own table schema and
            # include values for all businessTable attributes
            for val in data['friends']:
                sql_str = "INSERT INTO friendsTable (user_id, friend_id) " \
                          "VALUES ('" + cleanStr4SQL(data['user_id']) + "', '" + str(val) + "');"

                try:
                    cur.execute(sql_str)
                except:
                    print("Insert to friendsTable failed!" + " " + data['user_id'] + " " + val)
                conn.commit()
                # optionally you might write the INSERT statement to a file.
                # outfile.write(sql_str)

            line = f.readline()
            count_line += 1

        cur.close()
        conn.close()

    print(count_line)
    # outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()


def parseOpeningTimes(hours, business_id):
    sql_str = []
    for day in hours.items():
        time = day[1].split("-", 1)
        sql_hours = ""

        day = day[0] + "'"
        sql_hours = "INSERT INTO openingtimes (dayinweek, opening, closing , business_id) " \
                    "VALUES ('" + str(day) + ", '" + time [0] + "', '" + time[1] + "', '" + business_id + "');"
        sql_str.append(sql_hours)

    return sql_str


def insert2OpeningTimesTable():
    # reading the JSON file
    with open('../Project Milestone 2/yelp_business.JSON', 'r') as f:  # TODO: update path for the input file
        # outfile = open('../Project Milestone 2/yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        # TODO: update the database name, username, and password
        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='durian123'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            # Generate the INSERT statement for the current business
            # TODO: The below INSERT statement is based on a simple (and incomplete) businesstable schema. Update the statement based on your own table schema and
            # include values for all businessTable attributes
            hours = parseOpeningTimes(data['hours'], cleanStr4SQL(data['business_id']))
            for val in hours:
                sql_str = val

                try:
                    cur.execute(sql_str)
                except:
                    print("Insert to openingTimesTable failed!" + " " + data['user_id'] + " " + val)
                conn.commit()
                # optionally you might write the INSERT statement to a file.
                # outfile.write(sql_str)

            line = f.readline()
            count_line += 1

        cur.close()
        conn.close()

    print(count_line)
    # outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()


# insert2BusinessTable()
# insert2UsersTable()
# insert2CheckinsTable()
# insert2ReviewsTable()
# insert2CategoryTable()
insert2FriendsTable()
# insert2OpeningTimesTable()

