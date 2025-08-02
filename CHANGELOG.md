# Changelog - FoundationDesign-ACI318

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-08-02

### Added - Major Migration to ACI 318M-25

#### New Design Standard Implementation
- **Complete migration from Eurocode 2 to ACI 318M-25** Building Code Requirements for Structural Concrete (Metric)
- Implementation of **ACI 318M-25 Chapter 13.1 Foundations**
- New `PadFoundationACI318` class replacing Eurocode-based design
- New `padFoundationDesignACI318` function for complete foundation design

#### ACI 318M-25 Load Combinations (Section 5.3.1)
- Dead load factor: 1.2 (was 1.35 in Eurocode)
- Live load factor: 1.6 (was 1.5 in Eurocode)  
- Wind load factor: 1.0 (new implementation)
- Minimum dead load factor: 0.9 for counteracting cases

#### ACI 318M-25 Strength Reduction Factors (Section 5.4.2)
- Flexure: φ = 0.90
- Shear: φ = 0.75
- Compression (tied): φ = 0.65
- Compression (spiral): φ = 0.75
- Bearing: φ = 0.65

#### Flexural Design (Section 7)
- **Whitney stress block method** replacing Eurocode rectangular stress block
- β₁ factor calculation based on concrete strength
- Tension-controlled section limits
- New minimum reinforcement requirements per Section 7.6:
  - As,min = max(1.4bwd/fy, √f'c bwd/(4fy))

#### Shear Design (Section 22)
- **One-way shear** per Section 22.5: Vc = 0.17λ√f'c bwd
- **Two-way shear (punching)** per Section 22.6:
  - Critical section at d/2 from column face
  - Three governing equations for different failure modes
  - Column aspect ratio effects
  - Location factors for interior/edge/corner columns

#### Material Properties
- Concrete strength: f'c (specified compressive strength) instead of fck
- Steel strength: fy (specified yield strength) instead of fyk
- Material property validation against ACI limits

#### Concrete Cover Requirements (Section 20.5)
- Foundations cast against earth: 75mm minimum
- Foundations formed against earth: 50mm minimum
- Updated cover requirements for different exposure conditions

### New Modules and Functions

#### `concretedesignfunc_aci318.py`
- `flexural_design_aci318()` - Whitney stress block flexural design
- `minimum_flexural_reinforcement_aci318()` - ACI minimum steel requirements
- `maximum_flexural_reinforcement_aci318()` - ACI maximum steel limits
- `one_way_shear_strength_aci318()` - One-way shear capacity
- `punching_shear_strength_aci318()` - Punching shear capacity
- `critical_section_punching_aci318()` - Critical section geometry
- `whitney_stress_block_factor()` - β₁ calculation
- `aci_load_factors()` - Load factor definitions
- `aci_strength_reduction_factors()` - φ factor definitions
- `concrete_cover_aci318()` - Cover requirements
- `development_length_tension_aci318()` - Development length calculation
- `reinforcement_bar_spacing_aci318()` - Bar spacing requirements

#### `foundationdesign_aci318.py`  
- `PadFoundationACI318` class - Main foundation analysis per ACI 318M-25
- `padFoundationDesignACI318()` - Complete design function
- ACI load combination implementations
- Updated analysis methods for ultimate and service conditions

#### Updated Examples
- `Concentric_Footing_ACI318_Example.ipynb` - Complete ACI 318M-25 design example
- Updated documentation and theory references

### Changed

#### Load Combinations
- **Before (Eurocode)**: ULS = 1.35D + 1.5L
- **After (ACI 318M-25)**: U = 1.2D + 1.6L (basic combination)
- Additional combinations for wind and minimum dead load cases

#### Flexural Design Method
- **Before**: Eurocode rectangular stress block with k-factor
- **After**: Whitney stress block with β₁ factor and strain compatibility

#### Shear Design Philosophy  
- **Before**: Eurocode VRd,c with complex expressions
- **After**: ACI simplified method Vc = 0.17λ√f'c bwd

#### Punching Shear Design
- **Before**: Eurocode critical perimeter at 2d from column
- **After**: ACI critical section at d/2 from column face
- **Before**: Single governing equation
- **After**: Three governing equations (aspect ratio, location, maximum)

#### Material Terminology
- **Before**: fck (characteristic compressive strength)
- **After**: f'c (specified compressive strength)
- **Before**: fyk (characteristic yield strength)  
- **After**: fy (specified yield strength)

#### Minimum Reinforcement
- **Before**: As,min = 0.078(fck^(2/3)/fyk) × bt × d
- **After**: As,min = max(1.4bd/fy, √f'c bd/(4fy))

### Package Structure Changes
- New file naming convention with `_aci318` suffix
- Separate modules for ACI 318M-25 implementation
- Updated `__init__.py` with ACI 318M-25 imports
- Updated `setup.py` with new package name and description

### Documentation Updates
- Updated README.md with ACI 318M-25 references
- New examples demonstrating ACI 318M-25 design process
- Updated API documentation with ACI section references
- Theory documentation updated for ACI design methods

### Validation and Testing
- Material property validation against ACI limits
- Load combination validation
- Design check validation against ACI requirements
- Updated test cases for ACI 318M-25 methods

## [0.1.2] - Previous Version (Eurocode 2)

### Features (Legacy - Eurocode 2 Based)
- Pad foundation design per Eurocode 2
- Combined footing design per Eurocode 2
- Eurocode load factors and partial safety factors
- Eurocode flexural and shear design methods

## Migration Guide

### For Existing Users
If you were using the Eurocode-based version, note these key changes:

1. **Class Names**: 
   - `PadFoundation` → `PadFoundationACI318`
   - `padFoundationDesign` → `padFoundationDesignACI318`

2. **Load Factors**:
   - Dead: 1.35 → 1.2
   - Live: 1.5 → 1.6

3. **Material Properties**:
   - Use f'c instead of fck
   - Use fy instead of fyk

4. **Design Methods**:
   - All calculations now follow ACI 318M-25
   - Different shear and flexural design approaches
   - New punching shear critical section location

### Backward Compatibility
- The original Eurocode modules remain available for legacy support
- Import the appropriate module based on your design standard preference

## Future Releases

### Planned for v0.3.0
- Combined footing design per ACI 318M-25
- Strip footing design per ACI 318M-25
- Seismic design provisions per ACI 318M-25 Chapter 18

### Planned for v0.4.0
- Mat foundation design per ACI 318M-25
- Pile cap design per ACI 318M-25
- Enhanced crack control provisions

---

**Contributors**: Kunle Yusuf  
**Repository**: https://github.com/buildsmart888/FoundationDesign-ACI318  
**License**: GPL-3.0
