import time
import threading
import redis

class RedisBenchmarker:
    def __init__(self, host='localhost', port=6379, db=0, password=None):
        # 使用连接池提高效率
        self.pool = redis.ConnectionPool(
            host=host, port=port, db=db, password=password, decode_responses=True
        )
        self.results = []
        self.errors = 0

    def _worker(self, num_requests, payload_size):
        r = redis.Redis(connection_pool=self.pool)
        for i in range(num_requests):
            key = f"perf:test:{threading.get_ident()}:{i}"
            value = "x" * payload_size
            start = time.perf_counter()
            try:
                r.set(key, value)
                latency = time.perf_counter() - start
                self.results.append(latency)
            except Exception:
                self.errors += 1

    def run_benchmark(self, total_requests=1000, concurrent_threads=10, payload_size=100):
        self.results = []
        self.errors = 0
        req_per_thread = total_requests // concurrent_threads
        
        threads = []
        start_time = time.perf_counter()
        
        for _ in range(concurrent_threads):
            t = threading.Thread(target=self._worker, args=(req_per_thread, payload_size))
            threads.append(t)
            t.start()
            
        for t in threads:
            t.join()
            
        end_time = time.perf_counter() - start_time
        
        # 计算指标
        total_success = len(self.results)
        tps = total_success / end_time
        error_rate = (self.errors / total_requests) * 100
        avg_latency = sum(self.results) / total_success if total_success > 0 else 0
        
        return {
            "tps": round(tps, 2),
            "error_rate": f"{error_rate}%",
            "avg_latency_ms": round(avg_latency * 1000, 4),
            "total_time": round(end_time, 2)
        }