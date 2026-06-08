"""DNAvisit Types and Enums."""

from __future__ import annotations

from enum import Enum, StrEnum


class DNAvisitBirthSex(StrEnum):
    """Birth sex values accepted by the DNAvisit API."""

    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class AppointmentStatusEnum(StrEnum):
    """Appointment Status Enum."""

    SCHEDULED = "scheduled"
    RESCHEDULED = "rescheduled"
    CANCELLED = "cancelled"


class EnvironmentEnum(StrEnum):
    """Environment Enum."""

    PROD = "prod"
    TEST = "test"


class InsuranceEnum(StrEnum):
    """Insurance Enum."""

    AETNA = "Aetna"
    AETNA_OPEN = "Aetna Open"
    AMBETTER = "Ambetter"
    ANTHEM_BCBS = "Anthem (BCBS)"
    AVMED = "AVMED"
    BCBS = "BCBS"
    CAREFIRST = "Carefirst"
    CAREPLUS_HEALTH = "Careplus Health"
    CAYMAN = "Cayman"
    CENTENE = "Centene"
    CIGNA = "Cigna"
    COVENTRY = "Coventry"
    CYPRESS = "Cypress"
    GOLDEN_RULE_INSURANCE = "Golden Rule Insurance"
    HCSC = "HCSC"
    HEALTH_NET_OF_CALIFORNIA = "Health Net of California"
    HIGHMARK = "Highmark"
    HUMANA = "Humana"
    INDEPENDENCE_BLUE_CROSS = "Independence Blue Cross"
    MEDICAID_HUMANA = "Medicaid - Humana"
    MEDICAID_SIMPLY_HEALTHCARE = "Medicaid - Simply Healthcare"
    MEDICAID_STAYWELL = "Medicaid - Staywell"
    MEDICAID_UNITED_HEALTHCARE = "Medicaid - United Healthcare"
    MEDICAID_VIVIDA_HEALTH = "Medicaid - Vivida Health"
    MEDICARE = "Medicare"
    MEDICARE_HUMANA = "Medicare - Humana"
    MEDICARE_MEDICA = "Medicare - Medica"
    MEMORIAL_INTEGRATED_HEALTHCARE = "Memorial Integrated Healthcare"
    MOLINA = "Molina"
    PRESTIGE = "Prestige"
    STAYWELL = "Staywell"
    SUNSHINE_STATE_HEALTH_PLAN = "Sunshine State Health Plan"
    TRICARE = "Tricare"
    UMR = "UMR"
    UNITED_HEALTHCARE = "United Healthcare"
    WELLCARE = "Wellcare"
    WELLPOINT = "Wellpoint"
    OTHER = "Other"


class RelationshipEnum(StrEnum):
    """Relationship Enum."""

    GUARDIAN = "Guardian"
    CAREGIVER = "Caregiver"
    PARTNER = "Partner"


class ServiceTypeEnum(int, Enum):
    """Service Type Enum."""

    POSTTEST = 1
    POSTTESTPLUS = 2
    PRETEST = 3
    PRETESTPLUS = 4


class InsightsStatusEnum(StrEnum):
    """Insights Status Enum model."""

    IN_PROGRESS = "In-progress"
    COMPLETE = "Complete"


class TestStatusEnum(StrEnum):
    """Test Status Enum model."""

    IN_PROGRESS = "In-progress"
    COMPLETE = "Complete"
    NOT_REACHABLE = "Not reachable"


class TestTypeEnum(StrEnum):
    """Canonical outbound test types — values we SEND to DNAvisit."""

    __test__ = False

    ACMG_SF = "ACMG-SF"
    ANTIBIOTIC = "Antibiotic"
    CARDIO = "Cardio"
    CARRIER = "Carrier"
    CGX = "CGx"
    CHOLESTEROL = "Cholesterol"
    DIABETES_OBESITY = "Diabetes-Obesity"
    FH = "FH"
    FSH = "FSH"
    GENERAL = "General"
    GENOME = "Genome"
    HEALTH = "Health"
    HEARING_LOSS = "Hearing-Loss"
    IMMUNODEFICIENCY = "Immunodeficiency"
    NEURO = "Neuro"
    OTHER = "Other"
    PGX = "PGx"
    PROACTIVE_HEALTH = "Proactive Health"
    PULMONARY = "Pulmonary"
    REPRODUCTIVE = "Reproductive"
    TESTOSTERONE = "Testosterone"
    THYROID = "Thyroid"
    VITAMIND = "VitaminD"


# Flexible type alias for test_type values received FROM DNAvisit.
DNAvisitTestType = str


class YesNoEnum(StrEnum):
    """Yes/No/- Enum."""

    YES = "Yes"
    NO = "No"
    UNANSWERED = "-"


# Chat blurb IDs
CHAT_BLURB_HEALTH_NEGATIVE = "6811b4bae17aa2078f9a2d6a"
CHAT_BLURB_CARDIO_NEGATIVE = "69c34c38e17a555609bd0ea6"
CHAT_BLURB_CARDIO_VUS = "69c34c75e17a555609bd0eac"
