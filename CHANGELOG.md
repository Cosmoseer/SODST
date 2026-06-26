# Changelog

All notable changes to this project will be documented here.

# Unreleased
- Certain orbital parameters can now be displayed in the plot

# 0.6.0 - 15/06/2026
- Orbit determination panel added
- Can use the Gibbs preliminary determination algorithm
- Variables panel renamed to "Elements"

# 0.5.0 - 06/05/2026
- 3D orbits now implemented
- UI overhauled to variables | plot | properties
- UI now built based on OS being used
- Fixed figure home button bug where it sometimes didn't return plot to original view
- Fixed issue where certain UI elements in Linux overlapped
- Caching introduced to some astrodynamics calculations

# 0.4.5 - 17/02/2026
- Refactored the design architecture of the core objects
- Created file containing orbital and kinematic helper functions
- Wrote unit tests for helper functions
- Refactored orbit propagation script and tests to align with new core design
- Refactored invariant tests to align with new core design
- Refactored GUI properties display panel to show current state and orbital elements
- Improved docstrings

# 0.4.4 - 12/02/2026
- Implemented basic orbit propagation
- Wrote orbit propagation tests

# 0.4.3 - 09/02/2026
- Implemented automatic testing
- Tests architecture rewritten
- Wrote invariants unit tests
- PerifocalOrbitEq refactored to live in the Satellite class

# 0.4.2 - 08/02/2026
- Refactored config builder and controller into variable, property and display builders/controllers
- Created new folder for common ui types
- Made ui imports safer

# 0.4.1 - 08/02/2026
- VariableSpec dataclass refactored as a subclass of PropertySpec

# 0.4.0 - 08/02/2026
- Interactive satellite orbit plotted
- Orbital variables have adjustable sliders and inputs
- Orbital and satellite parameters calculated and displayed