"""DNAvisit API Models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from altissimo.dnavisit.models.base import (
    BaseRequest,
    PatientInfo,
    PostTestInfo,
    PreTestInfo,
    PrimaryInsuranceInfo,
    ProviderInfo,
    SecondaryIndividual,
    SecondaryInsuranceInfo,
    SupportFiles,
    TestReportFiles,
)


class AuthenticationRequest(BaseModel):
    """DNAvisit Authentication Request model."""

    username: str
    password: str
    apikey: str


class GenerateClientUserSSOTokenRequest(BaseModel):
    """DNAvisit Generate Client User SSO Token Request model."""

    userName: str
    password: str
    apiKey: str
    userEmail: str


class DNAvisitInsightsRequest(SecondaryInsuranceInfo, PrimaryInsuranceInfo, ProviderInfo, PatientInfo):
    """DNAvisit Insights Request."""


class InsightsRequest(DNAvisitInsightsRequest, BaseRequest):
    """DNAvisit Insights Request."""


class InsightsResponse(BaseModel):
    """Insights Response model."""

    orderId: str
    model_config = ConfigDict(extra="allow")


class DNAvisitPostTestRequest(
    SupportFiles,
    TestReportFiles,
    SecondaryIndividual,
    SecondaryInsuranceInfo,
    PrimaryInsuranceInfo,
    ProviderInfo,
    PatientInfo,
    PostTestInfo,
):
    """DNAvisit Post-Test Request."""


class PostTestRequest(DNAvisitPostTestRequest, BaseRequest):
    """DNAvisit Post-Test Request."""


class PostTestResponse(BaseModel):
    """Post-Test Response model."""

    orderId: str
    model_config = ConfigDict(extra="allow")


class DNAvisitPreTestRequest(
    SecondaryIndividual,
    SecondaryInsuranceInfo,
    PrimaryInsuranceInfo,
    ProviderInfo,
    PatientInfo,
    PreTestInfo,
):
    """DNAvisit Pre-Test Request."""


class PreTestRequest(DNAvisitPreTestRequest, BaseRequest):
    """DNAvisit Pre-Test Request."""


class PreTestResponse(BaseModel):
    """Pre-Test Response model."""

    orderId: str
    model_config = ConfigDict(extra="allow")
