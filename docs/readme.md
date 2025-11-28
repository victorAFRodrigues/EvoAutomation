# 🤖 GoEvo RPA

O **GoEvo RPA** é uma aplicação de **automação agnóstica**, desenvolvida em **Python**, projetada para integrar e automatizar tarefas em diferentes sistemas — sejam eles **web**, **desktop**, ou **ERP corporativos** como o **Protheus** e **DealerNet**.  

Ela é considerada **agnóstica** porque **não depende de um sistema, tecnologia ou interface específica**: suas automações são construídas por módulos independentes, capazes de operar com qualquer interface gráfica ou navegador, conforme a necessidade do processo.

---

## ⚙️ Principais Características

✅ **Automação de interface gráfica (Desktop)** com [PyAutoGUI](https://pyautogui.readthedocs.io/)  
✅ **Automação Web** via [Selenium WebDriver](https://selenium.dev)  
✅ **Ícone na bandeja (System Tray)** para controle da aplicação com [PyStray](https://pypi.org/project/pystray/)  
✅ **Execução de rotinas autônomas** organizadas por módulos  
✅ **Integração de dados via JSON**  
✅ **Suporte para múltiplos sistemas ERP** (ex: TOTVS Protheus, DealerNet, NBS e etc.)  
✅ **Arquitetura modular e expansível** — novos fluxos podem ser adicionados sem afetar os existentes  

---

## 🧠 Conceito de Automação Agnóstica

O **GoEvo RPA** foi desenhado para **não depender de um único contexto de execução**.  
Ele detecta e interage com elementos de tela, janelas ou páginas web, sem amarrar o código a um sistema fixo. O projeto é estruturado de forma modular, permitindo fácil manutenção, extensão e empacotamento em executável único via **PyInstaller**.

Isso possibilita:
- Reaproveitar fluxos de automação entre diferentes empresas ou sistemas.  
- Centralizar todas as automações num mesmo **núcleo de execução (core)**.  
- Criar scripts reutilizáveis, dinâmicos e independentes de ambiente.  

---


## 📂 Estrutura de Diretórios

```
├── .build/
├── .venv/
├── database/
│   └── dealernet/
│       ├── fornecedor.json
│       ├── nf_produto.json
│       └── nf_servico.json
├── docs/
│   ├── readme.md
│   └── tree.txt
├── modules/
│   ├── __init__.py
│   ├── automations/
│   │   ├── __init__.py
│   │   ├── automation_model/
│   │   │   ├── __init__.py
│   │   │   ├── helpers
│   │   │   |   ├── __init__.py
│   │   │   |   └── login.py
│   │   │   └── automation_file.py
│   │   └── dealernet/
│   │       ├── __init__.py
│   │       ├── helpers/
│   │       │   ├── __init__.py
│   │       │   ├── categoriza_produtos.py
│   │       │   ├── importar_xml.py
│   │       │   ├── login.py
│   │       │   ├── preenche_capa_nf_produto.py
│   │       │   ├── preenche_capa_nf_servico.py
│   │       │   ├── preenche_form_pt1.py
│   │       │   ├── preenche_item.py
│   │       │   ├── preenche_parcelas.py
│   │       │   ├── preenche_rateio.py
│   │       │   ├── procura_fornecedor.py
│   │       │   ├── seleciona_nf_xmltable.py
│   │       │   └── seleciona_nota.py
│   │       ├── cadastrar_nf_produto.py
│   │       ├── cadastrar_nf_servico.py
│   │       └── validar_fornecedor.py
│   ├── core/
|   |   ├── __init__.py
│   │   ├── api.py
│   │   ├── app.py
│   │   ├── automation.py
│   │   ├── updater.py
│   │   └── worker.py 
│   └── utils/
│       ├── __init__.py
│       ├── browser_automation.py
│       ├── desktop_automation.py
│       ├── general.py
│       └── models.py
├── public/
│   └── icon/
│       └── rpa_goevo.ico
├── .env-example
├── .gitignore
├── GRPA.spec
├── build.ps1
└── requirements.txt
```

<br><br>

## ⚙️ Configuração do Ambiente

### 1. Criar e ativar o ambiente virtual

`python -m venv .venv
.\.venv\Scripts\Activate.ps1` 

### 2. Instalar dependências

`pip install -r requirements.txt` 

### 3. Configurar variáveis de ambiente

Copie o arquivo `.env-example` e renomeie para `.env`, preenchendo as seguintes variaveis:

```
API_URL=https://suaapi.com
GOEVO_APP_TPTOKEN=SEU_TOKEN_AQUI
RPA_EXECUTOR=SRV_RPA_001
``` 

> ⚠️ **Atenção:**                         
> Nunca versionar `.env` com credenciais reais.
> O arquivo `.env-example` serve apenas como modelo. <br><br>
> As variaveis: `APPLICATION`, `SEARCH_TIMEOUT`, `SYSTEM_URL`, `USER`, `PASSWORD` Serão preenchidas via dinamicamente via API

<br><br>

## 🚀 Como usar
### 🔧 Desenvolvimento
Atualiza automaticamente ao salvar arquivos:
```
docker compose -f docker-compose.yml up
```


### 🏗️ Produção
Gera imagem fechada e leve:
```
docker compose -f docker-compose.prod.yml build --no-cache
docker compose -f docker-compose.prod.yml up -d
```


### 🧩 Script de Build (build.ps1)

O projeto já possui um script completo em PowerShell para gerar o executável automaticamente.

#### 🔨 Executar o build

`.\build.ps1` 

O script:

1.  Cria ou ativa o ambiente virtual.
    
2.  Instala as dependências.
    
3.  Remove builds antigos (`build`, `dist`).
    
4.  Gera um novo executável via **PyInstaller** com:
    
    -   Inclusão de pastas `public`, `modules`, `.env`
        
    -   Ícone customizado `rpa_goevo.ico`
        
    -   Coleta automática de dependências Selenium
        
    -   Saída final em `.build/GRPA.exe`
        
<br>

## 🧰 Dependências Principais

As dependências estão listadas em `requirements.txt`.  
Algumas das mais importantes:

Biblioteca                                                          => Função

`selenium`                                                       => Automação de browsers
`pyautogui`, `pystray`, `opencv-python` => Automação e interação com desktop
`requests`, `python-dotenv`                       => Comunicação HTTP e variáveis de ambiente
`pyinstaller`                                                 => Empacotamento do projeto em executável
`Eel`, `bottle`                                               => Interface local e APIs embutidas
`pydantic`                                                       => Validação e tipagem de dados
`numpy`, `pillow`                                           => Manipulação de dados e imagens

<br>

## 🚀 Execução

Após o build, o executável será gerado em:

`.build/GRPA.exe` 

Para executar diretamente do código-fonte:

`python main.py` 

<br>

## 🧩 Estrutura de Automação

-   **modules/core/**  
    Núcleo do sistema RPA (executor, atualizador, comunicação com API).
    
-   **modules/automations/dealernet/**  
    Automação principal do sistema Dealernet, com scripts de preenchimento, login e validação.
    
-   **modules/utils/**  
    Ferramentas genéricas de suporte (navegação, automação desktop, modelos e helpers).
    
-   **database/dealernet/**  
    Dados auxiliares em JSON para teste de rotinas durante o desenvolvimento (fornecedores, notas fiscais, etc.).
    
<br>

## 🧱 Build Flags Importantes

Usadas no `build.ps1`:

`Flag`                                     => Função
`--onefile`                           => Gera executável único
`--clean`                               => Remove temporários antes do build
`--add-data`                         => Inclui diretórios ou arquivos extras
`--distpath`                         => Define pasta de saída (`.build`)
`--icon`                                 => Define ícone do executável
`--collect-all selenium` => Garante inclusão completa do Selenium
`--noconsole` _(opcional)_   => Oculta terminal do executável


<br>

### Desenvolvido  por **GoEvo**  
> *Automação sem fronteiras — para qualquer sistema.*
