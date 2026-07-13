from bs4 import BeautifulSoup
import requests

url = "https://wolfcrow.com/100-films-to-see-before-you-die/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
response = requests.get(url, headers=headers)
response.raise_for_status()

contents = response.text 

soup = BeautifulSoup(contents, "html.parser")

tags_list = soup.find_all(name="figcaption")

list_of_movies = [movie.getText().split(" on ")[0] for movie in tags_list]
list_of_movies.reverse()

with open("best_100_movies", mode="w") as file:
    file.write("\n".join(list_of_movies))