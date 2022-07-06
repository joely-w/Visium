# Visium 🎉
Data visualisation for Pythium. This repository runs on a Flask backend with JS frontend.
This library is made to be customisable, so each chart has its own class that is made in such a way that it can be used as a local 
python deployment separate from the rest of the library (given a valid filepath), so that each chart can be customized individually. 
Documentation on this to follow!
## Get started 🍴
First navigate to `./src`
### Development environment 🔨

Install packages `pip install -r ./src/requirements.txt`

Then set flask app environment variables:

**Windows**

`set FLASK_APP=app& set FLASK_ENV=development& set FLASK_DEBUG=TRUE`

--------------
**Unix, Linux, macOS**

`export FLASK_APP=app FLASK_ENV=development FLASK_DEBUG=TRUE`

--------------
You can then run `flask run`, which by default serves content to http:/localhost:5000.

### Production environment 🚀
Documentation not complete, but to get started go to `/docs/SETUP.md`.

## Docs 😎
Everything static (e.g. HTML/CSS and JS) can be found in `src/static`.

I've started writing docs for deployment wrt CERN, which can be found in `docs`.
 