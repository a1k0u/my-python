import math
import os
import concurrent.futures
import time
import functools


def __wrapper(f, a, b, n_jobs, n_iter):
    print(f"RUN({n_jobs=}): [{a}, {b}]")
    acc = 0
    n_iter = n_iter // n_jobs
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


def integrate(f, a, b, *, n_jobs=1, n_iter=10000000):
    step = b / n_jobs
    start = a
    while start < b:
        yield functools.partial(__wrapper, f, start, start + step, n_jobs, n_iter)
        start += step


artifact = open("4_2.txt", "w")

for n_jobs in range(1, os.cpu_count() * 2 + 1):
    def run_pool(pool, pool_name):
        with pool(max_workers=n_jobs) as executor:
            time_start = time.time()
            futures = [executor.submit(work) for work in integrate(math.cos, 0, math.pi / 2, n_jobs=n_jobs)]
            result = sum([future.result() for future in concurrent.futures.as_completed(futures)])
            time_end = time.time()

            print(f"{pool_name:19}: {n_jobs=:2} {result=} duration={time_end - time_start}", file=artifact)
        print(f"Finish {pool_name} with {n_jobs=}")

    run_pool(concurrent.futures.ThreadPoolExecutor, "ThreadPoolExecutor")
    run_pool(concurrent.futures.ProcessPoolExecutor, "ProcessPoolExecutor")
    print(file=artifact)

artifact.close()
