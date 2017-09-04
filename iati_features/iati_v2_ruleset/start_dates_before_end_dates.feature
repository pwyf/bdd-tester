Feature: Start dates chronologically before end dates

  Scenario Outline: Planned activity dates (IATI 2.x)
    Given `activity-date[@type='1']/@iso-date` is a valid date
     and `activity-date[@type='3']/@iso-date` is a valid date
     then `activity-date[@type='1']/@iso-date` should be chronologically before `activity-date[@type='3']/@iso-date`

  Scenario Outline: Actual activity dates (IATI 2.x)
    Given `activity-date[@type='2']/@iso-date` is a valid date
     and `activity-date[@type='4']/@iso-date` is a valid date
     then `activity-date[@type='2']/@iso-date` should be chronologically before `activity-date[@type='4']/@iso-date`
