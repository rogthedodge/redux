import falcon
import reduxData
import json

incorrect_params = {"error": "Incorrect Parameters"}
# no_such_user = {"error": "No such user"}

class MessageResource(object):

    def on_get(self, req, resp):
        #check parameters and get next message object from the PS model
        if len(req.params) == 1 and 'name' in req.params :
            response = mdl.get_message(req.params['name'])
            if 'message' in response:
                resp.body = json.dumps(response)
                resp.status = falcon.HTTP_200
            else:
                resp.body = no_such_user
                resp.status = falcon.HTTP_204
        else:
            resp.body = incorrect_params
            resp.status = falcon.HTTP_403

'''    def on_post(self, req, resp):
        #check parameters and create Message object in the PS model
        if len(req.params) == 2 and 'name' in req.params \
        and 'message' in req.params :
            response = mdl.add_message(req.params['name'], \
            req.params['message'])
            if 'message' in response:
                resp.body = json.dumps(response)
                resp.status = falcon.HTTP_200
            else:
                resp.body = no_such_user
                resp.status = falcon.HTTP_204
        else:
            resp.body = incorrect_params
            resp.status = falcon.HTTP_403


class UserResource(object):

    def on_get(self, req, resp):
        #check parameters and get a named user or a list of users
        #from the PS model
        if len(req.params) == 0 :
            resp.body = json.dumps(mdl.get_users())
            resp.status = falcon.HTTP_200
        elif len(req.params) == 1 and 'name' in req.params :
            resp.body = json.dumps(mdl.get_user(req.params['name']))
            resp.status = falcon.HTTP_200
        else:
            resp.body = incorrect_params
            resp.status = falcon.HTTP_403

    def on_delete(self, req, resp):
        #check parameters and delete User object from the PS model
        if len(req.params) == 1 and 'name' in req.params :
            response = mdl.delete_user(req.params['name'])
            if 'name' in response:
                resp.body = json.dumps(response)
                resp.status = falcon.HTTP_200
            else:
                resp.body = no_such_user
                resp.status = falcon.HTTP_204
        else:
            resp.body = incorrect_params
            resp.status = falcon.HTTP_403

    def on_post(self, req, resp):
        #check parameters and create User object in the PS model
        if len(req.params) == 2 and 'name' in req.params \
            and 'email' in req.params :
            resp.body = json.dumps(mdl.add_user(req.params['name'], \
            req.params['email']))
            resp.status = falcon.HTTP_200
        else:
            resp.body = incorrect_params
            resp.status = falcon.HTTP_403'''

# Start the app and add routes and handlers
mdl = PSDataModel.PubSubModel()
api = falcon.API()
message = MessageResource()
user = UserResource()
api.add_route('/users', user)
api.add_route('/messages', message)
