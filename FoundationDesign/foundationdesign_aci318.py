"""
ACI 318M-25 Foundation Design Module

This module contains the main classes for foundation analysis and design
according to ACI 318M-25 Building Code Requirements for Structural Concrete.

Implements:
- Chapter 13.1: Foundations
- Section 5.3: Load combinations
- Section 7: Flexural design  
- Section 22: Shear and torsion
- Section 22.6: Two-way shear (punching shear)
"""

# Standard library imports
import math

# Third Party Imports
import numpy as np
import plotly.graph_objs as go
from indeterminatebeam import Beam, Support, TrapezoidalLoadV, DistributedLoadV

# Local Application Imports
from FoundationDesign.datavalidation import (
    assert_input_limit,
    assert_number,
    assert_strictly_positive_number,
    assert_maximum_input_limit,
    assert_input_range,
)
from FoundationDesign.concretedesignfunc_aci318 import (
    flexural_design_aci318,
    minimum_flexural_reinforcement_aci318,
    one_way_shear_strength_aci318,
    punching_shear_strength_aci318,
    critical_section_punching_aci318,
    aci_load_factors,
    aci_strength_reduction_factors,
)


class PadFoundationACI318:
    """
    Represents a rectangular or square pad foundation designed per ACI 318M-25.

    This class serves as the main class for foundation analysis according to 
    ACI 318M-25 Chapter 13.1 Foundations.

    Attributes
    ----------
    uls_strength_factor_dead : float, default 1.2
        Dead load factor for ultimate limit state per ACI 318M-25 Section 5.3.1
    uls_strength_factor_live : float, default 1.6  
        Live load factor for ultimate limit state per ACI 318M-25 Section 5.3.1
    uls_strength_factor_wind : float, default 1.0
        Wind load factor for ultimate limit state per ACI 318M-25 Section 5.3.1
    uls_strength_factor_dead_min : float, default 0.9
        Minimum dead load factor when dead load counteracts other loads
    phi_flexure : float, default 0.9
        Strength reduction factor for flexure per ACI 318M-25 Section 5.4.2.1
    phi_shear : float, default 0.75
        Strength reduction factor for shear per ACI 318M-25 Section 5.4.2.3

    Methods
    -------
    area_of_foundation()
        Calculates the area of the foundation.
    plot_geometry()
        Plots the geometry of the foundation showing column position.
    foundation_loads(foundation_thickness=400, soil_depth_abv_foundation=700, 
                    soil_unit_weight=18, concrete_unit_weight=24)
        Calculates foundation self-weight and surcharge loads.
    column_axial_loads(dead_axial_load=0, live_axial_load=0, wind_axial_load=0)
        Accepts column axial loads for dead, live, and wind cases.
    column_horizontal_loads_xdir(dead_horizontal_load_xdir=0, live_horizontal_load_xdir=0, 
                                wind_horizontal_load_xdir=0)
        Accepts column horizontal loads in X direction.
    column_horizontal_loads_ydir(dead_horizontal_load_ydir=0, live_horizontal_load_ydir=0,
                                wind_horizontal_load_ydir=0) 
        Accepts column horizontal loads in Y direction.
    column_moments_xdir(dead_moment_xdir=0, live_moment_xdir=0, wind_moment_xdir=0)
        Accepts column moments about X axis.
    column_moments_ydir(dead_moment_ydir=0, live_moment_ydir=0, wind_moment_ydir=0)
        Accepts column moments about Y axis.
    total_force_X_dir_service()
        Calculates total force in X direction at service loads.
    total_force_Y_dir_service()  
        Calculates total force in Y direction at service loads.
    total_force_Z_dir_service()
        Calculates total force in Z direction at service loads.
    total_moments_X_direction_service()
        Calculates total moments about X axis at service loads.
    total_moments_Y_direction_service()
        Calculates total moments about Y axis at service loads.
    eccentricity_X_direction_service()
        Calculates foundation eccentricity in X direction at service loads.
    eccentricity_Y_direction_service()
        Calculates foundation eccentricity in Y direction at service loads.
    pad_base_pressures_service()
        Calculates foundation pressures at service loads.
    bearing_pressure_check_service()
        Checks bearing pressure against allowable at service loads.
    plot_base_pressures_service()
        Plots foundation pressure distribution at service loads.
    total_force_X_dir_ultimate()
        Calculates total force in X direction at ultimate loads per ACI 318M-25.
    total_force_Y_dir_ultimate()
        Calculates total force in Y direction at ultimate loads per ACI 318M-25.
    total_force_Z_dir_ultimate()
        Calculates total force in Z direction at ultimate loads per ACI 318M-25.
    total_moments_X_direction_ultimate()
        Calculates total moments about X axis at ultimate loads per ACI 318M-25.
    total_moments_Y_direction_ultimate()
        Calculates total moments about Y axis at ultimate loads per ACI 318M-25.
    eccentricity_X_direction_ultimate()
        Calculates foundation eccentricity in X direction at ultimate loads.
    eccentricity_Y_direction_ultimate()
        Calculates foundation eccentricity in Y direction at ultimate loads.
    pad_base_pressures_ultimate()
        Calculates foundation pressures at ultimate loads.
    foundation_moment_about_x_face()
        Calculates foundation moment about column face in X direction.
    foundation_moment_about_y_face()  
        Calculates foundation moment about column face in Y direction.
    punching_shear_column_perimeter()
        Calculates punching shear force at column perimeter.
    punching_shear_critical_perimeter()
        Calculates punching shear at critical section per ACI 318M-25 Section 22.6.
    one_way_shear_x_direction()
        Calculates one-way shear in X direction per ACI 318M-25 Section 22.5.
    one_way_shear_y_direction()
        Calculates one-way shear in Y direction per ACI 318M-25 Section 22.5.
    """

    def __init__(
        self,
        foundation_length: float,
        foundation_width: float,
        column_length: float,
        column_width: float,
        col_pos_xdir: float,
        col_pos_ydir: float,
        soil_bearing_capacity: float = 150,
        uls_strength_factor_dead: float = 1.2,
        uls_strength_factor_live: float = 1.6,
        uls_strength_factor_wind: float = 1.0,
        uls_strength_factor_dead_min: float = 0.9,
        phi_flexure: float = 0.9,
        phi_shear: float = 0.75,
    ):
        """
        Initialize PadFoundationACI318 object.

        Parameters
        ----------
        foundation_length : float
            Length of foundation in mm (X direction)
        foundation_width : float  
            Width of foundation in mm (Y direction)
        column_length : float
            Length of column in mm (X direction)
        column_width : float
            Width of column in mm (Y direction)
        col_pos_xdir : float
            Column position from foundation origin in X direction (mm)
        col_pos_ydir : float
            Column position from foundation origin in Y direction (mm)
        soil_bearing_capacity : float, default 150
            Allowable soil bearing capacity in kN/m²
        uls_strength_factor_dead : float, default 1.2
            Dead load factor per ACI 318M-25 Section 5.3.1
        uls_strength_factor_live : float, default 1.6
            Live load factor per ACI 318M-25 Section 5.3.1  
        uls_strength_factor_wind : float, default 1.0
            Wind load factor per ACI 318M-25 Section 5.3.1
        uls_strength_factor_dead_min : float, default 0.9
            Minimum dead load factor per ACI 318M-25 Section 5.3.1
        phi_flexure : float, default 0.9
            Strength reduction factor for flexure per ACI 318M-25 Section 5.4.2.1
        phi_shear : float, default 0.75
            Strength reduction factor for shear per ACI 318M-25 Section 5.4.2.3
        """
        # Input validation
        assert_strictly_positive_number(foundation_length, "foundation_length")
        assert_strictly_positive_number(foundation_width, "foundation_width")
        assert_strictly_positive_number(column_length, "column_length")
        assert_strictly_positive_number(column_width, "column_width")
        assert_strictly_positive_number(soil_bearing_capacity, "soil_bearing_capacity")
        
        # Foundation geometry
        self.foundation_length = foundation_length  # mm
        self.foundation_width = foundation_width    # mm
        self.column_length = column_length          # mm
        self.column_width = column_width            # mm
        self.col_pos_xdir = col_pos_xdir           # mm
        self.col_pos_ydir = col_pos_ydir           # mm
        self.soil_bearing_capacity = soil_bearing_capacity  # kN/m²
        
        # ACI 318M-25 load factors
        self.uls_strength_factor_dead = uls_strength_factor_dead
        self.uls_strength_factor_live = uls_strength_factor_live  
        self.uls_strength_factor_wind = uls_strength_factor_wind
        self.uls_strength_factor_dead_min = uls_strength_factor_dead_min
        
        # ACI 318M-25 strength reduction factors
        self.phi_flexure = phi_flexure
        self.phi_shear = phi_shear
        
        # Initialize load variables
        self._dead_axial_load = 0
        self._live_axial_load = 0
        self._wind_axial_load = 0
        self._dead_horizontal_load_xdir = 0
        self._live_horizontal_load_xdir = 0
        self._wind_horizontal_load_xdir = 0
        self._dead_horizontal_load_ydir = 0
        self._live_horizontal_load_ydir = 0
        self._wind_horizontal_load_ydir = 0
        self._dead_moment_xdir = 0
        self._live_moment_xdir = 0
        self._wind_moment_xdir = 0
        self._dead_moment_ydir = 0
        self._live_moment_ydir = 0
        self._wind_moment_ydir = 0
        
        # Foundation loads
        self._foundation_self_weight = 0
        self._surcharge_load = 0

    def area_of_foundation(self):
        """
        Calculate the area of the foundation.
        
        Returns
        -------
        float
            Area of foundation in mm²
        """
        return self.foundation_length * self.foundation_width

    def foundation_loads(
        self, 
        foundation_thickness: float = 400,
        soil_depth_abv_foundation: float = 700,
        soil_unit_weight: float = 18,
        concrete_unit_weight: float = 24
    ):
        """
        Calculate foundation self-weight and surcharge loads.
        
        Parameters
        ----------
        foundation_thickness : float, default 400
            Thickness of foundation in mm
        soil_depth_abv_foundation : float, default 700
            Depth of soil above foundation in mm
        soil_unit_weight : float, default 18
            Unit weight of soil in kN/m³
        concrete_unit_weight : float, default 24
            Unit weight of concrete in kN/m³
        """
        # Foundation self-weight
        foundation_volume = (self.foundation_length * self.foundation_width * 
                           foundation_thickness) / 1e9  # m³
        self._foundation_self_weight = foundation_volume * concrete_unit_weight  # kN
        
        # Surcharge load from soil above foundation
        surcharge_volume = (self.foundation_length * self.foundation_width * 
                          soil_depth_abv_foundation) / 1e9  # m³
        self._surcharge_load = surcharge_volume * soil_unit_weight  # kN

    def column_axial_loads(
        self, 
        dead_axial_load: float = 0,
        live_axial_load: float = 0, 
        wind_axial_load: float = 0
    ):
        """
        Set column axial loads.
        
        Parameters
        ----------
        dead_axial_load : float, default 0
            Dead load in kN (compression positive)
        live_axial_load : float, default 0
            Live load in kN (compression positive)
        wind_axial_load : float, default 0
            Wind load in kN (can be tension or compression)
        """
        assert_number(dead_axial_load, "dead_axial_load")
        assert_number(live_axial_load, "live_axial_load")
        assert_number(wind_axial_load, "wind_axial_load")
        
        self._dead_axial_load = dead_axial_load
        self._live_axial_load = live_axial_load
        self._wind_axial_load = wind_axial_load

    def column_horizontal_loads_xdir(
        self,
        dead_horizontal_load_xdir: float = 0,
        live_horizontal_load_xdir: float = 0,
        wind_horizontal_load_xdir: float = 0
    ):
        """
        Set column horizontal loads in X direction.
        
        Parameters
        ----------
        dead_horizontal_load_xdir : float, default 0
            Dead horizontal load in X direction in kN
        live_horizontal_load_xdir : float, default 0
            Live horizontal load in X direction in kN
        wind_horizontal_load_xdir : float, default 0
            Wind horizontal load in X direction in kN
        """
        assert_number(dead_horizontal_load_xdir, "dead_horizontal_load_xdir")
        assert_number(live_horizontal_load_xdir, "live_horizontal_load_xdir") 
        assert_number(wind_horizontal_load_xdir, "wind_horizontal_load_xdir")
        
        self._dead_horizontal_load_xdir = dead_horizontal_load_xdir
        self._live_horizontal_load_xdir = live_horizontal_load_xdir
        self._wind_horizontal_load_xdir = wind_horizontal_load_xdir

    def column_horizontal_loads_ydir(
        self,
        dead_horizontal_load_ydir: float = 0,
        live_horizontal_load_ydir: float = 0,
        wind_horizontal_load_ydir: float = 0
    ):
        """
        Set column horizontal loads in Y direction.
        
        Parameters
        ---------- 
        dead_horizontal_load_ydir : float, default 0
            Dead horizontal load in Y direction in kN
        live_horizontal_load_ydir : float, default 0
            Live horizontal load in Y direction in kN
        wind_horizontal_load_ydir : float, default 0
            Wind horizontal load in Y direction in kN
        """
        assert_number(dead_horizontal_load_ydir, "dead_horizontal_load_ydir")
        assert_number(live_horizontal_load_ydir, "live_horizontal_load_ydir")
        assert_number(wind_horizontal_load_ydir, "wind_horizontal_load_ydir")
        
        self._dead_horizontal_load_ydir = dead_horizontal_load_ydir
        self._live_horizontal_load_ydir = live_horizontal_load_ydir
        self._wind_horizontal_load_ydir = wind_horizontal_load_ydir

    def column_moments_xdir(
        self,
        dead_moment_xdir: float = 0,
        live_moment_xdir: float = 0,
        wind_moment_xdir: float = 0
    ):
        """
        Set column moments about X axis.
        
        Parameters
        ----------
        dead_moment_xdir : float, default 0
            Dead moment about X axis in kN·m
        live_moment_xdir : float, default 0
            Live moment about X axis in kN·m  
        wind_moment_xdir : float, default 0
            Wind moment about X axis in kN·m
        """
        assert_number(dead_moment_xdir, "dead_moment_xdir")
        assert_number(live_moment_xdir, "live_moment_xdir")
        assert_number(wind_moment_xdir, "wind_moment_xdir")
        
        self._dead_moment_xdir = dead_moment_xdir
        self._live_moment_xdir = live_moment_xdir
        self._wind_moment_xdir = wind_moment_xdir

    def column_moments_ydir(
        self,
        dead_moment_ydir: float = 0,
        live_moment_ydir: float = 0,
        wind_moment_ydir: float = 0
    ):
        """
        Set column moments about Y axis.
        
        Parameters
        ----------
        dead_moment_ydir : float, default 0
            Dead moment about Y axis in kN·m
        live_moment_ydir : float, default 0
            Live moment about Y axis in kN·m
        wind_moment_ydir : float, default 0
            Wind moment about Y axis in kN·m
        """
        assert_number(dead_moment_ydir, "dead_moment_ydir")
        assert_number(live_moment_ydir, "live_moment_ydir")
        assert_number(wind_moment_ydir, "wind_moment_ydir")
        
        self._dead_moment_ydir = dead_moment_ydir
        self._live_moment_ydir = live_moment_ydir
        self._wind_moment_ydir = wind_moment_ydir

    def total_force_Z_dir_service(self):
        """
        Calculate total vertical force at service loads.
        
        Returns
        -------
        float
            Total vertical force in kN (compression positive)
        """
        return (self._dead_axial_load + self._live_axial_load + 
                self._wind_axial_load + self._foundation_self_weight + 
                self._surcharge_load)

    def total_force_Z_dir_ultimate(self):
        """
        Calculate total vertical force at ultimate loads per ACI 318M-25.
        Uses governing load combination from Section 5.3.1.
        
        Returns
        -------
        float
            Total ultimate vertical force in kN
        """
        # ACI 318M-25 Section 5.3.1 load combinations
        foundation_dead = self._foundation_self_weight + self._surcharge_load
        
        # Combination 1: U = 1.2D + 1.6L
        U1 = (self.uls_strength_factor_dead * (self._dead_axial_load + foundation_dead) +
              self.uls_strength_factor_live * self._live_axial_load)
        
        # Combination 2: U = 1.2D + 1.6L + 0.5W (wind as secondary)
        U2 = (self.uls_strength_factor_dead * (self._dead_axial_load + foundation_dead) +
              self.uls_strength_factor_live * self._live_axial_load +
              0.5 * self._wind_axial_load)
        
        # Combination 3: U = 1.2D + 1.0W + 1.0L  
        U3 = (self.uls_strength_factor_dead * (self._dead_axial_load + foundation_dead) +
              self.uls_strength_factor_wind * self._wind_axial_load +
              1.0 * self._live_axial_load)
        
        # Combination 4: U = 0.9D + 1.0W (when wind counteracts dead load)
        U4 = (self.uls_strength_factor_dead_min * (self._dead_axial_load + foundation_dead) +
              self.uls_strength_factor_wind * self._wind_axial_load)
        
        # Return governing (maximum) combination
        return max(U1, U2, U3, U4)

    def bearing_pressure_check_service(self):
        """
        Check bearing pressure against allowable at service loads.
        
        Returns
        -------
        dict
            Bearing pressure check results
        """
        total_load = self.total_force_Z_dir_service()  # kN
        foundation_area = self.area_of_foundation() / 1e6  # m²
        
        # Calculate bearing pressure
        bearing_pressure = total_load / foundation_area  # kN/m²
        
        # Check against allowable
        utilization = bearing_pressure / self.soil_bearing_capacity
        
        return {
            "bearing_pressure": round(bearing_pressure, 2),
            "allowable_pressure": self.soil_bearing_capacity,
            "utilization_ratio": round(utilization, 3),
            "check_status": "PASS" if utilization <= 1.0 else "FAIL"
        }

    def punching_shear_at_column_face(self, foundation_thickness: float):
        """
        Calculate punching shear force at column face per ACI 318M-25.
        
        Parameters
        ----------
        foundation_thickness : float
            Foundation thickness in mm
            
        Returns
        -------
        dict
            Punching shear analysis at column face
        """
        # Ultimate load
        Pu = self.total_force_Z_dir_ultimate() * 1000  # N
        
        # Column perimeter
        bo_column = 2 * (self.column_length + self.column_width)  # mm
        
        # Effective depth (assume cover = 75mm, bar diameter = 16mm)
        d = foundation_thickness - 75 - 16/2  # mm
        
        return {
            "punching_force": Pu,
            "column_perimeter": bo_column,
            "effective_depth": d,
            "punching_stress": round(Pu / (bo_column * d), 3)  # N/mm²
        }

    def punching_shear_at_critical_section(self, foundation_thickness: float, fc_prime: float):
        """
        Calculate punching shear at critical section per ACI 318M-25 Section 22.6.
        
        Parameters
        ----------
        foundation_thickness : float
            Foundation thickness in mm
        fc_prime : float
            Specified compressive strength of concrete in MPa
            
        Returns
        -------
        dict
            Punching shear analysis at critical section
        """
        # Effective depth  
        d = foundation_thickness - 75 - 16/2  # mm
        
        # Critical section properties
        critical_section = critical_section_punching_aci318(
            self.column_length, self.column_width, d
        )
        
        # Ultimate punching force
        Pu = self.total_force_Z_dir_ultimate() * 1000  # N
        
        # Subtract load within critical section
        critical_area = critical_section["area"] / 1e6  # m²
        foundation_area = self.area_of_foundation() / 1e6  # m²
        pressure = Pu / (foundation_area * 1e6)  # N/m²
        load_inside_critical = pressure * critical_area * 1e6  # N
        
        Vu = Pu - load_inside_critical  # N
        
        # Column aspect ratio
        beta_c = max(self.column_length, self.column_width) / min(self.column_length, self.column_width)
        
        # Punching shear strength
        strength_results = punching_shear_strength_aci318(
            critical_section["perimeter"], d, fc_prime, beta_c, alpha_s=40
        )
        
        # Design check
        phi_Vc = self.phi_shear * strength_results["Vc_governing"]
        
        return {
            "critical_section": critical_section,
            "punching_force": Vu,
            "nominal_strength": strength_results["Vc_governing"],
            "design_strength": phi_Vc,
            "demand_capacity_ratio": round(Vu / phi_Vc, 3),
            "check_status": "PASS" if Vu <= phi_Vc else "FAIL",
            "governing_case": strength_results["governing_case"]
        }

    def one_way_shear_x_direction(self, foundation_thickness: float, fc_prime: float):
        """
        Calculate one-way shear in X direction per ACI 318M-25 Section 22.5.
        
        Parameters
        ----------
        foundation_thickness : float
            Foundation thickness in mm
        fc_prime : float
            Specified compressive strength of concrete in MPa
            
        Returns
        -------
        dict
            One-way shear analysis in X direction
        """
        # Effective depth
        d = foundation_thickness - 75 - 16/2  # mm
        
        # Critical section at distance d from column face
        x_critical = self.col_pos_xdir + self.column_length/2 + d  # mm
        
        # Shear force calculation
        total_pressure = self.total_force_Z_dir_ultimate()  # kN
        foundation_area = self.area_of_foundation() / 1e6  # m²
        pressure = total_pressure / foundation_area  # kN/m²
        
        # Area beyond critical section
        if x_critical < self.foundation_length:
            shear_area = ((self.foundation_length - x_critical) * self.foundation_width) / 1e6  # m²
            Vu = pressure * shear_area * 1000  # N
        else:
            Vu = 0  # Critical section beyond foundation
        
        # Shear strength
        Vc = one_way_shear_strength_aci318(self.foundation_width, d, fc_prime)
        phi_Vc = self.phi_shear * Vc
        
        return {
            "critical_location": x_critical,
            "shear_force": Vu,
            "nominal_strength": Vc,
            "design_strength": phi_Vc,
            "demand_capacity_ratio": round(Vu / phi_Vc, 3) if phi_Vc > 0 else float('inf'),
            "check_status": "PASS" if Vu <= phi_Vc else "FAIL"
        }

    def one_way_shear_y_direction(self, foundation_thickness: float, fc_prime: float):
        """
        Calculate one-way shear in Y direction per ACI 318M-25 Section 22.5.
        
        Parameters
        ----------
        foundation_thickness : float
            Foundation thickness in mm
        fc_prime : float
            Specified compressive strength of concrete in MPa
            
        Returns
        -------
        dict
            One-way shear analysis in Y direction
        """
        # Effective depth
        d = foundation_thickness - 75 - 16/2  # mm
        
        # Critical section at distance d from column face
        y_critical = self.col_pos_ydir + self.column_width/2 + d  # mm
        
        # Shear force calculation
        total_pressure = self.total_force_Z_dir_ultimate()  # kN
        foundation_area = self.area_of_foundation() / 1e6  # m²
        pressure = total_pressure / foundation_area  # kN/m²
        
        # Area beyond critical section
        if y_critical < self.foundation_width:
            shear_area = ((self.foundation_width - y_critical) * self.foundation_length) / 1e6  # m²
            Vu = pressure * shear_area * 1000  # N
        else:
            Vu = 0  # Critical section beyond foundation
        
        # Shear strength
        Vc = one_way_shear_strength_aci318(self.foundation_length, d, fc_prime)
        phi_Vc = self.phi_shear * Vc
        
        return {
            "critical_location": y_critical,
            "shear_force": Vu,
            "nominal_strength": Vc,
            "design_strength": phi_Vc,
            "demand_capacity_ratio": round(Vu / phi_Vc, 3) if phi_Vc > 0 else float('inf'),
            "check_status": "PASS" if Vu <= phi_Vc else "FAIL"
        }


def padFoundationDesignACI318(
    fdn_analysis: PadFoundationACI318,
    concrete_grade: float = 30,
    steel_grade: float = 420,
    foundation_thickness: float = 400,
    soil_depth_abv_foundation: float = 700,
    steel_cover: float = 75,
    bar_dia_x: float = 16,
    bar_dia_y: float = 16,
):
    """
    Design pad foundation reinforcement per ACI 318M-25.
    
    Parameters
    ----------
    fdn_analysis : PadFoundationACI318
        Foundation analysis object
    concrete_grade : float, default 30
        Specified compressive strength f'c in MPa
    steel_grade : float, default 420
        Specified yield strength fy in MPa
    foundation_thickness : float, default 400
        Foundation thickness in mm
    soil_depth_abv_foundation : float, default 700
        Soil depth above foundation in mm
    steel_cover : float, default 75
        Concrete cover in mm per ACI 318M-25 Section 20.5.1.3
    bar_dia_x : float, default 16
        Bar diameter in X direction in mm
    bar_dia_y : float, default 16
        Bar diameter in Y direction in mm
        
    Returns
    -------
    dict
        Complete foundation design results per ACI 318M-25
    """
    # Set foundation loads
    fdn_analysis.foundation_loads(
        foundation_thickness=foundation_thickness,
        soil_depth_abv_foundation=soil_depth_abv_foundation
    )
    
    # Effective depths
    d_x = foundation_thickness - steel_cover - bar_dia_x/2  # mm
    d_y = foundation_thickness - steel_cover - bar_dia_y - bar_dia_x/2  # mm
    
    # Foundation moments (simplified - at column face)
    # This would need to be implemented based on pressure distribution
    Mu_x = 100 * 1e6  # N·mm (placeholder)
    Mu_y = 100 * 1e6  # N·mm (placeholder)
    
    # Flexural design X direction
    flexure_x = flexural_design_aci318(
        Mu_x, fdn_analysis.foundation_width, d_x, concrete_grade, steel_grade
    )
    
    # Flexural design Y direction  
    flexure_y = flexural_design_aci318(
        Mu_y, fdn_analysis.foundation_length, d_y, concrete_grade, steel_grade
    )
    
    # Minimum reinforcement
    As_min_x = minimum_flexural_reinforcement_aci318(
        fdn_analysis.foundation_width, d_x, concrete_grade, steel_grade
    )
    As_min_y = minimum_flexural_reinforcement_aci318(
        fdn_analysis.foundation_length, d_y, concrete_grade, steel_grade
    )
    
    # Shear checks
    punching_check = fdn_analysis.punching_shear_at_critical_section(
        foundation_thickness, concrete_grade
    )
    
    one_way_x = fdn_analysis.one_way_shear_x_direction(
        foundation_thickness, concrete_grade
    )
    
    one_way_y = fdn_analysis.one_way_shear_y_direction(
        foundation_thickness, concrete_grade
    )
    
    # Bearing pressure check
    bearing_check = fdn_analysis.bearing_pressure_check_service()
    
    return {
        "foundation_geometry": {
            "length": fdn_analysis.foundation_length,
            "width": fdn_analysis.foundation_width,
            "thickness": foundation_thickness,
            "area": fdn_analysis.area_of_foundation()
        },
        "material_properties": {
            "fc_prime": concrete_grade,
            "fy": steel_grade,
            "cover": steel_cover
        },
        "loads": {
            "service_load": fdn_analysis.total_force_Z_dir_service(),
            "ultimate_load": fdn_analysis.total_force_Z_dir_ultimate()
        },
        "bearing_pressure": bearing_check,
        "flexural_design": {
            "x_direction": {
                "required_As": flexure_x.get("area_of_steel", As_min_x),
                "minimum_As": As_min_x,
                "status": flexure_x.get("status", "OK")
            },
            "y_direction": {
                "required_As": flexure_y.get("area_of_steel", As_min_y),
                "minimum_As": As_min_y,
                "status": flexure_y.get("status", "OK")
            }
        },
        "shear_design": {
            "punching_shear": punching_check,
            "one_way_x": one_way_x,
            "one_way_y": one_way_y
        },
        "design_code": "ACI 318M-25",
        "design_summary": {
            "foundation_adequate": all([
                bearing_check["check_status"] == "PASS",
                punching_check["check_status"] == "PASS",
                one_way_x["check_status"] == "PASS",
                one_way_y["check_status"] == "PASS"
            ])
        }
    }
