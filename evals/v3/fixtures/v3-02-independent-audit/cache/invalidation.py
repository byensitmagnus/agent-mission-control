def invalidate_tenant(keys: list[str], tenant: str) -> list[str]:
    return [key for key in keys if not key.startswith(tenant)]
