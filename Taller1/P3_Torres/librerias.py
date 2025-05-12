import subprocess
import sys

# Lista de paquetes que necesitamos
paquetes_necesarios = ['networkx', 'matplotlib', 'imageio']

def instalar_paquete(paquete):
    """Instala un paquete usando pip"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", paquete])

def verificar_e_instalar(paquetes):
    """Verifica e instala los paquetes que falten"""
    for paquete in paquetes:
        try:
            __import__(paquete)
            print(f"✅ El paquete '{paquete}' ya está instalado.")
        except ImportError:
            print(f"⚠️ El paquete '{paquete}' no está instalado. Instalando...")
            instalar_paquete(paquete)
            print(f"✅ '{paquete}' instalado correctamente.")

if __name__ == "__main__":
    verificar_e_instalar(paquetes_necesarios)
    print("\n🚀 Todos los paquetes necesarios están listos.")
