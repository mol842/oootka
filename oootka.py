from flask import Flask, redirect, url_for, request, render_template
import random
from captcha.image import ImageCaptcha
from rooms import get_room
from datetime import datetime
import os

app = Flask(__name__, static_folder="static")

app.static_folder = 'static'
@app.route('/', methods=['POST', 'GET'])
def feedback():
    n = 0
    return render_template("feedback.html")


@app.route('/verify', methods=['POST', 'GET'])
def start():
    n = 0
    return render_template("oootka.html", leftmost=str(n), remaining=10)

@app.route('/success/<name>/<n>/<remaining>')
def success(name, n, remaining):
    remaining = int(remaining)
    n_int = int(n) + 100
    nn = str(n_int)
    return render_template("oootka.html", leftmost=nn, remaining=remaining)

@app.route('/findme/<remaining>')
def hiding(remaining):
    remaining = int(remaining)
    left = random.randint(-1000, 3000)
    down = random.randint(0, 3000)
    return render_template("runaway.html", leftmost=str(left), downmost=str(down), remaining=remaining)

@app.route('/failed/')
def failed():
    return render_template("FAILED.html", remaining=10)

@app.route('/conditions/<remaining>')
def conditions(remaining):
    return render_template("conditions.html", remaining=remaining)



@app.route('/captcha/<remaining>')
def captcha(remaining):
    remaining = int(remaining)
    image = ImageCaptcha(width = 800, height = 200)
    capcha_options = ["I LOVE VERIFICATION", "LOVE VERIFYING", "I PLEDGE ALLEGIANCE TO OOTKA","I LOVE THIS UNIVERSITY", "I LOVE LOGGING IN"]
    captcha_text = random.choice(capcha_options)
    data = image.generate(captcha_text)
    image.write(captcha_text, './static/images/CAPTCHA.png')

    return render_template("capatacha.html", remaining=remaining)

@app.route('/checkcapatcha', methods=['POST', 'GET'])
def check():
    remaining = int(request.form['remaining'])
    if request.method == 'POST':
        submission = request.form['nm']
        capcha_options = ["test", "I LOVE VERIFICATION", "LOVE VERIFYING", "I PLEDGE ALLEGIANCE TO OOTKA","I LOVE THIS UNIVERSITY", "I LOVE LOGGING IN"]

        if submission not in capcha_options:
            return redirect(url_for('failed'))
        else:
            return redirect(url_for('login', remaining=remaining))
        #return redirect(url_for('success', name=user, n=nn))
    else:
        # user = request.args.get('nm')
        # nn = request.args.get('count')
        return redirect(url_for('failed'))

        #return redirect(url_for('success', name=user, n=nn))

    image = ImageCaptcha(width = 400, height = 90)
    captcha_text = "I LOVE VERIFICATION"
    data = image.generate(captcha_text)
    image.write(captcha_text, './static/images/CAPTCHA.png')

    return render_template("capatacha.html")


@app.route('/login/<remaining>', methods=['POST', 'GET'])
def login(remaining):
    options = ['hiding', 'captcha', 'room', 'conditions', 'bouncy']
    chosen = random.choice(options)
    if request.method == 'POST':
        num_remaining = int(request.form['remaining']) - 1
        if num_remaining == 0:
            return redirect(url_for('verified'))
        return redirect(url_for(chosen, remaining=num_remaining))
    else:
        #num_remaining = int(request.args.get('remaining')) - 1
        num_remaining = int(remaining)
        if num_remaining == 0:
            return redirect(url_for('verified'))
        # user = request.args.get('nm')
        # nn = request.args.get('count')
        return redirect(url_for(chosen, remaining=num_remaining))

    if request.method == 'POST':
        # user = request.form['nm']
        # nn = request.form['count']
        return redirect(url_for(chosen))
        #return redirect(url_for('success', name=user, n=nn))

        #return redirect(url_for('success', name=user, n=nn))

@app.route('/verified')
def verified():
    return render_template("success.html")


@app.route('/room/<remaining>')
def room(remaining):
    num, name = get_room(0)
    return render_template("dropdown.html", room_num=num, room_name=name, remaining=remaining)

@app.route('/bouncy/<remaining>')
def bouncy(remaining):
    return render_template("bouncy.html", remaining=remaining)


@app.route('/checkroom/<remaining>', methods=['POST', 'GET'])
def checkroom(remaining):
    if request.method == 'POST':
        num = request.form['building_num']
        name = request.form['building_name']
        name1, num1 = get_room(num)
        if name != name1:
            return redirect(url_for('failed'))
        else:
            return redirect(url_for('login', remaining=remaining))
        #return redirect(url_for('success', name=user, n=nn))
    else:
        # user = request.args.get('nm')
        # nn = request.args.get('count')
        return redirect(url_for('failed'))


@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    email = request.form['email']
    feedback = request.form['feedback']
    
    # Create a filename with the current date and time
    now = datetime.now()
    filename = now.strftime("%Y-%m-%d_%H-%M-%S") + '.txt'
    filepath = os.path.join('feedback', filename)
    
    # Ensure the feedback directory exists
    os.makedirs('feedback', exist_ok=True)
    
    # Write the feedback to the file
    with open(filepath, 'w') as file:
        file.write(f"Name: {name}\n")
        file.write(f"Email: {email}\n")
        file.write(f"Feedback:\n{feedback}\n")
    
    return redirect(url_for('start'))





if __name__ == '__main__':
    app.run(debug=True)


def get_random_name():
    first_names = ["copter", "stopper", "cop car", "optus", "octo", "otter", "lotto"]
    second_names = ["verify", "barely fly", "family guy", "want to cry", "gonna die", "spotify", "side of fries", "barely alive"]


