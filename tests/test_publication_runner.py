"""Procedure-level checks using synthetic households, never survey respondents."""
from pathlib import Path
import json
import sys
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
import publication_model as model
import run_publication_validation as runner


def synthetic(groups=60):
    rows = []
    for i in range(groups):
        for member in range(1 + (i % 3 == 0)):
            rows.append({"uqno": f"HH{i:03d}", "psu": f"PSU{i:03d}",
                "person_weight": "1", "y": str(int(i % 3 == 0)),
                "age": str(60 + (i + member) % 30), "sex": str(1 + i % 2),
                "schooling_raw": "5" if i % 2 else "12",
                "settlement": ["1", "2", "4", "5"][i % 4], "welfare_distance": "2"})
    return model.prepare_frame(pd.DataFrame(rows))


CONFIG = {"outer_folds": 3, "inner_folds": 3, "c_grid": [.1]}


class RunnerTests(unittest.TestCase):
    def test_nested_coverage_and_training_only_reference(self):
        work = synthetic()
        result = runner.nested_repetition(work, "uqno", 123, CONFIG)
        self.assertTrue(result["row"]["valid"])
        qa = result["qa"]
        np.testing.assert_array_equal(qa["coverage"], np.ones(len(work)))
        for fold in range(1, 4):
            training = work.iloc[qa["outer_fold"] != fold]
            np.testing.assert_array_equal(qa["p_reference"][qa["outer_fold"] == fold],
                                          np.full(sum(qa["outer_fold"] == fold), training["y_n"].mean()))
        direct = np.mean((qa["y"] - qa["p_reference"]) ** 2) - np.mean((qa["y"] - qa["p_model"]) ** 2)
        self.assertAlmostEqual(result["row"]["paired_brier_improvement"], direct, places=14)

    def test_household_sample_preserves_multiplicity_and_original_groups(self):
        work = synthetic()
        boot, oob, support = runner.sample_households(work, 739)
        self.assertEqual(support["draws"], work["uqno"].nunique())
        self.assertLess(support["unique_households"], support["draws"])
        original_sizes = work.groupby("uqno").size()
        sampled_sizes = boot.groupby("uqno").size()
        self.assertTrue(((sampled_sizes / original_sizes.loc[sampled_sizes.index]) % 1 == 0).all())
        self.assertTrue(set(boot["uqno"]).isdisjoint(oob["uqno"]))
        self.assertEqual(list(boot.index), list(range(len(boot))))
        folds = model.group_folds(boot, "uqno", 71, n_splits=3)
        check = pd.DataFrame({"household": boot["uqno"], "fold": folds})
        self.assertEqual(check.groupby("household")["fold"].nunique().max(), 1)

    def test_invalid_bootstrap_draw_is_logged_without_redraw(self):
        work = synthetic()
        error = model.UnsupportedSampleError("deliberate synthetic failure")
        with patch.object(runner, "sample_households", wraps=runner.sample_households) as sampler:
            with patch.object(model, "tune_and_fit", side_effect=error):
                result = runner.bootstrap_replicate(work, 730001, 1, CONFIG)
        self.assertEqual(sampler.call_count, 1)
        self.assertFalse(result["row"]["valid"])
        self.assertEqual(result["row"]["seed"], 730001)
        self.assertEqual(result["row"]["replicate"], 1)
        self.assertIn("deliberate", result["row"]["error"])

    def test_paired_bootstrap_deltas_and_optimism_sign(self):
        work = synthetic()
        result = runner.bootstrap_replicate(work, 730002, 2, CONFIG)
        row = result["row"]
        self.assertTrue(row["valid"])
        self.assertAlmostEqual(row["delta_paired_brier_improvement"],
                               row["delta_reference_brier"] - row["delta_brier"], places=14)
        apparent = {"brier": .05, "roc_auc": .8, "reference_brier": .06, "paired_brier_improvement": .01}
        draws = pd.DataFrame({"valid": [True, True, False], "delta_brier": [.01, .02, 100],
            "delta_roc_auc": [-.05, -.03, 100], "delta_reference_brier": [.002, .004, 100],
            "delta_paired_brier_improvement": [-.008, -.016, 100]})
        summary = {r["metric"]: r for r in runner.optimism_summary(apparent, draws)}
        self.assertAlmostEqual(summary["brier"]["optimism_corrected_estimate"], .065)
        self.assertAlmostEqual(summary["roc_auc"]["optimism_corrected_estimate"], .76)
        self.assertEqual(summary["brier"]["valid_replicates"], 2)
        self.assertAlmostEqual(summary["brier"]["correction_MCSE"], .005)
        self.assertAlmostEqual(summary["paired_brier_improvement"]["optimism_corrected_estimate"], -.002)

    def test_public_and_private_output_destinations(self):
        runner.validate_destinations(runner.DEFAULT_OUTPUT, Path("/tmp/controlled-qa"), False)
        with self.assertRaises(ValueError):
            runner.validate_destinations(runner.ROOT / "output/phase5", None, False)
        with self.assertRaises(ValueError):
            runner.validate_destinations(runner.DEFAULT_OUTPUT, runner.ROOT / "qa", False)
        with self.assertRaises(ValueError):
            runner.validate_destinations(runner.DEFAULT_OUTPUT, None, True)

    def test_all_invalid_bootstrap_retains_zero_valid_denominator(self):
        apparent = {"brier": .05, "roc_auc": .8, "reference_brier": .06,
                    "paired_brier_improvement": .01}
        rows = runner.optimism_summary(apparent, pd.DataFrame({"valid": [False, False]}))
        for row in rows:
            self.assertEqual(row["valid_replicates"], 0)
            self.assertTrue(np.isnan(row["optimism_corrected_estimate"]))
            self.assertTrue(np.isnan(row["correction_MCSE"]))

    def test_oob_failure_does_not_invalidate_successful_bootstrap_correction(self):
        original = model.metrics
        calls = []
        def diagnostic_failure(y, probability):
            calls.append(len(y))
            if len(calls) == 3:
                raise model.UnsupportedSampleError("synthetic OOB diagnostic failure")
            return original(y, probability)
        with patch.object(model, "metrics", side_effect=diagnostic_failure):
            result = runner.bootstrap_replicate(synthetic(), 730002, 2, CONFIG)
        row = result["row"]
        self.assertEqual(len(calls), 3)
        self.assertTrue(row["valid"])
        self.assertFalse(row["oob_valid"])
        self.assertTrue(np.isfinite(row["delta_brier"]))
        self.assertIn("diagnostic", row["oob_error"])
        self.assertNotIn("error", row)

    def test_configuration_drift_is_rejected_before_fitting(self):
        config = json.loads(runner.DEFAULT_CONFIG.read_text())
        runner.validate_config(config, 827)
        for name, altered in [("solver", "liblinear"), ("bootstrap_resample_size_households", 826),
                               ("outer_seed_start", 22), ("inner_folds", 4)]:
            with self.subTest(field=name):
                changed = {**config, name: altered}
                with self.assertRaisesRegex(ValueError, name):
                    runner.validate_config(changed, 827)


if __name__ == "__main__":
    unittest.main()
