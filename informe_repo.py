"""
informe_repo.py - Reporte automático del repositorio con PyGitHub.

Uso:
    python informe_repo.py

Requiere:
    - Archivo .env con GH_TOKEN y GITHUB_REPO.
    - Dependencias instaladas desde requirements.txt.

Nota:
    El archivo outputs/metrics.json se lee localmente si existe.
    No se busca en GitHub porque está ignorado por .gitignore.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from github import Github, GithubException


load_dotenv()

TOKEN = os.getenv("GH_TOKEN")
REPO_NAME = os.getenv("GITHUB_REPO")

if not TOKEN:
    raise EnvironmentError(
        "Variable GH_TOKEN no encontrada. Revisa tu archivo .env"
    )

if not REPO_NAME:
    raise EnvironmentError(
        "Variable GITHUB_REPO no encontrada. Revisa tu archivo .env"
    )


def separador(titulo: str) -> None:
    """Imprime un separador visual."""
    ancho = 70
    print(f"\n{'-' * ancho}")
    print(f" {titulo}")
    print(f"{'-' * ancho}")


def formatear_numero(valor: Any, decimales: int = 2) -> str:
    """Formatea números de manera segura."""
    if isinstance(valor, (int, float)):
        return f"{valor:,.{decimales}f}"
    return "N/A"


def mostrar_metricas_locales() -> None:
    """Muestra métricas si existe outputs/metrics.json localmente."""
    ruta_metricas = Path("outputs/metrics.json")

    if not ruta_metricas.exists():
        print(" No se encontró outputs/metrics.json en tu máquina.")
        print(" Ejecuta: python -m scripts.entrenar")
        return

    with open(ruta_metricas, "r", encoding="utf-8") as archivo:
        metricas = json.load(archivo)

    print(f" MAE: {formatear_numero(metricas.get('mae'))} USD")
    print(f" R2: {formatear_numero(metricas.get('r2'), 4)}")
    print(f" Train: {metricas.get('n_train', 'N/A')} muestras")
    print(f" Test: {metricas.get('n_test', 'N/A')} muestras")


def main() -> None:
    """Genera el informe del repositorio."""
    github_client = Github(TOKEN)

    try:
        repo = github_client.get_repo(REPO_NAME)
    except GithubException as exc:
        raise RuntimeError(
            "No se pudo acceder al repositorio. "
            "Verifica GITHUB_REPO y los permisos del token."
        ) from exc

    print(f"\n{'=' * 70}")
    print(" INFORME DEL REPOSITORIO")
    print(f" Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'=' * 70}")

    separador("INFORMACIÓN GENERAL")
    print(f" Repositorio: {repo.full_name}")
    print(f" Descripción: {repo.description}")
    print(f" Rama default: {repo.default_branch}")
    print(f" Estrellas: {repo.stargazers_count}")
    print(f" Forks: {repo.forks_count}")
    print(f" Issues abiertos: {repo.open_issues_count}")

    separador("ÚLTIMOS 5 COMMITS")
    commits = list(repo.get_commits()[:5])

    if not commits:
        print(" No se encontraron commits.")
    else:
        for commit in commits:
            sha = commit.sha[:7]
            mensaje = commit.commit.message.split("\n")[0]
            autor = commit.commit.author.name
            fecha = commit.commit.author.date.strftime("%Y-%m-%d")

            print(f" [{sha}] {fecha} - {autor}")
            print(f" {mensaje}")

    separador("ISSUES ABIERTOS")
    issues = [
        issue
        for issue in repo.get_issues(state="open")
        if issue.pull_request is None
    ]

    if not issues:
        print(" No hay issues abiertos.")
    else:
        for issue in issues:
            etiquetas = ", ".join(label.name for label in issue.labels)
            etiquetas = etiquetas or "sin etiqueta"
            fecha = issue.created_at.strftime("%Y-%m-%d")

            print(f" #{issue.number} {issue.title}")
            print(f" Etiquetas: {etiquetas} | Abierto: {fecha}")

    separador("ÚLTIMAS EJECUCIONES DE WORKFLOWS")
    workflows = list(repo.get_workflows())

    if not workflows:
        print(" No se encontraron workflows.")
    else:
        for workflow in workflows:
            runs = list(workflow.get_runs()[:2])

            if not runs:
                continue

            print(f"\n Workflow: {workflow.name}")

            for run in runs:
                estado = run.conclusion or run.status

                if estado == "success":
                    emoji = "[OK]"
                elif estado == "failure":
                    emoji = "[FALLA]"
                else:
                    emoji = "[EN PROCESO]"

                fecha = run.created_at.strftime("%Y-%m-%d %H:%M")

                print(
                    f" {emoji} Run #{run.run_number} - "
                    f"{estado} - {fecha} - rama: {run.head_branch}"
                )

    separador("MÉTRICAS LOCALES DEL ÚLTIMO ENTRENAMIENTO")
    mostrar_metricas_locales()

    print(f"\n{'=' * 70}\n")
    github_client.close()


if __name__ == "__main__":
    main()