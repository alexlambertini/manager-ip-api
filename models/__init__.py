from .group import Group
from .site import Site

# Resolve os forward references dos relacionamentos
Group.update_forward_refs()
Site.update_forward_refs()

__all__ = ["Group", "Site"]
