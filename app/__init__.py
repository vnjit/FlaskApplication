from flask import Flask


def create_app():
    """Construct the core app object."""
    app = Flask(
        __name__,
        instance_relative_config=False,
        template_folder="templates"
    )
    # Application Configuration
    app.config.from_object('config.Config')

    with app.app_context():
        from Route import routes
        from Example import example

        return app