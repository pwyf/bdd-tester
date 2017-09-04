Feature: Actual dates should be in the past

  Scenario Outline: Transaction dates past
    Given `transaction/transaction-date/@iso-date` is a valid date
     then `transaction/transaction-date/@iso-date` should be today, or in the past

  Scenario Outline: Value dates past
    Given `transaction/value-date/@iso-date` is a valid date
     then `transaction/value-date/@iso-date` should be today, or in the past
