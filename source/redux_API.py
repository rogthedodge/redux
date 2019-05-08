import falcon
import json
from source import redux_DB
from falcon_cors import CORS


class CampaignResource(object):

    cors = CORS(allow_all_origins=True)

    def on_get(self, req, resp, group_name):
        #get active campaigns for the group from the redux model
        response = model.list_campaigns(group_name)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(response)


class MemberResource(object):

    cors = CORS(allow_all_origins=True)

    def on_get(self, req, resp, campaign_name):
        #get next member for the campaign from the redux model
        response = model.get_next_member_to_call(campaign_name)
        resp.body = json.dumps(response)


class CallResource(object):

    cors = CORS(allow_all_origins=True)

    def on_post(self, req, resp):
        #check parameters and create a new Call object in the redux model
        if 'member_id' in req.params and 'campaign_id' in req.params and 'outcome'\
        in req.params and 'notes' in req.params and 'date' in req.params:
            model.record_call_details(req.params)
            resp.status = falcon.HTTP_201


# Create the redux model and the HTTP routes and handlers,
cors = CORS(allow_all_origins=True)
model = redux_DB.redux_model()
api = falcon.API(middleware=[cors.middleware])
api.req_options.auto_parse_form_urlencoded = True
api.add_route('/campaigns/{group_name}', CampaignResource())
api.add_route('/call-member/{campaign_name}', MemberResource())
api.add_route('/record-call', CallResource())
