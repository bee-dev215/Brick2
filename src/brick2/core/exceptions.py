"""Custom exceptions."""


class AdOrchestratorException(Exception):
    """Base exception for Ad Orchestrator."""
    pass


class CampaignNotFoundError(AdOrchestratorException):
    """Raised when campaign is not found."""
    pass


class UserNotFoundError(AdOrchestratorException):
    """Raised when user is not found."""
    pass


class AdNotFoundError(AdOrchestratorException):
    """Raised when ad is not found."""
    pass


class LeadNotFoundError(AdOrchestratorException):
    """Raised when lead is not found."""
    pass


class PerformanceNotFoundError(AdOrchestratorException):
    """Raised when performance record is not found."""
    pass
