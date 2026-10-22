import Devs

def main : IO Unit := do
  let sampleTotal := (120 + 240 + 120 : Nat)
  let pool := (256 + 256 + 512 : Nat)
  let margin := 10000 * 48 / 240
  let badCritic := Devs.Criticism.survivors [true, false] (fun x => !x)
  let badCriticKeepsFalse := badCritic == [false]
  IO.println ("{\"sample_total\":" ++ toString sampleTotal ++
    ",\"critic_output_pool\":" ++ toString pool ++
    ",\"margin_basis_points\":" ++ toString margin ++
    ",\"bad_critic_keeps_false\":" ++ toString badCriticKeepsFalse ++
    ",\"physics_validation\":false}")
