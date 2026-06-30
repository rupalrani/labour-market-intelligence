# Interview Guide — Labour Market Intelligence Dashboard (Real PLFS Data)

**For:** Data Analyst and Research Analyst roles  
**Project:** Wage Gaps and Earnings Inequality in India — PLFS 2022–23 microdata  
**Author:** Rupal Rani | TISS Mumbai

---

## Core Narrative (30-Second Version)

> "I analysed real PLFS 2022–23 microdata — 42,000 records from India's official employment survey — to study the gender wage gap. I built a Mincer earnings regression, a Blinder-Oaxaca decomposition, and Gini/Theil inequality measures from scratch in Python, all survey-weighted. The finding that stood out: almost none of the gender wage gap is explained by differences in education or experience between men and women in this sample — it's almost entirely a story of different pay for similar workers. But I'm careful about that claim, because it's very likely shaped by who selects into wage employment in the first place."

---

## Headline Numbers to Have Ready

| Metric | Value |
|--------|-------|
| Sample size | 41,913 wage workers |
| Data period | PLFS 2022–23 (July 2022 – June 2023) |
| Raw gender wage gap | 22.5% |
| Return to schooling | 10.3% per year |
| Regression-adjusted female penalty | 34.5% |
| Oaxaca — explained by endowments | 0.3% |
| Oaxaca — unexplained (returns) | 99.7% |
| Gini coefficient | 0.427 |
| Theil — within-sex share | 98.3% |

---

## Anticipated Questions and Strong Answers

### Q1: "Walk me through this project."

1. **Data:** "PLFS 2022–23 unit-level microdata from MoSPI — India's official labour force survey. I worked with a 42,803-record extract, restricted to employed wage workers with positive earnings, giving 41,913 usable records."
2. **Methods:** "Survey-weighted descriptive statistics, a Mincer earnings regression by weighted least squares with robust standard errors, a Blinder-Oaxaca decomposition of the gender wage gap, and Gini/Theil inequality measures — all coded from first principles in Python, not a black-box library."
3. **Headline finding:** "The gender wage gap is large, but almost none of it is explained by education or experience differences between men and women in the sample. Nearly the whole gap is a 'different pay for similar workers' story."
4. **The caveat I lead with, not hide:** "That finding is shaped by who's in the sample — only women in wage employment are observed, and female labour force participation is much lower than male. So this describes the gap among wage-employed women, not all women."

---

### Q2: "Your Oaxaca decomposition shows 99.7% unexplained — isn't that a sign something is wrong with your model?"

**This is the most important question you will be asked. Answer it directly and confidently — it is not a flaw, it's a finding, and you understood it.**

> "I checked this carefully before reporting it. It's not a coding error — I verified the underlying means directly: male and female wage workers in this sample have nearly identical average education, 11.1 versus 10.7 years, and women actually have a slightly higher urban share than men. Because the two groups look similar on the variables in my model, the decomposition correctly attributes almost none of the gap to those variables. The real story is that I'm only observing women who are already in wage employment, and given how much lower female labour force participation is in India, that's a selected group — probably more educated and more urban than working-age women generally. So the 99.7% figure is accurate for the sample, but I'm explicit in my write-up that it shouldn't be read as 'there's no education gap behind the gender wage gap in India' — it's 'there's not much of one among women who are already wage-employed.' The standard next step is a Heckman selection correction with a labour-force-participation equation, and I name that directly as the priority extension in my limitations section."

---

### Q3: "What is the Mincer earnings regression, and what did you find?"

> "It's the standard model in labour economics for valuing education, from Jacob Mincer's 1974 work. I regressed log monthly wages on years of schooling, experience, experience squared, and controls for sex, social group, and urban location, using weighted least squares with the PLFS survey weights. I found a return to schooling of about 10.3% per year — meaning each additional year of education is associated with roughly a 10% wage increase, holding other factors constant. That's on the higher end of what's typically reported for India, but it's consistent with the very steep wage-education gradient I saw in the raw data — workers with postgraduate education earn almost four times what workers with primary education earn."

---

### Q4: "Why did you use survey weights, and how did you implement them without statsmodels?"

> "PLFS uses a stratified, multistage sampling design, so different households are sampled at different rates. Without weights, my estimates would just describe my sample, not the population. I implemented weighted least squares manually — scaling the design matrix by normalized weights before computing (X'WX)⁻¹X'Wy — because statsmodels wasn't available in my environment. I also derived heteroskedasticity-robust standard errors using the sandwich estimator, weighted the same way. Building it from scratch rather than calling a library function meant I had to actually understand the mechanics, which I think is a stronger signal of competence than importing a package."

---

### Q5: "What's the Gini coefficient, and what does 0.427 mean here?"

> "It measures inequality on a 0 to 1 scale based on the Lorenz curve — the gap between the actual cumulative distribution of wages and a hypothetical equal distribution. I computed it directly from the weighted, sorted wage data using the trapezoidal-area method. A value of 0.427 indicates moderate-to-high wage inequality among employed workers — there's a meaningful concentration of earnings at the top of the distribution, consistent with the nearly four-fold gap I found between the lowest and highest education bands."

---

### Q6: "What is the Theil index telling you that the Gini doesn't?"

> "The Theil T index is decomposable — total inequality splits exactly into a between-group component and a within-group component. I decomposed it by sex and found that 98.3% of total wage inequality is *within* each gender group, and only 1.7% is *between* men and women. That's an important complement to the gender-gap finding: even though the gender pay gap itself is large in percentage terms, gender differences account for a small share of overall wage dispersion. Most of the inequality in this labour market comes from variation within the male workforce and within the female workforce — likely driven by education, location, and occupation differences I haven't fully modelled yet."

---

### Q7: "What are the limitations of this analysis?"

Lead with the selection issue — it's the most important one and shows analytical maturity:

1. **Selection into wage employment (the big one):** "Female labour force participation is much lower than male in India. The women in my wage-employed sample are not representative of all working-age women. This is very likely why the explained share of the Oaxaca decomposition is so small. A Heckman two-step correction is the right next step."
2. **Limited controls:** "I don't have occupation, industry detail, firm size, or hours worked. Richer controls would likely raise the explained share of the gap — so my 99.7% unexplained figure is a ceiling, not a final answer."
3. **Cross-sectional design:** "PLFS is a repeated cross-section. My regression coefficients are associations, not causal effects — particularly the schooling coefficient, which could partly reflect unobserved ability."
4. **Working extract, not the full national file:** "My data is a 42,803-record extract. For any claim about official national PLFS indicators, I'd point to MoSPI's published annual report rather than my own numbers."
5. **No wage top-coding:** "I didn't winsorize extreme wage values. A robustness check capping wages at the 99th percentile would be a sensible next step to confirm the Mincer and Oaxaca results aren't driven by a small number of very high earners."
6. **Unexplained ≠ discrimination:** "The Oaxaca unexplained component captures differential returns to measured characteristics, but it also absorbs unobserved skill and any model mis-specification. It's an upper bound on discrimination, not a clean estimate of it."

---

### Q8: "Why does the regression-adjusted gender penalty (34.5%) differ from the raw gap (22.5%)?"

> "Good catch — this is a real and explainable pattern, not an inconsistency. The raw 22.5% gap is a simple arithmetic comparison of mean wages. The 34.5% comes from the regression coefficient on the female indicator, holding education, experience, social group, and location constant. Because women in my sample are not actually disadvantaged on those observable characteristics — their average education is close to men's, and their urban share is even slightly higher — controlling for those variables doesn't shrink the gap, it reveals a *larger* one. In other words, the raw gap actually understates how much less women are paid for the same measured qualifications."

---

## Concepts to Be Fluent In

| Concept | One-sentence definition |
|---------|------------------------|
| Survey weight | Multiplier representing how many population units one sample record stands for |
| Mincer earnings function | Log-wage regression on schooling and experience, valuing returns to human capital |
| Blinder-Oaxaca decomposition | Splits a wage gap into explained (endowments) and unexplained (differential returns) |
| Explained component | Share of the gap due to differing average characteristics, valued at one group's returns |
| Unexplained component | Share of the gap due to differing returns to the same characteristics |
| Selection bias | Bias from observing a non-random subset (e.g., only wage-employed women) |
| Heckman correction | Two-step method correcting wage equations for non-random selection into employment |
| Gini coefficient | 0–1 inequality measure from the Lorenz curve |
| Theil T index | Entropy-based inequality measure, decomposable into within/between components |
| Weighted least squares | Regression where each observation is weighted, here by the survey multiplier |
| Robust standard errors | Standard errors that don't assume constant error variance across observations |

---

## What NOT to Say

| Avoid | Say instead |
|-------|-------------|
| "99.7% of the gender gap is discrimination" | "99.7% is unexplained by my observed variables — that's a ceiling on what discrimination could explain, not a direct measurement, and selection into the sample matters here too" |
| "Women in India have no education disadvantage" | "Among women who are wage-employed, the education gap with men is small — that's different from working-age women overall" |
| "My data shows India's official gender wage gap is 22.5%" | "My analysis of this PLFS extract finds a 22.5% raw gap; official MoSPI figures should be the reference for national statistics" |
| "Correlation means causation" | "The regression shows an association; the schooling coefficient in particular may partly reflect unobserved ability rather than a pure causal effect" |
| Getting defensive about the 99.7% number | Treating it as the most interesting finding in the project and walking through exactly why it appears and what it does and doesn't mean |

---

## Closing Statement for Interviews

> "What I'm proudest of in this project isn't that I ran the right statistical methods — it's that when I got a surprising result, a 99.7% unexplained wage gap, I didn't either hide it or oversell it. I checked the underlying data to understand why it appeared, found the likely explanation in selection into wage employment, and reported both the finding and its limitation honestly. That's the difference between running an analysis and actually understanding one — and it's the standard I want to bring to a data analyst role."
