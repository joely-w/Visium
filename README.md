# Visium 🎉
Data visualisation for Pythium. This repository runs on a Flask backend with JS frontend.
Ideally, the JS frontend does not need to be changed.
## Get started 🍴
### Development environment 🔨

First install packages `pip install -r ./src/requirements.txt`

Then set flask app environment variables:

**Windows**

`set FLASK_APP=app & FLASK_ENV=development & FLASK_DEBUG=TRUE`

--------------
**Unix, Linux, macOS**

`export FLASK_APP=app FLASK_ENV=development FLASK_DEBUG=TRUE`

--------------
You can then run `flask run`, which by default serves content to http:/localhost:5000.

### Production environment 🚀
Documentation not complete, but to get started go to `/docs/SETUP.md`.

## Docs 😎
Everything static can be found in `src/static`.

I've started writing docs for deployment wrt CERN, which can be found in `docs`.
 