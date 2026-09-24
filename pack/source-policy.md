# Source policy

1. Preserve source bytes before deriving claims.
2. Label reconstructions as reconstructed.
3. Strip secrets (`auth.json`, `KILO_SERVER_PASSWORD`, tokens, bearer headers) before packing.
4. Agents propose. Mechanical tests and review gates decide promotion.
5. Do not treat chat summaries in this pack as verbatim evidence of the Kilo session.
6. Pack writes are scoped to `pack_70d838252b9cbbdca9f5b07e068103d3` only.
7. Do not promote `artifacts/reconstructed/` over the session bytes.
8. Do not treat the 2026-09-20 export as the 2026-09-21 gold session.
9. Do not relabel the proposed receipt as W3C PROV, and do not rewrite `dkg.event.v1` events into `prov:Entity` records.
10. Do not treat `session_diff` plan files as a history of the live Kilo config.
