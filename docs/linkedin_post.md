# LinkedIn Post — Labour Market Intelligence Dashboard (Real PLFS Data)

---

## Draft A — Data-focused (recommended for Data Analyst roles)

🔍 **I analysed 42,000 real government survey records to understand India's gender wage gap — and found something I didn't expect.**

Using Periodic Labour Force Survey (PLFS) 2022–23 microdata — India's official employment survey from MoSPI — I built an end-to-end wage analysis covering 41,913 employed wage workers across 36 states.

**The expected story:** women earn less because they have less education or experience than men.

**What the data actually shows:** male and female wage workers in this sample have almost identical average education (11.1 vs 10.7 years) and a similar urban share. A Blinder-Oaxaca decomposition — the standard labour-economics method for this question — finds that only **0.3% of the gender wage gap** is explained by these differences. **99.7% comes from women being paid less for the same measured qualifications.**

**Headline numbers:**
📊 Raw gender wage gap: 22.5% (₹21,136 vs ₹16,388/month)
📈 Return to schooling: 10.3% per additional year (Mincer regression)
⚖️ Regression-adjusted female wage penalty: 34.5%
📉 Gini coefficient: 0.427 — moderate-to-high wage inequality

**The important caveat I want to be upfront about:** female labour force participation in India is much lower than male participation. The women who do appear in this wage-employment dataset are a selected, relatively advantaged group. That's very likely *why* the "explained" share is so small — the most disadvantaged women may not be in wage work at all. A Heckman selection correction is the right next step, and I say so directly in the write-up rather than overselling the headline number.

**Tools:** Python (pandas, numpy, scipy) · weighted least squares regression built from scratch · Blinder-Oaxaca decomposition · Gini/Theil inequality measures · SQL · matplotlib/seaborn

Full code, data dictionary, and write-up: github.com/rupalrani/labour-market-intelligence

This is real MoSPI microdata, properly survey-weighted throughout — not a toy dataset.

---

#DataAnalytics #LabourEconomics #India #Python #PLFS #GenderPayGap #OpenData #WageInequality #DataScience #PortfolioProject

---

## Draft B — Story-led (recommended for broader audiences)

🌏 **42,000 workers. One government survey. A finding that surprised me.**

India's Periodic Labour Force Survey is the country's official employment census. I spent the last few weeks analysing the 2022–23 microdata to understand the gender wage gap properly — not just citing a headline number, but breaking down *why* it exists.

The standard explanation for gender wage gaps is that women have less education or work experience than men, on average. So I checked, using the Blinder-Oaxaca decomposition method that labour economists have used since the 1970s to answer exactly this question.

**In this data, that explanation barely holds.** Male and female wage workers have nearly the same average education. Almost the entire 22.5% wage gap — 99.7% of it — comes from women being paid less for the *same* measured qualifications, not from having fewer of them.

I don't want to overstate this. Female labour force participation in India is far lower than male participation, so the women captured in a wage-employment survey are a selected group — likely more educated and more urban than working-age women as a whole. That selection is probably part of why the gap looks like a "pay" story rather than a "qualifications" story in this particular sample. I say this clearly in my write-up rather than burying it.

What I can say with more confidence: returns to education are high (about 10% per extra year of schooling), the gender gap is widest for SC workers and narrows — but doesn't close — at higher education levels, and overall wage inequality (Gini = 0.43) is driven mostly by variation *within* each gender, not between them.

Full analysis, code, and an honest limitations section: github.com/rupalrani/labour-market-intelligence

---

#India #LabourMarket #DataScience #GenderPayGap #PLFS #Analytics #OpenSource #WageInequality

---

## Posting Tips

- Lead with Figure 9 (`09_oaxaca_components_PLFS.png`) or Figure 4 (`04_oaxaca_PLFS.png`) — the explained-vs-unexplained visual is the most attention-grabbing and most defensible image to post first.
- Post Tuesday–Thursday, 9–11 AM IST for best reach.
- In the first comment, share the GitHub link and say "Full methodology, data dictionary, and limitations in the repo."
- If anyone challenges the 99.7% figure (some will), the selection-bias caveat in the post is your answer — point to it directly rather than getting defensive. That caveat is what makes this credible to people who know the literature.
- Tag TISS Mumbai if appropriate for your institution's visibility norms.
