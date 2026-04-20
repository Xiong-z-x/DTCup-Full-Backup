export function shouldSyncBundledBank({ currentBankName, currentQuestionCount, bundledBank }) {
  const bundledQuestionCount = bundledBank?.questions?.length ?? 0

  if (bundledQuestionCount === 0) {
    return false
  }

  if ((currentQuestionCount ?? 0) === 0) {
    return true
  }

  return currentBankName === bundledBank?.name && currentQuestionCount !== bundledQuestionCount
}
