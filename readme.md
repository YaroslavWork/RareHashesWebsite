# Rare Hash Website

### Description

This project showcases the rarest hashes — SHA-256 hashes that start with at least 25 consecutive zeros or ones from the beginning. It serves as a portfolio piece demonstrating both backend logic and integration with external bots.

Users can submit their own hashes, which are then converted to SHA-256 (with plans to add more hashing methods in the future). When a rare hash meeting the criteria is found, it is saved to the database along with the user’s name for recognition.

The project is part of a system consisting (microservices) of three components:

- A web interface displaying the rarest hashes found.

- A [telegram bot](https://github.com/YaroslavWork/RareHashesTelegramBot) that notifies users about new rare hashes.

- An [automated searching bot](https://github.com/YaroslavWork/RareHashFinder) that scans and uploads rare hashes to the database.

This combination highlights advanced backend processing , database management, and real-time user notification integration.

*"Do one thing, and do it well."*

---

### Installation (for linux)

1. Install MongoDB (On Ubuntu):

    [Follow installation process.](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/)

2. Run MongoDB:

    To start and enable it to run on startup:
    ```
    sudo systemctl start mongod
    sudo systemctl enable mongod
    ```

3. Make admin access:

    Connect to mongo shell:
    ```
    mongosh
    ```

    Run inside mongosh:
    ```
    use admin

    db.createUser({
        user: "admin_login",
        pwd: "superVeryStrongPassword",
        roles: [ { role: "userAdminAnyDatabase", db: "admin" }, "readWriteAnyDatabase" ]
    })
    ```

    Enable authentication: 
    ```sh
    sudo nano /etc/mongod.conf
    ```

    Find the security section and add:
    ```yaml
    security:
        authorization: "enabled"
    ```

    Apply changes:
    ```
    sudo systemctl restart mongod
    ```

4. Make user access for database:

    Inside the Mongo shell connected as admin:
    ```
    use hashes

    db.createUser({
        user: "database_login",
        pwd: "veryStrongPassword",
        roles: [ { role: "readWrite", db: "hashDatabase" } ]
    })

5. Launch Telegram Bot (Optional):

    [See installation process.](https://github.com/YaroslavWork/RareHashesTelegramBot)

6. Create **.env** file:

    This file contains all necessary private information. Your **.env** must contain:

    ```
    DATABASE_IP_AND_PORT=127.0.0.1:25000
    TELEGRAM_BOT_IP_AND_PORT=127.0.0.1:33000
    DATABASE_LOGIN=database_login
    DATABASE_PASSWORD=veryStrongPassword
    HOST=127.0.0.1:5000
    DEBUG=False
    PEM_PASS=veryStrongPassword
    ```

    This configuration file contains:
    - ```DATABASE_IP_AND_PORT``` - connection to mongoDB database. This database must have collection 'hashes';
    - ```TELEGRAM_BOT_IP_AND_PORT``` - my other project to connects telegram bot and send notifications in case if users need;
    - ```DATABASE_LOGIN``` - login to mongoDB;
    - ```DATABASE_PASSWORD``` - password to mongoDB;
    - ```HOST``` - site domain;
    - ```DEBUG``` - debugging for developers;
    - ```PEM_PASS``` - https conection password.

7. Create an ssl sertificates:

    Create an **rareHashes.crt** and **rareHashes.key** with for ex. `openssl` and put in **./ssl** directory.

---

### Usage

1. Install docker (In Arch):
    ```
    pacman -S docker
    ```

2. Run docker:

    ```
    sudo systemctl start docker
    ```

    To run docker everytime when you launch:
    ```
    sudo systemctl enable docker
    ```

3. Create an image:
    ```sh
    docker build -t web-server .
    ```

4. Create and run a container:
    ```sh
    docker run -d --name web-server-cont -p 6798:6798 web-server
    ```

---

### Project Structure

This project follows an MVC-inspired architecture. The entry point is **main.py**, and the core logic is organized within the **app** directory:

- **app/services/\*** - Core services responsible for communication with other microservices;
- **app/routes/\*** - Logic handling HTTP routes and request processing;
- **app/static/\*** and **./app/templates/\*** - Frontend assets and HTML templates;
- **app/utils/\*** -  Utility functions used across the project;
- **app/database_utils/\*** - Helper functions for communicating with the database;
- **app/models/\*** - Static classes used to organize and structure data for convenience;
- **app/__init__.py** - Initializes the Flask app and registers Blueprints for modular organization;
- **Dockerfile** and **requirements.txt** - Used to build and run the application in Docker containers.

---

### Dependency

- Python 3.13+;
- All python modules are in **requirements.txt**.

---

### Contributing

Interested in improving the frontend? Contributions are very welcome! Feel free to open a pull request with your changes.

---

### License

MIT License - see `LICENSE` file for details.

---

### Demo

If my server isn’t being used for something else, the project should be running [here](https://158.220.119.11:6798/).