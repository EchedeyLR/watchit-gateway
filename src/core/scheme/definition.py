"""
Scheme definition for movies used in watchit app
Exceptions:
    - If imdb_code cannot be found add your custom imdb_code ex: tt{movie_id}
"""
from datetime import date
from marshmallow import Schema, fields, validate, INCLUDE

DEFAULT_RATE_MAX = 10
# Just in case according this
# https://en.wikipedia.org/wiki/1870s_in_film
# https://en.wikipedia.org/wiki/List_of_longest_films
# https://en.wikipedia.org/wiki/Fresh_Guacamole
FIRST_MOVIE_YEAR_EVER = 1880
LONGEST_RUNTIME_MOVIE = 51420
SHORTEST_RUNTIME_MOVIE = 100

DEFAULT_GENRES = [
    'All', 'Action', 'Adventure', 'Animation', 'Biography',
    'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
    'Fantasy', 'Film-Noir', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Romance',
    'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western'
]


class ResourceScheme(Schema):
    url = fields.Url(required=True)  # File link
    hash = fields.Str(required=True)  # File hash
    quality = fields.Str(required=True)  # Quality ex: 720p, 1080p..


class MovieSchema(Schema):
    title = fields.Str(validate=validate.Length(min=6))
    # Optional resource id to keep linked ex: origin?id=45
    resource_id = fields.Int(missing=0)
    # Where the data comes from?
    resource_name = fields.Str(validate=validate.Length(min=2))
    # https://es.wikipedia.org/wiki/Internet_Movie_Database
    imdb_code = fields.Str(validate=validate.Regexp(r'^tt[0-9]{5,10}$'))
    rating = fields.Float(validate=validate.Range(min=0, max=DEFAULT_RATE_MAX))
    year = fields.Int(validate=validate.Range(min=FIRST_MOVIE_YEAR_EVER, max=date.today().year + 1))
    runtime = fields.Float(validate=validate.Range(min=SHORTEST_RUNTIME_MOVIE, max=LONGEST_RUNTIME_MOVIE))
    genres = fields.List(fields.Str(), validate=validate.ContainsOnly(choices=DEFAULT_GENRES))
    synopsis = fields.Str(required=True)
    trailer_code = fields.Str(missing=None)  # Youtube trailer code
    # https://meta.wikimedia.org/wiki/Template:List_of_language_names_ordered_by_code
    lang = fields.Str(validate=validate.Length(min=2, max=10))
    # https://en.wikipedia.org/wiki/Motion_Picture_Association_film_rating_system
    mpa_rating = fields.Str(missing=None, validate=validate.Length(min=1, max=5))
    small_cover_image = fields.Url(required=True)
    medium_cover_image = fields.Url(required=True)
    large_cover_image = fields.Url(required=True)
    resource = fields.List(fields.Nested(ResourceScheme()))
    date_uploaded_unix = fields.Int()
