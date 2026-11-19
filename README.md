## Section 2 - AI Patents by Country

### Research Question
Which countries lead AI patenting, and how has their share of world AI patents changed from 2010 to 2024?

### Overview
This section shows AI-related patent counts for the five countries with the most AI patents in 2024 (United States, China, Japan, Korea, and Germany). All other countries and territories are grouped as "Others". The source file covers 1995–2024, and the page displays 2010–2024.

Audience: policy analysts comparing national innovation in AI.

Concentration indices (HHI and Top-3 share) for patents are in Section 4, which covers 2016–2024.

### Data
- **Source file:** `Evolution_of_AI-related_patents_by_country.csv`, from OECD AI patent indicators, based on Patent Cooperation Treaty (PCT) applications
- **Columns:** `AI_counts`, `Country/territory`, `Country/territory_label`, `sector`, `year`
- **Unit:** patents, counted by priority year
- **Coverage:** 1995–2024 in the source file; 2010–2024 on the page
- **Latest observation:** 2024. Recent years may be estimates.
- **Aggregate rows** (`ALL`, `OECD`, `EU27`) are excluded from rankings and country shares. `ALL` is used only as the world total.
- **Territories:** the source includes territories such as Hong Kong, Puerto Rico, and the Cayman Islands. The page refers to them as "countries", so the README uses "countries and territories".
- **Processed file used by the page:** `data/processed/<file-name>.csv`. TODO: confirm this file and how it was derived from the source file.

### Methodology
- **Country selection:** the five countries with the highest 2024 patent count, excluding aggregate rows. Germany (628) ranks fifth. The United Kingdom (406) ranks sixth.
- **Country share:** country count divided by the world total (`ALL`) for the same year.
- **Others:** world total minus the five countries shown. `EU27` is an aggregate of member countries, so it is not used. Each member country is counted once in Others.
- **Rank:** position among the five countries shown for the selected year. This is not a world ranking.
- Each year's shares sum to approximately 100%, allowing for rounding.

### Key Results (2010 to 2024)
- **United States:** 5,192 patents in 2024 (+4,839 since 2010). Share fell from 30.9% to 28.9%.
- **China:** 4,913 patents in 2024 (+4,857 since 2010). Share rose from 4.9% to 27.3%. China ranked first in 2020 and 2021.
- **Japan:** 1,930 patents in 2024 (+1,571 since 2010). Share fell from 31.4% to 10.7%. Japan ranked first in 2010 and 2012.
- **Korea:** 1,920 patents in 2024 (+1,873 since 2010). Share rose from 4.1% to 10.7%. Korea ranked third in 2022 and 2023.
- **Germany:** 628 patents in 2024 (+580 since 2010). Share fell from 4.2% to 3.5%.
- **Others:** share fell from 24.6% to 18.9%.

### Verification
- Shares for 2010 and 2024 were recalculated from the source file. They match the page for all five countries.
- Ranks were checked against the source for 2010, 2014, 2020, 2021, and 2022.
- The 2024 selection was checked against every other country and territory in the source.
- Not yet verified: that `ALL` equals the sum of all country rows.
- TODO: describe how the processed file was produced from the source file.

### Implementation
- `pages/2_Patents.py`: Streamlit page with country filters, charts, a rank slider, and data tables.
- `src/patents.py`: `render_patent_view` function that builds the page.
- Data: see the Data section above.

### How to Run
pip install -r requirements.txt
streamlit run app.py

### Limitations
- Patent counts measure inventions that were patented, not research quality or commercial success.
- Patent rules and examination practices differ between offices, so counts may not be directly comparable across countries.
- Recent years may be estimates, so 2023–2024 values should be interpreted with caution.
- Rankings compare only the five countries shown and are not a world ranking.
- The source includes territories alongside countries.
- "Korea" refers to the Republic of Korea.
- Patent counts are not a comprehensive measure of AI capability.
