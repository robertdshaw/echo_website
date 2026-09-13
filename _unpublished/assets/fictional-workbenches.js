// The interactive workbenches use fictional, local examples only.
const actorRecords = {
  authority: ['Port authority', 'Formal responsibility for the access procedure described in the fictional permit.', 'The published instrument, named office, scope of authority, and effective date.', 'Whether the procedure has been implemented at this terminal and whether another body has a separate approval role.'],
  operator: ['Operator', 'Responsibility for operating the fictional terminal and communicating its operating position.', 'The operating agreement, dated statement, and records that identify the activity and access category being described.', 'Whether a statement about an open terminal also describes ordinary contractor access at the relevant gate.'],
  workers: ['Worker representatives', 'A documented local position concerning entry and working conditions.', 'The underlying statement, its date, the group represented, and an independently recorded observation of the relevant activity.', 'Whether the account concerns every contractor, a particular shift, or one access point.'],
  counterparty: ['Service counterparty', 'A fictional service dependency that may require ordinary contractor access.', 'The relevant service scope, named entity, access requirement, and dated record of the dependency.', 'Whether the provider controls access, is affected by it, or can use an alternative operating arrangement.']
};
document.querySelectorAll('[data-actor]').forEach(button => button.addEventListener('click', () => {
  ['title','role','evidence','gap'].forEach((key,index) => { document.getElementById('actor-'+key).textContent = key === "title" ? headingCopy(actorRecords[button.dataset.actor][index]) : actorRecords[button.dataset.actor][index]; });
  document.querySelectorAll('[data-actor]').forEach(other => other.setAttribute('aria-pressed', String(other === button)));
}));
document.querySelectorAll('[data-ledger-filter]').forEach(button => button.addEventListener('click', () => {
  let count = 0;
  document.querySelectorAll('[data-ledger-state]').forEach(row => {
    row.hidden = button.dataset.ledgerFilter !== 'all' && row.dataset.ledgerState !== button.dataset.ledgerFilter;
    if (!row.hidden) count++;
  });
  document.querySelectorAll('[data-ledger-filter]').forEach(other => other.setAttribute('aria-pressed', String(other === button)));
  document.querySelector('#ledger-status').textContent = `${count} fictional record${count === 1 ? '' : 's'} shown.`;
}));
const pathwayRecords = {
  supported: ['Check scope before revising the assessment.', 'Confirm that the observed access applies to ordinary contractors, the relevant gate, and the stated period. An exceptional one-off entry does not resolve the broader question.', 'Record the new evidence, the prior assessment, the change in reasoning, and the next date for review.'],
  challenged: ['Test whether the restriction matches the question.', 'Identify the responsible office, activity, access category, and duration. Confirm that the document or observation actually concerns Terminal A during the resolution period.', 'Preserve the original assumption. Record the contrary evidence, surviving alternatives, and the reason for revising or retaining the assessment.'],
  unresolved: ['Keep the gap visible at the deadline.', 'A lack of adequate evidence is not proof that access is normal or restricted. Record the question as unresolved under its original rule and identify the observation still needed.', 'Do not change the outcome definition retrospectively. Record why the evidence was insufficient and what that means for the next research decision.']
};
document.querySelectorAll('[data-pathway]').forEach(button => button.addEventListener('click', () => {
  ['title','copy','record'].forEach((key,index) => { document.getElementById('pathway-'+key).textContent = key === "title" ? headingCopy(pathwayRecords[button.dataset.pathway][index]) : pathwayRecords[button.dataset.pathway][index]; });
  document.querySelectorAll('[data-pathway]').forEach(other => other.setAttribute('aria-pressed', String(other === button)));
}));
