import sqlite3
import random


def get_sql(query, parametr):
    """
    :param query: str
    :param parametr: str
    :return: class 'sqlite3.Cursor'
    обращается к БД и экуземпляр класса class 'sqlite3.Cursor'
    """
    with sqlite3.connect('data/netflix.db') as connection:
        cursor = connection.cursor()
        print (type(cursor))
        return cursor.execute(query, parametr)


def read_all_sql():
    """
    :return:  tuple
    Читает БД возвращает все ее поля
    """
    with sqlite3.connect('data/netflix.db') as connection:
        cursor = connection.cursor()
        query = """
            SELECT *
            FROM netflix
            """
        sql_explorer = cursor.execute(query)
        return sql_explorer.fetchall()


def get_film_on_title(film):
    """
    :param film:str
    :return: list
    Возвращает список словарей с запрощенным названием
    """
    query = """
            SELECT "title", "country", "release_year", "listed_in", "description"
            FROM netflix
            WHERE "title" LIKE (?)
            """
    film =f"%{film}%"
    parametr = (film,)

    sql_data = get_sql(query, parametr)
    sql_read = sql_data.fetchall()

    return [
        {
            "title": item[0],
            "country": item[1],
            "release_year": item[2],
            "genre": item[3],
            "description": item[4]
        }
        for item in sql_read
    ]


def get_year_to_year(start, end):
    """
    :param start: str
    :param end: str
    :return: list
    Запрашивает в БД фильмы с года start по год end, выводит от новго к старому
    """
    query = """
                SELECT "title", "release_year"
                FROM netflix
                WHERE "release_year" BETWEEN @start AND @end
                ORDER BY "release_year" DESC
                LIMIT 100
                OFFSET 0
                """
    parametr = (start, end)

    sql_data = get_sql(query, parametr)
    sql_read = sql_data.fetchall()

    return [
        {
            "title": item[0],
            "release_year": item[1]
        }
        for item in sql_read
    ]


def get_rating(rating_low, rating_midle, rating_hight):
    """
    :param rating_low: str
    :param rating_midle: str
    :param rating_hight: str
    :return: list
    Возвращает из БД список фильмов с запрошенным рейтингом
    """
    query = """
                    SELECT "title", "rating", "description"
                    FROM netflix
                    WHERE rating IN (@rating_low, @rating_midle, @rating_hight)
                    """

    # sql_data = cursor.execute(query, (rating_low, rating_midle, rating_hight))
    sql_data = get_sql(query, (rating_low, rating_midle, rating_hight))
    sql_read = sql_data.fetchall()
    return [
        {
            "title": item[0],
            "rating": item[1],
            "description": item[2]
        }
        for item in sql_read
    ]


def get_genre(genre):
    """
    :param genre: str
    :return: list
    Возвращает из БД список фильмов по жанру
    """

    query = """
                    SELECT "title", "description"
                    FROM netflix
                    WHERE "listed_in" LIKE (@genre)
                    ORDER BY "release_year" DESC
                    LIMIT 10
                    OFFSET 0
                    
                    """

    sql_data = get_sql(query, (genre,))
    sql_read = sql_data.fetchall()
    return [
        {
            "title": item[0],
            "description": item[1]
        }
        for item in sql_read
    ]


def get_change(type_film, year, genre):
    """
    :param type_film: str
    :param year: str
    :param genre: str
    :return: dict
    Получает тип, год выхода, жанр вормирует запрос к БД
    и возвращает словарь с ключами title  и  "description"
    """
    query = """
                    SELECT "title", "description"
                    FROM netflix
                    WHERE "type" = @type_film AND "release_year" = @year AND "listed_in" LIKE @genre                  
                    ORDER BY "release_year" DESC
                    LIMIT 10
                    OFFSET 0
            """

    sql_data = get_sql(query, (type_film, year, genre))
    sql_read = sql_data.fetchall()
    return [
        {
            "title": item[0],
            "description": item[1]
        }
        for item in sql_read
    ]


def get_by_cast(actor_1, actor_2):
    """
    Формирует кортеж с кол-ом фильмов, в которых играла пара и актеров, которые играли с парой,
    при условии если пара играла в 2 и более фильмах
    """
    query = """
                        SELECT COUNT("cast") AS count_coast, "cast"
                        FROM netflix
                        WHERE "cast" LIKE @actor_1 AND "cast" LIKE @actor_2
                        GROUP BY "coast"                       
                        HAVING count_coast >=2                           
                        """
    sql_data = get_sql(query, (actor_1, actor_2))
    return sql_data.fetchall()


def get_party(actor_1, actor_2):
    """
    :param actor_1: str
    :param actor_2: str
    :return: list
    Вибирает из БД фильмы, в которых играла пара actor_1, actor_2
    возвращает список актеров, которые играли с парой в более чем 2 фильмах
    """

    query = """
                        SELECT "title", "cast"
                        FROM netflix
                        WHERE "cast" LIKE @actor_1 AND "cast" LIKE @actor_2

                        """
    sql_data = get_sql(query, (actor_1, actor_2))
    sql_read = sql_data.fetchall()

    actors = ''
    # Получили строку с именами всех актеров, которые играли с запрошенной парой

    for i in sql_read:
        actors += i[1] + ','
    actors_list = actors.split(',')[:-1]
    party = {men.lstrip(' ') for men in actors_list if
             actors_list.count(men) >= 2 and men.lstrip(' ') != actor_1.strip('%') and men.lstrip(' ') != actor_2.strip(
                 '%')}
    # Получили множество актеров, которые играли с запрошенными в 2 и более картинах
    return list(party)


def get_random(rating, genre, old_year, new_year):
    """
    :param rating: str
    :param genre: str
    :param old_year: str
    :param new_year: str
    :return: dict
    Когда незнаешь что посмотреть, выбери жанр, рейтинг и годы выхода фильма в прокат...
    Подбирает случайный фильм по заданным параметрам
    """
    query = """
                    SELECT "title", "listed_in", "release_year", "description"
                    FROM netflix
                    WHERE rating LIKE @rating AND "listed_in" LIKE @genre                
                    GROUP BY "release_year"
                    HAVING "release_year" BETWEEN @old_year AND @new_year
                    ORDER BY "release_year" DESC
                    
            """
    sql_data = get_sql(query, (rating, genre, old_year, new_year))
    sql_read = sql_data.fetchall()

    films = [
        {
            "title": item[0],
            "genre": item[1],
            "release_year": item[2],
            "description": item[3]
        }
        for item in sql_read
    ]

    return films[random.randint(0,len(films)-1)]
