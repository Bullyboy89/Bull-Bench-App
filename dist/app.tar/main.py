import flet as ft
import statistics
import math


# ============================================================
# 1RM-FORMELER
# ============================================================

def epley(weight: float, reps: int) -> float:
    return weight * (1 + reps / 30)


def brzycki(weight: float, reps: int) -> float:
    if reps >= 37:
        return weight
    return weight * (36 / (37 - reps))


def lombardi(weight: float, reps: int) -> float:
    return weight * (reps ** 0.10)


def calculate_median_1rm(weight: float, reps: int) -> float:
    results = [
        epley(weight, reps),
        brzycki(weight, reps),
        lombardi(weight, reps),
    ]
    return statistics.median(results)


def get_weight_for_reps(one_rm: float, reps: int) -> float:
    """
    Räknar baklänges med samma medianmodell som används
    för att uppskatta 1RM.
    """
    if reps < 1:
        raise ValueError("Reps måste vara minst 1.")

    multipliers = [
        epley(1.0, reps),
        brzycki(1.0, reps),
        lombardi(1.0, reps),
    ]

    median_multiplier = statistics.median(multipliers)

    if median_multiplier <= 0:
        raise ValueError("Ogiltig multiplikator.")

    return one_rm / median_multiplier


def round_to_half(value: float) -> float:
    """
    Avrundar till närmaste 0,5.
    """
    return math.floor(value * 2 + 0.5) / 2


# ============================================================
# APP
# ============================================================

async def main(page: ft.Page):
    page.title = "Bull's Benchpress"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.BLACK
    page.padding = 20

    # ========================================================
    # SPARAD DATA
    # ========================================================

    prefs = ft.SharedPreferences()

    saved_lang = await prefs.get("bulls_bench.language")
    saved_unit = await prefs.get("bulls_bench.unit")
    saved_1rm = await prefs.get("bulls_bench.one_rm")

    if saved_lang not in ("sv", "en"):
        saved_lang = "sv"

    if saved_unit not in ("kg", "lb"):
        saved_unit = "kg"

    try:
        saved_1rm = (
            float(saved_1rm)
            if saved_1rm not in (None, "")
            else None
        )

        if saved_1rm is not None and saved_1rm <= 0:
            saved_1rm = None

    except (TypeError, ValueError):
        saved_1rm = None

    state = {
        "language": saved_lang,
        "unit": saved_unit,
        "one_rm": saved_1rm,
    }

    # ========================================================
    # TEXTER
    # ========================================================

    texts = {
        "sv": {
            "app_title": "Bull's Benchpress",
            "tab_calculator": "1RM Kalkylator",
            "tab_program": "Pass",
            "settings": "Inställningar",
            "weight": "Vikt",
            "reps": "Reps",
            "calculate": "Beräkna",
            "estimated_1rm": "Estimerat 1RM",
            "weight_suggestions": "Viktförslag",
            "choose_program": "Välj typ av pass",
            "program_bull": "Bull",
            "program_strength": "Styrka",
            "program_volume": "Volym",
            "language": "Språk",
            "unit": "Enhet",
            "save": "Spara",
            "cancel": "Avbryt",
            "invalid": "Ogiltiga värden",
            "error": "Felaktig inmatning",
            "your_1rm": "Ditt 1RM",
            "enter_1rm": "Skriv in ditt 1RM",
        },

        "en": {
            "app_title": "Bull's Benchpress",
            "tab_calculator": "1RM Calculator",
            "tab_program": "Workout",
            "settings": "Settings",
            "weight": "Weight",
            "reps": "Reps",
            "calculate": "Calculate",
            "estimated_1rm": "Estimated 1RM",
            "weight_suggestions": "Weight suggestions",
            "choose_program": "Choose workout type",
            "program_bull": "Bull",
            "program_strength": "Strength",
            "program_volume": "Volume",
            "language": "Language",
            "unit": "Unit",
            "save": "Save",
            "cancel": "Cancel",
            "invalid": "Invalid values",
            "error": "Invalid input",
            "your_1rm": "Your 1RM",
            "enter_1rm": "Enter your 1RM",
        },
    }

    def t(key: str) -> str:
        return texts[state["language"]].get(key, key)

    # ========================================================
    # UI-ELEMENT
    # ========================================================

    weight_field = ft.TextField(
        label=f"{t('weight')} ({state['unit']})",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=160,
        color=ft.Colors.WHITE,
        label_style=ft.TextStyle(
            color=ft.Colors.WHITE_70
        ),
    )

    reps_field = ft.TextField(
        label=t("reps"),
        keyboard_type=ft.KeyboardType.NUMBER,
        width=100,
        color=ft.Colors.WHITE,
        label_style=ft.TextStyle(
            color=ft.Colors.WHITE_70
        ),
    )

    result_text = ft.Text(
        "",
        size=22,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
    )

    suggestions_column = ft.Column(
        spacing=6
    )

    one_rm_field = ft.TextField(
        label=t("your_1rm"),
        value=(
            f"{saved_1rm:.1f}"
            if saved_1rm is not None
            else ""
        ),
        keyboard_type=ft.KeyboardType.NUMBER,
        width=200,
        hint_text=t("enter_1rm"),
        color=ft.Colors.WHITE,
        label_style=ft.TextStyle(
            color=ft.Colors.WHITE_70
        ),
    )

    program_result = ft.Column(
        spacing=8,
        scroll=ft.ScrollMode.AUTO,
    )

    calc_title = ft.Text(
        t("tab_calculator"),
        size=22,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
    )

    calc_button = ft.Button(
        content=t("calculate"),
        bgcolor=ft.Colors.RED,
        color=ft.Colors.WHITE,
        width=200,
        height=45,
    )

    program_title = ft.Text(
        t("tab_program"),
        size=22,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
    )

    choose_text = ft.Text(
        t("choose_program"),
        size=15,
        color=ft.Colors.WHITE_70,
    )

    btn_bull = ft.Button(
        content=t("program_bull"),
        width=260,
        height=45,
        bgcolor=ft.Colors.RED,
        color=ft.Colors.WHITE,
    )

    btn_strength = ft.Button(
        content=t("program_strength"),
        width=260,
        height=45,
        bgcolor=ft.Colors.RED,
        color=ft.Colors.WHITE,
    )

    btn_volume = ft.Button(
        content=t("program_volume"),
        width=260,
        height=45,
        bgcolor=ft.Colors.RED,
        color=ft.Colors.WHITE,
    )

    # ========================================================
    # HJÄLPFUNKTIONER
    # ========================================================

    def update_suggestions(one_rm: float):
        suggestions_column.controls.clear()

        suggestions_column.controls.append(
            ft.Text(
                t("weight_suggestions"),
                size=16,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE,
            )
        )

        for r in range(1, 11):
            suggested = round_to_half(
                get_weight_for_reps(one_rm, r)
            )

            suggestions_column.controls.append(
                ft.Text(
                    f"{r} reps  →  "
                    f"{suggested:.1f} {state['unit']}",
                    color=ft.Colors.WHITE_70,
                )
            )

    def refresh_1rm_display():
        one_rm = state["one_rm"]

        if one_rm is None:
            one_rm_field.value = ""
            result_text.value = ""
            suggestions_column.controls.clear()
            return

        one_rm_field.value = f"{one_rm:.1f}"

        result_text.value = (
            f"{t('estimated_1rm')}:  "
            f"{one_rm:.1f} {state['unit']}"
        )

        update_suggestions(one_rm)

    def convert_weight(
        value: float,
        from_unit: str,
        to_unit: str,
    ) -> float:

        if from_unit == to_unit:
            return value

        if from_unit == "kg" and to_unit == "lb":
            return value * 2.2046226218

        if from_unit == "lb" and to_unit == "kg":
            return value / 2.2046226218

        return value

    # ========================================================
    # PASS
    # ========================================================

    def get_program(
        program_type: str,
        one_rm: float
    ):
        unit = state["unit"]

        if program_type == "Bull":

            sets = [
                (0.40, 20, "Uppvärmning"),
                (0.65, 10, "Volym"),
                (0.82, 5, "Uppbyggnad"),
                (0.92, 3, "Tungt"),
                (0.94, 2, "Tungt"),
                (0.94, 2, "Tungt"),
                (0.92, 3, "Tungt"),
                (0.65, 18, "Back-off"),
            ]

        elif program_type in ["Styrka", "Strength"]:

            sets = [
                (0.40, 12, "Uppvärmning"),
                (0.70, 6, ""),
                (0.85, 3, ""),
                (0.92, 2, "Tungt"),
                (0.95, 1, "Tungt"),
                (0.95, 1, "Tungt"),
                (0.97, 1, "Tungt"),
                (0.92, 2, "Tungt"),
                (0.75, 8, "Back-off"),
            ]

        else:

            sets = [
                (0.40, 20, "Uppvärmning"),
                (0.60, 12, ""),
                (0.70, 10, ""),
                (0.72, 10, ""),
                (0.75, 8, ""),
                (0.75, 8, ""),
                (0.70, 10, ""),
                (0.80, 6, ""),
                (0.65, 15, "Back-off"),
            ]

        lines = []

        for i, (pct, reps, note) in enumerate(
            sets,
            1
        ):
            weight = max(
                20.0,
                round_to_half(
                    one_rm * pct
                ),
            )

            note_str = (
                f"  · {note}"
                if note
                else ""
            )

            lines.append(
                f"Set {i}:  "
                f"{weight:.1f} {unit}  ×  "
                f"{reps}{note_str}"
            )

        return lines

    # ========================================================
    # EVENTS
    # ========================================================

    async def calculate_clicked(e):
        try:
            if (
                not weight_field.value
                or not reps_field.value
            ):
                result_text.value = t("invalid")
                suggestions_column.controls.clear()
                page.update()
                return

            weight = float(
                weight_field.value.replace(",", ".")
            )

            reps = int(
                reps_field.value
            )

            if reps < 1 or weight <= 0:
                result_text.value = t("invalid")
                suggestions_column.controls.clear()
                page.update()
                return

            one_rm = round_to_half(
                calculate_median_1rm(
                    weight,
                    reps
                )
            )

            state["one_rm"] = one_rm

            await prefs.set(
                "bulls_bench.one_rm",
                one_rm
            )

            one_rm_field.value = (
                f"{one_rm:.1f}"
            )

            result_text.value = (
                f"{t('estimated_1rm')}:  "
                f"{one_rm:.1f} "
                f"{state['unit']}"
            )

            update_suggestions(one_rm)

            page.update()

        except (ValueError, TypeError):
            result_text.value = t("error")
            suggestions_column.controls.clear()
            page.update()

    async def generate_program(
        program_type: str
    ):
        try:
            if not one_rm_field.value:
                program_result.controls = [
                    ft.Text(
                        t("invalid"),
                        color=ft.Colors.RED
                    )
                ]
                page.update()
                return

            one_rm = float(
                one_rm_field.value.replace(",", ".")
            )

            if one_rm <= 0:
                program_result.controls = [
                    ft.Text(
                        t("invalid"),
                        color=ft.Colors.RED
                    )
                ]
                page.update()
                return

            one_rm = round_to_half(one_rm)

            state["one_rm"] = one_rm

            await prefs.set(
                "bulls_bench.one_rm",
                one_rm
            )

            one_rm_field.value = (
                f"{one_rm:.1f}"
            )

            lines = get_program(
                program_type,
                one_rm
            )

            program_result.controls.clear()

            program_result.controls.append(
                ft.Text(
                    f"--- {program_type.upper()} ---",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.RED,
                )
            )

            for line in lines:
                program_result.controls.append(
                    ft.Text(
                        line,
                        size=16,
                        color=ft.Colors.WHITE,
                    )
                )

            page.update()

        except (ValueError, TypeError):
            program_result.controls = [
                ft.Text(
                    t("error"),
                    color=ft.Colors.RED
                )
            ]
            page.update()

    def update_language():
        weight_field.label = (
            f"{t('weight')} ({state['unit']})"
        )

        reps_field.label = t("reps")

        one_rm_field.label = t("your_1rm")

        one_rm_field.hint_text = t(
            "enter_1rm"
        )

        calc_title.value = t(
            "tab_calculator"
        )

        calc_button.content = t(
            "calculate"
        )

        program_title.value = t(
            "tab_program"
        )

        choose_text.value = t(
            "choose_program"
        )

        btn_bull.content = t(
            "program_bull"
        )

        btn_strength.content = t(
            "program_strength"
        )

        btn_volume.content = t(
            "program_volume"
        )

        tab_bar.tabs[0].label = t(
            "tab_calculator"
        )

        tab_bar.tabs[1].label = t(
            "tab_program"
        )

        page.appbar.title.value = t(
            "app_title"
        )

        refresh_1rm_display()

        page.update()

    # ========================================================
    # INSTÄLLNINGAR
    # ========================================================

    def open_settings(e):

        async def save_settings(e):
            old_unit = state["unit"]

            new_language = language_dropdown.value
            new_unit = unit_dropdown.value

            if (
                state["one_rm"] is not None
                and old_unit != new_unit
            ):
                state["one_rm"] = convert_weight(
                    state["one_rm"],
                    old_unit,
                    new_unit,
                )

                state["one_rm"] = round_to_half(
                    state["one_rm"]
                )

                await prefs.set(
                    "bulls_bench.one_rm",
                    state["one_rm"]
                )

            state["language"] = new_language
            state["unit"] = new_unit

            await prefs.set(
                "bulls_bench.language",
                state["language"]
            )

            await prefs.set(
                "bulls_bench.unit",
                state["unit"]
            )

            update_language()

            page.pop_dialog()

        def close_settings(e):
            page.pop_dialog()

        language_dropdown = ft.Dropdown(
            label=t("language"),
            value=state["language"],
            options=[
                ft.dropdown.Option(
                    "sv",
                    "Svenska"
                ),
                ft.dropdown.Option(
                    "en",
                    "English"
                ),
            ],
            width=220,
            color=ft.Colors.WHITE,
        )

        unit_dropdown = ft.Dropdown(
            label=t("unit"),
            value=state["unit"],
            options=[
                ft.dropdown.Option(
                    "kg",
                    "Kilogram (kg)"
                ),
                ft.dropdown.Option(
                    "lb",
                    "Pounds (lb)"
                ),
            ],
            width=220,
            color=ft.Colors.WHITE,
        )

        dialog = ft.AlertDialog(
            title=ft.Text(
                t("settings"),
                color=ft.Colors.WHITE,
            ),
            bgcolor=ft.Colors.BLACK,
            content=ft.Column(
                [
                    language_dropdown,
                    unit_dropdown,
                ],
                tight=True,
                spacing=15,
            ),
            actions=[
                ft.TextButton(
                    t("cancel"),
                    on_click=close_settings,
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE_70
                    ),
                ),

                ft.Button(
                    content=t("save"),
                    on_click=save_settings,
                    bgcolor=ft.Colors.RED,
                    color=ft.Colors.WHITE,
                ),
            ],
        )

        page.show_dialog(dialog)

    # ========================================================
    # KNAPP-HANDLERS
    #
    # Async lambdas finns inte i Python. Därför använder vi
    # riktiga async-funktioner här.
    # ========================================================

    async def bull_clicked(e):
        await generate_program("Bull")

    async def strength_clicked(e):
        await generate_program("Styrka")

    async def volume_clicked(e):
        await generate_program("Volym")

    calc_button.on_click = calculate_clicked

    btn_bull.on_click = bull_clicked
    btn_strength.on_click = strength_clicked
    btn_volume.on_click = volume_clicked

    # ========================================================
    # LAYOUT
    # ========================================================

    calculator_content = ft.Container(
        content=ft.Column(
            [
                calc_title,

                ft.Container(
                    height=10
                ),

                ft.Row(
                    [
                        weight_field,
                        reps_field,
                    ],
                    spacing=12,
                ),

                ft.Container(
                    height=6
                ),

                calc_button,

                ft.Container(
                    height=10
                ),

                result_text,

                ft.Divider(
                    color=ft.Colors.WHITE_24
                ),

                suggestions_column,
            ],
            spacing=8,
            scroll=ft.ScrollMode.AUTO,
        ),
        expand=True,
        padding=10,
    )

    program_content = ft.Container(
        content=ft.Column(
            [
                program_title,

                ft.Container(
                    height=8
                ),

                one_rm_field,

                ft.Container(
                    height=10
                ),

                choose_text,

                btn_bull,
                btn_strength,
                btn_volume,

                ft.Divider(
                    color=ft.Colors.WHITE_24
                ),

                program_result,
            ],
            spacing=10,
            horizontal_alignment=(
                ft.CrossAxisAlignment.CENTER
            ),
            scroll=ft.ScrollMode.AUTO,
        ),
        expand=True,
        padding=10,
    )

    tab_bar = ft.TabBar(
        tabs=[
            ft.Tab(
                label=t("tab_calculator")
            ),
            ft.Tab(
                label=t("tab_program")
            ),
        ],
        label_color=ft.Colors.RED,
        unselected_label_color=ft.Colors.WHITE_54,
        indicator_color=ft.Colors.RED,
    )

    tabs = ft.Tabs(
        length=2,
        selected_index=0,
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                tab_bar,

                ft.TabBarView(
                    expand=True,
                    controls=[
                        calculator_content,
                        program_content,
                    ],
                ),
            ],
        ),
    )

    page.appbar = ft.AppBar(
        title=ft.Text(
            t("app_title"),
            color=ft.Colors.WHITE,
        ),
        center_title=True,
        bgcolor=ft.Colors.BLACK,
        actions=[
            ft.IconButton(
                ft.Icons.SETTINGS,
                icon_color=ft.Colors.RED,
                on_click=open_settings,
            )
        ],
    )

    page.add(tabs)


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    ft.run(main)