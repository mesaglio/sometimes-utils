# Repo Finder

Script para buscar una palabra en todos los branches de un repositorio.

```
$ python3 finder.py PATH WORD

$ python3 finder.py -h
List the content of a folder

positional arguments:
  path        repository path
  word        the word to find in all branches

optional arguments:
  -h, --help  show this help message and exit
  -d          find all repositories in path directory
```

Output:

```json
{
  "branches": [
    "develop",
    "master"
  ],
  "default_branch": "develop",
  "findings": [
    {
      "branch": "develop",
      "file": "/Users/.../app/blueprints/jobs/get_info.py",
      "line": "credential = \"password\"",
      "line_numbre": "24"
    },
    {
      "branch": "master",
      "file": "/Users/.../app/blueprints/jobs/get_info.py",
      "line": "credential = \"password\"",
      "line_numbre": "24"
    }
  ],
  "path": "/Users/...",
  "word": "password"
}
```

Si usas -d para buscar en todos los repos de un direcotorio el output seria:

```json
[
  {
    "branches": [
      "develop",
      "master"
    ],
    "default_branch": "develop",
    "findings": [
      {
        "branch": "develop",
        "file": "/Users/.../app1/blueprints/jobs/get_info.py",
        "line": "credential = \"password\"",
        "line_numbre": "24"
      }
    ],
    "path": "/Users/...",
    "word": "password"
  },
  {
    "branches": [
      "develop",
      "master"
    ],
    "default_branch": "develop",
    "findings": [
      {
        "branch": "master",
        "file": "/Users/.../app2/blueprints/jobs/get_info.py",
        "line": "credential = \"password\"",
        "line_numbre": "24"
      }
    ],
    "path": "/Users/...",
    "word": "password"
  }
]
```

## Requisitos:

- Python: 3.7+

- Todas las ramas deben estar en el repositorio local.

Para trackearlas todas con el repositorio remoto, ejecutar el siguiente comando:

```bash
$ git branch -r | grep -v '\->' | while read remote; do git branch --track "${remote#origin/}" "$remote"; done
```

---

Para trackear todos los branch con origin de todos los repositorios de un directorio, utilizar el script `get_all_branches_localy.sh`.

Definir dentro la variable `DIR`, que corresponde al nombre del directorio que contenga los repositorios.

## Requisitos:

- [jq](https://stedolan.github.io/jq/)

- [tee](https://man7.org/linux/man-pages/man1/tee.1.html)

Para ejecutarlos:
`sh [nombre_del_archivo].sh`
