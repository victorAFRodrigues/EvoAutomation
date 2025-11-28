$caminhoPasta = ".\.venv"

if(Test-Path -Path $caminhoPasta)
{
    .venv/Scripts/Activate.ps1 # Abre o ambiente virtual
} 
else 
{
    python -m venv .venv # Cria um ambiente virtual
    .venv/Scripts/Activate.ps1 # Abre o ambiente virtual
    pip install -r .\requirements.txt # Instala as dependencias
}


# Limpar pastas antigas
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue
Remove-Item -Force main.spec -ErrorAction SilentlyContinue


# Gerar novo executável
# Adicione caso não queria o terminal de debug dentro do executavel
# Adicione --debug=imports caso queira gerar um txt com os logs de importação
pyinstaller --onefile `
    --clean `
    --name GRPA `
    --add-data "public;public" `
    --add-data "modules;modules" `
    --add-data ".env;." `
    --specpath "dist" `
    --distpath "dist" `
    --workpath "dist/temp" `
    --icon="public/icon/rpa_goevo.ico" `
    --collect-all selenium `
    # --noconsole ` ## Adicione caso não queria o terminal de debug dentro do executavel
    main.py


# Desativar ambiente virtual
deactivate