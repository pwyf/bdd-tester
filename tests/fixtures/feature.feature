@feature-tag
Feature: Shopping list tests

  @test-tag
  Scenario: Eggs should be on the list
    Given text is a shopping list
     Then "Eggs" should be present
