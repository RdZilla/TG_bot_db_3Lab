import logging

import mysql.connector as mariadb
from config_sql import user, password, host, port, db_name


logging.basicConfig(level=logging.INFO)


def sql_connection():
    try:
        mariadb_connection = mariadb.connect(user=user, password=password, host=host, port=port, database=db_name)
        logging.info('Connection is successful')
        # print('Connection is successful')
        # print("=" * 64, '\n')
        return mariadb_connection

    except Exception as ex:
        # logging.info('Connection refused...\n', ex)
        print('Connection refused...\n', ex)


# sql query for output someone table
def sql_output_table(table_name):
    mariadb_connection = sql_connection()
    try:
        with mariadb_connection.cursor() as cursor:
            print_table = f"SELECT * FROM {table_name};"
            cursor.execute(print_table)
            rows = cursor.fetchall()
            return rows
    finally:
        mariadb_connection.close()


# sql query for search someone by code
def sql_output_code(desired_element, table_name, name_element, code_element):
    mariadb_connection = sql_connection()
    try:
        with mariadb_connection.cursor() as cursor:
            print_table = f"SELECT {desired_element} FROM {table_name} WHERE {name_element} = {code_element};"
            cursor.execute(print_table)
            answer = cursor.fetchall()
            return answer[0]
    finally:
        mariadb_connection.close()


# sql query for adding user data to the table "authors"
def sql_input_in_table_authors(value_name_author, value_birthday):
    mariadb_connection = sql_connection()
    try:
        with mariadb_connection.cursor(buffered=True) as cursor:
            add_new_string = f"SELECT AddInAuthors('{value_name_author}', '{value_birthday}');"
            cursor.execute(add_new_string)

            # update the database
            mariadb_connection.commit()

        # returning a new line number
        with mariadb_connection.cursor() as cursor:
            counter_string = "SELECT COUNT(Code_author) FROM authors"
            cursor.execute(counter_string)
            answer = cursor.fetchall()
            return answer[0]
    finally:
        mariadb_connection.close()


# sql query for adding user data to the table "books"
def sql_input_in_table_books(value_title_book, value_code_author, value_pages, value_code_publish):
    mariadb_connection = sql_connection()
    try:
        with mariadb_connection.cursor(buffered=True) as cursor:
            add_new_string = f"SELECT AddInBooks('{value_title_book}', " \
                                               f"'{value_code_author}', " \
                                               f"'{value_pages}', " \
                                               f"'{value_code_publish}');"
            cursor.execute(add_new_string)

            # update the database
            mariadb_connection.commit()

        # returning a new line number
        with mariadb_connection.cursor() as cursor:
            counter_string = "SELECT COUNT(Code_book) FROM books"
            cursor.execute(counter_string)
            answer = cursor.fetchall()
            return answer[0]
    finally:
        mariadb_connection.close()


# sql query for adding user data to the table "deliveries"
def sql_input_in_table_deliveries(value_name_delivery, value_name_company, value_address, value_phone, value_ogrn):
    mariadb_connection = sql_connection()
    try:
        with mariadb_connection.cursor(buffered=True) as cursor:
            add_new_string = f"SELECT AddInDeliveries('{value_name_delivery}', " \
                                                    f"'{value_name_company}', " \
                                                    f"'{value_address}', " \
                                                    f"'{value_phone}', " \
                                                    f"'{value_ogrn}');"
            cursor.execute(add_new_string)

            # update the database
            mariadb_connection.commit()

        # returning a new line number
        with mariadb_connection.cursor() as cursor:
            counter_string = "SELECT COUNT(Code_delivery) FROM deliveries"
            cursor.execute(counter_string)
            answer = cursor.fetchall()
            return answer[0]
    finally:
        mariadb_connection.close()


# sql query for adding user data to the table "publishing_house"
def sql_input_in_table_publishing_house(value_publish, value_city):
    mariadb_connection = sql_connection()
    try:
        with mariadb_connection.cursor(buffered=True) as cursor:
            add_new_string = f"SELECT AddInPublishingHouse('{value_publish}', '{value_city}');"
            cursor.execute(add_new_string)

            # update the database
            mariadb_connection.commit()

        # returning a new line number
        with mariadb_connection.cursor() as cursor:
            counter_string = "SELECT COUNT(Code_publish) FROM publishing_house"
            cursor.execute(counter_string)
            answer = cursor.fetchall()
            return answer[0]
    finally:
        mariadb_connection.close()


# sql query for adding user data to the table "purchases"
def sql_input_in_table_purchases(value_code_book, value_date_order, value_code_delivery, value_amount):
    mariadb_connection = sql_connection()
    try:
        with mariadb_connection.cursor(buffered=True) as cursor:
            add_new_string = f"SELECT AddInPurchases('{value_code_book}', " \
                                                   f"'{value_date_order}', " \
                                                   f"'{value_code_delivery}', " \
                                                   f"'{value_amount}');"
            cursor.execute(add_new_string)

            # update the database
            mariadb_connection.commit()

        # returning a new line number
        with mariadb_connection.cursor() as cursor:
            counter_string = "SELECT COUNT(Code_purchase) FROM purchases"
            cursor.execute(counter_string)
            answer = cursor.fetchall()
            return answer[0]
    finally:
        mariadb_connection.close()


# sql query for using database functions
def sql_output_function(name_function):
    mariadb_connection = sql_connection()
    try:
        with mariadb_connection.cursor() as cursor:
            func = f"SELECT {name_function};"
            cursor.execute(func)
            answer = cursor.fetchall()
            return answer
    finally:
        mariadb_connection.close()


# sql query for deleting a row from the table "authors"
def sql_delete_from_table_authors(value_code_author):
    mariadb_connection = sql_connection()
    try:
        with mariadb_connection.cursor(buffered=True) as cursor:
            func = f"SELECT delete_from_authors({value_code_author});"
            cursor.execute(func)

            # update the database
            mariadb_connection.commit()
            return 0
    finally:
        mariadb_connection.close()


# sql query for deleting a row from the table "books"
def sql_delete_from_table_books(value_code_book):
    mariadb_connection = sql_connection()
    try:
        with mariadb_connection.cursor(buffered=True) as cursor:
            func = f"SELECT delete_from_books({value_code_book});"
            cursor.execute(func)

            # update the database
            mariadb_connection.commit()
            return 0
    finally:
        mariadb_connection.close()


# sql query for deleting a row from the table "deliveries"
def sql_delete_from_table_deliveries(value_code_delivery):
    mariadb_connection = sql_connection()
    try:
        with mariadb_connection.cursor(buffered=True) as cursor:
            func = f"SELECT delete_from_deliveries({value_code_delivery});"
            cursor.execute(func)

            # update the database
            mariadb_connection.commit()
            return 0
    finally:
        mariadb_connection.close()


# sql query for deleting a row from the table "publishing_house"
def sql_delete_from_table_publishing_house(value_code_publish):
    mariadb_connection = sql_connection()
    try:
        with mariadb_connection.cursor(buffered=True) as cursor:
            func = f"SELECT delete_from_publishing_house({value_code_publish});"
            cursor.execute(func)

            # update the database
            mariadb_connection.commit()
            return 0
    finally:
        mariadb_connection.close()


# sql query for deleting a row from the table "purchases"
def sql_delete_from_table_purchases(value_code_purchase):
    mariadb_connection = sql_connection()
    try:
        with mariadb_connection.cursor(buffered=True) as cursor:
            func = f"SELECT delete_from_purchases({value_code_purchase});"
            cursor.execute(func)

            # update the database
            mariadb_connection.commit()
            return 0
    finally:
        mariadb_connection.close()
