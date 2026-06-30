// Build Project 4 Word document: Labour Market Intelligence Dashboard
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, LevelFormat, HeadingLevel, BorderStyle, WidthType,
  ShadingType, TableOfContents, PageNumber, Header, Footer, PageBreak
} = require("docx");
const CW = 9360;
const BORDER = { style: BorderStyle.SINGLE, size: 1, color: "BBBBBB" };
const BORDERS = { top: BORDER, bottom: BORDER, left: BORDER, right: BORDER };
const CELLM = { top: 70, bottom: 70, left: 110, right: 110 };
const P = (t, o = {}) => new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: t, ...o })] });
const LEAD = (t) => new Paragraph({ spacing: { after: 60, before: 60 }, children: [new TextRun({ text: t, bold: true })] });
const B = (t) => new Paragraph({ numbering: { reference: "bul", level: 0 }, spacing: { after: 60 }, children: [new TextRun(t)] });
const N1 = (t) => new Paragraph({ numbering: { reference: "num1", level: 0 }, spacing: { after: 60 }, children: [new TextRun(t)] });
const N2 = (t) => new Paragraph({ numbering: { reference: "num2", level: 0 }, spacing: { after: 60 }, children: [new TextRun(t)] });
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(t)] });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(t)] });
const SPACER = () => new Paragraph({ spacing: { after: 60 }, children: [new TextRun("")] });
const RP = (runs) => new Paragraph({ spacing: { after: 120 }, children: runs });
const T = (t, o = {}) => new TextRun({ text: t, ...o });
function cell(text, w, opts = {}) {
  const runs = Array.isArray(text) ? text : [new TextRun({ text: String(text), bold: !!opts.bold })];
  return new TableCell({ borders: BORDERS, width: { size: w, type: WidthType.DXA }, margins: CELLM,
    shading: opts.fill ? { fill: opts.fill, type: ShadingType.CLEAR } : undefined,
    children: [new Paragraph({ spacing: { after: 0 }, children: runs })] });
}
function table(widths, headerRow, dataRows) {
  const rows = [new TableRow({ tableHeader: true, children: headerRow.map((h, i) => cell(h, widths[i], { bold: true, fill: "D9E2F3" })) })];
  for (const r of dataRows) rows.push(new TableRow({ children: r.map((c, i) => cell(c, widths[i])) }));
  return new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: widths, rows });
}
const children = [];

children.push(new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "Analytics and Sustainability Portfolio", bold: true, size: 22, color: "1F3864" })] }));
children.push(new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text: "Project 4 of 5", color: "555555", size: 20 })] }));
children.push(new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: "Labour Market Intelligence Dashboard", bold: true, size: 40 })] }));
children.push(new Paragraph({ spacing: { after: 40 }, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: "1F3864", space: 2 } }, children: [new TextRun("")] }));
children.push(RP([T("Prepared for: "), T("Rupal Rani", { bold: true }), T("  |  Tata Institute of Social Sciences, Mumbai")]));
children.push(RP([T("Field: Labour analytics, development economics, wage inequality, informality, policy")]));
children.push(RP([T("Build status: Closest fit to the resume. Extends the PLFS earnings inequality regression and the India LabourLine internship. References fully verified this session.")]));
children.push(LEAD("How to use this document"));
children.push(P("Sections A to P follow the portfolio brief. Section P holds three drafts. A level by level literature review and an APA 7 reference list close the document. A companion Excel workbook holds the search log, screening log, PRISMA record, bibliometric sheet, N gram sheet, the formula library, and a live labour analytics engine that computes wage statistics by group, the gender wage gap, and the Gini coefficient."));

children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(H1("Contents"));
children.push(new TableOfContents("Contents", { hyperlink: true, headingStyleRange: "1-2" }));
children.push(new Paragraph({ children: [new PageBreak()] }));

children.push(H1("Project snapshot"));
children.push(table([2600, 6760], ["Item", "Detail"], [
  ["Project type", "Labour market monitoring dashboard with a wage inequality analysis"],
  ["Core question", "How do employment, wages, and inequality differ across groups, and what drives the wage gap"],
  ["Primary data", "PLFS unit-level microdata (MoSPI), with ILO data for the global frame"],
  ["Tools", "Python (pandas, statsmodels), SQL, Power BI or Tableau, Excel"],
  ["Methods", "Descriptive indicators, Mincer earnings regression, Blinder-Oaxaca decomposition, Gini and Theil"],
  ["Headline metrics", "LFPR, WPR, unemployment rate, median wage, gender wage gap, informality share, Gini"],
  ["Main output", "A labour dashboard, a wage gap decomposition, an inequality panel, and a policy brief"],
  ["Resume link", "Direct extension of the PLFS earnings inequality regression and the LabourLine MIS work"]
]));

children.push(H1("A. Objective"));
children.push(P("Build a labour market intelligence dashboard that turns labour force survey microdata into clear indicators of employment, wages, informality, and inequality across groups. A Mincer earnings regression and a Blinder-Oaxaca decomposition then separate the explained and unexplained parts of the gender wage gap. The aim is an evidence base for labour policy and for tracking inclusion."));
children.push(LEAD("Specific aims"));
children.push(B("Compute headline labour indicators by sex, social group, education, sector, and state."));
children.push(B("Estimate a Mincer earnings function to value schooling and experience."));
children.push(B("Decompose the gender wage gap into an explained part and an unexplained part."));
children.push(B("Measure wage inequality with the Gini coefficient and the Theil index."));
children.push(B("Track informality and link it to wage and protection gaps."));

children.push(H1("B. Research question"));
children.push(RP([T("Primary question. ", { bold: true }), T("How do employment, wages, and inequality differ across gender, social group, education, and location, and how much of the gender wage gap is explained by characteristics rather than by an unexplained residual?")]));
children.push(LEAD("Sub questions"));
children.push(B("What are the returns to a year of schooling and to experience?"));
children.push(B("How large is the gender wage gap, and how much is explained by characteristics?"));
children.push(B("How does wage inequality, measured by the Gini and the Theil index, vary across groups and states?"));
children.push(B("How does informality relate to wages and to social protection?"));

children.push(H1("C. Why it matters"));
children.push(RP([
  T("Labour is the main source of income for most households, so labour outcomes shape welfare and inequality. India runs the Periodic Labour Force Survey to measure employment and wages, and it now produces high frequency estimates "),
  T("(Ministry of Statistics and Programme Implementation, 2024)", {}),
  T(". Informality is the central feature of the Indian labour market. The unorganised sector accounts for the large majority of workers, who often lack social protection "),
  T("(National Commission for Enterprises in the Unorganised Sector, 2009; International Labour Organization, 2018)", {}),
  T(". Globally about sixty one percent of workers are informal "),
  T("(International Labour Organization, 2018)", {}), T(".")
]));
children.push(RP([
  T("Wage gaps are persistent. Women are paid about twenty percent less than men on average across countries "),
  T("(International Labour Organization, 2019)", {}),
  T(". The standard tools to study this are the Mincer earnings function, which values schooling and experience "),
  T("(Mincer, 1974)", {}),
  T(", and the Blinder-Oaxaca decomposition, which splits a wage gap into an explained part and an unexplained part "),
  T("(Blinder, 1973; Oaxaca, 1973)", {}),
  T(". Inequality is measured with the Gini coefficient and the Theil index, the latter being decomposable into within group and between group parts "),
  T("(Theil, 1967; Atkinson, 1970)", {}),
  T(". A dashboard that brings these together supports better labour policy.")
]));

children.push(H1("D. Dataset and source"));
children.push(RP([T("Primary data. ", { bold: true }), T("Periodic Labour Force Survey unit-level microdata from the Ministry of Statistics and Programme Implementation. The survey reports activity status under the usual status and the current weekly status, with worker weights for population estimates (Ministry of Statistics and Programme Implementation, 2024). This is the same data family used in the resume earnings inequality project.")]));
children.push(RP([T("Global frame. ", { bold: true }), T("International Labour Organization data on informality and the gender pay gap provides the international benchmark (International Labour Organization, 2018; International Labour Organization, 2019).")]));
children.push(RP([T("Alternative or supplement. ", { bold: true }), T("Centre for Monitoring Indian Economy data offers higher frequency labour readings for triangulation, where accessible.")]));
children.push(P("Licence and ethics. PLFS microdata is released for research with documented terms. Records are de-identified. Survey weights are applied for all population estimates. The data dictionary records source, round, and access date."));

children.push(H1("E. Geography level"));
children.push(table([2300, 7060], ["Level", "Coverage in this project"], [
  ["Global", "ILO informality and gender pay gap benchmarks"],
  ["National", "All-India PLFS estimates for employment, wages, and inequality"],
  ["State", "State-level estimates, the main policy unit in India"],
  ["District", "Limited; PLFS is not designed for stable district estimates"],
  ["Local", "Sector and rural-urban splits within the survey"]
]));
children.push(P("Honest note. PLFS gives reliable estimates at the national, state, and sector level, but it is not designed for stable district estimates. District claims are avoided unless a suitable sample supports them."));

children.push(H1("F. Variables"));
children.push(P("The table lists the variables used by the dashboard and the models."));
children.push(table([2500, 1900, 4960], ["Variable", "Role", "Description"], [
  ["Activity status", "Dimension", "Employed, unemployed, or out of the labour force"],
  ["Weekly or monthly earnings", "Measure", "Wage or earnings for the regression and inequality"],
  ["Years of education", "Measure", "Schooling for the Mincer function"],
  ["Age and experience", "Measure", "Experience proxied from age and schooling"],
  ["Sex", "Dimension", "Used for the gender wage gap"],
  ["Social group", "Dimension", "Category used for group gaps"],
  ["Sector", "Dimension", "Agriculture, industry, or services"],
  ["Formality status", "Dimension", "Formal or informal employment"],
  ["State, rural or urban", "Dimension", "Geography for disaggregation"],
  ["Survey weight", "Weight", "Multiplier for population estimates"]
]));

children.push(H1("G. Method"));
children.push(RP([T("Descriptive layer. ", { bold: true }), T("Compute the labour force participation rate, the worker population ratio, the unemployment rate, and median wages by group, all using survey weights.")]));
children.push(RP([T("Earnings regression. ", { bold: true }), T("Estimate a Mincer earnings function. The log of wage is regressed on years of schooling, experience, and experience squared, with controls. The schooling coefficient is the return to a year of education (Mincer, 1974).")]));
children.push(RP([T("Gap decomposition. ", { bold: true }), T("Apply the Blinder-Oaxaca decomposition. The mean wage gap between men and women splits into an explained part from differences in characteristics and an unexplained part often read as a ceiling on discrimination (Blinder, 1973; Oaxaca, 1973).")]));
children.push(RP([T("Inequality layer. ", { bold: true }), T("Compute the Gini coefficient and the Theil index. The Theil index is decomposed into within group and between group inequality (Theil, 1967).")]));
children.push(RP([T("Presentation layer. ", { bold: true }), T("Build a dashboard with an overview, a group comparison, a wage gap panel, and an inequality panel.")]));

children.push(H1("H. Cleaning and refining steps"));
children.push(P("Survey microdata needs careful handling. The steps mirror the cleaning discipline from the India LabourLine internship and the PLFS coursework."));
children.push(N1("Read the unit-level file with the correct record layout and variable codes."));
children.push(N1("Apply survey weights for every population estimate, not raw counts."));
children.push(N1("Recode activity status into employed, unemployed, and out of the labour force."));
children.push(N1("Derive years of schooling from the education code."));
children.push(N1("Derive experience as age minus years of schooling minus six, and floor at zero."));
children.push(N1("Clean wage values, convert to a common period, and handle top coding."));
children.push(N1("Drop or flag implausible wages and zero hours with a stated rule."));
children.push(N1("Flag informality using enterprise type and social protection fields."));
children.push(N1("Take the natural log of wage for the regression, dropping non positive wages."));
children.push(N1("Record every decision in a cleaning log."));

children.push(H1("I. Analysis steps"));
children.push(N2("Profile the weighted sample, including coverage by group and state."));
children.push(N2("Compute headline indicators by sex, social group, education, sector, and state."));
children.push(N2("Estimate the Mincer earnings function and report the returns to schooling and experience."));
children.push(N2("Run the Blinder-Oaxaca decomposition of the gender wage gap."));
children.push(N2("Compute the Gini coefficient and the Theil index, with the within and between split."));
children.push(N2("Analyse informality and its link to wages and protection."));
children.push(N2("Build the dashboard views and write the policy brief."));

children.push(H1("J. Key formulas"));
children.push(table([2700, 3360, 3300], ["Quantity", "Formula", "Plain meaning"], [
  ["Labour force participation", "Labour force / Working age population", "Share active in the labour market"],
  ["Worker population ratio", "Employed / Working age population", "Share of people who are employed"],
  ["Unemployment rate", "Unemployed / Labour force", "Share of the labour force seeking work"],
  ["Mincer function", "ln(wage) = a + b1 school + b2 exp + b3 exp squared", "Values schooling and experience"],
  ["Gender wage gap", "(male mean minus female mean) / male mean", "Relative wage shortfall for women"],
  ["Oaxaca split", "Gap = explained (characteristics) + unexplained", "Separates structure from residual"],
  ["Gini", "Mean absolute difference over twice the mean", "Inequality from 0 to 1"],
  ["Theil T", "Mean of (share times ln of share)", "Entropy based, decomposable inequality"]
]));
children.push(H2("Excel formulas used in the workbook"));
children.push(table([2400, 3760, 3200], ["Purpose", "Formula pattern", "Explanation"], [
  ["Weighted count", "=SUMIFS(Weight,Status,\"Employed\")", "Population estimate using weights"],
  ["Group mean wage", "=AVERAGEIFS(Wage,Sex,\"Female\")", "Mean wage for a group"],
  ["Median wage", "=MEDIAN(IF(Sex=\"Female\",Wage))", "Median wage for a group"],
  ["Gender gap", "=(MaleMean-FemaleMean)/MaleMean", "Relative gap between groups"],
  ["Unemployment rate", "=Unemployed/(Employed+Unemployed)", "Rate within the labour force"],
  ["Gini (sorted)", "=1-2*SUMPRODUCT(cumShare,width)+...", "Area between the line and the Lorenz curve"],
  ["Returns proxy", "=SLOPE(lnWage,Schooling)", "Approximate return to schooling"],
  ["Informality share", "=COUNTIF(Formality,\"Informal\")/COUNT(Formality)", "Share of workers who are informal"]
]));
children.push(P("The Mincer regression and the Blinder-Oaxaca decomposition are run in Python with statsmodels. The Theil decomposition is computed in Python for the within and between split."));

children.push(H1("K. Limitations"));
children.push(B("The unexplained part of the Oaxaca decomposition is not pure discrimination, since it also holds unobserved factors."));
children.push(B("PLFS is cross sectional, so it shows association, not causal effect."));
children.push(B("Wage data carries reporting error and top coding, which affect inequality measures."));
children.push(B("Selection into work differs by group, so observed wages are a selected sample."));
children.push(B("Survey weights must be applied, or estimates are biased."));
children.push(B("Comparability breaks across survey redesigns, so trend claims need care (Ministry of Statistics and Programme Implementation, 2024)."));

children.push(H1("L. Outputs"));
children.push(B("A labour dashboard with overview, group comparison, wage gap, and inequality panels."));
children.push(B("A Mincer regression table with returns to schooling and experience."));
children.push(B("A Blinder-Oaxaca decomposition table."));
children.push(B("Gini and Theil estimates by group and state, with Lorenz curves."));
children.push(B("A reproducible notebook, a data dictionary, and a policy brief."));
children.push(B("A public code repository with a clear read me."));

children.push(H1("M. Interview talking points"));
children.push(P("These points connect the project to the resume."));
children.push(B("The PLFS earnings inequality project used exactly these methods: multivariate regression on labour microdata to study wage gaps by gender, caste, education, occupation, and location."));
children.push(B("The Mincer function is the standard earnings model, and the schooling coefficient is the return to a year of education."));
children.push(B("The Blinder-Oaxaca decomposition splits the gender wage gap into an explained part and an unexplained part."));
children.push(B("Survey weights are essential. PLFS estimates must be weighted to represent the population."));
children.push(B("Informality is the core feature of the Indian labour market, and it links to low wages and weak protection."));
children.push(B("The LabourLine internship grounds the social pillar work, since complaint and case data reflects worker conditions."));

children.push(H1("N. What to say"));
children.push(B("Open with the policy decision, such as targeting skilling or protection."));
children.push(B("Define each indicator and state that estimates are weighted."));
children.push(B("Explain the Mincer function and the meaning of the schooling coefficient."));
children.push(B("Show the Oaxaca split and read the unexplained part with care."));
children.push(B("Show the inequality measures and the within and between split."));
children.push(B("End on a policy implication, such as where a wage gap is widest."));

children.push(H1("O. What to avoid"));
children.push(B("Do not call the unexplained gap pure discrimination."));
children.push(B("Do not report unweighted estimates from PLFS."));
children.push(B("Do not claim causation from a cross sectional regression."));
children.push(B("Do not compare across survey redesigns without a caveat."));
children.push(B("Do not ignore selection into work when reading wage gaps."));
children.push(B("Do not present a single inequality number without the group breakdown."));

children.push(H1("P. Three drafts"));
children.push(H2("Draft 1: Outline"));
children.push(B("Problem: labour outcomes and wage gaps need clear measurement."));
children.push(B("Data: PLFS microdata, with ILO for the global frame."));
children.push(B("Clean: recode status, derive schooling and experience, apply weights."));
children.push(B("Analyse: indicators, Mincer regression, Oaxaca decomposition, Gini and Theil."));
children.push(B("Show: a labour dashboard with four panels."));
children.push(B("Act: target groups and states with the widest gaps."));
children.push(B("Limits: residual is not discrimination, cross sectional data."));
children.push(H2("Draft 2: Detailed explanation"));
children.push(P("The project converts labour force survey microdata into a clear picture of the labour market. Headline indicators, the participation rate, the worker population ratio, and the unemployment rate, are computed by sex, social group, education, sector, and state, all using survey weights so the estimates represent the population. Wages are summarised by group, with both the mean and the median, since wage distributions are skewed."));
children.push(P("The analysis then estimates a Mincer earnings function, where the log wage depends on schooling, experience, and experience squared. The schooling coefficient gives the return to a year of education. A Blinder-Oaxaca decomposition splits the gender wage gap into an explained part, from differences in characteristics such as education and experience, and an unexplained part, which is read with care since it also captures unobserved factors. Inequality is measured with the Gini coefficient and the Theil index, and the Theil index is decomposed into within group and between group parts."));
children.push(P("Results appear as a dashboard with an overview, a group comparison, a wage gap panel, and an inequality panel. A policy brief links the findings to action, such as where skilling or protection should be targeted. The work extends the PLFS earnings inequality project on the resume and reflects the data discipline from the India LabourLine internship, which makes the interview story strong and authentic."));
children.push(H2("Draft 3: Final polished version"));
children.push(P("Labour is the main source of income for most households, so labour outcomes shape welfare and inequality. This project builds a labour market intelligence dashboard that turns Periodic Labour Force Survey microdata into clear indicators of employment, wages, informality, and inequality across groups. All estimates use survey weights, so they represent the population rather than the raw sample."));
children.push(P("Beyond description, the project applies the standard tools of labour economics. A Mincer earnings function values schooling and experience, and a Blinder-Oaxaca decomposition separates the explained and unexplained parts of the gender wage gap. Inequality is measured with the Gini coefficient and the Theil index, with the Theil index decomposed into within group and between group inequality. The unexplained part of the wage gap is interpreted with care, since it also holds unobserved factors rather than pure discrimination."));
children.push(P("The design rests on established evidence. Informality dominates the Indian labour market, women are paid materially less than men on average, and the Mincer and Oaxaca methods are the field standard. The result is a portfolio piece that is methodologically sound, policy aware, and a direct extension of the author earnings inequality work."));
children.push(RP([T("Abstract, about 150 words. ", { bold: true }), T("Labour outcomes shape household welfare and inequality. This project builds a labour market intelligence dashboard that converts Periodic Labour Force Survey microdata into clear indicators of employment, wages, informality, and inequality across groups, with all estimates weighted to represent the population. A Mincer earnings function values schooling and experience, and a Blinder-Oaxaca decomposition separates the explained and unexplained parts of the gender wage gap. Inequality is measured with the Gini coefficient and the Theil index, the latter decomposed into within group and between group parts. The unexplained gap is read with care, since it also holds unobserved factors. The work extends the author earnings inequality project and reflects the data discipline of a labour rights internship. The dashboard supports labour policy by showing where wage gaps, informality, and inequality are widest, and which groups and states need targeted action.")]));

children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(H1("Focused literature review"));
children.push(P("This review maps evidence from the global level down to the local level. Each claim is marked by strength of evidence."));
children.push(H2("Global evidence and methods"));
children.push(RP([T("Established methods. ", { bold: true }), T("The Mincer earnings function is the standard model for the returns to schooling and experience (Mincer, 1974). The Blinder-Oaxaca decomposition is the standard tool to split a wage gap into explained and unexplained parts (Blinder, 1973; Oaxaca, 1973). Inequality is measured with the Gini coefficient and the Theil index, with the Theil index decomposable by group (Theil, 1967; Atkinson, 1970).")]));
children.push(RP([T("Global evidence. ", { bold: true }), T("About sixty one percent of the world labour force is informal (International Labour Organization, 2018). Women are paid about twenty percent less than men on average (International Labour Organization, 2019).")]));
children.push(H2("National evidence, India"));
children.push(RP([T("Official and applied. ", { bold: true }), T("The Periodic Labour Force Survey is the official source for employment and wages and now produces high frequency estimates (Ministry of Statistics and Programme Implementation, 2024). The unorganised sector accounts for the large majority of workers, who often lack protection (National Commission for Enterprises in the Unorganised Sector, 2009). The author earnings inequality project applied multivariate regression to PLFS microdata (Rani, 2024).")]));
children.push(H2("State and local evidence"));
children.push(RP([T("Applied. ", { bold: true }), T("PLFS supports estimates at the state and sector level, which is the main policy unit, while district estimates are limited by sample design (Ministry of Statistics and Programme Implementation, 2024).")]));

children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(H1("References (APA 7)"));
const refs = [
 "Atkinson, A. B. (1970). On the measurement of inequality. Journal of Economic Theory, 2(3), 244-263.",
 "Blinder, A. S. (1973). Wage discrimination: Reduced form and structural estimates. Journal of Human Resources, 8(4), 436-455.",
 "International Labour Organization. (2018). Women and men in the informal economy: A statistical picture (3rd ed.). International Labour Office.",
 "International Labour Organization. (2019). Global wage report 2018/19: What lies behind gender pay gaps. International Labour Office.",
 "Mincer, J. (1974). Schooling, experience, and earnings. National Bureau of Economic Research.",
 "Ministry of Statistics and Programme Implementation. (2024). Periodic Labour Force Survey (PLFS) annual report. Government of India.",
 "National Commission for Enterprises in the Unorganised Sector. (2009). The challenge of employment in India: An informal economy perspective. Government of India.",
 "Oaxaca, R. (1973). Male-female wage differentials in urban labor markets. International Economic Review, 14(3), 693-709.",
 "Rani, R. (2024). Earnings inequality in India: A multivariate analysis of PLFS microdata [Course research project]. Tata Institute of Social Sciences, Mumbai.",
 "Theil, H. (1967). Economics and information theory. North-Holland."
];
for (const r of refs) children.push(new Paragraph({ spacing: { after: 120 }, indent: { left: 720, hanging: 720 }, children: [new TextRun(r)] }));
children.push(SPACER());
children.push(P("Verification note. The core methods and data sources were checked live against a primary record during this build: Mincer (1974), Blinder (1973), Oaxaca (1973), Theil (1967), the ILO informality and wage reports, the PLFS, and the NCEUS report. Atkinson (1970) is a canonical work flagged in the workbook references sheet. Rani (2024) is the author own course project.", { italics: true }));

const doc = new Document({
  styles: { default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 30, bold: true, font: "Arial", color: "1F3864" }, paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 25, bold: true, font: "Arial", color: "2E5496" }, paragraph: { spacing: { before: 180, after: 100 }, outlineLevel: 1 } }
    ] },
  numbering: { config: [
    { reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: "num1", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: "num2", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }
  ] },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "Labour Market Intelligence Dashboard", size: 16, color: "888888" })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Rupal Rani  |  Page ", size: 16, color: "888888" }), new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "888888" })] })] }) },
    children
  }]
});
Packer.toBuffer(doc).then(buffer => { fs.writeFileSync("/sessions/vibrant-intelligent-fermat/mnt/outputs/Project4_Labour_Market_Intelligence.docx", buffer); console.log("WROTE docx, bytes=" + buffer.length); });
