
if __name__ == '__main__':
    from app import app
    app.run(port=443, ssl_context='adhoc')

