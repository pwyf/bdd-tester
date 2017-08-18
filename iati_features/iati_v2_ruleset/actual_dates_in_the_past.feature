Feature: Actual dates should be in the past

  Scenario Outline: Actual start dates past (IATI 2.x)
    Given `activity-date[@type='2']/@iso-date` is a valid date
     then `activity-date[@type='2']/@iso-date` should be today, or in the past

  Scenario Outline: Actual end dates past (IATI 2.x)
    Given `activity-date[@type='4']/@iso-date` is a valid date
     then `activity-date[@type='4']/@iso-date` should be today, or in the past
