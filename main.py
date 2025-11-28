from json import loads, load
from time import sleep
from modules.core.api import Api
from modules.core.worker import Worker
from modules.core.updater import EnvUpdate
from modules.utils.general import DotEnv, ExecTime

def local():
    EnvUpdate()

    # Le o arquivo json e disponibiliza os dados pela variavel Jdados
    files = ["data.json", "data2.json"]
    file = f"data/systemOrApplication_name/{files[3]}"

    with open(file, "r", encoding="utf-8") as file:
        Jdata = load(file)

    Jdata = Jdata["content"][0]

    automation_source = Jdata["RPA_SOURCE"]
    automation_parameters = Jdata["RPA_PARAMS"]

    status, message = Worker(automation_source, automation_parameters)
    print(status, message)   

def run(app):
    api = Api()

    while app.running:
        EnvUpdate()
        search_timeout = int(DotEnv().get('SEARCH_TIMEOUT'))
        response = api.getTask("/IniciarTarefa").json()["content"]

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
                "?/FinalizarTarefa", 
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
