# stay-manager
<div align="center">
  <img src="http://roemer.kleerebezem.eu/stay-manager/images/reservation-tab.PNG">
</div>

*Screenshot of the reservation tab*


**stay-manager** is a web-app made for holiday homes to facilitate the management of their bookings.
Notably, it can be used to :

- Record and modify bookings (overnight stays and catering)
- Sync the bookings with a Google Calendar
- Edit invoices and save them as PDFs

<div align="center">
  <img src="http://roemer.kleerebezem.eu/stay-manager/images/invoice-example.PNG">
</div>

*Invoice example*


The front-end was made in **[Vue](https://vuejs.org/)**, using **Buefy** and **Vuex** state management.
The back-end is written in **Python**, using a simple RESTful **[Flask](https://github.com/pallets/flask)** API.

Both services are only served locally, so there are no complementary security features present.

## Install

After cloning the repository, install all dependencies.
```
npm install
```
In order for the Google Calendar synchronisation to work, you will need to create the following files

```
src/scripts/googleapi-key.json
src/scripts/settings.js
```
replacing credentials as indicated in the sample files from the same folder.

You will also need to create an empty *mdm-stay-manager-db.json* file in 

    src/scripts/database

## Run

Run the Python Flask server
```
cd src/scripts
py3 flask_api.py
```
*Make sure the right packages are installed and the server is running on port 5000 of your machine.*

Run the Node front-end
```
npm run serve
```

Then navigate to http://localhost:8080/booking on your browser.


## Disclaimer
This project is was made for internal use at the [Moulin du Merle](http://moulindumerle.com), our familial gite in Burgundy, France.
Please keep in mind that usability was the main focus of the project, so the code will not be perfectly clean.
