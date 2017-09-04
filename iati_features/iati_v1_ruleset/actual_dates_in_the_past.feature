Feature: Actual dates should be in the past

  Scenario Outline: Actual start dates past (IATI 1.x)
    Given `activity-date[@type='start-actual']/@iso-date` is a valid date
     then `activity-date[@type='start-actual']/@iso-date` should be today, or in the past

  Scenario Outline: Actual end dates past (IATI 1.x)
    Given `activity-date[@type='end-actual']/@iso-date` is a valid date
     then `activity-date[@type='end-actual']/@iso-date` should be today, or in the past
