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
delete from lemondefr_gros_titres;