from __future__ import annotations

import strawberry

from src.api.mutations import Mutation
from src.api.queries import Query

schema = strawberry.Schema(query=Query, mutation=Mutation)
