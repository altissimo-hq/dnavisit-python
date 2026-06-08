"""Unit tests for DNAvisit client, settings, and models."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
import requests
from pydantic import ValidationError

from altissimo.dnavisit import (
    DNAvisitAuthenticationFailedError,
    DNAvisitBirthSex,
    DNAvisitClient,
    DNAvisitClientUserNotFoundError,
    DNAvisitRequestError,
    DNAvisitSettings,
    ServiceTypeEnum,
    TestTypeEnum,
)
from altissimo.dnavisit.models import (
    DNAvisitInsightsRequest,
    DNAvisitPostTestRequest,
    DNAvisitPreTestRequest,
    InsightsResponse,
    PatientInfo,
    PostTestResponse,
    PreTestResponse,
)


def test_dnavisit_settings_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test DNAvisitSettings environment variable resolution."""
    monkeypatch.setenv("DNAVISIT_API_KEY", "env-key")
    monkeypatch.setenv("DNAVISIT_PASSWORD", "env-pass")
    monkeypatch.setenv("DNAVISIT_USERNAME", "env-user")
    monkeypatch.setenv("DNAVISIT_BASE_URL", "https://env-url.com")
    monkeypatch.setenv("ENV", "dev")

    settings = DNAvisitSettings.from_env()

    assert settings.api_key == "env-key"
    assert settings.password == "env-pass"
    assert settings.username == "env-user"
    assert settings.base_url == "https://env-url.com"
    assert settings.environment == "test"

    # Test environment mapping to prod
    monkeypatch.setenv("ENV", "prod")
    settings_prod = DNAvisitSettings.from_env()
    assert settings_prod.environment == "prod"


def test_dnavisit_client_ensure_configured() -> None:
    """Test DNAvisitClient raises ValueError when not configured properly."""
    client = DNAvisitClient(DNAvisitSettings(api_key="", password="pass", username="user"))
    with pytest.raises(ValueError, match="DNAVISIT_API_KEY is not set"):
        client._ensure_configured()

    client = DNAvisitClient(DNAvisitSettings(api_key="key", password="", username="user"))
    with pytest.raises(ValueError, match="DNAVISIT_PASSWORD is not set"):
        client._ensure_configured()

    client = DNAvisitClient(DNAvisitSettings(api_key="key", password="pass", username=""))
    with pytest.raises(ValueError, match="DNAVISIT_USERNAME is not set"):
        client._ensure_configured()


@patch("requests.post")
def test_dnavisit_client_authenticate_success(mock_post: MagicMock) -> None:
    """Test successful authentication and token caching."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"apitoken": "token-xyz"}
    mock_post.return_value = mock_response

    settings = DNAvisitSettings(api_key="key", password="pass", username="user")
    client = DNAvisitClient(settings)

    token = client.authenticate()
    assert token == "token-xyz"
    assert client.api_token == "token-xyz"

    # Subsequent auth call should use cached token and not call post again
    assert client.authenticate() == "token-xyz"
    mock_post.assert_called_once()


@patch("requests.post")
def test_dnavisit_client_authenticate_failure(mock_post: MagicMock) -> None:
    """Test authentication raises error when token is missing from response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_post.return_value = mock_response

    settings = DNAvisitSettings(api_key="key", password="pass", username="user")
    client = DNAvisitClient(settings)

    with pytest.raises(DNAvisitAuthenticationFailedError, match=r"Authentication failed\."):
        client.authenticate()


@patch("requests.post")
def test_generate_client_sso_token_success(mock_post: MagicMock) -> None:
    """Test successful SSO token generation."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"token": "sso-token-123"}
    mock_post.return_value = mock_response

    settings = DNAvisitSettings(api_key="key", password="pass", username="user")
    client = DNAvisitClient(settings)

    res = client.generate_client_sso_token("patient@example.com")
    assert res == {"token": "sso-token-123"}
    mock_post.assert_called_once_with(
        "https://www.dnavisit.com/api/1.0/clientlogin/GenerateClientUserSSOToken",
        headers=client.headers,
        json={
            "userName": "user",
            "password": "pass",
            "apiKey": "key",
            "userEmail": "patient@example.com",
        },
        timeout=10,
    )


@patch("requests.post")
def test_generate_client_sso_token_not_found(mock_post: MagicMock) -> None:
    """Test SSO token generation raises error when client user is not found."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = '"Client user not found."'
    # Make raise_for_status raise HTTPError
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Not Found", response=mock_response)
    mock_post.return_value = mock_response

    settings = DNAvisitSettings(api_key="key", password="pass", username="user")
    client = DNAvisitClient(settings)

    with pytest.raises(DNAvisitClientUserNotFoundError, match=r"Client user not found: bad@example\.com"):
        client.generate_client_sso_token("bad@example.com")


@patch("requests.post")
def test_submit_insights_request_success(mock_post: MagicMock) -> None:
    """Test successful insights request submission."""
    # 1. Mock api auth post
    mock_auth_res = MagicMock()
    mock_auth_res.status_code = 200
    mock_auth_res.json.return_value = {"apitoken": "auth-token-123"}

    # 2. Mock submission post
    mock_sub_res = MagicMock()
    mock_sub_res.status_code = 200
    mock_sub_res.json.return_value = {"orderId": "ORD-INSIGHTS"}

    mock_post.side_effect = [mock_auth_res, mock_sub_res]

    settings = DNAvisitSettings(api_key="key", password="pass", username="user", environment="test")
    client = DNAvisitClient(settings)

    body = DNAvisitInsightsRequest(
        patientId="P-1",
        patientFirstName="A",
        patientLastName="B",
        patientDOB="01/01/2000",
        patientEmail="a@example.com",
        patientState="NY",
        patientZip="10001",
        patientBirthSex=DNAvisitBirthSex.FEMALE,
    )

    res = client.submit_insights_request(body)
    assert isinstance(res, InsightsResponse)
    assert res.orderId == "ORD-INSIGHTS"

    # Verify requests called correctly
    assert mock_post.call_count == 2
    _auth_call, sub_call = mock_post.call_args_list

    # Verify insights request payload structure
    sent_payload = sub_call.kwargs["json"]
    assert sent_payload["authToken"] == "auth-token-123"
    assert sent_payload["apikey"] == "key"
    assert sent_payload["targetEnvironment"] == "test"
    assert sent_payload["patientId"] == "P-1"
    assert sent_payload["patientBirthSex"] == "female"


@patch("requests.post")
def test_submit_posttest_request_success(mock_post: MagicMock) -> None:
    """Test successful post-test request submission."""
    mock_auth_res = MagicMock()
    mock_auth_res.status_code = 200
    mock_auth_res.json.return_value = {"apitoken": "auth-token-123"}

    mock_sub_res = MagicMock()
    mock_sub_res.status_code = 200
    mock_sub_res.json.return_value = {"orderId": "ORD-POST"}

    mock_post.side_effect = [mock_auth_res, mock_sub_res]

    settings = DNAvisitSettings(api_key="key", password="pass", username="user", environment="prod")
    client = DNAvisitClient(settings)

    body = DNAvisitPostTestRequest(
        patientId="P-1",
        patientFirstName="A",
        patientLastName="B",
        patientDOB="01/01/2000",
        patientEmail="a@example.com",
        patientState="NY",
        patientZip="10001",
        patientBirthSex=DNAvisitBirthSex.MALE,
        testServiceType=ServiceTypeEnum.POSTTEST,
        testType=TestTypeEnum.CARDIO,
    )

    res = client.submit_posttest_request(body)
    assert isinstance(res, PostTestResponse)
    assert res.orderId == "ORD-POST"

    _auth_call, sub_call = mock_post.call_args_list
    sent_payload = sub_call.kwargs["json"]
    assert sent_payload["authToken"] == "auth-token-123"
    assert sent_payload["targetEnvironment"] == "prod"
    assert sent_payload["testServiceType"] == 1
    assert sent_payload["testType"] == "Cardio"


@patch("requests.post")
def test_submit_pretest_request_success(mock_post: MagicMock) -> None:
    """Test successful pre-test request submission."""
    mock_auth_res = MagicMock()
    mock_auth_res.status_code = 200
    mock_auth_res.json.return_value = {"apitoken": "auth-token-123"}

    mock_sub_res = MagicMock()
    mock_sub_res.status_code = 200
    mock_sub_res.json.return_value = {"orderId": "ORD-PRE"}

    mock_post.side_effect = [mock_auth_res, mock_sub_res]

    settings = DNAvisitSettings(api_key="key", password="pass", username="user", environment="test")
    client = DNAvisitClient(settings)

    body = DNAvisitPreTestRequest(
        patientId="P-1",
        patientFirstName="A",
        patientLastName="B",
        patientDOB="01/01/2000",
        patientEmail="a@example.com",
        patientState="NY",
        patientZip="10001",
        patientBirthSex=DNAvisitBirthSex.MALE,
        testServiceType=ServiceTypeEnum.PRETEST,
        preTestTestType=TestTypeEnum.CARDIO,
    )

    res = client.submit_pretest_request(body)
    assert isinstance(res, PreTestResponse)
    assert res.orderId == "ORD-PRE"

    _auth_call, sub_call = mock_post.call_args_list
    sent_payload = sub_call.kwargs["json"]
    assert sent_payload["authToken"] == "auth-token-123"
    assert sent_payload["targetEnvironment"] == "test"
    assert sent_payload["testServiceType"] == 3
    assert sent_payload["preTestTestType"] == "Cardio"


@patch("requests.post")
def test_submit_request_error_propagation(mock_post: MagicMock) -> None:
    """Test API submission error triggers DNAvisitRequestError."""
    mock_auth_res = MagicMock()
    mock_auth_res.status_code = 200
    mock_auth_res.json.return_value = {"apitoken": "auth-token-123"}

    mock_sub_res = MagicMock()
    mock_sub_res.status_code = 400
    mock_sub_res.json.return_value = {"errorMessage": "Invalid ZIP code"}
    mock_sub_res.raise_for_status.side_effect = requests.exceptions.HTTPError("Bad Request", response=mock_sub_res)

    mock_post.side_effect = [mock_auth_res, mock_sub_res]

    settings = DNAvisitSettings(api_key="key", password="pass", username="user")
    client = DNAvisitClient(settings)

    body = DNAvisitPreTestRequest(
        patientId="P-1",
        patientFirstName="A",
        patientLastName="B",
        patientDOB="01/01/2000",
        patientEmail="a@example.com",
        patientState="NY",
        patientZip="bad-zip",
        patientBirthSex=DNAvisitBirthSex.MALE,
        testServiceType=ServiceTypeEnum.PRETEST,
        preTestTestType=TestTypeEnum.CARDIO,
    )

    with pytest.raises(DNAvisitRequestError, match="400 Invalid ZIP code"):
        client.submit_pretest_request(body)


def test_patient_info_validation() -> None:
    """Test validation and default helper methods on PatientInfo."""
    # 1. Validation error on bad email
    with pytest.raises(ValidationError):
        PatientInfo(
            patientId="P-1",
            patientFirstName="A",
            patientLastName="B",
            patientDOB="01/01/2000",
            patientEmail="not-an-email",
            patientState="NY",
            patientZip="10001",
            patientBirthSex=DNAvisitBirthSex.MALE,
        )

    # 2. Happy path
    patient = PatientInfo(
        patientId="P-1",
        patientFirstName="A",
        patientLastName="B",
        patientDOB="01/01/2000",
        patientEmail="a@example.com",
        patientState="NY",
        patientZip="10001",
        patientBirthSex=DNAvisitBirthSex.OTHER,
    )
    assert patient.patientFirstName == "A"
    assert patient.patientBirthSex.value == "other"
    assert patient.to_patient_info().patientEmail == "a@example.com"
