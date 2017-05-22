Feature: Allocation policy

  Scenario: Allocation policy is present
    Given an organisation file
     then `document-link/category[@code="B04"]` should be present
