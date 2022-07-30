from flask import request
from flask_restx import Resource, Namespace

from project.container import genre_service
from project.dao.models import GenreSchema

genre_ns = Namespace('genres')
genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()


@genre_ns.route('/')
class GenresViews(Resource):
    @genre_ns.doc(description='Get all genres', params={'page': 'Page number'})
    def get(self):
        page = request.args.get('page', type=int)

        genres = genre_service.get_all(page)
        return genres_schema.dump(genres), 200

@genre_ns.route('/<int:gid>/')
class GenreView(Resource):
    @genre_ns.doc(description='Get genre by id')
    def get(self, gid):
        genre = genre_service.get_one(gid)
        return genre_schema.dump(genre), 200