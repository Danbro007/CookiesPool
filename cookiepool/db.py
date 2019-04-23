from redis import StrictRedis
from cookiepool.settings import *
from random import choice


class RedisClient:
    def __init__(self, type, website, port=REDIS_PORT, host=REDIS_HOST, password=REDIS_PASSWORD):
        self.redis = StrictRedis(host=host, port=port, password=password, decode_responses=True)
        self.type = type
        self.website = website

    def name(self):
        return "{type}:{website}".format(type=self.type, website=self.website)

    def set(self, username, value):
        return self.redis.hset(self.name(), username, value)

    def get(self, username):
        return self.redis.hget(self.name(), username)

    def delete(self, username):
        return self.redis.hdel(self.name(), username)

    def count(self):
        return self.redis.hlen(self.name())

    def random(self):
        return choice(self.redis.hvals(self.name()))

    def usernames(self):
        return self.redis.hkeys(self.name())

    def all(self):
        return self.redis.hgetall(self.name())
if __name__ == '__main__':
    print(REDIS_PORT)