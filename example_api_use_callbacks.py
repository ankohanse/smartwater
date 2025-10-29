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
logging.getLogger("grpc").setLevel(logging.WARNING)


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

        # Once the profile is available, register callbacks.
        # This will return the initial value and any changes.
        # Typically, the devices send an update every 30 minutes.

        await api.on_profile(on_profile_change)
    
        for id in gateway_ids:
            await api.on_gateway(id, on_gateway_change)

        for id in tank_ids:
            await api.on_device(id, on_tank_change)

        for id in pump_ids:
            await api.on_device(id, on_pump_change)

        # Keep the application alive...
        for t in range(500):
            # Wait a couple of minutes and retrieve statuses again
            logger.info("")
            logger.info(f"wait ({datetime.now().strftime("%H:%M")})")
            await asyncio.sleep(300)

    except Exception as e:
        logger.info(f"Unexpected exception: {e}")

    finally:
        if api:
            await api.close()


# Limitation: callbacks passed into api.on_[xyz] must be sync functions not async!
def on_profile_change(profile_id: str, profile_dict: dict):
    logger.info(f"profile change {profile_id}")     #: {profile_dict}")

def on_gateway_change(gateway_id: str, gateway_dict: dict):
    logger.info(f"gateway change {gateway_id}")     #: {gateway_dict}")

def on_tank_change(tank_id: str, tank_dict: dict):
    logger.info(f"tank change {tank_id}")     #: {tank_dict}")

def on_pump_change(pump_id: str, pump_dict: dict):
    logger.info(f"pump change {pump_id}")     #: {pump_dict}")


asyncio.run(main())  # main loop