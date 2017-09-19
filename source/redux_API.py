import falcon
from falcon_cors import CORS
import redux_DB
import json


class EventResource(object):

    def on_get(self, req, resp, event):
        #check parameters and get next person object from the redux model
        response = model.get_next_call(event)
        if 'error' in response:
            resp.status = falcon.HTTP_204
        else:
            resp.status = falcon.HTTP_200
        resp.body = json.dumps(response)


# Create the redux model and the HTTP routes and handlers,
# including allowed cross-domain origin URLs
model = redux_DB.redux_model()
cors = CORS(allow_origins_list=['http://localhost:8080'])
api = falcon.API(middleware=[cors.middleware])
event = EventResource()
api.add_route('/{event}', event)
