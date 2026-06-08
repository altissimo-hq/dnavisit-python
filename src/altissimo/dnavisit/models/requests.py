"""DNAvisit Requests Models."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from altissimo.dnavisit.types import ServiceTypeEnum, TestTypeEnum, YesNoEnum


class PatientInsightsRequest(BaseModel):
    """Patient Insights Request model."""


class PatientInsightsResponse(BaseModel):
    """Patient Insights Response model."""

    order_id: str
    model_config = ConfigDict(extra="allow")


class PatientInternalMessageRequest(BaseModel):
    """Patient Internal Message Request model."""

    criteria_met: YesNoEnum
    other_metadata: dict[str, str] = {}


class PatientInternalMessageResponse(BaseModel):
    """Patient Internal Message Response model."""

    model_config = ConfigDict(extra="allow")


class PatientPostTestRequest(BaseModel):
    """Patient Post-Test Request model."""

    service_type: Literal[ServiceTypeEnum.POSTTEST, ServiceTypeEnum.POSTTESTPLUS] = Field(
        default=ServiceTypeEnum.POSTTEST,
        description="1: Post-Test with Approval Only, 2: Post-Test with Proactive Call",
    )
    test_type: TestTypeEnum
    order_id: str | None = None
    test_file_name: str
    test_file_content_stream: str
    test_file2_name: str | None = None
    test_file2_content_stream: str | None = None
    notes: str | None = None
    shareWithPatient: bool = False
    chatBlurb: str | None = None


class PatientPostTestResponse(BaseModel):
    """Patient Post-Test Response model."""

    order_id: str
    model_config = ConfigDict(extra="allow")


class PatientPreTestRequest(BaseModel):
    """Patient Pre-Test Request model."""

    service_type: Literal[ServiceTypeEnum.PRETEST, ServiceTypeEnum.PRETESTPLUS] = Field(
        default=ServiceTypeEnum.PRETEST,
        description="3: Pre-Test with Approval Only, 4: Pre-Test with Proactive Call",
    )
    test_type: TestTypeEnum


class PatientPreTestResponse(BaseModel):
    """Patient Pre-Test Response model."""

    order_id: str
    model_config = ConfigDict(extra="allow")
