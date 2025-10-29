import json
import logging
import sys
import threading

from dataclasses import asdict
from datetime import datetime
import time

from smartwater import SmartWaterApi

# Setup logging to StdOut
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("grpc").setLevel(logging.WARNING)


TEST_USERNAME = "fill in your DConnect username here"
TEST_PASSWORD = "fill in your DConnect password here"
#
# Comment out the line below if username and password are set above
from tests import TEST_USERNAME, TEST_PASSWORD


def main():
    api = None
    try:
        # Process these calls in the right order
        api = SmartWaterApi(TEST_USERNAME, TEST_PASSWORD, diagnostics_collect=True)

        # Retrieve profile of this user.
        profile = api.fetch_profile()
        logger.info(f"profile ({api.profile_id}): {profile}")

        gateway_ids = []
        tank_ids = []
        pump_ids = []
        account_type = profile.get("accountConfig", {}).get("type")
        if account_type == "basic":
            gateway_id = profile.get("accountConfig", {}).get("basicAccountConfig", {}).get("gatewayId")
            tank_id = profile.get("accountConfig", {}).get("basicAccountConfig", {}).get("tankId")
            pump_id = profile.get("accountConfig", {}).get("basicAccountConfig", {}).get("pumpId")

            if gateway_id: gateway_ids.append(gateway_id)
            if tank_id: tank_ids.append(tank_id)
            if pump_id: pump_ids.append(pump_id)

        # Once the profile is available, the calls below can be repeated periodically.
        for t in range(30):
            # Retrieve gateway(s) for the profile
            for id in gateway_ids:
                gateway = api.fetch_gateway(id)
                logger.info(f"gateway {id}: {gateway}")

            # Retrieve tanks(s) for the profile
            for id in tank_ids:
                device = api.fetch_device(id)
                logger.info(f"tank {id}: {device}")

            # Retrieve pumps(s) for the profile
            for id in pump_ids:
                device = api.fetch_device(id)
                logger.info(f"pump {id}: {device}")

            # # Alternative: Retrieve all gateway(s) and devices for this user
            # logger.info("")
            # logger.info(f"Query all gateways")

            # gateways = api.fetch_gateways()
            # for gw_id,gw_dict in gateways.items():
            #     logger.info(f"gateway {gw_id}: {gw_dict}")

            #     devices = api.fetch_devices(gw_id)
            #     for dev_id,dev_dict in devices.items():
            #         logger.info(f"  device {dev_id}: {dev_dict}")

            # Wait a couple of minutes and retrieve statuses again
            logger.info("")
            logger.info(f"wait ({datetime.now().strftime("%H:%M")})")
            time.sleep(300)

    except Exception as e:
        logger.info(f"Unexpected exception: {e}")

    finally:
        if api:
            api.close()


main()  # main loop