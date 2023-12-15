from flask import Flask, render_template, request
import csv
from zoomus import ZoomClient
import logging
import dotenv
import os
import json
dotenv.load_dotenv()

logging.basicConfig(level=logging.DEBUG)
#log to stdout
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Flask(__name__)



zoomclientId = os.getenv("zoomservertoserverClientID")
zoomclientSecret = os.getenv("zoomservertoserverClientSecret")
zoomaccountId = os.getenv("zoomservertoserverAccountID")



def defaut_site_id():

    client = ZoomClient(zoomclientId, zoomclientSecret, zoomaccountId)
    call_queues_response = client.phone.call_queues()

    call_queues = json.loads(call_queues_response.content)
    for queue in call_queues['call_queues']:
        logging.debug(queue)
        if queue['site']['name'] == 'Main Site':
            logging.debug("Main Site ID is: " + queue['id'])
            return queue['site']['id']
            
def call_queue_id(cq_name):
    client = ZoomClient(zoomclientId, zoomclientSecret, zoomaccountId)
    call_queues_response = client.phone.call_queues()

    call_queues = json.loads(call_queues_response.content)
    for queue in call_queues['call_queues']:
        logging.debug(queue)
        if queue['name'] == cq_name:
            logging.debug("call queue id is : " + queue['id'])
            return queue['id']



@app.route('/update_zoom_oauth', methods=['GET', 'POST'])
def update_zoom_oauth():
    global zoomclientId
    global zoomclientSecret
    global zoomaccountId

    if request.method == 'POST':
        zoomclientId = request.form['zoomclientId']
        zoomclientSecret = request.form['zoomclientSecret']
        zoomaccountId = request.form['zoomaccountId']

        # Add your code to update the Zoom credentials here
        # Example: print(zoomclientId, zoomclientSecret, zoomaccountid)
        print(zoomclientId, zoomclientSecret, zoomaccountId)

    return render_template('index.html', zoomclientId=zoomclientId, zoomclientSecret=zoomclientSecret, zoomaccountId=zoomaccountId)

@app.route('/', methods=['GET', 'POST'])

def index():

    return render_template('index.html', zoomclientId=zoomclientId, zoomclientSecret=zoomclientSecret, zoomaccountId=zoomaccountId)


@app.route('/add_call_queue_members', methods=['GET', 'POST'])

def add_call_queue_members():
        client = ZoomClient(zoomclientId, zoomclientSecret, zoomaccountId)
        output = None
        action_success = False
        
        if request.method == 'POST':
            file = request.files['csv_file']
            # Process the CSV file here
            # You can access the file using file.stream

            # Add your code to process the CSV file
            csv_data = file.stream.read().decode('utf-8')
            reader = csv.reader(csv_data.splitlines())
            next(reader)
            for row in reader:
                id = call_queue_id(row[0])
                # Process each row of the CSV file
                # Example: print(row)
                dict = {'users': [ { 'email' : row[1]} ] } 
                client_request = client.phone.call_queue_members(id=id , members = dict)
                
                

            if client_request.status_code == 201:
                logger.debug("queue member added successfully")
                action_success = True
                output = "complete! check the logs for details"
            else:
                output = client_request.json()

           

        return render_template('index.html', zoomclientId=zoomclientId, zoomclientSecret=zoomclientSecret, zoomaccountId=zoomaccountId, output=output, action_success=action_success)

@app.route('/change_call_queue_manager', methods=['GET', 'POST'])
def change_call_queue_manager():
    output = None
    action_success = False
    if request.method == 'POST':
        file = request.files['csv_file']
        # Process the CSV file here
        # You can access the file using file.stream
        client = ZoomClient(zoomclientId, zoomclientSecret, zoomaccountId)
        # Add your code to process the CSV file
        csv_data = file.stream.read().decode('utf-8')
        reader = csv.reader(csv_data.splitlines())
        next(reader)
        for row in reader:
            client_request = client.phone.call_queues_manager(id=row[0],member_id=row[1])
            # Process each row of the CSV file
            # Example: print(row)
           
            print(client_request.json())
        if client_request.status_code == 201:
            logger.debug("queue manager updated successfully")
            action_success = True
            output = client_request.json()
        

    return render_template('index.html', zoomclientId=zoomclientId, zoomclientSecret=zoomclientSecret, zoomaccountId=zoomaccountId, output=output, action_success=action_success)


@app.route('/create_call_queue', methods=['GET', 'POST'])
def create_call_queue():
    output = None
    action_success = False
    if request.method == 'POST':
        
        
        
        default_id = defaut_site_id()
        
        file = request.files['csv_file']
        # Process the CSV file here
        # You can access the file using file.stream

        # Add your code to process the CSV file
        csv_data = file.stream.read().decode('utf-8')
        reader = csv.reader(csv_data.splitlines())
        #skip the headers
        client = ZoomClient(zoomclientId, zoomclientSecret, zoomaccountId)
        next(reader)
        for row in reader:
            #client.phone.call_queues_create(name=row[0], description=row[1], extension_number=row[2])
            # Process each row of the CSV file
            # Example: print(row)
            client_request = client.phone.call_queues_create(name=row[0],site_id=default_id,extension_number=row[3])
            
            output = client_request.json()
        
        if client_request.status_code == 201:
            logger.debug("Call Queue Created Successfully")
            action_success = True
            
                  
                       

    return render_template('index.html', zoomclientId=zoomclientId, zoomclientSecret=zoomclientSecret, zoomaccountId=zoomaccountId, output=output, action_success=action_success)
    

if __name__ == '__main__':
    app.run(debug=True)
