from time import time
import base64
import tempfile
import os
import sys
from dotenv import load_dotenv


class ExecTime:
    def __init__(self, name="Bloco"):
        self.name = name

    def __enter__(self):
        self.start = time()
        return self  # permite acessar atributos depois, se quiser

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time()
        print(f"\nO tempo de execução de '{self.name}' foi: {end - self.start:.4f} segundos\n")

class Xml:
    def __init__(self, file_content, file_name):
        self.__file_content = file_content
        self.__file_name = file_name
    
    def generate(self):
        """Recebe uma string base64, decodifica e salva como arquivo XML temporário."""

        xml_data = base64.b64decode(self.__file_content)

        # Cria caminho do arquivo temporário
        temp_path = os.path.join(tempfile.gettempdir(), self.__file_name)

        # Salva o conteúdo no arquivo
        with open(temp_path, "wb") as f:
            f.write(xml_data)

        return temp_path
    
class DotEnv:
    def __init__(self):
        load_dotenv(ResourcePath(".env"))

    def get(self, key):
        value = os.getenv(key)
        if value is None:
            raise KeyError(f'A variável de ambiente "{key}" não está cadastrada.')
        
        return value

    def set(self, key, value):
        try:
            with open(ResourcePath(".env"), "r") as f:
                rows = f.readlines()
        except FileNotFoundError:
            rows = []

        found = False
        with open(ResourcePath(".env"), "w") as f:
            for row in rows:
                if row.startswith(f"{key}="):
                    f.write(f'{key}="{value}"\n')
                    found = True
                else:
                    f.write(row)
            if not found:
                f.write(f'{key}="{value}"\n')
    
class Json:
    """
    A função procura dentro do json a chave passada via parametro

    Parametros: 
        - json (dict): Espera um json no construtor para iterar
        
    Retorno: 
        - str: o valor da chave "Conteudo"
    """
    def __init__(self, json):
        self.__json = json

                
    def get(self, key):
        """
        A função procura dentro do json a chave passada via parametro
        Parametros: 
            - key (str): Espera uma chave para procurar
        Retorno: 
            - str: o valor da chave "Conteudo"
        """
        for data in self.__json:
                if data["Nome"] == key:
                    return (data['Conteudo'])
           
class ResourcePath:
    """
    Classe que resolve o caminho absoluto de um recurso.
    Executa automaticamente a lógica ao ser instanciada.
    """
    def __init__(self, relative_path: str):
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS  # usado pelo PyInstaller
        else:
            base_path = os.path.abspath(".")
        
        # resultado final
        self.result = os.path.join(base_path, relative_path)
    
    def __str__(self):
        """Permite usar print(ResourcePath('...')) diretamente"""
        return self.result
    
    def __fspath__(self):
        """Permite usar este objeto onde um caminho de arquivo é esperado."""
        return self.result

