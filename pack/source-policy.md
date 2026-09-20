# Source policy

1. Preserve source bytes before deriving claims.
2. Label reconstructions as reconstructed.
3. Strip secrets (`auth.json`, `KILO_SERVER_PASSWORD`, tokens, bearer headers) before packing.
4. Agents propose. Mechanical tests and review gates decide promotion.
5. Do not treat chat summaries in this pack as verbatim evidence of the Kilo session.
6. Pack writes are scoped to `pack_70d838252b9cbbdca9f5b07e068103d3` only.
