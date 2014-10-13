# coding: utf8
# intente algo como
@auth.requires_login()
def index():
    car=request.vars['c']
    carrera=db(db.Carrera.Titulo==car).select().first()
    db.Partida.insert(IdUsuario=auth.user.id,IdCarrera=carrera.id)
    Partida=db(db.Partida.IdUsuario==auth.user.id).select().last()
    session.partida=Partida.id
    Academias=db(db.Academia.IdCarrera==carrera.id).select()
    for academia in Academias:
        db.NivelPericia.insert(IdPartida=Partida.id,IdAcademia=academia.id)
    redirect(URL('perfil'))
    return locals()

def perfil():
    print session.partida
    semestre=db(db.Semestre.IdPartida==session.partida).select().last()
    if not semestre:
        semestre="No se ha iniciado algun semestre"
    pericia=db(db.NivelPericia.IdPartida==session.partida).select()
    return locals()

def oferta():
    ofertada=[]
    materias=db(db.Materia).select(orderby=db.Materia.Ciclo)
    for materia in materias:
        ofertada.append(curso(materia.id))
    print ofertada
    return locals()

import random
def curso(materia):
    ofertada=db(db.Materia_Docente.IdMateria==materia).select(limitby=(0, 1), orderby='<random>')
    return ofertada
