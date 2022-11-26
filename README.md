### Database commands:
- Flask db init
- Flask db migrate
- Flask db upgrade
- More: https://flask-migrate.readthedocs.io/en/latest/

### To run the app locally:
- Create a PostgreSQL DB and declare the URI path to instance/dev_config.toml
- Create a file .env with content from the template .env.example
- Run the DB commands
- Use poetry to spawn a virtual env
- Run the app: `flask run`
- Open http://127.0.0.1:5000/graphql to play around with the APIs, which have automatic documentation


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
