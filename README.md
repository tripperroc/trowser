.trowser

To build this, install mongodb at: 

> http://www.mongodb.org

Install meteor at: 

> https://www.meteor.com

Create default mongo directory

> sudo mkdir -p /data/db

Start up mongodb

>sudo ongod --fork --logpath mongodb.log

Run Makefile

> make all

Set MONGO_URL environment variable

> export MONGO_URL=mongodb://localhost:27017/trowser

Run meteor server

> meteor

Connect to local meteor database

> http://localhost:3000
