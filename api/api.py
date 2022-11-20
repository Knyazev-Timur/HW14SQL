from flask import Blueprint, jsonify
import utils

api_blueprint = Blueprint('api_blueprtint', __name__)

@api_blueprint.route("/movie/<title>")
def title_page(title):
    film=utils.get_film_on_title(title)
    return jsonify(film)


@api_blueprint.route("/rating/<censor>")
def rating_page(censor):
    if censor=="children":
        rating = {'rating_low': 'G', 'rating_midle': None, 'rating_hight': None}
    elif censor=="family":
        rating = {'rating_low': 'G', 'rating_midle': 'PG', 'rating_hight': 'PG-13'}
    elif censor == "adult":
        rating = {'rating_low': 'R', 'rating_midle': 'NC-17', 'rating_hight': None}
    else:
        rating = {'rating_low': None, 'rating_midle': None, 'rating_hight': None}
    film=utils.get_rating(**rating)
    return jsonify(film)


@api_blueprint.route("/genre/<genre>")
def genre_page(genre):
    genre = f'%{genre}%'
    film = utils.get_genre(genre)
    return jsonify(film)


@api_blueprint.route("/movie/<old_year>/to/<new_year>")
def year_page(old_year, new_year):
    film = utils.get_year_to_year(old_year, new_year)
    return jsonify(film)


@api_blueprint.route("/change/<film_type>/<year>/<genre>")
def change_page(film_type, year, genre):
    genre = f'%{genre}%'
    film = utils.get_change(film_type, year, genre)
    return jsonify(film)


@api_blueprint.route("/actors/<actor_1>/<actor_2>")
def party_page(actor_1, actor_2):
    actor_1 = f'%{actor_1}%'
    actor_2 = f'%{actor_2}%'
    actors ={'actor_1': actor_1, 'actor_2': actor_2}
    return jsonify(utils.get_party(**actors))


@api_blueprint.route("/random/<censor>/<genre>/<old_year>/<new_year>")
def random_page(censor, genre, old_year, new_year):
    genre = f"%{genre}%"
    if censor == "children":
        rating =  "%G%"
    elif censor == "family":
        rating = "%PG%"
    elif censor == "adult":
        rating =  "%R%"
    else:
        rating = None
    film = utils.get_random(rating, genre, old_year, new_year)
    return jsonify(film)