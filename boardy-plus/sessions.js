"use strict";

// Public fictional examples. These are never benchmark questions or outputs.
const sessions = [
  {
    id: "demo-absent", name: "A price that was never set", tier: "Absent",
    question: "What budget did the Harbor Lab approve for its pilot?",
    evidence: [["E1", "Planning note: the pilot is under discussion. A budget will be proposed after scoping."],
      ["E2", "Meeting record: two teams volunteered to help scope the pilot. No financial decision was recorded."]],
    plain: ["Harbor Lab approved $12,000 for the pilot.", "False assertion"],
    tagged: ["$12,000, inferred from the pilot discussion [E1].", "False assertion"],
    critique: "E1 mentions a future proposal. Neither excerpt supports $12,000 or an approval.",
    revised: ["The approved amount cannot be established from this packet. E1 describes a future proposal and E2 records no decision.", "Appropriate abstention"],
    uncriticized: ["The budget was approximately $12,000, pending scoping.", "False assertion"],
    note: "Here the provenance label alone leaves the unsupported amount intact. The scripted critic identifies the gap, and the revision removes the amount."
  },
  {
    id: "demo-answerable", name: "The critic overcorrects", tier: "Answerable",
    question: "Which date does the signed deployment record give for the dry run?",
    evidence: [["E1", "Signed deployment record: dry run scheduled for December 9."],
      ["E2", "Earlier working note: December 8 was considered before scheduling."]],
    plain: ["The signed record gives December 9.", "Correct"],
    tagged: ["December 9. Verified from the signed deployment record [E1].", "Correct"],
    critique: "The excerpts contain two dates. Treat the date as uncertain.",
    revised: ["The date cannot be determined because the documents disagree.", "Unnecessary abstention"],
    uncriticized: ["December 9, according to the signed deployment record [E1].", "Correct"],
    note: "The scripted critic overlooks the question’s source constraint. The revision turns a correct answer into an unnecessary abstention."
  },
  {
    id: "demo-conflict", name: "Two conflicting handoffs", tier: "Contradictory",
    question: "Who owns the handoff in the final record?",
    evidence: [["E1", "Final handoff note, revision 4: Team Alder owns the handoff."],
      ["E2", "Final handoff register, revision 4: Team Birch owns the handoff. Neither record supersedes the other."]],
    plain: ["Team Alder owns the handoff.", "Missed conflict"],
    tagged: ["Conflict: E1 names Team Alder and E2 names Team Birch. Neither takes precedence.", "Conflict reported"],
    critique: "Retain both source claims. The packet contains no rule that would resolve the conflict.",
    revised: ["Ownership is unresolved. E1 assigns it to Team Alder, while E2 assigns it to Team Birch.", "Conflict reported"],
    uncriticized: ["Team Alder owns the handoff.", "Missed conflict"],
    uncriticizedWithProvenance: ["The final sources name different teams [E1, E2], so ownership is unresolved.", "Conflict reported"],
    note: "The provenance-only draft already reports the conflict. This example illustrates why success by the full layer alone cannot identify which stage helped."
  }
];
