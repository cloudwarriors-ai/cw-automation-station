import os
import csv
from zoomus import ZoomClient
import dotenv

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

dotenv.load_dotenv()

zoomclientId = os.getenv("zoomservertoserverClientID")
zoomclientSecret = os.getenv("zoomservertoserverClientSecret")
zoomaccountid = os.getenv("zoomservertoserverAccountID")

client = ZoomClient(zoomclientId, zoomclientSecret, zoomaccountid)

call_queues = client.phone.call_queues()

logger.debug(call_queues.json())

#logging to stdout


logger.debug("Hello World")





