"""DNAvisit Base Models."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, EmailStr, Field, Json

from altissimo.dnavisit.types import (
    DNAvisitBirthSex,
    EnvironmentEnum,
    InsuranceEnum,
    RelationshipEnum,
    ServiceTypeEnum,
    TestTypeEnum,
    YesNoEnum,
)


class CriteriaMetDetails(BaseModel):
    """Criteria Met Details."""

    criteriaMet_ACMG_SF: YesNoEnum | None = Field(default=None, alias="criteriaMet_ACMG-SF")
    criteriaMet_Antibiotic_Resistance: YesNoEnum | None = Field(default=None, alias="criteriaMet_Antibiotic Resistance")
    criteriaMet_Baseline: YesNoEnum | None = None
    criteriaMet_Cardio: YesNoEnum | None = None
    criteriaMet_Carrier: YesNoEnum | None = None
    criteriaMet_CGx: YesNoEnum | None = None
    criteriaMet_Cholesterol: YesNoEnum | None = None
    criteriaMet_Diabetes_Obesity: YesNoEnum | None = Field(default=None, alias="criteriaMet_Diabetes-Obesity")
    criteriaMet_FH: YesNoEnum | None = None
    criteriaMet_FSH: YesNoEnum | None = None
    criteriaMet_Genome: YesNoEnum | None = None
    criteriaMet_Hearing_Loss: YesNoEnum | None = Field(default=None, alias="criteriaMet_Hearing Loss")
    criteriaMet_Neuro: YesNoEnum | None = None
    criteriaMet_Other: YesNoEnum | None = None
    criteriaMet_PGx: YesNoEnum | None = None
    criteriaMet_Proactive_Health: YesNoEnum | None = Field(default=None, alias="criteriaMet_Proactive Health")
    criteriaMet_Pulmonary_Respiratory: YesNoEnum | None = Field(default=None, alias="criteriaMet_Pulmonary-Respiratory")
    criteriaMet_Reproductive_Health: YesNoEnum | None = Field(default=None, alias="criteriaMet_Reproductive Health")
    criteriaMet_Testosterone: YesNoEnum | None = None
    criteriaMet_Thyroid: YesNoEnum | None = None
    criteriaMet_VitaminD: YesNoEnum | None = None


class PayerCriteriaMetDetails(BaseModel):
    """Payer Criteria Met Details."""

    payerCriteriaMet_ACMG_SF: YesNoEnum | None = Field(default=None, alias="payerCriteriaMet_ACMG-SF")
    payerCriteriaMet_Antibiotic_Resistance: YesNoEnum | None = Field(
        default=None, alias="payerCriteriaMet_Antibiotic Resistance"
    )
    payerCriteriaMet_Baseline: YesNoEnum | None = None
    payerCriteriaMet_Cardio: YesNoEnum | None = None
    payerCriteriaMet_Carrier: YesNoEnum | None = None
    payerCriteriaMet_CGx: YesNoEnum | None = None
    payerCriteriaMet_Cholesterol: YesNoEnum | None = None
    payerCriteriaMet_Diabetes_Obesity: YesNoEnum | None = Field(default=None, alias="payerCriteriaMet_Diabetes-Obesity")
    payerCriteriaMet_FH: YesNoEnum | None = None
    payerCriteriaMet_FSH: YesNoEnum | None = None
    payerCriteriaMet_Genome: YesNoEnum | None = None
    payerCriteriaMet_Hearing_Loss: YesNoEnum | None = Field(default=None, alias="payerCriteriaMet_Hearing Loss")
    payerCriteriaMet_Neuro: YesNoEnum | None = None
    payerCriteriaMet_Other: YesNoEnum | None = None
    payerCriteriaMet_PGx: YesNoEnum | None = None
    payerCriteriaMet_Proactive_Health: YesNoEnum | None = Field(default=None, alias="payerCriteriaMet_Proactive Health")
    payerCriteriaMet_Pulmonary_Respiratory: YesNoEnum | None = Field(
        default=None, alias="payerCriteriaMet_Pulmonary-Respiratory"
    )
    payerCriteriaMet_Reproductive_Health: YesNoEnum | None = Field(
        default=None, alias="payerCriteriaMet_Reproductive Health"
    )
    payerCriteriaMet_Testosterone: YesNoEnum | None = None
    payerCriteriaMet_Thyroid: YesNoEnum | None = None
    payerCriteriaMet_VitaminD: YesNoEnum | None = None


class BaseRequest(BaseModel):
    """DNAvisit Base Request model."""

    authToken: str
    apikey: str
    targetEnvironment: EnvironmentEnum = EnvironmentEnum.TEST


class PatientInfo(BaseModel):
    """DNAvisit Patient Info model."""

    patientId: str
    patientFirstName: str
    patientLastName: str
    patientDOB: str
    patientEmail: EmailStr
    patientPhone: str | None = None
    patientAddress1: str | None = None
    patientAddress2: str | None = None
    patientCity: str | None = None
    patientState: str
    patientZip: str
    patientCountry: str | None = None
    patientLanguage: str | None = None
    patientBirthSex: DNAvisitBirthSex

    def to_patient_info(self) -> PatientInfo:
        """Return patient Info."""
        return PatientInfo(**self.model_dump())


class PostTestInfo(BaseModel):
    """Post-Test Info model."""

    testServiceType: ServiceTypeEnum
    testType: TestTypeEnum

    iCD10Codes: str | None = None
    isP2P: bool = False
    medications: str | None = None
    orderId: str | None = None
    notes: str | None = None
    rxcui: str | None = None
    postTestIsWebConference: bool = False
    testDate: str | None = None
    testResultsPortalUrl: str | None = None
    shareWithPatient: bool = False
    chatBlurb: str | None = None

    def to_posttest_info(self) -> PostTestInfo | None:
        """Return Post-Test Info."""
        if not self.model_dump(exclude_none=True, exclude_unset=True):
            return None
        return PostTestInfo(**self.model_dump())


class PreTestInfo(BaseModel):
    """Pre-Test Info model."""

    testServiceType: ServiceTypeEnum
    preTestTestType: TestTypeEnum

    otherMetadata: Json[Any] | None = None
    preTestFileName: str | None = None
    preTestFileContentStream: str | None = None
    preTestIsWebConference: bool | None = None
    preTestSupportFile1Name: str | None = None
    preTestSupportFile1ContentStream: str | None = None
    preTestSupportFile2Name: str | None = None
    preTestSupportFile2ContentStream: str | None = None
    preTestPhysicianFileName: str | None = None
    preTestPhysicianFileContentStream: str | None = None

    def to_pretest_info(self) -> PreTestInfo | None:
        """Return Pre-Test Info."""
        if not self.model_dump(exclude_none=True, exclude_unset=True):
            return None
        return PreTestInfo(**self.model_dump())


class ProviderInfo(BaseModel):
    """DNAvisit Provider Info model."""

    providerNPINumber: str | None = None
    providerEmail: EmailStr | None = None
    providerPhone: str | None = None
    providerFax: str | None = None
    providerName: str | None = Field(alias="provider Name", default=None)

    def to_provider_info(self) -> ProviderInfo | None:
        """Return Provider Info."""
        if not self.model_dump(exclude_none=True, exclude_unset=True):
            return None
        return ProviderInfo(**self.model_dump())


class PrimaryInsuranceInfo(BaseModel):
    """DNAvisit Primary Insurance Info model."""

    primaryInsurance: InsuranceEnum | None = None
    insurancePolicyNumber: str | None = None
    insuranceGroupNumber: str | None = None
    insuranceSubscriberFirstname: str | None = None
    insuranceSubscriberLastname: str | None = None
    insuranceSubscriberDOB: str | None = None

    def to_primary_insurance_info(self) -> PrimaryInsuranceInfo | None:
        """Return Primary Insurance Info."""
        if not self.model_dump(exclude_none=True, exclude_unset=True):
            return None
        return PrimaryInsuranceInfo(**self.model_dump())


class SecondaryIndividual(BaseModel):
    """DNAvisit Secondary Individual model."""

    secondaryIndPatientId: str | None = None
    secondaryIndFirstname: str | None = None
    secondaryIndLastname: str | None = None
    secondaryIndPhone: str | None = None
    secondaryIndRelationship: RelationshipEnum | None = None

    def to_secondary_individual_info(self) -> SecondaryIndividual | None:
        """Return Secondary Individual Info."""
        if not self.model_dump(exclude_none=True, exclude_unset=True):
            return None
        return SecondaryIndividual(**self.model_dump())


class SecondaryInsuranceInfo(BaseModel):
    """DNAvisit Secondary Insurance Info model."""

    secondaryInsurance: InsuranceEnum | None = None
    insurancePolicyNumber2: str | None = None
    insuranceGroupNumber2: str | None = None
    insuranceSubscriberFirstname2: str | None = None
    insuranceSubscriberLastname2: str | None = None
    insuranceSubscriberDOB2: str | None = None

    def to_secondary_insurance_info(self) -> SecondaryInsuranceInfo | None:
        """Return Secondary Insurance Info."""
        if not self.model_dump(exclude_none=True, exclude_unset=True):
            return None
        return SecondaryInsuranceInfo(**self.model_dump())


class SupportFiles(BaseModel):
    """Support Files model."""

    supportFile1Name: str | None = None
    supportFile1ContentStream: str | None = None
    supportFile2Name: str | None = None
    supportFile2ContentStream: str | None = None
    supportFile3Name: str | None = None
    supportFile3ContentStream: str | None = None
    rawReportFileName: str | None = None
    rawReportFileContentStream: str | None = None

    def to_support_files(self) -> SupportFiles | None:
        """Return Support Files."""
        if not self.model_dump(exclude_none=True, exclude_unset=True):
            return None
        return SupportFiles(**self.model_dump())


class TestReportFiles(BaseModel):
    """Test Report Files model."""

    testReportFileName: str | None = None
    testReportFileContentStream: str | None = None
    testReportFile2Name: str | None = None
    testReportFile2ContentStream: str | None = None
    testReportFile3Name: str | None = None
    testReportFile3ContentStream: str | None = None
    testReportFile4Name: str | None = None
    testReportFile4ContentStream: str | None = None

    def to_test_report_files(self) -> TestReportFiles | None:
        """Return Test Report Files."""
        if not self.model_dump(exclude_none=True, exclude_unset=True):
            return None
        return TestReportFiles(**self.model_dump())
