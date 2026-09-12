from cache.invalidation import invalidate_tenant


assert invalidate_tenant(["acme:user:1", "acme2:user:2"], "acme") == ["acme2:user:2"]
