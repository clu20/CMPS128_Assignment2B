from flask import Flask, jsonify, request, make_response, g
from flask_restful import Api, Resource

import os, requests

app = Flask(__name__)
api = Api(app)
forwarding = os.environ.get('FORWARDING_ADDRESS') or 0 ## forwarding ip
newdict = {}

class key_value(Resource):
    def get(self, key):
        #nonempty forwarding address forward to main instance
        if 'FORWARDING_ADDRESS' in os.environ:
            try:
                return requests.get('http://main-container:8080/key-value-store/course1').json()
            except:
                return make_response(jsonify(error= 'Main instance is down', message = 'Error in GET'), 503)
        else:
            if key in newdict:
                #on key value found return found value
                value = newdict[key]
                return make_response(jsonify(doesExist=True, message="Retrieved successfully", value=value), 200)
            else:
                #on key value not found error
                return make_response(jsonify(doesExist=False, error="Key does not exist", message="Error in GET"), 404)

    def put(self, key):
            if len(key) < 50:
                message = request.get_json()
                if key in newdict: ## edit the message
                    if message.get('value'):## data exists
                        newdict[key] = message.get('value')
                        return make_response(jsonify(message="Updated successfully",replaced=True), 200)
                    else: ## data nonexistent
                        return make_response(jsonify(error="Value is missing",message="Error in PUT"), 400)
                else: ##add a new message at key
                    if message.get('value'): ##data exists
                        ##change message of 'key'
                        newdict[key] = message.get('value')
                        return make_response(jsonify(message="Added successfully",replaced=False), 201)
                    else: ##data nonexistent
                        return make_response(jsonify(error="Value is missing",message="Error in PUT"), 400)
            else:
                return make_response(jsonify(error="Key is too long", message="Error in PUT"), 400)

    def delete(self, key):
            if newdict.pop(key,None) == None:
                return make_response(jsonify(doesExist=False, error="Key does not exist", message="Error in DELETE"), 404)
            else:
                return make_response(jsonify(doesExist=True, message="Deleted successfully"), 200)

api.add_resource(key_value, '/key-value-store/', '/key-value-store/<key>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
