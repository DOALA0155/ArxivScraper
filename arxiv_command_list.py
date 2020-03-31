import requests
from bs4 import BeautifulSoup
import webbrowser
import time

def command_explain():
    print("-" * 48)
    print("|    name     |       command        | example |")
    print("-" * 48)
    print("|Get title    | title + index        | title5  |")
    print("|Get authors  | author + index       | author5 |")
    print("|Get abstract | abs + index          | abs5    |")
    print("|Download pdf | pdf + index          | pdf5    |")
    print("|Go to arxiv  | arxiv + index        | arxiv5  |")
    print("|Quit         | type q or conntrol C | q or ^C | ")
    print("-" * 48)
    print("|Current page number                 |page     |")
    print("|Move to next page                   |next     |")
    print("|Move to previous page               |back     |")
    print("|Show current page data              |show     |")
    print("-" * 48 + "\n")

def get_data(data):
    pdf = get_pdf(data)
    title = data.find("p", class_="title is-5 mathjax").text.strip()
    arxiv = data.find("p", class_="list-title is-inline-block").find("a")["href"]
    id = arxiv.split("/")[-1]
    abstract = data.find("span", class_="abstract-full has-text-grey-dark mathjax").text.strip("△ Less\n ")
    author_data = [i.text for i in data.find("p", class_="authors").find_all("a")]
    authors = ", ".join(author_data)
    return title, arxiv, abstract, authors, pdf, id

def get_pdf(data):
    links = data.find("span")
    pdf = ""

    for link in links:
        if "pdf" in link:
            pdf = link["href"]
        else:
            continue

    if pdf == "":

        print("There is no pdf file")

    return pdf

def print_data(title, authors, arxiv, pdf, index):
    print("-" * 160)
    print(index + 1)
    print("title   | {}".format(title))
    print("authors | {}".format(authors))
    print("arxiv   | {}".format(arxiv))
    print("pdf     | {}".format(pdf))
    print("-" * 160 + "\n")

def get_search(search_word):
    word_list = search_word.split(" ")

    search = ""
    for word in word_list:
        if search == "":
            search += word
        else:
            search += "+" + word

    url = "https://arxiv.org/search/?query={}&searchtype=all&abstracts=show&order=-announced_date_first&start=0".format(search)

    return url

def check_command(command_type, data):
    if command_type == "title":
        print("title: {}".format(data["title"]))

    elif command_type == "author":
        print("author: {}".format(data["author"]))

    elif command_type == "abs":
        print("abstract: {}".format(data["abstract"]))

    elif command_type == "pdf":
        url = data["pdf"]
        file = requests.get(url)
        id = data["id"]

        with open("/Users/katsuyamashouki/Desktop/Report/{}.pdf".format(id), "wb") as f:
            f.write(file.content)

        print("pdf is downloaded.")

    elif command_type == "arxiv":
        url = data["arxiv"]
        webbrowser.open(url)

    else:
        print("command is not found.")

def next_page(url, url_number):
    number_len = len(str(url_number))
    url = url[:-number_len:]
    url += str(url_number + 50)
    url_number += 50
    return url, url_number

def show_data(all_data):
    for data in all_data:
        title = data["title"]
        arxiv = data["arxiv"]
        authors = data["author"]
        pdf = data["pdf"]
        index = data["index"]
        print_data(title, authors, arxiv, pdf, index)

def get_all_data(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")

    all_data = []
    data_list = soup.find("ol", class_="breathe-horizontal").find_all("li", class_="arxiv-result")

    for index, data in enumerate(data_list):
        title, arxiv, abstract, authors, pdf, id = get_data(data)

        report_data = {"index": index, "title": title, "arxiv": arxiv, "pdf": pdf, "abstract": abstract, "author": authors, "id": id}
        all_data.append(report_data)

    return all_data

def update_data(url):
    all_data = get_all_data(url)
    count = len(all_data)
    return all_data, count
