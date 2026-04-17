def fetch_data(self, settings):
    symbols = settings.get("symbols")
    if not symbols:
        return {}

    url = f"https://yahoo-finance-proxy.pietrowicz.workers.dev/?symbols={symbols}"

    try:
        session = get_http_session()
        resp = session.get(url, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        logger.error("MarketSnapshot fetch failed: %s", e)
        return {}
