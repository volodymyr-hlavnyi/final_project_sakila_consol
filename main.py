from tools.Connector import Connector
from tools.get_db_config import get_db_config
from tools.SakilaTools import SakilaTools


def init_app():
    dbconfig, dbconfig_write = get_db_config()
    loc_db = Connector(dbconfig, "r")
    loc_db_write = Connector(dbconfig_write, "rw")
    print("==" * 15)
    print("Sakila tools for search films by different parameters.")
    return loc_db, loc_db_write


def close_app(loc_db, loc_db_write):
    loc_db.close()
    loc_db_write.close()
    print("Bye! See you soon!")


def get_menu(menu_num: int = 1):
    menu_list = []
    if menu_num == 1:
        menu_list = [
            "Exit",
            "Search by keyword or phrase (by title or description)",
            "Search by genre and year",
            "View top search queries",
        ]
    elif menu_num == 2:
        pass
    return menu_list


def print_menu_and_input_answer(menu, add_text: str = "item"):
    print("==" * 15)
    for index, line in enumerate(menu):
        print(f" {index} - {line}")
    try:
        result = int(input(f"Select {add_text} (0 - exit)): "))
    except ValueError as e:
        print(f"Error {e}, please try again...")
        result = print_menu_and_input_answer(menu, add_text)
    return result


def print_result(result):
    for index, value in enumerate(result):
        print_index_str = str(index + 1).zfill(len(str(len(result))))
        print(f"{print_index_str} - {value}")


def get_and_print_search_result(wo_print=False):
    key_word = input("Enter key word for search: ")
    SakilaTools.save_query_to_db(db_write, "sakila_history_search", key_word)
    table_name = "film"
    # result = SakilaTools.search_all_fields(db, table_name, key_word)
    result = SakilaTools.search_film_by_title_and_description(db, table_name, key_word)
    if not wo_print:
        print_result(result)


def get_and_print_search_result_by_genre_and_year(wo_print=False):
    while True:
        text_for_search = input("Enter genre and year for search: ").strip()
        if len(text_for_search.split(" ")) != 2:
            print("Error, please enter genre and year in format: genre year")
        else:
            break
    genre = text_for_search.split(" ")[0]
    year = text_for_search.split(" ")[1]
    SakilaTools.save_query_to_db(db_write, "sakila_history_search", text_for_search)
    result = SakilaTools.search_genre_and_year(db, genre, year)
    if not wo_print:
        print_result(result)


def get_and_print_top_search_result(wo_print=False):
    limit = input("Enter limit for top search queries (default 10): ")
    if limit == "":
        limit = 10
    else:
        limit = int(limit)
    result = SakilaTools.get_top_searches(db_write, "sakila_history_search", limit)
    if not wo_print:
        print_result(result)


if __name__ == "__main__":
    db, db_write = init_app()
    while True:
        num_menu_1 = print_menu_and_input_answer(get_menu(1))
        if num_menu_1 == 0:
            break
        elif num_menu_1 == 1:
            get_and_print_search_result()
        elif num_menu_1 == 2:
            get_and_print_search_result_by_genre_and_year()
        elif num_menu_1 == 3:
            get_and_print_top_search_result()
    close_app(db, db_write)
