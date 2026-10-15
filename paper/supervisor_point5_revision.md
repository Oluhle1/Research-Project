# Supervisor feedback point 5: software evaluation

Revision date: **15 October 2026**. Parent: `7c0a317`. Series baseline:
`f9bab60378a9b01ce5d6153194720cd52c736253`.

> Sections IV and VI.C (Software Evaluation): Distinguish technical software
> verification from usability evaluation. Avoid claims about user experience or
> usability without independent participant-based evidence.

**Status: revised in Sections IV and VI.C and checked against the saved
software record. Awaiting user review.** No participant was recruited. No
model was refitted, and the application suite was not rerun.

Section IV now separates the two evaluations. Technical verification compares
the program with specified expectations: screening decisions, excluded
predictors, links, repeated runs, reports, saved predictions, and command-line
versus Streamlit behaviour, including invalid inputs and outdated results.
Those tests ask whether the software follows the stated rules and returns the
same outputs. The owner's Windows walkthrough is part of that technical record.
The author ran the synthetic workflow locally, and the exported files were
compared with expected contents. The author is not an independent participant.
The walkthrough does not measure ease, errors or acceptance by someone else.

Usability evaluation is stated as a separate study. It would ask people other
than the developer to attempt set tasks and would record completion, time,
errors, ease and assistance. The written protocol for three to five consenting
users, restricted to synthetic records, has not been used. No task time, error
count, ease rating or acceptance result exists. Participant usability remains
untested. Filters, labels and reports are described as functions of the
program, not as measurements of user experience. An automated Streamlit test
is described as a check of program state, not as a session with a nontechnical
participant.

Section VI.C is now headed "Technical verification, separate from usability."
RQ3 asks whether the tool can repeat the analysis and clearly explain screening
decisions and model results. The completed evidence is limited to repetition
and to the presence of those explanations in the program. It does not show
that an independent person finds the explanations clear. Table IX is read as
layers of technical correctness and repeatability inside the tests that were
run. A matching reloaded score confirms the stored model. It does not estimate
performance for new people, and it does not show that a user understands the
distinction between historical out-of-fold results and an uploaded file. The
section states that the paper makes no claim about user experience, ease of
use, acceptance or success in ordinary work.

The abstract still says "No participant study tested ease of use." Its **141
whitespace tokens** are unchanged. Table IX is unchanged, including the row
"Participant usability | Not conducted." Section V.D still reports the saved
walkthrough counts and already limits that walkthrough to functions and
exports. Sections II.C, VI.E, VII and VIII already stated the usability limit
and were not rewritten. Tables, figures, results, screening rules, model code
and the application are unchanged. The builder was not changed.

The manuscript has **6,002 whitespace tokens**. The Word export has **nine
Letter pages**. The user deferred the eight-page limit and later format edits,
so this revision does not cut the added prose. Pages 5, 7 and 8 were inspected.
Page 5 contains the Section IV distinction. Page 7 keeps Table IX and the
walkthrough limit. Page 8 contains Section VI.C. Fresh checks passed **209
numerical and 103 supporting comparisons**, with zero failures, **317
claim-register rows** and four documented limits. This PDF was exported from
Microsoft Word with Times New Roman. No independent second-reviewer pass is
claimed. No screening rerun, model refit, application-suite run, participant
study or submission is claimed.

See [point 5 validation](supervisor_point5_validation.json),
[current manuscript validation](manuscript_validation.json),
[staged response](supervisor_feedback_response.md),
[PDF](Jawe_OPG_nonreceipt_KZN.pdf) and [Word](Jawe_OPG_nonreceipt_KZN.docx).

Points 3 and 4 remain as previously recorded and still await user review.
Points 6–10 remain pending.
