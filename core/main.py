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

# Register blueprints:
# app.register_blueprint(diary_bp)
