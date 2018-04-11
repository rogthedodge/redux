import falcon
import json

from source import redux_DB


class EventResource(object):

    def on_get(self, req, resp, event):
        #get next person for the event from the redux model
        response = model.get_next_person_to_call(event)
        if 'error' in response:
            resp.status = falcon.HTTP_404
        else:
            resp.status = falcon.HTTP_200
        resp.body = json.dumps(response)



class CallResource(object):

    def on_post(self, req, resp):
        #check parameters and create a new Call object in the redux model
        if 'person_id' in req.params and 'event_id' in req.params and 'outcome'\
        in req.params and 'notes' in req.params and 'date' in req.params:
            model.record_call_details(req.params)
            resp.status = falcon.HTTP_201



# Create the redux model and the HTTP routes and handlers,
model = redux_DB.redux_model()
api = falcon.API()
api.req_options.auto_parse_form_urlencoded = True
api.add_route('/event/{event}', EventResource())
api.add_route('/call', CallResource())
