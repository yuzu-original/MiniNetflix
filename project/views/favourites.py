from flask import request
from flask_restx import Resource, Namespace, abort

from project.container import favourite_service, auth_service, user_service, movie_service
from project.dao.models import FavouriteSchema, MovieSchema

favourite_ns = Namespace('favorites')
favourites_schema = FavouriteSchema(many=True)
favourite_schema = FavouriteSchema()
movies_schema = MovieSchema(many=True)


@favourite_ns.route('/movies/')
class FavouritesViews(Resource):
    @favourite_ns.doc(description='Get user favourites')
    def get(self):
        auth_data = request.headers['Authorization']
        token = auth_data.split("Bearer ")[-1]

        email = auth_service.get_email(token)
        user_id = user_service.get_by_email(email).id

        favourites = favourite_service.get_user_favourites(user_id)
        return movies_schema.dump(favourites), 200



@favourite_ns.route('/movies/<int:movie_id>/')
class FavouriteView(Resource):
    @favourite_ns.doc(description='Add favourites')
    def post(self, movie_id):
        auth_data = request.headers['Authorization']
        token = auth_data.split("Bearer ")[-1]

        email = auth_service.get_email(token)
        user_id = user_service.get_by_email(email).id
        movie_service.get_one(movie_id) # check movie

        favourite_service.add_favourite(user_id, movie_id)
        return "", 200


    @favourite_ns.doc(description='Delete favourites')
    def delete(self, movie_id):
        auth_data = request.headers['Authorization']
        token = auth_data.split("Bearer ")[-1]

        email = auth_service.get_email(token)
        user_id = user_service.get_by_email(email).id

        favourite_service.delete_favourite(user_id, movie_id)
        return "", 200
