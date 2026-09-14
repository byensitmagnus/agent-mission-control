# planted: retries ignore 429
def should_retry(status):
    return status >= 500
