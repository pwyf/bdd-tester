Feature: Procurement policy

  Scenario: Procurement policy is present
    Given an organisation file
     then `document-link/category[@code="B05"]` should be present
