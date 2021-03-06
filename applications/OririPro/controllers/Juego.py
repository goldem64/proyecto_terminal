pericia=0
TerceraOportunidad=0
session.ma=[]
cont=0
# coding: utf8
# intente algo como
#TODO: Agregar parciales y sacar promedio de ellas
# Agregar encuesta y ponderar puntos por contestar
# Agregar dinero y canje por puntos de encuestas

@auth.requires_login()
def index():##TODO leer partidas pues este solo crea nuevas partidas enbelleser
    car=request.vars['c']
    if not car:
        redirect(URL('default','index'))
    else:
        carrera=db(db.Carrera.Titulo==car).select().first()
        Partida=db.Partida.insert(IdUsuario=auth.user.id,IdCarrera=carrera.id,BajasTemporales=0,Dinero=2500,Creditos=0,Estado=1,SoftSkills=100,VidaFamiliar=100,VidaSocial=100,VidaLaboral=100)
        #Partida=db(db.Partida.IdUsuario==auth.user.id).select().last()
        session.partida=Partida
        session.semestre=0
        Academias=db(db.Academia.IdCarrera==carrera.id).select()
        for academia in Academias:
            db.NivelPericia.insert(IdPartida=Partida.id,IdAcademia=academia.id,Pericia=10)
        redirect(URL('perfil'))
    return locals()

@auth.requires_login()
def perfil():##Reglas de terminacion de juego en funcion GameOver
    if not session.partida:
        redirect(URL('default','index'))
    else:
        pericia=db(db.NivelPericia.IdPartida==session.partida).select()
        partida=db(db.Partida.id==session.partida).select().first()
        semestre=db(db.Semestre.IdPartida==session.partida).select().last()
        db(db.Partida.id==session.partida).update(Estado=Estado(semestre))
        partida=db(db.Partida.id==session.partida).select().first()
        if semestre:
                session.semestre=semestre.Numero#selecciona el ultimo semestre
    return locals()

def Estado(semestre):
    reprobadas=db((db.Calificacion.IdPartida==session.partida) & (db.Calificacion.Aprobada==2)).select()
    if reprobadas:
        estado=2
    else:
        estado=1
    if semestre:
        CursadasUltimoSemestre=db(db.Calificacion.IdSemestre==semestre.id).select()
        reprobadasUltimoSemestre=db((db.Calificacion.IdSemestre==semestre.id) & (db.Calificacion.Aprobada==2)).select()
        limite=len(CursadasUltimoSemestre)/2
        reprobadas=len(reprobadasUltimoSemestre)
        if reprobadas>=limite:
            estado=3
    if GameOver():
        estado=4
    session.estado=estado
    return estado

def savetime():#guarda el tiempo que se le dedica al estudio
        if not session.partida:
            redirect(URL('default','index'))
        else:
            x=int(request.vars['time'])
            y=int(request.vars['trabajo'])
            ts=int(request.vars['social'])
            tf=int(request.vars['familia'])
            session.time=int((x/100.00)*168)#porcentaje pasado a horas de estudio
            session.trabajo=y
            session.familia=tf
            session.social=ts
            redirect=URL('ofertada')
            session.parcial=1;
        return 1

@auth.requires_login()
def oferta():
    if not session.partida:
        redirect(URL('default','index'))
    else:
        if not session.semestre:
            db.Semestre.insert(IdPartida=session.partida,Numero=1)#si no existe semestre inicializa en 1
        else:
            semestre=db(db.Semestre.IdPartida==session.partida).select().last()#selecciona el objeto del ultimo semestre
            db.Semestre.insert(IdPartida=session.partida,Numero=semestre.Numero+1)# Y agrega un semestre mas
        semestre=db(db.Semestre.IdPartida==session.partida).select().last()
        ofertada=[None]#Lista de oferta de materias bacia
        session.semestre=semestre.Numero#guarda en una variable de session el semestre
        materias=db(db.Materia).select(orderby=db.Materia.Ciclo)#Selecciona todas las materias ordenadas por siclo TODO:Quitar las aprobadas
        aprobadas=db((db.Calificacion.IdPartida==session.partida)&(db.Calificacion.Aprobada==1)).select()
        for materia in materias:
            ofertada.append(curso(materia.id,aprobadas))
        ofertada=list(set(ofertada))
        del ofertada[ofertada.index(None)]
    return locals()

import random
def curso(materia,pasadas):##colocar que materias se han pasado y su oportunidad
    if pasadas:
        for aprobada in pasadas:
            if aprobada.IdMateriaDocente.IdMateria==materia:
                return
            else:
                ofertada=db(db.Materia_Docente.IdMateria==materia).select(limitby=(0, 1), orderby='<random>')#selecciona de manera aleatoria la oferta segun el docente
    else:
        ofertada=db(db.Materia_Docente.IdMateria==materia).select(limitby=(0, 1), orderby='<random>')
    return ofertada

def addMateria():##ingresa por semestre las materias
    IdMD=request.get_vars
    semestre=db(db.Semestre.IdPartida==session.partida).select().last()
    m=db.Calificacion.insert(IdMateriaDocente=IdMD.id,Calificacion=10,IdSemestre=semestre.id,Oportunidad=GetOportunidad(IdMD.id),IdPartida=session.partida)
    db.Parcial.insert(IdCalificacion=m.id,p1=0,p2=0,p3=0,promedio=0)
    return locals()

def GetOportunidad(IdMD):## Optiene oportunidad mas 1
    foo=0
    semestres=db(db.Semestre.IdPartida==session.partida).select()
    Materia=db(db.Materia_Docente.id==IdMD).select().last()
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
def ronda():#selecciona las materias cagadas del semestre en session
    if not session.partida:
        redirect(URL('default','index'))
    else:
        semestre=db((db.Semestre.IdPartida==session.partida)&(db.Semestre.Numero==session.semestre)).select().last
        materias=db(db.Calificacion.IdSemestre==semestre.id).select()
    return locals()

@auth.requires_login()
def carga():
    if not session.partida:
        redirect(URL('default','index'))
    else:
        semestre=db(db.Semestre.IdPartida==session.partida).select().last()
        carga=db(db.Calificacion.IdSemestre==semestre.id).select()
        for i in carga:
            session.ma.append(db(db.Parcial.IdCalificacion==i.id).select().first())
        m=0
        if len(carga)<3:
            db(db.Partida.id==session.partida).update(BajasTemporales=GetBajasTemporales()+1)
            m='Baja temporal'
        partida=db(db.Partida.id==session.partida).select().first()
        if partida.Dinero<2300 and session.parcial==1:
            db(db.Partida.id==session.partida).update(BajasTemporales=GetBajasTemporales()+1)
            m='Baja temporal:Sin fondos para cursar el siguiente semestre'
        elif session.parcial==1:
            db(db.Partida.id==session.partida).update(Dinero=partida.Dinero-2300)
    return locals()

def GetBajasTemporales():#Regresa las bajas temporales
    Partida=db(db.Partida.id==session.partida).select().first()
    return Partida.BajasTemporales

def SetCalificacion():#regresa la calificacion dependiente de NivelExigenciaDoc,DifMateria,Varianza,Pericia,Tiempo,Creditos
    #time tiempo total tiempo tiempo de 1 materia
    var=request.get_vars
    idcalf=int(var.id)
    time=int(var.time)#Tiempo Total de estudio TODO: MENOR QUE 0 return message
    tiempo=var.tiempo
    #calf=calf-1
    dbCal=db(db.Calificacion.id==idcalf).select().first()
    partida=db(db.Partida.id==session.partida).select().first()
    Creditos=dbCal.IdMateriaDocente.IdMateria.Creditos #Creditos
    Promedio=dbCal.IdMateriaDocente.IdMateria.Media #Promedio de materia
    DifMD=dbCal.IdMateriaDocente.IdDocente.Dificultad#Dificultad Docente
    V=dbCal.IdMateriaDocente.IdMateria.Varianza
    IDMateria=dbCal.IdMateriaDocente.IdMateria
    print IDMateria
    if tiempo=="plus10":#T= tiempo dedicado a esa materia
        T=10
        time=time-10
    elif tiempo=="plus8":
        T=8
        time=time-8
    elif tiempo=="plus6":
        T=6
        time=time-6
    elif tiempo=="plus4":
        T=4
        time=time-4
    rand=random.uniform(-1*(V),V)
    calf=4*(T/float(Creditos))+0.01*MediaPericia(IDMateria)+0.3*(10-DifMD)+0.2*Promedio+rand#metodo de regresion lineal multiple
    VS=CalcularVidaSocial(partida.VidaSocial,session.social)
    VF=CalcularVidaFamiliar(partida.VidaFamiliar,session.familia)
    VL=VidaLaboral(partida.VidaLaboral,session.trabajo)
    SS=CalcularSoftSkills(VS,VF,VL)
    pericia=CalcularPericia(DifMD,Promedio,IDMateria,calf,SS)#calcular pericia TODO SS Softskills
    calf=int(round(calf))
    if calf >10:
        calf=10
    promedio=GuardaParcial(idcalf,calf)
    return response.json([{'time':time},{'calf':calf},{'promedio':int(promedio)}])

def GuardaParcial(idcalf,cal):
    if session.parcial==2:
        promedio=cal
        db(db.Parcial.IdCalificacion==idcalf).update(p1=cal,promedio=cal)
    elif session.parcial==3:
        parcial=db(db.Parcial.IdCalificacion==idcalf).select().first()
        promedio=(cal+parcial.p1)/2.00
        db(db.Parcial.IdCalificacion==idcalf).update(p2=cal,promedio=promedio)
    elif session.parcial==4:
         parcial=db(db.Parcial.IdCalificacion==idcalf).select().first()
         promedio=(cal+parcial.p1+parcial.p2)/3.00
         db(db.Parcial.IdCalificacion==idcalf).update(p3=cal,promedio=promedio)
    return promedio

def FinalizaSemestre():
    semestre=db(db.Semestre.IdPartida==session.partida).select().last()
    carga=db(db.Calificacion.IdSemestre==semestre.id).select()
    for materia in carga:
        final=db(db.Parcial.IdCalificacion==materia.id).select().first()
        db(db.Calificacion.id==materia.id).update(Calificacion=final.promedio)
        if final.promedio>6:
            db(db.Calificacion.id==materia.id).update(Aprobada=1)#Estado 1 indica aprobada estado 2 indica reprobada
        else:
            db(db.Calificacion.id==materia.id).update(Aprobada=2)
        Mat=db(db.Materia_Docente.id==materia.IdMateriaDocente).select().first()
        Creditos=db(db.Materia.id==Mat.IdMateria).select().first()## obtiene los creditos de la materia
        Acumulado=db(db.Partida.id==session.partida).select().first()
        TCreditos=Creditos.Creditos+Acumulado.Creditos
        db(db.Partida.id==session.partida).update(Creditos=TCreditos)
    CalculaDinero()
    redirect(URL('perfil'))
    return locals()

def CalculaDinero():
    partida=db(db.Partida.id==session.partida).select().first()
    Din=partida.Dinero+session.trabajo*100
    db(db.Partida.id==session.partida).update(Dinero=Din)
    return True


def CalcularPericia(DifMD,Promedio,IdMateria,cal,SS):#en funcion de exigenciaMaestro
    pericia=(0.2*(1+DifMD)+0.2*(10-Promedio)+0.02*MediaPericia(IdMateria)+0.3*cal+0.1*SS)*10
    return pericia

import math
def CalcularVidaSocial(VS,TS):#en funcion de TiempoSocial,VidaSocial y un random
    VSocial=int(100*(1-math.exp(-1*(int(VS/7)+int(TS/2)))))# apartir de int(VS/7)+int(TS/2)=25 da 100
    return VSocial

def CalcularVidaFamiliar(VF,TF):#en funcion de TiempoFamiliar,VidaFamiliar y un random
    VFamiliar=(random.uniform(-1*(4),4))*10+(VF+TF)/2
    return VFamiliar

def VidaLaboral(VL,TL):#depende de VidaLaboral,TiempoLaboral
    VLaboral=(random.uniform(-1*(1),1))*10+(VL+TL)/2
    return VLaboral

def CalcularSoftSkills(VS,VF,VL):#En funcion de Vida social,Vida Familiar,VidaLaboral.
    SS=int((VS+VF+VL)/3.00)
    return SS

def MediaPericia(IDMat):##Obtiene la media para cursar cierta materia en cierto ciclo
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

def GameOver():## Verifica si el juego se ha terminado
    semestre=db((db.Semestre.IdPartida==session.partida)&(db.Semestre.Numero==session.semestre)).select().last()
    if session.semestre:
        TerceraOportuniad=db((db.Calificacion.IdSemestre==semestre.id)&(db.Calificacion.Oportunidad>=3)&(db.Calificacion.Calificacion<7))
        if TerceraOportunidad:
            print "por tercera"
            return True
    Partida=db(db.Partida.id==session.partida).select().first()
    if session.semestre > 16:
        print session.semestre
        return True
    elif Partida.BajasTemporales >=3:
        print "por baja temporal"
        return True
    else:
        return False

def BajaTemporal():## TODO BAJA TEMPORAL ESTA ES COPIA DE SET TIME
    if not session.partida:
        redirect(URL('default','index'))
    else:
        if not session.semestre:
            db.Semestre.insert(IdPartida=session.partida,Numero=1)#si no existe semestre inicializa en 1
        else:
            semestre=db(db.Semestre.IdPartida==session.partida).select().last()#selecciona el objeto del ultimo semestre
            db.Semestre.insert(IdPartida=session.partida,Numero=semestre.Numero+1)# Y agrega un semestre mas
        CalculaDinero()
        redirect(URL('perfil'))
    return locals()

def eliminar():
    db.Calificacion.drop()
    return True
