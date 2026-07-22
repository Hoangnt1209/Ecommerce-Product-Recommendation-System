---
goal: Persistent Recommendation Cache
version: 1.0
date_created: 2026-07-22
last_updated: 2026-07-22
owner: Recommendation API
status: 'Completed'
tags: [feature, caching, serving]
---

# Introduction

![Status: Completed](https://img.shields.io/badge/status-Completed-brightgreen)

Persist deterministic recommendation responses so repeat requests avoid model inference and can be served before ML checkpoints are loaded.

## 1. Requirements & Constraints

- **REQ-001**: Cache registered-user and interactive recommendation responses on disk.
- **REQ-002**: Invalidate cached responses whenever a checkpoint artifact changes.
- **REQ-003**: Preserve the existing API response schema and routes.
- **CON-001**: Use only Python standard-library persistence; add no runtime dependency.

## 2. Implementation Steps

### Implementation Phase 1

- GOAL-001: Implement versioned, atomic JSON cache storage.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-001 | Add `src/services/recommendation_cache.py` with fingerprinted keys, JSON reads, and atomic writes. | ✅ | 2026-07-22 |
| TASK-002 | Add cache directory configuration to `src/config/settings.py`. | ✅ | 2026-07-22 |

### Implementation Phase 2

- GOAL-002: Use cache before model initialization and validate behavior.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-003 | Integrate cache lookup and persistence into `RecommendationService.recommend` and `recommend_from_items`; defer model loading so cache hits bypass checkpoint deserialization. | ✅ | 2026-07-22 |
| TASK-005 | Add `scripts/warm_recommendation_cache.py` to precompute persistent responses after training. | ✅ | 2026-07-22 |
| TASK-004 | Add unit tests for cache hit, persistence, and checkpoint-fingerprint invalidation. | ✅ | 2026-07-22 |

## 3. Alternatives

- **ALT-001**: Redis was not selected because the project has no mandatory Redis service and disk JSON keeps local development self-contained.
- **ALT-002**: Caching only in process memory was not selected because cache would disappear after every API restart.

## 4. Dependencies

- **DEP-001**: Existing checkpoint files in `checkpoints/` provide the cache version fingerprint.

## 5. Files

- **FILE-001**: `src/services/recommendation_cache.py` stores versioned response files.
- **FILE-002**: `src/services/recommendation_service.py` consumes the cache.
- **FILE-003**: `tests/test_recommendation_cache.py` verifies cache behavior.
- **FILE-004**: `scripts/warm_recommendation_cache.py` precomputes the cache.

## 6. Testing

- **TEST-001**: Verify the same request is returned from disk cache without calling the producer.
- **TEST-002**: Verify a changed checkpoint fingerprint produces a cache miss.

## 7. Risks & Assumptions

- **RISK-001**: JSON cache size grows with the number of distinct request keys.
- **ASSUMPTION-001**: Recommendation response dictionaries are JSON serializable.

## 8. Related Specifications / Further Reading

`src/services/recommendation_service.py`
