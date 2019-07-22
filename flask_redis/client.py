try:
    import redis
    from redis.sentinel import Sentinel
except ImportError:
    # We can still allow custom provider-only usage without redis-py being installed
    redis = None


class FlaskRedis(object):
    def __init__(self, app=None, strict=True, config_prefix="REDIS", **kwargs):
        self._redis_client = None
        self.provider_class = redis.StrictRedis if strict else redis.Redis
        self.provider_kwargs = kwargs
        self.config_prefix = config_prefix

        if app is not None:
            self.init_app(app)
            self._app = app

    @classmethod
    def from_custom_provider(cls, provider, app=None, **kwargs):
        assert provider is not None, "your custom provider is None, come on"

        # We never pass the app parameter here, so we can call init_app
        # ourselves later, after the provider class has been set
        instance = cls(**kwargs)

        instance.provider_class = provider
        if app is not None:
            instance.init_app(app)
            instance._app = app
        return instance

    def init_app(self, app, **kwargs):
        self._app = app
        redis_url = app.config.get(
            "{0}_URL".format(self.config_prefix), "redis://localhost:6379/0"
        )

        self.reconnect(redis_url, **kwargs)

        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions[self.config_prefix.lower()] = self

    def reconnect(self, redis_url=None, **kwargs):
        self.provider_kwargs.update(kwargs)

        if self._app.config.get('{0}_SENTINEL_URL'.format(self.config_prefix)):
            if not hasattr(self, '_redis_sentinel'):
                self._redis_sentinel = Sentinel(
                    self._app.config.get('{0}_SENTINEL_URL'.format(self.config_prefix)),
                    socket_timeout=self._app.config.get(
                        '{0}_SENTINEL_TIMEOUT'.format(self.config_prefix), 0.1
                    )
                )

            self._redis_client = self._redis_sentinel.master_for(
                self._app.config.get('{0}_SENTINEL_MASTER'.format(self.config_prefix)),
                **self.provider_kwargs,
            )
        else:
            self._redis_client = self.provider_class.from_url(
                redis_url, **self.provider_kwargs
            )

    def __getattr__(self, name):
        return getattr(self._redis_client, name)

    def __getitem__(self, name):
        return self._redis_client[name]

    def __setitem__(self, name, value):
        self._redis_client[name] = value

    def __delitem__(self, name):
        del self._redis_client[name]
