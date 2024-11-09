from sqlalchemy import create_engine
from omegaconf import DictConfig


def new(database_config: DictConfig):
    url_conn = "{}:{}@{}({}:{})/{}".format(database_config.user,
                                           database_config.password,
                                           database_config.protocol,
                                           database_config.host,
                                           database_config.port,
                                           database_config.name_db)
    engine = create_engine(url_conn, echo=True)

    return engine
