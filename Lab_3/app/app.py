from flask import Flask, render_template, request, session, redirect, url_for, flash

from flask_login import LoginManager, UserMixin , login_user, logout_user, login_required

login_manager = LoginManager()

app = Flask(__name__)
application = app

login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = ' для доступа к данной странице необходима авторизация'
login_manager.login_message_category = 'warning'


app.config['SECRET_KEY'] = b'\xd4\x9c6\xe5\xc7\xa5V\xbb\xbbd\xab\x8b3\xc2"d'



def get_users():
    return [{'user_id' : '1', 'login' : 'user' , 'password' : '1'}]


class User(UserMixin):
    def __init__(self, user_id, login, password):
        super().__init__()
        self.id = user_id
        self.login = login
        self.password = password



@login_manager.user_loader
def load_user(user_id):
    for user in get_users():
        if user['user_id'] == user_id:
            return User(**user)
    return None        




@app.route('/')
def index():
    return render_template('index.html', delete_footer=True)


@app.route('/visits')
def visits():
    if session.get('visits'): 
        session['visits']+=1
    else:
        session['visits'] = 1


    return render_template('visits.html')


@app.route('/login' , methods=['GET','POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me') == 'on'
        if login and password:
            for user in get_users():
                if user["login"] == login and user['password'] == password:
                    user_object = User(**user)
                    login_user(user_object, remember=remember_me)
                    
                    flash('вы успешно вошли','success')

                    next = request.args.get('next')

                    return redirect (next or url_for('index'))   

        flash('ВВедены не верные логин или пароль','danger')    

    return render_template('login.html')



@app.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('index'))


@app.route('/secret_page')
@login_required
def secret_page():
    return render_template('secret_page.html')



if __name__ == "__main__":
    app.run()
