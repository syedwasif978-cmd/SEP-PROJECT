import urllib.request, json, time, sys

BASE = 'http://127.0.0.1:5000'

def get_json(path):
    url = BASE + path
    try:
        with urllib.request.urlopen(url) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        return {'_error': str(e)}

def post_json(path, payload):
    url = BASE + path
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers={'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req) as r:
            txt = r.read().decode()
            try:
                return json.loads(txt)
            except Exception:
                return {'_raw': txt}
    except urllib.error.HTTPError as he:
        try:
            body = he.read().decode()
            return {'_http_error': he.code, 'body': body}
        except Exception:
            return {'_http_error': he.code, 'body': str(he)}
    except Exception as e:
        return {'_error': str(e)}

# wait for server
for i in range(20):
    res = get_json('/api/info')
    if 'app' in res:
        print('SERVER_OK')
        break
    time.sleep(0.5)
else:
    print('SERVER_NOT_AVAILABLE', file=sys.stderr)
    sys.exit(2)

# 1) create PR
pr = post_json('/api/pr/', {'item':'E2E Test Item','qty':2,'requester':'e2e-script'})
print('PR_CREATE:', json.dumps(pr))
pr_id = pr.get('pr', {}).get('id') or pr.get('id')
if not pr_id:
    print('PR_ID_MISSING', file=sys.stderr); sys.exit(3)

# 2) recommend PR
rec = post_json(f'/api/pr/{pr_id}/recommend', {})
print('PR_RECOMMEND:', json.dumps(rec))

# 3) commercial decision (approve)
comm = post_json('/api/commercial/decision', {'pr_id': pr_id, 'approve': True})
print('COMM_DECISION:', json.dumps(comm))

# 4) create PO from PR
po = post_json(f'/api/pr/{pr_id}/create_po', {'vendor_id': None})
print('PO_CREATE:', json.dumps(po))
po_id = po.get('po_id') or (po.get('po', {}).get('id') if isinstance(po.get('po'), dict) else None) or po.get('id')
if not po_id:
    print('PO_ID_MISSING', file=sys.stderr); sys.exit(4)

# 5) receive PO
recv = post_json(f'/api/po/{po_id}/receive', {})
print('PO_RECEIVE:', json.dumps(recv))

# 6) inspect PO (pass)
insp = post_json(f'/api/po/{po_id}/inspect', {'result':'pass'})
print('PO_INSPECT:', json.dumps(insp))

# 7) create invoice (should have been auto-created by inspect) - list pending
acct_pending = get_json('/api/accounts/pending')
print('ACCOUNTS_PENDING:', json.dumps(acct_pending))
acct_id = None
if isinstance(acct_pending, list) and len(acct_pending)>0:
    acct_id = acct_pending[0].get('id')

if acct_id:
    pay = post_json(f'/api/accounts/{acct_id}/pay', {})
    print('ACCOUNT_PAY:', json.dumps(pay))
else:
    print('NO_PENDING_ACCOUNT')

print('E2E_DONE')
