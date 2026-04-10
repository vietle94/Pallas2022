import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import string
# %%
# Briggs 1969
def plume_rise(F, u, x):
    """Calculate the plume rise using the Briggs 1969 formula.

    Parameters
    ----------
    F : float
        Buoyancy flux (m^4/s^3)
    u : float
        Wind speed (m/s)
    x : float
        Downwind distance (m)

    Returns
    -------
    float
        Plume rise (m)
    """
    return 1.6 * (F / u) ** (1 / 3) * x ** (2 / 3)


def buoyancy_flux(Ts, Ta, vs, d):
    """Calculate the buoyancy flux.

    Parameters
    ----------
    Ts : float
        Source temperature (K)
    Ta : float
        Ambient temperature (K)
    vs : float
        Source velocity (m/s)
    d : float
        Source diameter (m)

    Returns
    -------
    float
        Buoyancy flux (m^4/s^3)
    """
    g = 9.81  # m/s^2
    return g * (Ts - Ta) / Ts * vs * (d / 2) ** 2


def Gaussian_plume_sigma_y(x):
    """Calculate the horizontal dispersion parameter sigma_y for a Gaussian plume.

    Parameters
    ----------
    x : float
        Downwind distance (m)

    Returns
    -------
    float
        Horizontal dispersion parameter sigma_y (m)
    """
    Iy = -1.104
    Jy = 0.9878
    Ky = -0.0076
    return np.exp(Iy + Jy*np.log(x) + Ky*(np.log(x))**2)

def Gaussian_plume_sigma_z(x):
    """Calculate the vertical dispersion parameter sigma_z for a Gaussian plume.

    Parameters
    ----------
    x : float
        Downwind distance (m)

    Returns
    -------
    float
        Vertical dispersion parameter sigma_z (m)
    """
    Iz = 4.679
    Jz = -1.7172
    Kz = 0.2770
    return np.exp(Iz + Jz*np.log(x) + Kz*(np.log(x))**2)


def Gaussian_plume_concentration(Q, u, sigma_y, sigma_z, y, z, h):
    """Calculate the concentration of a Gaussian plume.

    Parameters
    ----------
    Q : float
        Emission rate (g/s)
    u : float
        Wind speed (m/s)
    sigma_y : float
        Horizontal dispersion parameter (m)
    sigma_z : float
        Vertical dispersion parameter (m)
    y : float
        Crosswind distance (m)
    z : float
        Height above ground (m)

    Returns
    -------
    float
        Concentration (g/m^3)
    """
    return Q / (2 * np.pi * u * sigma_y * sigma_z) * \
        np.exp(-y**2 / (2 * sigma_y**2)) * \
            (np.exp(-(z - h)**2 / (2 * sigma_z**2)) + np.exp(-(z + h)**2 / (2 * sigma_z**2)))

# %%
x = np.arange(1, 1e3, 10)
z = np.arange(1, 1e3, 10)
X, Z = np.meshgrid(x, z)
Q = 1
u = 1
Ts = 600
Ta = 280
vs = 20
d = 0.05
F = buoyancy_flux(Ts, Ta, vs, d)
plume_rise_values = plume_rise(F, u, X)
sigma_y_values = Gaussian_plume_sigma_y(X)
sigma_z_values = Gaussian_plume_sigma_z(X)

# %%
concentration_values = Gaussian_plume_concentration(Q, u, sigma_y_values, sigma_z_values,
                                                    0, Z, plume_rise_values)
fig, ax = plt.subplots(1, 3, sharex=True, sharey=True,
        figsize=(9, 3), constrained_layout=True)
p = ax[0].pcolormesh(X, Z, concentration_values, shading='auto',
                 norm=LogNorm(vmin=1e-6, vmax=1e-3))
ax[0].set_xlim(20, None)
ax[0].set_xlabel('Downwind distance (m)')
ax[0].set_ylabel('Height above ground (m)')

concentration_values = Gaussian_plume_concentration(Q, u, sigma_y_values, sigma_z_values,
                                                    50, Z, plume_rise_values)
p = ax[1].pcolormesh(X, Z, concentration_values, shading='auto',
                 norm=LogNorm(vmin=1e-6, vmax=1e-3))
ax[1].set_xlim(20, None)
ax[1].set_xlabel('Downwind distance (m)')

concentration_values = Gaussian_plume_concentration(Q, u, sigma_y_values, sigma_z_values,
                                                    100, Z, plume_rise_values)
p = ax[2].pcolormesh(X, Z, concentration_values, shading='auto',
                 norm=LogNorm(vmin=1e-6, vmax=1e-3))
ax[2].set_xlim(20, None)
ax[2].set_xlabel('Downwind distance (m)')

fig.colorbar(p, ax=ax, label='Relative concentration \n(normalized to source)')

for n, ax_ in enumerate(ax.flatten()):
    ax_.grid()
    ax_.text(
        -0.0,
        1.05,
        "(" + string.ascii_lowercase[n] + ")",
        transform=ax_.transAxes,
        size=12,
    )
fig.savefig(fr"C:\Users\le\OneDrive - Ilmatieteen laitos\PaCE_2022\ESSD special issue\Viet_et_al_2025\Ver2\Editor_reply/gaussian_plume_{u}.png",
            dpi=300, bbox_inches='tight')
