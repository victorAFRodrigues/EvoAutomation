from json import loads, load
from time import sleep
from modules.core.api import Api
from modules.core.worker import Worker
from modules.core.updater import EnvUpdate
from modules.utils.general import DotEnv, ExecTime

def local():
    EnvUpdate()

    # Le o arquivo json e disponibiliza os dados pela variavel Jdados
    files = ["nf_produto.json", "nf_servico.json", "fornecedor.json", 'nf_produto_GOEVO.json']
    file = f"database/dealernet/{files[3]}"

    with open(file, "r", encoding="utf-8") as file:
        Jdata = load(file)

    Jdata = Jdata["content"][0]

    print(Jdata)

    RPA_SOURCE = Jdata["RPA_SOURCE"]
    RPA_PARAMS = Jdata["RPA_PARAMS"]

    status, msg = Worker(RPA_SOURCE, RPA_PARAMS)
    print(msg)   

def test():
    api = Api()
    APP_DATA = api.getVariables('?Grupolelacteste/RPAManager/AtualizarVariaveis')

    for key, value in {
        "SEARCH_TIMEOUT": APP_DATA['searchTimeout'],
        "SYSTEM":  APP_DATA['application']['system'],
        "SYSTEM_URL":  APP_DATA['application']['systemUrl'],
        "USER":  APP_DATA['application']['user'],
        "PASSWORD":  APP_DATA['application']['password'],
    }.items():
        DotEnv().set(key, value)

def run(app):
    api = Api()

    while app.running:
        EnvUpdate()
        search_timeout = int(DotEnv().get('SEARCH_TIMEOUT'))
        response = api.getTask("?Grupolelacteste/RPAManager/IniciarTarefa").json()["content"]

        if not response:
            print(f"Nenhuma Task de automação foi encontrada. Tentando novamente em {search_timeout} segundos...\n")
            sleep(search_timeout)
        else:
            response = loads(response)[0]

            RPA_GUID = response["RPA_GUID"]
            RPA_SOURCE = response["RPA_SOURCE"]
            RPA_PARAMS = loads(response["RPA_PARAMS"])

            print(f"\nIniciando tarefa: \n guid: {RPA_GUID} \n source: {RPA_SOURCE}")

            success, WorkerMsg = Worker(RPA_SOURCE, RPA_PARAMS)

            api.finishTask(
                "?Grupolelacteste/RPAManager/FinalizarTarefa", 
                WorkerMsg,  
                "00" if success else "01", 
                RPA_GUID
            )

            print(WorkerMsg)

def main(): 
    EnvUpdate()   
    # caso SYSTEM_URL exista ele cria uma classe app simulando o comportamento do modulo app.py assim evitando erros em automações web.
    if DotEnv().get('SYSTEM_URL'):
        class App():
            def __init__(self):
                self.running = True

            def __enter__(self):
                self.running = True
                return self
            
            def __exit__(self, exc_type, exc_value, traceback):
                if exc_type:
                    pass
                return False
    else:
        from modules.core.app import App
    
    with App() as app:
        run(app)

if __name__ == "__main__":
    # main()
    local()
