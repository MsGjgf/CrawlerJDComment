import concurrent.futures
import queue
import threading
import time

import psutil

from utils.custom_logger import logger

names = queue.Queue()


# 下载视频的函数
def download_video(name):
    thread_id = threading.get_ident()
    try:
        print(f"Thread {thread_id} started processing: {name}")
        # 模拟下载过程
        time.sleep(1)
        print(f"Thread {thread_id} finished processing: {name}")
    except Exception as e:
        print(f"Thread {thread_id} error processing {name}: {e}")


# 加法函数
def add_num():
    print('添加')
    global names
    for num in range(40):
        names.put(num)
    time.sleep(20)
    add_num()


# 获取线程池的状态信息
def get_pool_status(executor, futures):
    active_threads = sum(future.running() for future in futures)
    total_threads = len(executor._threads)
    idle_threads = total_threads - active_threads
    work_queue_size = executor._work_queue.qsize()
    return active_threads, idle_threads, work_queue_size


# 创建线程池
def create_thread_pool():
    max_workers = int(psutil.cpu_count(logical=True) * 3 / 2)
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
    return executor


# 开启线程池并执行任务
def start_thread_pool_and_executor_tasks(task_queue, target_method):
    # 1、创建线程池
    global futures
    executor = create_thread_pool()
    # 2、提交任务到线程池
    # futures = [executor.submit(target_method, task_queue.pop()) for _ in task_queue]
    # 3、无限循环查看线程池状态
    try:
        while True:
            # 1、继续提交任务到线程池
            if task_queue.qsize() > 0:
                futures = [executor.submit(target_method, task_queue.get()) for _ in range(task_queue.qsize())]

            # 2、查看线程池状态
            active_threads,idle_threads,work_queue_size = get_pool_status(executor, futures)
            completed_count = sum(future.done() for future in futures)
            total_tasks = len(futures)
            logger.info(
                f"活跃线程数: {active_threads}, 空闲线程数: {idle_threads}, "
                f"任务队列剩余任务: {work_queue_size}, 完成任务数: {completed_count}/{total_tasks}")
            time.sleep(1)  # 每隔一秒更新一次状态信息

            # 如果所有任务都已完成，打印一条消息
            if completed_count == total_tasks:
                logger.info("所有任务已完成")
                final_active_threads, final_idle_threads, final_work_queue_size = get_pool_status(executor, futures)
                logger.info(
                    f"最终状态 - 活跃线程数: {final_active_threads}, 空闲线程数: {final_idle_threads}, "
                    f"任务队列剩余任务: {final_work_queue_size}, 完成任务数: {completed_count}/{total_tasks}")
    except KeyboardInterrupt:
        logger.error("程序被手动中断")

    finally:
        # 关闭线程池
        executor.shutdown(wait=True)


# 主函数
def main():
    for num in range(40):
        names.put(num)

    # 创建一条线程
    thread = threading.Thread(target=add_num)
    thread.start()
    thread = threading.Thread(target=add_num)
    thread.start()
    thread = threading.Thread(target=add_num)
    thread.start()
    thread = threading.Thread(target=add_num)
    thread.start()
    thread = threading.Thread(target=add_num)
    thread.start()
    thread = threading.Thread(target=add_num)
    thread.start()

    # 线程池
    start_thread_pool_and_executor_tasks(names, download_video)


if __name__ == "__main__":
    main()

    q = queue.Queue()
    for i in range(20):
        q.put(i)
    print(q.qsize())