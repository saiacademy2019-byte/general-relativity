"""
Part 5 — Curvature
4 scenes:
  CurvatureConcept      — parallel transport: flat vs sphere, arrow returns rotated
  CurvatureAndRiemann   — sphere 3D: Christoffel frame tilt + Riemann loop test (no equations)
  RicciAndScalar        — contraction ladder; sphere R = 2/r²
  SchwarzschildMetric   — Earth + warped grid + Schwarzschild metric matrix
"""
from manim import *
import numpy as np

CURV_COL     = "#F5D040"   # yellow — curvature
RIEMANN_COL  = "#C77DFF"   # purple — Riemann / Ricci
CHRISTOF_COL = "#50C878"   # green  — Christoffel
EINST_COL    = "#FF6B6B"   # red    — Einstein / Schwarzschild
SCHWARZ_COL  = "#3ABEFF"   # cyan   — Schwarzschild metric entries


# ══════════════════════════════════════════════════════════════════════════════
# Scene 1 — CurvatureConcept
# ══════════════════════════════════════════════════════════════════════════════
class CurvatureConcept(Scene):
    def construct(self):
        title = Text("What Is Curvature?", font_size=40, weight=BOLD)
        title.to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=1.5)

        # ── LEFT: flat square loop ────────────────────────────────────────────
        flat_lbl = Text("Flat surface", font_size=22, color=BLUE_D)
        flat_lbl.move_to(LEFT * 3.5 + UP * 1.5)
        self.play(FadeIn(flat_lbl), run_time=0.8)

        sq = Square(side_length=2.4, color=BLUE_D, stroke_width=2)
        sq.move_to(LEFT * 3.5 + DOWN * 0.5)
        self.play(Create(sq), run_time=1.2)

        bl = sq.get_corner(DL)
        arr_flat = Arrow(bl, bl + RIGHT * 0.7, color=CURV_COL,
                         buff=0, stroke_width=3,
                         max_tip_length_to_length_ratio=0.28)
        self.play(GrowArrow(arr_flat), run_time=0.8)

        corners = [sq.get_corner(DR), sq.get_corner(UR),
                   sq.get_corner(UL), sq.get_corner(DL)]
        for corner in corners:
            new_arr = Arrow(corner, corner + RIGHT * 0.7, color=CURV_COL,
                            buff=0, stroke_width=3,
                            max_tip_length_to_length_ratio=0.28)
            self.play(Transform(arr_flat, new_arr), run_time=0.5)

        flat_ok = Text("Arrow returns unchanged ✓", font_size=18, color=BLUE_D)
        flat_ok.next_to(sq, DOWN, buff=0.18)
        self.play(Write(flat_ok), run_time=1)

        # ── RIGHT: sphere loop ────────────────────────────────────────────────
        curv_lbl = Text("Curved surface (sphere)", font_size=22, color=ORANGE)
        curv_lbl.move_to(RIGHT * 3.0 + UP * 1.5)
        self.play(FadeIn(curv_lbl), run_time=0.8)

        cx, cy, R = 3.0, -0.5, 1.3
        def arc_pt(theta):
            return np.array([cx + R * np.cos(theta), cy + R * np.sin(theta), 0])

        t0, t1, t2 = np.radians(270), np.radians(30), np.radians(150)
        v0, v1, v2 = arc_pt(t0), arc_pt(t1), arc_pt(t2)
        ctr = np.array([cx, cy, 0])

        arc01 = Arc(radius=R, start_angle=t0, angle=(t1-t0),   arc_center=ctr, color=ORANGE, stroke_width=2.5)
        arc12 = Arc(radius=R, start_angle=t1, angle=(t2-t1),   arc_center=ctr, color=ORANGE, stroke_width=2.5)
        arc20 = Arc(radius=R, start_angle=t2, angle=(t0-t2+TAU), arc_center=ctr, color=ORANGE, stroke_width=2.5)
        self.play(Create(arc01), Create(arc12), Create(arc20), run_time=1.5)

        arr_curv = Arrow(v0, v0+RIGHT*0.65, color=CURV_COL, buff=0, stroke_width=3,
                         max_tip_length_to_length_ratio=0.28)
        self.play(GrowArrow(arr_curv), run_time=0.8)

        # transport: v0→v1 (arrow now UP), v1→v2 (still UP), v2→v0 (back but now UP)
        for pos, direction in [(v1, UP), (v2, UP), (v0, UP)]:
            a = Arrow(pos, pos + direction*0.65, color=CURV_COL, buff=0, stroke_width=3,
                      max_tip_length_to_length_ratio=0.28)
            self.play(Transform(arr_curv, a), run_time=0.65)

        # Show final arrow is RED (different from start)
        a_final = Arrow(v0, v0+UP*0.65, color=RED, buff=0, stroke_width=3,
                        max_tip_length_to_length_ratio=0.28)
        self.play(Transform(arr_curv, a_final), run_time=0.4)

        # Ghost of original direction
        ghost = Arrow(v0, v0+RIGHT*0.65, color=CURV_COL, buff=0, stroke_width=2,
                      stroke_opacity=0.4, max_tip_length_to_length_ratio=0.28)
        self.play(FadeIn(ghost), run_time=0.4)

        curv_warn = Text("Arrow ROTATED — space is curved!", font_size=18, color=RED)
        curv_warn.next_to(arc20, DOWN, buff=0.28)
        self.play(Write(curv_warn), run_time=1)

        punchline = Text(
            "Curvature = failure of directions to fit together\nwhen you travel around a closed loop",
            font_size=23, color=CURV_COL
        )
        punchline.to_edge(DOWN, buff=0.35)
        self.play(Write(punchline), run_time=2.5)
        self.wait(2)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 2 — CurvatureAndRiemann
#   Left panel: sphere with basis arrows tilting at different positions
#               (Christoffel intuition — frame changes as you move)
#   Right panel: sphere with a triangle loop; arrow returns rotated
#                (Riemann — only TRUE curvature survives)
#   No equations anywhere.
# ══════════════════════════════════════════════════════════════════════════════
class CurvatureAndRiemann(Scene):
    def _draw_sphere(self, cx, cy, R, color):
        ctr = np.array([cx, cy, 0])
        outline = Circle(radius=R, color=color, stroke_width=2.5).move_to(ctr)
        eq = Ellipse(width=R*2, height=R*0.4, color=color,
                     stroke_opacity=0.45, stroke_width=1.5).move_to(ctr)
        m1 = Arc(radius=R, start_angle=PI/2, angle=PI,
                 arc_center=ctr, color=color, stroke_opacity=0.3, stroke_width=1.2)
        return VGroup(outline, eq, m1)

    def construct(self):
        title = Text("How Curvature Is Detected", font_size=38, weight=BOLD)
        title.to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=1.5)

        div = DashedLine(UP*2.8, DOWN*3.8, color=GRAY, stroke_opacity=0.3)
        self.add(div)

        # ── LEFT: Christoffel — frame tilts as you move ───────────────────────
        lbl_l = Text("Local frames tilt on a curved surface", font_size=20, color=CHRISTOF_COL)
        lbl_l.move_to(LEFT*3.4 + UP*1.7)

        sph_l = self._draw_sphere(-3.4, -0.2, 1.5, BLUE_D)
        self.play(FadeIn(lbl_l), Create(sph_l), run_time=1.5)

        # Draw arrows at 4 positions on the sphere equator, each showing
        # a local radial + tangential basis that tilts with position
        cx_l, cy_l = -3.4, -0.2
        for angle_deg in [0, 90, 180, 270]:
            a  = np.radians(angle_deg)
            r  = 1.5
            pos = np.array([cx_l + r*np.cos(a), cy_l + r*np.sin(a), 0])
            # radial (points away from centre)
            er  = Arrow(pos - 0.4*np.array([np.cos(a), np.sin(a), 0]),
                        pos + 0.35*np.array([np.cos(a), np.sin(a), 0]),
                        color=CHRISTOF_COL, buff=0, stroke_width=2.5,
                        max_tip_length_to_length_ratio=0.35)
            # tangential (90° to radial)
            et  = Arrow(pos,
                        pos + 0.45*np.array([-np.sin(a), np.cos(a), 0]),
                        color=ORANGE, buff=0, stroke_width=2.5,
                        max_tip_length_to_length_ratio=0.35)
            self.play(GrowArrow(er), GrowArrow(et), run_time=0.4)

        christof_note = Text(
            "Γ: the rate at which your\nlocal compass tilts as you move",
            font_size=18, color=CHRISTOF_COL
        )
        christof_note.move_to(LEFT*3.4 + DOWN*2.1)
        self.play(Write(christof_note), run_time=1.5)

        warn = Text("Γ ≠ 0 alone does NOT prove real curvature",
                    font_size=17, color=GRAY)
        warn.next_to(christof_note, DOWN, buff=0.14)
        self.play(FadeIn(warn), run_time=1)

        # ── RIGHT: Riemann — carry vector around a loop, see if it rotates ────
        lbl_r = Text("Carry a vector around a loop — does it rotate?", font_size=20, color=RIEMANN_COL)
        lbl_r.move_to(RIGHT*3.0 + UP*1.7)

        sph_r = self._draw_sphere(3.0, -0.2, 1.5, BLUE_D)
        self.play(FadeIn(lbl_r), Create(sph_r), run_time=1.5)

        cx_r, cy_r, R2 = 3.0, -0.2, 1.5
        ctr_r = np.array([cx_r, cy_r, 0])

        def arc_pt2(theta):
            return np.array([cx_r + R2*np.cos(theta), cy_r + R2*np.sin(theta), 0])

        tN  = np.radians(90)   # north pole
        tER = np.radians(0)    # equator right
        tEL = np.radians(180)  # equator left

        vN2  = arc_pt2(tN)
        vER2 = arc_pt2(tER)
        vEL2 = arc_pt2(tEL)

        loop1 = Arc(radius=R2, start_angle=tN,  angle=(tER-tN+TAU) % TAU - TAU,
                    arc_center=ctr_r, color=CURV_COL, stroke_width=2.5)
        # North to East is -90 degrees
        loop1 = Arc(radius=R2, start_angle=tN, angle=-PI/2,
                    arc_center=ctr_r, color=CURV_COL, stroke_width=2.5)
        loop2 = Arc(radius=R2, start_angle=tER, angle=PI/2,
                    arc_center=ctr_r, color=CURV_COL, stroke_width=2.5)
        # North back to EL is a straight horizontal line (meridian through back)
        loop3 = Line(vEL2, vN2, color=CURV_COL, stroke_width=2.5)

        self.play(Create(loop1), Create(loop2), Create(loop3), run_time=1.5)

        # Starting arrow at north pole: pointing RIGHT
        v_r = Arrow(vN2, vN2+RIGHT*0.6, color=CURV_COL, buff=0, stroke_width=3,
                    max_tip_length_to_length_ratio=0.28)
        self.play(GrowArrow(v_r), run_time=0.8)

        # Transport N→ER: arrow is now pointing DOWN
        v_r2 = Arrow(vER2, vER2+DOWN*0.6, color=CURV_COL, buff=0, stroke_width=3,
                     max_tip_length_to_length_ratio=0.28)
        self.play(Transform(v_r, v_r2), run_time=0.7)

        # Transport ER→EL: arrow still pointing DOWN (along equator)
        v_r3 = Arrow(vEL2, vEL2+DOWN*0.6, color=CURV_COL, buff=0, stroke_width=3,
                     max_tip_length_to_length_ratio=0.28)
        self.play(Transform(v_r, v_r3), run_time=0.7)

        # Transport EL back to N: arrow now points LEFT (90° rotation from start!)
        v_r4 = Arrow(vN2, vN2+LEFT*0.6, color=RED, buff=0, stroke_width=3,
                     max_tip_length_to_length_ratio=0.28)
        self.play(Transform(v_r, v_r4), run_time=0.7)

        ghost_r = Arrow(vN2, vN2+RIGHT*0.6, color=CURV_COL, buff=0, stroke_width=2,
                        stroke_opacity=0.4, max_tip_length_to_length_ratio=0.28)
        self.play(FadeIn(ghost_r), run_time=0.4)

        riemann_note = Text(
            "Rotation = the Riemann tensor\nCannot be removed by any coordinate trick",
            font_size=18, color=RIEMANN_COL
        )
        riemann_note.move_to(RIGHT*3.0 + DOWN*2.1)
        self.play(Write(riemann_note), run_time=1.5)

        self.wait(2)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 3 — RicciAndScalar
# ══════════════════════════════════════════════════════════════════════════════
class RicciAndScalar(Scene):
    def construct(self):
        title = Text("Ricci Tensor & Ricci Scalar", font_size=38, weight=BOLD)
        title.to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=1.5)

        sub = Text("Compressing the Riemann tensor to something simpler",
                   font_size=21, color=GRAY)
        sub.next_to(title, DOWN, buff=0.18)
        self.play(FadeIn(sub), run_time=1)

        ladder_items = [
            ("Riemann tensor",  "R^ρ_σμν", RIEMANN_COL, "Full curvature — every detail"),
            ("Ricci tensor",    "R_μν",     RIEMANN_COL, "Does a cloud of particles shrink or grow?"),
            ("Ricci scalar",    "R",        CURV_COL,    "One number: how curved is this point?"),
        ]

        y_positions = [1.1, 0.0, -1.1]
        for i, (label, formula, col, desc) in enumerate(ladder_items):
            rect = RoundedRectangle(width=9.2, height=0.82, corner_radius=0.18,
                                    color=col, stroke_width=1.5,
                                    fill_color=BLACK, fill_opacity=0.55)
            rect.move_to(np.array([0, y_positions[i], 0]))
            t_lbl  = Text(label,   font_size=20, color=WHITE)
            t_form = Text(formula, font_size=20, color=col, weight=BOLD)
            t_desc = Text(desc,    font_size=17, color=GRAY)
            t_lbl .move_to(rect.get_center() + LEFT*3.3)
            t_form.move_to(rect.get_center() + LEFT*0.9)
            t_desc.move_to(rect.get_center() + RIGHT*2.4)
            self.play(Create(rect), FadeIn(t_lbl), FadeIn(t_form), FadeIn(t_desc), run_time=0.9)
            if i < 2:
                arr = Arrow(np.array([0, y_positions[i]-0.41, 0]),
                            np.array([0, y_positions[i+1]+0.41, 0]),
                            color=GRAY, buff=0, stroke_width=1.5,
                            max_tip_length_to_length_ratio=0.5)
                ctr_lbl = Text("compress", font_size=14, color=GRAY)
                ctr_lbl.next_to(arr, RIGHT, buff=0.1)
                self.play(GrowArrow(arr), FadeIn(ctr_lbl), run_time=0.55)

        self.wait(0.5)

        # ── Sphere example ────────────────────────────────────────────────────
        ex_bar = Text("Concrete example: a sphere of radius r",
                      font_size=21, color=ORANGE)
        ex_bar.move_to(DOWN*2.05)
        self.play(Write(ex_bar), run_time=1)
        self.wait(0.4)

        # Fade ladder, bring in sphere + matrix
        self.play(FadeOut(sub), run_time=0.6)

        # Sphere (left)
        cx, cy = -3.2, -0.3
        sph = Circle(radius=1.55, color=BLUE_D, stroke_width=2.5).move_to(np.array([cx,cy,0]))
        eq  = Ellipse(width=3.1, height=0.52, color=BLUE_D,
                      stroke_opacity=0.45, stroke_width=1.5).move_to(np.array([cx,cy,0]))
        lon = Arc(radius=1.55, start_angle=PI/2, angle=PI,
                  arc_center=np.array([cx,cy,0]),
                  color=BLUE_D, stroke_opacity=0.35, stroke_width=1.2)
        t_theta = Text("θ", font_size=26, color=BLUE).move_to(np.array([cx-1.55, cy+0.4, 0]))
        t_phi   = Text("φ", font_size=26, color=RED ).move_to(np.array([cx+0.2,  cy+0.3, 0]))
        arc_th  = Arc(radius=0.5, start_angle=PI/2, angle=PI/2,
                      arc_center=np.array([cx,cy,0]), color=BLUE, stroke_width=2)
        arc_ph  = Arc(radius=1.55, start_angle=PI/2, angle=PI/3,
                      arc_center=np.array([cx,cy,0]), color=RED, stroke_width=2.5)

        self.play(Create(sph), Create(eq), Create(lon),
                  Create(arc_th), Create(arc_ph),
                  FadeIn(t_theta), FadeIn(t_phi), run_time=1.5)

        # Metric matrix (right)
        panel = RoundedRectangle(width=5.6, height=4.4, corner_radius=0.22,
                                 color=RIEMANN_COL, stroke_width=1.5,
                                 fill_color="#0A0A1A", fill_opacity=0.92)
        panel.move_to(RIGHT*2.8 + DOWN*0.3)
        self.play(Create(panel), run_time=0.8)

        m_lbl = Text("Metric on 2-sphere:", font_size=20, color=WHITE)
        m_lbl.move_to(RIGHT*2.8 + UP*1.68)
        self.play(FadeIn(m_lbl), run_time=0.6)

        dth_h = Text("dθ",       font_size=19, color=BLUE).move_to(RIGHT*1.6 + UP*0.85)
        dph_h = Text("dφ",       font_size=19, color=RED ).move_to(RIGHT*3.55+ UP*0.85)
        dth_r = Text("dθ",       font_size=19, color=BLUE).move_to(RIGHT*0.6 + UP*0.15)
        dph_r = Text("dφ",       font_size=19, color=RED ).move_to(RIGHT*0.6 + DOWN*0.95)
        e00   = Text("r²",       font_size=21, color=WHITE).move_to(RIGHT*1.6 + UP*0.15)
        e01   = Text("0",        font_size=21, color=GRAY ).move_to(RIGHT*3.55+ UP*0.15)
        e10   = Text("0",        font_size=21, color=GRAY ).move_to(RIGHT*1.6 + DOWN*0.95)
        e11   = Text("r²cos²θ",  font_size=21, color=WHITE).move_to(RIGHT*3.55+ DOWN*0.95)

        brk_lx, brk_rx = RIGHT*1.02, RIGHT*4.18
        brk_ty, brk_by = UP*0.54, DOWN*1.34
        tk = 0.17
        brac_l = VGroup(
            Line(brk_lx+brk_ty, brk_lx+brk_ty+RIGHT*tk, color=WHITE, stroke_width=2),
            Line(brk_lx+brk_ty, brk_lx+brk_by,          color=WHITE, stroke_width=2),
            Line(brk_lx+brk_by, brk_lx+brk_by+RIGHT*tk, color=WHITE, stroke_width=2),
        )
        brac_r = VGroup(
            Line(brk_rx+brk_ty, brk_rx+brk_ty+LEFT*tk,  color=WHITE, stroke_width=2),
            Line(brk_rx+brk_ty, brk_rx+brk_by,          color=WHITE, stroke_width=2),
            Line(brk_rx+brk_by, brk_rx+brk_by+LEFT*tk,  color=WHITE, stroke_width=2),
        )

        self.play(FadeIn(dth_h), FadeIn(dph_h), FadeIn(dth_r), FadeIn(dph_r), run_time=0.7)
        self.play(Write(e00), Write(e01), Write(e10), Write(e11),
                  Create(brac_l), Create(brac_r), run_time=1.4)

        scalar_box = RoundedRectangle(width=3.1, height=0.85, corner_radius=0.18,
                                      color=CURV_COL, stroke_width=2,
                                      fill_color=BLACK, fill_opacity=0.75)
        scalar_box.move_to(RIGHT*2.8 + DOWN*2.45)
        scalar_txt = Text("R = 2/r²", font_size=28, color=CURV_COL, weight=BOLD)
        scalar_txt.move_to(scalar_box.get_center())
        scalar_sub = Text("Ricci scalar — single-number curvature", font_size=16, color=GRAY)
        scalar_sub.next_to(scalar_box, DOWN, buff=0.12)
        self.play(Create(scalar_box), Write(scalar_txt), run_time=1.2)
        self.play(FadeIn(scalar_sub), run_time=0.8)

        note = Text("Larger sphere → smaller R → flatter.\nFlat space → R = 0.",
                    font_size=18, color=GRAY)
        note.move_to(LEFT*3.2 + DOWN*2.6)
        self.play(Write(note), run_time=1.5)
        self.wait(2)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 4 — SchwarzschildMetric
#   Act 1 — flat grid with Earth dot placed at centre-left
#   Act 2 — grid warps toward Earth (apply_function)
#   Act 3 — Schwarzschild metric matrix revealed on right
#   Act 4 — highlight g_tt and g_rr with physical interpretation
# ══════════════════════════════════════════════════════════════════════════════
class SchwarzschildMetric(Scene):
    def construct(self):
        title = Text("Earth's Spacetime — the Schwarzschild Metric",
                     font_size=32, weight=BOLD, color=EINST_COL)
        title.to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=1.5)

        earth_pos = np.array([-4.0, -0.4, 0])

        # ── ACT 1: flat grid ──────────────────────────────────────────────────
        grid = NumberPlane(
            x_range=[-7, 2, 1], y_range=[-4, 3.5, 1],
            x_length=13, y_length=7.5,
            background_line_style={"stroke_color": BLUE_D,
                                   "stroke_opacity": 0.75, "stroke_width": 2.0},
            axis_config={"stroke_opacity": 0},
        )
        self.play(Create(grid), run_time=1.5)

        # Earth circle
        earth = Circle(radius=0.38, fill_color=BLUE_E, fill_opacity=1,
                       stroke_color=WHITE, stroke_width=1.5)
        earth.move_to(earth_pos)
        earth_lbl = Text("M", font_size=18, color=WHITE, weight=BOLD)
        earth_lbl.move_to(earth_pos)
        self.play(FadeIn(earth), FadeIn(earth_lbl), run_time=0.8)

        flat_note = Text("Flat spacetime: uniform grid everywhere", font_size=20, color=GRAY)
        flat_note.to_edge(DOWN, buff=0.38)
        self.play(FadeIn(flat_note), run_time=0.8)
        self.wait(0.8)

        # ── ACT 2: warp grid toward Earth ─────────────────────────────────────
        self.play(FadeOut(flat_note), run_time=0.5)

        ex, ey = earth_pos[0], earth_pos[1]
        def warp(p):
            dp = np.array([p[0]-ex, p[1]-ey, 0])
            r  = np.linalg.norm(dp[:2])
            if r < 0.18:
                return np.array([ex, ey, 0])
            # Pull toward Earth; strength falls off with distance
            strength = 1.1
            factor   = r / (r + strength)
            new_xy   = np.array([ex, ey]) + dp[:2] * factor
            return np.array([new_xy[0], new_xy[1], p[2]])

        warped_grid = grid.copy()
        warped_grid.apply_function(warp)

        warp_note = Text("Mass M bends the grid — spacetime is no longer flat",
                         font_size=20, color=ORANGE)
        warp_note.to_edge(DOWN, buff=0.38)

        self.play(
            Transform(grid, warped_grid),
            FadeIn(warp_note),
            run_time=2.5
        )
        self.wait(0.8)

        # ── ACT 3: Schwarzschild metric matrix ───────────────────────────────
        self.play(FadeOut(warp_note), run_time=0.5)

        panel = RoundedRectangle(width=5.8, height=5.2, corner_radius=0.25,
                                 color=EINST_COL, stroke_width=1.8,
                                 fill_color="#100010", fill_opacity=0.94)
        panel.move_to(RIGHT*3.2 + DOWN*0.2)
        self.play(Create(panel), run_time=0.8)

        # Column/row headers
        headers = ["t", "r", "θ", "φ"]
        hcolors = [SCHWARZ_COL, RED, RED, RED]
        col_xs  = [RIGHT*1.55, RIGHT*2.45, RIGHT*3.40, RIGHT*4.40]
        row_ys  = [UP*0.55, DOWN*0.10, DOWN*0.75, DOWN*1.45]

        for i, (h, c, x) in enumerate(zip(headers, hcolors, col_xs)):
            t = Text(h, font_size=19, color=c, weight=BOLD).move_to(x + UP*1.38)
            self.add(t)
        for i, (h, c, y) in enumerate(zip(headers, hcolors, row_ys)):
            t = Text(h, font_size=19, color=c, weight=BOLD).move_to(RIGHT*0.88 + y)
            self.add(t)

        # Matrix entries  (row, col) → (i, j)
        entries_data = [
            # row 0 (t)
            [("c²-2GM/r",          SCHWARZ_COL, 17), ("0", GRAY, 20), ("0", GRAY, 20), ("0", GRAY, 20)],
            # row 1 (r)
            [("0", GRAY, 20), ("-1/(1-2GM/rc²)", SCHWARZ_COL, 14), ("0", GRAY, 20), ("0", GRAY, 20)],
            # row 2 (θ)
            [("0", GRAY, 20), ("0", GRAY, 20), ("-r²", SCHWARZ_COL, 20), ("0", GRAY, 20)],
            # row 3 (φ)
            [("0", GRAY, 20), ("0", GRAY, 20), ("0", GRAY, 20), ("-r²sin²θ", SCHWARZ_COL, 17)],
        ]

        entry_mobjs = []
        for i, row in enumerate(entries_data):
            for j, (txt, col, sz) in enumerate(row):
                m = Text(txt, font_size=sz, color=col)
                m.move_to(col_xs[j] + row_ys[i])
                entry_mobjs.append(m)

        # Bracket lines around the 4×4 block
        bx_l = RIGHT*1.16;  bx_r = RIGHT*4.78
        by_t = UP*0.86;     by_b = DOWN*1.78
        tk   = 0.17
        brac_l = VGroup(
            Line(bx_l+by_t, bx_l+by_t+RIGHT*tk, color=WHITE, stroke_width=2),
            Line(bx_l+by_t, bx_l+by_b,           color=WHITE, stroke_width=2),
            Line(bx_l+by_b, bx_l+by_b+RIGHT*tk, color=WHITE, stroke_width=2),
        )
        brac_r = VGroup(
            Line(bx_r+by_t, bx_r+by_t+LEFT*tk,  color=WHITE, stroke_width=2),
            Line(bx_r+by_t, bx_r+by_b,           color=WHITE, stroke_width=2),
            Line(bx_r+by_b, bx_r+by_b+LEFT*tk,  color=WHITE, stroke_width=2),
        )

        self.play(*[Write(m) for m in entry_mobjs],
                  Create(brac_l), Create(brac_r), run_time=2)
        self.wait(0.6)

        # ── ACT 4: highlight and explain key entries ──────────────────────────
        # Highlight g_tt
        box_tt = SurroundingRectangle(entry_mobjs[0], color=CURV_COL, buff=0.08)
        ann_tt = Text("Time slows near M\n(gravitational time dilation)",
                      font_size=16, color=CURV_COL)
        ann_tt.next_to(panel, DOWN, buff=0.22)
        self.play(Create(box_tt), Write(ann_tt), run_time=1.2)
        self.wait(1.2)

        # Highlight g_rr
        box_rr = SurroundingRectangle(entry_mobjs[5], color=ORANGE, buff=0.08)
        ann_rr = Text("Radial distances stretch near M\n(space is compressed)",
                      font_size=16, color=ORANGE)
        ann_rr.next_to(panel, DOWN, buff=0.22)
        self.play(FadeOut(box_tt), FadeOut(ann_tt),
                  Create(box_rr), Write(ann_rr), run_time=1.2)
        self.wait(1.2)

        # Flat limit note
        self.play(FadeOut(box_rr), FadeOut(ann_rr), run_time=0.6)
        flat_lim = Text("Set M = 0 → c²-2GM/r = c², -1/(1-0) = -1 → flat Minkowski metric",
                        font_size=16, color=GRAY)
        flat_lim.next_to(panel, DOWN, buff=0.22)
        self.play(Write(flat_lim), run_time=1.5)
        self.wait(2)
