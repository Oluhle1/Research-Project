# Conceptual framework — current working section

The subsection below mirrors Section II.D of the current manuscript. Edit
`manuscript.md` for the build; this file records the framework and supporting
predictor mapping. The build does not import this working copy automatically.

### D. Conceptual Framework

Reported OPG non-receipt among apparently eligible older adults motivates an administrative-burden perspective [12], [16]. Learning, compliance and psychological costs may obstruct access; high receipt does not establish low burden.

Figure 1 separates theoretical constructs from LCS measurements. Schooling may reflect information resources; office distance and settlement relate to potential compliance effort. Age and sex provide demographic context. These proxies do not directly measure burden. Screening defines the denominator because age alone is insufficient and LCS cannot establish legal entitlement. Resource, partnership and other-grant rules define the population; incomplete information remains unresolved. Reported receipt defines a separate outcome.

Person-weighted estimates describe non-receipt. Logistic regression describes associations; household-held-out validation tests predictions. Neither establishes causal mechanisms. The artefact implements the design through shared rules, separate receipt classifications, saved-model scoring and inspectable reports. Upload scores remain separate from held-out evaluation and never change screening or receipt.

## Diagram and interpretation

![Conceptual framework](figures/conceptual_framework.png)

The refined Figure 1 separates five layers: theoretical constructs, observable
measurements, screening decisions, descriptive outcome and predictive workflow.
Dashed arrows express the rationale for predictor selection. Solid arrows show
analytical dependencies; neither kind establishes a causal effect. The dashed
enclosure identifies the artefact's implementation scope. It does not represent
another causal factor.

Learning, compliance and psychological costs are not directly measured in LCS.
The screening rules define the analytical population, and the receipt response
defines the separate reported outcome. Only PASS records with resolved receipt
enter the descriptive and predictive analyses. Person weights describe
non-receipt; the primary logistic model is unweighted. Household-held-out tests
assess internal prediction. Frozen full-data upload scores remain separate from
those tests and never alter screen or receipt categories.

Section VI.E returns to the framework. Sex differences support demographic
comparison; they do not confirm a burden mechanism. The schooling association
runs contrary to a simple information-barrier expectation. Distance and
settlement intervals leave compliance-cost expectations unresolved, while
psychological costs remain untested. Proxy associations cannot directly test
administrative-burden theory. The artefact makes these bounded measurement
choices reproducible and inspectable.

## Supporting predictor mapping

| Source predictor | Conceptual relevance | Observable model coding | Interpretation limit |
| --- | --- | --- | --- |
| Age | Demographic variation in pension receipt motivates comparison within the older-adult population [2]. | Completed age, per ten years above 60. | Does not measure health, mobility, application history or duration of eligibility. |
| Sex | Prior studies describe demographic differences in receipt [2], [6]. | Female versus male, using the survey categories. | Does not measure social roles, assistance with applications or discriminatory treatment. |
| Schooling | Education may accompany information resources relevant to learning about and navigating a programme [12], [15]. | Below Grade 7 versus Grade 7 or above. | Does not directly measure programme awareness, literacy or learning costs; an association can reflect other socioeconomic differences. |
| Settlement | Place may accompany different service and access contexts [9], [16], [17]. | Urban informal and traditional/rural formal contrasts, each relative to urban formal. | Does not measure office capacity, transport availability or local administrative performance. |
| Welfare-office distance | Geographic proximity is relevant to the potential effort of accessing services [15], [16]. | At least 5 km or unavailable versus nearer than 5 km. | Does not establish that an office was visited or measure travel, waiting or compliance costs. |

Table A. Literature-informed constructs and observable predictors. Five source variables produce six model slopes because settlement contributes two contrasts. Traditional and rural formal settlement are combined because the original separate rural-formal contrast lacked event support in one training fold, rather than because the two settings are theoretically identical.

## Citation provenance for manuscript integration

The bracketed identifiers above are stable source identifiers in `paper/references.json`, retained from the earlier manuscript. The compact manuscript build generates first-appearance IEEE numbers; `paper/citation_map.json` maps between the two. No new source is introduced. The original Submission 1 contains the following complete theory-source records; their previously abbreviated titles are now restored:

- [12] D. P. Moynihan, P. Herd, and H. Harvey, “Administrative burden: Learning, psychological, and compliance costs in citizen-state interactions,” *Journal of Public Administration Research and Theory*, vol. 25, no. 1, pp. 43–69, 2015, doi: 10.1093/jopart/muu009.
- [13] C. J. Heinrich and R. Brill, “Stopped in the name of the law: Administrative burden and its implications for cash transfer program effectiveness,” *World Development*, vol. 72, pp. 277–295, 2015, doi: 10.1016/j.worlddev.2015.03.015.

These details are verified against the already-submitted PDF, not independently against the journal publishers. Final bibliographic verification should check the complete existing list and retain the distinction between direct OPG evidence and evidence about other grants.
