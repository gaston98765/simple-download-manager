import time


def retry_request(operation, retries=3, delay=2):
    last_error = None

    for attempt in range(retries):
        try:
            return operation()
        except Exception as error:
            last_error = error
            print(f"Attempt {attempt + 1} failed: {error}")

            if attempt < retries - 1:
                time.sleep(delay)

    raise last_error