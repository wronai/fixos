# fixOS — API Changelog

> 33 change(s) detected

## Added

- 🆕 **function** `features()`
- 🆕 **function** `features_audit(profile, json_output)`
- 🆕 **function** `features_install(profile, dry_run, yes, category)`
- 🆕 **function** `features_profiles()`
- 🆕 **function** `features_system()`
- 🆕 **class** `fixos.features.SystemDetector`
- 🆕 **method** `detect(self)`
- 🆕 **class** `fixos.features.SystemInfo`
- 🆕 **class** `fixos.features.auditor.AuditResult`
- 🆕 **method** `to_dict(self)`
- 🆕 **class** `fixos.features.auditor.FeatureAuditor`
- 🆕 **method** `audit(self, profile)`
- 🆕 **class** `fixos.features.catalog.PackageCatalog`
- 🆕 **method** `get_package(self, pkg_id)`
- 🆕 **method** `get_packages_by_category(self, category)`
- 🆕 **method** `list_categories(self)`
- 🆕 **method** `load(cls, data_dir)`
- 🆕 **class** `fixos.features.catalog.PackageCategory`
- 🆕 **class** `fixos.features.catalog.PackageInfo`
- 🆕 **method** `get_distro_name(self, distro)`
- 🆕 **method** `is_available_on(self, distro)`
- 🆕 **class** `fixos.features.installer.FeatureInstaller`
- 🆕 **method** `get_rollback_commands(self, installed_packages)`
- 🆕 **method** `install(self, packages)`
- 🆕 **class** `fixos.features.profiles.UserProfile`
- 🆕 **method** `list_available(cls, data_dir)`
- 🆕 **method** `load(cls, profile_name, data_dir)`
- 🆕 **method** `resolve_packages(self, catalog, system_info)`
- 🆕 **method** `to_dict(self)`
- 🆕 **class** `fixos.features.renderer.FeatureRenderer`
- 🆕 **method** `render_audit(result)`
- 🆕 **method** `render_package_list(packages, title)`
- 🆕 **method** `render_system_info(system)`
