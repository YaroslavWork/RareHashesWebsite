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

### Installation

Click **[Here](https://app.notion.com/p/Linux-Installation-Process-4157e2027a0d80ca986cc3197471b731?t=4157e2027a0d80ac897000a9d6b39560)** to see installation process for linux

To deal with SSL certificates create **rareHashes.crt** and **rareHashes.key** with, for example, `openssl` and put them in the **./ssl** directory.

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
- **requirements-dev.txt** - Development dependencies (includes **requirements.txt** and adds `pytest`);
- **run.sh** - Local development runner (Hypercorn) reading `HOST` from **.env**;
- **tests/*** - Unit tests for this project.

---

### Dependencies

- Python 3.10.9 (later versions have a problem with hashlib dependencies)
- All runtime Python modules are listed in **requirements.txt**. Docker images install only this file.
- Development and testing modules (with `pytest`) are listed in **requirements-dev.txt**, which includes **requirements.txt**.

For development:
```sh
python3 -m venv venv
venv/bin/pip install -r requirements-dev.txt
venv/bin/python -m pytest -v
```

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