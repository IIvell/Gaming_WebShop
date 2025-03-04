import requests
from django.views import View
from django.shortcuts import render

class SearchGameView(View):
    template_name = 'main/search.html'

    def get(self, request, *args, **kwargs):
        name = request.GET.get('name', '').strip()  # Uzmi ime iz GET parametra

        if not name:  # Ako nema imena u pretrazi, vrati prazne rezultate
            return render(request, self.template_name, {
                'search_results': [],
                'igre': [],
            })

        client_id = "m1omcez0w0d381ai3t4ph15psb9qdx"
        api_key = "vwlk7a56i826otz3pyttsar87ilcxh"
        url = "https://api.igdb.com/v4/games/"

        headers = {
            "Client-ID": client_id,
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # Formiraj upit za IGDB
        base_query = "fields id, name, rating, first_release_date, rating_count, cover.image_id; "
        search_query = f'search "{name}"; '  # Pretraga po imenu
        filters = "where rating_count > 100 & version_parent = null; "
        data = f"{search_query}{base_query}{filters}limit 10;"

        try:
            response = requests.post(url, headers=headers, data=data)

            if response.status_code == 200:
                games = response.json()

                # Dodavanje URL-a za slike
                for game in games:
                    if "cover" in game and "image_id" in game["cover"]:
                        game["cover"]["url"] = f"https://images.igdb.com/igdb/image/upload/t_cover_big/{game['cover']['image_id']}.jpg"
                        game['pk'] = game.get('id')  # Dodajemo 'pk' za svaku igru

                return render(request, self.template_name, {
                    'search_results': games,  # Igra koja je pronađena putem API-a
                    'igre': games,  # Sve igre za prikaz
                })

            else:
                # U slučaju greške sa API-em
                return render(request, self.template_name, {
                    'search_results': [],
                    'igre': [],
                })

        except requests.exceptions.RequestException as e:
            # Ako dođe do greške u komunikaciji s API-jem
            return render(request, self.template_name, {
                'search_results': [],
                'igre': [],
            })