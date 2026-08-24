"""
Synthwave Horizon — identidade visual do portfólio.

Uso:
    import estilo
    estilo.aplicar()
    fig, ax = estilo.figura('Título do gráfico', 'rótulo do eixo y')

A paleta e a regra 60/30/10 estão no manual de padronização.
Mapeamento de segmentos segue a narrativa, não a ordem alfabética:
    Banco   -> ciano  (métrica normal: o controle imóvel)
    Fintech -> rosa   (série de alto contraste: o achado)
    IP      -> laranja (ponto de atenção: o segmento instável)
"""

import matplotlib as mpl
import matplotlib.pyplot as plt

# ---------------------------------------------------------------- paleta
FUNDO = '#1A0B2E'        # Deep Violet Space  — 60%
CARTAO = '#2A144E'       # Deep Imperial Purple
CIANO = '#30C0B7'        # Synthwave Cyan     — 30%
ROSA = '#EE227D'         # Neon Pink          — 30%
LARANJA = '#FA8057'      # Sunset Orange      — 10%
AMARELO = '#FAD009'      # Yellow Accent      — 10%
CREME = '#FEFECC'        # Pastel Cream       — títulos, eixos
LAVANDA = '#BB99FF'      # Soft Lavender      — apoio
INDIGO = '#4B0082'       # Indigo             — grade

# Aceita os nomes nos dois idiomas: o notebook roda em inglês, mas a fonte
# (Banco Central do Brasil) nomeia os segmentos em português.
CORES_SEGMENTO = {
    'Banco': CIANO,               'Bank': CIANO,
    'Fintech': ROSA,
    'Instituição de pagamento': LARANJA,
    'Payment institution': LARANJA,
}

CICLO = [CIANO, ROSA, LARANJA, AMARELO, LAVANDA]


def aplicar():
    """Aplica o tema aos rcParams. Chamar uma vez, no início do notebook."""
    mpl.rcParams.update({
        'figure.facecolor': FUNDO,
        'figure.edgecolor': FUNDO,
        'savefig.facecolor': FUNDO,
        'savefig.edgecolor': FUNDO,
        'savefig.dpi': 150,
        'savefig.bbox': 'tight',

        'axes.facecolor': FUNDO,
        'axes.edgecolor': INDIGO,
        'axes.labelcolor': LAVANDA,
        'axes.titlecolor': CREME,
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
        'axes.prop_cycle': mpl.cycler(color=CICLO),

        'grid.color': INDIGO,
        'grid.alpha': 0.55,
        'grid.linewidth': 0.7,

        'text.color': CREME,
        'xtick.color': LAVANDA,
        'ytick.color': LAVANDA,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,

        'legend.facecolor': CARTAO,
        'legend.edgecolor': INDIGO,
        'legend.labelcolor': CREME,
        'legend.framealpha': 0.95,
        'legend.fontsize': 9,
        'legend.borderpad': 0.8,

        'lines.linewidth': 2.0,
        'lines.solid_capstyle': 'round',

        'figure.figsize': (11, 5),
        'font.size': 10,
    })


def figura(titulo='', ylabel='', subtitulo='', figsize=None):
    """Cria fig/ax já titulados. Devolve (fig, ax)."""
    fig, ax = plt.subplots(figsize=figsize or mpl.rcParams['figure.figsize'])
    if titulo:
        ax.set_title(titulo, loc='left')
    if subtitulo:
        ax.text(0, 1.015, subtitulo, transform=ax.transAxes,
                color=LAVANDA, fontsize=9.5, va='bottom')
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.set_xlabel('')
    return fig, ax


def cores(colunas):
    """Cores na ordem das colunas passadas, respeitando o mapa de segmentos.

    Avisa em vez de silenciar: cor de fallback repetida deixa duas séries
    indistinguíveis, que é pior do que um erro visível.
    """
    faltando = [c for c in colunas if c not in CORES_SEGMENTO]
    if faltando:
        import warnings
        warnings.warn(f'sem cor definida para {faltando} — usando fallback', stacklevel=2)
    return [CORES_SEGMENTO.get(c, LAVANDA) for c in colunas]


def finalizar(ax, fonte_texto='', legenda=True):
    """Acabamento pós-plot.

    Precisa vir DEPOIS de .plot(): o pandas reescreve o rótulo do eixo x com o
    nome do índice, sobrescrevendo o que figura() tinha limpado.
    """
    ax.set_xlabel('')
    if legenda and ax.get_legend() is not None:
        ax.legend(title='')
    if fonte_texto:
        fonte(ax, fonte_texto)
    return ax


def marcar(ax, x, texto, cor=AMARELO):
    """Linha vertical de anotação — usar para cortes de versão e quebras."""
    ax.axvline(x, color=cor, linestyle='--', linewidth=1.2, alpha=0.8)
    ax.text(x, ax.get_ylim()[1], f' {texto}', color=cor,
            fontsize=8.5, va='top', ha='left')


def fonte(ax, texto):
    """Rodapé de atribuição, canto inferior esquerdo."""
    ax.annotate(texto, xy=(0, -0.13), xycoords='axes fraction',
                color=LAVANDA, fontsize=8, alpha=0.85)
