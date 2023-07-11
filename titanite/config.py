
from loguru import logger
from pydantic import BaseModel


class Config(BaseModel):
    id: int
    name: str
    email: str


if __name__ == "__main__":

    config_data = {
        "id": 1,
        "name": "John Doe",
        "email": "johndoe@example.com"
    }

    config = Config(**config_data)
    logger.debug(config.id)
    logger.debug(config.name)
    logger.debug(config.email)