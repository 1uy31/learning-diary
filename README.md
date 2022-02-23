# learning-diary (WIP)
### Purpose:
- Build first Flask + GraphQL backend
- Personal use
### Database commands:
- Flask db init
- Flask db migrate
- Flask db upgrade
- More: https://flask-migrate.readthedocs.io/en/latest/

### Dislikes:
##### For flask migration to automatically detect change from model, models need to inherit from db.Model (db = flask.current_app.extensions["migrate"].db).
- Leads to several occasions that models import need to be wrapped under 
flask.current_app.app_context().
- Not convenient to set up, tear down and isolate test database between tests (see conftest.py).
