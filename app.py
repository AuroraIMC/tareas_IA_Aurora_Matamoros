from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tareas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    estado = db.Column(db.String(20), default='pendiente')  
    fecha_vencimiento = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Tarea {self.id}: {self.titulo}>'


# Crear la base de datos 
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    tareas = Tarea.query.all()
    return render_template('index.html', tareas=tareas)
#esto me ccrea una tarea
@app.route('/agregar', methods=['POST'])
def agregar():
    titulo = request.form['titulo']
    descripcion = request.form.get('descripcion')
    fecha_str = request.form.get('fecha_vencimiento')

    fecha_vencimiento = None
    if fecha_str:
        fecha_vencimiento = datetime.strptime(fecha_str, '%Y-%m-%d')

    nueva_tarea = Tarea(
        titulo=titulo,
        descripcion=descripcion,
        fecha_vencimiento=fecha_vencimiento
    )
    db.session.add(nueva_tarea)
    db.session.commit()
    return redirect(url_for('index'))
#esto me edita una tarea
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    tarea = Tarea.query.get_or_404(id)

    if request.method == 'POST':
        tarea.titulo = request.form['titulo']
        tarea.descripcion = request.form.get('descripcion')
        tarea.estado = request.form['estado']
        fecha_str = request.form.get('fecha_vencimiento')
        tarea.fecha_vencimiento = datetime.strptime(fecha_str, '%Y-%m-%d') if fecha_str else None

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('editar.html', tarea=tarea)
#marca completado 
@app.route('/marcar_completada/<int:id>')
def marcar_completada(id):
    tarea = Tarea.query.get_or_404(id)
    tarea.estado = 'completada'
    db.session.commit()
    return redirect(url_for('index'))
#marca proceso
@app.route('/marcar_en_proceso/<int:id>')
def marcar_en_proceso(id):
    tarea = Tarea.query.get_or_404(id)
    tarea.estado = 'en proceso'
    db.session.commit()
    return redirect(url_for('index'))


#esto me elimina una tarea
@app.route('/eliminar/<int:id>')
def eliminar(id):
    tarea = Tarea.query.get_or_404(id)
    db.session.delete(tarea)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
