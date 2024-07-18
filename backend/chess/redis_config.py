import redis

REDIS_HOST = 'redis'
REDIS_PORT = 6379
REDIS_DB = 0

def get_redis_connection():
    return redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)