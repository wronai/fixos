# Pyqual Pipeline Report

**Generated:** 2026-04-04 16:00:56
**Pipeline run:** 2026-04-04T14:00:56.640368+00:00

---

## 🔄 Pipeline Flow Diagram

```mermaid
flowchart LR
    S0["push<br/>2.6s"]
    style S0 fill:#90EE90
    S1["publish<br/>2.4s"]
    style S1 fill:#90EE90
    S0 --> S1
    S2["calibrate<br/>60.1s"]
    style S2 fill:#FFB6C1
    S1 --> S2
    S3["markdown_report<br/>25.4s"]
    style S3 fill:#90EE90
    S2 --> S3
    S4["lint<br/>0.2s"]
    style S4 fill:#90EE90
    S3 --> S4
    S5["setup<br/>20.0s"]
    style S5 fill:#90EE90
    S4 --> S5
    G["✓ All Gates Passed"]
    style G fill:#90EE90,stroke:#228B22,stroke-width:3px
    S5 --> G
```

## 📈 ASCII Visualization

```
┌─────────────────────────────────────────────────────────────────┐
│                    PYQUAL PIPELINE FLOW                         │
├─────────────────────────────────────────────────────────────────┤
│  ✓ push                         2.6s 🟢        │
│  ✓ publish                      2.4s 🟢        │
│  ✗ calibrate                   60.1s 🔴        │
│  ✓ markdown_report             25.4s 🟢        │
│  ✓ lint                         0.2s 🟢        │
│  ✓ setup                       20.0s 🟢        │
├─────────────────────────────────────────────────────────────────┤
│  🎉 ALL GATES PASSED ✓                                           │
│  ⏱️  Total time: 110.7s                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 Quality Gates

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|

### 🔧 Stage Execution Details

#### ✅ push
- **Status:** passed
- **Duration:** 2.6s
- **Return code:** 0

#### ✅ publish
- **Status:** passed
- **Duration:** 2.4s
- **Return code:** 0

#### ❌ calibrate
- **Status:** failed
- **Duration:** 60.1s
- **Return code:** 124

#### ✅ markdown_report
- **Status:** passed
- **Duration:** 25.4s
- **Return code:** 0

#### ✅ lint
- **Status:** passed
- **Duration:** 0.2s
- **Return code:** 0

#### ✅ setup
- **Status:** passed
- **Duration:** 20.0s
- **Return code:** 0


---

## 📝 Summary

✅ **All quality gates passed!** Pipeline completed successfully in 110.7s.
