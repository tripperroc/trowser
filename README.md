# In
# Install mongodb at: 

# Install meteor at: 

# Create default mongo directory
sudo mkdir -p /data/db

# Start up mongodb 
mongod --fork --logpath mongodb.log

# Run Makefile
make all

# Set MONGO_URL environment variable
export MONGO_URL=mongodb://localhost:27017/trowser

# In a separate shell run meteor server
meteor

# connect to local meteor database
# http://localhost:3000