# ---------- CHOICES---------------------
CHOICE_TIPO_ORGANISMO = [
    (None, ''),
    ('Admisión', 'Admisión'),
    ('Comisaria', 'Comisaria'),
    ('Institucional', 'Institucional'),
    ('Salud', 'Salud'),
    ('U.F.I.s', 'U.F.I.s'),
    ('Escuelas', 'Escuelas'),
    ('Zonal', 'Zonal'),
    ('Oficios judiciales', 'Oficios judiciales'),
    ('Politicas de genero', 'Politicas de genero'),
    ('Expediente civil', 'Expediente civil'),
]


CHOICE_1A5=[
    (None, ''),
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('Más de 5', 'Más de 5'),
]

CHOICE_EMB_RIESGO=[
    (None, ''),
    ('Normal', 'Normal'),
    ('Adolescente', 'Adolescente'),
    ('De riesgo (Diabetes, Hipertension, Sífilis, etc.)', 'De riesgo (Diabetes, Hipertension, Sífilis, etc.)'),
]

CHOICE_EDUCACION=[
    (None, ''),
    ('Primario', 'Primario'),
    ('Secundario', 'Secundario'),
    ('Terciario', 'Terciario'),
    ('Universitario', 'Universitario'),
]
CHOICE_ESTADO=[
    (None, ''),
    ('Completo', 'Completo'),
    ('Incompleto', 'Incompleto'),
    ('En curso', 'En curso'),
    ('No aplica', 'No aplica'),
]

CHOICE_TIPO_IVI=[
    (None, ''),
    ('Madre o Cuidador principal', 'Madre o Cuidador principal'),
    ('Bebé, niño o niña', 'Bebé, niño o niña'),
    ('Familia', 'Familia'),
    ('Ajustes', 'Ajustes'),
]
CHOICE_NOSI=[
    (None, ''),
    ('SI', 'SI'),
    ('NO', 'NO'),
]
CHOICE_RESPONSABLES=[
    ('Garcia Maria Begoña','Garcia Maria Begoña'),
    ('Vivas Antonella','Vivas Antonella'),
    ('Rodriguez Vanina Natalia','Rodriguez Vanina Natalia'),
    ('Torres Liliana Yanet','Torres Liliana Yanet'),
    ('Palavecino Marianela Celeste','Palavecino Marianela Celeste'),
    ('Mancuso Agostina Lourdes','Mancuso Agostina Lourdes'),
    ('Autelli Florencia Belen','Autelli Florencia Belen'),
    ('Cardozo Claudia Yamila Noemi','Cardozo Claudia Yamila Noemi'),
    ('Ganduglia Lourdes Rocío','Ganduglia Lourdes Rocío'),
    ('Diaz Karen Marlene Sara','Diaz Karen Marlene Sara'),
    ('Bastrate Brenda Yamila','Bastrate Brenda Yamila'),
    ('Gonzalez Ana Laura','Gonzalez Ana Laura'),
    ('Azcurra Maria Luz','Azcurra Maria Luz'),
    ('Araoz Luisa Emilia','Araoz Luisa Emilia'),
]

CHOICE_ACCION_DESARROLLADA = [
    ('Entrevista', 'Entrevista'),
    ('Entrevista telefonica', 'Entrevista telefonica'),
    ('Escucha', 'Escucha'),
    ('Entrevista en domicilio', 'Entrevista en domicilio'),
    ('Articulacion con otro efector', 'Articulacion con otro efector'),
    ('Solicita informe', 'Solicita informe'),
    ('Responde oficio', 'Responde oficio'),
    ('Informa', 'Informa'),
    ('Solicita vacante institucional', 'Solicita vacante institucional'),
    ('Adopcion de medida de abrigo – comunica', 'Adopcion de medida de abrigo – comunica'),
    ('Adopcion de medida de abrigo – acta', 'Adopcion de medida de abrigo – acta'),
    ('Adopcion de medida de abrigo – notificacion progenitores', 'Adopcion de medida de abrigo – notificacion progenitores'),
    ('Per inicial', 'Per inicial'),
    ('Cambio de lugar de implementacion', 'Cambio de lugar de implementacion'),
    ('Restitucion de derechos', 'Restitucion de derechos'),
    ('Cese por abandono', 'Cese por abandono'),
    ('Per 45', 'Per 45'),
    ('Per 90', 'Per 90'),
    ('Per 120', 'Per 120'),
    ('Per 150', 'Per 150'),
    ('Per conclusion', 'Per conclusion'),
    ('Recepcion oficio judicial', 'Recepcion oficio judicial'),
    ('Recepcion denuncia', 'Recepcion denuncia'),
    ('Audiencia juzgado', 'Audiencia juzgado'),
    ('Pase a equipo', 'Pase a equipo'),
    ('Solicita intervencion a equipo fortalecimiento', 'Solicita intervencion a equipo fortalecimiento'),
    ('Acta compromiso familiar', 'Acta compromiso familiar'),
    ('Recepcion de informe', 'Recepcion de informe'),
    ('Gestion', 'Gestion'),
    ('Solicitud de intervencion a otro sl', 'Solicitud de intervencion a otro sl'),
    ('Solicita intervencion otro efector', 'Solicita intervencion otro efector'),
    ('Solicita fuerza publica', 'Solicita fuerza publica'),
    ('Acta', 'Acta'),
    ('Intervencion por guardia', 'Intervencion por guardia'),
]


CHOICE_1to40=[(i, str(i)) for i in range(1, 41)]

CHOICE_4to40=[(i, str(i)) for i in range(4, 41)]

CHOICE_MOTIVO_INGRESO=[
    (None, ''),
    ('ASI', 'ASI'),
    ('Violencia/negligencia', 'Violencia/negligencia'),
    ('Maltrato infantil', 'Maltrato infantil'),
    ('Incump. D. D. Asistencia', 'Incump. D. D. Asistencia'),
    ('Situación de calle', 'Situación de calle'),
    ('Riesgo habitacional/salud/alimenticio', 'Riesgo habitacional/salud/alimenticio'),
    ('Fuga de hogar', 'Fuga de hogar'),
    ('Adolescente en riesgo (embarazo/aborto)', 'Adolescente en riesgo (embarazo/aborto)'),
    ('Riesgo escolar', 'Riesgo escolar'),
    ('Conflictos con la ley', 'Conflictos con la ley'),
    ('Adicciones', 'Adicciones'),
    ('Niño en riesgo', 'Niño en riesgo'),
    ('Filiación y guardia', 'Filiación y guardia'),
    ('Otros', 'Otros'),
]

CHOICE_CONOCIMIENTO_SITUACION=[
    (None, ''),
    ('Denuncia Policial', 'Denuncia Policial'),
    ('Familiares', 'Familiares'),
    ('Motivo3', 'Motivo3'),
    ('Motivo4', 'Motivo4'),
    ('Motivo5', 'Motivo5'),
    ('Motivo6', 'Motivo6'),
    ('Otros', 'Otros'),
]

CHOICE_TIPO_INGRESO=[
    (None, ''),
    ('Criteros autónomos de ingreso', 'Criteros autónomos de ingreso'),
    ('Motivo de falta de control o control insuficiente', 'Motivo de falta de control o control insuficiente'),
    ('Criterios combinables de ingreso', 'Criterios combinables de ingreso'),
    ('Criterios sociales para el ingreso', 'Criterios sociales para el ingreso'),
]