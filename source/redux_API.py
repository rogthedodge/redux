import falcon
import redux_DB
import json


class EventResource(object):

    def on_get(self, req, resp):
        #check parameters and get next person object from the redux model
        if len(req.params) == 1 and 'event' in req.params :
            response = model.get_person(req.params['event'])
            if 'person_name' in response:
                resp.status = falcon.HTTP_200
            else:
                resp.status = falcon.HTTP_204
        else:
            resp.status = falcon.HTTP_403
            response = "{'error': 'incorrect parameters'}"
        resp.body = json.dumps(response)


# Start the app and add routes and handlers
model = redux_DB.redux_model()
api = falcon.API()
event = EventResource()
api.add_route('/event', event)
