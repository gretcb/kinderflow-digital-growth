# Data dictionary

## tableau_master.csv
- `category`: analytical section
- `metric`: display metric
- `segment`: population/subgroup
- `geography`: geography
- `year`: reference year
- `value`: numeric value
- `unit`: unit for formatting
- `source_id`: joins to source_register.csv
- `confidence`: evidence confidence
- `limitation`: caveat to surface in tooltip/source note
- `insight`: decision interpretation

## competitive_positioning.csv
Scoring is a transparent consulting coding, not a market-performance dataset.

- `x_contextual_learning_0_5`
  - 0 = primarily static/dictionary content
  - 5 = contextual programme connected to real usage
- `y_guided_interactive_0_5`
  - 0 = passive viewing/reference
  - 5 = strongly guided/interactive learning
- `school_home_integration_0_5`
  - 0 = no observed school-home integration
  - 5 = school-home continuity is central
- `professional_validation_0_5`
  - 0 = unclear/no visible validation
  - 5 = professional validation central to proposition
- `spanish_localisation_0_5`
  - 0 = no meaningful Spanish localisation
  - 5 = Spanish-first/local specialist offer

Kinder Signs is a **target-position hypothesis**, not an observed competitor score.
