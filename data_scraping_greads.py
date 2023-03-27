from bs4 import BeautifulSoup
import requests
import json

# def get_num_pages(base_url):    
#     pass

def get_html_info(base_url, page_site):
    
    books = []    
    for n in range(1, page_site): 
        # Creating a new url for each page.      
        url = base_url + f"page={n}"         
        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')
        books_found = soup.find('table', {'class': 'tableList js-dataTooltip'})        
        # It's a list comprehension. It's a way to create a list from an iterable.
        books += [x for x in books_found if x != '\n' and x != ' Add query string params ']
        
    return books

def get_info_book(book):
    
    info_book = {}
    info_book["Title"] = book.find('span', itemprop='name').text
    info_book["Author"] = book.find('span', itemprop='author').find('span', itemprop='name').text  
    info_book["Rating"] = book.find('span', class_='minirating').text
    info_book["Score"] = book.find('span', class_='smallText uitext').find('a').text
    info_book["Votes"] = book.find('span', class_='smallText uitext').find_all('a')[1].text    
    
    return info_book
     
# run the main function only when you want to run the module as a program
if __name__ == "__main__":
    
    BASE_URL = 'https://www.goodreads.com/list/show/1.Best_Books_Ever?'
    
    #"101 Range page number enabled in site"
    page_site = 101
    books = get_html_info(BASE_URL,page_site)
    
    list_info_books = []
    
    for book in books:
        info_book = get_info_book(book)
        list_info_books.append(info_book)
    
    data_json = r"E:\Practicas\Proyects\book_tracker_buddy\data\goodreads.json" 
    with open(data_json, "w") as outfile:
        json.dump(list_info_books, outfile, indent=4)