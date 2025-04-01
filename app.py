from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail 
from itsdangerous import URLSafeTimedSerializer as Serealizer 

app = Flask(__name__)
bcrypt = Bcrypt(app)

#Clave secreta para sesiones 
app.secret_key = "saulxd"

#Configuracion de MongoDB Atlas
client = MongoClient("mongodb+srv://saulazyu:MongoDB@cluster0.eakmhvq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['Vocacitonal_Test']
collecition = db['Users']

@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Si viene un email no vacío, se asume registro
        if 'email' in request.form and request.form['email'].strip() != "":
            # REGISTRO
            user = request.form['user']
            email = request.form['email']
            password = request.form['password']
            
            # Verificar si el usuario ya existe (por nombre o email)
            if collecition.find_one({'user': user}):
                flash("El nombre de usuario ya está registrado. Intentalo de nuevo", "error")
                return render_template('Login.html')
            if collecition.find_one({'email': email}):
                flash("El correo electrónico ya está registrado. Intentalo de nuevo", "error")
                return render_template('Login.html')
            
            # Hashear la contraseña y guardar el usuario
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            collecition.insert_one({
                'user': user,
                'email': email,
                'password': hashed_password
            })
            
            flash("Registro exitoso. Ahora inicia sesión.", "success")
            return redirect(url_for('login'))
        else:
            # LOGIN
            user = request.form['user']
            password = request.form['password']
            
            userBD = collecition.find_one({'user': user})
            if userBD and bcrypt.check_password_hash(userBD['password'], password):
                session['user'] = user
                return redirect(url_for('pagina_principal'))
            else:
                flash("Usuario o contraseña incorrectos. Intentalo de nuevo", "error")
                return render_template('Login.html')
    return render_template('Login.html')


@app.route('/pagina_principal')
def pagina_principal():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('Index.html', user=session['user'])

@app.route('/mi_perfil')
def mi_perfil():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    user_data = collecition.find_one({'user': user})
    return render_template('mi_perfil.html', user=user_data['user'], email=user_data['email'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True) 




