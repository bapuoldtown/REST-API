from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item should have a store is associated with it!!!"
                        )
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return ItemModel.json(item)
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}
        data = Item.parser.parse_args()
        #item=ItemModel(name,data['price'],data['store_id'])
        try:
            ItemModel.save_to_db(ItemModel(name,data['price'],data['store_id'])) #cHECKS THE ITEM EXISTENCE ABOVE IN THE TABLE AND TRIGGER THE INSERT FUNCTION BELOW IF NOT PRESENT ELSE ERROR
        except:
            return {"message": "An error occurred inserting the item."}
        return ItemModel(name,data['price'],data['store_id']).json()

    @jwt_required()
    def delete(self, name):
        item=ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message':'Item has been deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        #updated_item = ItemModel(name,data['price'])
        if item is None:
            try:
                item=ItemModel(name,data['price'],data['store_id'])
            except:
                return {"message": "An error occurred inserting the item."}
        else:
            try:
                item.price=data['price']
            except:
                raise
                return {"message": "An error occurred updating the item."}

        item.save_to_db()
        return item.json()

class ItemList(Resource):
    def get(self):
        if len(ItemModel.query.all()) == 0:
            return {'message':"There are currently no items to be displayed"}
        else:
            return {'items': [item.json() for item in ItemModel.query.all()]}
