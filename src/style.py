"""
Synthwave Horizon — the portfolio's visual identity.

Usage:
    import style
    style.apply()
    fig, ax = style.figure('Chart title', 'y axis label')

The palette and the 60/30/10 rule come from the standardisation manual.
Segment mapping follows the narrative, not alphabetical order:
    Bank    -> cyan   (the ordinary metric: the control that does not move)
    Fintech -> pink   (the high-contrast series: the finding)
    PI      -> orange (the point of concern: the unstable segment)
"""

import matplotlib as mpl
import matplotlib.pyplot as plt

# ---------------------------------------------------------------- palette
BACKGROUND = '#1A0B2E'   # Deep Violet Space  — 60%
CARD = '#2A144E'         # Deep Imperial Purple
CYAN = '#30C0B7'         # Synthwave Cyan     — 30%
PINK = '#EE227D'         # Neon Pink          — 30%
ORANGE = '#FA8057'       # Sunset Orange      — 10%
YELLOW = '#FAD009'       # Yellow Accent      — 10%
CREAM = '#FEFECC'        # Pastel Cream       — titles, axes
LAVENDER = '#BB99FF'     # Soft Lavender      — support
INDIGO = '#4B0082'       # Indigo             — grid

# Accepts the names in both languages: the notebook reads in English, but the
# source (Banco Central do Brasil) names the segments in Portuguese.
SEGMENT_COLORS = {
    'Banco': CYAN,                'Bank': CYAN,
    'Fintech': PINK,
    'Instituição de pagamento': ORANGE,
    'Payment institution': ORANGE,
}

CYCLE = [CYAN, PINK, ORANGE, YELLOW, LAVENDER]


def apply():
    """Apply the theme to rcParams. Call once, at the top of the notebook."""
    mpl.rcParams.update({
        'figure.facecolor': BACKGROUND,
        'figure.edgecolor': BACKGROUND,
        'savefig.facecolor': BACKGROUND,
        'savefig.edgecolor': BACKGROUND,
        'savefig.dpi': 150,
        'savefig.bbox': 'tight',

        'axes.facecolor': BACKGROUND,
        'axes.edgecolor': INDIGO,
        'axes.labelcolor': LAVENDER,
        'axes.titlecolor': CREAM,
        'axes.titlesize': 13,
        'axes.titleweight': 'bold',
        'axes.titlepad': 26,
        'axes.labelsize': 10,
        'axes.labelpad': 8,
        'axes.linewidth': 1.0,
        'axes.grid': True,
        'axes.axisbelow': True,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.prop_cycle': mpl.cycler(color=CYCLE),

        'grid.color': INDIGO,
        'grid.alpha': 0.55,
        'grid.linewidth': 0.7,

        'text.color': CREAM,
        'xtick.color': LAVENDER,
        'ytick.color': LAVENDER,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,

        'legend.facecolor': CARD,
        'legend.edgecolor': INDIGO,
        'legend.labelcolor': CREAM,
        'legend.framealpha': 0.95,
        'legend.fontsize': 9,
        'legend.borderpad': 0.8,

        'lines.linewidth': 2.0,
        'lines.solid_capstyle': 'round',

        'figure.figsize': (11, 5),
        'font.size': 10,
    })


def figure(title='', ylabel='', subtitle='', figsize=None):
    """Create a titled fig/ax pair. Returns (fig, ax)."""
    fig, ax = plt.subplots(figsize=figsize or mpl.rcParams['figure.figsize'])
    if title:
        ax.set_title(title, loc='left')
    if subtitle:
        ax.text(0, 1.015, subtitle, transform=ax.transAxes,
                color=LAVENDER, fontsize=9.5, va='bottom')
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.set_xlabel('')
    return fig, ax


def colors(columns):
    """Colours in the order of the given columns, honouring the segment map.

    Warns instead of staying silent: a repeated fallback colour makes two
    series indistinguishable, which is worse than a visible error.
    """
    missing = [c for c in columns if c not in SEGMENT_COLORS]
    if missing:
        import warnings
        warnings.warn(f'no colour defined for {missing} — using fallback', stacklevel=2)
    return [SEGMENT_COLORS.get(c, LAVENDER) for c in columns]


def finalize(ax, source_text='', legend=True):
    """Post-plot finishing touches.

    Must run AFTER .plot(): pandas rewrites the x axis label with the index
    name, overwriting what figure() had cleared.
    """
    ax.set_xlabel('')
    if legend and ax.get_legend() is not None:
        ax.legend(title='')
    if source_text:
        source(ax, source_text)
    return ax


def mark(ax, x, text, color=YELLOW):
    """Vertical annotation line — use for version cut-offs and breaks."""
    ax.axvline(x, color=color, linestyle='--', linewidth=1.2, alpha=0.8)
    ax.text(x, ax.get_ylim()[1], f' {text}', color=color,
            fontsize=8.5, va='top', ha='left')


def source(ax, text):
    """Attribution footer, bottom left corner."""
    ax.annotate(text, xy=(0, -0.13), xycoords='axes fraction',
                color=LAVENDER, fontsize=8, alpha=0.85)
