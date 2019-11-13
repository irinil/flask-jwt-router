import logging
logger = logging.getLogger()


class _Config:
    """
    :param secret_key:
    :param entity_key:
    :param entity_model:
    :param whitelist_routes:
    :param api_name:
    """
    def __init__(self,
                 secret_key=None,
                 entity_key=None,
                 whitelist_routes=None,
                 api_name=None,
                 entity_model=None,
                 ):

        self.secret_key = secret_key
        self.entity_key = entity_key
        self.entity_model = entity_model
        self.whitelist_routes = whitelist_routes
        self.api_name = api_name


class FlaskJwtRouter:

    logger = logging
    config = {}
    app = None
    exp = 30
    secret_key = "DEFAULT_SECRET_KEY"
    entity_key = "id"
    _auth_model = None
    extensions: _Config

    def __init__(self, app=None, **kwargs):
        """
        If there app is None then self.init_app(app=None, **kwargs) need to be called
        inside the Flask app factory pattern
        :param app:
        :param kwargs:
        """
        if app:
            self.app = app
            config = self.get_app_config(app)
            self.config = config
            self.extensions = self.init_flask_jwt_router(config)

    def init_flask_jwt_router(self, config, entity_model=None):
        config = _Config(
            config.get("SECRET_KEY"),
            config.get("ENTITY_KEY"),
            config.get("WHITE_LIST_ROUTES"),
            config.get("JWT_ROUTER_API_NAME"),
            entity_model,
        )
        return config

    def init_app(self, app):
        """
        You can use this to set up your config at runtime
        :param app:
        :param kwargs:
        :return:
        """
        self.app = app
        config = self.get_app_config(app)
        self.config = config

    def get_app_config(self, app):
        """
        :param app: Flask Application Instance
        :return: Dict[str, Any]
        """
        config = getattr(app, "config", {})
        return config

    def get_entity_key(self):
        """
        :return: str
        """
        if "ENTITY_KEY" in self.config and self.config["ENTITY_KEY"] is not None:
            return self.config["ENTITY_KEY"]
        else:
            return self.entity_key

    def get_entity_id(self, **kwargs):
        """
        :param kwargs: Dict[str, int]
        :return: str
        """
        try:
            return kwargs['entity_id']
        except KeyError as _:
            return None

    def get_exp(self, **kwargs):
        """
        :param kwargs: Dict[str, int]
        :return: number
        """
        try:
            return kwargs['exp']
        except KeyError as _:
            return 30

    def get_secret_key(self):
        """
        :return: str
        """
        if "SECRET_KEY" in self.config and self.config["SECRET_KEY"] is not None:
            return self.config["SECRET_KEY"]
        else:
            self.logger.warning("Warning: Danger! You have't set a SECRET_KEY in your flask app.config")
            return self.secret_key

    @property
    def auth_model(self):
        return self._auth_model

    @auth_model.setter
    def auth_model(self, value):
        self._auth_model = value

    @staticmethod
    def set_entity_model(model):
        if "entity_model" in model and model["entity_model"] is not None:
            return model["entity_model"]


