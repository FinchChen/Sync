# redids

## 1.

redis-benchmark 性能测试,上线之前测试
redis-check-aof / redis-check-rdb 检查修复持久化问题
redis-sentinel 哨兵集群

set mset setnx 
setex 同时设置过期
ttl


./redis-server /home/YifanChen/redismain/redis-5.0.7/redis.conf --loadmodule /home/YifanChen/redisbloom.so INITIAL_SIZE 50000 ERROR_RATE 0.001

dump.rdb这辈子都不能删

save会阻塞 用bgsave异步持久化

aof,rdb记得自定义

r.zcard('Zarten') # zcard统计个数

r.zrank('Zarten','hello') # Zarten表中 hello的索引

r.scan(match='Zar*',count=10) # 用这个不要用key(), 这个不会阻塞但是有可能返回重复的


