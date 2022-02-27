class MissingConfigurationError(Exception):
    """
    Custom error class for configuration errors.
    """
    pass


class TokenError(Exception):
    """
    Custom error class for token errors.
    """
    pass


class AzureUrlError(Exception):
    """
    Custom error class for azure url errors.
    """
    pass


class LoggerError(Exception):
    """
    Custom error class for logger errors.
    """
    pass


class AgentSetupError(Exception):
    """
    Custom error class for agent setup errors.
    """
    pass


class PipelineNotFoundError(Exception):
    """
    Custom error class for pipeline not found errors.
    """
    pass


class APIError(Exception):
    """
    Custom error class for API errors.
    """
    pass


class MoveFileError(Exception):
    """
    Custom error class for move file errors.
    """
    pass

class FileMetadataError(Exception):
    """
    Custom error class for file metadata errors.
    """
    pass

class FileMetadataNotFound(FileMetadataError):
    """
    Custom error class for file metadata errors.
    """
    pass
  