from plugins.base_plugin.base_plugin import BasePlugin
from utils.http_client import get_http_session
import logging

logger = logging.getLogger(__name__)


class MarketSnapshot(BasePlugin):
    def generate_settings_template(self):
        params = super().generate_settings_template()
        params["style_settings"] = True
        return params

    # ✅ REQUIRED: this is how InkyPi populates cached data
    def fetch_data(self, settings):
        symbols = settings.get("symbols")
        if not symbols:
            return {}

        url = (
            "https://yahoo-finance-proxy.pietrowicz.workers.dev/"
            f"?symbols={symbols}"
        )

        try:
            session = get_http_session()
            resp = session.get(url, timeout=15)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logger.error("MarketSnapshot fetch failed: %s", e)
            return {}

    def generate_image(self, settings, device_config):
        dimensions = device_config.get_resolution()
        if device_config.get_config("orientation") == "vertical":
            dimensions = dimensions[::-1]

        # ✅ NOW this actually exists
        data = self.get_cached_data() or {}

        image = self.render_image(
            dimensions,
            "market_snapshot.html",
            "market_snapshot.css",
            {
                "indices": data.get("indices", []),
                "stocks": data.get("stocks", []),
                "commodities": data.get("commodities", []),
                "last_updated": data.get("last_updated"),
                "plugin_settings": settings,
            },
        )
        return image
