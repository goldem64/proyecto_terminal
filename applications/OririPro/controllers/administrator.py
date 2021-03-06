# coding: utf8
def index():
    return dict(message="hello from admin.py")

import xml.etree.ElementTree as ET
import os
def leerMaterias():
    materias=os.path.join(request.folder, 'static', 'materias.xml')
    print materias
    print '-------------Iniciando parsing del xml-------------'
    tree=ET.parse(materias)
    root=tree.getroot()
    Clave=root.get('clave')
    Carrera=root.get('carrera')
    db.Carrera.update_or_insert(db.Carrera.Clave==Clave,Titulo=Carrera,Clave=Clave)
    CarreraData=db(db.Carrera.Clave==Clave).select().first()
    print Clave
    print Carrera
    print
    for Academia in root.findall('academia'):
        print '---------------------ACADEMIA---------------------'
        NombreAcademia = Academia.get('nombre')
        db.Academia.update_or_insert(db.Academia.Titulo==NombreAcademia,Titulo=NombreAcademia,IdCarrera=CarreraData.id)
        AcademiaData=db(db.Academia.Titulo==NombreAcademia).select().first()
        print NombreAcademia
        for Materia in Academia.findall('materia'):
               NombreMateria=Materia.get('nombre')
               ClaveMateria=Materia.get('clave')
               Creditos= Materia.find('creditos')
               #Cast Creditos
               Creditos=int(format(Creditos.text))
               Media= Materia.find('media')
               #Cast Media
               Media=int(format(Media.text))
               Varianza=Materia.find('varianza')
               #Cast Varianza
               Varianza=int(format(Varianza.text))
                #Cast Tipo
               TipoMateria=format(Materia.find('tipo').text)
               Tipo=db(db.TipoMateria.Tipo==TipoMateria).select().first()
               #Cast Ciclo
               CicloMateria=Materia.find('ciclo')
               CicloMateria=format(CicloMateria.text)
               db.Materia.update_or_insert(db.Materia.Nombre==NombreMateria,Nombre=NombreMateria,Creditos=Creditos,Media=Media,
                                                       Varianza=Varianza,Clave=ClaveMateria,IDTipoMateria=Tipo.id,Ciclo=CicloMateria,IdAcademia=AcademiaData.id)
               MateriaData=db(db.Materia.Nombre==NombreMateria).select().first()
               print NombreMateria
               print 'creditos:',Creditos
               print Tipo.Tipo
               for Docente in Materia.findall('participante'):
                    Docente=format(Docente.text)
                    DocenteData=db(db.Docente.Nombre==Docente).select().first()
                    db.Materia_Docente.insert(IdMateria=MateriaData.id,IdDocente=DocenteData.id)
                    print Docente
    return locals()

def leerDocentes():
    docentes=os.path.join(request.folder, 'static', 'docentes.xml')
    print '-------------Iniciando parsing del xml-------------'
    tree=ET.parse(docentes)
    root=tree.getroot()
    for docente in root.findall('docente'):
        print '---------------------Docente---------------------'
        NombreDocente = docente.find('nombre')
        Dificultad=docente.find('dificultad')
        Dificultad=int(format(Dificultad.text))
        NombreDocente=format(NombreDocente.text)
        print NombreDocente
        print Dificultad
        db.Docente.update_or_insert(db.Docente.Nombre==NombreDocente,Nombre=NombreDocente,Dificultad=Dificultad)
    session.flash=("Docentes insertados correctamente")
    redirect(URL('index'))
    return locals()

@auth.requires_login()
def admin():
    db.Materia.IDTipoMateria.represent=lambda id,row:db.TipoMateria(id).Tipo
    db.Materia.IdAcademia.represent=lambda id,row:db.Academia(id).Titulo
    grid=SQLFORM.smartgrid(db.Materia,linked_tables=['Academia'],searchable= dict(Materia=True, Academia=False))
    return locals()
