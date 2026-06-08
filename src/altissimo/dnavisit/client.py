"""DNAvisit Client class."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import requests

from altissimo.dnavisit.exceptions import (
    DNAvisitAuthenticationFailedError,
    DNAvisitClientUserNotFoundError,
    DNAvisitRequestError,
)
from altissimo.dnavisit.models import (
    AuthenticationRequest,
    DNAvisitInsightsRequest,
    DNAvisitPostTestRequest,
    DNAvisitPreTestRequest,
    GenerateClientUserSSOTokenRequest,
    InsightsRequest,
    InsightsResponse,
    PostTestRequest,
    PostTestResponse,
    PreTestRequest,
    PreTestResponse,
)
from altissimo.dnavisit.types import EnvironmentEnum


@dataclass(frozen=True)
class DNAvisitSettings:
    """Settings for DNAvisit client."""

    api_key: str
    password: str
    username: str
    base_url: str = "https://www.dnavisit.com/api/1.0"
    environment: str = "test"

    @classmethod
    def from_env(
        cls,
        *,
        api_key_env: str = "DNAVISIT_API_KEY",
        password_env: str = "DNAVISIT_PASSWORD",  # noqa: S107
        username_env: str = "DNAVISIT_USERNAME",
        base_url_env: str = "DNAVISIT_BASE_URL",
        environment_env: str = "ENV",
    ) -> DNAvisitSettings:
        """Build settings from environment variables."""
        api_key = os.environ.get(api_key_env, "")
        password = os.environ.get(password_env, "")
        username = os.environ.get(username_env, "everygenegc")
        base_url = os.environ.get(base_url_env, "https://www.dnavisit.com/api/1.0")
        env_val = os.environ.get(environment_env, "dev")

        environment = "prod" if env_val == "prod" else "test"

        return cls(
            api_key=api_key,
            password=password,
            username=username,
            base_url=base_url,
            environment=environment,
        )


class DNAvisitClient:
    """DNAvisit API Client class."""

    def __init__(self, settings: DNAvisitSettings | None = None) -> None:
        """Initialize a DNAvisitClient instance."""
        self._settings = settings
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self.api_token: str | None = None

    def _get_settings(self) -> DNAvisitSettings:
        if self._settings is None:
            self._settings = DNAvisitSettings.from_env()
        return self._settings

    def _ensure_configured(self) -> None:
        """Validate that all required environment variables are set."""
        settings = self._get_settings()
        if not settings.api_key:
            raise ValueError("DNAVISIT_API_KEY is not set")
        if not settings.password:
            raise ValueError("DNAVISIT_PASSWORD is not set")
        if not settings.username:
            raise ValueError("DNAVISIT_USERNAME is not set")
        if not settings.base_url:
            raise ValueError("DNAVISIT_BASE_URL is not set")

    def __post_request(self, path: str, data: dict[str, Any], timeout: int = 10) -> dict[str, Any]:
        """Submit a POST request to DNAvisit."""
        settings = self._get_settings()
        url = f"{settings.base_url}/{path}"
        response = requests.post(url, headers=self.headers, json=data, timeout=timeout)
        response.raise_for_status()
        return response.json()  # type: ignore[no-any-return]

    #
    # Authentication methods
    #
    def authenticate(self) -> str:
        """Authenticate to DNAvisit API."""
        if not self.api_token:
            self.api_token = self.create_api_token()
        return self.api_token

    def create_api_token(self) -> str:
        """Authenticate to DNAvisit API."""
        self._ensure_configured()
        settings = self._get_settings()
        path = "clientlogin/apiauthenticate"
        data = AuthenticationRequest(
            username=settings.username,
            password=settings.password,
            apikey=settings.api_key,
        ).model_dump()
        response = self.__post_request(path, data)
        api_token = response.get("apitoken")
        if not api_token or not isinstance(api_token, str):
            raise DNAvisitAuthenticationFailedError("Authentication failed.")
        self.api_token = api_token
        return api_token

    def generate_client_sso_token(self, email: str) -> dict[str, Any]:
        """Generate a client SSO token."""
        self._ensure_configured()
        settings = self._get_settings()
        url = f"{settings.base_url}/clientlogin/GenerateClientUserSSOToken"
        data = GenerateClientUserSSOTokenRequest(
            userName=settings.username,
            password=settings.password,
            apiKey=settings.api_key,
            userEmail=email,
        ).model_dump()
        response = requests.post(url, headers=self.headers, json=data, timeout=10)
        try:
            response.raise_for_status()
            return response.json()  # type: ignore[no-any-return]
        except requests.exceptions.HTTPError as e:
            if response.text == '"Client user not found."':
                raise DNAvisitClientUserNotFoundError(f"Client user not found: {email}") from e
            raise e

    #
    # Submitting to DNAvisit
    #
    def submit_insights_request(self, body: DNAvisitInsightsRequest) -> InsightsResponse:
        """Create a new Insights Request."""
        self._ensure_configured()
        settings = self._get_settings()
        auth_token = self.authenticate()
        url = f"{settings.base_url}/insights/request/"
        target_env = EnvironmentEnum.PROD if settings.environment == "prod" else EnvironmentEnum.TEST
        data = InsightsRequest(
            authToken=auth_token,
            apikey=settings.api_key,
            targetEnvironment=target_env,
            **body.model_dump(),
        ).model_dump()
        response = requests.post(url, headers=self.headers, json=data, timeout=10)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                detail = response.json().get("errorMessage", str(e))
            except Exception:
                detail = str(e)
            raise DNAvisitRequestError(f"{response.status_code} {detail}") from e
        return InsightsResponse(**response.json())

    def submit_posttest_request(self, body: DNAvisitPostTestRequest) -> PostTestResponse:
        """Create a new Post-Test Request."""
        self._ensure_configured()
        settings = self._get_settings()
        auth_token = self.authenticate()
        url = f"{settings.base_url}/clientportal/submitpatientposttest/"
        target_env = EnvironmentEnum.PROD if settings.environment == "prod" else EnvironmentEnum.TEST
        data = PostTestRequest(
            authToken=auth_token,
            apikey=settings.api_key,
            targetEnvironment=target_env,
            **body.model_dump(exclude_none=True),
        ).model_dump(exclude_none=True)
        response = requests.post(url, headers=self.headers, json=data, timeout=10)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                detail = response.json().get("errorMessage", str(e))
            except Exception:
                detail = str(e)
            raise DNAvisitRequestError(f"{response.status_code} {detail}") from e
        return PostTestResponse(**response.json())

    def submit_pretest_request(self, body: DNAvisitPreTestRequest) -> PreTestResponse:
        """Create a new Pre-Test Request."""
        self._ensure_configured()
        settings = self._get_settings()
        auth_token = self.authenticate()
        url = f"{settings.base_url}/clientportal/submitpatientpretest/"
        target_env = EnvironmentEnum.PROD if settings.environment == "prod" else EnvironmentEnum.TEST
        data = PreTestRequest(
            authToken=auth_token,
            apikey=settings.api_key,
            targetEnvironment=target_env,
            **body.model_dump(),
        ).model_dump()
        response = requests.post(url, headers=self.headers, json=data, timeout=10)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                detail = response.json().get("errorMessage", str(e))
            except Exception:
                detail = str(e)
            raise DNAvisitRequestError(f"{response.status_code} {detail}") from e
        return PreTestResponse(**response.json())
