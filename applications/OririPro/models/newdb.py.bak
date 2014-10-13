db.define_table('Carrera',Field ('Titulo',requires=(IS_SLUG(),IS_LOWER(),IS_NOT_IN_DB(db,'Carrera.Titulo'))),
                Field ('Clave',requires=IS_NOT_EMPTY()))

db.define_table('Academia',
               Field ('IdCarrera','reference Carrera',readable=False,writable=False),
               Field ('Titulo',requires=IS_NOT_EMPTY()))

db.define_table('Docente',
                Field('Nombre',requires=IS_NOT_EMPTY()),
                Field('Dificultad','integer',requires=IS_NOT_EMPTY()))

db.define_table('TipoMateria',
                Field('Tipo',requires=IS_NOT_EMPTY())
                )

db.define_table('Materia',
                   Field('IdAcademia','reference Academia',requires=IS_NOT_EMPTY()),
                   Field('Nombre',requires=IS_NOT_EMPTY()),
                   Field ('Media','integer'),
                   Field('Varianza','integer'),
                   Field('Creditos','integer'),
                   Field('Ciclo',requires=IS_NOT_EMPTY()),
                   Field('IDTipoMateria','reference TipoMateria'),
                   Field('Clave',requires=IS_NOT_EMPTY())
                   )

db.define_table('Materia_Docente',
                Field('IdMateria','reference Materia'),
                Field('IdDocente','reference Docente'),
                )

db.define_table('Partida',
                Field('IdUsuario','reference auth_user'),
                Field('IdCarrera','reference Carrera')
                )
db.define_table('Semestre',
                Field('IdPartida','reference Partida'),
                Field('Numero','integer')
)

db.define_table('Calificacion',
                Field('IdPartida','reference Partida'),
                Field('IdMateriaDocente','reference Materia_Docente'),
                Field('Calificacion','integer',readable=False,writable=False),
                Field('IdSemestre','reference Semestre'),
                Field('Oportunidad','integer',readable=False,writable=False)
                )

db.define_table('NivelPericia',
                Field('IdPartida','reference Partida'),
                Field('IdAcademia','reference Academia'),
                Field('Pericia','integer',default=0))
