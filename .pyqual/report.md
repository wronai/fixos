# Pyqual Pipeline Report

**Generated:** 2026-04-04 16:03:19
**Pipeline run:** 2026-04-04T14:03:19.735797+00:00

---

## 🔄 Pipeline Flow Diagram

```mermaid
flowchart LR
    S0["setup<br/>21.2s"]
    style S0 fill:#90EE90
    S1["prefact<br/>190.6s"]
    style S1 fill:#90EE90
    S0 --> S1
    S2["verify<br/>3.8s"]
    style S2 fill:#FFB6C1
    S1 --> S2
    S3["calibrate<br/>60.1s"]
    style S3 fill:#FFB6C1
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
│  ✓ setup                       21.2s 🟢        │
│  ✓ prefact                    190.6s 🟢        │
│  ✗ verify                       3.8s 🔴        │
│  ✗ calibrate                   60.1s 🔴        │
│  ✓ lint                         0.2s 🟢        │
├─────────────────────────────────────────────────────────────────┤
│  🎉 ALL GATES PASSED ✓                                           │
│  ⏱️  Total time: 275.8s                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 Quality Gates

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|

### 🔧 Stage Execution Details

#### ✅ setup
- **Status:** passed
- **Duration:** 21.2s
- **Return code:** 0

#### ✅ prefact
- **Status:** passed
- **Duration:** 190.6s
- **Return code:** 0

#### ❌ verify
- **Status:** failed
- **Duration:** 3.8s
- **Return code:** 2

#### ❌ calibrate
- **Status:** failed
- **Duration:** 60.1s
- **Return code:** 124

#### ✅ lint
- **Status:** passed
- **Duration:** 0.2s
- **Return code:** 0


---

## 📝 Summary

✅ **All quality gates passed!** Pipeline completed successfully in 275.8s.
