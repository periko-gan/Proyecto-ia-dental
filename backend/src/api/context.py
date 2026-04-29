from __future__ import annotations

from dataclasses import dataclass
from strawberry.fastapi import BaseContext

from src.persistence.user_models import UserRecord
from src.services.analysis_service import AnalysisService
from src.services.auth_service import AuthService


@dataclass
class AppContext(BaseContext):
    analysis_service: AnalysisService
    auth_service: AuthService
    current_user: UserRecord | None = None
