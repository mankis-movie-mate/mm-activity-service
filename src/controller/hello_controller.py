from flask_restx import Namespace, Resource

ns = Namespace("hello", description="Initial endpoint")


@ns.route("/")
class HelloController(Resource):
    def get(self):
        return {"message": "Hello, World!"}
    

@ns.route("/<string:name>")
class HelloUser(Resource):
    def get(self, name):
        return {"message": f"Hello, {name}!"}