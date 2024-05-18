from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__, static_folder="static")

app.static_folder = 'static'

@app.route('/')
def start():
    n = 0
    return render_template("oootka.html", leftmost=str(n))

@app.route('/success/<name>/<n>/')
def success(name, n):
    n_int = int(n) + 100
    nn = str(n_int)
    return render_template("oootka.html", leftmost=nn)



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        nn = request.form['count']
        ##nn = "1"
        return redirect(url_for('success', name=user, n=nn))
    else:
        user = request.args.get('nm')
        nn = request.args.get('count')
        return redirect(url_for('success', name=user, n=nn))


if __name__ == '__main__':
    app.run(debug=True)
