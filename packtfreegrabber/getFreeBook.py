"""Retrieve the Free PacktPub Book of the Day
"""

import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass


PACKTFREE_URL = "https://www.packtpub.com/free-learning"


@dataclass
class FreeBook:
    title: str
    author: str
    description: str
    release: str
    pages: str

    def __post_init__(self):
        self.title = self.title.title()
        self.author = self.author.title()

    def __str__(self):
        s = []
        s.append(f"{'Title:':>12s} {self.title}")
        s.append(f"{'Author:':>12s} {self.author}")
        s.append(f"{'Description:':>12s} {self.description}")
        s.append(f"{'Release:':>12s} {self.release}")
        s.append(f"{'Pages:':>12s} {self.pages}")
        return "\n".join(s)


def get_soup(url: str = None) -> BeautifulSoup:
    """Get a BeautifulSoup for the given URL.

    :param url: optional str URL
    :return: BeautifulSoup
    """

    url = url or PACKTFREE_URL

    with requests.Session() as session:
        response = session.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
    return soup


def find_book_in_soup(soup: BeautifulSoup) -> FreeBook:
    """Looks for a book in the given BeautifulSoup.
    :param soup: BeautifulSoup
    :return: FreeBook
    """

    # XXX what happens when a book isn't found?
    try:
        free_book = soup.find("div", {"class": "main-product"})
        book_title = free_book.find("h3", {"class": "product-info__title"})
        book_author = free_book.find("span", {"class": "free_learning__author"})
        book_desc = free_book.find("div", {"class": "free_learning__product_description"})
        book_release = free_book.find("div", {"class": "free_learning__product_pages_date"})
        book_pages = free_book.find_all(
            "div", {"class": "free_learning__product_pages_date"}
        )
        # Packt might change the classes.
    except AttributeError as ex:
        print("Web page layout has been changed so scraper needs to be updated!")
        print("Open an issue on github when this occurs with the following info:")
        raise ex

    return FreeBook(
        title=book_title.text.strip("\n"),
        author=book_author.text.strip("\n")[3:],
        description=book_desc.text.strip("\n"),
        release=book_release.text.strip("\n"),
        pages=book_pages[1].text.strip("\n"),
    )


def main():
    soup = get_soup()
    book = find_book_in_soup(soup)
    print(book)

