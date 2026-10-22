import Std

namespace Devs.Provenance

inductive Status where
  | proposed | derived | simulated | observed | replicated
  | contradicted | superseded | unknown
  deriving DecidableEq, Repr

structure Citation where
  document : String
  revision : String
  firstLine : Nat
  lastLine : Nat
  deriving Repr

def Citation.valid (c : Citation) : Prop :=
  c.document ≠ "" ∧ c.revision ≠ "" ∧ 0 < c.firstLine ∧ c.firstLine ≤ c.lastLine

structure Claim where
  status : Status
  references : List Citation
  deriving Repr

def grounded (c : Claim) : Prop := ∃ r ∈ c.references, r.valid
def observedEvidence (c : Claim) : Prop :=
  (c.status = .observed ∨ c.status = .replicated) ∧ grounded c

theorem observed_requires_reference (c : Claim) (h : observedEvidence c) :
    c.references ≠ [] := by
  rcases h.2 with ⟨r, hr, _⟩
  intro hempty
  simp [hempty] at hr

theorem proposed_is_not_observed (c : Claim) (h : c.status = .proposed) :
    ¬observedEvidence c := by simp [observedEvidence, h]

theorem simulation_is_not_observation (c : Claim) (h : c.status = .simulated) :
    ¬observedEvidence c := by simp [observedEvidence, h]

theorem derivation_is_not_observation (c : Claim) (h : c.status = .derived) :
    ¬observedEvidence c := by simp [observedEvidence, h]

/-- An acyclic dependency certificate assigns a strictly increasing natural
rank to each dependency edge. The rank certificate is an assumption to audit. -/
def Ranked (edge : α → α → Prop) (rank : α → Nat) : Prop :=
  ∀ a b, edge a b → rank a < rank b

theorem ranked_no_self_dependency (edge : α → α → Prop) (rank : α → Nat)
    (h : Ranked edge rank) (x : α) : ¬edge x x := by
  intro hx
  have := h x x hx
  omega

theorem ranked_no_two_cycle (edge : α → α → Prop) (rank : α → Nat)
    (h : Ranked edge rank) (a b : α) : ¬(edge a b ∧ edge b a) := by
  rintro ⟨hab, hba⟩
  have := h a b hab
  have := h b a hba
  omega

inductive Path (edge : α → α → Prop) : α → α → Prop where
  | single : edge a b → Path edge a b
  | next : Path edge a b → edge b c → Path edge a c

theorem path_increases_rank (edge : α → α → Prop) (rank : α → Nat)
    (h : Ranked edge rank) (p : Path edge a b) : rank a < rank b := by
  induction p with
  | single he => exact h _ _ he
  | next _ he ih => exact Nat.lt_trans ih (h _ _ he)

theorem ranked_no_cycle (edge : α → α → Prop) (rank : α → Nat)
    (h : Ranked edge rank) (x : α) : ¬Path edge x x := by
  intro p
  have := path_increases_rank edge rank h p
  omega

end Devs.Provenance
