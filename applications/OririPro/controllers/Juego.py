pericia=0
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

@auth.requires_login()
def perfil():
    semestre=db(db.Semestre.IdPartida==session.partida).select().last()
    if semestre:
        session.n=semestre.Numero
    pericia=db(db.NivelPericia.IdPartida==session.partida).select()
    return locals()

@auth.requires_login()
def oferta():
    if not session.n:
        db.Semestre.insert(IdPartida=session.partida,Numero=1)
    else:
        semestre=db(db.Semestre.IdPartida==session.partida).select().last()
        db.Semestre.insert(IdPartida=session.partida,Numero=semestre.Numero+1)
    semestre=db(db.Semestre.IdPartida==session.partida).select().last()
    ofertada=[]
    session.semestre=semestre.Numero
    materias=db(db.Materia).select(orderby=db.Materia.Ciclo)
    for materia in materias:
        ofertada.append(curso(materia.id))
    return locals()

import random
def curso(materia):
    ofertada=db(db.Materia_Docente.IdMateria==materia).select(limitby=(0, 1), orderby='<random>')
    return ofertada

def addMateria():
    IdMD=request.get_vars
    semestre=db(db.Semestre.IdPartida==session.partida).select().last()
    db.Calificacion.insert(IdMateriaDocente=IdMD.id,Calificacion=10,IdSemestre=semestre.id,Oportunidad=GetOportunidad(IdMD.id),IdPartida=session.partida)
    return locals()

def GetOportunidad(IdMD):
    foo=0
    semestres=db(db.Semestre.IdPartida==session.partida).select()
    Materia=db(db.Materia_Docente.id==IdMD).select().last()
    print Materia.IdMateria
    for semestre in semestres:
        Temp=db(db.Calificacion.IdSemestre==semestre.id).select()
        for calificacion in Temp:
            if calificacion.IdMateriaDocente.IdMateria==Materia.IdMateria:
                foo=foo+1
    if not foo:
     return 1
    else:
     return foo

@auth.requires_login()
def ronda():
    semestre=db((db.Semestre.IdPartida==session.partida)&(db.Semestre.Numero==session.semestre)).select().last
    materias=db(db.Calificacion.IdSemestre==semestre.id).select()
    return locals()

@auth.requires_login()
def carga():
    semestre=db(db.Semestre.IdPartida==session.partida).select().last()
    carga=db(db.Calificacion.IdSemestre==semestre.id).select()
    return locals()

def SetCalificacion():
    var=request.get_vars
    calf=int(var.id)
    time=int(var.time)#Tiempo Total de estudio
    tiempo=var.tiempo
    calf=calf-1
    dbCal=db(db.Calificacion.id==calf).select().first()
    Creditos=dbCal.IdMateriaDocente.IdMateria.Creditos #Creditos
    Promedio=dbCal.IdMateriaDocente.IdMateria.Media #Promedio
    DifMD=dbCal.IdMateriaDocente.IdDocente.Dificultad#Dificultad Docente
    print DifMD
    V=dbCal.IdMateriaDocente.IdMateria.Varianza
    if tiempo=="plus10":#T= tiempo dedicado a esa materia
        T=10
    elif tiempo=="plus8":
        T=8
    elif tiempo=="plus6":
        T=6
    elif tiempo=="plus4":
        T=4
    rand=random.uniform(-1*(V),V)
    print "rela"
    calf=5*(T/float(Creditos))+0.01*MediaPericia(dbCal.IdMateriaDocente.IdMateria)+0.2*(10-DifMD)+0.2*Promedio+rand#metodo de regresion lineal multiple
    pericia=0
    print calf
    calf=int(calf)
    return calf

def MediaPericia(IDMat):
    global pericia
    Materia=db(db.Materia.id==IDMat).select().first()
    Ciclo=Materia.Ciclo
    TempPericia=db((db.NivelPericia.IdPartida==session.partida)&(db.NivelPericia.IdAcademia==Materia.IdAcademia))
    if Ciclo=="1":
        pericia=100
    elif Ciclo=="2":
        total=len(db((db.Materia.Ciclo=="1")&(db.Materia.IdAcademia==Materia.IdAcademia)))
        pericia=TempPericia/total
    elif Ciclo=="3":
        total=len(db((db.Materia.Ciclo=="1")&(db.Materia.Ciclo=="2")&(db.Materia.IdAcademia==Materia.IdAcademia)))
        pericia=TempPericia/total
    elif Ciclo=="3-4":
        total=len(db((db.Materia.Ciclo=="1")&(db.Materia.Ciclo=="2")&(db.Materia.IdAcademia==Materia.IdAcademia)))
        pericia=TempPericia/total
    elif Ciclo=="4":
        total=len(db((db.Materia.Ciclo=="1")&(db.Materia.Ciclo=="2")&(db.Materia.Ciclo=="3")&(db.Materia.IdAcademia==Materia.IdAcademia)))
        pericia=TempPericia/total
    return pericia
