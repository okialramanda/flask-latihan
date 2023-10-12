from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.recipe import *
from flask_jwt_extended import get_jwt_identity, jwt_required


class RecipeListResource(Resource):
    def get(self):
        recipes = Recipe.get_all_published()
        data = []  # data diawal masih kosong
        for recipe in recipes:
            data.append(recipe.data())  # data diisi
        return {"data": data}, HTTPStatus.OK

    @jwt_required()
    def post(self):
        data = request.get_json()  # format JSON
        current_user = get_jwt_identity()  # mendapatkan user.id
        recipe = Recipe(  # pengecekan dengan model Recipe
            name=data["name"],
            description=data["description"],
            num_of_servings=data["num_of_servings"],
            cook_time=data["cook_time"],
            directions=data["directions"],
            user_id=current_user,
        )
        # recipe_list.append(recipe)  # mengisi recipe_list dengan data
        recipe.save()  # insert into
        return recipe.data(), HTTPStatus.CREATED  # status created


class RecipeResource(Resource):
    @jwt_required(optional=True)
    def get(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {"message": "recipe not found"}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()  # user.id
        if recipe.user_id != current_user and recipe.is_publish == False:
            return {"message": "Access is denied"}, HTTPStatus.FORBIDDEN

        return recipe.data(), HTTPStatus.OK  # bila access allowed

    @jwt_required()
    def put(self, recipe_id):
        data = request.get_json()
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {"message": "recipe not found"}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()  # user.id
        if current_user != recipe.user_id:
            return {"message": "Access is denied"}, HTTPStatus.FORBIDDEN

        recipe.name = data["name"]
        recipe.description = data["description"]
        recipe.num_of_servings = data["num_of_servings"]
        recipe.cook_time = data["cook_time"]
        recipe.directions = data["directions"]
        recipe.save()  # insert into
        return recipe.data(), HTTPStatus.OK


class RecipePublishResource(Resource):
    def put(self, recipe_id):
        recipe = next(
            (recipe for recipe in recipe_list if recipe.id == recipe_id), None
        )
        if recipe is None:
            return {"message": "recipe not found"}, HTTPStatus.NOT_FOUND
        recipe.is_publish = True
        return {}, HTTPStatus.NO_CONTENT

    def delete(self, recipe_id):
        recipe = next(
            (recipe for recipe in recipe_list if recipe.id == recipe_id), None
        )
        if recipe is None:
            return {"message": "recipe not found"}, HTTPStatus.NOT_FOUND
        recipe.is_publish = False
        # recipe_list.remove(recipe)  # menghapus data dari recipe_list
        return {}, HTTPStatus.NO_CONTENT
