import requests
from bs4 import BeautifulSoup
from collections import namedtuple


PACKTFREE_URL = "https://www.packtpub.com/free-learning"
FreeBook = namedtuple("FreeBook", "title author description release pages")

def get_soup():
    with requests.Session() as _rs:
        response = _rs.get(PACKTFREE_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def find_book_in_soup(soup):
    free_book = soup.find('div', {'class': 'main-product'})
    book_title = free_book.find('h3', {'class': 'product-info__title'})
    book_author = free_book.find('span', {'class': 'free_learning__author'})
    book_desc = free_book.find('div', {'class': 'free_learning__product_description'})
    book_release = free_book.find('div', {'class': 'free_learning__product_pages_date'})
    book_pages = free_book.find_all('div', {'class': 'free_learning__product_pages_date'})

    fb = FreeBook(
        title=book_title.text.strip("\n"),
        author=book_author.text.strip("\n")[3:],
        description=book_desc.text.strip("\n"),
        release=book_release.text.strip("\n"),
        pages=book_pages[1].text.strip("\n")
    )

    return fb


soup = get_soup()
book = find_book_in_soup(soup)
print(book)