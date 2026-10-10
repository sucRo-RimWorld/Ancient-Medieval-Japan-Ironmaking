Feature: Ironmaking actual production bills

  Scenario: Exact Ironmaking development source and profile are loaded
    Then the exact Ironmaking source and expected profile are loaded

  @quickstart:IronmakingWorkMap @timeout:240
  Scenario: Charcoal bill consumes wood and produces charcoal
    Then a colonist completes the charcoal bill and consumes its wood

  @quickstart:IronmakingWorkMap @timeout:240
  Scenario: Smelting bill consumes sand and charcoal and produces bloom
    Then a colonist completes the sand-smelting bill and consumes sand and charcoal

  @quickstart:IronmakingWorkMap @timeout:240
  Scenario: Forging bill consumes bloom and produces the profile metal
    Then a colonist completes the bloom-forging bill with the profile metal output
