import Std

/-! Predicate models of the paper's CollapseΩ. These are ordinary constraint
intersections; they make no claim about physical wavefunction collapse. -/
namespace Devs.Possibility

abbrev Space (α : Type) := α → Prop
def update (s evidence : Space α) : Space α := fun x => s x ∧ evidence x
def included (a b : Space α) : Prop := ∀ x, a x → b x
def expand (s alternatives : Space α) : Space α := fun x => s x ∨ alternatives x

theorem update_sound (s e : Space α) : included (update s e) s :=
  fun _ h => h.1

theorem update_satisfies_evidence (s e : Space α) : included (update s e) e :=
  fun _ h => h.2

theorem update_idempotent (s e : Space α) (x : α) :
    update (update s e) e x ↔ update s e x := by
  simp [update]

theorem independent_constraints_commute (s e f : Space α) (x : α) :
    update (update s e) f x ↔ update (update s f) e x := by
  simp [update, and_comm, and_left_comm]

theorem incompatible_evidence_empties (s e : Space α)
    (h : ∀ x, s x → ¬e x) : ¬∃ x, update s e x := by
  rintro ⟨x, hs, he⟩
  exact h x hs he

theorem expansion_keeps_old (s alternatives : Space α) :
    included s (expand s alternatives) := fun _ h => Or.inl h

theorem expansion_admits_new (s alternatives : Space α) (x : α)
    (h : alternatives x) : expand s alternatives x := Or.inr h

theorem evidence_then_expansion_can_reopen :
    expand (update (fun _ : Bool => True) (fun x => x = false))
      (fun x => x = true) true := by
  exact Or.inr rfl

end Devs.Possibility
