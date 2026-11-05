// Validate diagram.json with FlowStory's own validator (vendored, pinned).
// Usage: node validate.mjs
import { readFileSync } from 'node:fs';
import { validateDiagram } from './vendor/flowstory/flowstory.min.js';

const diagram = JSON.parse(readFileSync(new URL('./diagram.json', import.meta.url)));
const result = validateDiagram(diagram);
const errors = Array.isArray(result) ? result : (result?.errors ?? []);
const flows = diagram.flows;
// Extra checks the schema cannot do: every step references existing nodes.
for (const [key, flow] of Object.entries(flows)) {
  flow.steps.forEach((s, i) => {
    for (const ref of [s.from, s.to, s.target].filter(Boolean)) {
      if (!diagram.nodes[ref]) errors.push(`flows.${key}.steps[${i}]: unknown node '${ref}'`);
    }
  });
}
for (const [key, muts] of Object.entries(diagram.inspector?.mutations ?? {})) {
  muts.forEach(m => {
    if (m.step < 1 || m.step > flows[key].steps.length) errors.push(`inspector.${key}: step ${m.step} out of range`);
  });
}
if (errors.length) { console.error(errors.join('\n')); process.exit(1); }
console.log(`diagram.json valid: ${Object.keys(diagram.nodes).length} nodes, ${Object.keys(flows).length} flows`);
