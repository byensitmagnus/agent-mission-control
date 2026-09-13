"""Decide whether the required release checks have actually passed."""


def release_ready(required, results):
    return all(row.get("status") == "PASS" for row in results)
