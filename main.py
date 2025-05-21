import os
import ssl

from app import create_app

app = create_app()

if __name__ == '__main__':
    IP, PORT = os.getenv('HOST').split(':')
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain('./ssl/rareHashes.crt', './ssl/rareHashes.key', password=app.config['PEM_PASS'])
    app.run(host=IP,
            port=int(PORT),
            debug=app.config['DEBUG'],
            ssl_context=ssl_context)