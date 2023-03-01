import config
from redis import Redis

redis_client = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)
