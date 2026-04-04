# Pyqual Pipeline Report

**Generated:** 2026-04-04 15:59:45
**Pipeline run:** 2026-04-04T13:59:44.439241+00:00

---

## 🔄 Pipeline Flow Diagram

```mermaid
flowchart LR
    S0["push<br/>2.3s"]
    style S0 fill:#90EE90
    S1["publish<br/>1.2s"]
    style S1 fill:#90EE90
    S0 --> S1
    S2["calibrate<br/>60.1s"]
    style S2 fill:#FFB6C1
    S1 --> S2
    S3["markdown_report<br/>9.4s"]
    style S3 fill:#90EE90
    S2 --> S3
    S4["lint<br/>0.2s"]
    style S4 fill:#90EE90
    S3 --> S4
    G["✓ All Gates Passed"]
    style G fill:#90EE90,stroke:#228B22,stroke-width:3px
    S4 --> G
```

## 📈 ASCII Visualization

```
┌─────────────────────────────────────────────────────────────────┐
│                    PYQUAL PIPELINE FLOW                         │
├─────────────────────────────────────────────────────────────────┤
│  ✓ push                         2.3s 🟢        │
│  ✓ publish                      1.2s 🟢        │
│  ✗ calibrate                   60.1s 🔴        │
│  ✓ markdown_report              9.4s 🟢        │
│  ✓ lint                         0.2s 🟢        │
├─────────────────────────────────────────────────────────────────┤
│  🎉 ALL GATES PASSED ✓                                           │
│  ⏱️  Total time: 73.1s                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 Quality Gates

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|

### 🔧 Stage Execution Details

#### ✅ push
- **Status:** passed
- **Duration:** 2.3s
- **Return code:** 0

#### ✅ publish
- **Status:** passed
- **Duration:** 1.2s
- **Return code:** 0

#### ❌ calibrate
- **Status:** failed
- **Duration:** 60.1s
- **Return code:** 124

#### ✅ markdown_report
- **Status:** passed
- **Duration:** 9.4s
- **Return code:** 0

#### ✅ lint
- **Status:** passed
- **Duration:** 0.2s
- **Return code:** 0


---

## 📝 Summary

✅ **All quality gates passed!** Pipeline completed successfully in 73.1s.
