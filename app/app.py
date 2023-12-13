from flask import Flask, render_template, request
import csv
from zoomus import ZoomClient
import logging
import dotenv
import os
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
        if request.method == 'POST':
            file = request.files['csv_file']
            # Process the CSV file here
            # You can access the file using file.stream

            # Add your code to process the CSV file
            csv_data = file.stream.read().decode('utf-8')
            reader = csv.reader(csv_data.splitlines())
            for row in reader:
                # Process each row of the CSV file
                # Example: print(row)
                print(row)
            

        return render_template('index.html', zoomclientId=zoomclientId, zoomclientSecret=zoomclientSecret, zoomaccountId=zoomaccountId)

@app.route('/change_call_queue_manager', methods=['GET', 'POST'])
def change_call_queue_manager():
    if request.method == 'POST':
        file = request.files['csv_file']
        # Process the CSV file here
        # You can access the file using file.stream

        # Add your code to process the CSV file
        csv_data = file.stream.read().decode('utf-8')
        reader = csv.reader(csv_data.splitlines())
        for row in reader:
            # Process each row of the CSV file
            # Example: print(row)
            print(row)
        

    return render_template('index.html', zoomclientId=zoomclientId, zoomclientSecret=zoomclientSecret, zoomaccountId=zoomaccountId)

@app.route('/create_call_queue', methods=['GET', 'POST'])
def create_call_queue():
    if request.method == 'POST':
        client = ZoomClient(zoomclientId, zoomclientSecret, zoomaccountId)
        file = request.files['csv_file']
        # Process the CSV file here
        # You can access the file using file.stream

        # Add your code to process the CSV file
        csv_data = file.stream.read().decode('utf-8')
        reader = csv.reader(csv_data.splitlines())
        #skip the headers
        next(reader)
        for row in reader:
            #client.phone.call_queues_create(name=row[0], description=row[1], extension_number=row[2])
            # Process each row of the CSV file
            # Example: print(row)
            client_request = client.phone.call_queues_create(name=row[0],site_id=row[2],extension_number=row[3])
            print(row[0], row[1], row[2])
            print(client_request.json())
        if client_request.status_code == 201:
            logger.debug("Call Queue Created Successfully")
            action_success = True
            output = client_request.json()
                  
           
            

    return render_template('index.html', zoomclientId=zoomclientId, zoomclientSecret=zoomclientSecret, zoomaccountId=zoomaccountId, output=output, action_success=action_success)
    

if __name__ == '__main__':
    app.run(debug=True)
