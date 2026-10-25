# Acceptance matrix - FREG-PUBLIC-ARCH-001
24-10-2026. PASS local does not mean published. Evidence under reports/public_arch001.

| ID | Requirement | Expected / observed | Status | Evidence |
|---|---|---|---|---|
| AC-P01 | Browser access without installation | Browser opens loopback; external URL absent | PASS local / NOT RUN Internet | UI01 |
| AC-P02 | Anonymous visitor | No login prompt or session identity needed | PASS local | UI01 |
| AC-P03 | Desktop/mobile | Query works at1440x1080 and390x844; no horizontal overflow | PASS local | UI09, internal visual QA |
| AC-P04 | Approved synthetic corpus | Private/unknown/retired/unapproved data rejected | PASS | Python negatives; Node case6 |
| AC-P05 | Actual documentary evidence | Exact chunk with matching source section | PASS | Python vectors; UI02/03 |
| AC-P06 | No fake generation | Explicit lexical label; no LLM/API | PASS inspection | templates, six initial requests |
| AC-P07 | No private indexes/data | Allowlist artifact; no DB/env/lab | PASS local | build test, UI11 |
| AC-P08 | No public admin writes | No backend; local review POST501 | PASS in subset | UI11 |
| AC-P09 | Proportionate resource bounds | Input/stream/chunks bounded; per-tab pacing; provider abuse limits unverified | PASS client / NOT RUN provider | Node5/10/11; UI07 |
| AC-P10 | Provider restrictions | Size below documented limits; no hosted validation yet | NOT RUN hosted | hosting evaluation |
| AC-P11 | Identifiable version | version, commit, engine, policy and corpus in manifest | PASS local | release.json, receipt |
| AC-P12 | Reproducibility | Two builds same bytes; no fresh Windows install | PASS build / NOT RUN clean install | Python repeat build |
| AC-P13 | Automated tests | 104Python+15Node+11UI, distinct scopes | PASS | XML, TAP, browser.json |
| AC-P14 | Rollback | Procedure preserves current corpus; full host/CDN rollback not executed | NOT RUN operational | versioning strategy |
| AC-P15 | Visitor guidance | Purpose, corpus, limitations and citations visible | PASS internal review | UI and guide |

Not run: two original Streamlit tests, four real semantic integration cases, fresh vulnerability scanner, remoteCI, public URL/load, host/MFA/ACL, realLLM. No claims of certification or complete coverage.
