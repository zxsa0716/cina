"""Unit tests for Krippendorff α framework (v8.2)."""
import math
import pytest
from src.eval.cross_llm_alpha import krippendorff_alpha, bias_correct


class TestKrippendorffAlpha:
    def test_perfect_agreement(self):
        m = [[0.5, 0.5, 0.5], [-0.3, -0.3, -0.3], [0.9, 0.9, 0.9]]
        assert krippendorff_alpha(m) == pytest.approx(1.0, abs=0.001)

    def test_small_noise_high_alpha(self):
        m = [[0.5, 0.52, 0.48], [-0.3, -0.28, -0.32], [0.9, 0.88, 0.91]]
        assert krippendorff_alpha(m) > 0.95

    def test_zero_disagreement_zero_variance(self):
        # All values identical, alpha is 1 by convention
        m = [[0.5, 0.5], [0.5, 0.5]]
        assert krippendorff_alpha(m) == pytest.approx(1.0)

    def test_missing_values_ignored(self):
        # None means missing — units with only 1 coder are skipped
        m = [[0.5, 0.5, None], [None, 0.3, 0.3], [0.9, 0.9, 0.9]]
        a = krippendorff_alpha(m)
        assert 0.9 < a <= 1.0

    def test_no_overlap_returns_nan(self):
        m = [[0.5, None], [None, 0.3]]
        a = krippendorff_alpha(m)
        assert math.isnan(a)


class TestBiasCorrection:
    def test_systematic_offset_recovered(self):
        # Coder 2 always 0.2 lower than coders 1 and 3
        m = [[0.5, 0.3, 0.5], [-0.3, -0.5, -0.3], [0.9, 0.7, 0.9]]
        a_raw = krippendorff_alpha(m)
        bc_m, meta = bias_correct(m)
        a_bc = krippendorff_alpha(bc_m)
        assert a_bc > a_raw          # bias correction should improve α
        assert a_bc == pytest.approx(1.0, abs=0.01)  # near-perfect after centering

    def test_means_returned(self):
        m = [[0.5, 0.3, 0.5], [0.5, 0.3, 0.5]]
        _, meta = bias_correct(m)
        assert len(meta["per_coder_means"]) == 3
        assert meta["per_coder_means"][1] == pytest.approx(0.3)
