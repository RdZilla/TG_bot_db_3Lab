from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# selecting the program function
button_table_output = KeyboardButton('Вывод данных из таблицы')
button_table_input = KeyboardButton('Ввод данных в таблицу')
button_choice_function = KeyboardButton('Выбор функции')
button_value_output = KeyboardButton('Удаление данных из таблицы')
button_help = KeyboardButton('Помощь')

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_table_output,
                                                                                 button_table_input,
                                                                                 button_choice_function,
                                                                                 button_value_output,
                                                                                 button_help)

# selecting the output format of the table
button_with_code_output = KeyboardButton('С кодами')
button_Extended_output = KeyboardButton('Расширенная таблица')

output_format_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_with_code_output,
                                                                 button_Extended_output)

# selecting the table for input/output/delete
button_table_authors = KeyboardButton('Авторы')
button_table_books = KeyboardButton('Книги')
button_table_deliveries = KeyboardButton('Службы доставки')
button_table_publishing_house = KeyboardButton('Издательства')
button_table_purchases = KeyboardButton('Заказы')

output_table_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_table_authors,
                                                                button_table_books,
                                                                button_table_deliveries,
                                                                button_table_publishing_house,
                                                                button_table_purchases)

# selecting the database function
button_func_AvgPurchase = KeyboardButton('Средний чек')
button_func_RatingBooks = KeyboardButton('Топ книг по продажам')
button_func_RatingAuthors = KeyboardButton('Топ авторов по продажам')
button_func_SortPurchases = KeyboardButton('Сортировка заказов по общей стоимости')

functions_table_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_func_AvgPurchase,
                                                                   button_func_RatingBooks,
                                                                   button_func_RatingAuthors,
                                                                   button_func_SortPurchases)
