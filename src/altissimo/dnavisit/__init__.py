"""dnavisit-python client."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from altissimo.dnavisit.client import DNAvisitClient, DNAvisitSettings
from altissimo.dnavisit.exceptions import (
    DNAvisitAuthenticationFailedError,
    DNAvisitCallbackEventNotFoundError,
    DNAvisitClientUserNotFoundError,
    DNAvisitOrderConflictError,
    DNAvisitOrderNotFoundError,
    DNAvisitRequestError,
)
from altissimo.dnavisit.types import (
    CHAT_BLURB_CARDIO_NEGATIVE,
    CHAT_BLURB_CARDIO_VUS,
    CHAT_BLURB_HEALTH_NEGATIVE,
    AppointmentStatusEnum,
    DNAvisitBirthSex,
    DNAvisitTestType,
    EnvironmentEnum,
    InsightsStatusEnum,
    InsuranceEnum,
    RelationshipEnum,
    ServiceTypeEnum,
    TestStatusEnum,
    TestTypeEnum,
    YesNoEnum,
)

try:
    __version__ = version("dnavisit-python")
except PackageNotFoundError:  # pragma: no cover — editable install without metadata
    __version__ = "0.1.0"

__all__ = [
    "CHAT_BLURB_CARDIO_NEGATIVE",
    "CHAT_BLURB_CARDIO_VUS",
    "CHAT_BLURB_HEALTH_NEGATIVE",
    "AppointmentStatusEnum",
    "DNAvisitAuthenticationFailedError",
    "DNAvisitBirthSex",
    "DNAvisitCallbackEventNotFoundError",
    "DNAvisitClient",
    "DNAvisitClientUserNotFoundError",
    "DNAvisitOrderConflictError",
    "DNAvisitOrderNotFoundError",
    "DNAvisitRequestError",
    "DNAvisitSettings",
    "DNAvisitTestType",
    "EnvironmentEnum",
    "InsightsStatusEnum",
    "InsuranceEnum",
    "RelationshipEnum",
    "ServiceTypeEnum",
    "TestStatusEnum",
    "TestTypeEnum",
    "YesNoEnum",
    "__version__",
]
