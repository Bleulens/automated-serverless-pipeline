class TransformError(Exception):
    """Custom exception for transform-related errors."""

    pass


class S3ReadError(Exception):
    """Custom exception for S3 read errors."""

    pass


class S3WriteError(Exception):
    """Custom exception for S3 write errors."""

    pass
