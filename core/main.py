from typing import Optional

from flask_graphql import GraphQLView

from core import create_app

app = create_app()

with app.app_context():
    from core.schema import schema

    # GraphQl route:
    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view(
            "graphql", schema=schema, graphiql=True  # for having the GraphiQL interface
        ),
    )


@app.teardown_appcontext
def shutdown_session(_: Optional[BaseException] = None) -> None:
    """
    Close database session before closing the app.
    """
    app.extensions["migrate"].db.session.remove()
