from flask_restful import Resource

class Demo(Resource):

    def get(self):
        return {'message': "Hi good afternoon, it's 14:4 now"},200
   