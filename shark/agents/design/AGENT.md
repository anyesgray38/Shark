# SHARK Agent Framework

The agent system is organized as **Markdown-defined agents + executable scripts**.

## Contract

- `AGENT.md` defines mission, constraints, inputs, outputs, evidence rules, and handoffs.
- `*.md` files hold domain knowledge, procedures, scoring rules, and workflow definitions.
- Python scripts execute deterministic operations and route work according to the Markdown contract.
- Agents never silently promote research into production behavior.
- Research claims must preserve provenance and validation state.

## Routing

1. Orchestrator reads the requested workflow.
2. It loads the relevant agent `AGENT.md` files.
3. It executes only the scripts permitted by the workflow.
4. Outputs are passed to the next agent with validation metadata.
5. Validator can reject any result that violates evidence or statistical requirements.
6. Reporter produces the final research artifact.
