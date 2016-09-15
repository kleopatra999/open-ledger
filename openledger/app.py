from flask import Flask, render_template

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

@app.route("/")
def index():
    from handlers.handler_500px import photos
    results = photos(search='greyhound')
    return render_template('index.html', results=results)

if __name__ == '__main__':
    # Run me as 'python -m app' to avoid path/import problems
    app.run(debug=True)