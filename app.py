from flask import Flask,request,jsonify,json
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)

# Create a new client and connect to the server
def get_db():
    uri = "mongodb+srv://test_user:test_password@cluster0.cowkeck.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)

    #local database
    # client = MongoClient('localhost', 27017)

    db = client['employee']
    collection = db['user']

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    return collection


@app.route("/")
def home():
    endpoint_data={"All users: ":"/user","Add user: ":"/user + data","Update user: ":"/user<int:id> + data","Delete user: ":"/user/<int:id>"}
    return jsonify(endpoint_data),200

@app.route("/user/",methods=['GET','POST'])
def user():
    if request.method == 'GET':
        try:
            collection=get_db()
            data=collection.find()
            data=dumps(list(data),indent = 2)
            data=json.loads(data)
            return jsonify(data),200
        except:
            pass
        finally:
            if type(collection)==MongoClient:
                collection.close()

    if request.method == 'POST':
        try:
            collection=get_db()
            data=request.get_json()
            # print(data)
            id=data.get('id')
            name=data.get('name')
            email=data.get('email')
            password=data.get('password')
            user_data=collection.find({"id":id})
            if len(list(user_data)):
                return jsonify("already exists"),400
            collection.insert_one({"id":id,"name":name,"email":email,"password":password})
            return jsonify("inserted successfully"),200
        except:
            pass
        finally:
            if type(collection)==MongoClient:
                collection.close()
    

@app.route("/user/<int:id>/",methods=['GET','DELETE','PUT'])
def user_id(id):
    if request.method == 'GET':
        try:
            collection=get_db()
            user_data=collection.find({"id":id})
            if len(list(user_data)):
                data=collection.insert_one({"id": id}).inserted_id
                data=dumps(list(data),indent = 2)
                data=json.loads(data)
                return jsonify(data),200
            return jsonify("user does not exists"),400
        except:
            pass
        finally:
            if type(collection)==MongoClient:
                collection.close()
    
    if request.method == 'PUT':
        try:
            collection=get_db()
            user_data=collection.find({"id":id})
            if len(list(user_data)):
                data=request.get_json()
                id=data.get('id')
                name=data.get('name')
                email=data.get('email')
                password=data.get('password')
                collection.update_one({"id":id},{ "$set": {"name": name, "email": email, "password": password } })
                return jsonify("updated successfully"),200
            return jsonify("user does not exists"),400
        except:
            pass
        finally:
            if type(collection)==MongoClient:
                collection.close()

    if request.method == 'DELETE':
        try:
            collection=get_db()
            user_data=collection.find({"id":id})
            if len(list(user_data)):
                collection.delete_one({"id": id})
                return jsonify("deleted successfully"),200
            return jsonify("user does not exists"),400
        except:
            pass
        finally:
            if type(collection)==MongoClient:
                collection.close()
    

if __name__ == "__main__":
    app.run(debug=True)