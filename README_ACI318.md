# FoundationDesign-ACI318

[![PyPi](https://img.shields.io/pypi/v/FoundationDesign-ACI318.svg)](https://pypi.org/project/FoundationDesign-ACI318/)
![PyPI - License](https://img.shields.io/pypi/l/FoundationDesign-ACI318)
[![Downloads](https://static.pepy.tech/badge/foundationdesign-aci318)](https://pepy.tech/project/foundationdesign-aci318)
[![Downloads](https://static.pepy.tech/badge/foundationdesign-aci318/month)](https://pepy.tech/project/foundationdesign-aci318)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/FoundationDesign-ACI318)
[![build & test](https://github.com/buildsmart888/FoundationDesign-ACI318/actions/workflows/build-and-test.yml/badge.svg?branch=main)](https://github.com/buildsmart888/FoundationDesign-ACI318/actions/workflows/build-and-test.yml)
[![Documentation Status](https://readthedocs.org/projects/foundationdesign-aci318/badge/?version=latest)](https://foundationdesign-aci318.readthedocs.io/en/latest/?badge=latest)
[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/format.json)](https://github.com/charliermarsh/ruff)

🚀 **New Version**: Updated to comply with **ACI 318M-25 Chapter 13.1 Foundations** standards for comprehensive foundation design and analysis.

---

FoundationDesign-ACI318 is a Python module for the structural analysis and design of different foundation types in accordance with **ACI 318M-25 Chapter 13.1 Foundations**. This project provides a free, open-source Python package that can be used to analyze and design foundations with results comparable to commercial software.

## Key Features

This module is useful for determining:

- **Flexural Design**: Critical bending moments and reinforcement requirements per ACI 318M-25 Section 7
- **Shear Analysis**: One-way and two-way shear checks according to ACI 318M-25 Section 22
- **Punching Shear**: Critical punching shear analysis per ACI 318M-25 Section 22.6
- **Load Combinations**: Ultimate and service load combinations per ACI 318M-25 Section 5.3
- **Reinforcement Provisions**: Minimum and maximum steel requirements per ACI 318M-25 Section 7.6
- **Bearing Pressure**: Soil bearing capacity checks and foundation sizing
- **Crack Control**: Service load crack width limitations per ACI 318M-25 Section 10.6

## Design Standards Compliance

The project is based on:
- **ACI 318M-25**: Building Code Requirements for Structural Concrete (Metric)
- **Chapter 13.1**: Foundations
- **Section 5.3**: Load combinations and load factors
- **Section 7**: Flexural design requirements
- **Section 22**: Shear and torsion design
- **Section 22.6**: Two-way shear (punching shear)

## Supported Foundation Types

Currently supports:
- **Isolated Pad Foundations** (Concentric and Eccentric loading)
- **Combined Pad Foundations** (Two-column footings)
- **Future**: Strip footings, mat foundations, and pile caps

## Quick Start Example

### Basic Pad Foundation Design

```python
from FoundationDesign import PadFoundation, padFoundationDesign

# Create foundation object
# Foundation dimensions: 2.5m x 2.5m
# Column dimensions: 400mm x 400mm  
# Concentric loading (column at center)
# Allowable soil bearing capacity: 200 kN/m²
fdn = PadFoundation(
    foundation_length=2500,      # mm
    foundation_width=2500,       # mm
    column_length=400,           # mm
    column_width=400,            # mm
    col_pos_xdir=1250,          # mm (center position)
    col_pos_ydir=1250,          # mm (center position)
    soil_bearing_capacity=200,   # kN/m²
)

# Apply loads (ACI 318M-25 load combinations will be applied automatically)
fdn.column_axial_loads(
    permanent_axial_load=800,    # Dead load (kN)
    imposed_axial_load=300,      # Live load (kN)
    wind_axial_load=0           # Wind load (kN)
)

# Check foundation adequacy
pressure_check = fdn.bearing_pressure_check_sls()
print(f"Foundation pressure check: {pressure_check}")

# Design reinforcement
design = padFoundationDesign(
    fdn_analysis=fdn,
    concrete_grade=30,           # f'c = 30 MPa
    steel_grade=420,             # fy = 420 MPa  
    foundation_thickness=400,    # mm
    soil_depth_abv_foundation=700, # mm
    steel_cover=75,              # mm (per ACI 318M-25 Section 20.5.1.3)
    bar_dia_x=16,               # mm
    bar_dia_y=16,               # mm
)

# Get design results
results = design.design_results()
print("Foundation Design Results (ACI 318M-25):")
print(f"Required As,x: {results['reinforcement_x_dir']['area_of_steel']} mm²/m")
print(f"Required As,y: {results['reinforcement_y_dir']['area_of_steel']} mm²/m")
print(f"Punching shear check: {results['punching_shear']['check_status']}")
```

### ACI 318M-25 Load Factors

The module automatically applies ACI 318M-25 load combinations:

**Ultimate Limit State (ULS) - Section 5.3.1:**
- U = 1.2D + 1.6L + 0.5(S or R)
- U = 1.2D + 1.6(L or S or R) + (1.0W or 0.5W)
- U = 1.2D + 1.0W + 1.0L + 0.5(S or R)
- U = 0.9D + 1.0W

**Service Limit State (SLS):**
- Service loads without factors for deflection and crack control

## Installation

### From PyPI (Recommended)
```bash
pip install FoundationDesign-ACI318
```

### From Source
```bash
git clone https://github.com/buildsmart888/FoundationDesign-ACI318.git
cd FoundationDesign-ACI318
pip install -e .
```

## Documentation

Comprehensive documentation with examples and theory:
- [Full Documentation](https://foundationdesign-aci318.readthedocs.io/)
- [API Reference](https://foundationdesign-aci318.readthedocs.io/en/latest/api.html)
- [Design Examples](https://foundationdesign-aci318.readthedocs.io/en/latest/examples.html)
- [ACI 318M-25 Implementation](https://foundationdesign-aci318.readthedocs.io/en/latest/theory.html)

## Examples

Interactive Jupyter notebook examples:
- [Concentric Pad Foundation (ACI 318M-25)](https://colab.research.google.com/github/buildsmart888/FoundationDesign-ACI318/blob/main/examples/Concentric_Footing_ACI318_Example.ipynb)
- [Eccentric Pad Foundation (ACI 318M-25)](https://colab.research.google.com/github/buildsmart888/FoundationDesign-ACI318/blob/main/examples/Eccentric_Footing_ACI318_Example.ipynb)
- [Combined Footing Design (ACI 318M-25)](https://colab.research.google.com/github/buildsmart888/FoundationDesign-ACI318/blob/main/examples/Combined_Footing_ACI318_Example.ipynb)

## Key Differences from Eurocode Version

This ACI 318M-25 implementation includes:

1. **Load Factors**: ACI 318M-25 Section 5.3 combinations instead of Eurocode partial factors
2. **Flexural Design**: Whitney stress block and ACI strength reduction factors
3. **Minimum Steel**: ACI 318M-25 Section 7.6 requirements  
4. **Shear Design**: ACI 318M-25 Section 22 simplified and detailed methods
5. **Punching Shear**: ACI 318M-25 Section 22.6 critical section and design provisions
6. **Material Properties**: ACI material strength definitions (f'c, fy)
7. **Cover Requirements**: ACI 318M-25 Section 20.5 concrete cover provisions

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Roadmap

- [x] Isolated Pad Foundation Design (ACI 318M-25)
- [x] Combined Footing Design (ACI 318M-25)  
- [ ] Strip Footing Design (ACI 318M-25)
- [ ] Mat Foundation Design (ACI 318M-25)
- [ ] Pile Cap Design (ACI 318M-25)
- [ ] Seismic Design Provisions (ACI 318M-25 Chapter 18)
- [ ] Web-based Calculator Interface

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this software in your research, please cite:

```bibtex
@software{foundationdesign_aci318,
  author = {Yusuf, Kunle},
  title = {FoundationDesign-ACI318: Python library for foundation design per ACI 318M-25},
  url = {https://github.com/buildsmart888/FoundationDesign-ACI318},
  version = {0.2.0},
  year = {2025}
}
```

## Support

- 📧 Email: kunleyusuf858@gmail.com
- 🐛 Bug Reports: [GitHub Issues](https://github.com/buildsmart888/FoundationDesign-ACI318/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/buildsmart888/FoundationDesign-ACI318/discussions)
- 📚 Documentation: [ReadTheDocs](https://foundationdesign-aci318.readthedocs.io/)

---

**Note**: This software is provided for educational and professional use. Users should verify all results and comply with local building codes and engineering judgment in their specific applications.
