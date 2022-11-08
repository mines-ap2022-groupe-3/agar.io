# Style

Le but de ce TP est de s'assurer que le document soit correctement formater.

Pour formatter les fichiers python, il existe plusieurs outils. Nous allons utiliser [black](https://github.com/psf/black).

Le style/format doit-être préservé aux fil des commits/PR. Pour cela, nous allons voir plusieurs stratégies.

## Setup

Créer une nouvelle branches `<nom github>-style` à partir de `main`.

Vérifier que l'on travail bien dans le bon environnement virtuel conda.

```bash
(base) $ conda activate agario
# votre terminal doit indiquer le nom d'environnement:
(agario) $
```

Installer black

```bash
(agario) $ pip install black
```

## Formatage

Pour formatter un fichier python, il suffit de lancer la commande suivante:

```bash
(agario) $ black .
```

!attention! Cette commande va formatter tous les fichiers python du dossier courant. Il est donc important de commiter ses changements avant de lancer cette commande.

Conseil: penser à utiliser `git diff` pour vérifier que les changements sont corrects (si ce n'est pas le cas, il est toujours possible de revenir en arrière avec `git checkout`). 
Vous êtes responsable de vos changements et pas `black` qui n'est qu'un outil pour vous aider.

Pour les plus courageux, il est possible (mais pas toujours recommender) de lancer `black` avec une configuration spécifique (voir documentation).

## Next steps

* Configurer vs-code pour qu'il formate automatiquement le code python lorsqu'on sauvegarde un fichier.
* Configurer les hooks git. (voir [pre-commit](https://pre-commit.com/)).
* Configurer les actions github pour qu'elles vérifient le style du code python => chercher sur google "github actions black".