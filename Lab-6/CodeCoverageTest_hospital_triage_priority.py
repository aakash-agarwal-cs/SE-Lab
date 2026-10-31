"""
Lab 6 - CODE (LINE) COVERAGE tests for hospital_triage_priority.py

Goal: execute every line of the module at least once (>= 90% line coverage).

Run:
    coverage run -m pytest CodeCoverageTest_hospital_triage_priority.py
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


# ---------- process_triage_wards ----------

def test_single_normal_patient():
    # Provided example: stable patient adds default acuity score
    wards = [make_ward([{"spo2": 98, "hr": 72, "unconscious": False}])]
    result = process_triage_wards(wards, 10)
    assert result == {"acuity_score": 10, "status": "TRIAGE_STABLE"}


def test_invalid_wards_type_raises():
    # line 3: raise ValueError
    with pytest.raises(ValueError):
        process_triage_wards("not a list", 10)


def test_negative_default_score_raises():
    with pytest.raises(ValueError):
        process_triage_wards([], -1)


def test_ward_not_accepting_is_skipped():
    # line 10: continue
    wards = [make_ward([{"spo2": 98, "hr": 72}], accepting=False)]
    result = process_triage_wards(wards, 10)
    assert result == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_invalid_vitals_are_flagged_and_skipped():
    # lines 21-22: spo2 <= 0 or hr <= 0
    wards = [make_ward([{"spo2": 0, "hr": 80}])]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 0
    assert result["status"] == "NO_URGENT_CASES"


def test_unconscious_patient_adds_100():
    # lines 25-26, 29: unconscious in non-outpatient ward
    wards = [make_ward([{"spo2": 95, "hr": 80, "unconscious": True}])]
    result = process_triage_wards(wards, 10)
    assert result == {"acuity_score": 100, "status": "TRIAGE_STABLE"}


def test_unconscious_in_outpatient_resets_score():
    # lines 27-28: total_acuity reset to 0 and break
    wards = [make_ward(
        [{"spo2": 98, "hr": 72},
         {"spo2": 95, "hr": 80, "unconscious": True},
         {"spo2": 98, "hr": 72}],
        tier="outpatient")]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 0
    assert result["status"] == "NO_URGENT_CASES"


def test_low_spo2_adds_60():
    # line 31
    wards = [make_ward([{"spo2": 85, "hr": 80}])]
    assert process_triage_wards(wards, 10)["acuity_score"] == 60


def test_icu_standby_adds_25():
    # line 36
    wards = [make_ward([{"spo2": 98, "hr": 72}], icu=True)]
    assert process_triage_wards(wards, 10)["acuity_score"] == 35


def test_ward_alert_when_more_than_four_flagged():
    # line 39: flagged_entries > 4
    patients = [{"spo2": 0, "hr": 80} for _ in range(5)]
    result = process_triage_wards([make_ward(patients)], 10)
    assert result["status"] == "WARD_ALERT"


def test_no_urgent_cases_with_empty_wards():
    # line 41
    assert process_triage_wards([], 10) == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


# ---------- monitor_oxygen_manifolds ----------

def test_oxygen_no_data():
    # line 46
    assert monitor_oxygen_manifolds([]) == "NO_DATA"


def test_oxygen_pressure_failure():
    # lines 47-55: two consecutive low readings
    assert monitor_oxygen_manifolds([[5.0, 3.5, 3.0]]) == "PRESSURE_FAILURE"


def test_oxygen_pressure_normal():
    # lines 56-58: streak reset, normal return
    assert monitor_oxygen_manifolds([[5.0, 3.5, 5.0, 3.9, 6.0]]) == "PRESSURE_NORMAL"
