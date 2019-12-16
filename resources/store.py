from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
from models.store import StoreModel

class Store(Resource):
    def get(self,name):
        storeobj=StoreModel.find_by_name(name)
        if storeobj:
            return StoreModel.json(storeobj),200
        return {'message': 'Store not found'}, 404

    def post(self,name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}
        try:
            storeobj=StoreModel(name)
            storeobj.save_to_db()
        except:
            return {'messagae':"An Error detected while uploading the store or creating the store"},500
        return storeobj.json()

    def delete(self,name):
        storeobj=StoreModel(name)
        if storeobj:
            storeobj.delete_from_db()
        return {'message':"Store Deleted Successfully"},200

class StoreList(Resource):
    def get(self):
        return {'stores':[i.json() for i in StoreModel.query.all()]}