"""Meaningful isolation/grouping safeguards for the new publication procedure.

Run without pytest: python -m unittest discover -s tests -p test_publication_validation.py
"""
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
from scipy.special import expit

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
import publication_model as model


def synthetic(n_groups=40):
    rows = []
    for i in range(n_groups):
        for member in range(1 + (i % 3 == 0)):
            rows.append({
                "uqno": f"HH{i:03d}", "psu": f"PSU{i:03d}", "person_weight": "1",
                "y": str(int(i % 3 == 0)), "age": str(60 + (i * 3 + member) % 29),
                "sex": str(1 + (i + member) % 2),
                "schooling_raw": "5" if i % 2 else "12",
                "settlement": ["1", "2", "4", "5"][i % 4],
                "welfare_distance": "2" if i % 2 else "6",
            })
    return pd.DataFrame(rows)


class PublicationValidationTests(unittest.TestCase):
    def test_unseen_rows_and_labels_do_not_change_training_preprocessing(self):
        work = model.prepare_frame(synthetic())
        training, test = work.iloc[:30].copy(), work.iloc[30:].copy()
        training.loc[training.index[0], "age_per_10"] = np.nan
        training.loc[training.index[1], "school_code"] = None
        original = model.learn_preprocessor(training)
        expected = model.transform(training, original)
        test["age_per_10"] = 1e9
        test["school_code"] = "unseen"
        test["y_n"] = 1 - test["y_n"]
        model.transform(test, original)
        self.assertEqual(model.learn_preprocessor(training), original)
        np.testing.assert_array_equal(model.transform(training, original), expected)
        changed_labels = training.copy()
        changed_labels["y_n"] = 1 - changed_labels["y_n"]
        self.assertEqual(model.learn_preprocessor(changed_labels), original)

    def test_identifier_outcome_and_income_columns_cannot_enter_predictors(self):
        raw = synthetic()
        initial = model.prepare_frame(raw)
        state = model.learn_preprocessor(initial)
        matrix = model.transform(initial, state)
        poisoned = raw.copy()
        poisoned["y"] = (1 - poisoned["y"].astype(int)).astype(str)
        poisoned["uqno"] = [f"different{i}" for i in range(len(raw))]
        poisoned["psu"] = "other"
        poisoned["person_weight"] = "100000"
        for forbidden in ["personno", "applicant_private_income", "opg_income_annual",
                          "reason_codes", "eligibility_status", "in_final_cohort"]:
            poisoned[forbidden] = poisoned["y"]
        altered = model.prepare_frame(poisoned)
        np.testing.assert_array_equal(model.transform(altered, state), matrix)
        self.assertEqual(matrix.shape[1], 7)
        self.assertNotIn("settle_traditional_or_rural", model.SLOPE_NAMES)

    def test_bootstrap_copies_of_original_households_never_split(self):
        work = model.prepare_frame(synthetic(60))
        # Duplicated index labels as well as duplicated original household IDs.
        duplicated = pd.concat([work, work.iloc[:35], work.iloc[:20]], ignore_index=False)
        folds = model.group_folds(duplicated, "uqno", 77)
        check = pd.DataFrame({"hh": duplicated["uqno"].to_numpy(), "fold": folds})
        self.assertEqual(check.groupby("hh")["fold"].nunique().max(), 1)
        for outer in range(5):
            training = duplicated.iloc[folds != outer]
            test = duplicated.iloc[folds == outer]
            self.assertTrue(set(training["uqno"]).isdisjoint(test["uqno"]))
            inner = model.group_folds(training, "uqno", 80 + outer)
            for fold in range(5):
                self.assertTrue(set(training.iloc[inner != fold]["uqno"]).isdisjoint(
                    training.iloc[inner == fold]["uqno"]))

    def test_household_with_multiple_psus_is_rejected_before_preparation_or_folding(self):
        raw = synthetic(45)
        self.assertEqual(raw.loc[0, "uqno"], raw.loc[1, "uqno"])
        invalid = raw.copy()
        invalid.loc[1, "psu"] = "a different PSU"
        with self.assertRaisesRegex(model.UnsupportedSampleError, "exactly one PSU"):
            model.prepare_frame(invalid)
        prepared = model.prepare_frame(raw)
        prepared.loc[1, "psu"] = "a different PSU"
        for group_col in ("uqno", "psu"):
            with self.subTest(group_col=group_col):
                with self.assertRaisesRegex(model.UnsupportedSampleError, "exactly one PSU"):
                    model.group_folds(prepared, group_col, 17)

    def test_penalty_tie_and_failed_candidate_handling(self):
        records = [
            {"C": 3.0, "pooled_inner_brier": .1, "all_inner_converged": True},
            {"C": .1, "pooled_inner_brier": .1, "all_inner_converged": True},
            {"C": .01, "pooled_inner_brier": .001, "all_inner_converged": False},
        ]
        self.assertEqual(model.select_penalty(records), .1)
        with self.assertRaises(model.UnsupportedSampleError):
            model.select_penalty(records[-1:])

    def test_selection_follows_pooled_loss_even_when_fold_means_prefer_other_c(self):
        records = [
            {"C": .1, "pooled_inner_brier": .10, "mean_fold_brier": .07,
             "all_inner_converged": True},
            {"C": 3., "pooled_inner_brier": .09, "mean_fold_brier": .08,
             "all_inner_converged": True},
        ]
        self.assertEqual(model.select_penalty(records), 3.)

    def test_absent_training_category_keeps_original_seven_column_design(self):
        work = model.prepare_frame(synthetic(45))
        work["settlement_code"] = work["settlement_code"].replace("5", "1")
        fitted = model.tune_and_fit(work, "uqno", 523, c_grid=[.1], n_splits=3)
        test = work.iloc[:2].copy()
        test["settlement_code"] = "5"
        train_matrix = model.transform(work, fitted.state)
        test_matrix = model.transform(test, fitted.state)
        self.assertEqual(train_matrix.shape[1], 7)
        np.testing.assert_array_equal(train_matrix[:, 5], np.zeros(len(work)))
        np.testing.assert_array_equal(test_matrix[:, 5], np.ones(len(test)))
        self.assertEqual(fitted.coefficients_original_scale()["settle_rural_formal"], 0)
        self.assertTrue(np.isfinite(fitted.predict(test)).all())

    def test_failed_tuning_and_final_fit_preserve_attempt_audit(self):
        work = model.prepare_frame(synthetic(40))
        original_fit = model._fit_logistic
        def nonconverged(matrix, y, penalty):
            estimator, _, iterations = original_fit(matrix, y, penalty)
            return estimator, False, iterations
        with patch.object(model, "_fit_logistic", side_effect=nonconverged):
            with self.assertRaises(model.UnsupportedSampleError) as context:
                model.tune_and_fit(work, "uqno", 111, c_grid=[.1, 1.], n_splits=3)
        error = context.exception
        self.assertEqual(len(error.inner_records), 6)
        self.assertEqual(len(error.grid_records), 2)
        self.assertFalse(error.final_attempted)
        def final_nonconverged(matrix, y, penalty):
            estimator, converged, iterations = original_fit(matrix, y, penalty)
            return estimator, converged and len(y) < len(work), iterations
        with patch.object(model, "_fit_logistic", side_effect=final_nonconverged):
            with self.assertRaises(model.UnsupportedSampleError) as context:
                model.tune_and_fit(work, "uqno", 111, c_grid=[.1], n_splits=3)
        error = context.exception
        self.assertEqual(len(error.inner_records), 3)
        self.assertTrue(error.final_attempted)
        self.assertFalse(error.final_converged)

    def test_tuning_uses_pooled_person_loss_not_mean_fold_loss(self):
        work = model.prepare_frame(synthetic(30))
        calls = []
        class DummyEstimator:
            def __init__(self, p):
                self.p = p
            def predict_proba(self, matrix):
                return np.column_stack([np.full(len(matrix), 1 - self.p),
                                        np.full(len(matrix), self.p)])
        def dummy_fit(matrix, y, penalty):
            # Deliberately different training prevalences across unequal folds.
            p = float(np.mean(y))
            calls.append((len(y), p))
            return DummyEstimator(p), True, 1
        with patch.object(model, "_fit_logistic", side_effect=dummy_fit):
            fitted = model.tune_and_fit(work, "uqno", 991, c_grid=[.1], n_splits=3)
        rows = fitted.inner_records
        pooled = sum(row["brier"] * row["test_people"] for row in rows) / len(work)
        self.assertAlmostEqual(fitted.grid_records[0]["pooled_inner_brier"], pooled, places=15)
        self.assertNotAlmostEqual(pooled, np.mean([row["brier"] for row in rows]), places=10)
        self.assertEqual(fitted.fit_count_attempted, 4)

    def test_nested_tuning_learns_each_preprocessor_without_its_validation_households(self):
        work = model.prepare_frame(synthetic(45))
        folds = model.group_folds(work, "uqno", 717, n_splits=3)
        # A validation-only extreme would noticeably alter a full-data scale.
        work.loc[folds == 0, "age_per_10"] = 10000.0
        captured = []
        original = model.learn_preprocessor
        def tracked(training):
            state = original(training)
            captured.append((set(training["uqno"]), state))
            return state
        with patch.object(model, "learn_preprocessor", side_effect=tracked):
            model.tune_and_fit(work, "uqno", 717, c_grid=[.1], n_splits=3)
        self.assertEqual(len(captured), 4)
        for fold in range(3):
            self.assertTrue(captured[fold][0].isdisjoint(work.iloc[folds == fold]["uqno"]))
            self.assertEqual(captured[fold][1], original(work.iloc[folds != fold]))
        self.assertLess(captured[0][1].means[0], 10)
        self.assertGreater(captured[-1][1].means[0], 100)
        self.assertEqual(captured[-1][0], set(work["uqno"]))

    def test_real_fitted_predictions_ignore_heldout_outcomes_and_extra_fields(self):
        work = model.prepare_frame(synthetic(45))
        fitted = model.tune_and_fit(work, "uqno", 422, c_grid=[.1], n_splits=3)
        expected = fitted.predict(work)
        test = work.copy()
        test["y_n"] = 1 - test["y_n"]
        test["uqno"] = "an entirely different ID"
        test["applicant_private_income"] = test["y_n"] * 1e10
        np.testing.assert_array_equal(fitted.predict(test), expected)
        coefficients = fitted.coefficients_original_scale()
        raw = model._unscaled_matrix(work, fitted.state.age_median, fitted.state.category_modes)
        expected_logit = coefficients["intercept"] + raw @ np.array(
            [coefficients[name] for name in model.SLOPE_NAMES])
        np.testing.assert_allclose(expit(expected_logit), expected, rtol=1e-12, atol=1e-14)

    def test_calibration_recovers_known_binomial_probabilities(self):
        p = np.repeat([.1, .3, .6, .8], 100)
        y = np.concatenate([np.r_[np.ones(k), np.zeros(100 - k)] for k in [10, 30, 60, 80]])
        result = model.metrics(y, p)
        self.assertAlmostEqual(result["calibration_in_the_large"], 0, places=10)
        self.assertAlmostEqual(result["calibration_slope"], 1, places=6)
        self.assertTrue(result["calibration_slope_valid"])
        constant = model.metrics(y, np.repeat(y.mean(), len(y)))
        self.assertAlmostEqual(constant["calibration_in_the_large"], 0, places=10)
        self.assertTrue(np.isnan(constant["calibration_slope"]))
        self.assertEqual(constant["calibration_status"], "constant_prediction")
        separated = model.metrics(np.array([0, 0, 1, 1]), np.array([.1, .2, .8, .9]))
        self.assertFalse(separated["calibration_slope_valid"])
        self.assertTrue(np.isnan(separated["calibration_slope"]))
        self.assertEqual(separated["calibration_status"], "complete_or_quasi_separation")

    def test_invalid_codes_stay_missing_until_training_imputation(self):
        raw = synthetic()
        raw.loc[0, "schooling_raw"] = "not a code"
        raw.loc[1, "welfare_distance"] = np.nan
        raw.loc[2, "schooling_raw"] = "22"
        raw.loc[3, "settlement"] = "3"
        raw.loc[4, "sex"] = "99"
        work = model.prepare_frame(raw)
        for row, field in [(0, "school_code"), (1, "welfare_code"),
                           (2, "school_code"), (3, "settlement_code"), (4, "sex_code")]:
            self.assertTrue(pd.isna(work.loc[row, field]))
        self.assertTrue(np.isfinite(model.transform(work, model.learn_preprocessor(work))).all())

    def test_unsupported_event_grouping_fails_instead_of_relaxing_groups(self):
        work = model.prepare_frame(synthetic(9))
        with self.assertRaises(model.UnsupportedSampleError):
            model.group_folds(work, "uqno", 1, n_splits=5)
        with self.assertRaises(model.UnsupportedSampleError):
            model.metrics(np.zeros(5), np.repeat(.1, 5))


if __name__ == "__main__":
    unittest.main()
