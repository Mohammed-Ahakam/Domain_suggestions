def domain_status(domain: str) -> str:
    if not DR_CLIENT or not DR_SECRET:
        return 'maybe'
    try:
        resp = requests.get(
            DOMAINR_URL,
            params={"domain": domain, "client_id": DR_CLIENT, "client_secret": DR_SECRET},
            timeout=5
        )
        data = resp.json()
        status = data.get('status', [{}])[0].get('status', '').lower()
        if status.startswith('undelegated'):
            return 'available'
        if status.startswith('inactive'):
            return 'maybe'
        return 'taken'
    except:
        return 'maybe'