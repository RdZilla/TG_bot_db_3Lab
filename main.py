import time
import datetime
import logging
import re
import random

# framework for sql queries
import mysql

# framework for telegram bot
import aiogram
from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.utils.markdown import text, italic, code, hcode, hitalic, hunderline
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

# framework for output emoji in message
from emoji import emojize
# framework for a beautiful output of the result
import tabulate

# contains telegram_bot's keyboard for selecting program functions/tables/output format of the table/database functions
import py_scripts.keyboards as kb
# contains telegram_bot's TOKEN
from py_scripts.config_bot import TOKEN
# contains sql queries for selecting database functions
import py_scripts.sql_queries as sq


# counter for aggressive mode
funny_counter = 0

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


# for enter user data into the database
class UserState(StatesGroup):
    waiting_user_string = State()


# for delete from the database
class StringState(StatesGroup):
    waiting_delete_number = State()


# input of values not provided by the functional
class Aggressive(StatesGroup):
    first_warning = State()
    second_warning = State()
    final_warning = State()


def write_log(message, name_function):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} | {user_full_name=} | {name_function=} | {message.text=} | {time.asctime()}')
    return 0


# output table "authors"
def output_authors(rows):
    data = [['code', 'name_surname', 'birthday']]

    for row_unprocessed in rows:
        counter = row_unprocessed[0]
        name = row_unprocessed[1]
        birthday = str(row_unprocessed[2])

        # for a beautiful output of the result
        list_for_insert = [counter, name, birthday]
        data.insert(counter, list_for_insert)

    # for a beautiful output of the result
    rows_message = '<pre>' + tabulate.tabulate(data) + '</pre>'
    return rows_message


# output table "books"
def output_books(rows):
    data = [['code', 'title', 'code_author', 'pages', 'code_publish']]

    for row_unprocessed in rows:
        counter = row_unprocessed[0]
        title = row_unprocessed[1]
        code_author = row_unprocessed[2]
        pages = row_unprocessed[3]
        code_publish = row_unprocessed[4]

        # for a beautiful output of the result
        list_for_insert = [counter, title, code_author, pages, code_publish]
        data.insert(counter, list_for_insert)

    # for a beautiful output of the result
    rows_message = '<pre>' + tabulate.tabulate(data) + '</pre>'
    return rows_message


# output extended table "books"
def help_output_books(rows):
    data = [['code', 'title', 'name_author', 'pages', 'code_publish']]

    for row_unprocessed in rows:
        counter = row_unprocessed[0]
        title = row_unprocessed[1]
        code_author = row_unprocessed[2]

        # sql query for search for a name authors by code
        name_author_unprocessed = sq.sql_output_code("name_author", "authors", "code_author", int(code_author))
        name_author = name_author_unprocessed[0]

        pages = row_unprocessed[3]
        code_publish = row_unprocessed[4]

        # sql query for search for a name publish by code
        publish_unprocessed = sq.sql_output_code("publish", "publishing_house", "code_publish", int(code_publish))
        publish = publish_unprocessed[0]

        # for a beautiful output of the result
        list_for_insert = [counter, title, name_author, pages, publish]
        data.insert(counter, list_for_insert)

    # for a beautiful output of the result
    rows_message = '<pre>' + tabulate.tabulate(data) + '</pre>'
    return rows_message


# output table "deliveries"
def output_deliveries(rows):
    data = [['code', 'delivery', 'company', 'address', 'phone', 'OGRN']]

    for row_unprocessed in rows:
        counter = row_unprocessed[0]
        delivery = row_unprocessed[1]
        company = row_unprocessed[2]
        address = row_unprocessed[3]
        phone = row_unprocessed[4]
        ogrn = row_unprocessed[5]

        # for a beautiful output of the result
        list_for_insert = [counter, delivery, company, address, phone, ogrn]
        data.insert(counter, list_for_insert)

    # for a beautiful output of the result
    rows_message = '<pre>' + tabulate.tabulate(data) + '</pre>'
    return rows_message


# output table "publishing_house"
def output_publishing_house(rows):
    data = [['code', 'publishing_house', 'city']]

    for row_unprocessed in rows:
        counter = row_unprocessed[0]
        publishing_house = row_unprocessed[1]
        city = row_unprocessed[2]

        # for a beautiful output of the result
        list_for_insert = [counter, publishing_house, city]
        data.insert(counter, list_for_insert)

    # for a beautiful output of the result
    rows_message = '<pre>' + tabulate.tabulate(data) + '</pre>'
    return rows_message


# output table "purchases"
def output_purchases(rows):
    data = [['code', 'code_book', 'date_order', 'code_delivery', 'amount']]

    for row_unprocessed in rows:
        counter = row_unprocessed[0]
        code_book = row_unprocessed[1]
        date_order = row_unprocessed[2]
        code_delivery = row_unprocessed[3]
        amount = row_unprocessed[4]

        # for a beautiful output of the result
        list_for_insert = [counter, code_book, date_order, code_delivery, amount]
        data.insert(counter, list_for_insert)

    # for a beautiful output of the result
    rows_message = '<pre>' + tabulate.tabulate(data) + '</pre>'
    return rows_message


# output extended table "purchases"
def help_output_purchases(rows):
    data = [['code', 'name_book', 'date_order', 'name_delivery', 'amount']]

    for row_unprocessed in rows:
        counter = row_unprocessed[0]
        code_book = row_unprocessed[1]

        # sql query for search for a name book by code
        name_book_unprocessed = sq.sql_output_code("title_book", "books", "code_book", int(code_book))
        name_book = name_book_unprocessed[0]

        date_order = row_unprocessed[2]
        code_delivery = row_unprocessed[3]

        # sql query for search for a name delivery by code
        name_delivery_unprocessed = sq.sql_output_code("Name_delivery", "deliveries",
                                                       "code_delivery", int(code_delivery))
        name_delivery = name_delivery_unprocessed[0]
        amount = row_unprocessed[4]

        # for a beautiful output of the result
        list_for_insert = [counter, name_book, date_order, name_delivery, amount]
        data.append(list_for_insert)

    # for a beautiful output of the result
    rows_message = '<pre>' + tabulate.tabulate(data) + '</pre>'
    return rows_message


flag = ''
flag_table = ''
name_table = ''
user_check = ''


@dp.message_handler(commands=['start'], state="*")
async def start_handler(message: types.Message, state: FSMContext):
    name_function = 'start'
    write_log(message, name_function)

    # stop aggressive mode
    await state.finish()
    user_full_name = message.from_user.full_name

    sticker_id = 'CAACAgIAAxkBAAIJz2RBrH9FFhptBeObQ2bzYAHLqNChAAIOAAMOR8co1hNgkbBsfpkvBA'
    await bot.send_sticker(message.chat.id, sticker_id)

    await message.reply(f"Привет, {user_full_name}!\n"
                        f"Я - бот-помощник для книжного магазина"
                        f"\nВыберите желаемую функцию", reply_markup=kb.greet_kb)


@dp.message_handler(commands=['back'], state="*")
async def back_handler(message: types.Message, state: FSMContext):
    name_function = 'back'
    write_log(message, name_function)

    # stop aggressive mode
    await state.finish()

    sticker_id = 'CAACAgIAAxkBAAIJ9GRBrgF5iz1cw76EWm7TmM-BU7IeAALwQwAC6VUFGMx1yzGbj_KrLwQ'
    await bot.send_sticker(message.chat.id, sticker_id)

    await message.reply("Выберите желаемую функцию", reply_markup=kb.greet_kb)


@dp.message_handler(filters.Text(['/help', 'Помощь']), state="*")
async def process_help_command(message: types.Message, state: FSMContext):
    name_function = 'help'
    write_log(message, name_function)

    # stop aggressive mode
    await state.finish()

    sticker_id = 'CAACAgIAAxkBAAIKDmRBroBj4vcb-68cr0dtqY1UMrSrAAJkNAAC6VUFGIkDwHeRWb8tLwQ'
    await message.reply_sticker(sticker_id)
    await message.reply("Тут могла бы быть помощь, но...😮"
                        "\nЯ даже не знаю, чем тут помочь... Всё ведь просто и понятно\n    "
                        "\nМожно попробовать посмотреть ниже и увидеть кнопки..."
                        "\nНу или нажать на кнопочку справа от поля ввода и опять же увидеть кнопки"
                        "\nУдобные... Красивые..."
                        "\nНажмите, не стесняйтесь🥰"
                        "\nЗнаете ли, грех их игнорировать👇",
                        reply_markup=kb.greet_kb)


@dp.message_handler(commands="cancel", state="*")
async def cancel_get_user_string(message: types.Message, state: FSMContext):
    name_function = 'cancel'
    write_log(message, name_function)

    # stop aggressive mode
    await state.finish()

    sticker_id = 'CAACAgIAAxkBAAIJwmRBq3iwMS7-zBFucjzJ2jfx0f2YAAJdAAOQczMb4eoMAAEMJG5kLwQ'
    await bot.send_sticker(message.chat.id, sticker_id)

    await bot.send_message(message.chat.id, "Действие отменено")
    await message.answer("Выберите желаемую функцию", reply_markup=kb.greet_kb)


@dp.message_handler(filters.Text("Ввод данных в таблицу"), state="*")
async def process_input_table_db(message: types.Message, state: FSMContext):
    global flag
    name_function = 'input_table'
    write_log(message, name_function)

    # stop aggressive mode
    await state.finish()

    flag = 'input'

    sticker_id = 'CAACAgQAAxkBAAIKEGRBrrcgk8EJgb2QLCSyS0gZxnykAAL-DAACCfvAUuUu-nWPfzh4LwQ'
    await bot.send_sticker(message.chat.id, sticker_id)

    await message.reply("Выберите таблицу для ввода (для возврата используйте /back)",
                        reply_markup=kb.output_table_kb)


@dp.message_handler(filters.Text("Вывод данных из таблицы"), state="*")
async def process_output_table_db(message: types.Message, state: FSMContext):
    global flag
    name_function = 'output'
    write_log(message, name_function)

    # stop aggressive mode
    await state.finish()

    flag = 'output'

    sticker_id = 'CAACAgIAAxkBAAIKEmRBrvimodMbJrCRy8cYXO-qhH7-AAJ5LAAC6VUFGE9k5JtV8M8pLwQ'
    await bot.send_sticker(message.chat.id, sticker_id)

    await message.reply("Выберите формат вывода таблицы (для возврата используйте /back)",
                        reply_markup=kb.output_format_kb)


@dp.message_handler(filters.Text(['С кодами', 'Расширенная таблица']), state="*")
async def process_format_output_table_db(message: types.Message, state: FSMContext):
    global flag_format_output
    name_function = 'format_output'
    write_log(message, name_function)

    # stop aggressive mode
    await state.finish()

    if message.text == 'С кодами':
        flag_format_output = 'with_code'
    if message.text == 'Расширенная таблица':
        flag_format_output = 'Extended'

    sticker_id = 'CAACAgIAAxkBAAIKEmRBrvimodMbJrCRy8cYXO-qhH7-AAJ5LAAC6VUFGE9k5JtV8M8pLwQ'
    await bot.send_sticker(message.chat.id, sticker_id)

    await message.reply("Выберите таблицу для вывода (для возврата используйте /back)",
                        reply_markup=kb.output_table_kb)


@dp.message_handler(filters.Text("Удаление данных из таблицы"), state="*")
async def process_delete_from_table_db(message: types.Message, state: FSMContext):
    global flag
    name_function = 'delete'
    write_log(message, name_function)

    # stop aggressive mode
    await state.finish()

    flag = 'delete'

    sticker_id = 'CAACAgIAAxkBAAM5ZG0MV5xuI6gqxMHv8cs15a9zSvIAAn43AALpVQUYv6Is4c8gVWovBA'
    await bot.send_sticker(message.chat.id, sticker_id)

    await message.reply("Выберите таблицу из которой нужно удалить строку\n"
                        "(для возврата используйте /back)",
                        reply_markup=kb.output_table_kb)


@dp.message_handler(filters.Text(["Авторы", "Книги", "Службы доставки", "Издательства", "Заказы"]), state="*")
async def process_select_table(message: types.Message, state: FSMContext):
    global name_table
    name_function = 'select_table'
    write_log(message, name_function)

    # stop aggressive mode
    await state.finish()

    if message.text == "Авторы":
        name_table = "authors"
    if message.text == "Книги":
        name_table = "books"
    if message.text == "Службы доставки":
        name_table = "deliveries"
    if message.text == "Издательства":
        name_table = "publishing_house"
    if message.text == "Заказы":
        name_table = "purchases"

    if flag == 'input':
        sticker_id = 'CAACAgIAAxkBAAIKOWRBsWxJLElyecUdVcuEXbL4s95aAAIUHwACHBGpShPDJScebBqXLwQ'
        await bot.send_sticker(message.chat.id, sticker_id)

        if name_table == "authors":
            message_text = text('Введите данные для добавления в таблицу в формате\n',
                                hcode('name_surname date_birthday(YYYY-MM-DD)'), '\n\n',
                                hitalic('Данные вводятся исключительно на английском языке\n'
                                        'Вместо пробелов - нижнее подчёркивание'),
                                hcode('_'), '\n\n\n',
                                'Для отмены действия - команда /cancel')
            await bot.send_message(message.from_user.id, message_text, parse_mode="HTML",
                                   reply_markup=types.ReplyKeyboardRemove())

            # waiting for user data to be entered into the database
            await UserState.waiting_user_string.set()

        if name_table == "books":

            # auxiliary tables
            rows_authors = sq.sql_output_table('authors')  # sql query for table output
            rows_message_authors = output_authors(rows_authors)
            rows_publish = sq.sql_output_table('publishing_house')  # sql query for table output
            rows_message_publish = output_publishing_house(rows_publish)

            await bot.send_message(message.from_user.id, "Вспомогательные таблицы\nAuthors\n" + rows_message_authors,
                                   parse_mode='HTML')
            await bot.send_message(message.from_user.id, "publishing_house\n" + rows_message_publish, parse_mode='HTML')

            message_text = text('Введите данные для добавления в таблицу в формате\n',
                                hcode('title_book code_author pages code_publish'), '\n\n',
                                hunderline('Количество страниц должно быть больше 5\n'),
                                hitalic('Данные вводятся исключительно на английском языке\n'
                                        'Вместо пробелов - нижнее подчеркивание\n'
                                        'Используйте вспомогательные таблицы для ввода\n'),
                                hcode('code_author'), 'и',
                                hcode('code_publish'), '\n\n\n',
                                'Для отмены действия - команда /cancel')
            await bot.send_message(message.from_user.id, message_text, parse_mode="HTML",
                                   reply_markup=types.ReplyKeyboardRemove())

            # waiting for user data to be entered into the database
            await UserState.waiting_user_string.set()

        if name_table == "deliveries":
            message_text = text('Введите данные для добавления в таблицу в формате\n',
                                hcode('name_delivery name_company address phone OGRN'), '\n\n',
                                hitalic('Данные вводятся исключительно на английском языке\n'
                                        'Вместо пробелов - нижнее подчеркивание'), '\n\n\n',
                                'Для отмены действия - команда /cancel')
            await bot.send_message(message.from_user.id, message_text, parse_mode="HTML",
                                   reply_markup=types.ReplyKeyboardRemove())

            # waiting for user data to be entered into the database
            await UserState.waiting_user_string.set()

        if name_table == "publishing_house":
            message_text = text('Введите данные для добавления в таблицу в формате\n',
                                hcode('publishing_house city'), '\n\n',
                                hitalic('Данные вводятся исключительно на английском языке\n'
                                        'Вместо пробелов - нижнее подчеркивание'), '\n\n\n',
                                'Для отмены действия - команда /cancel')
            await bot.send_message(message.from_user.id, message_text, parse_mode="HTML",
                                   reply_markup=types.ReplyKeyboardRemove())

            # waiting for user data to be entered into the database
            await UserState.waiting_user_string.set()

        if name_table == "purchases":
            # auxiliary tables
            rows_books = sq.sql_output_table('books')  # sql query for table output
            rows_message_books = help_output_books(rows_books)
            rows_deliveries = sq.sql_output_table('deliveries')  # sql query for table output
            rows_message_deliveries = output_deliveries(rows_deliveries)

            await bot.send_message(message.from_user.id, "Вспомогательные таблицы\nBooks\n" + rows_message_books,
                                   parse_mode='HTML')
            await bot.send_message(message.from_user.id, "deliveries\n" + rows_message_deliveries, parse_mode='HTML')

            message_text = text('Введите данные для добавления в таблицу в формате\n',
                                hcode('code_book date_order(YYYY-MM-DD), code_delivery, amount\n'),
                                '\n\n',
                                hitalic('Данные вводятся исключительно на английском языке\n'
                                        'Вместо пробелов - нижнее подчеркивание\n'
                                        'Используйте вспомогательные таблицы для ввода\n'),
                                hcode('code_book'), 'и',
                                hcode('code_delivery'), '\n\n\n',
                                'Для отмены действия - команда /cancel')
            await bot.send_message(message.from_user.id, message_text, parse_mode="HTML",
                                   reply_markup=types.ReplyKeyboardRemove())

            # waiting for user data to be entered into the database
            await UserState.waiting_user_string.set()

    if flag == 'output':
        if flag_format_output == 'with_code':
            # sql query for table output
            rows = sq.sql_output_table(name_table)

            if name_table == "authors":
                rows_message = output_authors(rows)
            if name_table == "books":
                rows_message = output_books(rows)
            if name_table == "deliveries":
                rows_message = output_deliveries(rows)
            if name_table == "publishing_house":
                rows_message = output_publishing_house(rows)
            if name_table == "purchases":
                rows_message = output_purchases(rows)

            sticker_id = 'CAACAgIAAxkBAAIKFGRBr3ntH9cNe4bBG0PGvfGld_u6AALnLgAC4KOCB8flxtpDPV_ILwQ'
            await bot.send_sticker(message.chat.id, sticker_id)

            await bot.send_message(message.from_user.id, rows_message, parse_mode='HTML', reply_markup=kb.greet_kb)
        if flag_format_output == 'Extended':
            sticker_id = 'CAACAgIAAxkBAAIKFGRBr3ntH9cNe4bBG0PGvfGld_u6AALnLgAC4KOCB8flxtpDPV_ILwQ'
            await bot.send_sticker(message.chat.id, sticker_id)

            # sql query for table output
            rows = sq.sql_output_table(name_table)
            if name_table == "authors":
                await bot.send_message(message.from_user.id, output_authors(rows), parse_mode='HTML',
                                       reply_markup=kb.greet_kb)
            if name_table == "books":
                await bot.send_message(message.from_user.id, help_output_books(rows), parse_mode='HTML',
                                       reply_markup=kb.greet_kb)
            if name_table == "deliveries":
                await bot.send_message(message.from_user.id, output_deliveries(rows), parse_mode='HTML',
                                       reply_markup=kb.greet_kb)
            if name_table == "publishing_house":
                await bot.send_message(message.from_user.id, output_publishing_house(rows), parse_mode='HTML',
                                       reply_markup=kb.greet_kb)
            if name_table == "purchases":
                await bot.send_message(message.from_user.id, help_output_purchases(rows), parse_mode='HTML',
                                       reply_markup=kb.greet_kb)

    if flag == 'delete':
        sticker_id = 'CAACAgIAAxkBAAODZG0PuZ8JvmgLbjhaQTygHyVy0VEAAoIVAAKGirFKZsIRBLomVCIvBA'
        await bot.send_sticker(message.chat.id, sticker_id)

        # sql query for table output
        rows = sq.sql_output_table(name_table)
        if name_table == "authors":
            await bot.send_message(message.from_user.id, output_authors(rows), parse_mode='HTML')
        if name_table == "books":
            await bot.send_message(message.from_user.id, help_output_books(rows), parse_mode='HTML')
        if name_table == "deliveries":
            await bot.send_message(message.from_user.id, output_deliveries(rows), parse_mode='HTML')
        if name_table == "publishing_house":
            await bot.send_message(message.from_user.id, output_publishing_house(rows), parse_mode='HTML')
        if name_table == "purchases":
            await bot.send_message(message.from_user.id, help_output_purchases(rows), parse_mode='HTML')

        message_text = text('Введите номер строки, которую требуется удалить из таблицы\n',
                            'Пример: ', hcode('1'), ' или ', hcode('357'), '\n\n\n',
                            'Для отмены действия - команда /cancel')

        await bot.send_message(message.from_user.id, message_text, parse_mode="HTML",
                               reply_markup=types.ReplyKeyboardRemove())

        # waiting for user data to be deleted from the database
        await StringState.waiting_delete_number.set()


@dp.message_handler(state=UserState.waiting_user_string)
async def get_user_string_for_input(message: types.Message, state: FSMContext):
    name_function = 'string_for_table'
    write_log(message, name_function)

    if re.search('[а-яА-ЯЁё]', message.text):
        sticker_id = 'CAACAgIAAxkBAAIKMGRBr9YDFYSloaHsTh4v9XzRcs-EAAJJCwACZ48hSo1PZZN4TIGRLwQ'
        await bot.send_sticker(message.chat.id, sticker_id)

        await message.answer("Пожалуйста, введите данные для добавления в таблицу на английском языке!"
                             "\n\nДля отмены действия - команда /cancel")
        return

    if name_table == "authors":  # template: name_surname YYYY-MM-DD
        try:
            list_string = message.text.split()
            date = datetime.datetime.strptime(list_string[1], '%Y-%m-%d')
            value_birthday = str(date.date())

        # non-template input
        except ValueError:
            sticker_id = 'CAACAgIAAxkBAAIKMGRBr9YDFYSloaHsTh4v9XzRcs-EAAJJCwACZ48hSo1PZZN4TIGRLwQ'
            await bot.send_sticker(message.chat.id, sticker_id)

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return
        except IndexError:
            sticker_id = 'CAACAgIAAxkBAAIKMGRBr9YDFYSloaHsTh4v9XzRcs-EAAJJCwACZ48hSo1PZZN4TIGRLwQ'
            await bot.send_sticker(message.chat.id, sticker_id)

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return

        pattern = '[a-zA-Z]*_[a-zA-Z]*'
        value_name_author = list_string[0]

        # non-template input field "authors"
        if not re.fullmatch(pattern, value_name_author):
            sticker_id = 'CAACAgIAAxkBAAIKMGRBr9YDFYSloaHsTh4v9XzRcs-EAAJJCwACZ48hSo1PZZN4TIGRLwQ'
            await bot.send_sticker(message.chat.id, sticker_id)

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return

        try:
            answer_unprocessed = str(sq.sql_input_in_table_authors(value_name_author, value_birthday))

        # non-template input
        except mysql.connector.errors.DataError:
            sticker_id = 'CAACAgIAAxkBAAIKMGRBr9YDFYSloaHsTh4v9XzRcs-EAAJJCwACZ48hSo1PZZN4TIGRLwQ'
            await bot.send_sticker(message.chat.id, sticker_id)

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return

    if name_table == "books":  # template: title_book code_author pages code_publish
        try:
            list_string = message.text.split()
            title_book = list_string[0]
            code_author = int(list_string[1])
            pages = int(list_string[2])
            code_publish = int(list_string[3])

        # non-template input
        except ValueError:
            sticker_id = 'CAACAgIAAxkBAAIKMGRBr9YDFYSloaHsTh4v9XzRcs-EAAJJCwACZ48hSo1PZZN4TIGRLwQ'
            await bot.send_sticker(message.chat.id, sticker_id)

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return
        except IndexError:
            sticker_id = 'CAACAgIAAxkBAAIKMGRBr9YDFYSloaHsTh4v9XzRcs-EAAJJCwACZ48hSo1PZZN4TIGRLwQ'
            await bot.send_sticker(message.chat.id, sticker_id)

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return

        try:
            answer_unprocessed = str(sq.sql_input_in_table_books(title_book, code_author, pages, code_publish))

        # non-template input
        except mysql.connector.errors.DataError:
            sticker_id = 'CAACAgIAAxkBAAIKMGRBr9YDFYSloaHsTh4v9XzRcs-EAAJJCwACZ48hSo1PZZN4TIGRLwQ'
            await bot.send_sticker(message.chat.id, sticker_id)

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return

    if name_table == "deliveries":  # template: name_delivery name_company address phone OGRN
        try:
            list_string = message.text.split()
            name_delivery = list_string[0]
            name_company = list_string[1]
            address = list_string[2]
            phone = int(list_string[3])
            ogrn = int(list_string[4])

        # non-template input
        except ValueError:
            sticker_id = 'CAACAgIAAxkBAAIKMGRBr9YDFYSloaHsTh4v9XzRcs-EAAJJCwACZ48hSo1PZZN4TIGRLwQ'
            await bot.send_sticker(message.chat.id, sticker_id)

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return
        except IndexError:
            sticker_id = 'CAACAgIAAxkBAAIKMGRBr9YDFYSloaHsTh4v9XzRcs-EAAJJCwACZ48hSo1PZZN4TIGRLwQ'
            await bot.send_sticker(message.chat.id, sticker_id)

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return

        try:
            answer_unprocessed = str(sq.sql_input_in_table_deliveries(name_delivery, name_company,
                                                                      address, phone, ogrn))

        # non-template input
        except mysql.connector.errors.DataError:
            sticker_id = 'CAACAgIAAxkBAAIKMGRBr9YDFYSloaHsTh4v9XzRcs-EAAJJCwACZ48hSo1PZZN4TIGRLwQ'
            await bot.send_sticker(message.chat.id, sticker_id)

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return

    if name_table == "publishing_house":  # template: publishing_house city
        try:
            list_string = message.text.split()
            publishing_house = list_string[0]
            city = list_string[1]

        # non-template input
        except IndexError:
            sticker_id = 'CAACAgIAAxkBAAIKMGRBr9YDFYSloaHsTh4v9XzRcs-EAAJJCwACZ48hSo1PZZN4TIGRLwQ'
            await bot.send_sticker(message.chat.id, sticker_id)

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return

        try:
            answer_unprocessed = str(sq.sql_input_in_table_publishing_house(publishing_house, city))

        # non-template input
        except mysql.connector.errors.DataError:
            sticker_id = 'CAACAgIAAxkBAAIKMGRBr9YDFYSloaHsTh4v9XzRcs-EAAJJCwACZ48hSo1PZZN4TIGRLwQ'
            await bot.send_sticker(message.chat.id, sticker_id)

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return

    if name_table == "purchases":  # template: code_book date_order, code_delivery, amount
        try:
            list_string = message.text.split()
            code_book = int(list_string[0])
            date = datetime.datetime.strptime(list_string[1], '%Y-%m-%d')
            date_order = str(date.date())
            code_delivery = int(list_string[2])
            amount = float(list_string[3])

        # non-template input
        except ValueError:
            sticker_id = 'CAACAgIAAxkBAAIKMGRBr9YDFYSloaHsTh4v9XzRcs-EAAJJCwACZ48hSo1PZZN4TIGRLwQ'
            await bot.send_sticker(message.chat.id, sticker_id)

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return
        except IndexError:
            sticker_id = 'CAACAgIAAxkBAAIKMGRBr9YDFYSloaHsTh4v9XzRcs-EAAJJCwACZ48hSo1PZZN4TIGRLwQ'
            await bot.send_sticker(message.chat.id, sticker_id)

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return

        try:
            answer_unprocessed = str(sq.sql_input_in_table_purchases(code_book, date_order, code_delivery, amount))

        # non-template input
        except mysql.connector.errors.DataError:
            sticker_id = 'CAACAgIAAxkBAAIKMGRBr9YDFYSloaHsTh4v9XzRcs-EAAJJCwACZ48hSo1PZZN4TIGRLwQ'
            await bot.send_sticker(message.chat.id, sticker_id)

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return

    # user data to be entered into the database
    await state.update_data(user_string=message.text)
    data = await state.get_data()

    # notification of successful completion
    answer = re.sub(r'[(),]', "", answer_unprocessed)

    sticker_id = 'CAACAgQAAxkBAAIKMmRBsGyW_A_XseQQVJaARWnw41zfAAI-AQACqCEhBrJy8YE-YrIMLwQ'
    await bot.send_sticker(message.chat.id, sticker_id)

    await message.answer(f"Ваша строка \"{data['user_string']}\" успешна занесена в базу данных на {answer} позицию",
                         reply_markup=kb.greet_kb)

    # result of successful execution
    rows = sq.sql_output_table(name_table)
    if name_table == "authors":
        await bot.send_message(message.from_user.id, output_authors(rows), parse_mode='HTML')
    if name_table == "books":
        await bot.send_message(message.from_user.id, help_output_books(rows), parse_mode='HTML')
    if name_table == "deliveries":
        await bot.send_message(message.from_user.id, output_deliveries(rows), parse_mode='HTML')
    if name_table == "publishing_house":
        await bot.send_message(message.from_user.id, output_publishing_house(rows), parse_mode='HTML')
    if name_table == "purchases":
        await bot.send_message(message.from_user.id, help_output_purchases(rows), parse_mode='HTML')

    # stop waiting for user data to be entered into the database
    await state.finish()


@dp.message_handler(state=StringState.waiting_delete_number)
async def get_user_number_for_delete(message: types.Message, state: FSMContext):  # (some one number) template: /d+
    name_function = 'number_for_delete'
    write_log(message, name_function)

    # non-template input
    if re.search(r'\D+', message.text):
        sticker_id = 'CAACAgIAAxkBAAIKMGRBr9YDFYSloaHsTh4v9XzRcs-EAAJJCwACZ48hSo1PZZN4TIGRLwQ'
        await bot.send_sticker(message.chat.id, sticker_id)

        await message.answer("Пожалуйста, введите только число и только одно число!"
                             "\n\nДля отмены действия - команда /cancel")
        return

    # input - 0
    if re.fullmatch(r'0', message.text):
        sticker_id = 'CAACAgIAAxkBAAIKMGRBr9YDFYSloaHsTh4v9XzRcs-EAAJJCwACZ48hSo1PZZN4TIGRLwQ'
        await bot.send_sticker(message.chat.id, sticker_id)

        await message.answer("Пожалуйста, не вводите 0... Зачем?\n"
                             "Поглядите, нет же строки с таким номером..."
                             "\n\nДля отмены действия - команда /cancel")
        return

    # delete from table "authors"
    if name_table == "authors":
        try:
            sq.sql_delete_from_table_authors(message.text)  # sql query for delete from the table

        # non-template input
        except mysql.connector.errors.DataError:
            sticker_id = 'CAACAgIAAxkBAAIKMGRBr9YDFYSloaHsTh4v9XzRcs-EAAJJCwACZ48hSo1PZZN4TIGRLwQ'
            await bot.send_sticker(message.chat.id, sticker_id)

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return

    # delete from table "books"
    if name_table == "books":
        try:
            sq.sql_delete_from_table_books(message.text)  # sql query for delete from the table

        # non-template input
        except mysql.connector.errors.DataError:
            sticker_id = 'CAACAgIAAxkBAAIKMGRBr9YDFYSloaHsTh4v9XzRcs-EAAJJCwACZ48hSo1PZZN4TIGRLwQ'
            await bot.send_sticker(message.chat.id, sticker_id)

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return

    # delete from table "deliveries"
    if name_table == "deliveries":
        try:
            sq.sql_delete_from_table_deliveries(message.text)  # sql query for delete from the table

        # non-template input
        except mysql.connector.errors.DataError:
            sticker_id = 'CAACAgIAAxkBAAIKMGRBr9YDFYSloaHsTh4v9XzRcs-EAAJJCwACZ48hSo1PZZN4TIGRLwQ'
            await bot.send_sticker(message.chat.id, sticker_id)

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return

    # delete from table "publishing_house"
    if name_table == "publishing_house":
        try:
            sq.sql_delete_from_table_publishing_house(message.text)  # sql query for delete from the table

        # non-template input
        except mysql.connector.errors.DataError:
            sticker_id = 'CAACAgIAAxkBAAIKMGRBr9YDFYSloaHsTh4v9XzRcs-EAAJJCwACZ48hSo1PZZN4TIGRLwQ'
            await bot.send_sticker(message.chat.id, sticker_id)

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return

    # delete from table "purchases"
    if name_table == "purchases":
        try:
            sq.sql_delete_from_table_purchases(message.text)  # sql query for delete from the table

        # non-template input
        except mysql.connector.errors.DataError:
            sticker_id = 'CAACAgIAAxkBAAIKMGRBr9YDFYSloaHsTh4v9XzRcs-EAAJJCwACZ48hSo1PZZN4TIGRLwQ'
            await bot.send_sticker(message.chat.id, sticker_id)

            await message.answer("Пожалуйста, проверьте ввёденную строку и повторите ввод"
                                 "\n\nДля отмены действия = команда /cancel")
            return

    # user data to be deleted from the database
    await state.update_data(delete_number=message.text)
    data = await state.get_data()

    sticker_id = 'CAACAgIAAxkBAAIBcmRtHfb1AV-Map2-_UrYeEMEgR0AA3wsAALpVQUYN1pRhvpxOmQvBA'
    await bot.send_sticker(message.chat.id, sticker_id)

    await message.answer(f"Ваша строка \"{data['delete_number']}\" успешна удалена из таблицы {name_table}",
                         reply_markup=kb.greet_kb)

    # result of successful execution
    rows = sq.sql_output_table(name_table)  # sql query for delete table output
    if name_table == "authors":
        await bot.send_message(message.from_user.id, output_authors(rows), parse_mode='HTML')
    if name_table == "books":
        await bot.send_message(message.from_user.id, help_output_books(rows), parse_mode='HTML')
    if name_table == "deliveries":
        await bot.send_message(message.from_user.id, output_deliveries(rows), parse_mode='HTML')
    if name_table == "publishing_house":
        await bot.send_message(message.from_user.id, output_publishing_house(rows), parse_mode='HTML')
    if name_table == "purchases":
        await bot.send_message(message.from_user.id, help_output_purchases(rows), parse_mode='HTML')

    # stop waiting for user data to be deleted from the database
    await state.finish()


@dp.message_handler(filters.Text("Выбор функции"), state="*")
async def process_select_function(message: types.Message, state: FSMContext):
    name_function = 'select_function'
    write_log(message, name_function)

    # stop aggressive mode
    await state.finish()

    sticker_id = 'CAACAgIAAxkBAAIKPmRBshqWxIcnfgl7nidDOsEtpSGKAALrFQACFHHAS6IldI7EubbeLwQ'
    await bot.send_sticker(message.chat.id, sticker_id)

    await message.reply("Выберите функцию (для возврата используйте /back)", reply_markup=kb.functions_table_kb)


@dp.message_handler(filters.Text(['Сортировка заказов по общей стоимости', 'Средний чек', 'Топ книг по продажам',
                                  'Топ авторов по продажам']), state="*")
async def process_function_execution(message: types.Message, state: FSMContext):
    name_function = 'execution_function'
    write_log(message, name_function)

    # stop aggressive mode
    await state.finish()

    user_function = message.text

    sticker_id = 'CAACAgIAAxkBAAIKPWRBshrBNyghM2PMeGj72Pq3wiVWAAJ8FAAC-ERoSMJeKBz08FQCLwQ'
    await bot.send_sticker(message.chat.id, sticker_id)

    if user_function == 'Сортировка заказов по общей стоимости':
        user_function = '* FROM purchases ORDER BY Amount DESC;'

        # sql query for functions
        rows = sq.sql_output_function(user_function)
        answer_message = "Функция: Сортировка заказов по общей стоимости\n" + "Результат:\n" + \
                         help_output_purchases(rows)

    if user_function == 'Средний чек':
        user_function = 'AvgPurchase()'

        # sql query for functions
        answer_unprocessed = str(sq.sql_output_function(user_function)[0])
        answer = re.sub(r'[(),]', "", answer_unprocessed)
        answer_message = text("Функция: Средний чек" +
                              "\nРезультат:" +
                              "\n    Средний чек = " + hcode(answer))

    if message.text == 'Топ книг по продажам':
        user_function = 'code_book, COUNT(code_book) AS total FROM purchases GROUP BY code_book ORDER BY total DESC'

        # sql query for functions
        rows = sq.sql_output_function(user_function)
        data = [['Название', 'Количество']]

        for row_unprocessed in rows:
            code_book = row_unprocessed[0]

            # sql query for search for a name book by code
            title_book_unprocessed = sq.sql_output_code("title_book", "books", "code_book", int(code_book))
            title_book = title_book_unprocessed[0]
            count_books = row_unprocessed[1]

            # for a beautiful output of the result
            list_for_insert = [title_book, count_books]
            data.append(list_for_insert)

        # for a beautiful output of the result
        rows_message = '<pre>' + tabulate.tabulate(data) + '</pre>'
        answer_message = "Функция: Топ книг по продажам\n" + "Результат:\n" + rows_message

    if message.text == 'Топ авторов по продажам':
        user_function = 'code_book, COUNT(code_book) AS total FROM purchases GROUP BY code_book ORDER BY total DESC'

        # sql query for functions
        rows = sq.sql_output_function(user_function)
        data = [['ФИО автора', 'Количество']]

        for row_unprocessed in rows:
            code_book = row_unprocessed[0]

            # sql query for search for a name book by code
            code_author_unprocessed = sq.sql_output_code("code_author", "books", "code_book", int(code_book))
            code_author = code_author_unprocessed[0]

            # sql query for search for a name author by code
            name_author_unprocessed = sq.sql_output_code("name_author", "authors", "code_author", int(code_author))
            name_author = name_author_unprocessed[0]
            count_books = row_unprocessed[1]

            # for a beautiful output of the result
            list_for_insert = [name_author, count_books]
            data.append(list_for_insert)

        # for a beautiful output of the result
        rows_message = '<pre>' + tabulate.tabulate(data) + '</pre>'
        answer_message = "Функция: Топ авторов по продажам\n" + "Результат:\n" + rows_message

    await bot.send_message(message.from_user.id, answer_message, reply_markup=kb.greet_kb, parse_mode='HTML')


@dp.message_handler(content_types=types.ContentType.ANY)
async def unknown_message(message: types.Message):
    name_function = 'unknown_message'
    write_log(message, name_function)

    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    message_text = text(emojize('Я не знаю, что с этим делать 😲'),
                        italic('\nЯ просто напомню,'), 'что есть кнопки...\nНу в крайнем случае',
                        code('команда'), '/help', '\nНу мало ли поможет...')

    logging.info(f'{user_id=} | {user_full_name=} | {message.text=} | {time.asctime()}')
    await message.reply(message_text, parse_mode=types.ParseMode.MARKDOWN, reply_markup=kb.greet_kb)

    sticker_id = 'CAACAgIAAxkBAAIKZ2RBtCdiS49S1M7U481qTRiQPL6JAAJWLAAC6VUFGFGX2gqMHlZ_LwQ'
    await bot.send_sticker(message.chat.id, sticker_id)

    # waiting for the second value not provided by the functional
    await Aggressive.first_warning.set()


@dp.message_handler(state=Aggressive.first_warning, content_types=types.ContentType.ANY)
async def second_unknown_message(message: types.Message, state: FSMContext):
    name_function = 'second_unknown_message'
    write_log(message, name_function)

    # the second value not provided by the functional
    await state.update_data(secord_user_message=message.text)

    message_text = text("Не, я серьёзно не понимаю, что происходит🧐\n",
                        italic('Я ещё разок намекну'), ', что есть кнопки или',
                        code('команда'), '/help', '\nНе советую продолжать в том же ключе...')
    await message.reply(message_text, parse_mode=types.ParseMode.MARKDOWN, reply_markup=kb.greet_kb)

    sticker_id = 'CAACAgIAAxkBAAIJwGRBq2U2i6Y-EjqOCAop3bnsFuBGAAJDAAOQczMbR2Gt8nYqJWIvBA'
    await bot.send_sticker(message.chat.id, sticker_id)

    # waiting for the third value not provided by the functional
    await Aggressive.next()


@dp.message_handler(state=Aggressive.second_warning, content_types=types.ContentType.ANY)
async def third_unknown_message(message: types.Message, state: FSMContext):
    name_function = 'third_unknown_message'
    write_log(message, name_function)

    global funny_counter
    funny_counter = 0

    # the third value not provided by the functional
    await state.update_data(third_user_message=message.text)

    message_text = text("Серьёзно?🤨\n",
                        "Работаю только по кнопкам, либо по",
                        code('командам'), '\nНе иначе...')
    await message.reply(message_text, parse_mode=types.ParseMode.MARKDOWN, reply_markup=kb.greet_kb)

    sticker_id = 'CAACAgIAAxkBAAIJvmRBq1RIAns2qUUTnpDVk1QTjmUIAALXQwAC6VUFGAuq1SRIBxqeLwQ'
    await bot.send_sticker(message.chat.id, sticker_id)

    # waiting for the fourth value not provided by the functional
    await Aggressive.next()


@dp.message_handler(state=Aggressive.final_warning, content_types=types.ContentType.ANY)
async def final_unknown_message(message: types.Message, state: FSMContext):
    name_function = 'final_unknown_message'
    write_log(message, name_function)

    global funny_counter

    # the fourth value not provided by the functional
    await state.update_data(final_user_message=message.text)

    # aggressive mode
    # 3 times repeat user's message
    while funny_counter < 3:
        funny_counter += 1
        if not message.text:
            try:
                sticker_id = message.sticker.file_id  # repeat a user's sticker
                await bot.send_sticker(message.chat.id, sticker_id)

            # if user's message is someone file
            except AttributeError:
                sticker_id = 'CAACAgIAAxkBAAIKeWRBtMDLcMJK5ZyQGA9LlkU0yvBoAAKAAAOQczMb-VD4SuSITFYvBA'
                await bot.send_sticker(message.chat.id, sticker_id)
                await bot.send_message(message.chat.id, 'Ну... Вы разошлись на файлы? Поздравляю, что сказать...😒')
            except aiogram.utils.exceptions.MessageTextIsEmpty:
                sticker_id = 'CAACAgIAAxkBAAIKeWRBtMDLcMJK5ZyQGA9LlkU0yvBoAAKAAAOQczMb-VD4SuSITFYvBA'
                await bot.send_sticker(message.chat.id, sticker_id)
                await bot.send_message(message.chat.id, 'Ну... Вы разошлись на файлы? Поздравляю, что сказать...😒')
        # if user's message is text
        else:
            # repeat user's text
            await bot.send_message(message.chat.id, message.text)
        return

    while True:
        smile_list = ['😁', '😒', '😉', '🤝', '🥲', '😙', '😎', '🤓', '😏', '🥺', '😤', '🤯', '🫣',
                      '🤭', '🫡', '🫠', '🫤', '😑', '🙄', '😬', '👍', '🤞', '🌚', '🌝', '↙']
        random_smile = random.choice(smile_list)

        sticker_id = 'CAACAgIAAxkBAAIKPGRBshqifiCSrPxjGOgl9UUQpRusAAKZFgACFEZoSBVmyntC84wLLwQ'
        await bot.send_sticker(message.chat.id, sticker_id)

        message_text = text(emojize("\n\n Если подумали над своим поведением и научились пользоваться командами, "
                                    f"то самое время проверить {random_smile}"
                                    f"\n      /back      /cancel      /help"))

        # if user's message is someone file or sticker
        if not message.text:
            try:
                # repeat user's sticker
                sticker_id = message.sticker.file_id
                await bot.send_sticker(message.chat.id, sticker_id)
            # if user's message is someone file
            except AttributeError:
                sticker_id = 'CAACAgIAAxkBAAIKe2RBtRpQSGDzKEjRfTqL8Z8rUFWcAAJFIAACpFR5SlZabV_Stf-rLwQ'
                await bot.send_sticker(message.chat.id, sticker_id)
                await bot.send_message(message.chat.id, 'Ну... Вы разошлись на файлы? Поздравляю, что сказать...😒')
            except aiogram.utils.exceptions.MessageTextIsEmpty:
                sticker_id = 'CAACAgIAAxkBAAIKe2RBtRpQSGDzKEjRfTqL8Z8rUFWcAAJFIAACpFR5SlZabV_Stf-rLwQ'
                await bot.send_sticker(message.chat.id, sticker_id)
                await bot.send_message(message.chat.id, 'Ну... Вы разошлись на файлы? Поздравляю, что сказать...😒')
        # if user's message is text
        else:
            # repeat user's text
            await bot.send_message(message.chat.id, message.text)

        await bot.send_message(message.chat.id, message_text)
        return


if __name__ == '__main__':
    executor.start_polling(dp)
