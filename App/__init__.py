from flask import Flask

app = Flask(__name__)
app.config.update(SERVER_NAME='localhost:5000')

lookup = {
    'hello': 'hello.jpg',
    'garland-dance': 'garland-dance.gif',
}


@app.route("/", subdomain='<query>')
def subdomains(query):
    try:
        filename = lookup[query]
    except LookupError:
        filename = 'hello.jpg'

    return app.send_static_file(filename)

if __name__ == "__main__":
    app.run(debug=True)
