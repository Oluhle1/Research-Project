"""Draw aggregate diagnostics for the separately recorded validation extension."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'paper/publication/figures'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(qa_file: Path):
    qa_file = qa_file.resolve()
    if qa_file == ROOT or ROOT in qa_file.parents:
        raise ValueError('Controlled respondent-level input must stay outside Git')
    OUT.mkdir(parents=True, exist_ok=True)
    with np.load(qa_file) as qa:
        assert np.all(qa['coverage'] == 1)
        frame = pd.DataFrame({'p': qa['p_model'], 'y': qa['y']})
    frame['bin'] = pd.qcut(frame['p'], 5, duplicates='drop')
    bins = (frame.groupby('bin', observed=True)
            .agg(people=('y', 'size'), events=('y', 'sum'),
                 mean_predicted=('p', 'mean'), observed_nonreceipt=('y', 'mean'))
            .reset_index(drop=True))
    assert bins['people'].sum() == 1013 and bins['events'].sum() == 67
    bins.insert(0, 'quantile_bin', np.arange(1, len(bins) + 1))
    bins.to_csv(OUT / 'calibration_bins.csv', index=False)
    with plt.rc_context({'font.size': 10, 'axes.spines.top': False,
                         'axes.spines.right': False}):
        figure, axis = plt.subplots(figsize=(5.9, 4.8))
        limit = max(.22, float(bins[['mean_predicted', 'observed_nonreceipt']].max().max()) * 1.17)
        axis.plot([0, limit], [0, limit], color='.55', lw=1, label='Perfect agreement')
        axis.plot(bins['mean_predicted'], bins['observed_nonreceipt'], color='#26729b', lw=.8)
        axis.scatter(bins['mean_predicted'], bins['observed_nonreceipt'],
                     s=65, color='#26729b', zorder=3)
        for row in bins.itertuples():
            axis.annotate(f'{row.events}/{row.people}',
                          (row.mean_predicted, row.observed_nonreceipt),
                          xytext=(4, 7), textcoords='offset points', fontsize=8)
        axis.set(xlim=(0, limit), ylim=(0, limit),
                 xlabel='Mean held-out predicted probability',
                 ylabel='Observed reported non-receipt',
                 title='Original-category ridge: household-held-out calibration')
        axis.legend(frameon=False, fontsize=8, loc='lower right')
        figure.text(.5, .015, 'Five quantile bins; labels show events/people. Fixed split: seed 201415.\n'
                    'Descriptive bin summaries; no confidence intervals are plotted.',
                    ha='center', fontsize=8)
        figure.tight_layout(rect=(0, .07, 1, 1))
        figure.savefig(OUT / 'calibration.png', dpi=220)
        figure.savefig(OUT / 'calibration.pdf')
        plt.close(figure)

        metrics = pd.read_csv(ROOT / 'output/publication_validation/nested_metrics.csv')
        assert len(metrics) == 40 and metrics['valid'].all()
        groups = [metrics.loc[metrics['grouping'].eq(name)] for name in ['uqno', 'psu']]
        figure, axes = plt.subplots(1, 2, figsize=(7.3, 4.1))
        for axis, column, label in zip(axes, ['roc_auc', 'paired_brier_improvement'],
                                      ['AUC', 'Brier(reference) − Brier(ridge)']):
            values = [g[column].to_numpy() for g in groups]
            axis.boxplot(values, tick_labels=['Household', 'Derived PSU'], whis=(0, 100),
                         widths=.48, showfliers=False,
                         medianprops={'color': '#174e6a', 'linewidth': 1.7})
            for i, series in enumerate(values, 1):
                axis.scatter(i + np.linspace(-.085, .085, len(series)), series,
                             color='#26729b', s=12, alpha=.65)
            axis.set_ylabel(label)
            axis.grid(axis='y', color='.9', lw=.6)
        figure.text(.5, .02, '20 partitions per grouping, reusing the same cohort. Box: interquartile range; whiskers: range.\n'
                    'These are partition/refit sensitivity summaries, not confidence intervals.',
                    ha='center', fontsize=8)
        figure.tight_layout(rect=(0, .1, 1, 1))
        figure.savefig(OUT / 'partition_sensitivity.png', dpi=220)
        figure.savefig(OUT / 'partition_sensitivity.pdf')
        plt.close(figure)
    record = {'purpose': 'Aggregate held-out diagnostics for author review',
              'controlled_input_outside_repository': True,
              'controlled_input_sha256': digest(qa_file),
              'source_sha256': digest(Path(__file__)),
              'nested_metrics_sha256': digest(ROOT / 'output/publication_validation/nested_metrics.csv'),
              'no_row_level_predictions_exported': True,
              'files': {p.name: digest(p) for p in sorted(OUT.iterdir())
                        if p.name.startswith(('calibration', 'partition_sensitivity'))}}
    (OUT / 'diagnostic_manifest.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({'calibration_bins': len(bins), 'people': 1013, 'events': 67,
                      'output_directory': str(OUT)}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--qa-file', type=Path, required=True)
    build(parser.parse_args().qa_file)
