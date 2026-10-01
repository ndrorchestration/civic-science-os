from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, HttpUrl, model_validator

class ClaimStatus(str, Enum):
    OBSERVED = "OBSERVED"
    SUPPORTED = "SUPPORTED"
    INFERRED = "INFERRED"
    UNKNOWN = "UNKNOWN"

class AmbiguityCode(str, Enum):
    LOW_SIGNAL = "LOW_SIGNAL"
    STELLAR_VARIABILITY = "STELLAR_VARIABILITY"
    EDGE_EVENT = "EDGE_EVENT"
    MULTIPLE_CANDIDATES = "MULTIPLE_CANDIDATES"
    DATA_GAP_OR_ARTIFACT = "DATA_GAP_OR_ARTIFACT"
    TUTORIAL_RULE_UNCERTAINTY = "TUTORIAL_RULE_UNCERTAINTY"
    SIMULATION_FEEDBACK = "SIMULATION_FEEDBACK"
    OTHER = "OTHER"

class SessionRecord(BaseModel):
    schema_version: str = "0.1.0"
    session_id: UUID = Field(default_factory=uuid4)
    started_at: datetime
    ended_at: datetime
    recorded_at: datetime = Field(default_factory=lambda: datetime.now().astimezone())
    ecosystem: str
    project: str
    project_url: HttpUrl
    workflow: Optional[str] = None
    instruction_sources: list[HttpUrl]
    classification_mode: str = "HUMAN_ONLY"
    ai_assistance_during_classification: bool = False
    classifications_completed: Optional[int] = Field(default=None, ge=0)
    uncertainty_notes: str = ""
    ambiguity_codes: list[AmbiguityCode] = []
    procedural_friction: list[str] = []
    learning_notes: str = ""
    claim_status: ClaimStatus = ClaimStatus.OBSERVED
    follow_up: str = ""

    @property
    def duration_minutes(self) -> float:
        return round((self.ended_at - self.started_at).total_seconds() / 60.0, 2)

    @model_validator(mode="after")
    def validate_boundaries(self):
        if self.started_at.tzinfo is None or self.started_at.utcoffset() is None:
            raise ValueError("started_at must be timezone-aware")
        if self.ended_at.tzinfo is None or self.ended_at.utcoffset() is None:
            raise ValueError("ended_at must be timezone-aware")
        if self.ended_at < self.started_at:
            raise ValueError("ended_at must be >= started_at")
        if not self.instruction_sources:
            raise ValueError("at least one instruction source is required")
        if self.classification_mode == "HUMAN_ONLY" and self.ai_assistance_during_classification:
            raise ValueError("HUMAN_ONLY requires ai_assistance_during_classification=false")
        if self.project.strip().lower() == "planet hunters tess":
            if self.classification_mode != "HUMAN_ONLY" or self.ai_assistance_during_classification:
                raise ValueError("Planet Hunters TESS pilot requires HUMAN_ONLY with no AI classification assistance")
        return self
