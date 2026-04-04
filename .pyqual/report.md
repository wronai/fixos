# Pyqual Pipeline Report

**Generated:** 2026-04-04 15:59:32
**Pipeline run:** 2026-04-04T13:59:32.704824+00:00

---

## 🔄 Pipeline Flow Diagram

```mermaid
flowchart LR
    S0["publish<br/>1.8s"]
    style S0 fill:#90EE90
    S1["calibrate<br/>60.1s"]
    style S1 fill:#FFB6C1
    S0 --> S1
    S2["lint<br/>0.1s"]
    style S2 fill:#90EE90
    S1 --> S2
    S3["setup<br/>8.9s"]
    style S3 fill:#90EE90
    S2 --> S3
    S4["push<br/>2.2s"]
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
│  ✓ publish                      1.8s 🟢        │
│  ✗ calibrate                   60.1s 🔴        │
│  ✓ lint                         0.1s 🟢        │
│  ✓ setup                        8.9s 🟢        │
│  ✓ push                         2.2s 🟢        │
├─────────────────────────────────────────────────────────────────┤
│  🎉 ALL GATES PASSED ✓                                           │
│  ⏱️  Total time: 73.1s                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 Quality Gates

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|

### 🔧 Stage Execution Details

#### ✅ publish
- **Status:** passed
- **Duration:** 1.8s
- **Return code:** 0

#### ❌ calibrate
- **Status:** failed
- **Duration:** 60.1s
- **Return code:** 124

#### ✅ lint
- **Status:** passed
- **Duration:** 0.1s
- **Return code:** 0

#### ✅ setup
- **Status:** passed
- **Duration:** 8.9s
- **Return code:** 0

#### ✅ push
- **Status:** passed
- **Duration:** 2.2s
- **Return code:** 0


---

## 📝 Summary

✅ **All quality gates passed!** Pipeline completed successfully in 73.1s.
