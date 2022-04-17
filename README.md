# learning-diary APIs
### Purpose:
- Build first Flask + GraphQL backend
- Personal use
### Database commands:
- Flask db init
- Flask db migrate
- Flask db upgrade
- More: https://flask-migrate.readthedocs.io/en/latest/

### TODO:
- Instruction.

### Dislikes about Flask x GraphQL (graphene) x SQLAlchemy:
##### For flask migration to automatically detect change from model, models need to inherit from db.Model (db = flask.current_app.extensions["migrate"].db).
- Leads to several occasions that models-related import need to be wrapped under 
flask.current_app.app_context().

##### The implementation of SQLAlchemyConnectionField and relay.Node make it a pain to write request and access response data.
- For example, to get name of all categories and topic of their belonging diaries:
    ```
    query {
     categories {
        edges {
          node {
            name,
            diaries {
              edges {
                node { topic }
              }
          } }
        }
     }
    }
    ```
