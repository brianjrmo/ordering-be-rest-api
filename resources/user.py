from flask_restful import Resource
from models.user import UserModel

class UserRegister(Resource):
    def get(self,username,schema):
        user=UserModel.find_by_name(username,schema)
        if user:
            return user.json()
        return {'message': 'User not found'},404

    def post(self,username):
        if UserModel.find_by_name(username):
            return {'message':"A user with name '{}' already exists.".format(username)},400
        user = UserModel(username)
        try:
            user.save_to_db()
        except:
            return {'message':'An error occurred while creating the user.'},500
        return user.json(),201

    def delete(self,username):
        user=UserModel.find_by_name(username)
        if user:
            user.delete_from_db()
        return {'message':'user deleted'}


class UserList(Resource):
    def get(self):
        return {'users':[x.json() for x in UserModel.query.all()]}
