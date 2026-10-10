const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
        ShadingType, VerticalAlign, PageNumber, ImageRun, Column, SectionType } = require("docx");
const fs = require("fs");

const FONT = "Times New Roman";
const NAVY = "1F4E79";
const RULE = { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" };
const BORDERS = { top: RULE, bottom: RULE, left: RULE, right: RULE };
const NO = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const NOB = { top: NO, bottom: NO, left: NO, right: NO };
const PAGE = {
  size: { width: 12240, height: 15840 },
  margin: { top: 864, bottom: 792, left: 864, right: 864, header: 432, footer: 432 },
};
const COL_W = 5040;

function r(text, o = {}) {
  return new TextRun({
    text,
    font: FONT,
    size: o.size ?? 20,
    bold: o.bold,
    italics: o.italics,
    color: o.color,
  });
}

function para(children, o = {}) {
  return new Paragraph({
    spacing: { before: o.before ?? 0, after: o.after ?? 80, line: o.line ?? 230 },
    alignment: o.align,
    children: Array.isArray(children) ? children : [r(children, o)],
  });
}

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: NAVY, space: 1 } },
    spacing: { before: 160, after: 80, line: 230 },
    children: [r(text, { bold: true, size: 22, color: NAVY })],
  });
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 120, after: 60, line: 230 },
    children: [r(text, { bold: true, italics: true, size: 20 })],
  });
}

function caption(text) {
  return para([r(text, { bold: true, size: 16 })], { before: 100, after: 40, line: 200 });
}

function note(text) {
  return para([r(text, { italics: true, size: 15 })], { before: 20, after: 80, line: 200 });
}

function cell(text, width, header) {
  return new TableCell({
    borders: BORDERS,
    width: { size: width, type: WidthType.DXA },
    shading: header ? { fill: "1F4E79", type: ShadingType.CLEAR } : undefined,
    margins: { top: 28, bottom: 28, left: 40, right: 40 },
    verticalAlign: VerticalAlign.CENTER,
    children: [new Paragraph({
      spacing: { before: 0, after: 0, line: 180 },
      children: [r(text, { size: 14, bold: header, color: header ? "FFFFFF" : "000000" })],
    })],
  });
}

function table(headers, rows, widths) {
  const all = [headers, ...rows];
  return new Table({
    width: { size: COL_W, type: WidthType.DXA },
    columnWidths: widths,
    rows: all.map((row, i) => new TableRow({
      cantSplit: true,
      children: row.map((value, j) => cell(String(value), widths[j], i === 0)),
    })),
  });
}

const img = fs.readFileSync("C:/Users/oluhl/Desktop/research skills/output/runs/primary/calibration_plot.png");

const title = [
  para([r("Reported Non-Receipt of the Older Person\u2019s Grant among Apparently Eligible Adults in KwaZulu-Natal", { bold: true, size: 28 })], { align: AlignmentType.CENTER, after: 120, line: 276 }),
  para([r("Oluhle Jawe", { size: 22 })], { align: AlignmentType.CENTER, after: 0 }),
  para([r("ICT Honours (21634436), PRIC401", { italics: true, size: 18 })], { align: AlignmentType.CENTER, after: 0 }),
  para([r("Durban University of Technology, Durban, South Africa", { size: 18 })], { align: AlignmentType.CENTER, after: 140 }),
  para([r("Abstract\u2014", { bold: true, italics: true, size: 18 }), r("Reported non-receipt of South Africa\u2019s Older Person\u2019s Grant was estimated for adults aged 60 and older in KwaZulu-Natal in the Living Conditions Survey 2014/2015. An observable screen identified 1,013 apparently eligible adults. Sixty-seven reported non-receipt (6.6% unweighted; 7.5% person-weighted). Across stated eligibility alternatives the weighted figure stayed between 7.1% and 9.1%, and it was most sensitive to retention of people who reported their own disability grant. A six-predictor logistic model, scored on held-out households, had a ROC area of 0.75 and a Brier score of 0.058, against 0.062 for a constant risk. Sex and schooling carried the ranking. Settlement and welfare-office distance did not. One command reproduced the cohort, and 26 pre-specified screening decisions matched the program. The estimate describes reported receipt in a historical survey. It does not determine legal eligibility.", { size: 18 })], { after: 80, line: 220 }),
  para([r("Keywords\u2014", { bold: true, italics: true, size: 18 }), r("Older Person\u2019s Grant, non-receipt, Living Conditions Survey, logistic regression, reproducibility.", { size: 18 })], { after: 60, line: 220 }),
];

const body = [
  h1("I. Introduction"),
  para("The Older Person\u2019s Grant is the main cash transfer for adults aged 60 and older in South Africa. Research has shown that receipt is associated with consumption, health, and household welfare, and that reaching a grant office can be costly [2], [6], [16]. Much less is known about how many older adults who look eligible on a transparent survey screen nevertheless report that they do not receive the grant."),
  para("This paper estimates that quantity for KwaZulu-Natal in the Living Conditions Survey 2014/2015 and asks whether a small set of survey characteristics can rank reported non-receipt. Three questions organise the study. What proportion of the screened population reports non-receipt, and how does the proportion change when the eligibility rules change? How well does a small logistic model discriminate and calibrate on held-out households? Can a computational artefact reproduce the analysis and expose the screening decision for a person?"),
  para("\u201CApparently eligible\u201D means that the adult passes observable age, income, partnership, and grant-compatibility rules. It does not mean that the South African Social Security Agency would approve an application [1]. The contribution is a documented screen, a weighted description, an internally validated model, and a command that rebuilds all three."),

  h1("II. Related Work"),
  para("Two strands of evidence sit beside this question, and they answer different things. One strand estimates what happens after an older person receives the grant, including consumption and crisis response [8]. Those results do not identify who reports non-receipt. The other strand describes access. Godfrey and colleagues relate demographic characteristics to grant receipt among eligible households [6]. Ralston and colleagues compare rural pensioners with rural non-pensioners [2]. Work on the Child Support Grant in KwaZulu-Natal and elsewhere describes distance, documentation, and exclusion during application [9], [10], [14], [15]. Travel, waiting, and encounters with the payment system are part of that cost [12], [13], [16], and digital access conditions have been discussed as a further constraint [17]."),
  para("Those studies motivate candidate predictors. They do not provide a person-level OPG non-receipt rate for a screened KwaZulu-Natal sample, and they do not separate an income screen from a prediction model. A model of a rare event also needs more than a ROC area: precision should be read beside prevalence, and predicted probabilities should be checked against observed frequencies [19], [20]. Sample size and grouped validation constrain how sharp that check can be [21], [22]. The analysis below follows that reporting discipline [23]."),

  h1("III. Methods"),
  h2("A. Data and study population"),
  para("The data are the person, household, and person-income files of Statistics South Africa\u2019s Living Conditions Survey 2014/2015, with the released metadata, questionnaire, and COICOP codes [3]\u2013[5]. The frame is adults aged 60 or older, in completed years, living in sampled KwaZulu-Natal households. The unit is the person. The realised national sample and the provincial response rate describe the survey, not the analysis cohort. The household sample does not represent institutionalised older adults."),
  h2("B. Eligibility screen and outcome"),
  para("Person records were linked to households and to person-level annual income on the survey identifiers. The resource proxy sums nominal annualised income and excludes social-assistance grant codes. A missing income row is zero only when the person was marked as having no listed income source. Household totals were not allocated to individuals, and asset acquisitions were not treated as an assessable asset stock."),
  para("The income ceiling is the private income at which the statutory formula still pays R100 a month. It is R61,800 for a single person and R123,600 for a couple from the April 2014 grant maximum, and R64,680 and R129,360 from the April 2015 maximum [24], [25]. Each adult is screened with the ceiling in force in the interview month. Income at the ceiling passes. A married adult with a resident spouse who can be linked is screened on the couple ceiling. Never-married, widowed, and divorced adults are screened on the single ceiling. Living together, separated, and missing-spouse cases stay unresolved and are not moved onto the single ceiling. An own disability grant or war-veterans grant fails the primary screen. Caregiver child grants and grant-in-aid do not. Among people who pass, reported non-receipt is Y = 1 and reported receipt is Y = 0. Contradictory or unexplained grant answers stay out of the model. Disagreement with preceding-year OPG income is flagged and does not change Y."),
  h2("C. Model"),
  para("The predictors are age per ten years above 60, sex, schooling below Grade 7 versus Grade 7 or above, settlement, and welfare-office distance. The reference levels are male, Grade 7 or above, urban formal, and a welfare office nearer than 5 km. Rural formal settlement has one non-recipient in the final cohort, and the training fold that held that person out did not converge. Traditional area and rural formal are therefore one contrast. The retained model has six slopes and an intercept. Marital status is used in the screen and is not a predictor. Missing schooling class and missing welfare distance are filled with the training-fold mode. The outcome and the income proxy are not predictors."),
  para("The estimator is unweighted logistic regression, without class balancing and without a classification threshold. Validation is five-fold and keeps every member of a household in one fold. Households are stratified by whether any member reports non-receipt. The seed is 201415. Metrics on the pooled held-out predictions are average precision, ROC area, Brier score, calibration-in-the-large, and calibration slope. An intercept-only prediction, equal to the training-fold prevalence, is the reference for probability error. Uncertainty for the fixed predictions uses 1,000 household resamples. Person weights are used for the descriptive proportion. Strata were not released, so design-based intervals are not available."),

  h1("IV. Computational Artefact"),
  para("The minimum artefact is a Python command, python analysis/run_study.py. It reads the three survey files, applies the versioned screen, writes the cohort and the weighted description, and refits the held-out model. The run record stores rule version opg-kzn-primary-v1, the six slopes, the seed, software versions, and checksums of inputs and outputs. Cohort membership, reason codes, and fold identifiers are columns in the output files. A review interface and an exploratory random forest were not part of this command."),

  h1("V. Results"),
  h2("A. Cohort and reported non-receipt"),
  para("The KwaZulu-Natal files contain 15,388 people in 3,686 households. Of 1,317 adults aged 60 or older, 1,013 pass the screen and have a resolved grant answer (Table I). They include 946 recipients and 67 non-recipients. Another 117 fail a known rule and 187 remain unresolved. Of the failures, 93 are above the income ceiling and 25 report an own disability grant, one person being in both groups. No war-veterans grant is reported. Of the unresolved adults, 105 are married, mostly with a spouse outside the household, and 63 are recorded as living together."),
  caption("Table I. KwaZulu-Natal cohort"),
  table(
    ["Step", "People", "Households"],
    [
      ["KwaZulu-Natal respondents", "15,388", "3,686"],
      ["Aged 60 or older", "1,317", "1,068"],
      ["Failed a known rule", "117", "98"],
      ["Eligibility unresolved", "187", "168"],
      ["Passed, resolved answer", "1,013", "827"],
      ["Reported receipt", "946", "773"],
      ["Reported non-receipt", "67", "60"],
    ],
    [3040, 1000, 1000]
  ),
  note("Household counts are distinct households in the row. A household may appear more than once."),
  para("The unweighted non-receipt proportion is 6.6% (67/1,013). The person-weighted proportion is 7.5%. A sampling-unit approximation, using 345 derived primary sampling units and no strata, has a standard error of 1.3 percentage points and a normal 95% interval from 4.9% to 10.0%. No one who passed has an unresolved grant answer, and current receipt agrees with preceding-year OPG income for all 1,013 adults."),
  para("Composition differs, and the comparison is descriptive. Men are 34 of 67 non-recipients and 260 of 946 recipients. Grade 7 or above is recorded for 49 of 67 non-recipients and 290 of 946 recipients. Urban formal residence is recorded for 38 of 67 non-recipients and 284 of 946 recipients. A welfare office at least 5 km away, or unavailable, is recorded for 34 of 67 non-recipients and 717 of 946 recipients."),
  h2("B. Eligibility sensitivity"),
  para("Table II reports the alternatives that change the proportion. Moving the rand ceiling, the price basis, or the receipt period changes the primary figure by at most 0.2 percentage points. Treating adults who live together, or who are separated, as single adds up to 68 people, most of whom report receipt. Retaining own disability-grant recipients raises the weighted proportion from 7.5% to 9.1%."),
  caption("Table II. Non-receipt under alternative screens"),
  table(
    ["Screen", "N", "Events", "Unwtd.", "Wtd."],
    [
      ["Primary", "1,013", "67", "6.6%", "7.5%"],
      ["2015 ceiling for all interviews", "1,015", "69", "6.8%", "7.7%"],
      ["Living together and separated as single", "1,081", "69", "6.4%", "7.1%"],
      ["Disability-grant recipients retained", "1,032", "82", "7.9%", "9.1%"],
    ],
    [2140, 700, 700, 750, 750]
  ),
  note("Events are reported non-recipients. Unwtd. and Wtd. are the unweighted and person-weighted proportions."),
  h2("C. Held-out prediction"),
  para("Each adult received a probability from a model that did not train on that adult\u2019s household. The ROC area is 0.75, with a household-resample interval of 0.69 to 0.81. Average precision is 0.20, beside a prevalence of 0.066. The Brier score is 0.058, compared with 0.062 for the intercept-only reference. Calibration-in-the-large is 0.02, with a resample interval from \u22120.32 to 0.27. The calibration slope is 0.84, with an interval from 0.59 to 1.13. The intervals do not refit the model."),
  para("Fig. 1 plots five quantile bins. In the highest fifth the mean prediction is 0.19 and 35 of 203 adults report non-receipt. In the lowest fifth the mean prediction is 0.011 and 3 of 206 report non-receipt."),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 80, after: 40 },
    children: [new ImageRun({
      type: "png",
      data: img,
      transformation: { width: 230, height: 230 },
      altText: {
        name: "Calibration plot",
        description: "Observed non-receipt against mean predicted probability in five quantile bins, with a diagonal reference line.",
        title: "Out-of-fold calibration",
      },
    })],
  }),
  note("Fig. 1. Out-of-fold calibration. Each point is a quantile bin of predicted probability. The diagonal is exact calibration."),
  para("In a fit on the whole cohort, the odds ratio for women versus men is 0.39 (Wald interval 0.23 to 0.66). The odds ratio for schooling below Grade 7 versus Grade 7 or above is 0.24 (0.13 to 0.43). The intervals for age, settlement, and welfare-office distance include 1. These are full-sample associations, not cross-validated effects."),
  para("Refits leave the ROC area between 0.74 and 0.76. Retaining disability-grant recipients lowers it to 0.74 and raises the Brier score to 0.068, together with a higher event rate. Replacing welfare access with a married indicator leaves the Brier score at 0.058. A survey-weighted fit has a ROC area of 0.75 and a calibration slope of 0.72. Folds grouped by sampling unit have a ROC area of 0.76. Complete cases, 992 adults and 63 non-recipients, have a ROC area of 0.76."),

  h1("VI. Discussion"),
  para("Reported receipt is the usual situation under these observable rules. About seven in every hundred apparently eligible adults report non-receipt, and the weighted figure is close to the unweighted one. The statement depends on the denominator. The unresolved group, 187 adults, is larger than the non-recipient group. The rate describes people whose income, partnership, and grant answers can be resolved. It does not describe every older adult, and it does not describe everyone who might qualify under the full legal test [1]."),
  para("The rand ceiling is not the fragile part of the estimate. Changing it, or the price basis of income, moves the proportion by a fraction of a point. The disability-grant exclusion moves it further, which is expected if that rule is part of the legal boundary and also the rule that removes many non-recipients from the denominator [1]. Partnership rules change the headcount more than the rate, because the adults they add mostly report receipt. Studies of eligible households and of rural pensioners show that receipt has a demographic pattern [2], [6]. Studies of other grants show that application is costly [9], [12], [16], [17]. This survey does not record applications, documents, or waiting time, so a high receipt rate is not evidence that those costs are small."),
  para("The model ranks non-recipients better than chance and improves probability error only slightly. A ROC area of 0.75, read alone, overstates usefulness at a 6.6% prevalence [20]. A high score is still usually a recipient. Average calibration is acceptable, and the slope is too uncertain, with 67 events, for a strong claim about sharpness [19], [21]. The ranking is carried by sex and schooling. Women, and adults with less than Grade 7, are less likely to report non-receipt. Schooling was motivated as a possible information barrier [9], [15]. Inside this screened cohort the association runs the other way: less schooling goes with reported receipt. Settlement and welfare-office distance, motivated by the access literature [16], [17], are not precisely associated with non-receipt here. The model does not establish why non-receipt occurred, or whether the same ranking would hold in another province or year [22], [23]."),
  para("The command does the minimum job. It rebuilds the cohort and the predictions, a second run matches the first byte for byte, and 26 pre-stated decisions match the program, including the income boundary, a missing spouse, an incompatible grant, and a caregiver grant that must not set the label. A researcher can read one person\u2019s status, reasons, fold, and probability. That is inspectability of the research files. It is not a test of a review screen, which was not built."),

  h1("VII. Limitations and Ethics"),
  para("Legal eligibility is only partly observed. The asset test, deemed income from assets, and permitted deductions are not in the proxy. Income and reported receipt can be wrong. The non-recipient count is small. The design is cross-sectional, so the associations have no established time order. The 2014/2015 survey does not describe present-day access, and the household sample does not represent institutionalised older adults. Without strata, the variance figure is an approximation. Validation is internal."),
  para("The analysis uses the released survey files under their access conditions. Person identifiers and predictions remain in controlled storage. The cases used to test the rules are synthetic. The program records how this study screened survey respondents. It does not decide who should receive the grant."),

  h1("VIII. Conclusion"),
  para("In this KwaZulu-Natal screen, 6.6% of apparently eligible adults report OPG non-receipt, or 7.5% with person weights. The weighted figure stays between 7.1% and 9.1% when the eligibility rules change, and the disability-grant rule moves it more than the income ceiling. The unresolved group is larger than the non-recipient group, so the denominator is part of the answer."),
  para("Sex and schooling rank reported non-receipt moderately. The probabilities are only a little more accurate than a single risk, and settlement and welfare-office distance are not pinned down. The result limits what these survey items can predict. It does not explain non-receipt."),
  para("A single command reproduces the cohort, the description, and the held-out predictions, and the rule engine matches the decisions that were specified in advance. The analysis is inspectable as a research pipeline. It is not an eligibility service."),

  h1("References"),
  ...[
    "[1] Republic of South Africa, Social Assistance Act 13 of 2004, Government Gazette 26446, Jun. 10, 2004.",
    "[2] M. Ralston, E. Schatz, J. Menken, F. X. G\u00f3mez-Oliv\u00e9, and S. Tollman, \u201CWho benefits\u2014or does not\u2014from South Africa\u2019s old age pension?\u201D Int. J. Environ. Res. Public Health, vol. 13, no. 1, Art. 85, 2016.",
    "[3] Statistics South Africa, Living Conditions Survey 2014/2015: Metadata, Statistical Release P0310. Pretoria, South Africa, 2017.",
    "[4] Statistics South Africa, Living Conditions Survey: COICOP Codes. LCS 2014/2015 code list.",
    "[5] Statistics South Africa, Living Conditions Survey 2014/2015: Household Questionnaire.",
    "[6] E. B. Godfrey et al., \u201CWhich eligible households get grants? Demographic correlates of receipt in South Africa,\u201D Dev. South. Afr., vol. 33, no. 6, pp. 774\u2013789, 2016.",
    "[7] T. Raniga and B. Simpson, \u201CPoverty, HIV/AIDS and the old age pension in Bhambayi, KwaZulu-Natal,\u201D Dev. South. Afr., vol. 28, no. 1, pp. 75\u201385, 2011.",
    "[8] M. Alloush, J. R. Bloem, and J. G. Malacarne, \u201CSocial protection amid a crisis: New evidence from South Africa\u2019s Older Person\u2019s Grant,\u201D World Bank Econ. Rev., vol. 38, no. 2, pp. 371\u2013393, 2024.",
    "[9] A. Case, V. Hosegood, and F. Lund, \u201CThe reach and impact of Child Support Grants: Evidence from KwaZulu-Natal,\u201D Dev. South. Afr., vol. 22, no. 4, pp. 467\u2013482, 2005.",
    "[10] W. Zembe-Mkabile, T. Doherty, D. Sanders, and D. Jackson, \u201CChild Support Grant access and receipt among 12-week-old infants,\u201D Global Health Action, vol. 7, no. 1, Art. 25310, 2014.",
    "[11] J. Gazeaud, \u201CProxy means testing vulnerability to measurement errors?\u201D J. Dev. Stud., vol. 56, no. 11, pp. 2113\u20132133, 2020.",
    "[12] D. P. Moynihan, P. Herd, and H. Harvey, \u201CAdministrative burden: Learning, psychological, and compliance costs,\u201D J. Public Adm. Res. Theory, vol. 25, no. 1, pp. 43\u201369, 2015.",
    "[13] C. J. Heinrich and R. Brill, \u201CStopped in the name of the law: Administrative burden and cash transfer effectiveness,\u201D World Dev., vol. 72, pp. 277\u2013295, 2015.",
    "[14] A. Gibbs, L. Washington, N. Jama Shai, Y. Sikweyiya, and S. Willan, \u201CSystematically excluded: Young women\u2019s experiences of accessing child support grants,\u201D Global Public Health, vol. 13, no. 12, pp. 1820\u20131830, 2018.",
    "[15] T. N. Majola and P. Maharaj, \u201CChallenges associated with the Child Support Grant application process,\u201D J. Soc. Serv. Res., vol. 51, nos. 5\u20136, pp. 1140\u20131150, 2025.",
    "[16] S. Granlund, \u201CThey are not leaving without their money: Encounters with the state through cash transfers,\u201D South. Afr. J. Soc. Work Soc. Dev., vol. 34, no. 1, Art. 9052, 2022.",
    "[17] A. N. Vujovic, G. M. Jonathan, and S. Hacks, \u201CDigitalisation and its impact on social protection programmes effectiveness,\u201D Procedia Comput. Sci., vol. 237, pp. 882\u2013890, 2024.",
    "[18] M. T. Mabala, \u201CFactors associated with social grant uptake in South Africa,\u201D M.Res. report, Univ. Witwatersrand, Johannesburg, South Africa, 2023.",
    "[19] B. Van Calster et al., \u201CCalibration: The Achilles heel of predictive analytics,\u201D BMC Med., vol. 17, Art. 230, 2019.",
    "[20] T. Saito and M. Rehmsmeier, \u201CThe precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets,\u201D PLOS ONE, vol. 10, no. 3, Art. e0118432, 2015.",
    "[21] R. D. Riley et al., \u201CMinimum sample size for developing a multivariable prediction model: Part II,\u201D Stat. Med., vol. 38, no. 7, pp. 1276\u20131296, 2019.",
    "[22] D. R. Roberts et al., \u201CCross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure,\u201D Ecography, vol. 40, no. 8, pp. 913\u2013929, 2017.",
    "[23] G. S. Collins, J. B. Reitsma, D. G. Altman, and K. G. M. Moons, \u201CTransparent reporting of a multivariable prediction model (TRIPOD),\u201D Ann. Intern. Med., vol. 162, no. 1, pp. 55\u201363, 2015.",
    "[24] Dept. of Social Development, \u201CIncrease in respect of social grants,\u201D Government Notice 211, Government Gazette 37474, Mar. 28, 2014.",
    "[25] Dept. of Social Development, \u201CIncrease in respect of social grants,\u201D Government Notice 277, Government Gazette 38647, Mar. 30, 2015.",
  ].map((line) => new Paragraph({
    spacing: { before: 0, after: 40, line: 200 },
    indent: { left: 360, hanging: 360 },
    children: [r(line, { size: 16 })],
  })),
];

const doc = new Document({
  styles: {
    default: { document: { run: { font: FONT, size: 20 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 22, bold: true, color: NAVY },
        paragraph: { spacing: { before: 160, after: 80 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 20, bold: true, italics: true },
        paragraph: { spacing: { before: 120, after: 60 }, outlineLevel: 1 } },
    ],
  },
  sections: [
    {
      properties: { page: PAGE },
      headers: { default: new Header({ children: [new Paragraph({
        border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: NAVY, space: 1 } },
        spacing: { after: 60 },
        children: [r("Jawe \u2014 Reported OPG non-receipt, KwaZulu-Natal", { italics: true, size: 16, color: "595959" })],
      })] }) },
      footers: { default: new Footer({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [r("Page ", { size: 16 }), new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16 })],
      })] }) },
      children: title,
    },
    {
      properties: {
        type: SectionType.CONTINUOUS,
        column: { count: 2, space: 360, equalWidth: true },
        page: PAGE,
      },
      children: body,
    },
  ],
});

Packer.toBuffer(doc).then((buffer) => {
  const out = "C:/Users/oluhl/Desktop/research skills/paper/Jawe_OPG_nonreceipt_KZN.docx";
  fs.writeFileSync(out, buffer);
  console.log("wrote", out, buffer.length);
});
