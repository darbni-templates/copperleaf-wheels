"""The app's settings. On the server the secrets come from environment variables; the defaults
are for your laptop only."""

import os

SECRET_KEY = os.environ.get("WHEELS_SECRET_KEY", "dev-only-change-me")
# The staff pages under /admin need ?token=<ADMIN_TOKEN>.
ADMIN_TOKEN = os.environ.get("WHEELS_ADMIN_TOKEN", "dev-admin-token")

# PayLater, "buy now, pay in 3": the provider we added at launch.
PAYLATER_MERCHANT_ID = os.environ.get("PAYLATER_MERCHANT_ID", "wheels-sandbox")
PAYLATER_URL = "https://sandbox.paylater.example/v2/plans"
PAYLATER_INSTALMENTS = 3
