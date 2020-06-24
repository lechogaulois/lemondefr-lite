# Lemondefr-lite

Une base de données des gros titres du site lemonde.fr.

Période couverte actuellement : premier tour de la présidentielle de 2017.

Périmètre informationnel : pour chaque une référencée le gros titre (premier article) et sa catégorisation éditoriale.

## Requêtes d'intérêts concernant le débat public

Répartition des gros titres par catégorie sur tout l'échantillon. 

```sql
select category, count(*) as cpt
from lemondefr_gros_titres
group by category
order by cpt desc; 
```

```sql
select id, title, retrieved_at
from lemondefr_gros_titres
where title like '%fillon%' or subtitle like '%fillon%'
order by retrieved_at asc; 

/* 59 gros titres */
```

```sql
select distinct id, title, retrieved_at
from (
    select *
    from lemondefr_gros_titres
    where title like '%macron%' or subtitle like '%macron%'
    order by retrieved_at
); 

/* 22 gros titres */
```

```sql
select distinct url_article_lemondefr
from (
    select *
    from lemondefr_gros_titres
    where title like '%hamon%' or subtitle like '%hamon%'
    order by retrieved_at
); 

/* 20 gros titres */
```

```sql
select distinct url_article_lemondefr
from (
    select *
    from lemondefr_gros_titres
    where title like '%mélenchon%' or subtitle like '%mélenchon%'
    order by retrieved_at
); 

/* 14 gros titres */
```

```sql
select distinct url_article_lemondefr
from (
    select *
    from lemondefr_gros_titres
    where title like '%le pen%' or subtitle like '%le pen%'
    order by retrieved_at
); 

/* 12 gros titres */
```

## Méthodologie de récupération

Nous avons récupéré les enregistrements appartenant 
aux collections archive.org contenant le mot clé "lemonde". 
Dans le dossier `lemondefr_culture`
vous pourrez retrouver la moulinette pour télécharger les unes.



## Modèle de données

```sql
create table if not exists lemondefr_gros_titres (
    id integer primary key autoincrement,
    url_une_wa text,
    html_une_wa text,
    url_article_wa text,
    url_article_lemondefr text,
    retrieved_at datetime,
    last_updated_at text,
    category text,
    type text,
    title text,
    subtitle text
);
```

La mise au propre des données se fait via les instructions suivantes :

```sql
/* certaines addresses sont mal formatées */
update lemondefr_gros_titres
set url_article_lemondefr = replace(url_article_lemondefr, 'www.', '');

/* nous assurons la suppression des doublons associés */
delete from lemondefr_gros_titres where id in (select id from (
select id, count(*) as cpt from lemondefr_gros_titres
group by url_article_lemondefr
having cpt > 1));
```

## Constituer soi-même la base de données

Le projet nécessite :

- Python 3.7.
- poetry (https://python-poetry.org)
- SQLite

Poetry installé, il suffit de se rendre dans le terminal
à la racine du projet cloné et exécuter :

```bash
poetry run allume_lemonde
```

La base de données `lemondefr.lite` est reconstruite
à chaque exécution de cette commande à la racine de ce projet.

## Contributions

Nous encourageons la libre réappropriation de ce projet.
