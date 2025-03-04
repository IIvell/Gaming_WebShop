import requests, logging
from django.views.generic import ListView, DetailView
from datetime import datetime
from django.http import Http404
import logging
import json

# Postavljanje logger-a
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Postavljanje razine logiranja, možeš koristiti DEBUG, INFO,

class IgricaListView(ListView):
    template_name = 'main/list.html'
    context_object_name = 'igre'

    def get_queryset(self):
        client_id = "m1omcez0w0d381ai3t4ph15psb9qdx"
        api_key = "vwlk7a56i826otz3pyttsar87ilcxh"
        url = "https://api.igdb.com/v4/games/"

        headers = {
            "Client-ID": client_id,
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",  # Prihvaćamo JSON odgovor
            "Content-Type": "application/x-www-form-urlencoded",  # Osiguravamo ispravan Content-Type
            "User-Agent": "MyGameApp/1.0",  # Dodajemo User-Agent
        }

        order = self.request.GET.get('order', 'rating_desc').strip()

        # Početni upit
        base_query = "fields id, name, rating, first_release_date, rating_count, cover.image_id; "
        filters = "where rating_count > 100 & version_parent = null; "

        # Sortiranje u API-ju
        sort_query = ""
        if order == "date_desc":
            sort_query = "sort first_release_date desc; "
        elif order == "date_asc":
            sort_query = "sort first_release_date asc; "
        elif order == "rating_asc":
            sort_query = "sort rating asc; "
        elif order == "rating_desc":
            sort_query = "sort rating desc; "
        elif order == "name_asc":
            sort_query = "sort name asc; "
        elif order == "name_desc":
            sort_query = "sort name desc; "

        # Finalni upit
        data = f"{base_query}{filters}{sort_query}limit 100;"

        try:
            response = requests.post(url, headers=headers, data=data)

            if response.status_code == 200:
                games = response.json()

                # Dodavanje URL-a za slike
                for game in games:
                    if "cover" in game and "image_id" in game["cover"]:
                        game["cover"]["url"] = f"https://images.igdb.com/igdb/image/upload/t_cover_big/{game['cover']['image_id']}.jpg"
                    game['pk'] = game.get('id')

                return games

            else:
                logger.error(f"IGDB API ERROR {response.status_code}: {response.text}")
                return []

        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return []

        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            return []



class IgricaDetailView(DetailView):
    template_name = 'main/igrica_detail.html'
    context_object_name = 'igrica'

    def get_object(self):
        client_id = "m1omcez0w0d381ai3t4ph15psb9qdx"
        api_key = "vwlk7a56i826otz3pyttsar87ilcxh"
        url = "https://api.igdb.com/v4/games/"
        headers = {
            "Client-ID": client_id,
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
        
        data = f"fields id, name, rating, cover.image_id, summary; where id = {self.kwargs.get('pk')};"    
        response = requests.post(url, headers=headers, data=data)
        
        if response.status_code == 200 and response.json():
            game = response.json()[0]
            
            # Dodavanje URL-a za sliku
            if "cover" in game and "image_id" in game["cover"]:
                game["cover"]["url"] = f"https://images.igdb.com/igdb/image/upload/t_cover_big/{game['cover']['image_id']}.jpg"
            
            return game
        raise Http404("Igra nije pronađena u IGDB API-ju.")

    

