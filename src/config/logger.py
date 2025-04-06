import logging


class LoggerConfig:
    LOG_FORMAT = "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"

    @staticmethod
    def init_logger(app, log_level: str = "INFO"):
        if app.logger.hasHandlers():
            app.logger.handlers.clear()

        log_formatter = logging.Formatter(LoggerConfig.LOG_FORMAT)

        app.logger.setLevel(log_level)

        # Logs to stdout
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(log_formatter)
        app.logger.addHandler(console_handler)