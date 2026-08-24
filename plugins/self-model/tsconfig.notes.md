# Integration notes — placing these files into the DeepSeek Harness monorepo

These plugin files live outside the DSH monorepo and therefore cannot typecheck
here (the `@deepseek-ai/*` packages resolve only inside `tools/deepseek-harness/`).
They were written against the verified idioms of:

- `packages/goal/goal/src/types.ts` (Branded id, Ref, Snapshot, View shapes)
- `packages/goal/goal/src/fold.ts` (strict revision+1 CAS fence)
- `packages/goal/tool-goal/src/index.ts` (defineTool surface, inject array,
  schemastery Config style, JSDoc conventions)

## Placement

```bash
# domain + tools become a package sibling of tool-goal:
cp plugins/self-model/domain.ts  tools/deepseek-harness/packages/self-model/domain/src/index.ts
cp plugins/self-model/tools.ts   tools/deepseek-harness/packages/self-model/tool-self-model/src/index.ts
```

## Imports that resolve after placement

| import in our files | resolves via |
|---|---|
| `@deepseek-ai/dsh-brand` | existing workspace package (used by dsh-goal types) |
| `@deepseek-ai/dsh-tools` | workspace package providing `defineTool` |
| `@deepseek-ai/cordis` | framework context |
| `./domain.ts` | sibling file in same package |

## cordis registration (two lines)

```yaml
# in the profile/plugin bundle yaml alongside cognitive-architecture:
packages:
  - '@deepseek-ai/dsh-self-model'        # provides ctx.selfModel service
  - '@deepseek-ai/dsh-tool-self-model'   # registers the two model-facing tools
```

The host must supply `ctx.selfModel: { domain(), ref() }` backed by
`SelfModelDomain` (domain.ts). Authority rules live INSIDE the domain, so the
tool layer cannot bypass them; `external-write` is unreachable from the model
surface by construction (schema enum excludes it).

## Verification status

Pattern-fidelity reviewed against the real goal sources; NOT compiled here
(monorepo build requires Linux landlock packages — known macOS limitation).
Compile gate runs on the Linux CI box or WSL before first remote-battery use.
