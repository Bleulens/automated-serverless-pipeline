"""
errors.py

Custom exception hierarchy for the automated serverless pipeline.
Provides clear, structured error types for transformation and S3 operations.
"""


class PipelineError(Exception):
    """Base class for all pipeline-related errors."""

    pass


class InvalidEventError(PipelineError):
    """Raised when the incoming Lambda event is malformed."""

    pass


class TransformError(PipelineError):
    """Raised when data transformation fails."""

    pass


class SchemaValidationError(TransformError):
    """Raised when input JSON is missing required fields or structure."""

    pass


class S3ReadError(PipelineError):
    """Raised when reading from S3 fails."""

    pass


class S3WriteError(PipelineError):
    """Raised when writing to S3 fails."""

    pass
