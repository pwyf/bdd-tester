Feature: Shopping list tests

  Scenario: Eggs should be on the list
    Given text is a shopping list
     Then "Eggs" should be present
