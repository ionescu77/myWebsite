# myWebsite
Release Tests: [![Build Status](https://travis-ci.org/ionescu77/myWebsite.svg)](https://travis-ci.org/ionescu77/myWebsite)

Code Coverage: [![Coverage Status](https://coveralls.io/repos/ionescu77/myWebsite/badge.svg?branch=master&service=github)](https://coveralls.io/github/ionescu77/myWebsite?branch=master)

#Notes to (mainly) myself:

Codul sursă de la site-ul meu, încă nepublicat și mereu în lucru.

Run coverage locally and generate nice html reports (in ./reports/coverage)
```
python src/manage.py jenkins --enable-coverage --coverage-format html blogengine
```

Run tests locally with jenkins (django style does not work anymore)

```
python src/manage.py jenkins blogengine
```
2017.03.11

Workflow (using git hooks & shell scripts for deployment):
- local -> local virtualenv (python 2.7.9 & runserver)
- dev -> ionescu77.avproiect.com (python 2.7.9 & mod_passenger)
- test -> ionescu77.staging.avproiect.com (python 2.7.9 & mod_wsgi)
- live -> ionescu77.com (python 2.7.9 & & mod_wsgi)

2016.03.08

Am zis să public codul poate asta mă motivează să îi dau bice și să încep să mai și scriu câte ceva.

2015.12.11


#Future sprints
- adaugare Disqus pentru comentarii [Completed](https://github.com/ionescu77/myWebsite/issues/12)
- adăugare formular de contact
- css pt social icons
- code refactoring
- django i18n & localizare RO, DE, EN
- image credit
- CDN și alternativă la CDN pt boostrap, jquery
- publicare automată bookmark-uri folosind evernote API
- publicare imagini în articolele de blog
- optimizare SEO, meta și Structured Data Markup - schema.org
