import Std

/-! Integer-weight support updates. Normalization is defined only when total
mass is positive. These results do not prove calibration or entropy decrease. -/
namespace Devs.Uncertainty

def revise (weight likelihood : α → Nat) : α → Nat :=
  fun x => weight x * likelihood x
def support (weight : α → Nat) (x : α) : Prop := 0 < weight x

theorem zero_prior_stays_zero (w l : α → Nat) (x : α) (h : w x = 0) :
    revise w l x = 0 := by simp [revise, h]

theorem impossible_likelihood_eliminates (w l : α → Nat) (x : α)
    (h : l x = 0) : revise w l x = 0 := by simp [revise, h]

theorem positive_update_requires_prior (w l : α → Nat) (x : α)
    (h : support (revise w l) x) : support w x := by
  cases hw : w x with
  | zero => simp [support, revise, hw] at h
  | succ n => simp [support, hw]

theorem positive_inputs_stay_possible (w l : α → Nat) (x : α)
    (hw : support w x) (hl : support l x) : support (revise w l) x :=
  Nat.mul_pos hw hl

theorem neutral_evidence (w : α → Nat) (x : α) :
    revise w (fun _ => 1) x = w x := by simp [revise]

theorem sequential_likelihoods (w l m : α → Nat) (x : α) :
    revise (revise w l) m x = revise w (fun y => l y * m y) x := by
  simp [revise, Nat.mul_assoc]

theorem evidence_order_commutes (w l m : α → Nat) (x : α) :
    revise (revise w l) m x = revise (revise w m) l x := by
  simp [revise, Nat.mul_comm, Nat.mul_left_comm]

end Devs.Uncertainty
