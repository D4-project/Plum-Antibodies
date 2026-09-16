# Plum-Antibodies

Plum-Antibodies contient les règles YAML utilisées par
[Plum-Island](https://github.com/D4-project/Plum-Island) pour détecter et
classifier des services à partir des rapports produits par les scanners.

Lorsqu’un rapport de scan est reçu, Plum-Island extrait ses champs techniques
(bannières, titres HTTP, favicons, certificats, protocoles, etc.). Les règles
de ce dépôt recherchent des correspondances dans ces champs et ajoutent des
tags normalisés comme `product:nginx`, `vendor:cisco` ou `proto:ssh`.

Les règles sont stockées dans [`tags/`](tags/) au format YAML. Chaque règle
décrit :

- une description lisible ;
- une requête de recherche ;
- les tags à appliquer ;
- une version UTC utilisée lors des imports.

Exemple :

```yaml
description: HashiCorp Vault
query: http_favicon_mmhash:747250914 AND http_title.bg:Vault
tags:
- product:hashicorp-vault
- vendor:hashicorp
version: 20260428T170756Z
```

## Documentation

- [Guide des règles de tags](documentation/tagging.md)
- [Syntaxe des recherches Plum-Island](https://github.com/D4-project/Plum-Island/blob/main/documentation/search.md)
- [Outils d’import et de réindexation](https://github.com/D4-project/Plum-Island/blob/main/documentation/tools.md#tag-tools)
- [Installation de Plum-Island et initialisation du sous-module](https://github.com/D4-project/Plum-Island/blob/main/documentation/installation.md)

La syntaxe utilisée dans le champ `query` est celle de la recherche Plum-Island.
Consultez sa documentation avant de créer une règle, notamment pour les
opérateurs exacts, `.bg`/`.begin`, `.lk`/`.like`, `AND`, `OR` et `NOT`.

## Utilisation comme sous-module

Plum-Island monte ce dépôt dans `webapp/tags/`. Les règles sont donc visibles
dans l’application sous `webapp/tags/tags/`.

```bash
git clone --recurse-submodules https://github.com/D4-project/Plum-Island.git
```

Pour mettre à jour les règles dans une installation existante :

```bash
git -C webapp/tags pull --ff-only origin main
```

Après une modification de règle, importez les règles puis réindexez les
documents existants avec les outils de Plum-Island.
