import Std

namespace Devs.Criticism

/-- A criticism pass only retains items that satisfy the supplied predicate.
Whether that predicate detects real errors is an empirical question. -/
def survivors (claims : List α) (accept : α → Bool) := claims.filter accept

theorem no_invented_claims (claims : List α) (accept : α → Bool) (x : α)
    (h : x ∈ survivors claims accept) : x ∈ claims := by
  exact (List.mem_filter.mp h).1

theorem survivors_satisfy_critic (claims : List α) (accept : α → Bool) (x : α)
    (h : x ∈ survivors claims accept) : accept x = true := by
  exact (List.mem_filter.mp h).2

theorem critic_idempotent (claims : List α) (accept : α → Bool) :
    survivors (survivors claims accept) accept = survivors claims accept := by
  simp [survivors, List.filter_filter]

theorem retained_truth_conditional (claims : List α) (accept : α → Bool)
    (trueClaim : α → Prop) (sound : ∀ x, accept x = true → trueClaim x)
    (x : α) (h : x ∈ survivors claims accept) : trueClaim x :=
  sound x (survivors_satisfy_critic claims accept x h)

/-- Counterexample: a bad critic can keep only the false item. Therefore there
is deliberately no theorem that arbitrary criticism improves accuracy. -/
theorem bad_critic_can_keep_only_false :
    survivors [true, false] (fun x => !x) = [false] := by decide

theorem agreement_can_preserve_error :
    survivors [false] (fun _ => true) = [false] := by decide

end Devs.Criticism
