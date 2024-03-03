# TG_bot_db_3Lab
## Project on the discipline "Databases"
### Date: 24.05.2023

A project on the discipline "Databases". 
-  This application is designed to manage the work of a Telegram bot. The Aiogram library is used to create and manage the bot. 
-  SQL queries are implemented in the Python programming language. The MySQL library is used to interact with the database.

> [!NOTE]
> You must deploy the database on your system. The corresponding sql file with the database structure and test data is located in the "sql_structure_&_data" directory.
> 
> To work correctly, you need to make changes to the files **"config_bot"** and **"config_sql"**.
> - In the **"config_bot"** file, you must specify the **Token** of your previously created Telegram bot, in the value of the ***"TOKEN"*** parameter. (You can learn how to do this on the official Telegram website in the relevant documentation **[here](https://core.telegram.org/bots#how-do-i-create-a-bot)**)
> - In the **"config_sql"** file, you must specify the connection parameters to your database: ***host***, ***user***, ***password***, ***port***.

> [!WARNING]
> Create a database named ***db_py_book_shop***. You can choose **any other database name**, but **do not forget to specify** a new name in the **"config_sql"** file in the value of the ***"db_name"*** parameter.
