import re
from pprint import pprint

from orator import DatabaseManager
from pathlib import Path
import bs4
import pendulum

PROJECT_ROOT_PATH = Path(__file__).parent.parent
DATA_DIRECTORY = PROJECT_ROOT_PATH.joinpath('data')

gros_titres_schema_sql = DATA_DIRECTORY.joinpath('schema-grostitres.sql').read_text()

config = {
    'default': 'sqlite',
    'sqlite': {
        'driver': 'sqlite',
        'database': PROJECT_ROOT_PATH.joinpath('lemondefr.lite'),
    }
}

db = DatabaseManager(config)


def mixeur(belle_soupe):
    belle_soupe["url_lemonde"] = lemonde_url(belle_soupe["url_wa"])
    belle_soupe["type"] = soupe_categorique(belle_soupe["url_lemonde"])["type"]
    belle_soupe["category"] = soupe_categorique(belle_soupe["url_lemonde"])["category"]

    return belle_soupe


def cuisine_meta_soupe(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')

    belle_soupe = {}
    ts_pattern = re.compile('(\d+)')
    ts_line = html.split("\n")[15]
    ts_utc_str = ts_pattern.findall(ts_line)[0]
    ts_date = pendulum.datetime(int(ts_utc_str[0:4]), int(ts_utc_str[4:6]), int(ts_utc_str[6:8]),
                                int(ts_utc_str[8:10]), int(ts_utc_str[10:12]), int(ts_utc_str[12:]))
    tz = pendulum.timezone("Europe/Paris")
    ts_date_france = tz.convert(ts_date)
    belle_soupe["retrieved_at"] = ts_date_france
    belle_soupe["last_updated_at"] = soup.select('a.date_maj')[0].text

    return belle_soupe


def cuisine_soupe_1(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')

    belle_soupe = {}

    belle_soupe["title"] = sterilisation(soup.select('article.titre_une h1')[0].text)
    belle_soupe["subtitle"] = sterilisation(soup.select('article.titre_une p.description')[0].text)
    belle_soupe["url_wa"] = full_wa_url(soup.select('article.titre_une a')[0]['href'])
    reactions = soup.select("h1.tt3 > span.nb_reactions")
    if (reactions.__len__() > 0):
        belle_soupe["n_comment"] = int(reactions[0].text)
    else:
        belle_soupe["n_comment"] = None

    return mixeur(belle_soupe)



def soupe_categorique(lemonde_url):
    tokens_url = lemonde_url.split('/')
    return {'category': tokens_url[3], 'type': tokens_url[4] }


def sterilisation(soupe_sale_text):
    soupe_sterile = soupe_sale_text.replace("Live", "")
    soupe_sterile = soupe_sale_text.replace("\n", "")
    soupe_sterile = soupe_sale_text.replace("\xa0", "")
    soupe_sterile = re.sub('\d+.*?$', '', soupe_sterile)
    soupe_sterile = soupe_sterile.strip()
    return soupe_sterile


def full_wa_url(truncated_wa_url):
    return "http://web.archive.org" + truncated_wa_url


def lemonde_url(truncated_wa_url):
    return truncated_wa_url[42:]


def cuisines_les_unes_presidentielles():
    for statement in gros_titres_schema_sql.split(';'):
        db.statement(statement)

    inserted_urls = [] # on évite les doublons, SQLite n'a pas de fonctions de fenêtrage de requête
    for une_file in DATA_DIRECTORY.joinpath("lemondefr-unes-elections2017-wa-html").glob("*.html"):
        print(une_file.absolute())
        une_html = une_file.read_text()
        meta_soupe = cuisine_meta_soupe(une_html)
        belle_soupe_1 = cuisine_soupe_1(une_html)

        if not inserted_urls.__contains__(belle_soupe_1["url_lemonde"]):
            db.table("lemondefr_gros_titres").insert(
                url_une_wa=une_file.name, # pour l'instant on se contente du nom de fichier
                                          # qui contient l'identifiant du snap
                url_article_wa=belle_soupe_1["url_wa"],
                url_article_lemondefr=belle_soupe_1["url_lemonde"],
                retrieved_at=meta_soupe["retrieved_at"],
                last_updated_at=meta_soupe["last_updated_at"],
                category=belle_soupe_1["category"],
                type=belle_soupe_1["type"],
                title=belle_soupe_1["title"],
                subtitle=belle_soupe_1["subtitle"]
            )

            inserted_urls.append(belle_soupe_1["url_lemonde"])



if __name__ == '__main__':
    cuisines_les_unes_presidentielles()


