import json
import pandas as pd
import numpy as np

def processing_title(title):
    return title.upper()

def processing_author(author):
    return author.title()

def processing_discount(discount):
    try:    
        discount = discount.replace('%dcto', '')
        return int(discount)
    except ValueError:
        return 0

def processing_price_now(price):
    try:    
        price = price.replace('.','')[2:]
        return int(price)
    except ValueError:
        return np.nan
    
def processing_price_before(row):
    if row['Discount'] == 0:
        return row['Price now']
    else:
        price = row['Price before'].replace('.','')[2:]
        return int(price)

def processing_info(info):      
    info = info.split(',')
    info_sorted = [i.strip().upper() for i in info]    
    return info_sorted

def extracting_editorial(info_sorted):
    editorial = info_sorted[0]
    return editorial

def extracting_year(info_list):
    for i in info_list:
        if i.isdigit() and len(i) == 4:
            return i
    return np.nan   

def process_data(df):
     
    df['Title'] = df['Title'].apply(processing_title)
    
    df['Author'] = df['Author'].apply(processing_author)
    
    df['Discount'] = df['Discount'].apply(processing_discount)
    
    df['Price now'] = df['Price now'].apply(processing_price_now)
    
    df['Price before'] = df.apply(processing_price_before, axis=1)
    
    df['Info_p'] = df['Info'].apply(processing_info)
    
    df['Editorial'] = df['Info_p'].apply(extracting_editorial)
    
    df['Year'] = df['Info_p'].apply(extracting_year)
    df['Year'] = df['Year'].fillna(0).astype('int64')
    
    df = df.drop(['Info', 'Info_p'], axis='columns') 
        
    return df

if __name__ == "__main__":
       
    data_json = r"E:\Practicas\Proyects\book_tracker_buddy\data\buscabooks.json" 
    with open(data_json) as file:
        books = json.load(file)

    df = pd.DataFrame(books)    
    df = process_data(df)
    
    data_csv = r"E:\Practicas\Proyects\book_tracker_buddy\data\buscabooks_process.csv"    
    df.to_csv(data_csv, index=False)
    


