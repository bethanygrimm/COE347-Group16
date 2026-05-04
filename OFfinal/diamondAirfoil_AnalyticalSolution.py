import numpy as np
from scipy.optimize import brentq, minimize_scalar


# Compressible flow functions (Oblique shock and Prandtl-Meyer expansion)
def p0_over_p(M, gamma=1.4):
    return (1 + (gamma - 1) / 2 * M**2) ** (gamma / (gamma - 1))


def prandtl_meyer(M, gamma=1.4):
    if M <= 1:
        raise ValueError("Prandtl-Meyer expansion requires M > 1.")

    return (
        np.sqrt((gamma + 1) / (gamma - 1))
        * np.arctan(np.sqrt((gamma - 1) / (gamma + 1) * (M**2 - 1)))
        - np.arctan(np.sqrt(M**2 - 1))
    )


def mach_from_pm(nu_target, gamma=1.4):
    return brentq(
        lambda M: prandtl_meyer(M, gamma) - nu_target,
        1.000001,
        100.0,
    )


def theta_from_beta(beta, M, gamma=1.4):
    return np.arctan(
        2 / np.tan(beta)
        * (M**2 * np.sin(beta)**2 - 1)
        / (M**2 * (gamma + np.cos(2 * beta)) + 2)
    )


def max_deflection_angle(M, gamma=1.4):
    beta_min = np.arcsin(1 / M) + 1e-8
    beta_max = np.pi / 2 - 1e-8

    result = minimize_scalar(
        lambda beta: -theta_from_beta(beta, M, gamma),
        bounds=(beta_min, beta_max),
        method="bounded",
    )

    return -result.fun


def oblique_shock(M1, theta_deg, gamma=1.4):
    theta = np.radians(theta_deg)

    if theta < 1e-12:
        return M1, 1.0, None

    theta_max = max_deflection_angle(M1, gamma)

    if theta > theta_max:
        raise ValueError(
            f"Detached shock: theta = {theta_deg:.3f} deg exceeds "
            f"theta_max = {np.degrees(theta_max):.3f} deg for M = {M1:.3f}"
        )

    beta_min = np.arcsin(1 / M1) + 1e-8
    beta_max = np.pi / 2 - 1e-8

    beta_values = np.linspace(beta_min, beta_max, 3000)
    f_values = theta_from_beta(beta_values, M1, gamma) - theta

    roots = []

    for i in range(len(beta_values) - 1):
        if f_values[i] * f_values[i + 1] < 0:
            root = brentq(
                lambda beta: theta_from_beta(beta, M1, gamma) - theta,
                beta_values[i],
                beta_values[i + 1],
                xtol=1e-12,
                rtol=1e-12,
            )
            roots.append(root)

    if len(roots) == 0:
        raise ValueError(
            f"No attached oblique shock root found for "
            f"M = {M1:.3f}, theta = {theta_deg:.3f} deg"
        )

    beta = min(roots)

    Mn1 = M1 * np.sin(beta)

    p2_p1 = 1 + 2 * gamma / (gamma + 1) * (Mn1**2 - 1)

    Mn2_sq = (1 + (gamma - 1) / 2 * Mn1**2) / (
        gamma * Mn1**2 - (gamma - 1) / 2
    )

    Mn2 = np.sqrt(Mn2_sq)

    M2 = Mn2 / np.sin(beta - theta)

    return M2, p2_p1, np.degrees(beta)


def expansion_fan(M1, theta_deg, gamma=1.4):
    theta = np.radians(theta_deg)

    if theta < 1e-12:
        return M1, 1.0

    nu1 = prandtl_meyer(M1, gamma)
    nu2 = nu1 + theta

    M2 = mach_from_pm(nu2, gamma)

    p2_p1 = p0_over_p(M1, gamma) / p0_over_p(M2, gamma)

    return M2, p2_p1

# Airfoil functions

def apply_turn(M1, p1_pinf, signed_turn_deg, gamma=1.4):
    """
    Main convention:

        signed_turn_deg > 0  --> compression shock
        signed_turn_deg < 0  --> Prandtl-Meyer expansion

    This is the same convention used in the hand solution.
    """

    if abs(signed_turn_deg) < 1e-12:
        return {
            "M": M1,
            "p/pinf": p1_pinf,
            "wave": "none",
            "turn_deg": signed_turn_deg,
            "beta_deg": None,
        }

    if signed_turn_deg > 0:
        M2, p2_p1, beta = oblique_shock(M1, signed_turn_deg, gamma)
        wave = "shock"
    else:
        M2, p2_p1 = expansion_fan(M1, abs(signed_turn_deg), gamma)
        beta = None
        wave = "expansion"

    return {
        "M": M2,
        "p/pinf": p1_pinf * p2_p1,
        "wave": wave,
        "turn_deg": signed_turn_deg,
        "beta_deg": beta,
    }


def pressure_coefficient(p_pinf, M_inf, gamma=1.4):
    return (p_pinf - 1) / (0.5 * gamma * M_inf**2)


def outward_normal(side, panel_angle_deg):
    """
    Normal vectors in chord-fixed axes.
    x is along chord.
    y is upward normal to chord.
    """

    theta = np.radians(panel_angle_deg)

    if side == "upper":
        return np.array([-np.sin(theta), np.cos(theta)])
    elif side == "lower":
        return np.array([np.sin(theta), -np.cos(theta)])
    else:
        raise ValueError("side must be 'upper' or 'lower'")


def diamond_airfoil(M_inf=3.0, alpha_deg=15.0, eps_deg=10.0, chord=1.0, gamma=1.4):
    eps_rad = np.radians(eps_deg)
    alpha_rad = np.radians(alpha_deg)

    ell = chord / (2 * np.cos(eps_rad))
    ell_over_c = ell / chord

    upper_front_angle = eps_deg
    upper_rear_angle = -eps_deg
    lower_front_angle = -eps_deg
    lower_rear_angle = eps_deg

    upper_front_turn = eps_deg - alpha_deg
    upper_rear_turn = -2 * eps_deg

    lower_front_turn = eps_deg + alpha_deg
    lower_rear_turn = -2 * eps_deg

    upper_front = apply_turn(M_inf, 1.0, upper_front_turn, gamma)
    upper_rear = apply_turn(
        upper_front["M"],
        upper_front["p/pinf"],
        upper_rear_turn,
        gamma,
    )

    lower_front = apply_turn(M_inf, 1.0, lower_front_turn, gamma)
    lower_rear = apply_turn(
        lower_front["M"],
        lower_front["p/pinf"],
        lower_rear_turn,
        gamma,
    )

    panels = {
        "upper_front": {
            **upper_front,
            "side": "upper",
            "panel_angle_deg": upper_front_angle,
        },
        "upper_rear": {
            **upper_rear,
            "side": "upper",
            "panel_angle_deg": upper_rear_angle,
        },
        "lower_front": {
            **lower_front,
            "side": "lower",
            "panel_angle_deg": lower_front_angle,
        },
        "lower_rear": {
            **lower_rear,
            "side": "lower",
            "panel_angle_deg": lower_rear_angle,
        },
    }

# Lift and Drag Coefficients

    force_chord_axes = np.array([0.0, 0.0])

    for panel in panels.values():
        Cp = pressure_coefficient(panel["p/pinf"], M_inf, gamma)
        panel["Cp"] = Cp

        n_out = outward_normal(panel["side"], panel["panel_angle_deg"])

        # Pressure force acts inward, opposite outward normal
        force_chord_axes += -Cp * n_out * ell_over_c

    Cx = force_chord_axes[0]
    Cy = force_chord_axes[1]

    # Rotate chord-axis forces into freestream drag/lift axes
    CD = Cx * np.cos(alpha_rad) + Cy * np.sin(alpha_rad)
    CL = -Cx * np.sin(alpha_rad) + Cy * np.cos(alpha_rad)

    return {
        "M_inf": M_inf,
        "alpha_deg": alpha_deg,
        "eps_deg": eps_deg,
        "chord": chord,
        "ell": ell,
        "ell/c": ell_over_c,
        "panels": panels,
        "Cx": Cx,
        "Cy": Cy,
        "CL": CL,
        "CD": CD,
    }


# ============================
# Excution and output
# ============================

if __name__ == "__main__":

    # Change these inputs
    M_inf = 3.0
    alpha_deg = -12.0
    eps_deg = 15.0
    chord = 1.0
    gamma = 1.4

    result = diamond_airfoil(
        M_inf=M_inf,
        alpha_deg=alpha_deg,
        eps_deg=eps_deg,
        chord=chord,
        gamma=gamma,
    )

    print("\n====================================")
    print(" Diamond-Wedge Airfoil Calculation")
    print("====================================")
    print(f"M_inf   = {result['M_inf']:.4f}")
    print(f"alpha   = {result['alpha_deg']:.4f} deg")
    print(f"epsilon = {result['eps_deg']:.4f} deg")
    print(f"chord   = {result['chord']:.4f} m")
    print(f"ell     = {result['ell']:.6f} m")
    print(f"ell/c   = {result['ell/c']:.6f}")

    print("\n--- Panel Results ---")
    print(
        f"{'Panel':<15} {'Turn(deg)':>10} {'Wave':>12} "
        f"{'Beta(deg)':>12} {'M':>12} {'p/pinf':>12} {'Cp':>12}"
    )

    for name, panel in result["panels"].items():
        beta_text = "none" if panel["beta_deg"] is None else f"{panel['beta_deg']:.6f}"

        print(
            f"{name:<15} "
            f"{panel['turn_deg']:>10.6f} "
            f"{panel['wave']:>12} "
            f"{beta_text:>12} "
            f"{panel['M']:>12.6f} "
            f"{panel['p/pinf']:>12.6f} "
            f"{panel['Cp']:>12.6f}"
        )

    print("\n--- Coefficients ---")
    print(f"Cx = {result['Cx']:.6f}")
    print(f"Cy = {result['Cy']:.6f}")
    print(f"CL = {result['CL']:.6f}")
    print(f"CD = {result['CD']:.6f}")