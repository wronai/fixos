"""
Global constants for fixOS - avoiding magic numbers.
"""

# Session timeouts
DEFAULT_SESSION_TIMEOUT = 300  # 5 minutes
HITL_TIMEOUT_BUFFER = 80  # Buffer time for HITL session (seconds)
AUTONOMOU_TIMEOUT_BUFFER = 40  # Buffer time for autonomous session
CLEANUP_TIMEOUT_ESTIMATE = 120  # Estimated cleanup timeout
DEFAULT_COMMAND_TIMEOUT = 300  # Default command timeout in HITL session
LONG_COMMAND_TIMEOUT = 1800  # Long-running operations like system updates
FAST_COMMAND_TIMEOUT = 60  # Read-only and quick diagnostic commands

# String lengths / limits
MAX_COMMAND_LENGTH = 200  # Maximum length for command display
MAX_SEARCH_QUERY_LENGTH = 500  # Maximum length for search query
MAX_OUTPUT_LINES = 40  # Maximum output lines to display
HOSTNAME_DISPLAY_LENGTH = 65  # Length for hostname display
CONFIG_DISPLAY_LENGTH = 40  # Length for config line display
PROFILE_DISPLAY_LENGTH = 55  # Length for profile display

# Token/API limits
DEFAULT_TOKEN_LIMIT = 2000  # Default token estimate
MAX_WEB_SEARCH_COUNT = 5  # Maximum web searches per session

# Service/process limits
DEFAULT_HISTORY_LIMIT = 20  # Default history items to show

# Text formatting
COMMAND_PREFIX_LENGTH = 80  # Max length for command prefix in output
MAX_SUMMARY_LENGTH = 200  # Max summary chars for derived search topic
