Feature: Ironmaking actual production bills

  Scenario: Exact Ironmaking development source and profile are loaded
    Then the exact Ironmaking source and expected profile are loaded

  @quickstart:IronmakingWorkMap @timeout:180
  Scenario: Loaded fuel component exclusivity
    Then AMJ Bill-fueled worktables have no loaded refuelable component

  @quickstart:IronmakingWorkMap @timeout:240
  Scenario: Charcoal bill consumes wood and produces charcoal
    Then a colonist completes the charcoal bill and consumes its wood

  @quickstart:IronmakingWorkMap @timeout:240
  Scenario: Smelting bill consumes sand and charcoal and produces bloom
    Then a colonist completes the sand-smelting bill and consumes sand and charcoal

  @quickstart:IronmakingWorkMap @timeout:240
  Scenario: Optional MO coal fuel and Vanilla isolation
    Then MO coal fuels a real smelting bill or Vanilla keeps MO resources absent

  @quickstart:IronmakingWorkMap @timeout:240
  Scenario: Interrupted smelting conserves resources
    Then an interrupted smelting bill resumes without losing or multiplying resources

  @quickstart:IronmakingWorkMap @timeout:240
  Scenario: Forging bill consumes bloom and produces the profile metal
    Then a colonist completes the bloom-forging bill with the profile metal output
