from pathlib import Path
from pprint import pprint

from lemondefr_lite.allume_lemonde import cuisine_meta_soupe, cuisine_soupe_1

def get_chaudron():
    html_file = Path('data', 'index_lemonde_20170206110227.html')
    return html_file.read_text()


def test_cuisine_meta_soupe():
    belle_soupe = cuisine_meta_soupe(get_chaudron())

    assert belle_soupe["last_updated_at"] == 'Mise à jour à 14h58'
    assert belle_soupe["live"] == False


def  test_cuisine_soupe_1():
    belle_soupe = cuisine_soupe_1(get_chaudron())

    assert belle_soupe["n_comment"] == 71
    assert belle_soupe["title"] == 'Penelope Fillon: «Jamais je n’ai officialisé ma qualité d’assistante parlementaire»'
    assert belle_soupe["subtitle"] == "Lors de son audition par la police judiciaire, l’épouse de François Fillon a tenté de justifier la réalité de son travail de collaboratrice parlementaire."
    assert belle_soupe["type"] == "article"
    assert belle_soupe["category"] == "police-justice"
    assert belle_soupe["url_wa"] == "http://web.archive.org/web/20170206140107/http://www.lemonde.fr/police-justice/article/2017/02/06/penelope-fillon-je-lui-preparais-des-fiches_5075189_1653578.html"
    assert belle_soupe["url_lemonde"] == "http://www.lemonde.fr/police-justice/article/2017/02/06/penelope-fillon-je-lui-preparais-des-fiches_5075189_1653578.html"

