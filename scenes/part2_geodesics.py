"""
Part 2 — Geodesics
5 scenes:
  GeodesicConcept       — flat vs curved surface, introduce geodesic
  SatelliteSpacetime    — orbit in physical space vs (t, φ) spacetime diagram
  CylinderStraightLine  — unrolled cylinder shows geodesic = straight line
  ParallelTransport     — flat vs curved parallel transport, holonomy
  GeodesicMath          — product-rule derivation of the geodesic equation
"""
from manim import *
import numpy as np

WLINE_COLOR = "#E07B54"
TAU_COLOR   = "#F5D040"
EARTH_COL   = "#3A7BD5"
GEO_COLOR   = "#50C878"    # emerald green — geodesic lines


# ══════════════════════════════════════════════════════════════════════════════
# Scene 1 — GeodesicConcept
# ══════════════════════════════════════════════════════════════════════════════
class GeodesicConcept(Scene):
    def construct(self):
        title = Text("Part 2 — Geodesics", font_size=44, weight=BOLD)
        self.play(Write(title), run_time=2); self.wait(0.6)
        self.play(FadeOut(title), run_time=1.5)

        div = DashedLine(UP * 3.8, DOWN * 4, color=GRAY, stroke_opacity=0.35)
        self.add(div)
        lt = Text("Flat surface",             font_size=24).move_to(LEFT * 3.5 + UP * 3.2)
        rt = Text("Curved surface  (sphere)", font_size=24).move_to(RIGHT * 3.0 + UP * 3.2)
        self.play(FadeIn(lt, rt), run_time=1.5)

        # ── Left: flat grid + dot tracing straight line ───────────────────
        flat_grid = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-2.5, 2.5, 1],
            x_length=5.5, y_length=4.8,
            background_line_style={"stroke_color": BLUE_D, "stroke_opacity": 0.75, "stroke_width": 2.0},
            axis_config={"stroke_opacity": 0},
        ).move_to(LEFT * 3.5 + DOWN * 0.3)
        self.play(Create(flat_grid), run_time=1.5)

        p0_f = np.array(flat_grid.c2p(-2.4, -1.5))
        p1_f = np.array(flat_grid.c2p( 2.4,  1.5))
        ref_flat = Line(p0_f, p1_f)
        dot_f  = Dot(p0_f, color=WHITE, radius=0.11)
        trace_f = TracedPath(dot_f.get_center, stroke_color=GEO_COLOR, stroke_width=4)
        self.add(trace_f, dot_f)
        self.play(MoveAlongPath(dot_f, ref_flat), run_time=3, rate_func=linear)
        flat_lbl = Text("geodesic = straight line", font_size=19, color=GEO_COLOR)
        flat_lbl.next_to(flat_grid, DOWN, buff=0.1)
        self.play(Write(flat_lbl), run_time=1)

        # ── Right: sphere + great circle ──────────────────────────────────
        sph_ctr = RIGHT * 3.0 + DOWN * 0.3
        sphere  = Circle(radius=1.9, color=BLUE_C, stroke_width=2).move_to(sph_ctr)
        equator = Ellipse(width=3.8, height=0.9, color=BLUE_E,
                          stroke_width=1.5, stroke_opacity=0.5).move_to(sph_ctr)
        self.play(Create(sphere), Create(equator), run_time=1.5)

        great = Ellipse(width=3.8, height=1.6, color=GEO_COLOR, stroke_width=4)
        great.move_to(sph_ctr).rotate(PI / 6)
        dot_s = Dot(great.point_from_proportion(0), color=WHITE, radius=0.11)
        self.add(dot_s)
        self.play(Create(great), MoveAlongPath(dot_s, great), run_time=4, rate_func=linear)
        sph_lbl = Text("geodesic = great circle", font_size=19, color=GEO_COLOR)
        sph_lbl.next_to(sphere, DOWN, buff=0.1)
        self.play(Write(sph_lbl), run_time=1)

        cap = Text(
            "Geodesic = the 'straightest possible path' on any surface.",
            font_size=24, color=GEO_COLOR,
        ).to_edge(DOWN, buff=0.30)
        self.play(Write(cap), run_time=2); self.wait(2)

        cap2 = Text(
            "In GR: freely falling objects follow GEODESICS in curved spacetime.",
            font_size=22, color=YELLOW,
        ).to_edge(DOWN, buff=0.30)
        self.play(ReplacementTransform(cap, cap2), run_time=1.5)
        self.wait(2.5); self.wait(0.5)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 2 — SatelliteSpacetime
# ══════════════════════════════════════════════════════════════════════════════
class SatelliteSpacetime(Scene):
    def construct(self):
        T_ORBIT   = 3.0      # animation seconds per orbit
        T_TOTAL   = 6.0      # two full orbits
        OMEGA     = 2*PI / T_ORBIT
        ORBIT_R   = 1.7
        EARTH_POS = LEFT * 3.5

        div = DashedLine(UP * 4, DOWN * 4, color=GRAY, stroke_opacity=0.35)
        self.add(div)
        lt = Text("Physical Space",     font_size=24).move_to(LEFT * 3.5 + UP * 3.4)
        rt = Text("Spacetime  (t, φ)",  font_size=24).move_to(RIGHT * 2.8 + UP * 3.4)
        self.add(lt, rt)

        # ── LEFT ──────────────────────────────────────────────────────────
        earth = Circle(radius=0.48, color=EARTH_COL, fill_opacity=0.9).move_to(EARTH_POS)
        earth_lbl = Text("Earth", font_size=18, color=BLUE_C).next_to(earth, DOWN, buff=0.08)
        orbit_ring = Circle(radius=ORBIT_R, color=GRAY_C,
                            stroke_width=1.5, stroke_opacity=0.5).move_to(EARTH_POS)
        phi_lbl = Text("φ", font_size=22, color=YELLOW)
        phi_lbl.move_to(EARTH_POS + RIGHT * (ORBIT_R + 0.45))
        self.play(FadeIn(earth, earth_lbl, orbit_ring, phi_lbl), run_time=1.5)

        # ── RIGHT: spacetime axes ─────────────────────────────────────────
        ax = Axes(
            x_range=[0, T_TOTAL, 1],
            y_range=[0, 4*PI, PI],
            x_length=5.5, y_length=5.0,
            axis_config={"color": WHITE, "include_tip": True, "tip_length": 0.18},
        ).move_to(RIGHT * 2.8 + DOWN * 0.3)
        x_lbl = Text("t", font_size=26, color=YELLOW).next_to(ax.x_axis.get_right(), DOWN, buff=0.12)
        y_lbl = Text("φ", font_size=26, color=YELLOW).next_to(ax.y_axis.get_top(),   LEFT, buff=0.12)
        lbl_2pi = Text("2π", font_size=15, color=GRAY).next_to(ax.c2p(0, 2*PI), LEFT, buff=0.08)
        lbl_4pi = Text("4π", font_size=15, color=GRAY).next_to(ax.c2p(0, 4*PI), LEFT, buff=0.08)
        dash_2pi = DashedLine(ax.c2p(0, 2*PI), ax.c2p(T_TOTAL, 2*PI),
                              color=GRAY, stroke_opacity=0.4, stroke_width=1.2)
        self.play(Create(ax), Write(x_lbl), Write(y_lbl), run_time=1.5)
        self.play(FadeIn(lbl_2pi, lbl_4pi, dash_2pi), run_time=1)

        # ── tracker drives both ───────────────────────────────────────────
        tracker = ValueTracker(0)

        def sat_pos(t):
            a = OMEGA * t
            return np.array([EARTH_POS[0] + ORBIT_R*np.cos(a), ORBIT_R*np.sin(a), 0])

        sat = Dot(sat_pos(0), color=RED_D, radius=0.13)
        sat.add_updater(lambda m: m.move_to(sat_pos(tracker.get_value())))

        st_dot = Dot(ax.c2p(0, 0), color=RED_D, radius=0.09)
        st_dot.add_updater(lambda m: m.move_to(
            ax.c2p(tracker.get_value(), OMEGA * tracker.get_value())))
        trace = TracedPath(st_dot.get_center, stroke_color=WLINE_COLOR, stroke_width=4)

        self.add(trace, st_dot, sat)
        cap = Text(
            "Circular orbit in space  →  straight line in (t, φ) spacetime.",
            font_size=22,
        ).to_edge(DOWN, buff=0.30)
        self.play(Write(cap), run_time=2)
        self.play(tracker.animate.set_value(T_TOTAL), run_time=8, rate_func=linear)
        sat.clear_updaters(); st_dot.clear_updaters()

        # label the world line
        mid_t = T_TOTAL * 0.55
        wl_lbl = Text("World line (straight!)", font_size=17, color=WLINE_COLOR, weight=BOLD)
        wl_lbl.move_to(ax.c2p(mid_t, OMEGA * mid_t * 0.85) + RIGHT * 0.5)
        self.play(Write(wl_lbl), run_time=1.5)
        self.wait(2); self.wait(0.5)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 3 — CylinderStraightLine
# ══════════════════════════════════════════════════════════════════════════════
class CylinderStraightLine(Scene):
    def construct(self):
        title = Text("Roll the Sheet into a Cylinder", font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=2)

        # ── Unrolled rectangle ────────────────────────────────────────────
        rect = Rectangle(width=5.8, height=3.4, color=BLUE_E, stroke_width=2)
        rect.shift(LEFT * 1.8 + DOWN * 0.5)

        x_lab = Text("φ  (0 → 2π)", font_size=20, color=YELLOW).next_to(rect, DOWN, buff=0.14)
        y_lab = Text("t",            font_size=22, color=YELLOW).next_to(rect, LEFT, buff=0.14)

        # Edge identification labels
        id_l = Text("φ = 0",  font_size=15, color=ORANGE).next_to(rect.get_left(),  LEFT,  buff=0.08)
        id_r = Text("φ = 2π", font_size=15, color=ORANGE).next_to(rect.get_right(), RIGHT, buff=0.08)
        eq_lbl = Text("≡  same!", font_size=16, color=ORANGE).next_to(id_r, RIGHT, buff=0.12)

        # Geodesic: straight diagonal line across the rectangle
        bl = rect.get_corner(DL) + RIGHT * 0.18 + UP * 0.18
        tr = rect.get_corner(UR) - RIGHT * 0.18 - UP * 0.18
        geo_line = Line(bl, tr, color=GEO_COLOR, stroke_width=4)
        geo_lbl  = Text("GEODESIC", font_size=17, color=GEO_COLOR, weight=BOLD)
        geo_lbl.next_to(geo_line.get_center(), UR, buff=0.10)

        self.play(Create(rect), Write(x_lab), Write(y_lab), run_time=2)
        self.play(FadeIn(id_l, id_r, eq_lbl), run_time=1.5)
        self.play(Create(geo_line), Write(geo_lbl), run_time=2)

        cap1 = Text(
            "On the flat (unrolled) sheet the geodesic is a straight line.",
            font_size=22,
        ).to_edge(DOWN, buff=0.42)
        self.play(Write(cap1), run_time=2); self.wait(2)
        self.play(FadeOut(cap1), run_time=1)

        cap2 = Text(
            "Now roll φ = 0 edge to meet φ = 2π  →  the sheet becomes a CYLINDER.",
            font_size=21,
        ).to_edge(DOWN, buff=0.42)
        self.play(Write(cap2), run_time=2); self.wait(1.5)

        # ── Stylised cylinder on the right ───────────────────────────────
        # Cylinder drawn in 2-D projection
        CX = 5.2;  CY = -0.5            # cylinder centre (scene coords)
        HW = 0.95; HH = 1.75            # half-width, half-height

        cyl_ctr = np.array([CX, CY, 0])
        cyl_l = Line(cyl_ctr + LEFT*HW + DOWN*HH, cyl_ctr + LEFT*HW  + UP*HH,
                     color=BLUE_E, stroke_width=2)
        cyl_r = Line(cyl_ctr + RIGHT*HW + DOWN*HH, cyl_ctr + RIGHT*HW + UP*HH,
                     color=BLUE_E, stroke_width=2)
        cyl_top = Ellipse(width=2*HW*2, height=0.46, color=BLUE_E, stroke_width=2)
        cyl_top.move_to(cyl_ctr + UP*HH)
        cyl_bot = Ellipse(width=2*HW*2, height=0.46, color=BLUE_E,
                          stroke_width=1.5, stroke_opacity=0.45)
        cyl_bot.move_to(cyl_ctr + DOWN*HH)

        # Helix on cylinder surface — sinusoidal in x, linear in y
        def helix_pt(s):
            x = CX + HW * np.sin(2 * 2*PI * s)
            y = CY - HH + 2*HH * s
            return np.array([x, y, 0])

        helix = ParametricFunction(helix_pt, t_range=[0, 1, 0.01],
                                   color=GEO_COLOR, stroke_width=3.5)

        roll_arrow = Arrow(np.array([rect.get_right()[0] + 0.15, CY, 0]),
                           np.array([CX - HW*2 - 0.15, CY, 0]),
                           color=YELLOW, stroke_width=2, buff=0.05, max_tip_length_to_length_ratio=0.2)
        roll_lbl = Text("roll up!", font_size=17, color=YELLOW)
        roll_lbl.move_to(np.array([(rect.get_right()[0] + CX - HW*2)/2, CY + 0.28, 0]))

        self.play(GrowArrow(roll_arrow), Write(roll_lbl), run_time=1.5)
        self.play(Create(cyl_l), Create(cyl_r), Create(cyl_top), Create(cyl_bot), run_time=2)
        self.play(Create(helix), run_time=2.5)

        helix_lbl = Text("same geodesic\n(now a helix)", font_size=15,
                         color=GEO_COLOR, line_spacing=1.2)
        helix_lbl.next_to(np.array([CX + HW + 0.1, CY, 0]), RIGHT, buff=0.1)
        self.play(Write(helix_lbl), run_time=1.5)

        self.play(FadeOut(cap2), run_time=1)
        cap3 = Text(
            "A geodesic is ALWAYS a straight line — in the right (unrolled) coordinates.",
            font_size=22, color=YELLOW,
        ).to_edge(DOWN, buff=0.42)
        self.play(Write(cap3), run_time=2)
        self.wait(2.5); self.wait(0.5)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 4 — ParallelTransport
# ══════════════════════════════════════════════════════════════════════════════
class ParallelTransport(Scene):
    def construct(self):
        title = Text("Parallel Transport", font_size=40, weight=BOLD)
        title.to_edge(UP, buff=0.40)
        self.play(Write(title), run_time=2)

        div = DashedLine(UP * 3.8, DOWN * 4, color=GRAY, stroke_opacity=0.35)
        self.add(div)
        lt = Text("Flat space",   font_size=24).move_to(LEFT * 3.5 + UP * 2.9)
        rt = Text("Curved space", font_size=24).move_to(RIGHT * 3.0 + UP * 2.9)
        self.play(FadeIn(lt, rt), run_time=1.5)

        T_ANIM    = 5.0
        ARROW_LEN = 0.58
        INIT_ANG  = PI / 4      # initial arrow angle (45° up-right)
        tracker   = ValueTracker(0)

        # ── Left: flat grid, straight path, constant arrow ────────────────
        flat_grid = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-2, 2, 1],
            x_length=5.5, y_length=4.5,
            background_line_style={"stroke_color": BLUE_D, "stroke_opacity": 0.75, "stroke_width": 2.0},
            axis_config={"stroke_opacity": 0},
        ).move_to(LEFT * 3.5 + DOWN * 0.3)
        self.play(Create(flat_grid), run_time=1)

        p0_f = np.array(flat_grid.c2p(-2.2, 0))
        p1_f = np.array(flat_grid.c2p( 2.2, 0))
        path_flat = Line(p0_f, p1_f, color=WHITE, stroke_width=2)
        self.play(Create(path_flat), run_time=1)

        def flat_pos():
            frac = tracker.get_value() / T_ANIM
            return p0_f + frac * (p1_f - p0_f)

        def flat_arrow():
            pos = flat_pos()
            end = pos + ARROW_LEN * np.array([np.cos(INIT_ANG), np.sin(INIT_ANG), 0])
            return Arrow(pos, end, color=GEO_COLOR, buff=0,
                         stroke_width=2.5, max_tip_length_to_length_ratio=0.30)

        dot_f2 = Dot(p0_f, color=WHITE, radius=0.11)
        dot_f2.add_updater(lambda m: m.move_to(flat_pos()))
        arr_flat = always_redraw(flat_arrow)
        self.add(dot_f2, arr_flat)

        # ── Right: circular loop on curved space, arrow rotates ───────────
        CURVE_CTR = RIGHT * 3.0 + DOWN * 0.3
        CIRC_R    = 1.55
        HOLONOMY  = -2 * PI / 3    # 120° rotation after one full loop

        # Suggest curved space with concentric ellipses
        sphere_bg = Circle(radius=1.9, color=BLUE_E, stroke_width=1.5, stroke_opacity=0.45)
        sphere_bg.move_to(CURVE_CTR)
        for sc in [0.55, 1.0, 1.45]:
            self.add(Ellipse(width=sc*2, height=sc*1.0, color=BLUE_E,
                             stroke_width=1, stroke_opacity=0.18).move_to(CURVE_CTR))
        self.add(sphere_bg)

        loop_path = Circle(radius=CIRC_R, color=WHITE, stroke_width=2).move_to(CURVE_CTR)
        self.play(Create(loop_path), run_time=1)

        def curved_pos():
            frac  = tracker.get_value() / T_ANIM
            angle = 2 * PI * frac
            return np.array([CURVE_CTR[0] + CIRC_R*np.cos(angle),
                             CURVE_CTR[1] + CIRC_R*np.sin(angle), 0])

        def curved_arrow():
            frac      = tracker.get_value() / T_ANIM
            pos       = curved_pos()
            arr_angle = INIT_ANG + HOLONOMY * frac
            end       = pos + ARROW_LEN * np.array([np.cos(arr_angle), np.sin(arr_angle), 0])
            return Arrow(pos, end, color=GEO_COLOR, buff=0,
                         stroke_width=2.5, max_tip_length_to_length_ratio=0.30)

        dot_c = Dot(curved_pos(), color=WHITE, radius=0.11)
        dot_c.add_updater(lambda m: m.move_to(curved_pos()))
        arr_curved = always_redraw(curved_arrow)
        self.add(dot_c, arr_curved)

        flat_note   = Text("Direction: preserved ✓",       font_size=19, color=GEO_COLOR)
        curved_note = Text("Direction: rotates  (holonomy!)", font_size=19, color=ORANGE)
        flat_note.next_to(flat_grid,  DOWN, buff=0.10)
        curved_note.next_to(sphere_bg, DOWN, buff=0.10)

        cap = Text(
            "Parallel transport: carry a vector without rotating it relative to the surface.",
            font_size=21,
        ).to_edge(DOWN, buff=0.42)
        self.play(Write(cap), run_time=2)
        self.play(tracker.animate.set_value(T_ANIM), run_time=7, rate_func=linear)
        dot_f2.clear_updaters()
        dot_c.clear_updaters()
        self.play(Write(flat_note), Write(curved_note), run_time=1.5)
        self.wait(1.5)
        self.play(FadeOut(cap), run_time=1)

        cap2 = Text(
            "Geodesic = path where the tangent vector IS its own parallel transport.",
            font_size=22, color=YELLOW,
        ).to_edge(DOWN, buff=0.42)
        self.play(Write(cap2), run_time=2)
        self.wait(2.5); self.wait(0.5)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 5 — GeodesicMath
#   Derives the geodesic equation step-by-step using the product rule,
#   matching the style of geodesics_1.png from the reference examples.
# ══════════════════════════════════════════════════════════════════════════════
class GeodesicMath(Scene):
    def construct(self):
        title = Text("Building the Geodesic Equation", font_size=37, weight=BOLD)
        title.to_edge(UP, buff=0.38)
        self.play(Write(title), run_time=2); self.wait(0.5)

        # ── Step definitions ──────────────────────────────────────────────
        # Each entry: (caption, equation, equation colour)
        steps = [
            (
                "A geodesic = the velocity vector v does not change:",
                "d / dτ  ( v )  =  0",
                WHITE,
            ),
            (
                "Write velocity in terms of components and basis vectors:",
                "v  =  vᵅ ēₐ",
                WHITE,
            ),
            (
                "Substitute and apply the product rule:",
                "d/dτ ( vᵅ ēₐ )  =  (dvᵅ/dτ) ēₐ  +  vᵅ (dēₐ/dτ)  =  0",
                YELLOW,
            ),
            (
                "Flat space:  dēₐ/dτ = 0  (basis vectors never change)",
                "  →   dvᵅ/dτ = 0       constant velocity  ✓",
                GEO_COLOR,
            ),
            (
                "Curved space:  dēₐ/dτ ≠ 0  (basis rotates as you move)",
                "  →   vᵅ (dēₐ/dτ) term  =  the gravitational correction",
                WLINE_COLOR,
            ),
            (
                "The Christoffel symbols  Γ  (Part 3) encode exactly  dēₐ/dτ :",
                "dvᵅ/dτ  +  Γᵅₐβ vᵅ v^β  =  0        ← Geodesic Equation",
                TAU_COLOR,
            ),
        ]

        # Pre-build all step VGroups and stack them
        step_groups = VGroup()
        for caption, eq, col in steps:
            cap_txt = Text(caption, font_size=17, color=GRAY)
            eq_txt  = Text(eq, font_size=21, color=col, weight=BOLD)
            grp = VGroup(cap_txt, eq_txt).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
            step_groups.add(grp)

        step_groups.arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        step_groups.next_to(title, DOWN, buff=0.28)
        step_groups.to_edge(LEFT, buff=0.55)

        # Animate each step in sequence
        for i, grp in enumerate(step_groups):
            self.play(FadeIn(grp[0], shift=RIGHT * 0.15), run_time=1.0)
            self.play(Write(grp[1]), run_time=1.6)
            self.wait(1.2)

        # Box the final geodesic equation
        final_box = SurroundingRectangle(step_groups[-1][1],
                                         color=TAU_COLOR, buff=0.14, stroke_width=2)
        self.play(Create(final_box), run_time=1.5)

        cap_final = Text(
            "The Γ term IS gravity.  Curved spacetime  →  objects follow curved paths.",
            font_size=21, color=YELLOW,
        ).to_edge(DOWN, buff=0.28)
        self.play(Write(cap_final), run_time=2)
        self.wait(3); self.wait(0.5)
