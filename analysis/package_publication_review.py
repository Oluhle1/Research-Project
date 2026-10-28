"""Package only the new validation code, documents and aggregate evidence."""
from datetime import datetime, timezone
from pathlib import Path
import csv
import hashlib
import json
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / 'paper/publication'
HONOURS = 'e5fd40302cfcc2da120e2d727b98ae054edbfb80'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    changes = subprocess.check_output(['git', 'diff', '--name-status', HONOURS],
                                      cwd=ROOT, text=True).splitlines()
    if any(not line.startswith('A\t') for line in changes):
        raise ValueError('An original Honours-tracked file changed')
    run = json.loads((ROOT / 'output/publication_validation/run_record.json').read_text())
    assert not run['pilot_only']
    assert run['nested_repetitions_valid'] == 40 and run['bootstrap_valid'] == 1000
    assert run['inner_fits_attempted'] == run['inner_fits_converged'] == 48040
    assert run['final_fits_attempted'] == run['final_fits_converged'] == 1201
    for name, value in run['output_sha256'].items():
        assert digest(ROOT / 'output/publication_validation' / name) == value
    report_review = json.loads((PAPER / 'report_review.json').read_text())
    for name, value in report_review['sha256'].items():
        assert digest(ROOT / name) == value
    files = [
        'analysis/publication_model.py', 'analysis/run_publication_validation.py',
        'analysis/build_publication_figures.py', 'analysis/render_publication_note.py',
        'analysis/package_publication_review.py', 'analysis/requirements-publication.txt',
        'tests/test_publication_validation.py', 'tests/test_publication_runner.py',
        'paper/requirements-docs.txt',
    ]
    files += ['paper/publication/' + name for name in [
        'README.md', 'methodology_protocol.md', 'validation_config.json',
        'methodology_results.md', 'Jawe_Publication_Methodology_Revision.docx',
        'Jawe_Publication_Methodology_Revision.pdf', 'methodological_review.json',
        'report_review.json', 'venue_requirements.md', 'preparation_status.json',
    ]]
    files += [str(p.relative_to(ROOT)) for p in sorted((PAPER / 'figures').iterdir()) if p.is_file()]
    files += ['output/publication_validation/' + name for name in [
        'nested_metrics.csv', 'nested_summary.csv', 'outer_coefficients.csv',
        'final_fits.csv', 'inner_fits.csv', 'tuning_scores.csv',
        'bootstrap_replicates.csv', 'bootstrap_coefficients.csv',
        'coefficient_stability.csv', 'optimism_correction.csv',
        'full_candidate.json', 'run_record.json',
    ]]
    forbidden = {'uqno', 'personno', 'person_id', 'household_id', 'record_id',
                 'research_id', 'y', 'y_n', 'p_model', 'p_reference', 'row_position'}
    for name in files:
        path = ROOT / name
        assert path.is_file() and not path.is_symlink()
        assert path.suffix not in {'.npz', '.sav', '.dta'}
        if path.suffix == '.csv':
            with path.open(newline='') as source:
                assert not set(next(csv.reader(source))) & forbidden, name
    manifest = {
        'created_at_utc': datetime.now(timezone.utc).isoformat(),
        'purpose': 'Completed supervisor-directed validation extension and author-review note',
        'honours_commit_preserved': HONOURS,
        'all_original_Honours_tracked_files_unchanged': True,
        'publication_branch': 'publication/methodology-strengthening',
        'original_primary_model_remains_exploratory': True,
        'new_candidate_replaces_production_model': False,
        'report_pages': 6, 'conference_submission_ready': False,
        'conference_format_remaining': 'Updated IST-Africa template, 8–10 pages, maximum4000words and double-blind preparation',
        'software_safeguards': {'passed': 22, 'failed': 0, 'framework': 'stdlib unittest'},
        'completed_validation': {'nested_repetitions': 40, 'bootstrap_draws': 1000,
                                  'inner_ridge_fits': 48040, 'final_ridge_fits': 1201},
        'calibration_slopes_available_per_bootstrap_evaluation_set': 993,
        'calibration_slopes_unavailable_per_bootstrap_evaluation_set': 7,
        'independent_numerical_and_visual_reviews': ['methodological_review.json', 'report_review.json'],
        'application_suite_rerun': False, 'new_participant_study': False,
        'external_validation': False, 'performance_CI_from_MCSE_claimed': False,
        'package_contains_survey_rows_or_respondent_predictions': False,
        'AI_assistance': 'OpenAI ChatGPT: methodological options, implementation/checking, figures and review-text drafting; author review required',
        'sha256': {name: digest(ROOT / name) for name in files},
    }
    manifest_path = PAPER / 'release_manifest.json'
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    files.append(str(manifest_path.relative_to(ROOT)))
    package = PAPER / 'Jawe_Publication_Methodology_Review.zip'
    with zipfile.ZipFile(package, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name in files:
            archive.write(ROOT / name, name)
        archive.writestr('README.txt', '''Publication methodology review — 28 October 2026

Read paper/publication/README.md and the six-page Word/PDF review note first.
This package contains the new validation code, focused tests, protocol, aggregate
results, diagrams and numerical/visual checks. It is not an IST-Africa submission.
The submitted Honours paper and production application/model are unchanged.
The original primary model remains exploratory. No external validation or
participant usability study is claimed; Monte Carlo errors are not sampling CIs.

The review excludes survey microdata, respondent identifiers and row-level
predictions. Reanalysis requires the provider-accessed data and frozen cohort
described in the repository. See release_manifest.json for exact artifact hashes.
''')
    with zipfile.ZipFile(package) as archive:
        assert len(archive.namelist()) == len(files) + 1
        for name in files:
            assert archive.read(name) == (ROOT / name).read_bytes()
    for name in ['Jawe_Publication_Methodology_Revision.docx',
                 'Jawe_Publication_Methodology_Revision.pdf', package.name]:
        shutil.copyfile(PAPER / name, Path('/workspace') / name)
    print(json.dumps({'package_members': len(files) + 1, 'zip_sha256': digest(package),
                      'report_pages': 6, 'original_Honours_files_unchanged': True}, indent=2))


if __name__ == '__main__':
    main()
