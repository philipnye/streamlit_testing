from st_aggrid import StAggridTheme

from streamlit_testing.config.colours import COLOURS

# AG Grid height calculation constants
# NB: These are best-guess values and aren't exactly that used by the AG Grid component
AG_GRID_HEADER_HEIGHT = 50
AG_GRID_ROW_HEIGHT = 50
AG_GRID_MIN_HEIGHT = 200
AG_GRID_MAX_HEIGHT = 800

ag_grid_theme = StAggridTheme(base="quartz").withParams(
    fontSize=14,
    fontFamily="Open Sans, sans-serif",
    headerFontFamily="Open Sans, sans-serif",
    headerFontWeight="normal",
    rowBorder=False,
    textColor=COLOURS["dark_grey"],
    headerBackgroundColor=COLOURS["grey_lighter_80pct"],
)
