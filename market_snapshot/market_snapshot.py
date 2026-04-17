from plugins.base_plugin.base_plugin import BasePlugin


class MarketSnapshot(BasePlugin):

    def generate_settings_template(self):
        params = super().generate_settings_template()
        params["style_settings"] = True
        return params

    def generate_image(self, settings, device_config):
        dimensions = device_config.get_resolution()
        if device_config.get_config("orientation") == "vertical":
            dimensions = dimensions[::-1]

        return self.render_image(
            dimensions,
            "market_snapshot.html",
            "market_snapshot.css",
            {
                "plugin_settings": settings  # ✅ styles only
            }
        )
