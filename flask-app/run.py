
if __name__ == '__main__':
    from app import app
    app.run(host="192.168.2.232",port=443, ssl_context='adhoc')

