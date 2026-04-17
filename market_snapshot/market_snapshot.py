from plugins.base import PluginBase


class MarketSnapshot(PluginBase):
    def get_template(self):
        return "market_snapshot.html"

    def get_request_url(self):
        symbols = self.get_setting("symbols")
        return (
            "https://yahoo-finance-proxy.pietrowicz.workers.dev/"
            f"?symbols={symbols}"
        )

    def get_template_context(self):
        data = self.data or {}

        return {
            "indices": data.get("indices", []),
            "stocks": data.get("stocks", []),
            "commodities": data.get("commodities", []),
            "last_updated": data.get("last_updated"),
        }
