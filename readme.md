# Rare Hash Website

### Description

This project showcases the rarest hashes — SHA-256 hashes that start with at least 25 consecutive zeros or ones from the beginning. It serves as a portfolio piece demonstrating both backend logic and integration with external bots.

Users can submit their own hashes, which are then converted to SHA-256 (with plans to add more hashing methods in the future). When a rare hash meeting the criteria is found, it is saved to the database along with the user’s name for recognition.

The project is part of a system consisting of three microservice components:

- A web interface displaying the rarest hashes found.
- A [Telegram bot](https://github.com/YaroslavWork/RareHashesTelegramBot) that notifies users about new rare hashes.
- An [automated searching bot](https://github.com/YaroslavWork/RareHashFinder) that scans and uploads rare hashes to the database.

This combination highlights advanced backend processing, database management, and real-time user notification integration.

*"Do one thing, and do it well."*

---

### Installation (for Linux)

1. Install MongoDB (on Ubuntu):

    [Follow installation process.](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/)

2. Run MongoDB:

    To start and enable it to run on startup:
    ```
    sudo systemctl start mongod
    sudo systemctl enable mongod
    ```

3. Create admin access:

    Connect to the mongo shell:
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

4. Create user access for the database:

    Inside the Mongo shell connected as admin:
    ```
    use hashes

    db.createUser({
        user: "database_login",
        pwd: "veryStrongPassword",
        roles: [ { role: "readWrite", db: "hashDatabase" } ]
    })
    ```

5. Launch Telegram Bot (Optional):

    [See installation process.](https://github.com/YaroslavWork/RareHashesTelegramBot)

6. Create a **.env** file:

    This file contains all necessary private information. Your **.env** must contain:

    ```
    DATABASE_IP_AND_PORT=127.0.0.1:25000
    DATABASE_LOGIN=database_login
    DATABASE_PASSWORD=veryStrongPassword
    HOST=127.0.0.1:5000
    RABBIT_LOGIN=webServer
    RABBIT_PASSWORD=insanelyStrongPassword
    RABBIT_HOST=127.0.0.1:5672
    DEBUG=False
    ```

    This configuration file contains:
    - `DATABASE_IP_AND_PORT` - connection to the MongoDB database. This database must have a collection 'hashes';
    - `DATABASE_LOGIN` - login for MongoDB;
    - `DATABASE_PASSWORD` - password for MongoDB;
    - `HOST` - site domain;
    - `RABBIT_LOGIN` - login for RabbitMQ communicator (see below);
    - `RABBIT_PASSWORD` - password for RabbitMQ communicator (see below);
    - `RABBIT_HOST` - connection to RabbitMQ communicator (see below);
    - `DEBUG` - debugging for developers;

7. Create SSL certificates:

    Create **rareHashes.crt** and **rareHashes.key** with, for example, `openssl` and put them in the **./ssl** directory.

---

### Usage

1. Install Docker (on Arch):
    ```
    pacman -S docker
    ```

2. Run Docker:

    ```
    sudo systemctl start docker
    ```

    To run Docker every time you launch:
    ```
    sudo systemctl enable docker
    ```

3. Launch a RabbitMQ container:
    ```
    docker run -d --hostname my-rabbit --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
    ```

4. Add users to enable communication between servers:

    - Go to the **Admin** section.
    - Add an admin. Username: `admin`; Password: `****`; Tags: `Admin`.
    - Add a management user for the web server. Username: `webServer`; Password: `****`; Tags: `Management`.
    - Add a management user for the Telegram bot. Username: `telegramBot`; Password: `****`; Tags: `Management`.
    - Click on the admin name in the table.
    - Click `Set Permission`. Make sure **Virtual Host** is set to `/`.
    - Repeat this for the other management users.
    - Delete the guest user and refresh RabbitMQ.
    - Log in as an admin and you will see the configuration panel.

5. Create an image:
    ```sh
    docker build -t web-server .
    ```

6. Create and run a container:
    ```sh
    docker run -d --name web-server-cont -p 6798:6798 web-server
    ```

---

### Project Structure

This project follows an MVC-inspired architecture. The entry point is **main.py**, and the core logic is organized within the **app** directory:

- **app/services/*** - Core services responsible for communication with other microservices;
- **app/routes/*** - Logic handling HTTP routes and request processing;
- **app/static/*** and **./app/templates/*** - Frontend assets and HTML templates;
- **app/utils/*** - Utility functions used across the project;
- **app/telegram_utils/*** - Helper functions to communicate with the Telegram service;
- **app/database_utils/*** - Helper functions to communicate with the database;
- **app/models/*** - Static classes used to organize and structure data for convenience;
- **app/__init__.py** - Initializes the Flask app and registers Blueprints for modular organization;
- **Dockerfile** and **requirements.txt** - Used to build and run the application in Docker containers;
- **tests/*** - Unit tests for this project.

---

### Dependencies

- Python 3.10.9 (later versions have a problem with hashlib dependencies)
- All Python modules are listed in **requirements.txt**.

---

### Contributing

Interested in improving the frontend? Contributions are very welcome! Feel free to open a pull request with your changes.

---

### License

MIT License - see the `LICENSE` file for details.

---

### Demo

If my server isn’t being used for something else, the project should be running [here](https://158.220.119.11:6798/). I created my own certificate for this project. Web browsers will warn you about this, and you will need to confirm to proceed to the page.

**[Rare Hashes Web Server - Demo](https://158.220.119.11:6798/)**