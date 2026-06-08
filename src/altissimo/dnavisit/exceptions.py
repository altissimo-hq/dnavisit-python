"""DNAvisit exceptions."""

from __future__ import annotations


class DNAvisitAuthenticationFailedError(Exception):
    """Raised when DNAvisit Authentication fails."""


class DNAvisitClientUserNotFoundError(Exception):
    """Raised when a DNAvisit User is not found."""


class DNAvisitOrderConflictError(Exception):
    """Raised when a DNAvisit Order already exists."""


class DNAvisitCallbackEventNotFoundError(Exception):
    """Raised when a DNAvisit Callback Event is not found."""


class DNAvisitOrderNotFoundError(Exception):
    """Raised when a DNAvisit Order is not found."""


class DNAvisitRequestError(Exception):
    """Raised when a DNAvisit request fails."""
