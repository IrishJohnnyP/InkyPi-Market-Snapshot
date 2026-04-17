from plugins.base_plugin.base_plugin import BasePlugin
from utils.http_client import get_http_session
import logging

logger = logging.getLogger(__name__)


class MarketSnapshot(BasePlugin):

    def generate_settings_template(self):
        template_params = super().generate_settings_template()
        template_params["style_settings"] = True
        return template_params

    def generate_image(self, settings, device_config):
        dimensions = device_config.get_resolution()
        if device_config.get_config("orientation") == "vertical":
            dimensions = dimensions[::-1]

        symbols = settings.get("symbols") or ""
        data = {}

        if symbols:
            try:
                session = get_http_session()
                resp = session.get(
                    f"https://yahoo-finance-proxy.pietrowicz.workers.dev/?symbols={symbols}",
                    timeout=15,
                )
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                logger.error("MarketSnapshot fetch failed: %s", e)

        template_params = {
            "indices": data.get("indices", []),
            "stocks": data.get("stocks", []),
            "commodities": data.get("commodities", []),
            "last_updated": data.get("last_updated"),
            "plugin_settings": settings,
        }

        return self.render_image(
            dimensions,
            "market_snapshot.html",
            "market_snapshot.css",
            template_params,
        )
