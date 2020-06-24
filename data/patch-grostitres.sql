/* certaines addresses sont mal formatées */
update lemondefr_gros_titres
set url_article_lemondefr = replace(url_article_lemondefr, 'www.', '');

/* nous assurons la suppression des doublons associés */
delete from lemondefr_gros_titres where id in (select id from (
select id, count(*) as cpt from lemondefr_gros_titres
group by url_article_lemondefr
having cpt > 1));