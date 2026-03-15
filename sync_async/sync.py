import time


def fetch_data(task_id):
    print(f"start task {task_id}")
    time.sleep(2)
    print(f"End task {task_id}")
    return f"data {task_id}"


def main():
    start = time.time()
    results = []

    for i in range(5):
        results.append(fetch_data(i))
    
    print(results)

    print(f"Time taken: {time.time() - start}")

main()