import Std

namespace Devs.Agency

structure Proposal where
  actionId : Nat
  revision : Nat
  deriving DecidableEq, Repr

/-- Authorization refers to this exact action and revision. This type models
the interface contract, not the trustworthiness of a real human or UI. -/
structure Authorized (permit : Proposal → Prop) where
  proposal : Proposal
  evidence : permit proposal

def execute (permit : Proposal → Prop) (a : Authorized permit) : Proposal := a.proposal

theorem execution_has_permission (permit : Proposal → Prop) (a : Authorized permit) :
    permit (execute permit a) := a.evidence

theorem no_authorized_value_without_permission (permit : Proposal → Prop)
    (h : ∀ p, ¬permit p) : ¬Nonempty (Authorized permit) := by
  rintro ⟨a⟩
  exact h a.proposal a.evidence

theorem approval_for_one_revision_does_not_cover_another
    (id oldRevision newRevision : Nat) (h : oldRevision ≠ newRevision) :
    (Proposal.mk id newRevision) ≠ (Proposal.mk id oldRevision) := by
  intro eq
  have : newRevision = oldRevision := congrArg Proposal.revision eq
  exact h this.symm

end Devs.Agency
