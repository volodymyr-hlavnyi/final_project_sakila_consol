from tools.Actor import Actor
from tools.Film import Film, FilmExtended
from tools.SearchQuery import SearchQuery


class SakilaTools:

    @staticmethod
    def get_categories(cursor):
        cursor.execute(
            """
            select category_id, name from category c
            ;
            """
        )
        result = cursor.fetchall()
        return {key: value for key, value in result}

    @staticmethod
    def get_films_by_category(cursor, category_id, page_number):
        cursor.execute(
            """
            select
                f.film_id,
                f.title,
                f.release_year,
                f.description 
            from film as f
            join
            film_category as fc
            on
            f.film_id = fc.film_id
            where
                fc.category_id = %s
            limit 10
            offset %s
            ;
            """,
            (category_id, page_number * 10),
        )
        result = cursor.fetchall()
        return [Film(data) for data in result]

    @staticmethod
    def get_actors_by_name(cursor, name):
        cursor.execute(
            """
            SELECT 
            actor_id,
            first_name,
            last_name
            from actor a
            where first_name like %s
            or last_name like %s
            ;
            """,
            ("%" + name + "%", "%" + name + "%"),
        )
        result = cursor.fetchall()
        return [Actor(data) for data in result]

    @staticmethod
    def get_films_by_actor(cursor, actor_id):
        cursor.execute(
            """
                select
        f.film_id,
        f.title,
        f.release_year,
        f.description
        from film as f
        join
        film_actor as a
        on
        f.film_id = a.film_id
        where
        a.actor_id = %s
        limit
        10
         """,
            (actor_id,),
        )
        result = cursor.fetchall()
        return [Film(data) for data in result]

    @staticmethod
    def get_columns(db, table_name):
        db.cursor.execute(
            """
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
                ;
            """,
            (db.connection.database, table_name),
        )
        result = db.cursor.fetchall()
        return [row[0] for row in result]

    @staticmethod
    def search_all_fields(db, table_name, search_value):
        columns = SakilaTools.get_columns(db, table_name)
        fileds = "film_id, title,  release_year, description"
        search_query = f"SELECT {fileds} FROM {table_name} WHERE " + " OR ".join([f"{col} LIKE %s" for col in columns])
        search_values = tuple([f"%{search_value}%"] * len(columns))
        db.cursor.execute(search_query, search_values)
        return [Film(f) for f in db.cursor.fetchall()]

    @staticmethod
    def search_film_by_title_and_description(db, table_name, search_value):
        columns = ["film_id", "title", "release_year", "description"]
        search_query = (
            f"SELECT {','.join(columns)} "
            f"FROM {table_name} "
            f"WHERE {columns[0]} LIKE %s "
            f"OR {columns[1]} LIKE %s "
            f"OR {columns[2]} LIKE %s "
            f";"
        )
        db.cursor.execute(
            search_query,
            (
                "%" + search_value + "%",
                "%" + search_value + "%",
                "%" + search_value + "%",
            ),
        )
        return [Film(f) for f in db.cursor.fetchall()]

    @staticmethod
    def search_genre_and_year(db, genre, year):
        search_query = """
                SELECT 
                    f.film_id, 
                    f.title, 
                    f.release_year, 
                    f.description,
                    c.name
                FROM film AS f
                JOIN film_category AS fc
                    ON f.film_id = fc.film_id
                JOIN category AS c
                    ON fc.category_id = c.category_id
                WHERE f.release_year = %s
                    AND c.name LIKE %s
            """
        search_values = (year, "%" + genre + "%")
        db.cursor.execute(search_query, search_values)
        return [FilmExtended(f) for f in db.cursor.fetchall()]

    @staticmethod
    def save_query_to_db(db, table_name, query):
        sql = f"INSERT INTO {table_name} (query) VALUES (%s);"
        db.cursor.execute(sql, (query,))
        db.connection.commit()

    @staticmethod
    def get_top_searches(db, table_name, limit):
        sql = (
            f"SELECT query, COUNT(*) AS cnt " f"FROM {table_name} " f"GROUP BY query " f"ORDER BY cnt DESC " f"LIMIT %s"
        )
        db.cursor.execute(sql, (limit,))
        return [SearchQuery(q) for q in db.cursor.fetchall()]

    @staticmethod
    def get_film_description(db, film_name, film_year):
        sql = """
                select 
                f.description
                from film as f
                join film_category as fc 
                on f.film_id = fc.film_id
                where f.title = %s and f.release_year = %s
                ;"""
        db.cursor.execute(
            sql,
            (
                film_name,
                film_year,
            ),
        )
        result = db.cursor.fetchone()
        return result[0] if result else None
