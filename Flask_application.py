from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.users import UserRegister
from resources.Items import Item, ItemList
from resources.store import Store,StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)
@app.before_first_request
def create_tables():
 db.create_all()

jwt = JWT(app, authenticate, identity)

#Association of the routes
api.add_resource(Item,'/items/<name>')
api.add_resource(ItemList,'/items')


#Add Store association of routes
api.add_resource(Store,'/stores/<name>') #all POST,DE and GET will instantiate this Class Module
api.add_resource(StoreList,'/stores')
api.add_resource(UserRegister,'/register')


if __name__=='__main__':
 from db import db
 db.init_app(app)
 app.run(host="127.0.0.1",port=6000)
