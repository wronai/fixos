# fixOS — API Changelog

> 9 change(s) detected

## Added

- 🆕 **class** `fixos.diagnostics.flatpak_analyzer.FlatpakAnalyzer`
- 🆕 **method** `analyze(self)`
- 🆕 **method** `get_cleanup_summary(self)`
- 🆕 **class** `fixos.diagnostics.flatpak_analyzer.FlatpakItemInfo`
- 🆕 **method** `to_dict(self)`
- 🆕 **class** `fixos.diagnostics.flatpak_analyzer.FlatpakItemType`
- 🆕 **function** `analyze_flatpak_for_cleanup()`

## Changed

- ✏️ **function** `cli(ctx, dry_run, version)`
  - signature changed
  - was: `cli(ctx, dry_run)`
- ✏️ **class** `fixos.diagnostics.service_scanner.ServiceDataScanner`
  - added methods: fixos.diagnostics.service_scanner.ServiceDataScanner._get_flatpak_details, fixos.diagnostics.service_scanner.ServiceDataScanner._parse_size_bytes
