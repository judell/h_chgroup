import json
import requests
import traceback
try:
    from urllib import urlencode
except:
    from urllib.parse import urlencode


class Hypothesis:
    def __init__(self, username=None, token=None, group=None, limit=None, max_results=None, domain=None, host=None, port=None):
        if domain is None:
            self.domain = 'hypothes.is'
        else:
            self.domain = domain
        self.app_url = 'https://%s/app' % self.domain
        self.api_url = 'https://%s/api' % self.domain
        self.query_url = 'https://%s/api/search?{query}' % self.domain
        self.anno_url = 'https://%s/a' % domain
        self.via_url = 'https://via.hypothes.is'
        self.token = token
        self.username = username
        self.single_page_limit = 200 if limit is None else limit  # per-page, the api honors limit= up to (currently) 200
        self.multi_page_limit = 200 if max_results is None else max_results  # limit for paginated results
        self.group = group if group is not None else '__world__'
        if self.username is not None:
            self.permissions = {
                "read": ['group:' + self.group],
                "update": ['acct:' + self.username + '@hypothes.is'],
                "delete": ['acct:' + self.username + '@hypothes.is'],
                "admin":  ['acct:' + self.username + '@hypothes.is']
                }
        else: self.permissions = {}

    def search_all(self, params={}):
        """Call search API with pagination, return row iterator """
        params['offset'] = 0
        params['limit'] = self.single_page_limit
        while True:
            h_url = self.query_url.format(query=urlencode(params, True))
            if self.token is not None:
                r = self.token_authenticated_query(h_url)
                obj = r
            else:
                r = requests.get(h_url)
                obj = r.json()
            rows = obj['rows']
            row_count = len(rows)
            if 'replies' in obj:
               rows += obj['replies']
            row_count = len(rows)
            params['offset'] += row_count
            if params['offset'] > self.multi_page_limit:
                break
            if len(rows) is 0:
                break
            for row in rows:
                yield row

    def post_annotation(self, payload):
        try:
            headers = {'Authorization': 'Bearer ' + self.token, 'Content-Type': 'application/json;charset=utf-8' }
            data = json.dumps(payload, ensure_ascii=False)
            r = requests.post(self.api_url + '/annotations', headers=headers, data=data.encode('utf-8'), verify=False)
            return r
        except:
            e = traceback.print_exc()
            return None

    def token_authenticated_query(self, url=None):
        try:
           headers = {'Authorization': 'Bearer ' + self.token, 'Content-Type': 'application/json;charset=utf-8' }
           r = requests.get(url, headers=headers)
           return r.json()
        except:
            print ( traceback.print_exc() )

       
    def get_annotation(self, id=None):
        h_url = '%s/annotations/%s' % ( self.api_url, id )
        if self.token is not None:
            obj = self.token_authenticated_query(h_url)
        else:
            obj = json.loads(requests.get(h_url))
        return obj
              

