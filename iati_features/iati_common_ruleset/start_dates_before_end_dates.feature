Feature: Start dates chronologically before end dates

  Scenario Outline: Result indicator period
    Given `result/indicator/period/period-start/@iso-date` is a valid date
     and `result/indicator/period/period-end/@iso-date` is a valid date
     then `result/indicator/period/period-start/@iso-date` should be chronologically before `result/indicator/period/period-end/@iso-date`

  Scenario Outline: Recipient organisation budget period
    Given `recipient-org-budget/period-start/@iso-date` is a valid date
     and `recipient-org-budget/period-end/@iso-date` is a valid date
     then `recipient-org-budget/period-start/@iso-date` should be chronologically before `recipient-org-budget/period-end/@iso-date`

  Scenario Outline: Recipient region budget period
    Given `recipient-region-budget/period-start/@iso-date` is a valid date
     and `recipient-region-budget/period-end/@iso-date` is a valid date
     then `recipient-region-budget/period-start/@iso-date` should be chronologically before `recipient-region-budget/period-end/@iso-date`

  Scenario Outline: Planned disbursement period
    Given `planned-disbursement/period-start/@iso-date` is a valid date
     and `planned-disbursement/period-end/@iso-date` is a valid date
     then `planned-disbursement/period-start/@iso-date` should be chronologically before `planned-disbursement/period-end/@iso-date`

  Scenario Outline: Recipient country budget period
    Given `recipient-country-budget/period-start/@iso-date` is a valid date
     and `recipient-country-budget/period-end/@iso-date` is a valid date
     then `recipient-country-budget/period-start/@iso-date` should be chronologically before `recipient-country-budget/period-end/@iso-date`

  Scenario Outline: Total expenditure period
    Given `total-expenditure/period-start/@iso-date` is a valid date
     and `total-expenditure/period-end/@iso-date` is a valid date
     then `total-expenditure/period-start/@iso-date` should be chronologically before `total-expenditure/period-end/@iso-date`

  Scenario Outline: Budget period
    Given `budget/period-start/@iso-date` is a valid date
     and `budget/period-end/@iso-date` is a valid date
     then `budget/period-start/@iso-date` should be chronologically before `budget/period-end/@iso-date`
