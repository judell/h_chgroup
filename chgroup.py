import traceback
from hypothesis import Hypothesis

from_group = 'HYPOTHESIS GROUP ID' # https://hypothes.is/groups/GROUP_ID/GROUP_DESCRIPTION
to_group = 'HYPOTHESIS GROUP ID'
username = 'HYPOTHESIS USERNAME'
token = 'HYPOTHESIS API TOKEN'  # https://hypothes.is/account/developer

h = Hypothesis(username, token)

params = {'group': from_group}

rows = h.search_all(params)

for row in rows:
    try:
        if 'references' in row:   # skip replies
            continue
        row['user'] = 'acct:' + h.username + '@hypothes.is'
        row['group'] = to_group
        permissions = row['permissions']
        permission_fields = ['admin','update','delete']
        for field in permission_fields:
            permissions[field][0] = 'acct:' + username + '@hypothes.is'
        row['permissions'] = permissions
        del row['created']
        del row['updated']
        del row['id']
        del row['links']
        r = h.post_annotation(row)
        print r.status_code
    except:
        print (traceback.print_exc()) 
    