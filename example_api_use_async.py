import asyncio
import json
import logging
import sys

from dataclasses import asdict
from datetime import datetime

from smartwater import AsyncSmartWaterApi

# Setup logging to StdOut
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


TEST_USERNAME = "fill in your DConnect username here"
TEST_PASSWORD = "fill in your DConnect password here"
#
# Comment out the line below if username and password are set above
from tests import TEST_USERNAME, TEST_PASSWORD


async def main():
    api = None
    try:
        # Process these calls in the right order
        api = AsyncSmartWaterApi(TEST_USERNAME, TEST_PASSWORD)

        # Retrieve profile of this user.
        profile = await api.fetch_profile()
        logger.info(f"profile: {profile}")

        # Once the profile is available, the calls below can be repeated periodically.
        for t in range(30):
            # Retrieve gateway(s) for the profile
            for id in profile.get("config", {}).get("gateway_ids", []):
                gateway = await api.fetch_gateway(id)
                logger.info(f"gateway {id}: {gateway}")

            # Retrieve tanks(s) for the profile
            for id in profile.get("config", {}).get("tank_ids", []):
                device = await api.fetch_device(id)
                logger.info(f"tank {id}: {device}")

            # Retrieve pumps(s) for the profile
            for id in profile.get("config", {}).get("pump_ids", []):
                device = await api.fetch_device(id)
                logger.info(f"pump {id}: {device}")

            # # Alternative: Retrieve all gateway(s) and devices for this user
            # logger.info("")
            # logger.info(f"Query all gateways")

            # gateways = await api.fetch_gateways()
            # for gw_id,gw_dict in gateways.items():
            #     logger.info(f"gateway {gw_id}: {gw_dict}")

            #     devices = await api.fetch_devices(gw_id)
            #     for dev_id,dev_dict in devices.items():
            #         logger.info(f"  device {dev_id}: {dev_dict}")

            # Wait a couple of minutes and retrieve statuses again
            logger.info("")
            logger.info(f"wait ({datetime.now().strftime("%H:%M")})")
            await asyncio.sleep(300)

    except Exception as e:
        logger.info(f"Unexpected exception: {e}")

    finally:
        if api:
            await api.close()


asyncio.run(main())  # main loop