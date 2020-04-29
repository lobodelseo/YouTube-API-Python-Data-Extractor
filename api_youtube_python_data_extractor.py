import json
import re
import requests
import isodate
import locale
import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

class MyHelper:
  def __init__(self):
    pass

  def id_from_url(self, url: str):
    return url.rsplit("/watch?v=", 1)[1]

  def id_from_channel(self, url: str):
    return url.rsplit("/channel", 1)[1]  

  def title_to_underscore(self, title: str):
    title = re.sub('[\W_]+', " ", title)
    title_underscore = title.lower()
    return title_underscore

  def clean_published_date(self, date: str):
    clean_date = date.rsplit(".", 1)[0].replace('T', ' ')
    date_object = datetime.strptime(clean_date, '%Y-%m-%d %H:%M:%S').date()
    return date_object

  def clean_published_time(self, time: str):
    clean_time = time.rsplit(".", 1)[0].replace('T', ' ')
    time_object = datetime.strptime(clean_time, '%Y-%m-%d %H:%M:%S').time()
    return time_object 

  def convert_array_to_string(self, input_seq: []):
    separator = ', '
    final_str = separator.join(input_seq).lower()
    return final_str

  def clean_duration_video(self, time: str):
    duration = isodate.parse_duration(time)
    seconds = duration.total_seconds()
    cleaned_time = timedelta(seconds=int(seconds))
    total_seconds = str(cleaned_time)
    beauty_duration = datetime.strptime(total_seconds, '%H:%M:%S').time()
    return beauty_duration 

  def add_number_thousand_points(self, number:str):
    # Definir el formato deseado
    locale.setlocale(locale.LC_ALL, "es_ES.utf-8")
    int_number = int(number)
    transform_number = locale.format_string('%10.0f', int_number, 1)
    return transform_number

  def convert_id_category_to_category_name(self, number:str):
    switcher = {
      "1":"Film & Animation", 
      "2":"Autos & Vehicles",
      "10":"Music",
      "15":"Pets & Animals",
      "17":"Sports",
      "18":"Short Movies",
      "19":"Travel & Events",
      "20":"Gaming",
      "21":"Videoblogging",
      "22":"People & Blogs",
      "23":"Comedy",
      "24":"Entertainment",
      "25":"News & Politics",
      "26":"Howto & Style",
      "27":"Education",
      "28":"Science & Technology",
      "29":"Nonprofits & Activism",
      "30":"Movies",
      "31":"Anime/Animation",
      "32":"Action/Adventure",
      "33":"Classics",
      "34":"Comedy",
      "35":"Documentary",
      "36":"Drama",
      "37":"Family",
      "38":"Foreign",
      "39":"Horror",
      "40":"Sc-Fi/Fantasy",
      "41":"Thriller",
      "42":"Shorts",
      "43":"Shows",
      "44":"Trailers"
    } 
    def_data = switcher.get(number,"ID inválido")
    return def_data

#==================================================================

class YouTubeAPI:
  def __init__(self, url: str):
    self.json_url = requests.get(url)
    self.data = json.loads(self.json_url.text) 

  def get_video_id(self):
    return self.data["items"][0]["id"]

  def get_video_channel_id(self):
    return self.data["items"][0]["snippet"]["channelId"]  

  def get_video_thumbnail_url(self):
    return self.data["items"][0]["snippet"]["thumbnails"]["high"]["url"] 

  def get_video_channel_name(self):
    return self.data["items"][0]["snippet"]["channelTitle"]

  def get_category_id(self):  
    return self.data["items"][0]["snippet"]["categoryId"]

  def get_made_for_kids(self):
    return self.data["items"][0]["status"]["madeForKids"]  

  def get_video_published_date_time(self):
    return self.data["items"][0]["snippet"]["publishedAt"]

  def get_video_duration(self):  
    return self.data["items"][0]["contentDetails"]["duration"]  

  def get_video_resolution(self):  
    return self.data["items"][0]["contentDetails"]["definition"]    

  def get_video_title(self):
    return self.data["items"][0]["snippet"]["title"]

  def get_video_description(self):
    return self.data["items"][0]["snippet"]["description"]

  def get_video_channel_tags(self):
    return self.data["items"][0]["snippet"]["tags"]

  def get_video_view_count(self):
    return self.data["items"][0]["statistics"]["viewCount"] 

  def get_video_like_count(self):
    return self.data["items"][0]["statistics"]["likeCount"] 

  def get_video_dislike_count(self):
    return self.data["items"][0]["statistics"]["dislikeCount"]

  def get_video_comment_count(self):
    return self.data["items"][0]["statistics"]["commentCount"]

#==================================================================
    
URL_key='ExAmPle0123'					 
path = "youtube-urls.csv"
dataSheet = []

with open(path, "r") as f:
  content = f.readlines()

content = list(map(lambda s: s.strip(), content))
content = list(map(lambda s: s.strip(','), content))       
helper = MyHelper()

for youtube_url in content:
  try: 
    url_for_subs = requests.get(youtube_url)
    pages_soup = BeautifulSoup(url_for_subs.text, 'html.parser')
    div_s = pages_soup.findAll('div')
    video_id = helper.id_from_url(youtube_url)
    url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&part=snippet,contentDetails,statistics,status&key={URL_key}'
    yt_stats = YouTubeAPI(url)
    _id = yt_stats.get_video_id()
    suscribers = div_s[1].find('span',class_="yt-subscription-button-subscriber-count-branded-horizontal yt-subscriber-count").text.strip().replace(',', '.')
    thumbnail_url = yt_stats.get_video_thumbnail_url()
    channel_name = yt_stats.get_video_channel_name() 
    title = yt_stats.get_video_title()
    title = helper.title_to_underscore(title)
    description = yt_stats.get_video_description()
    published_date = yt_stats.get_video_published_date_time()
    published_date = helper.clean_published_date(published_date)
    time = yt_stats.get_video_published_date_time()
    time = helper.clean_published_time(time)
    tags = yt_stats.get_video_channel_tags()
    tags = helper.convert_array_to_string(tags)
    category = yt_stats.get_category_id()
    category = helper.convert_id_category_to_category_name(category)
    duration = yt_stats.get_video_duration()
    duration = helper.clean_duration_video(duration)
    video_resolution = yt_stats.get_video_resolution()
    child_content = yt_stats.get_made_for_kids()
    view_count = yt_stats.get_video_view_count()
    view_count = helper.add_number_thousand_points(view_count)
    likes = yt_stats.get_video_like_count()
    likes = helper.add_number_thousand_points(likes)
    dislikes = yt_stats.get_video_dislike_count()
    dislikes = helper.add_number_thousand_points(dislikes)
    comments = yt_stats.get_video_comment_count()
    channel_id = yt_stats.get_video_channel_id()
    dataSheet.append([_id, thumbnail_url, channel_name, channel_id, title, description, published_date, time, tags, category, duration, video_resolution, child_content, suscribers, view_count, likes, dislikes, comments])
    columns = ['ID vídeo', 'Thumbnail', 'Nombre canal', 'ID canal', 'Título', 'Descripción', 'Fecha publicación', 'Hora publicación', 'Tags', 'Categoria', 'Duración', 'Resolución', 'Contenido infantil', 'Nº Suscriptores', 'Nº Visualizaciones', 'Nº Likes', 'Nº Dislikes', 'Nº Comentarios']
    df = pd.DataFrame(dataSheet, columns=columns)
    print(df)
  except Exception as e:
    print('Mi error ---->', e) 

df.to_csv("C:/Users/Usuario/Documents/Python Scripts/youtube_urls_results.csv")
# IMPORTANT: Close the file!!!
f.close() 
