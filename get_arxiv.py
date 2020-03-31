import requests
from bs4 import BeautifulSoup
import sys
from arxiv_command_list import *

search_word = sys.argv[1]
url_number = 0
page = 0
url = get_search(search_word)
urls = [url]

all_data, count = update_data(url)
data_list = [all_data]
counts = [count]

command_explain()
command_list = ["title", "author", "abs", "pdf", "arxiv", "next", "back", "show"]

while True:
    input_command = input("input command: ")

    if input_command == "q":
        break


    if input_command == "show":
        show_data(all_data)
        continue

    elif input_command == "next":
        if count == 50:
            url, url_number = next_page(url, url_number)
            urls.append(url)
            page += 1
            all_data, count = update_data(url)
            print("Moved to page {}".format(page))

        else:
            url = urls[0]
            all_data, count = data_list[0], counts[0]
            print("Moved to page {}".format(0))

        continue

    elif input_command == "back":
        if page != 0:
            url = urls[page - 1]
            url_number -= 50
            all_data, count = update_data(url)
            print("Moved to page {}".format(page))

        else:
            print("This page is first.")

        continue

    elif input_command == "page":
        print("page: {}".format(page))

    number = ""
    number_list = [str(i) for i in range(1, count + 1)]

    for command in command_list:
        if command in input_command:
            number = input_command[-1]

            if number in number_list:
                command_type = input_command.replace(number, "")
                data = all_data[int(number) - 1]
                check_command(command_type, data)
            else:
                print("input number is not exists in list.")

        else:
            continue

    if number == "":
        print("command invalid.")
