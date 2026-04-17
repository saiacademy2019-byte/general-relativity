"""
Part 1 — Spacetime and World Lines
Manim Community scenes. No LaTeX required (uses pango/cairo Text throughout).
"""
from manim import *
import numpy as np

WLINE_COLOR = "#E07B54"
TAU_COLOR   = "#F5D040"
EARTH_COL   = "#3A7BD5"


# ══════════════════════════════════════════════════════════════════════════════
# Scene 1 — SpacetimeGrid  (2× slower)
# ══════════════════════════════════════════════════════════════════════════════
class SpacetimeGrid(Scene):
    def construct(self):
        title = Text("Part 1 — Spacetime & World Lines", font_size=44, weight=BOLD)
        self.play(Write(title), run_time=2)
        self.wait(0.8)
        self.play(FadeOut(title), run_time=1.5)

        ax = Axes(
            x_range=[0, 8, 1], y_range=[0, 5, 1],
            x_length=10, y_length=6,
            axis_config={"color": WHITE, "include_tip": True, "tip_length": 0.25},
        ).shift(LEFT * 0.4 + DOWN * 0.25)

        x_lbl = Text("t", font_size=38, color=YELLOW).next_to(ax.x_axis.get_right(), DOWN, buff=0.15)
        y_lbl = Text("r", font_size=38, color=BLUE_C).next_to(ax.y_axis.get_top(), LEFT, buff=0.15)

        plane = NumberPlane(
            x_range=[0, 8, 1], y_range=[0, 5, 1],
            x_length=10, y_length=6,
            background_line_style={"stroke_color": BLUE_D, "stroke_opacity": 0.75, "stroke_width": 2.0},
            axis_config={"stroke_opacity": 0},
        ).shift(LEFT * 0.4 + DOWN * 0.25)

        self.play(Create(ax), Write(x_lbl), Write(y_lbl), run_time=3)
        self.play(Create(plane), run_time=1.6)

        post_lines = VGroup(
            Text("Einstein's Postulates", font_size=21, color=YELLOW, weight=BOLD),
            Text("① Physics is the same in all inertial frames", font_size=17),
            Text("② Speed of light c is constant in all frames", font_size=17),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        box = SurroundingRectangle(post_lines, color=YELLOW, buff=0.2, stroke_width=1.5)
        post_grp = VGroup(box, post_lines).to_corner(UR, buff=0.35)
        self.play(FadeIn(post_grp, shift=LEFT * 0.3), run_time=2)
        self.wait(1.5)

        ev = Dot(ax.c2p(5, 3), color=RED, radius=0.11)
        ev_lbl = Text("event  (t, r)", font_size=22, color=RED).next_to(ev, UR, buff=0.1)
        self.play(GrowFromCenter(ev), Write(ev_lbl), run_time=2)

        cap1 = Text(
            "Every point in this grid is an EVENT — a location at a moment in time.",
            font_size=21,
        ).to_edge(DOWN, buff=0.30)
        self.play(Write(cap1), run_time=2)
        self.wait(2.5)
        self.play(FadeOut(cap1, ev, ev_lbl), run_time=1.5)

        cap2 = Text(
            "This 2-D sheet is SPACETIME  (1 space + 1 time dimension).",
            font_size=25, color=YELLOW,
        ).to_edge(DOWN, buff=0.30)
        self.play(Write(cap2), run_time=2)
        self.wait(3)
        self.wait(0.5)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 2 — WorldLine  (2× slower; equation raised above t-axis)
# ══════════════════════════════════════════════════════════════════════════════
class WorldLine(Scene):
    def construct(self):
        # Reduced y_length + upward shift leaves clear space below for equation
        ax = Axes(
            x_range=[0, 8, 1], y_range=[0, 4, 1],
            x_length=10, y_length=5.0,
            axis_config={"color": WHITE, "include_tip": True, "tip_length": 0.22},
        ).shift(UP * 0.3)

        x_lbl = Text("t", font_size=36, color=YELLOW).next_to(ax.x_axis.get_right(), DOWN, buff=0.15)
        y_lbl = Text("r", font_size=36, color=BLUE_C).next_to(ax.y_axis.get_top(), LEFT, buff=0.15)

        plane = NumberPlane(
            x_range=[0, 8, 1], y_range=[0, 4, 1],
            x_length=10, y_length=5.0,
            background_line_style={"stroke_color": BLUE_D, "stroke_opacity": 0.75, "stroke_width": 2.0},
            axis_config={"stroke_opacity": 0},
        ).shift(UP * 0.3)
        self.add(plane, ax, x_lbl, y_lbl)

        # World-line: oscillates between r≈0.8 and r≈3.2  (stays well inside [0,4])
        T_END = 7.5
        def wl_pos(t):
            r = 2.0 + 1.2 * np.sin(0.75 * t)
            return ax.c2p(t, r)

        tracker = ValueTracker(0)
        dot = Dot(wl_pos(0), color=WLINE_COLOR, radius=0.13)
        dot.add_updater(lambda m: m.move_to(wl_pos(tracker.get_value())))
        trace = TracedPath(dot.get_center, stroke_color=WLINE_COLOR, stroke_width=4)

        wl_title = Text("WORLD LINE", font_size=32, color=WLINE_COLOR, weight=BOLD)
        wl_title.to_edge(UP, buff=0.35)
        self.play(Write(wl_title), run_time=2)
        self.add(trace, dot)
        self.play(tracker.animate.set_value(T_END), run_time=10, rate_func=linear)
        dot.clear_updaters()

        # Proper-time tick marks
        n_ticks = 9
        t_vals  = np.linspace(0.4, T_END - 0.4, n_ticks)
        dt      = 0.06
        ticks_grp  = VGroup()
        labels_grp = VGroup()
        for i, tv in enumerate(t_vals):
            p1  = np.array(wl_pos(tv - dt))
            p2  = np.array(wl_pos(tv + dt))
            tan = (p2 - p1) / np.linalg.norm(p2 - p1)
            nrm = np.array([-tan[1], tan[0], 0])
            ctr = np.array(wl_pos(tv))
            ticks_grp.add(Line(ctr - 0.16 * nrm, ctr + 0.16 * nrm,
                               color=WHITE, stroke_width=2.5))
            lbl = Text(f"τ{i}", font_size=17, color=TAU_COLOR)
            lbl.move_to(ctr + 0.40 * nrm)
            labels_grp.add(lbl)

        self.play(Create(ticks_grp), run_time=1.6)
        self.play(Write(labels_grp), run_time=1.6)

        cap = Text(
            "Equal arc-length segments = equal PROPER TIME  τ  (the particle's own clock)",
            font_size=22, color=TAU_COLOR,
        ).to_edge(DOWN, buff=0.50)      # raised: 0.50 gives clearance above t-axis
        self.play(Write(cap), run_time=2)
        self.wait(2.5)
        self.play(FadeOut(cap), run_time=1.5)

        # Proper-time formula — positioned well above the t-axis
        eq   = Text("dτ²  =  dt²  −  dr²/c²", font_size=36)
        note = Text("(τ = proper time, the particle's own clock)", font_size=20, color=GRAY)
        VGroup(eq, note).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.55)
        self.play(Write(eq), FadeIn(note), run_time=2)
        self.wait(3)
        self.wait(0.5)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 3 — AppleFalling
#   • 1.5× slower
#   • "World Line" label pushed to upper-right of spacetime panel
#   • Velocity decomposition: orange = total 4-velocity (constant length),
#     yellow = dt/dτ component, blue = dr/dτ component
# ══════════════════════════════════════════════════════════════════════════════

_R0    = 3.6
_G     = 0.45
_T_END = 4.0
_EARTH_CTR  = np.array([-3.6, -2.4, 0])
_EARTH_RAD  = 0.55
_APPLE_HMAX = 2.5


def _r(t: float) -> float:
    return max(0.08, _R0 - 0.5 * _G * t ** 2)


def _apple_phys(t: float) -> np.ndarray:
    frac = _r(t) / _R0
    y    = _EARTH_CTR[1] + _EARTH_RAD + frac * _APPLE_HMAX
    return np.array([_EARTH_CTR[0], y, 0])


class AppleFalling(Scene):
    def construct(self):
        div = DashedLine(UP * 4, DOWN * 4, color=GRAY, stroke_opacity=0.4)
        self.add(div)

        lt = Text("Physical Space",    font_size=26).move_to(LEFT * 3.6 + UP * 3.5)
        rt = Text("Spacetime Diagram", font_size=26).move_to(RIGHT * 2.8 + UP * 3.5)
        self.add(lt, rt)

        # ── LEFT: earth + clock ───────────────────────────────────────────
        earth = Circle(radius=_EARTH_RAD, color=EARTH_COL, fill_opacity=0.85)
        earth.move_to(_EARTH_CTR)
        earth_lbl = Text("Earth", font_size=20, color=BLUE_C).next_to(earth, DOWN, buff=0.08)

        ck_ctr = np.array([-5.9, 0.6, 0])
        ck_face = Circle(radius=0.38, color=GRAY_C, stroke_width=2).move_to(ck_ctr)
        ck_lbl  = Text("clock", font_size=18, color=GRAY_C).next_to(ck_face, DOWN, buff=0.06)
        self.add(earth, earth_lbl, ck_face, ck_lbl)

        # ── RIGHT: spacetime axes ─────────────────────────────────────────
        ax = Axes(
            x_range=[0, _T_END, 1], y_range=[0, _R0, 1],
            x_length=5.5, y_length=5.0,
            axis_config={"color": WHITE, "include_tip": True, "tip_length": 0.18},
        ).move_to(RIGHT * 2.8 + DOWN * 0.3)

        x_lbl = Text("t", font_size=28, color=YELLOW).next_to(ax.x_axis.get_right(), DOWN, buff=0.12)
        y_lbl = Text("r", font_size=28, color=BLUE_C).next_to(ax.y_axis.get_top(),   LEFT, buff=0.12)
        self.play(Create(ax), Write(x_lbl), Write(y_lbl), run_time=1.5)

        # ── axis unit vectors (used for velocity decomposition) ───────────
        p_orig = np.array(ax.c2p(0, 0))
        t_hat  = np.array(ax.c2p(1, 0)) - p_orig   # scene vector for 1 t-unit
        r_hat  = np.array(ax.c2p(0, 1)) - p_orig   # scene vector for 1 r-unit

        VLEN = 0.70   # fixed display length of total 4-velocity arrow

        def tang_scene(t):
            drdt = -_G * min(t, _T_END * 0.99)
            v = t_hat + r_hat * drdt
            n = np.linalg.norm(v)
            return (v / n * VLEN) if n > 1e-10 else (t_hat / np.linalg.norm(t_hat) * VLEN)

        def st_pos(t):
            return np.array(ax.c2p(t, _r(t)))

        # ── tracker ───────────────────────────────────────────────────────
        tracker = ValueTracker(0)

        # ── apple + clock hand ────────────────────────────────────────────
        apple = Dot(_apple_phys(0), color=RED_D, radius=0.14)
        apple.add_updater(lambda m: m.move_to(_apple_phys(tracker.get_value())))

        def ck_tip(t):
            a = -t / _T_END * 2 * PI
            return ck_ctr + 0.30 * np.array([np.sin(a), np.cos(a), 0])

        ck_hand = Line(ck_ctr, ck_tip(0), color=WHITE, stroke_width=2)
        ck_hand.add_updater(lambda m: m.become(
            Line(ck_ctr, ck_tip(tracker.get_value()), color=WHITE, stroke_width=2)))

        t_disp = always_redraw(lambda: Text(
            f"t = {tracker.get_value():.1f}", font_size=22, color=YELLOW,
        ).next_to(earth, DOWN, buff=0.75))

        # ── spacetime trace ───────────────────────────────────────────────
        st_dot = Dot(st_pos(0), color=RED_D, radius=0.10)
        st_dot.add_updater(lambda m: m.move_to(st_pos(tracker.get_value())))
        trace = TracedPath(st_dot.get_center, stroke_color=WLINE_COLOR, stroke_width=4)

        # ── velocity decomposition arrows (always_redraw) ─────────────────
        def arr_total():
            t  = tracker.get_value()
            p0 = st_pos(t);  v = tang_scene(t)
            return Arrow(p0, p0 + v, color=WLINE_COLOR, buff=0,
                         stroke_width=2.5, max_tip_length_to_length_ratio=0.22)

        def arr_t_comp():
            t  = tracker.get_value()
            p0 = st_pos(t);  v = tang_scene(t)
            end = p0 + np.array([v[0], 0, 0])
            if np.linalg.norm(end - p0) < 0.04:
                return VGroup()
            return Arrow(p0, end, color=YELLOW, buff=0,
                         stroke_width=2, max_tip_length_to_length_ratio=0.25)

        def arr_r_comp():
            t  = tracker.get_value()
            p0 = st_pos(t);  v = tang_scene(t)
            start = p0 + np.array([v[0], 0, 0])
            end   = p0 + v
            if np.linalg.norm(end - start) < 0.04:
                return VGroup()
            return Arrow(start, end, color=BLUE_C, buff=0,
                         stroke_width=2, max_tip_length_to_length_ratio=0.25)

        v_total = always_redraw(arr_total)
        v_t     = always_redraw(arr_t_comp)
        v_r     = always_redraw(arr_r_comp)

        # ── static velocity legend (upper-right of spacetime panel) ──────
        legend = VGroup(
            VGroup(Line(ORIGIN, RIGHT * 0.35, color=WLINE_COLOR, stroke_width=2.5),
                   Text("|u| = const", font_size=15, color=WLINE_COLOR)).arrange(RIGHT, buff=0.08),
            VGroup(Line(ORIGIN, RIGHT * 0.35, color=YELLOW,      stroke_width=2),
                   Text("dt/dτ",       font_size=15, color=YELLOW)).arrange(RIGHT, buff=0.08),
            VGroup(Line(ORIGIN, RIGHT * 0.35, color=BLUE_C,      stroke_width=2),
                   Text("dr/dτ",       font_size=15, color=BLUE_C)).arrange(RIGHT, buff=0.08),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        legend.move_to(ax.c2p(_T_END * 0.55, _R0 * 0.88))

        # ── assemble & animate ────────────────────────────────────────────
        self.add(trace, st_dot, apple, ck_hand, t_disp, v_total, v_t, v_r, legend)
        self.wait(0.6)
        self.play(tracker.animate.set_value(_T_END), run_time=10.5, rate_func=linear)

        apple.clear_updaters()
        ck_hand.clear_updaters()
        st_dot.clear_updaters()

        # "World Line" label — placed in upper-right area of spacetime panel
        wl_lbl = Text("World Line", font_size=20, color=WLINE_COLOR, weight=BOLD)
        wl_lbl.move_to(ax.c2p(_T_END * 0.25, _R0 * 0.78))
        self.play(Write(wl_lbl), run_time=1.5)

        cap = Text(
            "The apple's history through space AND time = its WORLD LINE.",
            font_size=21,
        ).to_edge(DOWN, buff=0.25)
        self.play(Write(cap), run_time=1.5)
        self.wait(3)
        self.wait(0.5)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 4 — RestMotion  (redesigned)
#   Left panel : physical space — earth + apple sitting on top, clock ticking
#   Right panel: spacetime diagram — BOTH earth and apple trace horizontal
#                world lines moving right together (same dt/dτ = 1)
# ══════════════════════════════════════════════════════════════════════════════
class RestMotion(Scene):
    def construct(self):
        title = Text(
            "'At Rest' in Space  ≠  At Rest in Spacetime",
            font_size=34, weight=BOLD,
        ).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=2)
        self.wait(0.5)

        # ── panel divider ─────────────────────────────────────────────────
        div = DashedLine(UP * 3.8, DOWN * 4, color=GRAY, stroke_opacity=0.4)
        self.add(div)

        lt = Text("Physical Space",    font_size=24).move_to(LEFT * 3.5 + UP * 2.9)
        rt = Text("Spacetime Diagram", font_size=24).move_to(RIGHT * 2.8 + UP * 2.9)
        self.play(FadeIn(lt, rt), run_time=1)

        # ── LEFT: earth (large circle) + apple on top + clock ─────────────
        EARTH_POS  = LEFT * 3.5 + DOWN * 1.6
        EARTH_RAD  = 1.1
        APPLE_RAD  = 0.18

        earth_phys = Circle(radius=EARTH_RAD, color=EARTH_COL, fill_opacity=0.88)
        earth_phys.move_to(EARTH_POS)
        earth_lbl  = Text("Earth", font_size=20, color=BLUE_C)
        earth_lbl.next_to(earth_phys, DOWN, buff=0.10)

        apple_center_phys = EARTH_POS + UP * (EARTH_RAD + APPLE_RAD + 0.04)
        apple_phys = Circle(radius=APPLE_RAD, color=RED_D, fill_opacity=1.0)
        apple_phys.move_to(apple_center_phys)
        apple_lbl  = Text("apple", font_size=18, color=RED_D)
        apple_lbl.next_to(apple_phys, RIGHT, buff=0.10)

        # "r = const" annotation (vertical dashed line at their x position)
        r_ann = Text("r = const", font_size=18, color=GRAY)
        r_ann.next_to(apple_phys, LEFT, buff=0.6)

        # clock in left panel
        ck_ctr  = np.array([-6.1, 0.8, 0])
        ck_face = Circle(radius=0.36, color=GRAY_C, stroke_width=2).move_to(ck_ctr)
        ck_lbl  = Text("clock", font_size=17, color=GRAY_C).next_to(ck_face, DOWN, buff=0.06)

        self.play(
            FadeIn(earth_phys, earth_lbl, apple_phys, apple_lbl, r_ann,
                   ck_face, ck_lbl),
            run_time=1.5,
        )

        # ── RIGHT: spacetime axes ─────────────────────────────────────────
        T_TOTAL = 6.0
        R_MAX   = 4.0
        # Earth and apple r-positions in axis units
        R_EARTH = 1.2
        R_APPLE = 2.0   # apple sits above Earth (constant Δr = 0.8)

        ax = Axes(
            x_range=[0, T_TOTAL, 1], y_range=[0, R_MAX, 1],
            x_length=5.5, y_length=4.5,
            axis_config={"color": WHITE, "include_tip": True, "tip_length": 0.18},
        ).move_to(RIGHT * 2.8 + DOWN * 0.5)

        x_lbl = Text("t", font_size=28, color=YELLOW).next_to(ax.x_axis.get_right(), DOWN, buff=0.12)
        y_lbl = Text("r", font_size=28, color=BLUE_C).next_to(ax.y_axis.get_top(),   LEFT, buff=0.12)
        self.play(Create(ax), Write(x_lbl), Write(y_lbl), run_time=1.5)

        # ── world-line labels (static, at t=0 end of each line) ──────────
        e_wl_lbl = Text("Earth", font_size=17, color=EARTH_COL)
        e_wl_lbl.next_to(ax.c2p(0, R_EARTH), LEFT, buff=0.25)
        a_wl_lbl = Text("Apple", font_size=17, color=WLINE_COLOR)
        a_wl_lbl.next_to(ax.c2p(0, R_APPLE), LEFT, buff=0.25)
        self.play(FadeIn(e_wl_lbl, a_wl_lbl), run_time=1)

        # Δr double-headed arrow (static)
        dr_start = ax.c2p(0.35, R_EARTH)
        dr_end   = ax.c2p(0.35, R_APPLE)
        dr_arrow = DoubleArrow(dr_start, dr_end, color=WHITE,
                               buff=0, stroke_width=1.5, tip_length=0.12)
        dr_lbl   = Text("Δr = const", font_size=15, color=WHITE)
        dr_lbl.next_to(dr_arrow, LEFT, buff=0.08)
        self.play(FadeIn(dr_arrow, dr_lbl), run_time=1)

        # ── tracker ───────────────────────────────────────────────────────
        tracker = ValueTracker(0)

        # clock hand
        def ck_tip(t):
            a = -t / T_TOTAL * 2 * PI
            return ck_ctr + 0.28 * np.array([np.sin(a), np.cos(a), 0])

        ck_hand = Line(ck_ctr, ck_tip(0), color=WHITE, stroke_width=2)
        ck_hand.add_updater(lambda m: m.become(
            Line(ck_ctr, ck_tip(tracker.get_value()), color=WHITE, stroke_width=2)))

        # t readout below earth
        t_disp = always_redraw(lambda: Text(
            f"t = {tracker.get_value():.1f}", font_size=20, color=YELLOW,
        ).next_to(earth_lbl, DOWN, buff=0.15))

        # Earth world-line dot
        e_dot = Dot(ax.c2p(0, R_EARTH), color=EARTH_COL, radius=0.11)
        e_dot.add_updater(lambda m: m.move_to(ax.c2p(tracker.get_value(), R_EARTH)))
        e_trace = TracedPath(e_dot.get_center, stroke_color=EARTH_COL, stroke_width=3.5)

        # Apple world-line dot
        a_dot = Dot(ax.c2p(0, R_APPLE), color=RED_D, radius=0.11)
        a_dot.add_updater(lambda m: m.move_to(ax.c2p(tracker.get_value(), R_APPLE)))
        a_trace = TracedPath(a_dot.get_center, stroke_color=WLINE_COLOR, stroke_width=3.5)

        self.add(e_trace, a_trace, e_dot, a_dot, ck_hand, t_disp)
        self.wait(0.4)

        cap1 = Text(
            "Both are stationary in space — r = const for each.",
            font_size=22,
        ).to_edge(DOWN, buff=0.30)
        self.play(Write(cap1), run_time=1.5)

        self.play(tracker.animate.set_value(T_TOTAL), run_time=7, rate_func=linear)
        e_dot.clear_updaters()
        a_dot.clear_updaters()
        ck_hand.clear_updaters()

        self.play(FadeOut(cap1), run_time=1)
        cap2 = Text(
            "…but both carve WORLD LINES through spacetime as time advances!",
            font_size=22, color=YELLOW,
        ).to_edge(DOWN, buff=0.30)
        self.play(Write(cap2), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(cap2), run_time=1)

        # 4-velocity equation
        eq   = Text("g_μν u^μ u^ν = −c²", font_size=32)
        note = Text(
            "All objects move through spacetime at the same 'speed'  c.",
            font_size=21, color=GRAY,
        )
        VGroup(eq, note).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.35)
        self.play(Write(eq), FadeIn(note), run_time=2)
        self.wait(3)
        self.wait(0.5)
