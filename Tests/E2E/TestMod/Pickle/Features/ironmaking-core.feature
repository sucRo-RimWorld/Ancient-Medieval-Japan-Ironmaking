Feature: Ironmaking in a real RimWorld 1.6 or 1.7 session

  Scenario: Exact Ironmaking development source and profile are loaded
    Then the exact Ironmaking source and expected profile are loaded

  Scenario: Processing Defs and Vanilla or MO result resolve
    Then the Ironmaking production Defs and final metal chain resolve

  @quickstart:IronmakingWorkMap @timeout:180
  Scenario: Native initial ironmaking research gate
    Then the initial ironmaking research gate operates in the loaded game

  Scenario: Loaded sand trade generators distinguish buying and selling
    Then the loaded bulk traders expose bounded sand buying and selling

  @quickstart:IronmakingLargeMap @timeout:180
  Scenario: Natural map creation produces finite iron sand
    Then the generated map has accessible natural iron-sand deposits

  @quickstart:IronmakingLargeMap @timeout:240
  Scenario: Natural iron-sand deposit is actually mineable and finite
    Then a mining colonist depletes naturally generated iron sand without respawn

  @quickstart:IronmakingWorkMap @timeout:240
  Scenario: Colonist mining job consumes finite deposit and yields sand
    Then a mining colonist depletes an iron-sand deposit and receives sand

  @quickstart:IronmakingLargeMap @timeout:180
  Scenario: Natural iron-sand locations survive save reload unchanged
    Given the generated natural iron-sand locations are recorded
    When I save and reload
    Then the generated natural iron-sand locations are unchanged after reload

  @quickstart:IronmakingWorkMap @timeout:180
  Scenario: Sand deposits survive real game save reload
    Given an iron-sand deposit is prepared for persistence
    When I save and reload
    Then the saved deposit still exists in the reloaded map
