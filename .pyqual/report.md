# Pyqual Pipeline Report

**Generated:** 2026-04-04 15:58:28
**Pipeline run:** 2026-04-04T13:58:28.284627+00:00

---

## 🔄 Pipeline Flow Diagram

```mermaid
flowchart LR
    S0["markdown_report<br/>3.1s"]
    style S0 fill:#90EE90
    S1["push<br/>1.8s"]
    style S1 fill:#90EE90
    S0 --> S1
    S2["setup<br/>3.1s"]
    style S2 fill:#90EE90
    S1 --> S2
    S3["publish<br/>0.7s"]
    style S3 fill:#90EE90
    S2 --> S3
    S4["calibrate<br/>60.1s"]
    style S4 fill:#FFB6C1
    S3 --> S4
    S5["lint<br/>0.1s"]
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
│  ✓ markdown_report              3.1s 🟢        │
│  ✓ push                         1.8s 🟢        │
│  ✓ setup                        3.1s 🟢        │
│  ✓ publish                      0.7s 🟢        │
│  ✗ calibrate                   60.1s 🔴        │
│  ✓ lint                         0.1s 🟢        │
├─────────────────────────────────────────────────────────────────┤
│  🎉 ALL GATES PASSED ✓                                           │
│  ⏱️  Total time: 68.9s                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 Quality Gates

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|

### 🔧 Stage Execution Details

#### ✅ markdown_report
- **Status:** passed
- **Duration:** 3.1s
- **Return code:** 0

#### ✅ push
- **Status:** passed
- **Duration:** 1.8s
- **Return code:** 0

#### ✅ setup
- **Status:** passed
- **Duration:** 3.1s
- **Return code:** 0

#### ✅ publish
- **Status:** passed
- **Duration:** 0.7s
- **Return code:** 0

#### ❌ calibrate
- **Status:** failed
- **Duration:** 60.1s
- **Return code:** 124

#### ✅ lint
- **Status:** passed
- **Duration:** 0.1s
- **Return code:** 0


---

## 📝 Summary

✅ **All quality gates passed!** Pipeline completed successfully in 68.9s.
