from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import smtplib


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
to_addrs = input("Please your E-mail :")

response = requests.get("https://www.billboard.com/charts/hot-100/"+date)
web_page_billboard = response.text

soup = BeautifulSoup(web_page_billboard, "html.parser")
articles = soup.find_all(name="span", class_="chart-element__information__song")
songs_titles = []
for art in articles:
    span = str(art)
    txt = span.rsplit('">')
    title = txt[-1].rsplit("</span>")[0]
    songs_titles.append(title)



for title in songs_titles:
    print(title)






sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="f60e91d37e2f4ef0ac91fb2f3e7628b3",
        client_secret="359b86e2e96f4339877a39fc7b374cf8",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in songs_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)






"""

from Send_Email import SendEmail

my_email = "makerlab.futuremakers@gmail.com"
my_password = "19950801Aa@"
subject = f"{date} Top 100 Music listened on your birthday week. "
url = playlist["external_urls"]["spotify"]
body = f'Hi,\n\n We are so glad to share with you the link of the top 100 music listened in your birthday week.\n have fun 🤪  !!!\n {url}'
msg = f"Subject : {subject} \n\n {body}"



SendEmail(my_email,to_addrs,msg,my_password)


"""

from_adress = "makerlab.futuremakers@gmail.com"
subject = f"{date} Top 100 Music listened on your birthday week. "
url = playlist["external_urls"]["spotify"]
body = f'Hi,\n\n We are so glad to share with you the link of the top 100 music listened in your birthday week.\n have fun 🤪  !!!\n {url}'
msg = f"Subject : {subject} \n\n {body}"
password = "19950801Aa@"




with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()
    connection.login(user=from_adress, password=password)
    connection.sendmail(
       from_addr=from_adress,
       to_addrs=to_addrs,
       msg=msg
    )
