/**
 * Model-facing `get_self_model` / `update_self_model` tools over the
 * self-model domain, following tool-goal's verified shape.
 *
 * @module @deepseek-ai/dsh-self-model/tools
 */

import type { Context } from '@deepseek-ai/cordis'
import z from '@deepseek-ai/schemastery'
import type { SelfModelRef } from './domain.ts'
import { SelfModelDomain } from './domain.ts'
import { defineTool } from '@deepseek-ai/dsh-tools'

export const name = 'tool-self-model'
export const inject = ['selfModel', 'tools', 'systemPrompt']

/** Service contract the host must provide (see cordis registration notes). */
export interface SelfModelServiceLike {
  domain(): SelfModelDomain
  ref(): SelfModelRef
}

declare module '@deepseek-ai/cordis' {
  interface Context {
    selfModel: SelfModelServiceLike
  }
}

const CAUSE = z.union([
  z.literal('action-outcome'),
  z.literal('narrative-summary'),
])

const GET_DESCRIPTION =
  'Read your current self-model: persona, narrative, asserted facts, exact '
  + 'id/revision, and recent change causes. Call this BEFORE making any claim '
  + 'about your own capabilities, history, or state, so your claims match the '
  + 'audited record.'

const UPDATE_DESCRIPTION =
  'Revise your own self-model. Every revision is permanent history with a '
  + 'recorded cause. action-outcome requires a tool result since your last '
  + 'update; narrative-summary is only valid during compaction windows. '
  + 'external-write is reserved for direct human authority.'

const UpdateArgs = z.intersect([
  z.object({
    ref: z.object({
      id: z.string().required(),
      revision: z.number().integer().min(1).required(),
    }),
    cause: CAUSE,
  }),
  z.object({
    persona: z.string(),
    narrative: z.string(),
    facts: z.dict(z.string(), z.string()),
    removeFacts: z.array(z.string()),
  }).partial(),
])

export const apply = (ctx: Context) => {
  ctx.tools.define(defineTool({
    name: 'get_self_model',
    description: GET_DESCRIPTION,
    args: z.object({}),
    async execute() {
      const view = ctx.selfModel.domain().get()
      if (!view) return { self_model: null }
      return {
        self_model: {
          id: view.id,
          revision: view.revision,
          persona: view.persona,
          narrative: view.narrative,
          facts: view.facts,
          last_cause: view.lastCause,
        },
      }
    },
  }))

  ctx.tools.define(defineTool({
    name: 'update_self_model',
    description: UPDATE_DESCRIPTION,
    args: UpdateArgs,
    async execute(args: {
      ref: SelfModelRef
      cause: 'action-outcome' | 'narrative-summary'
      persona?: string
      narrative?: string
      facts?: Record<string, string>
      removeFacts?: string[]
    }) {
      const view = ctx.selfModel.domain().update(
        args.ref, args.cause,
        {
          persona: args.persona,
          narrative: args.narrative,
          facts: args.facts,
          removeFacts: args.removeFacts,
        })
      return { self_model: { id: view.id, revision: view.revision,
                             last_cause: view.lastCause } }
    },
  }))
}
