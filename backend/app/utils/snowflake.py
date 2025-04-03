import time
import threading

# 64位ID的划分
WORKER_ID_BITS = 5
DATACENTER_ID_BITS = 5
SEQUENCE_BITS = 12

# 最大取值
MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)  # 31
MAX_DATACENTER_ID = -1 ^ (-1 << DATACENTER_ID_BITS)  # 31

# 移位偏移量
WORKER_ID_SHIFT = SEQUENCE_BITS
DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS

# 序列号掩码
SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)  # 4095

# 开始时间戳 (2023-01-01 00:00:00 UTC)
TWEPOCH = 1672531200000


class IdWorker:
    """
    雪花算法ID生成器
    """
    def __init__(self, worker_id=0, datacenter_id=0):
        """
        初始化
        :param worker_id: 工作机器ID
        :param datacenter_id: 数据中心ID
        """
        # 工作机器ID和数据中心ID的合法性判断
        if worker_id > MAX_WORKER_ID or worker_id < 0:
            raise ValueError(f"worker_id不能大于{MAX_WORKER_ID}或小于0")
        if datacenter_id > MAX_DATACENTER_ID or datacenter_id < 0:
            raise ValueError(f"datacenter_id不能大于{MAX_DATACENTER_ID}或小于0")
            
        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = 0
        self.last_timestamp = -1
        self.lock = threading.Lock()
    
    def _gen_timestamp(self):
        """
        生成整数时间戳
        :return: 时间戳 (毫秒)
        """
        return int(time.time() * 1000)
    
    def _wait_next_millis(self, last_timestamp):
        """
        等到下一个毫秒
        """
        timestamp = self._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._gen_timestamp()
        return timestamp
    
    def next_id(self):
        """
        生成下一个ID
        """
        with self.lock:
            timestamp = self._gen_timestamp()
            
            # 如果当前时间小于上一次ID生成的时间戳，说明系统时钟回退过这个时候应当抛出异常
            if timestamp < self.last_timestamp:
                raise ValueError(f"时钟向后移动。拒绝生成ID，直到{self.last_timestamp}。")
            
            if timestamp == self.last_timestamp:
                # 同一时间生成的，则进行毫秒内序列号递增
                self.sequence = (self.sequence + 1) & SEQUENCE_MASK
                # 毫秒内序列溢出
                if self.sequence == 0:
                    # 阻塞到下一个毫秒，获得新的时间戳
                    timestamp = self._wait_next_millis(self.last_timestamp)
            else:
                # 时间戳改变，毫秒内序列重置
                self.sequence = 0
            
            self.last_timestamp = timestamp
            
            # 返回雪花ID
            return ((timestamp - TWEPOCH) << TIMESTAMP_LEFT_SHIFT) | \
                   (self.datacenter_id << DATACENTER_ID_SHIFT) | \
                   (self.worker_id << WORKER_ID_SHIFT) | \
                   self.sequence


# 单例模式，全局唯一ID生成器实例
id_worker = IdWorker(worker_id=1, datacenter_id=1) 