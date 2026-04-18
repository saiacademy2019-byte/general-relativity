"""
Part 4 — The Metric Tensor
5 scenes:
  MetricProblem    — why coordinates alone don't give distances (the core problem)
  MetricFlatGrid   — metric as a local measuring rule, distorted grid
  MetricTensor     — ds² = g_μν dx^μ dx^ν, the general spacetime formula
  MinkowskiMetric  — flat spacetime, minus sign on time, light cone, proper time
  MetricGravity    — mass deforms the metric, gravity = geometry
"""
from manim import *
import numpy as np

WLINE_COLOR = "#E07B54"
TAU_COLOR   = "#F5D040"
EARTH_COL   = "#3A7BD5"
GEO_COLOR   = "#50C878"
METRIC_COL  = "#C77DFF"   # purple — metric tensor quantities


# ══════════════════════════════════════════════════════════════════════════════
# Scene 1 — MetricProblem
#   Show that equal coordinate steps do NOT mean equal physical distances.
#   Two acts:
#     Act 1 — rubber-sheet grid: same Δx on a stretched grid → different lengths
#     Act 2 — satellite paradox: two orbits, identical (Δt, Δφ), different speeds
# ══════════════════════════════════════════════════════════════════════════════
class MetricProblem(Scene):
    def construct(self):
        title = Text("The Problem: Coordinates ≠ Distances", font_size=38, weight=BOLD)
        title.to_edge(UP, buff=0.38)
        self.play(Write(title), run_time=2); self.wait(0.4)

        # ── ACT 1: flat grid vs stretched grid ───────────────────────────────
        act1 = Text("Act 1 — Uniform grid", font_size=22, color=GRAY)
        act1.next_to(title, DOWN, buff=0.22)
        self.play(FadeIn(act1), run_time=1)

        div = DashedLine(UP * 2.2, DOWN * 3.8, color=GRAY, stroke_opacity=0.35)
        self.add(div)

        # LEFT: uniform grid
        flat = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-2, 2, 1],
            x_length=5.6, y_length=3.6,
            background_line_style={"stroke_color": BLUE_D, "stroke_opacity": 0.75, "stroke_width": 2.0},
            axis_config={"stroke_opacity": 0},
        ).move_to(LEFT * 3.2 + DOWN * 1.0)

        flat_lbl = Text("Uniform grid", font_size=19, color=GRAY).next_to(flat, UP, buff=0.12)
        self.play(Create(flat), FadeIn(flat_lbl), run_time=1.5)

        # Draw two equal-step arrows on the flat grid
        p_a = np.array(flat.c2p(-2, -0.5))
        p_b = np.array(flat.c2p(-1, -0.5))
        p_c = np.array(flat.c2p( 0,  0.8))
        p_d = np.array(flat.c2p( 1,  0.8))

        arr_a = Arrow(p_a, p_b, color=GEO_COLOR, buff=0, stroke_width=2.5,
                      max_tip_length_to_length_ratio=0.25)
        arr_b = Arrow(p_c, p_d, color=GEO_COLOR, buff=0, stroke_width=2.5,
                      max_tip_length_to_length_ratio=0.25)
        lbl_a = Text("Δx = 1", font_size=15, color=GEO_COLOR).next_to(arr_a, DOWN, buff=0.08)
        lbl_b = Text("Δx = 1", font_size=15, color=GEO_COLOR).next_to(arr_b, UP,   buff=0.08)

        self.play(GrowArrow(arr_a), GrowArrow(arr_b), run_time=1.5)
        self.play(Write(lbl_a), Write(lbl_b), run_time=1)

        ok_lbl = Text("same coordinate step → same physical distance  ✓",
                      font_size=17, color=GEO_COLOR).next_to(flat, DOWN, buff=0.12)
        self.play(Write(ok_lbl), run_time=1.5)

        # RIGHT: stretched grid (simulated by uneven axis lengths)
        stretched = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-2, 2, 1],
            x_length=5.6, y_length=3.6,
            background_line_style={"stroke_color": ORANGE, "stroke_opacity": 0.80, "stroke_width": 2.0},
            axis_config={"stroke_opacity": 0},
        ).move_to(RIGHT * 3.2 + DOWN * 1.0)

        # Manually nudge the grid lines to look uneven
        stretched.apply_function(lambda p: np.array([
            p[0] * (1 + 0.18 * np.cos(p[0] * 0.7)),
            p[1] * (1 + 0.14 * np.sin(p[1] * 0.9)),
            0
        ]))

        str_lbl = Text("Stretched (uneven) grid", font_size=19, color=GRAY)
        str_lbl.next_to(stretched, UP, buff=0.12)
        self.play(Create(stretched), FadeIn(str_lbl), run_time=1.5)

        # Two arrows at different positions — same Δx=1 coordinate step
        q_a = np.array(stretched.c2p(-2, -0.5))
        q_b = np.array(stretched.c2p(-1, -0.5))
        q_c = np.array(stretched.c2p( 0,  0.8))
        q_d = np.array(stretched.c2p( 1,  0.8))

        arr_c = Arrow(q_a, q_b, color=ORANGE, buff=0, stroke_width=2.5,
                      max_tip_length_to_length_ratio=0.25)
        arr_d = Arrow(q_c, q_d, color=RED_D,  buff=0, stroke_width=2.5,
                      max_tip_length_to_length_ratio=0.25)
        lbl_c = Text("Δx = 1", font_size=15, color=ORANGE).next_to(arr_c, DOWN, buff=0.08)
        lbl_d = Text("Δx = 1", font_size=15, color=RED_D ).next_to(arr_d, UP,   buff=0.08)

        self.play(GrowArrow(arr_c), GrowArrow(arr_d), run_time=1.5)
        self.play(Write(lbl_c), Write(lbl_d), run_time=1)

        bad_lbl = Text("same coordinate step → DIFFERENT physical distance  ✗",
                       font_size=17, color=RED_D).next_to(stretched, DOWN, buff=0.12)
        self.play(Write(bad_lbl), run_time=1.5)
        self.wait(2)

        # ── ACT 2: satellite paradox ─────────────────────────────────────────
        self.play(
            FadeOut(flat, flat_lbl, arr_a, arr_b, lbl_a, lbl_b, ok_lbl,
                    stretched, str_lbl, arr_c, arr_d, lbl_c, lbl_d, bad_lbl,
                    div, act1),
            run_time=1.2,
        )

        act2 = Text("Act 2 — The Satellite Paradox", font_size=26, color=YELLOW, weight=BOLD)
        act2.next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(act2), run_time=1)

        earth_ctr = LEFT * 2.0 + DOWN * 0.4
        earth = Circle(radius=0.45, color=EARTH_COL, fill_opacity=0.9).move_to(earth_ctr)
        self.play(FadeIn(earth), run_time=1)

        # Two orbit rings at different radii
        R1, R2 = 1.35, 2.2
        orbit1 = Circle(radius=R1, color=WLINE_COLOR, stroke_width=2,
                        stroke_opacity=0.6).move_to(earth_ctr)
        orbit2 = Circle(radius=R2, color=METRIC_COL, stroke_width=2,
                        stroke_opacity=0.6).move_to(earth_ctr)
        sat1 = Dot(earth_ctr + RIGHT * R1, color=WLINE_COLOR, radius=0.13)
        sat2 = Dot(earth_ctr + RIGHT * R2, color=METRIC_COL,  radius=0.13)
        lbl1 = Text("Sat A  (low orbit)",  font_size=17, color=WLINE_COLOR)
        lbl2 = Text("Sat B  (high orbit)", font_size=17, color=METRIC_COL)
        lbl1.next_to(orbit1, DOWN, buff=0.12)
        lbl2.next_to(orbit2, DOWN, buff=0.08)

        self.play(Create(orbit1), Create(orbit2), run_time=1.5)
        self.play(FadeIn(sat1, sat2, lbl1, lbl2), run_time=1)

        # Animate both completing the same Δφ at the same time
        T = 4.0
        tracker = ValueTracker(0)
        OMEGA = 2 * PI / T

        sat1.add_updater(lambda m: m.move_to(
            earth_ctr + np.array([R1 * np.cos(OMEGA * tracker.get_value()),
                                  R1 * np.sin(OMEGA * tracker.get_value()), 0])))
        sat2.add_updater(lambda m: m.move_to(
            earth_ctr + np.array([R2 * np.cos(OMEGA * tracker.get_value()),
                                  R2 * np.sin(OMEGA * tracker.get_value()), 0])))

        self.play(tracker.animate.set_value(T), run_time=T, rate_func=linear)
        sat1.clear_updaters(); sat2.clear_updaters()

        # Show the "paradox" annotation on the right
        paradox_box = VGroup(
            Text("Both satellites complete 1 full orbit:", font_size=19),
            Text("  Δt  =  same", font_size=19, color=YELLOW),
            Text("  Δφ  =  2π  (same)", font_size=19, color=YELLOW),
            Text("Pythagoras says:  |v|  =  same  ??", font_size=19, color=RED_D, weight=BOLD),
            Text("But Sat B clearly travels farther!", font_size=19, color=RED_D),
        ).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        paradox_box.move_to(RIGHT * 3.2 + DOWN * 0.3)
        self.play(FadeIn(paradox_box, shift=LEFT * 0.2), run_time=2.5)
        self.wait(2)

        conclusion = Text(
            "Pythagoras fails in curved/distorted coordinates.\nWe need a new rule for measuring distances.",
            font_size=22, color=YELLOW, line_spacing=1.3,
        ).to_edge(DOWN, buff=0.28)
        self.play(Write(conclusion), run_time=2.5)
        self.wait(3)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 2 — MetricFlatGrid
#   Introduce the metric as a "local measuring rule".
#   Show flat 2D grid → distorted grid → metric components g₁₁, g₁₂, g₂₂
# ══════════════════════════════════════════════════════════════════════════════
class MetricFlatGrid(Scene):
    def construct(self):
        title = Text("The Metric — A Local Measuring Rule", font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.38)
        self.play(Write(title), run_time=2); self.wait(0.4)

        # ── Flat grid with Pythagoras ─────────────────────────────────────────
        grid = NumberPlane(
            x_range=[-4, 4, 1], y_range=[-3, 3, 1],
            x_length=6.5, y_length=4.5,
            background_line_style={"stroke_color": BLUE_D, "stroke_opacity": 0.75, "stroke_width": 2.0},
            axis_config={"color": WHITE, "stroke_opacity": 0.6},
        ).move_to(LEFT * 2.0 + DOWN * 0.5)
        self.play(Create(grid), run_time=1.5)

        # Displacement arrow
        A = np.array(grid.c2p(0, 0))
        B = np.array(grid.c2p(2, 1.5))
        arrow = Arrow(A, B, color=WLINE_COLOR, buff=0, stroke_width=3,
                      max_tip_length_to_length_ratio=0.20)
        dx_line = DashedLine(A, np.array(grid.c2p(2, 0)), color=YELLOW,   stroke_width=2)
        dy_line = DashedLine(np.array(grid.c2p(2, 0)), B,  color=GEO_COLOR, stroke_width=2)
        dx_lbl  = Text("dx", font_size=20, color=YELLOW).next_to(grid.c2p(1, 0),   DOWN, buff=0.10)
        dy_lbl  = Text("dy", font_size=20, color=GEO_COLOR).next_to(grid.c2p(2, 0.75), RIGHT, buff=0.10)
        ds_lbl  = Text("ds", font_size=20, color=WLINE_COLOR)
        ds_lbl.move_to(np.array(grid.c2p(0.8, 0.9)))

        self.play(Create(dx_line), Create(dy_line), run_time=1.2)
        self.play(Write(dx_lbl), Write(dy_lbl), run_time=0.8)
        self.play(GrowArrow(arrow), Write(ds_lbl), run_time=1.2)

        pyth = Text("ds²  =  dx²  +  dy²", font_size=26, color=WHITE, weight=BOLD)
        pyth.to_edge(RIGHT, buff=0.45).shift(UP * 1.5)
        pyth_sub = Text("(flat grid — Pythagoras)", font_size=17, color=GRAY)
        pyth_sub.next_to(pyth, DOWN, buff=0.10)
        self.play(Write(pyth), Write(pyth_sub), run_time=1.5)
        self.wait(1.5)

        # ── Distort the grid ─────────────────────────────────────────────────
        cap_distort = Text(
            "Now stretch the grid — the coordinate squares\nno longer represent equal physical distances.",
            font_size=20, color=ORANGE, line_spacing=1.3,
        ).to_edge(DOWN, buff=0.28)
        self.play(Write(cap_distort), run_time=2)

        distorted = grid.copy()
        distorted.apply_function(lambda p: np.array([
            p[0] * (1 + 0.22 * np.sin(p[0] * 0.5 + 0.5)),
            p[1] * (1 + 0.18 * np.cos(p[1] * 0.6 + 0.3)),
            0,
        ]))
        distorted.set_background_line_style({"stroke_color": ORANGE, "stroke_opacity": 0.80, "stroke_width": 2.0})

        self.play(Transform(grid, distorted), run_time=2.5)
        self.wait(1)

        # ── Metric formula replaces Pythagoras ───────────────────────────────
        self.play(FadeOut(pyth, pyth_sub), run_time=0.8)

        metric_box = VGroup(
            Text("Curved grid: Pythagoras breaks.", font_size=19, color=ORANGE),
            Text("Need extra factors at each point:", font_size=19, color=GRAY),
            Text("ds²  =  g₁₁ dx²  +  2g₁₂ dx dy  +  g₂₂ dy²", font_size=22,
                 color=METRIC_COL, weight=BOLD),
            Text("g₁₁, g₁₂, g₂₂ depend on WHERE you are", font_size=18, color=GRAY),
        ).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        metric_box.to_edge(RIGHT, buff=0.35).shift(UP * 0.8)
        box_rect = SurroundingRectangle(metric_box[2], color=METRIC_COL, buff=0.12, stroke_width=2)

        self.play(FadeIn(metric_box[0], metric_box[1]), run_time=1.2)
        self.play(Write(metric_box[2]), run_time=1.5)
        self.play(Create(box_rect), run_time=0.8)
        self.play(FadeIn(metric_box[3]), run_time=1)

        self.play(FadeOut(cap_distort), run_time=0.8)
        final_cap = Text(
            "The metric tensor is the collection of factors g that tells\n"
            "how much each coordinate step actually means physically.",
            font_size=21, color=YELLOW, line_spacing=1.3,
        ).to_edge(DOWN, buff=0.28)
        self.play(Write(final_cap), run_time=2.5)
        self.wait(3)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 3 — MetricTensor
#   The full spacetime metric: ds² = g_μν dx^μ dx^ν
#   Show what each index means; display as a 4×4 matrix schematic.
# ══════════════════════════════════════════════════════════════════════════════
class MetricTensor(Scene):
    def construct(self):
        title_txt = Text("The Metric Tensor  ", font_size=38, weight=BOLD)
        title_tex = MathTex(r"g_{\mu\nu}", font_size=52)
        title = VGroup(title_txt, title_tex).arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
        title.to_edge(UP, buff=0.38)
        self.play(Write(title), run_time=2); self.wait(0.4)

        # ── Core formula ─────────────────────────────────────────────────────
        formula = MathTex(
            r"ds^2 \;=\; g_{\mu\nu}\, dx^\mu\, dx^\nu",
            font_size=44, color=METRIC_COL,
        )
        formula.next_to(title, DOWN, buff=0.35)
        box = SurroundingRectangle(formula, color=METRIC_COL, buff=0.18, stroke_width=2.5)
        self.play(Write(formula), run_time=1.8)
        self.play(Create(box), run_time=1)
        self.wait(0.5)

        # ── Annotate each part ───────────────────────────────────────────────
        ann_ds = VGroup(MathTex(r"ds^2",          font_size=22, color=WHITE),
                        Text(" — actual physical interval",            font_size=17, color=WHITE)).arrange(RIGHT, buff=0.08)
        ann_g  = VGroup(MathTex(r"g_{\mu\nu}",   font_size=22, color=METRIC_COL),
                        Text(" — metric tensor (local measuring rule)", font_size=17, color=METRIC_COL)).arrange(RIGHT, buff=0.08)
        ann_dx = VGroup(MathTex(r"dx^\mu dx^\nu", font_size=22, color=YELLOW),
                        Text(" — coordinate displacements",             font_size=17, color=YELLOW)).arrange(RIGHT, buff=0.08)

        annotations = VGroup(ann_ds, ann_g, ann_dx).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        annotations.next_to(formula, DOWN, buff=0.40).to_edge(LEFT, buff=0.8)
        self.play(FadeIn(annotations, shift=DOWN * 0.2), run_time=1.5)
        self.wait(1.0)

        # ── 4×4 matrix using MobjectMatrix (handles brackets automatically) ──
        matrix_title = Text("In 4D spacetime  (t, x, y, z)  it is a 4×4 matrix:",
                            font_size=20, color=GRAY)
        matrix_title.next_to(annotations, DOWN, buff=0.35)
        self.play(Write(matrix_title), run_time=1.2)

        M_COLOR = METRIC_COL
        CELL_W, CELL_H = 0.78, 0.52
        symbol_rows = [
            ["g₀₀", "g₀₁", "g₀₂", "g₀₃"],
            ["g₁₀", "g₁₁", "g₁₂", "g₁₃"],
            ["g₂₀", "g₂₁", "g₂₂", "g₂₃"],
            ["g₃₀", "g₃₁", "g₃₂", "g₃₃"],
        ]
        matrix_entries = VGroup()
        for i, row in enumerate(symbol_rows):
            for j, sym in enumerate(row):
                txt = Text(sym, font_size=17,
                           color=M_COLOR if i == j else GRAY)
                txt.move_to(np.array([j * CELL_W, -i * CELL_H, 0]))
                matrix_entries.add(txt)

        # Place entries at their final position first, then compute bracket corners
        matrix_entries.next_to(matrix_title, DOWN, buff=0.28).to_edge(LEFT, buff=1.2)

        PAD_X, PAD_Y, TICK = 0.18, 0.14, 0.18
        c_ul = matrix_entries.get_corner(UL) + np.array([-PAD_X,  PAD_Y, 0])
        c_dl = matrix_entries.get_corner(DL) + np.array([-PAD_X, -PAD_Y, 0])
        c_ur = matrix_entries.get_corner(UR) + np.array([ PAD_X,  PAD_Y, 0])
        c_dr = matrix_entries.get_corner(DR) + np.array([ PAD_X, -PAD_Y, 0])

        def make_bracket(top, bot, facing_right):
            tick_dir = RIGHT * TICK if facing_right else LEFT * TICK
            return VGroup(
                Line(top, top + tick_dir, color=WHITE, stroke_width=2),
                Line(top, bot,            color=WHITE, stroke_width=2),
                Line(bot, bot + tick_dir, color=WHITE, stroke_width=2),
            )

        brack_l = make_bracket(c_ul, c_dl, facing_right=True)
        brack_r = make_bracket(c_ur, c_dr, facing_right=False)

        mat_group = VGroup(brack_l, matrix_entries, brack_r)

        diag_note = Text("Diagonal: measure stretch along each axis", font_size=17, color=METRIC_COL)
        off_note  = Text("Off-diagonal: mixing between coordinates",  font_size=17, color=GRAY)
        diag_note.next_to(mat_group, RIGHT, buff=0.45).shift(UP * 0.35)
        off_note .next_to(diag_note, DOWN,  buff=0.22)

        self.play(FadeIn(mat_group), run_time=1.8)
        self.play(Write(diag_note), Write(off_note), run_time=1.5)
        self.wait(2)

        sym_note = Text(
            "Key property:  g_μν = g_νμ  (symmetric)\n"
            "→ at most 10 independent components in 4D",
            font_size=19, color=YELLOW, line_spacing=1.3,
        ).to_edge(DOWN, buff=0.28)
        self.play(Write(sym_note), run_time=2)
        self.wait(2.5)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 4 — MinkowskiMetric
#   Flat spacetime: ds² = −c²dt² + dx²
#   The minus sign creates light cones; links back to proper time.
# ══════════════════════════════════════════════════════════════════════════════
class MinkowskiMetric(Scene):
    def construct(self):
        title = Text("Flat Spacetime — The Minkowski Metric", font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.38)
        self.play(Write(title), run_time=2); self.wait(0.4)

        # ── Show the interval formula ─────────────────────────────────────────
        mink = Text("ds²  =  −c² dt²  +  dx²  +  dy²  +  dz²",
                    font_size=28, color=METRIC_COL, weight=BOLD)
        mink.next_to(title, DOWN, buff=0.35)
        mink_box = SurroundingRectangle(mink, color=METRIC_COL, buff=0.16, stroke_width=2)
        self.play(Write(mink), run_time=1.8)
        self.play(Create(mink_box), run_time=0.8)

        # Metric matrix (Minkowski, 2D version for clarity)
        mat_lbl = Text("In matrix form (1+1 D for clarity):", font_size=19, color=GRAY)
        mat_lbl.next_to(mink, DOWN, buff=0.38)
        self.play(Write(mat_lbl), run_time=1)

        mat_entries = VGroup(
            Text("( −1     0 )", font_size=24, color=METRIC_COL),
            Text("(  0    +1 )", font_size=24, color=METRIC_COL),
        ).arrange(DOWN, buff=0.06)
        mat_entries.next_to(mat_lbl, DOWN, buff=0.20)

        mat_eq = Text("g_μν  =", font_size=24, color=WHITE)
        mat_eq.next_to(mat_entries, LEFT, buff=0.3)

        minus_note = Text("← time gets a MINUS sign", font_size=17, color=RED_D)
        plus_note  = Text("← space gets a PLUS sign",  font_size=17, color=GEO_COLOR)
        minus_note.next_to(mat_entries[0], RIGHT, buff=0.3)
        plus_note .next_to(mat_entries[1], RIGHT, buff=0.3)

        self.play(FadeIn(mat_eq, mat_entries), run_time=1.5)
        self.play(Write(minus_note), Write(plus_note), run_time=1.5)
        self.wait(1.2)

        # ── Light cone on the right ───────────────────────────────────────────
        ax = Axes(
            x_range=[-2.5, 2.5, 1], y_range=[0, 4, 1],
            x_length=4.0, y_length=3.5,
            axis_config={"color": WHITE, "include_tip": True, "tip_length": 0.16},
        ).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.4)
        t_lbl = Text("t", font_size=22, color=YELLOW).next_to(ax.y_axis.get_top(), LEFT, buff=0.10)
        x_lbl = Text("x", font_size=22, color=YELLOW).next_to(ax.x_axis.get_right(), DOWN, buff=0.10)
        self.play(Create(ax), Write(t_lbl), Write(x_lbl), run_time=1.2)

        # Light cone lines: t = ±x  (45°)
        lc_r = ax.plot(lambda x: x,  x_range=[0,  2.4], color=YELLOW, stroke_width=2.5)
        lc_l = ax.plot(lambda x: -x, x_range=[-2.4, 0], color=YELLOW, stroke_width=2.5)
        self.play(Create(lc_r), Create(lc_l), run_time=1.5)

        # Region labels
        future   = Text("timelike\n(ds² < 0)", font_size=14, color=TAU_COLOR, line_spacing=1.2)
        spacelike= Text("spacelike\n(ds² > 0)", font_size=14, color=GEO_COLOR, line_spacing=1.2)
        lightlbl = Text("light\n(ds²=0)", font_size=13, color=YELLOW, line_spacing=1.2)
        future.move_to(ax.c2p(0, 2.6))
        spacelike.move_to(ax.c2p(1.8, 0.5))
        lightlbl.move_to(ax.c2p(1.5, 1.8))
        self.play(FadeIn(future, spacelike, lightlbl), run_time=1.2)

        # ── Proper time link ─────────────────────────────────────────────────
        proper = Text(
            "For a massive object (timelike path):   ds² < 0\n"
            "Define proper time:   dτ²  =  −ds²/c²  =  dt²  −  dx²/c²",
            font_size=19, color=TAU_COLOR, line_spacing=1.3,
        ).to_edge(DOWN, buff=0.28)
        self.play(Write(proper), run_time=2.5)
        self.wait(3)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 5 — MetricGravity
#   Matter tells spacetime how to curve.
#   Show: uniform metric → place a mass → grid distorts near it.
#   Clocks at two heights tick at different rates.
# ══════════════════════════════════════════════════════════════════════════════
class MetricGravity(Scene):
    def construct(self):
        title = Text("The Metric is LOCAL — and Curvature is its Change", font_size=32, weight=BOLD)
        title.to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=2); self.wait(0.4)

        # ══ ACT 1: The metric is a LOCAL instruction card ════════════════════
        act1 = Text("Every point in spacetime carries its own measuring rule.",
                    font_size=22, color=GRAY)
        act1.next_to(title, DOWN, buff=0.28)
        self.play(FadeIn(act1), run_time=1.2)

        # Flat grid with identical little "g-cards" at each intersection
        GRID_CTR = DOWN * 0.6
        flat_g = NumberPlane(
            x_range=[-4, 4, 2], y_range=[-2, 2, 2],
            x_length=7.0, y_length=3.8,
            background_line_style={"stroke_color": BLUE_D, "stroke_opacity": 0.75, "stroke_width": 2.0},
            axis_config={"stroke_opacity": 0},
        ).move_to(GRID_CTR)
        self.play(Create(flat_g), run_time=1.2)

        # Place identical "instruction cards" at several grid points
        card_positions_flat = [(-3,-1), (-3,1), (0,-1), (0,1), (3,-1), (3,1)]
        flat_cards = VGroup()
        for cx, cy in card_positions_flat:
            card = Text("g = 1", font_size=13, color=BLUE_C)
            card.move_to(np.array(flat_g.c2p(cx, cy)) + UP * 0.28)
            flat_cards.add(card)

        flat_card_lbl = Text(
            "Flat space: every point has the SAME instructions  →  g = 1 everywhere",
            font_size=19, color=BLUE_C,
        ).to_edge(DOWN, buff=0.28)
        self.play(FadeIn(flat_cards), run_time=1.2)
        self.play(Write(flat_card_lbl), run_time=1.8)
        self.wait(2)

        # ══ ACT 2: Place a mass — instructions change with position ══════════
        self.play(FadeOut(flat_cards, flat_card_lbl, act1), run_time=0.8)

        act2 = Text(
            "Place a mass — the instructions at each point become DIFFERENT.",
            font_size=22, color=ORANGE,
        )
        act2.next_to(title, DOWN, buff=0.28)
        self.play(FadeIn(act2), run_time=1.2)

        MASS_POS = GRID_CTR   # mass at centre of grid

        # Warp the grid
        def warp(p):
            centre = np.array([MASS_POS[0], MASS_POS[1], 0])
            delta  = p - centre
            r      = np.linalg.norm(delta) + 0.01
            factor = 1 - 0.52 * np.exp(-r * 0.75)
            return centre + delta * factor

        curved_g = flat_g.copy()
        curved_g.set_background_line_style(
            {"stroke_color": ORANGE, "stroke_opacity": 0.80, "stroke_width": 2.0})
        self.play(Transform(flat_g, curved_g), run_time=2)

        mass_dot = Dot(MASS_POS, color=YELLOW, radius=0.26)
        self.play(FadeIn(mass_dot), run_time=0.8)

        # Now place DIFFERENT instruction cards — values vary with distance
        # Closer to mass → g value is larger (more stretching)
        card_data = [
            ((-3.2, -1.5), "g ≈ 1.01", BLUE_C),
            ((-3.2,  1.5), "g ≈ 1.01", BLUE_C),
            ((-1.4, -0.8), "g ≈ 1.18", GEO_COLOR),
            ((-1.4,  0.8), "g ≈ 1.18", GEO_COLOR),
            ((-0.5,  0.0), "g ≈ 1.55", WLINE_COLOR),
            (( 0.5,  0.0), "g ≈ 1.55", WLINE_COLOR),
            (( 1.4, -0.8), "g ≈ 1.18", GEO_COLOR),
            (( 3.2,  1.5), "g ≈ 1.01", BLUE_C),
        ]
        curved_cards = VGroup()
        for (cx, cy), label, col in card_data:
            card = Text(label, font_size=13, color=col)
            card.move_to(np.array(flat_g.c2p(cx, cy)) + UP * 0.30)
            curved_cards.add(card)

        self.play(FadeIn(curved_cards), run_time=1.5)

        curved_lbl = Text(
            "Curved space: each point has DIFFERENT instructions — g varies with position",
            font_size=19, color=ORANGE,
        ).to_edge(DOWN, buff=0.44)
        self.play(Write(curved_lbl), run_time=1.8)
        self.wait(2)

        # ══ ACT 3: Curvature = how fast the instructions change ══════════════
        self.play(FadeOut(curved_cards, curved_lbl, act2), run_time=0.8)

        act3 = Text(
            "CURVATURE = how rapidly the instructions change from point to point.",
            font_size=21, color=YELLOW, weight=BOLD,
        )
        act3.next_to(title, DOWN, buff=0.28)
        self.play(FadeIn(act3), run_time=1.2)

        # Draw a gradient arrow showing the change (far → near mass)
        p_far  = np.array(flat_g.c2p(-3.0, 0))
        p_near = np.array(flat_g.c2p(-0.4, 0))
        grad_arr = Arrow(p_far, p_near, color=YELLOW, stroke_width=3,
                         max_tip_length_to_length_ratio=0.18, buff=0)
        grad_lbl = Text("g increasing →\n(space more stretched)", font_size=15,
                        color=YELLOW, line_spacing=1.2)
        grad_lbl.next_to(grad_arr, UP, buff=0.12)

        self.play(GrowArrow(grad_arr), Write(grad_lbl), run_time=1.8)

        christoffel_note = Text(
            "The Christoffel symbols  Γ  measure this rate of change of g.\n"
            "No change in g  →  Γ = 0  →  no gravity.\n"
            "Rapidly changing g near a mass  →  Γ ≠ 0  →  objects accelerate.",
            font_size=18, color=GRAY, line_spacing=1.4,
        ).to_edge(DOWN, buff=0.28)
        self.play(Write(christoffel_note), run_time=3)
        self.wait(2)

        # ══ ACT 4: Clocks confirm the changing metric ════════════════════════
        self.play(FadeOut(christoffel_note, grad_arr, grad_lbl, act3,
                          mass_dot), run_time=0.8)

        act4 = Text("Physical consequence: clocks tick at different rates.",
                    font_size=21, color=GEO_COLOR)
        act4.next_to(title, DOWN, buff=0.28)
        self.play(FadeIn(act4), run_time=1)

        mass_dot2 = Dot(MASS_POS, color=YELLOW, radius=0.26)
        self.play(FadeIn(mass_dot2), run_time=0.5)

        T_ANIM     = 5.0
        OMEGA_FAR  = 2 * PI / 2.0
        OMEGA_NEAR = 2 * PI / 3.4

        CLK_FAR  = MASS_POS + UP * 1.55 + LEFT * 2.2
        CLK_NEAR = MASS_POS + UP * 0.55

        def clock_hand(centre, omega, tracker, length=0.27):
            angle = PI / 2 - omega * tracker.get_value()
            end   = centre + length * np.array([np.cos(angle), np.sin(angle), 0])
            return Line(centre, end, color=WHITE, stroke_width=3)

        face_far  = Circle(radius=0.30, color=WHITE, stroke_width=2).move_to(CLK_FAR)
        face_near = Circle(radius=0.30, color=WHITE, stroke_width=2).move_to(CLK_NEAR)

        lbl_far  = Text("far from mass\ng is small → time fast", font_size=13,
                        color=GEO_COLOR, line_spacing=1.2).next_to(face_far, LEFT, buff=0.12)
        lbl_near = Text("near mass\ng is large → time slow", font_size=13,
                        color=RED_D, line_spacing=1.2).next_to(face_near, RIGHT, buff=0.12)

        self.play(Create(face_far), Create(face_near),
                  Write(lbl_far), Write(lbl_near), run_time=1.5)

        clk_tracker = ValueTracker(0)
        hand_far  = always_redraw(lambda: clock_hand(CLK_FAR,  OMEGA_FAR,  clk_tracker))
        hand_near = always_redraw(lambda: clock_hand(CLK_NEAR, OMEGA_NEAR, clk_tracker))
        self.add(hand_far, hand_near)
        self.play(clk_tracker.animate.set_value(T_ANIM), run_time=T_ANIM, rate_func=linear)

        final = Text(
            "Matter tells the metric how to curve.\nThe curved metric tells matter how to move.",
            font_size=22, color=YELLOW, weight=BOLD, line_spacing=1.3,
        ).to_edge(DOWN, buff=0.28)
        self.play(Write(final), run_time=2.5)
        self.wait(3)
