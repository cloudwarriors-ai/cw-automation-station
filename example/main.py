import os
import csv
from zoomus import ZoomClient
import dotenv
import json

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

call_queues_response = client.phone.call_queues()

user_list_response = client.user.list()
user_list = json.loads(user_list_response.content)

call_queues = json.loads(call_queues_response.content)
for queue in call_queues['call_queues']:
    print (queue['id'],queue['name'])
#logger.debug(call_queues.json())


#for user in user_list['users']:
#    print (user['id'],user['display_name'])

cc_queues_response = client.contact_center.queues_list()

cc_queues = json.loads(cc_queues_response.content)

for queue in cc_queues['queues']:
    print (queue['queue_id'],queue['queue_name'])

#logging to stdout


logger.debug("Hello World")





