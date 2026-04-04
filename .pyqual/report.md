# Pyqual Pipeline Report

**Generated:** 2026-04-04 16:00:16
**Pipeline run:** 2026-04-04T14:00:15.380621+00:00

---

## 🔄 Pipeline Flow Diagram

```mermaid
flowchart LR
    S0["push<br/>2.4s"]
    style S0 fill:#90EE90
    S1["publish<br/>1.8s"]
    style S1 fill:#90EE90
    S0 --> S1
    S2["calibrate<br/>60.1s"]
    style S2 fill:#FFB6C1
    S1 --> S2
    S3["markdown_report<br/>15.7s"]
    style S3 fill:#90EE90
    S2 --> S3
    S4["lint<br/>0.2s"]
    style S4 fill:#90EE90
    S3 --> S4
    S5["prefact<br/>112.8s"]
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
│  ✓ push                         2.4s 🟢        │
│  ✓ publish                      1.8s 🟢        │
│  ✗ calibrate                   60.1s 🔴        │
│  ✓ markdown_report             15.7s 🟢        │
│  ✓ lint                         0.2s 🟢        │
│  ✓ prefact                    112.8s 🟢        │
├─────────────────────────────────────────────────────────────────┤
│  🎉 ALL GATES PASSED ✓                                           │
│  ⏱️  Total time: 193.0s                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 Quality Gates

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|

### 🔧 Stage Execution Details

#### ✅ push
- **Status:** passed
- **Duration:** 2.4s
- **Return code:** 0

#### ✅ publish
- **Status:** passed
- **Duration:** 1.8s
- **Return code:** 0

#### ❌ calibrate
- **Status:** failed
- **Duration:** 60.1s
- **Return code:** 124

#### ✅ markdown_report
- **Status:** passed
- **Duration:** 15.7s
- **Return code:** 0

#### ✅ lint
- **Status:** passed
- **Duration:** 0.2s
- **Return code:** 0

#### ✅ prefact
- **Status:** passed
- **Duration:** 112.8s
- **Return code:** 0


---

## 📝 Summary

✅ **All quality gates passed!** Pipeline completed successfully in 193.0s.
