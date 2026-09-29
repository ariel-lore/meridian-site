# Sample diagnostic (redacted)

**Service:** Meridian Vibe Code Rescue
**Date:** 27 September 2026
**Engagement ID:** SAMPLE-000
**Classification:** Illustrative. Fictionalised findings; no real client data

---

## Executive summary

**Recommendation:** **Harden** (salvage), not full rewrite.

The product UI and primary workflow are salvageable. Blocking issues cluster in secrets handling, Supabase RLS, and Stripe webhook verification. Estimated fixed-scope rescue: **1.5–2.5 weeks** after approval (band aligned with focused rescue pricing).

---

## Severity legend

| Level | Meaning |
|-------|---------|
| P0 | Exploit or data-loss path; fix before traffic/diligence |
| P1 | Production correctness / money path |
| P2 | Maintainability / deploy reliability |
| P3 | Cleanup / nice-to-have |

---

## Findings (excerpt)

### P0. Privileged API key referenced in client bundle
- **Evidence:** Key prefix pattern present in a client-shipped module (redacted).
- **Impact:** Anyone can extract and abuse the key.
- **Action:** Rotate immediately; move to server-only env; add secret scanning to CI.

### P0. RLS disabled on `profiles` and `workspaces`
- **Evidence:** Policies absent / row level security not applied (redacted schema notes).
- **Impact:** Cross-tenant read/write of user data.
- **Action:** Enable RLS; policies keyed to verified auth UID; add cross-tenant denial tests.

### P1. Stripe webhooks accept unsigned payloads
- **Evidence:** Handler trusts body without signature verification.
- **Impact:** Forged events can grant entitlements.
- **Action:** Verify signatures; reconcile subscription state server-side; remove client-trusted success flags.

### P1. Authz checks only in React components
- **Evidence:** Sensitive routes gated by UI conditionals only.
- **Impact:** Direct API access bypasses UI.
- **Action:** Enforce authz on server/edge; treat UI checks as UX only.

### P2. Production deploy fails on missing env
- **Evidence:** Preview host injects vars that production host does not.
- **Impact:** "Works in preview" false confidence.
- **Action:** Document required env; fail closed; smoke test post-deploy.

### P3. Inconsistent folder patterns from agent sessions
- **Impact:** Onboarding and future AI edits drift.
- **Action:** Light structure pass after P0/P1; optional agent rule files.

---

## Keep / harden / rebuild

| Area | Decision |
|------|----------|
| Marketing + app shell UI | Keep |
| Core booking/workflow screens | Keep + harden validation |
| Supabase data layer | Harden (RLS + tenancy tests) |
| Stripe integration | Harden (rewrite webhook path) |
| Auth | Harden (server enforcement) |
| Full framework rewrite | Not recommended now |

---

## Proposed fixed scope (illustrative)

1. Secret rotation runbook + CI secret scan
2. RLS policies + two cross-tenant tests
3. Stripe webhook verification + entitlement reconcile
4. Server authz on sensitive routes
5. Deploy env checklist + smoke script
6. Optional: Cursor/Claude rule files to protect tenancy and secrets patterns

**Out of scope (example):** New feature development, mobile apps, SOC2 programme.

---

## Next step

Reply to approve scope or ask questions. Do **not** paste live secrets into email; share via your secret manager or a private channel after rotation.

Meridian · hello@meridian.dev
