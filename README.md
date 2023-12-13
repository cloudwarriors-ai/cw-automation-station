You're going to have to create or have existing a server to server auth from the marketplace for the client

https://developers.zoom.us/docs/internal-apps/create/

once that is done place the following paramaters into the .env

zoomservertoserverClientID=<br />
zoomservertoserverAccountID=<br />
zoomservertoserverClientSecret=<br />

pull the zoomus git repo from here : git clone https://github.com/cloudwarriors-ai/zoomus.git

install the zoomus module from inside the zoom us directory like so : pip install .

install the requirements like so : pip install -r requirements.txt

run the application from the app directory like so: python app.py




