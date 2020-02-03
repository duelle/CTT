#!/usr/bin/env python3
import connexion

from swagger_server import encoder

import radonCTT.controller

app = connexion.App(__name__, specification_dir='./swagger/')
app.app.json_encoder = encoder.JSONEncoder
app.add_api('swagger.yaml', arguments={'title': 'Radon CTT API'}, pythonic_params=True)
application = app.app

def main():
    radonCTT.controller.run()
    app.run(port=20000)

if __name__ == '__main__':
    main()