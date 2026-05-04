"""
Human-in-the-Loop (HITL) Session for fixOS Agent
Interactive session where user approves each action.
"""

import time
from typing import Dict, Any, List, Tuple

from ..providers.llm import LLMClient, LLMError
from ..utils.anonymizer import anonymize, display_anonymized_preview
from ..utils.web_search import search_all, format_results_for_llm
from ..config import FixOsConfig
from ..constants import (
    HITL_TIMEOUT_BUFFER,
    AUTONOMOU_TIMEOUT_BUFFER,
    CLEANUP_TIMEOUT_ESTIMATE,
    MAX_COMMAND_LENGTH,
)
from ..platform_utils import (
    setup_signal_timeout, cancel_signal_timeout,
    get_os_info, get_package_manager,
)
from ..utils.timeout import SessionTimeout

from .session_core import CmdResult, SYSTEM_PROMPT, extract_fixes, extract_search_topic
from . import session_io as io
from . import session_handlers as handlers


class HITLSession:
    """Interactive Human-in-the-Loop diagnostic and repair session."""

    MAX_WEB_SEARCHES = 3

    def __init__(
        self,
        diagnostics: Dict[str, Any],
        config: FixOsConfig,
        show_data: bool = True,
    ):
        self.diagnostics = diagnostics
        self.config = config
        self.show_data = show_data
        self.llm = LLMClient(config)
        self.os_info = get_os_info()
        self.pkg_manager = get_package_manager() or "unknown"
        self.messages: List[Dict[str, str]] = []
        self.executed: List[CmdResult] = []
        self.web_search_count = 0
        self.last_fixes: List[Tuple[str, str]] = []
        self.start_ts = time.time()
        self._setup_timeout()

    def _setup_timeout(self):
        """Setup session timeout handler."""
        from . import session_io
        def _timeout(signum, frame):
            raise SessionTimeout()
        # Store reference in session_io for reinstatement during user input
        session_io._setup_timeout_ref(self, self.config.session_timeout, _timeout)
        setup_signal_timeout(self.config.session_timeout, _timeout)

    def _clear_timeout(self):
        """Clear the timeout alarm."""
        cancel_signal_timeout()

    def remaining(self) -> int:
        """Get remaining session time in seconds."""
        from . import get_remaining_time
        return get_remaining_time(self)

    def _initialize_messages(self) -> bool:
        """Initialize LLM message history with system prompt and diagnostics."""
        anon_str, report = anonymize(str(self.diagnostics))

        if self.show_data:
            display_anonymized_preview(anon_str, report)
            if not io.ask_send_data():
                io.console.print("  Anulowano.")
                return False

        self.messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"OS: {self.os_info['system']} {self.os_info['release']} | "
                    f"Package manager: {self.pkg_manager}\n\n"
                    f"Anonymized diagnostic data:\n```\n{anon_str}\n```\n\n"
                    f"Perform full analysis and list all detected problems."
                ),
            },
        ]
        return True

    def _print_header(self):
        """Print session header with system info."""
        io.print_session_header(
            self.os_info, self.pkg_manager,
            self.config.model, self.config.session_timeout,
            self.remaining
        )

    def _handle_llm_error(self) -> bool:
        """Handle LLM error - try web search if enabled."""
        if self.config.enable_web_search and self.web_search_count < self.MAX_WEB_SEARCHES:
            self.web_search_count += 1
            io.print_searching()
            results = search_all("linux system diagnostics repair", self.config.serpapi_key)
            if results:
                io.console.print(format_results_for_llm(results))
                return True
        return False

    def _check_low_confidence(self, reply: str) -> bool:
        """Check if LLM is uncertain and perform web search if enabled."""
        low_conf = any(p in reply.lower() for p in [
            "nie wiem", "nie jestem pewien", "i don't know",
            "not sure", "cannot determine",
        ])
        if low_conf and self.config.enable_web_search and self.web_search_count < self.MAX_WEB_SEARCHES:
            if io.ask_low_confidence_search():
                self.web_search_count += 1
                topic = extract_search_topic(reply)
                results = search_all(topic, self.config.serpapi_key)
                if results:
                    web_ctx = format_results_for_llm(results)
                    io.console.print(web_ctx)
                    self.messages.append({"role": "user",
                                     "content": f"External sources:\n{web_ctx}\nUpdate analysis."})
                    return True
        return False

    def _process_turn(self) -> bool:
        """Process one turn of the HITL session."""
        rem = self.remaining()
        if rem <= 0:
            raise SessionTimeout()

        io.print_thinking()
        try:
            reply = self.llm.chat(self.messages, max_tokens=2500, temperature=0.2)
            self.messages.append({"role": "assistant", "content": reply})
        except LLMError as e:
            io.clear_thinking()
            io.print_llm_error(e)
            if not self._handle_llm_error():
                return False
            return True
        io.clear_thinking()

        io.print_llm_reply(reply)
        self.last_fixes = extract_fixes(reply)

        if self._check_low_confidence(reply):
            return True

        io.print_action_menu(self.last_fixes, rem, self.llm.total_tokens)

        user_in = io.get_user_input(rem)
        if not user_in:
            return True

        # Handle all command types via handlers module
        should_continue, was_handled = handlers.parse_user_input(
            user_in, self.last_fixes, self.messages, self.executed,
            self.config.serpapi_key
        )
        
        if not was_handled:
            # Free text → send to LLM
            self.messages.append({"role": "user", "content": user_in})
        
        return should_continue

    def run(self) -> None:
        """Run the HITL session."""
        if not self._initialize_messages():
            return
        self._print_header()

        try:
            while True:
                should_continue = self._process_turn()
                if not should_continue:
                    break
        except SessionTimeout:
            io.print_timeout()
        finally:
            self._clear_timeout()

        self._print_summary()

    def _print_summary(self):
        """Print session summary."""
        elapsed = int(time.time() - self.start_ts)
        io.print_session_summary(len(self.messages)-2, elapsed, self.llm.total_tokens, self.executed)


def run_hitl_session(
    diagnostics: Dict[str, Any],
    config: FixOsConfig,
    show_data: bool = True,
) -> None:
    """Run interactive HITL session (backward compatible wrapper)."""
    session = HITLSession(
        diagnostics=diagnostics,
        config=config,
        show_data=show_data,
    )
    session.run()


# Backward compatibility exports
__all__ = [
    "CmdResult",
    "HITLSession", 
    "run_hitl_session",
    "SYSTEM_PROMPT",
]
