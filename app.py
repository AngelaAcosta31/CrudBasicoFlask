from flask.helpers import url_for
from forms import PersonaForm
from flask import Flask, render_template, request
from werkzeug.utils import redirect
from flask_migrate import Migrate
from database import db
from models import Persona


app = Flask(__name__)

#configuracion de la base de datos 
USER_DB = 'postgres'
PASS_DB = 'admin'
URL_DB = 'localhost'
NAME_DB = 'sap_flask_db'
#CADENA DE CONEXION A POSTGRESQL
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#inicialización del objeto db de sqlalchemy
db.init_app(app)

#configurar flask-migrate
migrate = Migrate()
migrate.init_app(app, db)

#configuracion flask-wtf
app.config['SECRET_KEY']='llave_secreta'


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def inicio():
    #listado de personas
    #personas = Persona.query.all()
    personas = Persona.query.order_by('id')
    total_personas = Persona.query.count()
    app.logger.debug(f'Listado Personas: {personas}')
    app.logger.debug(f'Total Personas: {total_personas}')
    return render_template('index.html', personas=personas, total_personas=total_personas)

@app.route('/ver/<int:id>')
def ver_detalle(id):
    #recuperamos la persona segun el id proporcionado
    #persona = Persona.query.get(id)
    persona = Persona.query.get_or_404(id)
    app.logger.debug(f'Ver persona: {persona}')
    return render_template('detalle.html', persona=persona)

@app.route('/agregar', methods=['GET', 'POST'])
def agregarPersona():
    persona = Persona()
    personaForm = PersonaForm(obj= persona)
    if request.method == 'POST':
        if personaForm.validate_on_submit():
            personaForm.populate_obj(persona)
            app.logger.debug(f'persona a insertar: {persona}')
            #insertamos el nuevo registro
            db.session.add(persona)
            db.session.commit()
            return redirect(url_for('inicio'))
    return render_template('agregar.html', forma=personaForm)




@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editarPersona(id):
    #recuperamos el objeto persona a editar
    persona = Persona.query.get_or_404(id)
    personaForma = PersonaForm(obj= persona)
    if request.method == 'POST':
        if personaForma.validate_on_submit():
            personaForma.populate_obj(persona)
            app.logger.debug(f'persona a actualizar: {persona}')
            #actualizamos el registro
            db.session.commit()
            return redirect(url_for('inicio'))
    return render_template('editar.html', forma=personaForma)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    persona = Persona.query.get_or_404(id)
    app.logger.debug(f'Persona a eliminar: {persona}')
    db.session.delete(persona)
    db.session.commit()
    return redirect(url_for('inicio'))