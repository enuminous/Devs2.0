import Std

namespace Devs.Budget

structure Usage where
  input : Nat
  output : Nat
  cached : Nat
  cachedWithinInput : cached ≤ input

def total (u : Usage) := u.input + u.output
def appendTotal (spent : Nat) (u : Usage) := spent + total u

theorem cached_input_still_counted (u : Usage) : u.cached ≤ total u := by
  have := u.cachedWithinInput
  unfold total
  omega

theorem append_never_reduces (spent : Nat) (u : Usage) :
    spent ≤ appendTotal spent u := by unfold appendTotal total; omega

theorem bounded_step (spent cap : Nat) (u : Usage)
    (h : total u ≤ cap - spent) (hs : spent ≤ cap) :
    appendTotal spent u ≤ cap := by unfold appendTotal; omega

theorem stage_allocations_equal : 256 + 256 + 512 = (1024 : Nat) := by decide

theorem cache_discount_does_not_reduce_token_total (input output c₁ c₂ : Nat)
    (h₁ : c₁ ≤ input) (h₂ : c₂ ≤ input) :
    total ⟨input, output, c₁, h₁⟩ = total ⟨input, output, c₂, h₂⟩ := rfl

end Devs.Budget
