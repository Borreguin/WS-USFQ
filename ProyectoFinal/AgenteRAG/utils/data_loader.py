import os
import PyPDF2

pdf_files = [
    os.path.join(os.path.dirname(__file__), '../data/AccionDePersonal.pdf'),
    os.path.join(os.path.dirname(__file__), '../data/DiarioDeGerente.pdf'),
    os.path.join(os.path.dirname(__file__), '../data/EmailPersonal.pdf'),
    os.path.join(os.path.dirname(__file__), '../data/ReporteIncidentes.pdf'),
]

# Extraer texto de los PDFs
def get_pdf_context(pdf_path):
    """Extrae y retorna el texto de un PDF como string."""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        pdf_text = ""
        for page in reader.pages:
            pdf_text += page.extract_text() or ""
    return pdf_text

# Concatena el texto de todos los PDFs
contexto_pdf = "\n\n".join([get_pdf_context(path) for path in pdf_files])

