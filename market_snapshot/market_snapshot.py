from plugins.base_plugin.base_plugin import BasePlugin
from utils.http_client import get_http_session


class MarketSnapshot(BasePlugin):

    def generate_settings_template(self):
        params = super().generate_settings_template()
        params["style_settings"] = True
        return params

    def _fetch_market_data(self):
        url = (
            "https://yahoo-finance-proxy.pietrowicz.workers.dev/"
            "?symbols=^DJI,^GSPC,^IXIC,^VIX|CME,MRX|BTC-USD,GC=F,CL=F"
        )
        session = get_http_session()
        response = session.get(url, timeout=15)
        response.raise_for_status()
        return response.json()

    def generate_image(self, settings, device_config):
        dimensions = device_config.get_resolution()
        if device_config.get_config("orientation") == "vertical":
            dimensions = dimensions[::-1]

        market_data = self._fetch_market_data()

        return self.render_image(
            dimensions,
            "market_snapshot.html",
            "market_snapshot.css",
            {
                "market": market_data,
                "plugin_settings": settings  # required for style pipeline
            }
        )
