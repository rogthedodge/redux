import falcon
import json
from source import redux_DB
from falcon_cors import CORS


class CampaignResource(object):

    def on_get(self, req, resp, group_name):
        #get active campaigns for the group from the redux model
        response = model.list_campaigns(group_name)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(response)


class MemberResource(object):

    def on_get(self, req, resp, campaign_name, prev_id):
        #get next member for the campaign from the redux model
        response = model.get_next_member_to_call(campaign_name, prev_id)
        resp.body = json.dumps(response)


class CallResource(object):

    def on_post(self, req, resp):
        call_data = (json.loads(req.stream.read().decode('utf-8')))
#       check parameters and create a new Call object in the redux model
        if 'member_id' in call_data and 'campaign_id' in call_data:
            model.record_call_details(call_data)
            resp.status = falcon.HTTP_201
            resp.body = "{}"
        else:
            resp.status = falcon.HTTP_500


class UserResource(object):

    def on_get(self, req, resp, email):
#       Get user data or return empty json
        response = model.get_user(email)
        resp.body = json.dumps(response)



# Create the redux model and the HTTP routes and handlers,
cors = CORS(allow_all_origins=True,
                      allow_all_headers=True,
                      allow_all_methods=True,
                      allow_credentials_all_origins=True)
model = redux_DB.redux_model()
api = falcon.API(middleware=[cors.middleware])
api.req_options.auto_parse_form_urlencoded = True
api.add_route('/campaigns/{group_name}', CampaignResource())
api.add_route('/call-member/{campaign_name}/{prev_id}', MemberResource())
api.add_route('/record-call', CallResource())
api.add_route('/user/{email}', UserResource())
