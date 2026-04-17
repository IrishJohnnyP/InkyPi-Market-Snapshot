from plugins.base import PluginBase
from plugins.decorators import plugin


@plugin
class MarketSnapshotPlugin(PluginBase):
    NAME = "market_snapshot"
    TEMPLATE = "market_snapshot.html"

    def get_data(self):
        return super().get_data()

    def get_request_url(self):
        symbols = self.get_setting("symbols")
        return (
            "https://yahoo-finance-proxy.pietrowicz.workers.dev/"
            f"?symbols={symbols}"
        )

    def get_template_context(self):
        data = self.get_data() or {}

        return {
            "indices": data.get("indices", []),
            "stocks": data.get("stocks", []),
            "commodities": data.get("commodities", []),
            "last_updated": data.get("last_updated"),
        }
