from flask import Flask, render_template, url_for
app = Flask(__name__)

posts = [
    {
        'author': 'Leo Igane',
        'title': 'Minute Pitch 1',
        'content': 'First pitch content',
        'date_posted': 'April 20, 20018'
    },
    {
    'author': 'Njeri Igane',
    'title': 'Minute Pitch 2',
    'content': 'Second pitch content',
    'date_posted': 'April 21, 20018'
    }
    ]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts = posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')


if __name__ == '__main__':
    app.run(debug=True)
