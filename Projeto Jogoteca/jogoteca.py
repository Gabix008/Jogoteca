from flask import Flask
from flask import render_template, request, redirect, session,flash, url_for
class Jogo: 
    def __init__(self, nome, categoria, console):
        self.nome=nome
        self.categoria=categoria
        self.console=console

jogo1 = Jogo('Tetris','Puzzle','Android')
jogo2 = Jogo('God of war','Acao','Ps2')
jogo3 = Jogo('Mortal combat','Luta','Ps2')
lista = [jogo1, jogo2, jogo3]

class Usuario:
    def __init__(self, nome, user, senha):
        self.nome=nome
        self.user=user
        self.senha=senha
usuario1 = Usuario('Gabi', 'gabix', 'abc123')
usuario2 = Usuario('Julia', 'ju123', 'ju123')
usuario3 = Usuario('Paula', 'Pp12', 'p123')
usuarios = {usuario1.user:usuario1, usuario2.user:usuario2, usuario3.user:usuario3}

app = Flask(__name__)
app.secret_key = 'abc'

@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos = lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima = url_for('novo')))
    
    return render_template('novo.html', titulo='Novo jogo')

@app.route('/criar', methods= ['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome,categoria,console)
    lista.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods= ['POST',])
def autenticar():

    if request.form['usuario'] in usuarios:
        usuario= usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.user
            flash(request.form['usuario'] + ' logado com sucesso!')
            proximaPagina = request.form['proxima']

            if proximaPagina!=None:
                return redirect(url_for('novo'))
            else:
                return redirect(url_for('index'))
            
        else:
            flash('Usuario nao logado')
            return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Bye bye')
    return redirect(url_for('login'))

app.run(debug = True)