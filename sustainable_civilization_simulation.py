"""
sustainable_civilization_simulation.py
=======================================
Conceptual proof-of-concept simulation.

Theme
-----
If the proposed desert regeneration system (HRS, DGS, Artificial Oasis,
Stepwise Food Transition, Pyramid Circulation Hubs) were implemented,
could it contribute to building a sustainable civilization?

Key premise encoded in this model
-----------------------------------
  - Technology alone is insufficient.
  - Ecological restoration alone does not guarantee sustainable civilization.
  - Human ethical alignment, cooperation, long-term governance, and
    restraint are necessary conditions.
  - Without Artificial Wisdom or an equivalent civilizational wisdom layer,
    advanced ecological systems may be misused, monopolized, or degraded.

IMPORTANT DISCLAIMER
--------------------
All values are hypothetical normalized indicators [0.0, 1.0].
This is NOT a scientific prediction, NOT a policy prescription, and
NOT a validated model of any kind.
Parameter values, weights, and dynamics are conceptual approximations
requiring independent scientific, social, ecological, and governance
validation before any real-world interpretation is made.

Author  : Master (inchacomisho / inchacomusho)
License : CC BY-SA 4.0
Outputs : figures/ directory (relative to script location)
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')          # headless rendering; must precede pyplot import
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

# ================================================================
# Directory setup
# ================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIGURES_DIR = os.path.join(SCRIPT_DIR, 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)

# ================================================================
# Time axis: 2026 through 2100 (75 simulation steps)
# ================================================================
YEARS = np.arange(2026, 2101)   # 75 elements
T = len(YEARS)                  # 75

# ================================================================
# Scenario display metadata
# ================================================================
SCENARIO_LABELS = [
    '1. Baseline Degradation',
    '2. Technology Without Wisdom',
    '3. Partial Transition',
    '4. Nature-Complementary\nSustainable Civilization',
]
SCENARIO_SHORT = [
    'Baseline',
    'Tech w/o Wisdom',
    'Partial Transition',
    'Nature-Complementary',
]
COLORS  = ['#555555', '#d62728', '#ff8c00', '#2ca02c']
STYLES  = ['-',       '--',       '-.',       '-']
WIDTHS  = [1.5,        1.5,        1.5,       2.5]

FOOTER = ('All values: hypothetical normalized indicators [0.0, 1.0]. '
          'Not a prediction or policy prescription.')

# ================================================================
# Utility helpers
# ================================================================
def clamp(x: float) -> float:
    """Clamp value to [0.0, 1.0]."""
    return float(np.clip(x, 0.0, 1.0))


def sustainability_index(s: dict) -> float:
    """
    Civilization Sustainability Index (CSI) -- hypothetical formula.

    CSI =   ecological_avg * 0.35
          + food_water_avg * 0.20
          + infrastructure * 0.15
          + ethical_alignment * 0.15
          + social_cooperation * 0.10
          + long_term_governance * 0.05
          - overexploitation * 0.20

    Design intent:
      - Ecological recovery is necessary (35%) but not sufficient alone.
      - Wisdom / ethics / governance contribute 30% combined (positive).
      - Overexploitation subtracts 20%: growth without restraint significantly
        reduces the index even when ecological variables appear healthy.
      - This encodes the premise: technology and ecology are conditions;
        civilizational quality is determined by human thought and governance.

    NOTE: Weights are conceptual approximations, not empirically calibrated.
    """
    eco_avg = (s['soil'] + s['micro'] + s['water']
               + s['veg'] + s['carb']) / 5.0
    fw_avg  = (s['food'] + s['water']) / 2.0
    csi = (eco_avg          * 0.35
           + fw_avg         * 0.20
           + s['infra']     * 0.15
           + s['ethics']    * 0.15
           + s['soc_coop']  * 0.10
           + s['gov']       * 0.05
           - s['overex']    * 0.20)
    return clamp(csi)


def init() -> dict:
    """
    Shared starting state (year 2026) for all scenarios.
    Represents a partially degraded dryland region with low social
    and governance capacity.  All values normalized [0.0, 1.0].
    These initial values are hypothetical.
    """
    return {
        'soil':     0.35,   # soil health index
        'micro':    0.30,   # microbial recovery index
        'water':    0.28,   # water stability index
        'veg':      0.22,   # vegetation cover index
        'carb':     0.25,   # carbon fixation capacity
        'food':     0.38,   # food security index
        'infra':    0.40,   # infrastructure resilience
        'soc_coop': 0.30,   # social cooperation
        'ethics':   0.20,   # ethical alignment
        'gov':      0.22,   # long-term governance capacity
        'overex':   0.65,   # overexploitation pressure (higher = worse)
    }


# ================================================================
# SCENARIO 1: Baseline Degradation
# ================================================================
def run_baseline() -> dict:
    """
    No intervention. Ecological degradation continues unabated.
    Social, ethical, and governance capacities stagnate.
    Overexploitation pressure increases over time.
    """
    np.random.seed(1001)
    s = init()
    h = {k: [] for k in s}
    h['csi'] = []

    def n(): return np.random.normal(0.0, 0.002)

    for _ in range(T):
        # Ecological decline
        s['soil']    = clamp(s['soil']    - 0.003 + n())
        s['micro']   = clamp(s['micro']   - 0.004 + n())
        s['water']   = clamp(s['water']   - 0.003 + n())
        s['veg']     = clamp(s['veg']     - 0.002 + n())
        s['carb']    = clamp(s['carb']    - 0.003 + n())
        s['food']    = clamp(s['food']    - 0.003 + n())
        s['infra']   = clamp(s['infra']   - 0.001 + n())
        # Social stagnation
        s['soc_coop'] = clamp(s['soc_coop'] + n() * 0.5)
        s['ethics']   = clamp(s['ethics']   + n() * 0.5)
        s['gov']      = clamp(s['gov']      + n() * 0.5)
        # Overexploitation worsens
        s['overex']   = clamp(s['overex']   + 0.002 + n())
        for k in s:
            h[k].append(s[k])
        h['csi'].append(sustainability_index(s))

    return {k: np.array(v) for k, v in h.items()}


# ================================================================
# SCENARIO 2: Technology Without Wisdom
# ================================================================
def run_tech_no_wisdom() -> dict:
    """
    HRS / DGS and related technologies are deployed aggressively.
    Strong early ecological gains result from the rollout.

    However, human wisdom, ethics, and governance stagnate throughout.
    Systems are monopolized, over-extracted, and underfunded after
    initial deployment pressure recedes (~year 2056, t=30).
    Overexploitation pressure rebounds sharply.

    Core message encoded:
      Technical excellence cannot substitute for ethical alignment
      and long-term governance. Advanced systems may be misused without
      a civilizational wisdom layer.
    """
    np.random.seed(1002)
    s = init()
    h = {k: [] for k in s}
    h['csi'] = []

    def n(): return np.random.normal(0.0, 0.002)

    for t in range(T):
        # -----------------------------------------------------------
        # Technology deployment phases (ecological delta per step)
        # -----------------------------------------------------------
        # Phase A (t < 15):  aggressive initial rollout
        # Phase B (15 <= t < 30): slowing gains, diminishing returns
        # Phase C (t >= 30): mismanagement and overuse erode gains
        if t < 15:
            eco_d = +0.009
        elif t < 30:
            eco_d = +0.003
        else:
            eco_d = -0.005    # degradation from overuse and neglect

        s['soil']    = clamp(s['soil']    + eco_d * 0.80 + n())
        s['micro']   = clamp(s['micro']   + eco_d * 1.00 + n())
        s['water']   = clamp(s['water']   + eco_d * 0.70 + n())
        s['veg']     = clamp(s['veg']     + eco_d * 1.00 + n())
        s['carb']    = clamp(s['carb']    + eco_d * 0.65 + n())
        s['food']    = clamp(s['food']    + eco_d * 0.50 + n())

        # Infrastructure: rises during tech rollout, deteriorates later
        if t < 30:
            s['infra'] = clamp(s['infra'] + 0.005 + n())
        else:
            s['infra'] = clamp(s['infra'] - 0.004 + n())

        # Wisdom stagnates -- key structural constraint in this model
        s['soc_coop'] = clamp(s['soc_coop'] + n() * 0.4)
        s['ethics']   = clamp(s['ethics']   + n() * 0.4)
        s['gov']      = clamp(s['gov']      + n() * 0.4)

        # Overexploitation: initially reduced by tech efficiency,
        # then rebounds sharply as short-term profit motives dominate
        if t < 20:
            s['overex'] = clamp(s['overex'] - 0.007 + n())
        else:
            s['overex'] = clamp(s['overex'] + 0.009 + n())

        for k in s:
            h[k].append(s[k])
        h['csi'].append(sustainability_index(s))

    return {k: np.array(v) for k, v in h.items()}


# ================================================================
# SCENARIO 3: Partial Transition
# ================================================================
def run_partial() -> dict:
    """
    Technology deployed at moderate pace.
    Some regions develop long-term cooperation and ethical frameworks.
    Moderate and steady improvement overall.
    No collapse, but no breakthrough to high sustainability either.
    """
    np.random.seed(1003)
    s = init()
    h = {k: [] for k in s}
    h['csi'] = []

    def n(): return np.random.normal(0.0, 0.002)

    for _ in range(T):
        eco_d = 0.003
        wis_d = 0.002

        s['soil']    = clamp(s['soil']    + eco_d * 0.75 + n())
        s['micro']   = clamp(s['micro']   + eco_d * 0.85 + n())
        s['water']   = clamp(s['water']   + eco_d * 0.65 + n())
        s['veg']     = clamp(s['veg']     + eco_d * 0.90 + n())
        s['carb']    = clamp(s['carb']    + eco_d * 0.55 + n())
        s['food']    = clamp(s['food']    + eco_d * 0.45 + n())
        s['infra']   = clamp(s['infra']   + 0.002        + n())

        # Partial wisdom growth in participating regions
        s['soc_coop'] = clamp(s['soc_coop'] + wis_d * 0.70 + n())
        s['ethics']   = clamp(s['ethics']   + wis_d * 0.55 + n())
        s['gov']      = clamp(s['gov']      + wis_d * 0.45 + n())

        # Overexploitation slowly reduces
        s['overex']   = clamp(s['overex']   - 0.003 + n())

        for k in s:
            h[k].append(s[k])
        h['csi'].append(sustainability_index(s))

    return {k: np.array(v) for k, v in h.items()}


# ================================================================
# SCENARIO 4: Nature-Complementary Sustainable Civilization
# ================================================================
def run_nature_complementary() -> dict:
    """
    HRS, DGS, water circulation, stepwise food relay, artificial oasis,
    and pyramid circulation hubs deployed systematically.

    Simultaneously, human thought transitions toward nature-complementary
    ethics, long-term governance, and voluntary restraint.
    Artificial Wisdom (or equivalent wisdom layer) supports alignment
    between human decisions and natural law.

    Technology and wisdom co-evolve. Positive feedback loops gradually
    reinforce both ecological and social recovery over time.

    Core message encoded:
      Sustainable civilization requires ecological restoration AND
      civilizational wisdom to develop in parallel. Neither alone
      is sufficient. The combination produces the highest long-term
      sustainability, but also takes the longest to fully manifest.
    """
    np.random.seed(1004)
    s = init()
    h = {k: [] for k in s}
    h['csi'] = []

    def n(): return np.random.normal(0.0, 0.002)

    for t in range(T):
        # Feedback acceleration: as systems mature and wisdom deepens,
        # reinforcing loops make each unit of input more effective.
        # Growth factor rises from 1.0 (year 2026) to 1.6 (year 2076+).
        grow   = 1.0 + 0.6 * min(t / 50.0, 1.0)
        eco_d  = 0.005 * grow
        wis_d  = 0.004 * grow

        s['soil']    = clamp(s['soil']    + eco_d * 0.90 + n())
        s['micro']   = clamp(s['micro']   + eco_d * 1.00 + n())
        s['water']   = clamp(s['water']   + eco_d * 0.85 + n())
        s['veg']     = clamp(s['veg']     + eco_d * 1.00 + n())
        s['carb']    = clamp(s['carb']    + eco_d * 0.80 + n())
        s['food']    = clamp(s['food']    + eco_d * 0.60 + n())
        s['infra']   = clamp(s['infra']   + 0.007        + n())

        # Strong and growing social wisdom
        # (Artificial Wisdom framework supports ethical calibration)
        s['soc_coop'] = clamp(s['soc_coop'] + wis_d * 1.00 + n())
        s['ethics']   = clamp(s['ethics']   + wis_d * 1.00 + n())
        s['gov']      = clamp(s['gov']      + wis_d * 0.85 + n())

        # Overexploitation declines as ethical restraint,
        # circular economy principles, and long-term governance deepen
        s['overex']   = clamp(s['overex']   - 0.008 + n())

        for k in s:
            h[k].append(s[k])
        h['csi'].append(sustainability_index(s))

    return {k: np.array(v) for k, v in h.items()}


# ================================================================
# Run all scenarios
# ================================================================
print('Running scenarios ...')
R = [
    run_baseline(),
    run_tech_no_wisdom(),
    run_partial(),
    run_nature_complementary(),
]
print('All scenarios complete.\n')


# ================================================================
# FIGURE 1: Civilization Sustainability Index
# ================================================================
fig, ax = plt.subplots(figsize=(11, 6))
fig.suptitle('Civilization Sustainability Index — Four Scenarios (2026–2100)',
             fontsize=13, fontweight='bold', y=0.98)

for r, label, color, ls, lw in zip(R, SCENARIO_LABELS, COLORS, STYLES, WIDTHS):
    ax.plot(YEARS, r['csi'], color=color, linestyle=ls, linewidth=lw, label=label)

ax.set_xlim(YEARS[0], YEARS[-1])
ax.set_ylim(0, 1.0)
ax.set_xlabel('Year', fontsize=11)
ax.set_ylabel('Civilization Sustainability Index [0–1]', fontsize=11)
ax.legend(loc='upper left', fontsize=9.5, framealpha=0.9)
ax.grid(True, alpha=0.3)

# Key message annotation
ax.annotate(
    'Conceptual observation (hypothetical model):\n'
    '"Technology Without Wisdom" peaks then declines sharply (red dashed).\n'
    'Co-development of wisdom and technology may support higher sustainability.',
    xy=(2062, 0.09), fontsize=8.5, color='#333333',
    bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow', alpha=0.85))

fig.text(0.5, 0.01, FOOTER, ha='center', fontsize=8, color='gray', style='italic')
plt.tight_layout(rect=[0, 0.03, 1, 1])
out = os.path.join(FIGURES_DIR, 'sustainable_civilization_index.png')
plt.savefig(out, dpi=150, bbox_inches='tight')
plt.close()
print(f'Saved: {out}')


# ================================================================
# FIGURE 2: Ecological Recovery Components
# ================================================================
eco_keys   = ['soil', 'micro', 'water', 'veg', 'carb', 'food']
eco_titles = ['Soil Health', 'Microbial Recovery', 'Water Stability',
              'Vegetation Cover', 'Carbon Fixation Capacity', 'Food Security']

fig, axes = plt.subplots(2, 3, figsize=(15, 8), sharex=True, sharey=True)
fig.suptitle('Ecological Recovery Components — Four Scenarios (2026–2100)',
             fontsize=13, fontweight='bold')

for idx, (key, title) in enumerate(zip(eco_keys, eco_titles)):
    ax = axes[idx // 3][idx % 3]
    for r, label, color, ls, lw in zip(R, SCENARIO_LABELS, COLORS, STYLES, WIDTHS):
        ax.plot(YEARS, r[key], color=color, linestyle=ls, linewidth=lw,
                label=label)
    ax.set_title(title, fontsize=10, fontweight='bold')
    ax.set_ylim(0, 1.0)
    ax.grid(True, alpha=0.3)
    ax.set_ylabel('Index [0–1]', fontsize=8)
    if idx >= 3:
        ax.set_xlabel('Year', fontsize=9)

# Shared legend below figure
handles = [mlines.Line2D([], [], color=c, linestyle=ls, linewidth=lw)
           for c, ls, lw in zip(COLORS, STYLES, WIDTHS)]
fig.legend(handles, SCENARIO_LABELS, loc='lower center',
           ncol=2, fontsize=9, bbox_to_anchor=(0.5, -0.06))
fig.text(0.5, -0.01, FOOTER, ha='center', fontsize=8, color='gray', style='italic')
plt.tight_layout(rect=[0, 0.08, 1, 1])
out = os.path.join(FIGURES_DIR, 'ecological_recovery_components.png')
plt.savefig(out, dpi=150, bbox_inches='tight')
plt.close()
print(f'Saved: {out}')


# ================================================================
# FIGURE 3: Social Wisdom Components
# ================================================================
soc_keys   = ['soc_coop', 'ethics', 'gov', 'overex']
soc_titles = ['Social Cooperation', 'Ethical Alignment',
              'Long-Term Governance', 'Overexploitation Pressure']
soc_notes  = ['higher = better', 'higher = better',
              'higher = better', 'higher = WORSE (more pressure)']

fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True)
fig.suptitle('Social Wisdom and Governance Components — Four Scenarios (2026–2100)',
             fontsize=13, fontweight='bold')

for idx, (key, title, note) in enumerate(zip(soc_keys, soc_titles, soc_notes)):
    ax = axes[idx // 2][idx % 2]
    for r, label, color, ls, lw in zip(R, SCENARIO_LABELS, COLORS, STYLES, WIDTHS):
        ax.plot(YEARS, r[key], color=color, linestyle=ls, linewidth=lw,
                label=label)
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.set_ylim(0, 1.0)
    ax.grid(True, alpha=0.3)
    ax.set_ylabel('Index [0–1]', fontsize=9)
    ax.annotate(f'({note})', xy=(2028, 0.88), fontsize=8,
                color='#d62728' if 'WORSE' in note else '#555555')
    if idx >= 2:
        ax.set_xlabel('Year', fontsize=9)

handles = [mlines.Line2D([], [], color=c, linestyle=ls, linewidth=lw)
           for c, ls, lw in zip(COLORS, STYLES, WIDTHS)]
fig.legend(handles, SCENARIO_LABELS, loc='lower center',
           ncol=2, fontsize=9, bbox_to_anchor=(0.5, -0.06))
fig.text(0.5, -0.01, FOOTER, ha='center', fontsize=8, color='gray', style='italic')
plt.tight_layout(rect=[0, 0.08, 1, 1])
out = os.path.join(FIGURES_DIR, 'social_wisdom_components.png')
plt.savefig(out, dpi=150, bbox_inches='tight')
plt.close()
print(f'Saved: {out}')


# ================================================================
# FIGURE 4: Technology vs Wisdom Gap
# Compares Scenario 2 (Tech Without Wisdom) and Scenario 4 (Nature-Complementary)
# to illustrate how wisdom co-development determines long-term outcomes.
# ================================================================
gap_keys   = ['csi',      'ethics',            'soc_coop',             'overex']
gap_titles = ['Civilization Sustainability Index',
              'Ethical Alignment',
              'Social Cooperation',
              'Overexploitation Pressure']
gap_notes  = ['Gap = the wisdom contribution to civilizational sustainability',
              'Stagnant ethics vs. steadily growing ethical alignment',
              'Stagnant cooperation vs. growing social cooperation',
              'Rebounding overexploitation vs. steadily declining pressure']

fig, axes = plt.subplots(2, 2, figsize=(13, 8), sharex=True)
fig.suptitle(
    'Technology Without Wisdom vs. Nature-Complementary Civilization\n'
    'The Wisdom Gap — 2026–2100  (Scenarios 2 and 4 only)',
    fontsize=12, fontweight='bold')

for idx, (key, title, note) in enumerate(zip(gap_keys, gap_titles, gap_notes)):
    ax = axes[idx // 2][idx % 2]
    y2 = R[1][key]    # Scenario 2: Tech Without Wisdom
    y4 = R[3][key]    # Scenario 4: Nature-Complementary

    ax.plot(YEARS, y2, color=COLORS[1], linestyle=STYLES[1],
            linewidth=1.8, label='2. Technology Without Wisdom')
    ax.plot(YEARS, y4, color=COLORS[3], linestyle=STYLES[3],
            linewidth=2.5, label='4. Nature-Complementary')

    # Shade the gap to make the divergence visually prominent
    ax.fill_between(YEARS, y2, y4, where=(y4 >= y2),
                    alpha=0.14, color='#2ca02c',
                    label='Nature-Complementary advantage')
    ax.fill_between(YEARS, y2, y4, where=(y4 < y2),
                    alpha=0.14, color='#d62728',
                    label='Tech-Without-Wisdom advantage')

    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.set_ylim(0, 1.0)
    ax.grid(True, alpha=0.3)
    ax.set_ylabel('Index [0–1]', fontsize=9)
    ax.annotate(note, xy=(2028, 0.02), fontsize=7.8,
                color='#555555', style='italic')
    if idx >= 2:
        ax.set_xlabel('Year', fontsize=9)
    if idx == 0:
        ax.legend(fontsize=8, loc='upper left', framealpha=0.9)

fig.text(0.5, 0.01, FOOTER, ha='center', fontsize=8, color='gray', style='italic')
plt.tight_layout(rect=[0, 0.03, 1, 1])
out = os.path.join(FIGURES_DIR, 'technology_vs_wisdom_gap.png')
plt.savefig(out, dpi=150, bbox_inches='tight')
plt.close()
print(f'Saved: {out}')


# ================================================================
# Console output: Year 2100 summary table
# ================================================================
VAR_DISPLAY = [
    ('soil',     'Soil Health'),
    ('micro',    'Microbial Recovery'),
    ('water',    'Water Stability'),
    ('veg',      'Vegetation Cover'),
    ('carb',     'Carbon Fixation Capacity'),
    ('food',     'Food Security'),
    ('infra',    'Infrastructure Resilience'),
    ('soc_coop', 'Social Cooperation'),
    ('ethics',   'Ethical Alignment'),
    ('gov',      'Long-Term Governance'),
    ('overex',   'Overexploitation Pressure (*)'),
    ('csi',      'Civilization Sustainability Index'),
]

W = 34   # column width for variable name
C = 12   # column width for each scenario value
SEP = '=' * (W + C * 4)

print(SEP)
print(' SIMULATION RESULTS: YEAR 2100')
print(' Hypothetical normalized indicators [0.0, 1.0].')
print(' NOT scientifically validated predictions.')
print(SEP)
header = f"{'Variable':<{W}}" + ''.join(f'{s:>{C}}' for s in SCENARIO_SHORT)
print(header)
print('-' * (W + C * 4))
for key, display in VAR_DISPLAY:
    vals = ''.join(f'{r[key][-1]:>{C}.3f}' for r in R)
    print(f'{display:<{W}}{vals}')
print(SEP)
print(' (*) Overexploitation Pressure: higher = worse (more pressure).')
print('     All other variables: higher = better.')
print()
print(' CONCEPTUAL OBSERVATION (hypothetical model):')
print('   In this model, "Technology Without Wisdom" and "Baseline Degradation"')
print('   end near the same low CSI range by 2100, despite early gains in')
print('   Scenario 2. This conceptually illustrates that ecological technologies')
print('   may lose sustainability when combined with overexploitation, weak')
print('   governance, and insufficient ethical alignment. It does not prove')
print('   that technological systems inevitably fail. Co-development of')
print('   ecological restoration and civilizational wisdom is the pathway')
print('   that produces higher sustainability in this hypothetical model.')
print(SEP)
