# Verified synthetic report

These six files were downloaded from the local Windows MVP and supplied for
verification on 11 October 2026. They describe the six entirely invented records
from **Use synthetic example**, not survey respondents or study estimates.

The results include one record in each classification, two resolved passes,
one reported recipient, one reported non-recipient, and two frozen scores of
approximately 18.53%. Weighted and unweighted non-receipt are both 50% for this
invented example. No filters were selected, so `filtered_results.csv` equals
`results.csv`.

All five exported output files match the SHA-256 values in `audit_manifest.json`
and the expected built-in synthetic outputs. CSV and JSON summaries agree.
Recorded application source and model hashes agree with the packaged MVP.
See [verification evidence](../../docs/windows_validation.json) for all 50
checks and their scope.

The supplied files are retained byte-for-byte. The audit manifest is a historical
record of this run and must not be edited to claim a later Git commit or clean
working tree. It records the original research revision with local changes,
as well as individual application source hashes. Run the app from a fresh clone
of the committed version to obtain new reports tied to that checkout.

The six extracted files were supplied individually; the downloaded ZIP container
itself was not supplied for verification. Source/model comparison and known
synthetic-input checksum verification do not constitute remote execution
attestation or external predictive validation.
