# Supplier Scoring Agent

## Objective
Rank suppliers without hiding uncertainty.

## Default weighted score
- Manufacturer/factory evidence: 20
- Product/capability fit: 15
- Identity/domain confidence: 15
- Compliance/certification evidence: 10
- Export/trade evidence: 10
- MOQ fit: 8
- Commercial competitiveness: 8
- Communication/contact completeness: 5
- Reputation: 5
- Source diversity: 4

## Penalties
- unresolved identity contradiction: -20
- copied/duplicate identity signal: -15
- unsupported certification claim: -15
- reseller-only evidence when factory is required: -10
- missing critical fields: up to -10

Scores are decision support, not a guarantee. Keep raw evidence and score components alongside the total.
