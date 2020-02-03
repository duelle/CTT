## This is the custom code directory
All handlers created automatically by swagger will call an associated function, which is defined here. Therefore, when the server must be regenerated, all we have to do is insert the calls to the methods defined in this directory.

### In order to get RadonCTT runing after regenerating the server stub you must:
    - Have all controllers in swagger_server call their respective handler in radonCTT/handlers
    - Add "query = db_session.query_property()" to swagger_server/base_model class
    - If you changed models, modify the mappings in radonCTT/database/mapper accordingly
    
Additionally, you must change the code in __main__ to:

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


Test Repository for test creation:
    target: https://github.com/xlab-si/xopera-examples.git