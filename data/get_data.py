import requests
def get_nowplaying(page):

    base_url = 'https://api.themoviedb.org/3'
    # path = '/movie/now_playing'
    path = '/movie/top_rated'
    # path = '/movie/popular'

    params = {
        'api_key' : '9a3de857f4748ebbdaf00bf2940d6c08',
        'language' : 'ko',
        'page':page,
        'region':'kr'
    }
    res = requests.get(base_url+path, params=params)
    data = res.json()
    result = data['results']
    print(len(result))
    return result

result = []

for i in range(1, 101):
    tmp = get_nowplaying(i)
    for i in tmp:
        if i['original_language'] == 'ko':
        # and 10749 not in i['genre_ids'] and 18 not in i['genre_ids']:
            del(i['original_language'])
            del(i['original_title'])
            del(i['backdrop_path'])
            del(i['adult'])
            del(i['vote_count'])
            del(i['video'])
            del(i['popularity'])
            i['pk'] = i['id']
            del(i['id'])
            result.append(i)
movies = []

for i in range(len(result)):
    movies.append({'model':"movies.movie"})
    movies[i]['fields'] = result[i]

# print(movies)

import json

# with open('./recent_kr_movies.json', 'w', encoding='utf-8') as f:
# with open('./popular_kr_movies.json', 'w', encoding='utf-8') as f:
with open('./top_rated_kr_movies.json', 'w', encoding='utf-8') as f:
    json.dump(movies, f, ensure_ascii=False, indent=4)

