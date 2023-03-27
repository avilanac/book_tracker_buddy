import json
import pandas as pd
import numpy as np

def processing_title(title):
   # Returning the title in upper case.
    return title.upper()

def processing_author(author):
    # Returning the author's name in title case.
    return author.title()

def clean_rating(rating):
    # Cleaning the rating column.
    rating = str(rating)
    rating = rating.replace("it was amazing ", "").replace("really liked it ", "").replace("liked it ", "").replace("—", "")
    info_rat = rating.split()
    return info_rat

def processing_star(rating):
    # Trying to convert the first element of the list to a float, which is the number of stars, If it fails, it returns a NaN.
    try:    
        stars = float(rating[0])
        return stars
    except ValueError:
        return np.nan  

def processing_rating(rating):
    # Taking the fourth element of the list, which is the number of ratings, and removing the comma.
    # Then, it is converting it to an integer and returning it.
    ratings = int(rating[3].replace(',', ''))
    return ratings

def processing_score(scores):
    # Taking the second element of the list, which is the number of scores, and removing the comma.
    # Then, it is converting it to an integer and returning it.
    score = scores.split()
    score = int(score[1].replace(',', ''))
    return score

def processing_votes(votes):
    # Taking the first element of the list, which is the number of votes, and removing the comma.
    # Then, it is converting it to an integer and returning it.
    voted = votes.split()
    voted = int(voted[0].replace(',', ''))
    return voted  

def process_data(df):
     
    df['Title'] = df['Title'].apply(processing_title)
    
    df['Author'] = df['Author'].apply(processing_author)
    
    df['Rating'] = df['Rating'].apply(clean_rating)
    
    df['Stars'] = df['Rating'].apply(processing_star)
    
    df['N.Ratings'] = df['Rating'].apply(processing_rating)
    
    df['Score'] = df['Score'].apply(processing_score)
    
    df['People voted'] = df['Votes'].apply(processing_votes)
    
    new_order = ['Title', 'Author', 'Stars', 'N.Ratings', 'Score', 'People voted']
    df = df.reindex(columns=new_order)
    
    return df

if __name__ == "__main__":
       
    data_json = r"E:\Practicas\Proyects\book_tracker_buddy\data\goodreads.json" 
    with open(data_json) as file:
        books = json.load(file)

    df = pd.DataFrame(books)    
    df = process_data(df)
    
    data_csv = r"E:\Practicas\Proyects\book_tracker_buddy\data\goodreads_process.csv"    
    df.to_csv(data_csv, index=False)



