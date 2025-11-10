
import importlib
import json
from urllib import parse, request


# Attempt to import `requests`. If it's not present, we'll use urllib as a
# lightweight fallback so the module doesn't fail at import time.
try:
    requests = importlib.import_module("requests")
except Exception:
    requests = None


ADZUNA_APP_ID = '48cd929b'
ADZUNA_APP_KEY = 'fc10c0373526c703d5ba5781c170aba7'


def _http_get_with_urllib(url, params, timeout=10):
    """Perform a GET request using urllib and return a tuple (status_code, body_bytes)."""
    query = parse.urlencode(params)
    full = f"{url}?{query}"
    req = request.Request(full, method="GET")
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            status = resp.getcode()
            body = resp.read()
            return status, body
    except Exception:
        return None, None


def fetch_jobs(skills, location="India", max_results=5):
    if not skills:
        return []

    query = '+'.join(skills[:3])

    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
    params = {
        'app_id': ADZUNA_APP_ID,
        'app_key': ADZUNA_APP_KEY,
        'results_per_page': max_results,
        'what': query,
        'where': location
    }

    # If requests is available, prefer it for simplicity
    try:
        if requests is not None:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                jobs = response.json().get('results', [])
            else:
                return []
        else:
            status, body = _http_get_with_urllib(url, params)
            if status != 200 or body is None:
                return []
            data = json.loads(body.decode('utf-8'))
            jobs = data.get('results', [])

        results = []
        for job in jobs:
            # Use `.get` everywhere to avoid KeyError when API shape changes
            results.append({
                'title': job.get('title', ''),
                'company': job.get('company', {}).get('display_name', ''),
                'location': job.get('location', {}).get('display_name', ''),
                'description': job.get('description', ''),
                'apply_link': job.get('redirect_url', '')
            })

        return results
    except Exception:
        # Don't raise from here; return empty list on any failure to match
        # previous behavior but keep the import-time resilient approach.
        return []
