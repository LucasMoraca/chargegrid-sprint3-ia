# Gera .gitignore (garante que .env e artefatos locais nunca vão para o Git)
gitignore_content = """\
# Segredos / credenciais
.env
*.key

# Ambiente Python
__pycache__/
*.pyc
.venv/
venv/

# Checkpoints e caches do Colab / Jupyter
.ipynb_checkpoints/

# Artefatos gerados localmente
*.log
"""
with open(".gitignore", "w", encoding="utf-8") as f:
    f.write(gitignore_content)

# Gera o arquivo de identificação dos integrantes (nome; RM; turma)
integrantes_content = """\
Nome: Renan Fracalossi Mano da Silva | RM: 569610 | Turma: 1CCPX
Nome: Gabriel Barbosa Furin | RM: 572941 | Turma: 1CCPX
Nome: Gabriel de Almeida Santos | RM: 569395 | Turma: 1CCPX
Nome: Herbert Soares de Jesus | RM: 571507 | Turma: 1CCPX
Nome: Lucas Kiodi Moraca | RM: 571004 | Turma: 1CCPX
"""
with open("integrantes.txt", "w", encoding="utf-8") as f:
    f.write(integrantes_content)

print("Arquivos gerados: .gitignore, integrantes.txt")
print("\nLembrete: confirme que '.env' está listado no .gitignore ANTES do primeiro commit,")
print("e nunca faça commit de chaves de API diretamente no código-fonte.")
