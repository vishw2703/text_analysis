import requests
from bs4 import BeautifulSoup
import os
from scrapping_links import scrapping_links_list

# function to fetch data from url

def fetch_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            text_content = soup.get_text(separator=' ')
            return text_content
        else:
            print("failed to fetch data from {}".format(url))
            return None
        
    except Exception as e:
        print("Error fetching data from {}:{}".format(url,e))
        return None
    

    
# function to save data to a file
    
def save_file(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
                file.write(data)
                print("data saved to {}".format(filename))

    except Exception as e:
        print("Erro saving data to {}:{}".format(filename, e))

# main function
        
def main():
    
    # directory to save files
    directory = "data"
    if not os.path.exists(directory):
        os.makedirs(directory)


    # fethc data from url and save to file
    for idx, url in enumerate(scrapping_links_list, start=1):
        data = fetch_data(url)
        if data:
            filename = os.path.join(directory, f"blackassign{idx:04d}.txt")
            save_file(data,filename)

if __name__ == "__main__":
    main()