from lemondefr_lite.allume_lemonde import lemonde_url, soupe_categorique

def test_soupe_categorique():
    soupe_fillon_url = "http://www.lemonde.fr/affaire-penelope-fillon/article/2017/02/06/fillon-une-riposte-aux-allures-d-operation-survie_5075185_5070021.html"
    soupe_fillon_categorique = soupe_categorique(soupe_fillon_url)
    assert soupe_fillon_categorique["type"] == "article"
    assert soupe_fillon_categorique["category"] == "affaire-penelope-fillon"

    soupe_presidentielle_url = "http://www.lemonde.fr/election-presidentielle-2017/live/2017/02/06/en-direct-semaine-cruciale-pour-fillon-hamon-en-campagne-suivez-l-actualite-politique_5075070_4854003.html"
    soupe_presidentielle_categorique = soupe_categorique(soupe_presidentielle_url)
    assert soupe_presidentielle_categorique["type"] == "live"
    assert soupe_presidentielle_categorique["category"] == "election-presidentielle-2017"

def test_lemonde_url():
    truncated_wa_url = "http://web.archive.org/web/20170206140107/http://www.lemonde.fr/politique/article/2017/02/06/de-nouveaux-elements-de-l-enquete-fragilisent-la-defense-de-francois-fillon_5075160_823448.html"
    expected_lemonde_url = "http://www.lemonde.fr/politique/article/2017/02/06/de-nouveaux-elements-de-l-enquete-fragilisent-la-defense-de-francois-fillon_5075160_823448.html"

    assert lemonde_url(truncated_wa_url) == expected_lemonde_url