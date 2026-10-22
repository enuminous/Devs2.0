import Std

namespace Devs.Benchmark

/-- Integer basis points, not floating-point arithmetic. -/
structure Decision where
  effect : Int
  lower : Int
  upper : Int
  ordered : lower ≤ upper
  tokenWithinCap : Bool
  utilityPass : Bool
  frozen : Bool
  independentReplication : Bool
  deriving Repr

def passes (d : Decision) : Prop :=
  2000 ≤ d.effect ∧ 0 < d.lower ∧ d.tokenWithinCap = true ∧ d.utilityPass = true
def killed (d : Decision) : Prop := d.upper ≤ 1000
def supported (d : Decision) : Prop :=
  passes d ∧ d.frozen = true ∧ d.independentReplication = true

/-- Disjointness additionally needs the point estimate inside its interval.
We state that assumption explicitly; percentile intervals need not contain
every possible statistic automatically. -/
theorem pass_and_kill_disjoint (d : Decision) (inside : d.effect ≤ d.upper) :
    ¬(passes d ∧ killed d) := by
  rintro ⟨hp, hk⟩
  have := hp.1
  unfold killed at hk
  omega

theorem draft_never_supported (d : Decision) (h : d.frozen = false) :
    ¬supported d := by simp [supported, h]

theorem replication_required (d : Decision) (h : supported d) :
    d.independentReplication = true := h.2.2

theorem headroom_required (a c : Int) (nonnegative : 0 ≤ c)
    (gain : 2000 ≤ a - c) : 2000 ≤ a := by omega

theorem paired_difference (bothFalse improves worsens : Int) :
    (bothFalse + improves) - (bothFalse + worsens) = improves - worsens := by omega

theorem approved_sample_total : 120 + 240 + 120 = (480 : Nat) := by decide

theorem approved_margin_example : 10000 * (48 : Nat) = 2000 * 240 := by decide

/-- Strict low-gain classification is not logical proof that the gain is zero. -/
theorem no_decision_example :
    ¬(2000 ≤ (1500 : Int)) ∧ ¬((2300 : Int) ≤ 1000) := by decide

end Devs.Benchmark
