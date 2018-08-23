from flask_restful import Resource

class Demo(Resource):

    def get(self):
        return {'message': "Hi good afternoon, it's 10:35 now"},200
   