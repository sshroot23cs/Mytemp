from flask import Flask, request 
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity


app = Flask(__name__)
app.secret_key = "howsthejosh"
api = Api(app)

# authentication
jwt = JWT(app, authenticate, identity)

# class Student(Resource):

# 	def get(self, name):
# 		return {"name":name}


# api.add_resource(Student,"/student/<string:name>")




# items

items = []


class Item(Resource):

	@jwt_required()
	def get(self, name):
		item = next(filter(lambda x: x["name"] == name, items), None)
		return {"item":item}, 200 if item else 404

	@jwt_required()
	def post(self, name):
		if next(filter(lambda x: x["name"] == name, items), None):
			return {"message": "An item '{}' already exists".format(name)}, 400
		else:
			data = request.get_json(silent=True)
			item = {"name":name, "price": data["price"]}
			items.append(item)
			return item, 201

	@jwt_required()
	def delete(self, name):
		global items
		items = list(filter(lambda x: x["name"] != name, items))
		return {"message": "Item deleted"}, 203

	# @jwt_required
	def put(self, name):
		data = request.get_json(silent=True)
		item = item = next(filter(lambda x: x["name"] == name, items), None)

		if item is None:
			# add item
			item = {"name":name, "price": data["price"]}
			items.append(item)
		else:
			item.update(data)

		return item


class ItemList(Resource):

	# @jwt_required()
	def get(self):
		return {"items":items}

api.add_resource(Item,"/item/<string:name>")
api.add_resource(ItemList,"/items")


app.run(port=5000, debug=True)