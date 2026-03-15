# fixOS — API Changelog

> 64 change(s) detected

## Added

- 🆕 **function** `history(limit, json_output)`
- 🆕 **function** `profile()`
- 🆕 **function** `profile_list()`
- 🆕 **function** `profile_show(name)`
- 🆕 **function** `quickfix(dry_run, modules)`
- 🆕 **function** `report(output_format, output, modules, profile)`
- 🆕 **function** `rollback()`
- 🆕 **function** `rollback_list(limit)`
- 🆕 **function** `rollback_show(session_id)`
- 🆕 **function** `rollback_undo(session_id, last, dry_run)`
- 🆕 **function** `watch(interval, modules, alert_on, max_iterations)`
- 🆕 **class** `fixos.orchestrator.rollback.RollbackEntry`
- 🆕 **class** `fixos.orchestrator.rollback.RollbackSession`
- 🆕 **method** `get_rollback_commands(self)`
- 🆕 **method** `list_sessions(cls, limit)`
- 🆕 **method** `load(cls, session_id)`
- 🆕 **method** `record(self, command, rollback_cmd, stdout, stderr, success, exit_code)`
- 🆕 **method** `rollback_last(self, n, dry_run)`
- 🆕 **class** `fixos.plugins.base.DiagnosticPlugin`
- 🆕 **method** `can_run(self)`
- 🆕 **method** `diagnose(self)`
- 🆕 **method** `get_metadata(self)`
- 🆕 **class** `fixos.plugins.base.DiagnosticResult`
- 🆕 **method** `to_dict(self)`
- 🆕 **class** `fixos.plugins.base.Finding`
- 🆕 **class** `fixos.plugins.base.Severity`
- 🆕 **class** `fixos.plugins.builtin.audio.Plugin`
- 🆕 **method** `diagnose(self)`
- 🆕 **class** `fixos.plugins.builtin.disk.Plugin`
- 🆕 **method** `diagnose(self)`
- 🆕 **class** `fixos.plugins.builtin.hardware.Plugin`
- 🆕 **method** `diagnose(self)`
- 🆕 **class** `fixos.plugins.builtin.resources.Plugin`
- 🆕 **method** `diagnose(self)`
- 🆕 **class** `fixos.plugins.builtin.security.Plugin`
- 🆕 **method** `diagnose(self)`
- 🆕 **class** `fixos.plugins.builtin.thumbnails.Plugin`
- 🆕 **method** `diagnose(self)`
- 🆕 **class** `fixos.plugins.registry.PluginRegistry`
- 🆕 **method** `discover(self)`
- 🆕 **method** `get_plugin(self, name)`
- 🆕 **method** `list_plugins(self, runnable_only)`
- 🆕 **method** `register(self, plugin)`
- 🆕 **method** `run(self, modules, progress_callback)`
- 🆕 **class** `fixos.profiles.Profile`
- 🆕 **method** `list_available(cls)`
- 🆕 **method** `load(cls, name)`
- 🆕 **method** `to_dict(self)`
- 🆕 **method** `chat_structured(self, messages, response_model)`
- 🆕 **class** `fixos.providers.schemas.CommandValidation`
- 🆕 **class** `fixos.providers.schemas.FixSuggestion`
- 🆕 **class** `fixos.providers.schemas.LLMDiagnosticResponse`
- 🆕 **class** `fixos.providers.schemas.NLPIntent`
- 🆕 **class** `fixos.providers.schemas.RiskLevel`
- 🆕 **class** `fixos.utils.timeout.SessionTimeout`
- 🆕 **function** `timeout_handler(signum, frame)`
- 🆕 **class** `fixos.watch.WatchDaemon`
- 🆕 **method** `run(self)`
- 🆕 **method** `stop(self)`

## Changed

- ✏️ **function** `scan(modules, output, show_raw, no_banner, disc, dry_run, interactive, json_output, llm_fallback, profile)`
  - signature changed
  - was: `scan(modules, output, show_raw, no_banner, disc, dry_run, interactive, json_output, llm_fallback)`
- ✏️ **class** `fixos.providers.llm.LLMClient`
  - added methods: fixos.providers.llm.LLMClient._extract_json, fixos.providers.llm.LLMClient.chat_structured

## Removed

- 🗑️ **class** `fixos.agent.autonomous.SessionTimeout`
- 🗑️ **class** `fixos.agent.hitl.SessionTimeout`
- 🗑️ **class** `fixos.llm_shell.SessionTimeout`
