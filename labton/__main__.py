from labton.labton_ui import flask_annotater_page

if __name__ == '__main__':
    app = flask_annotater_page.return_app()
    app.run(host='0.0.0.0', port=8080, debug='True')