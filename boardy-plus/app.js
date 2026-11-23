"use strict";

const element = id => document.getElementById(id);
const family = element("family");
const switches = ["provenance", "criticism", "revision"];
const limits = {answerable: 120, absent: 240, contradictory: 120, minimumImprovement: 0.2};
let step = 0;

function session() {
  const fixture = sessions[family.selectedIndex];
  const settings = Object.fromEntries(switches.map(id => [id, element(id).checked]));
  const draft = settings.provenance ? fixture.tagged : fixture.plain;
  const stages = [["Draft", draft[0]]];
  if (settings.criticism) stages.push(["Adversarial criticism", fixture.critique]);
  let final = draft;
  if (settings.revision) {
    final = settings.criticism ? fixture.revised
      : settings.provenance && fixture.uncriticizedWithProvenance ? fixture.uncriticizedWithProvenance
      : fixture.uncriticized;
  }
  if (settings.revision) stages.push(["Revision", final[0]]);
  return {fixture, settings, stages, final};
}

function paragraph(text) {
  const node = document.createElement("p");
  node.textContent = text;
  return node;
}

function transcript(id, stages) {
  element(id).replaceChildren(...stages.map(([title, content]) => {
    const li = document.createElement("li");
    const heading = document.createElement("strong");
    heading.textContent = title;
    li.append(heading, paragraph(content));
    return li;
  }));
}

function render() {
  const {fixture, stages, final} = session();
  element("category").textContent = fixture.tier + " · Fictional example";
  element("question").textContent = fixture.question;
  element("evidence").replaceChildren(...fixture.evidence.map(([id, text]) => paragraph(id + " · " + text)));
  transcript("baseline", step ? [["Direct answer", fixture.plain[0]]] : []);
  transcript("layer", stages.slice(0, step));
  element("progress").textContent = step ? "Stage " + step + " of " + stages.length : "Ready to replay";
  const complete = step === stages.length;
  element("next").disabled = complete;
  element("outcome").hidden = !complete;
  element("finding").textContent = "Boardy: " + fixture.plain[1] + " · Boardy+: " + final[1];
  element("note").textContent = complete && switches.every(id => element(id).checked)
    ? fixture.note : "The finding follows the selected scripted stages. Criticism only changes the submitted answer when revision is enabled.";
}

function reset() {
  step = 0;
  render();
}

for (const fixture of sessions) family.add(new Option(fixture.name, fixture.id));
family.addEventListener("change", reset);
for (const id of switches) element(id).addEventListener("change", reset);
element("reset").addEventListener("click", reset);
element("next").addEventListener("click", () => {
  step += 1;
  render();
});
element("export").addEventListener("click", () => {
  const {fixture, settings, stages, final} = session();
  const record = {
    simulation: true, heldOut: false, benchmarkStatus: "DRAFT_NOT_FROZEN_NOT_RUN",
    design: limits, fixtureId: fixture.id, tier: fixture.tier,
    question: fixture.question, sharedEvidence: fixture.evidence, settings,
    visibleStages: step, baseline: fixture.plain, layer: {stages, final}
  };
  const url = URL.createObjectURL(new Blob([JSON.stringify(record, null, 2)], {type: "application/json"}));
  const link = document.createElement("a");
  link.href = url;
  link.download = fixture.id + ".json";
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
render();
