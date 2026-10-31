"""
Lab 6 - BRANCH COVERAGE tests for hospital_triage_priority.py

Goal: make every decision evaluate to BOTH True and False
(>= 90% branch coverage), including loop-entry / loop-exit branches
and short-circuit sub-conditions.

Run:
    coverage run --branch -m pytest BranchCoverageTest_hospital_triage_priority.py
    coverage report -m
"""
import pytest
from hospital_triage_priority import process_triage_wards, monitor_oxygen_manifolds


def make_ward(patients, accepting=True, tier="general", icu=False):
    return {
        "is_accepting": accepting,
        "tier": tier,
        "icu_standby": icu,
        "patients": patients,
    }


# ---------- Line 2: `not isinstance(...) or score < 0` ----------

def test_wards_not_a_list_raises():                 # isinstance False -> True branch
    with pytest.raises(ValueError):
        process_triage_wards({"tier": "general"}, 10)


def test_negative_score_raises():                   # isinstance OK, score < 0 True
    with pytest.raises(ValueError):
        process_triage_wards([], -5)


def test_zero_score_is_valid():                     # score < 0 False (boundary 0)
    assert process_triage_wards([make_ward([{"spo2": 98, "hr": 72}])], 0) == {
        "acuity_score": 0, "status": "NO_URGENT_CASES"}


# ---------- Line 8 / 9: ward loop + is_accepting ----------

def test_empty_ward_list_skips_loop():              # outer for: never entered
    assert process_triage_wards([], 10)["status"] == "NO_URGENT_CASES"


def test_ward_not_accepting_skipped():              # is_accepting False -> continue
    wards = [make_ward([{"spo2": 98, "hr": 72}], accepting=False)]
    assert process_triage_wards(wards, 10)["acuity_score"] == 0


def test_missing_is_accepting_defaults_false():     # .get default False
    assert process_triage_wards([{"patients": [{"spo2": 98, "hr": 72}]}], 10)["acuity_score"] == 0


def test_ward_with_no_patients_key():               # inner for: empty default list
    assert process_triage_wards([{"is_accepting": True}], 10)["status"] == "NO_URGENT_CASES"


# ---------- Line 20: `spo2 <= 0 or heart_rate <= 0` ----------

def test_spo2_zero_flagged():                       # first operand True
    r = process_triage_wards([make_ward([{"spo2": 0, "hr": 80}])], 10)
    assert r["acuity_score"] == 0


def test_hr_zero_flagged():                         # first False, second True
    r = process_triage_wards([make_ward([{"spo2": 98, "hr": 0}])], 10)
    assert r["acuity_score"] == 0


def test_negative_vitals_flagged():
    r = process_triage_wards([make_ward([{"spo2": -1, "hr": -1}])], 10)
    assert r["acuity_score"] == 0


# ---------- Line 24-29: unconscious branches ----------

def test_unconscious_general_ward_adds_100():       # unconscious True, tier != outpatient
    r = process_triage_wards([make_ward([{"spo2": 95, "hr": 80, "unconscious": True}])], 10)
    assert r["acuity_score"] == 100


def test_unconscious_outpatient_resets_and_breaks():  # tier == outpatient -> reset + break
    patients = [{"spo2": 98, "hr": 72},
                {"spo2": 95, "hr": 80, "unconscious": True},
                {"spo2": 98, "hr": 72}]             # 3rd patient never processed
    r = process_triage_wards([make_ward(patients, tier="outpatient")], 10)
    assert r["acuity_score"] == 0


def test_outpatient_break_only_ends_that_ward():    # later wards still counted
    wards = [
        make_ward([{"spo2": 95, "hr": 80, "unconscious": True}], tier="outpatient"),
        make_ward([{"spo2": 98, "hr": 72}]),
    ]
    assert process_triage_wards(wards, 10)["acuity_score"] == 10


def test_conscious_outpatient_not_reset():          # outpatient but not unconscious
    r = process_triage_wards([make_ward([{"spo2": 98, "hr": 72}], tier="outpatient")], 10)
    assert r["acuity_score"] == 10


# ---------- Line 30: `spo2 < 90 or hr > 120` ----------

def test_low_spo2_adds_60():                        # first operand True
    assert process_triage_wards([make_ward([{"spo2": 89, "hr": 80}])], 10)["acuity_score"] == 60


def test_high_hr_adds_60():                         # first False, second True
    assert process_triage_wards([make_ward([{"spo2": 95, "hr": 121}])], 10)["acuity_score"] == 60


def test_boundary_values_are_normal():              # spo2 == 90, hr == 120 -> else
    assert process_triage_wards([make_ward([{"spo2": 90, "hr": 120}])], 7)["acuity_score"] == 7


def test_default_vitals_used_when_missing():        # .get defaults (95 / 75)
    assert process_triage_wards([make_ward([{}])], 10)["acuity_score"] == 10


# ---------- Line 35: icu_standby ----------

def test_icu_standby_true_adds_25():
    assert process_triage_wards([make_ward([{"spo2": 98, "hr": 72}], icu=True)], 10)["acuity_score"] == 35


def test_icu_standby_false_adds_nothing():
    assert process_triage_wards([make_ward([{"spo2": 98, "hr": 72}], icu=False)], 10)["acuity_score"] == 10


# ---------- Line 38 / 40: final status ----------

def test_exactly_four_flagged_is_not_alert():       # flagged > 4 False (boundary)
    patients = [{"spo2": 0, "hr": 80} for _ in range(4)]
    r = process_triage_wards([make_ward(patients)], 10)
    assert r["status"] == "NO_URGENT_CASES"


def test_five_flagged_triggers_ward_alert():        # flagged > 4 True (boundary)
    patients = [{"spo2": 0, "hr": 80} for _ in range(5)]
    r = process_triage_wards([make_ward(patients)], 10)
    assert r == {"acuity_score": 0, "status": "WARD_ALERT"}


def test_ward_alert_keeps_score():
    patients = [{"spo2": 95, "hr": 80, "unconscious": True} for _ in range(5)]
    r = process_triage_wards([make_ward(patients)], 10)
    assert r == {"acuity_score": 500, "status": "WARD_ALERT"}


def test_triage_stable_when_score_positive():
    r = process_triage_wards([make_ward([{"spo2": 98, "hr": 72}])], 10)
    assert r["status"] == "TRIAGE_STABLE"


# ---------- monitor_oxygen_manifolds ----------

def test_oxygen_empty_list_no_data():
    assert monitor_oxygen_manifolds([]) == "NO_DATA"


def test_oxygen_none_no_data():
    assert monitor_oxygen_manifolds(None) == "NO_DATA"


def test_oxygen_two_consecutive_low_fails():        # streak reaches 2
    assert monitor_oxygen_manifolds([[5.0, 3.0, 3.5]]) == "PRESSURE_FAILURE"


def test_oxygen_single_low_not_failure():           # streak == 1 only (>= 2 False)
    assert monitor_oxygen_manifolds([[5.0, 3.0, 5.0]]) == "PRESSURE_NORMAL"


def test_oxygen_streak_reset_between_lows():        # else branch resets streak
    assert monitor_oxygen_manifolds([[3.0, 5.0, 3.0, 5.0]]) == "PRESSURE_NORMAL"


def test_oxygen_boundary_4_0_is_normal():           # 4.0 is NOT < 4.0
    assert monitor_oxygen_manifolds([[4.0, 4.0, 4.0]]) == "PRESSURE_NORMAL"


def test_oxygen_failure_in_later_manifold():        # streak reset per manifold
    assert monitor_oxygen_manifolds([[5.0, 5.0], [3.0, 3.0]]) == "PRESSURE_FAILURE"


def test_oxygen_low_across_manifolds_not_combined():
    assert monitor_oxygen_manifolds([[5.0, 3.0], [3.0, 5.0]]) == "PRESSURE_NORMAL"


def test_oxygen_empty_manifold_inner_loop_skipped():
    assert monitor_oxygen_manifolds([[]]) == "PRESSURE_NORMAL"
