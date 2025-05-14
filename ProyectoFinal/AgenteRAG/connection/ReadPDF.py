import os

import PyPDF2
contenido = {}
script_path = os.path.dirname(os.path.realpath(__file__))
agente_path = os.path.dirname(script_path)

pdf1 = 'AccionDePersonal.pdf'
pdf2 = 'DiarioDeGerente.pdf'
pdf3 = 'EmailPersonal.pdf'
pdf4 = 'ReporteIncidentes.pdf'

rutas = [pdf1, pdf2, pdf3, pdf4]

for ruta in rutas:
    ruta_pdf = os.path.join(agente_path, 'data', ruta)
    contenido[ruta] = {}
    with open(ruta_pdf, 'rb') as archivo:
        lector = PyPDF2.PdfReader(archivo)
        for i, pagina in enumerate(lector.pages):
            texto = pagina.extract_text()
            contenido[ruta][i] = texto
            print(f'--- Página {i+1} ---\n{texto}\n')


print(contenido)

