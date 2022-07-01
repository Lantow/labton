from labton_ui import redact_flask_annotater_page

if __name__ == '__main__':
    app = redact_flask_annotater_page.return_app()
    app.run(host='0.0.0.0', port=8080, debug='True')