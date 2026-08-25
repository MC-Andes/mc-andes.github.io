# Sitio de MC-Andes

Fuente de [mc-andes.github.io](https://mc-andes.github.io/), construida con
MkDocs Material y publicada desde GitHub Actions.

## Desarrollo

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdocs serve
mkdocs build --strict
```

Los posts usan la convención **Contexto / Cambio / Impacto / Próximo paso** y
enlazan los issues, Pull Requests o repositorios relacionados.
