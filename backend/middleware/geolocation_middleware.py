import requests
import geoip2.database
from django.shortcuts import redirect
from django.conf import settings
from decouple import config
import logging
from django.http import JsonResponse
from monitoring.models import GeoAccessLog

logger = logging.getLogger("geolocation")

IPINFO_TOKEN = settings.IPINFO_TOKEN
PROXYCHECK_KEY = settings.PROXYCHECK_KEY
MAXMIND_DB_PATH = settings.MAXMIND_DB_PATH
REDIRECT_URL = settings.REDIRECT_URL
DEBUG_IP_OVERRIDE = config("DEBUG_IP_OVERRIDE", default=None)


class GeolocationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.reader = geoip2.database.Reader(MAXMIND_DB_PATH)

    # Logging
    def _save_log(self, ip, path, country, is_proxy, status):
        """
        Saves a geolocation access log entry to the database.

        Args:
            ip (str): IP address of the requestor.
            path (str): The requested URL path.
            country (str): Country code determined from the IP.
            is_proxy (bool): Whether the IP was detected as a proxy or VPN.
            status (str): Status description (e.g., 'allowed', 'blocked', 'vpn_blocked').

        Logs:
            Errors during log creation are recorded using the 'geolocation' logger.
        """
        try:
            # Attempt toto Create a Log Record
            GeoAccessLog.objects.create(
                ip_address=ip,
                path=path,
                country=country,
                is_proxy=is_proxy,
                status=status,
            )
        except Exception as e:
            # Log Error if Saving to DB Fails
            logger.error(f"Failed to save GeoAccessLog: {e}")

    def __call__(self, request):
        path = request.path

        if settings.DEBUG and not DEBUG_IP_OVERRIDE:
            return self.get_response(request)

        session = request.session

        # Skip geolocation checks for ignored paths (e.g., static files, admin, media)
        if self.is_ignored_path(request.path):
            return self.get_response(request)

        if session.get("geo_checked"):
            country = session.get("geo_country")
            is_proxy = session.get("geo_proxy")
        else:
            client_ip = DEBUG_IP_OVERRIDE or self.get_client_ip(request)
            country = self.get_country(client_ip)
            is_proxy = self.is_proxy_vpn(client_ip) if country == "CZ" else False

            session["geo_checked"] = True
            session["geo_country"] = country
            session["geo_proxy"] = is_proxy

        if not country:
            logger.warning("Could not determine country.")
            return redirect(REDIRECT_URL)

        if country != "CZ":
            logger.warning(f"Blocked non-CZ IP from {country}.")
            return redirect(REDIRECT_URL)

        if is_proxy:
            logger.warning("CZ user using VPN — showing warning.")
            return JsonResponse(
                {"detail": "VPN detected — please disable it to continue."},
                status=451
            )

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")

    def get_country(self, ip):
        try:
            response = requests.get(
                f"https://ipinfo.io/{ip}/json?token={IPINFO_TOKEN}",
                timeout=2,
            )
            if response.status_code == 200:
                return response.json().get("country")
        except Exception as e:
            logger.error(f"IPInfo error: {e}")

        try:
            response = self.reader.country(ip)
            return response.country.iso_code
        except Exception as e:
            logger.error(f"MaxMind error: {e}")

        return None

    def is_proxy_vpn(self, ip):
        try:
            response = requests.get(
                f"https://proxycheck.io/v2/{ip}?key={PROXYCHECK_KEY}&vpn=1&asn=1&risk=1",
                timeout=2,
            )
            if response.status_code == 200:
                result = response.json().get(ip, {})
                if result.get("proxy") == "yes":
                    return True
        except Exception as e:
            logger.error(f"ProxyCheck error: {e}")
        return False

    def is_ignored_path(self, path):
        return (
            path.startswith("/admin/") or
            path.startswith("/static/") or
            path.startswith("/media/") or
            "favicon" in path
        )