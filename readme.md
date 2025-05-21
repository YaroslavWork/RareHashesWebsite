**Run project (in linux)**

1. Install docker

    (In Arch)
    ```
    pacman -S docker
    ```
    or
    ```
    yay -S docker 
    ```

2. Run docker

    ``` 
    sudo systemctl start docker
    ```

    To run docker everytime when you launch linux type this command:
    ```
    sudo systemctl enable docker
    ```

3. Create ***.env*** file

    This file contains all necessary private information. Your ***.env*** must contain:

    ```
    DATABASE_IP_AND_PORT=127.0.0.1:25000
    TELEGRAM_BOT_IP_AND_PORT=127.0.0.1:33000
    DATABASE_LOGIN=databse_login
    DATABASE_PASSWORD=veryStrongPassword
    HOST=127.0.0.1:5000
    DEBUG=False
    PEM_PASS=veryStrongPassword
    ```

    This configuration file contains:
    - ```DATABASE_IP_AND_PORT``` - connection to mongoDB database. This database must have collection 'hashes'.
    - ```TELEGRAM_BOT_IP_AND_PORT``` - my other project to connects telegram bot and send notifications in case if users need.
    - ```DATABASE_LOGIN``` - login to mongoDB
    - ```DATABASE_PASSWORD``` - password to mongoDB
    - ```HOST``` - site domain
    - ```DEBUG``` - debugging for developers
    - ```PEM_PASS``` - https conection password

