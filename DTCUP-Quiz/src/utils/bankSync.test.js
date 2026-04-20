import test from 'node:test'
import assert from 'node:assert/strict'

import { shouldSyncBundledBank } from './bankSync.js'

test('syncs bundled bank when no questions are loaded', () => {
  assert.equal(
    shouldSyncBundledBank({
      currentBankName: null,
      currentQuestionCount: 0,
      bundledBank: { name: 'DTCUP Mega Bank', questions: [{ question: 'q1' }] },
    }),
    true,
  )
})

test('syncs bundled bank when stored bundled bank count is stale', () => {
  assert.equal(
    shouldSyncBundledBank({
      currentBankName: 'DTCUP Mega Bank',
      currentQuestionCount: 1002,
      bundledBank: { name: 'DTCUP Mega Bank', questions: new Array(2863).fill({ question: 'q' }) },
    }),
    true,
  )
})

test('does not sync when bundled bank is already current and counts match', () => {
  assert.equal(
    shouldSyncBundledBank({
      currentBankName: 'DTCUP Mega Bank',
      currentQuestionCount: 2863,
      bundledBank: { name: 'DTCUP Mega Bank', questions: new Array(2863).fill({ question: 'q' }) },
    }),
    false,
  )
})

test('does not replace a different custom bank', () => {
  assert.equal(
    shouldSyncBundledBank({
      currentBankName: '自定义题库',
      currentQuestionCount: 50,
      bundledBank: { name: 'DTCUP Mega Bank', questions: new Array(2863).fill({ question: 'q' }) },
    }),
    false,
  )
})
