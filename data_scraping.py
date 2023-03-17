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
        
        soup = BeautifulSoup(page.text, 'html.parser')
        books_found = soup.find_all('div', class_='box-producto')
       
        books.extend(books_found) #adds multiple elements
        
    return books

def get_info_book(book):
    
    info_book = {}
    info_book["Title"] = book.find('h3', class_='nombre').text
    info_book["Author"] = book.find('div', class_='autor').text  
    info_book["Discount"] = book.find('div', class_='descuento-v2').text
    info_book["Price before"] = book.find('p', class_='precio-antes').text
    info_book["Price now"] = book.find('p', class_='precio-ahora').text
    info_book["Info"] = book.find('div', class_='autor color-dark-gray metas hide-on-hover').text
    
    return info_book
     
# run the main function only when you want to run the module as a program
if __name__ == "__main__":
    
    BASE_URL = 'https://www.buscalibre.com.co/libros-envio-express-colombia_t.html?'
    
    #"101 Range page number enabled in site"
    page_site = 101
    books = get_html_info(BASE_URL,page_site)
    list_info_books = []
    
    for book in books:
        info_book = get_info_book(book)
        list_info_books.append(info_book)
    
    data_json = r"E:\Practicas\Proyects\book_tracker_buddy\data\buscabooks.json" 
    with open(data_json, "w") as outfile:
        json.dump(list_info_books, outfile, indent=4)