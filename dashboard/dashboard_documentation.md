# Kinder Signs Tableau dashboard

## Purpose

The dashboard supports one decision: whether the available market, digital-readiness, and competitor evidence justifies a controlled Kinder Signs pilot in Spain, with Madrid as the proposed starting area.

It is a decision-support artifact. It does not report product usage, school demand, revenue, or pilot results.

## Intended audience

The primary readers are Cleo, the pseudonymised owner and economic-buyer persona for Little Steps Nursery, and reviewers assessing the KinderFlow capstone. The dashboard lets them compare institutional access, digital readiness, parent-age proxy indicators, and the proposed Kinder Signs position without treating those signals as commercial validation.

## Dashboard preview

![Tableau dashboard titled Kinder Signs Market Opportunity and Pilot Readiness. Four views show Spanish early-childhood enrolment indicators, Madrid and Spain digital-use percentages, generative-AI use for two adult age cohorts, and a competitor positioning map in which Kinder Signs is a proposed target rather than observed performance.](tableau/kinder_signs_market_opportunity.png)

## Tableau views

### Spain provides meaningful institutional access

This view places the pilot inside the first-cycle Early Childhood Education population. The packaged workbook displays:

- 491,811 enrolled children;
- a 50.2% official enrolment-rate indicator for ages 0 to 2;
- 76.4% enrolment at age 2;
- 12.2 average pupils per unit;
- a net increase of 140 centres from the prior year; and
- an embedded age-transition callout of 76.4% to 96.4%.

The 50.2% figure is not a penetration rate for the full age 0 to 3 KinderFlow audience. The administrative data is provisional for 2025 to 2026.

### Madrid is digitally ready for a low-friction pilot

This view compares broad population indicators:

- internet use: Madrid 98.0% and Spain 96.3%;
- online purchasing: Madrid 65.0% and Spain 59.6%; and
- embedded context: 1,169 Early Childhood Education centres in Madrid, with about 58% described as private or concerted.

These values support the choice of Madrid as a practical test location. They do not show KinderFlow adoption or willingness to pay.

### Parent-age proxies show strong GenAI familiarity

The view displays 2025 generative-AI use for two adult age cohorts:

- ages 25 to 34: 57.2%; and
- ages 35 to 44: 43.8%.

The INE Household ICT Survey is not a survey of parents. These cohorts are only proxies for adults who may include parents or caregivers. Subgroup sample sizes are not available in the cited press-release evidence.

### The gap is contextual school-home learning

The positioning map compares BabySignLanguage.com, Baby Sign Spain, HCLM, Baby Sign and Learn, and Kinder Signs across contextual learning and guided or interactive practice. Equal-size points prevent the chart from implying market share.

The competitor scores are a transparent consulting coding of reviewed public offers. Kinder Signs is a target-position hypothesis. Its score is not observed customer performance, validated differentiation, or a measured competitive advantage. The workbook preview labels the point as Kinder Signs; readers must use the dataset field position_type to see its hypothesis status.

## Data model

The packaged workbook contains one Tableau workbook, three embedded CSV files, and three Hyper extracts.

The source tables are:

- data/tableau_master.csv: 14 market, digital, and AI indicator records plus the header;
- data/competitive_positioning.csv: four observed competitor records and one Kinder Signs target-position hypothesis;
- data/source_register.csv: nine source and methodology records; and
- dashboard/data_dictionary.md: field definitions and interpretation rules.

The master indicator table includes category, metric, segment, geography, year, value, unit, source ID, confidence, limitation, and decision insight. The positioning table uses coded zero-to-five fields for contextual learning, guided practice, school-home integration, professional validation, and Spanish localisation. The source register records the population, method, sample size where available, source type, link, confidence, limitation, and intended Tableau use.

The frozen source register contains one outdated persona spelling in the limitation for source S03. Documentation uses Cleo. The dataset remains unchanged because this reconciliation is limited to Markdown.

## Filters and interaction

The workbook uses fixed worksheet filters to select the records required by each view. The saved dashboard does not expose visible user filter controls. Do not describe it as a filterable application or live reporting service.

Tableau tooltips can expose source IDs, confidence, limitations, methodology, and competitor evidence. The current PNG is a static preview and has no interactive tooltips.

## Why Tableau

Tableau packages the decision views with embedded data and keeps the source structure inspectable. It is suitable here because the question requires several small comparisons, direct labels, and source-aware tooltips. It is not part of the KinderFlow product runtime.

## Open the artifacts

Open dashboard/tableau/Kinder Signs - Market Opportunity.twbx in Tableau Desktop or a compatible Tableau client. The package includes its data extracts. If Tableau is unavailable, inspect dashboard/tableau/kinder_signs_market_opportunity.png and the three CSV sources listed above.

Artifact paths:

- dashboard/tableau/Kinder Signs - Market Opportunity.twbx
- dashboard/tableau/kinder_signs_market_opportunity.png
- dashboard/tableau_build_brief.md
- dashboard/data_dictionary.md
- data/tableau_master.csv
- data/competitive_positioning.csv
- data/source_register.csv

## Evidence limits

The dashboard supports a pilot decision, not a launch decision. It does not prove:

- product-market fit;
- demand or willingness to pay;
- market size for KinderFlow;
- conversion, retention, customer acquisition cost, or revenue;
- market share;
- causal developmental benefits from Baby Sign;
- educator adoption or family engagement;
- current Kinder Signs professional validation; or
- a production Tableau deployment.

Primary interviews and a controlled service test are still required. The dashboard should be read with the source limitations, not as a substitute for pilot evidence.
