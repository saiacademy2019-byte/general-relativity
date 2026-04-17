"""
Part 6 — Einstein Field Equation & Equivalence Principle
2 scenes:
  EinsteinEquationLabeled  — animated equation G_μν = (8πG/c⁴) T_μν with annotations
                             + 4×4 grid showing 10 independent components
  EquivalencePrinciple     — rocket in space vs room on Earth, equivalence result
"""
from manim import *
import numpy as np

CURV_COL     = "#F5D040"   # yellow  — curvature
RIEMANN_COL  = "#C77DFF"   # purple  — Riemann / Ricci
CHRISTOF_COL = "#50C878"   # green   — Christoffel
EINST_COL    = "#FF6B6B"   # red     — Einstein tensor
SCHWARZ_COL  = "#3ABEFF"   # cyan    — misc


# ══════════════════════════════════════════════════════════════════════════════
# Scene 1 — EinsteinEquationLabeled
# ══════════════════════════════════════════════════════════════════════════════
class EinsteinEquationLabeled(Scene):
    def construct(self):
        # ── Title ─────────────────────────────────────────────────────────────
        title = Text("Einstein's Field Equation", font_size=40, weight=BOLD)
        title.to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=1.5)
        self.wait(0.3)

        # ── ACT 1: Show the equation ──────────────────────────────────────────
        # Build each piece separately so we can point arrows at them later
        eq_G   = Text("G", font_size=50, color=BLUE_D, weight=BOLD)
        eq_mnu = Text("μν", font_size=32, color=BLUE_D)
        eq_eq  = Text("=", font_size=50, color=WHITE)
        eq_8pi = Text("8πG", font_size=38, color=GRAY)
        eq_div = Line(ORIGIN, RIGHT * 1.05, color=GRAY, stroke_width=2.5)
        eq_c4  = Text("c⁴", font_size=38, color=GRAY)
        eq_T   = Text("T", font_size=50, color=ORANGE, weight=BOLD)
        eq_mnu2= Text("μν", font_size=32, color=ORANGE)

        # Position the fraction block
        frac_group = VGroup(eq_8pi, eq_div, eq_c4)
        eq_8pi.move_to(ORIGIN)
        eq_div.next_to(eq_8pi, DOWN, buff=0.08)
        eq_div.move_to(eq_8pi.get_center() + DOWN * 0.45)
        eq_c4.next_to(eq_div, DOWN, buff=0.08)

        # Widen the fraction bar to match numerator/denom
        eq_div.put_start_and_end_on(
            eq_div.get_start() + LEFT * 0.05,
            eq_div.get_end()   + RIGHT * 0.05,
        )

        # Assemble full equation row
        eq_G.move_to(LEFT * 3.6 + UP * 0.1)
        eq_mnu.next_to(eq_G, DOWN + RIGHT, buff=-0.22)
        eq_eq.next_to(eq_G, RIGHT, buff=0.45)
        frac_group.next_to(eq_eq, RIGHT, buff=0.55)
        eq_T.next_to(frac_group, RIGHT, buff=0.55)
        eq_mnu2.next_to(eq_T, DOWN + RIGHT, buff=-0.22)

        eq_all = VGroup(eq_G, eq_mnu, eq_eq, eq_8pi, eq_div, eq_c4, eq_T, eq_mnu2)
        eq_all.move_to(UP * 1.5)

        # Show equation piece by piece
        self.play(Write(eq_G), Write(eq_mnu), run_time=0.9)
        self.play(Write(eq_eq), run_time=0.4)
        self.play(Write(eq_8pi), Create(eq_div), Write(eq_c4), run_time=1.0)
        self.play(Write(eq_T), Write(eq_mnu2), run_time=0.9)
        self.wait(0.6)

        # ── ACT 2: Annotation arrows + label boxes ────────────────────────────
        # Helper: create a rounded label box
        def make_box(lines, col, width=3.2):
            txt = Text("\n".join(lines), font_size=17, color=col,
                       line_spacing=1.25)
            box = RoundedRectangle(
                width=width, height=len(lines) * 0.52 + 0.35,
                corner_radius=0.18,
                color=col, stroke_width=1.5,
                fill_color=BLACK, fill_opacity=0.6,
            )
            box.move_to(txt.get_center())
            return VGroup(box, txt)

        anchor_G = eq_G.get_center() + DOWN * 0.35
        anchor_k = eq_div.get_center()
        anchor_T = eq_T.get_center() + DOWN * 0.35

        box_G = make_box(["Spacetime curvature", "(Einstein tensor)"], BLUE_D)
        box_k = make_box(["Coupling constant", "(how strong gravity is)"], GRAY)
        box_T = make_box(["Matter & energy", "(stress-energy tensor)"], ORANGE)

        box_G.move_to(LEFT * 3.6 + DOWN * 1.2)
        box_k.move_to(ORIGIN      + DOWN * 1.55)
        box_T.move_to(RIGHT * 3.4 + DOWN * 1.2)

        arr_G = Arrow(anchor_G, box_G.get_top() + UP * 0.05,
                      color=BLUE_D, buff=0.05, stroke_width=2.5,
                      max_tip_length_to_length_ratio=0.25)
        arr_k = Arrow(anchor_k + DOWN * 0.28, box_k.get_top() + UP * 0.05,
                      color=GRAY, buff=0.05, stroke_width=2.5,
                      max_tip_length_to_length_ratio=0.25)
        arr_T = Arrow(anchor_T, box_T.get_top() + UP * 0.05,
                      color=ORANGE, buff=0.05, stroke_width=2.5,
                      max_tip_length_to_length_ratio=0.25)

        self.play(GrowArrow(arr_G), FadeIn(box_G), run_time=0.9)
        self.play(GrowArrow(arr_k), FadeIn(box_k), run_time=0.9)
        self.play(GrowArrow(arr_T), FadeIn(box_T), run_time=0.9)
        self.wait(1.5)

        # ── ACT 3: Worded version ─────────────────────────────────────────────
        self.play(
            FadeOut(arr_G), FadeOut(box_G),
            FadeOut(arr_k), FadeOut(box_k),
            FadeOut(arr_T), FadeOut(box_T),
            eq_all.animate.shift(UP * 0.9).scale(0.82),
            run_time=1.2,
        )

        word_G = Text("Spacetime Curvature", font_size=30, color=BLUE_D, weight=BOLD)
        word_eq = Text("=", font_size=30, color=WHITE)
        word_k  = Text("Constant", font_size=30, color=GRAY, weight=BOLD)
        word_x  = Text("×", font_size=30, color=WHITE)
        word_T  = Text("Matter-Energy", font_size=30, color=ORANGE, weight=BOLD)

        word_row = VGroup(word_G, word_eq, word_k, word_x, word_T)
        word_row.arrange(RIGHT, buff=0.32)
        word_row.move_to(DOWN * 0.4)

        self.play(Write(word_row), run_time=2.2)
        self.wait(1.2)

        caption = Text(
            "Mass and energy tell spacetime how to curve.\nCurved spacetime tells mass how to move.",
            font_size=21, color=CURV_COL, line_spacing=1.3,
        )
        caption.move_to(DOWN * 1.65)
        self.play(Write(caption), run_time=2.0)
        self.wait(1.2)

        # ── ACT 4: 4×4 grid — 10 independent equations ───────────────────────
        self.play(
            FadeOut(word_row), FadeOut(caption),
            FadeOut(eq_all),
            run_time=0.9,
        )

        note_head = Text(
            "10 equations in disguise",
            font_size=34, color=CURV_COL, weight=BOLD,
        )
        note_head.to_edge(UP, buff=0.35)
        note_sub = Text(
            "μ, ν each run 0 → 3  (t, x, y, z)  and the tensor is symmetric  →  10 independent components",
            font_size=19, color=GRAY,
        )
        note_sub.next_to(note_head, DOWN, buff=0.2)
        self.play(
            Transform(title, note_head),
            FadeIn(note_sub),
            run_time=1.2,
        )
        self.wait(0.5)

        # Build 4×4 grid of labels
        labels_row = ["t", "x", "y", "z"]
        cell_w, cell_h = 1.55, 0.72
        grid_origin = np.array([-2.5, 0.4, 0])

        # Which (i,j) are the 10 independent components (upper triangle + diagonal)
        independent = set()
        for i in range(4):
            for j in range(i, 4):
                independent.add((i, j))

        grid_cells = VGroup()
        for i in range(4):
            for j in range(4):
                cx = grid_origin[0] + j * cell_w
                cy = grid_origin[1] - i * cell_h
                pos = np.array([cx, cy, 0])

                is_ind = (i, j) in independent or (j, i) in independent
                col = CURV_COL if (i <= j) else GRAY
                op  = 1.0     if is_ind else 0.35

                cell_rect = RoundedRectangle(
                    width=cell_w - 0.08, height=cell_h - 0.08,
                    corner_radius=0.1,
                    color=col, stroke_width=1.2,
                    fill_color=BLACK, fill_opacity=0.55 * op,
                    stroke_opacity=op,
                )
                cell_rect.move_to(pos)

                lbl_str = f"G_{labels_row[i]}{labels_row[j]}"
                lbl = Text(lbl_str, font_size=18, color=col)
                lbl.set_opacity(op)
                lbl.move_to(pos)

                grid_cells.add(VGroup(cell_rect, lbl))

        # Row and column headers
        header_row = VGroup()
        for j, h in enumerate(labels_row):
            cx = grid_origin[0] + j * cell_w
            t = Text(h, font_size=19, color=WHITE, weight=BOLD)
            t.move_to(np.array([cx, grid_origin[1] + cell_h * 0.85, 0]))
            header_row.add(t)

        header_col = VGroup()
        for i, h in enumerate(labels_row):
            cy = grid_origin[1] - i * cell_h
            t = Text(h, font_size=19, color=WHITE, weight=BOLD)
            t.move_to(np.array([grid_origin[0] - cell_w * 0.75, cy, 0]))
            header_col.add(t)

        self.play(
            Create(grid_cells),
            FadeIn(header_row),
            FadeIn(header_col),
            run_time=2.0,
        )

        # Brace / annotation on right side
        count_box = RoundedRectangle(
            width=3.4, height=1.3, corner_radius=0.18,
            color=CURV_COL, stroke_width=1.5,
            fill_color=BLACK, fill_opacity=0.7,
        )
        count_box.move_to(RIGHT * 3.6 + UP * 0.3)
        count_txt1 = Text("10 independent", font_size=22, color=CURV_COL, weight=BOLD)
        count_txt2 = Text("equations", font_size=22, color=CURV_COL, weight=BOLD)
        count_txt1.move_to(count_box.get_center() + UP * 0.22)
        count_txt2.move_to(count_box.get_center() + DOWN * 0.22)

        sym_note = Text(
            "Lower triangle = upper triangle\n(symmetric tensor)",
            font_size=17, color=GRAY, line_spacing=1.2,
        )
        sym_note.next_to(count_box, DOWN, buff=0.28)

        self.play(Create(count_box), Write(count_txt1), Write(count_txt2), run_time=1.0)
        self.play(FadeIn(sym_note), run_time=0.9)
        self.wait(2.0)

        punchline = Text(
            "Each equation links curvature to the flow of energy and momentum",
            font_size=20, color=EINST_COL,
        )
        punchline.to_edge(DOWN, buff=0.38)
        self.play(Write(punchline), run_time=2.0)
        self.wait(2.5)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 2 — EquivalencePrinciple
# ══════════════════════════════════════════════════════════════════════════════
class EquivalencePrinciple(Scene):

    def _draw_stick_figure(self, pos, col=WHITE, scale=1.0):
        """Return a VGroup stick figure centered at pos."""
        s = scale
        head  = Circle(radius=0.18*s, color=col, stroke_width=2).move_to(pos + UP*(0.55*s))
        body  = Line(pos + UP*(0.37*s), pos + DOWN*(0.18*s), color=col, stroke_width=2)
        arm_l = Line(pos + UP*(0.20*s), pos + UP*(0.20*s) + LEFT*(0.30*s)  + DOWN*(0.15*s),
                     color=col, stroke_width=2)
        arm_r = Line(pos + UP*(0.20*s), pos + UP*(0.20*s) + RIGHT*(0.30*s) + DOWN*(0.15*s),
                     color=col, stroke_width=2)
        leg_l = Line(pos + DOWN*(0.18*s), pos + DOWN*(0.52*s) + LEFT*(0.18*s),
                     color=col, stroke_width=2)
        leg_r = Line(pos + DOWN*(0.18*s), pos + DOWN*(0.52*s) + RIGHT*(0.18*s),
                     color=col, stroke_width=2)
        return VGroup(head, body, arm_l, arm_r, leg_l, leg_r)

    def _draw_box(self, center, w, h, col=WHITE):
        return Rectangle(width=w, height=h, color=col, stroke_width=2.5,
                         fill_color=BLACK, fill_opacity=0.3).move_to(center)

    def construct(self):
        title = Text("The Equivalence Principle", font_size=40, weight=BOLD)
        title.to_edge(UP, buff=0.35)
        sub = Text("Einstein's 'happiest thought'", font_size=22, color=GRAY)
        sub.next_to(title, DOWN, buff=0.15)
        self.play(Write(title), FadeIn(sub), run_time=1.5)
        self.wait(0.4)

        # ── Divider ───────────────────────────────────────────────────────────
        div = DashedLine(UP * 2.2, DOWN * 3.8, color=GRAY, stroke_opacity=0.3)
        self.add(div)

        # ══════════════ LEFT PANEL — Rocket in deep space ════════════════════
        left_cx  = -3.3
        box_center_l = np.array([left_cx, -0.5, 0])

        lbl_left = Text("Rocket in deep space", font_size=21, color=SCHWARZ_COL, weight=BOLD)
        lbl_left.move_to(np.array([left_cx, 1.8, 0]))
        self.play(FadeIn(lbl_left), run_time=0.7)

        rocket_box = self._draw_box(box_center_l, 2.2, 2.8, col=SCHWARZ_COL)
        self.play(Create(rocket_box), run_time=0.9)

        # Flame / thruster at bottom
        flame1 = Triangle(color=ORANGE, fill_color=ORANGE, fill_opacity=0.8)
        flame1.scale(0.22).rotate(PI)
        flame1.move_to(box_center_l + DOWN * 1.52 + LEFT * 0.3)
        flame2 = Triangle(color=YELLOW, fill_color=YELLOW, fill_opacity=0.8)
        flame2.scale(0.16).rotate(PI)
        flame2.move_to(box_center_l + DOWN * 1.52 + RIGHT * 0.2)
        self.play(FadeIn(flame1), FadeIn(flame2), run_time=0.5)

        # Up arrow on the side
        accel_arrow = Arrow(
            box_center_l + LEFT * 1.35 + DOWN * 0.8,
            box_center_l + LEFT * 1.35 + UP * 0.8,
            color=SCHWARZ_COL, buff=0, stroke_width=3,
            max_tip_length_to_length_ratio=0.22,
        )
        accel_lbl = Text("accelerating\nupward", font_size=15, color=SCHWARZ_COL,
                         line_spacing=1.2)
        accel_lbl.next_to(accel_arrow, LEFT, buff=0.12)
        self.play(GrowArrow(accel_arrow), FadeIn(accel_lbl), run_time=0.9)

        # Stick figure pressed to the floor of the box
        fig_l = self._draw_stick_figure(box_center_l + DOWN * 0.72)
        self.play(FadeIn(fig_l), run_time=0.7)

        # Force arrow inside: person feels pushed down
        feel_arr_l = Arrow(
            box_center_l + RIGHT * 0.55 + DOWN * 0.05,
            box_center_l + RIGHT * 0.55 + DOWN * 0.85,
            color=EINST_COL, buff=0, stroke_width=2.5,
            max_tip_length_to_length_ratio=0.28,
        )
        self.play(GrowArrow(feel_arr_l), run_time=0.7)

        feel_lbl_l = Text("Feels a force\npushing DOWN", font_size=15, color=EINST_COL,
                          line_spacing=1.2)
        feel_lbl_l.move_to(box_center_l + DOWN * 1.88)
        self.play(Write(feel_lbl_l), run_time=0.8)

        # ══════════════ RIGHT PANEL — Room on Earth ═══════════════════════════
        right_cx = 3.3
        box_center_r = np.array([right_cx, -0.5, 0])

        lbl_right = Text("Room on Earth", font_size=21, color=CHRISTOF_COL, weight=BOLD)
        lbl_right.move_to(np.array([right_cx, 1.8, 0]))
        self.play(FadeIn(lbl_right), run_time=0.7)

        earth_box = self._draw_box(box_center_r, 2.2, 2.8, col=CHRISTOF_COL)
        self.play(Create(earth_box), run_time=0.9)

        # Floor hatch lines to suggest solid ground
        for k in range(-3, 4):
            hatch = Line(
                box_center_r + DOWN * 1.4 + LEFT * 0.32 + RIGHT * k * 0.25,
                box_center_r + DOWN * 1.6 + LEFT * 0.12 + RIGHT * k * 0.25,
                color=GRAY, stroke_width=1.2, stroke_opacity=0.6,
            )
            self.add(hatch)

        # Gravity arrow outside the box, pointing down
        grav_arrow = Arrow(
            box_center_r + RIGHT * 1.35 + UP * 0.4,
            box_center_r + RIGHT * 1.35 + DOWN * 0.8,
            color=CHRISTOF_COL, buff=0, stroke_width=3,
            max_tip_length_to_length_ratio=0.22,
        )
        grav_lbl = Text("gravity", font_size=15, color=CHRISTOF_COL)
        grav_lbl.next_to(grav_arrow, RIGHT, buff=0.1)
        self.play(GrowArrow(grav_arrow), FadeIn(grav_lbl), run_time=0.9)

        # Stick figure standing on floor
        fig_r = self._draw_stick_figure(box_center_r + DOWN * 0.72)
        self.play(FadeIn(fig_r), run_time=0.7)

        # Force arrow: person feels pushed down
        feel_arr_r = Arrow(
            box_center_r + LEFT * 0.55 + DOWN * 0.05,
            box_center_r + LEFT * 0.55 + DOWN * 0.85,
            color=EINST_COL, buff=0, stroke_width=2.5,
            max_tip_length_to_length_ratio=0.28,
        )
        self.play(GrowArrow(feel_arr_r), run_time=0.7)

        feel_lbl_r = Text("Feels a force\npushing DOWN", font_size=15, color=EINST_COL,
                          line_spacing=1.2)
        feel_lbl_r.move_to(box_center_r + DOWN * 1.88)
        self.play(Write(feel_lbl_r), run_time=0.8)

        self.wait(1.2)

        # ── Equivalence sign ─────────────────────────────────────────────────
        equiv_sign = Text("≡", font_size=72, color=CURV_COL, weight=BOLD)
        equiv_sign.move_to(ORIGIN + UP * 0.5)
        self.play(Write(equiv_sign), run_time=0.9)

        id_box = RoundedRectangle(
            width=7.2, height=0.85, corner_radius=0.2,
            color=CURV_COL, stroke_width=1.5,
            fill_color=BLACK, fill_opacity=0.65,
        )
        id_box.move_to(ORIGIN + DOWN * 0.55)
        id_txt = Text(
            "These two situations are IDENTICAL from the inside",
            font_size=19, color=CURV_COL, weight=BOLD,
        )
        id_txt.move_to(id_box.get_center())
        self.play(Create(id_box), Write(id_txt), run_time=1.2)
        self.wait(1.5)

        # ── Punchline ─────────────────────────────────────────────────────────
        punch_box = RoundedRectangle(
            width=9.6, height=0.88, corner_radius=0.22,
            color=EINST_COL, stroke_width=2,
            fill_color="#200000", fill_opacity=0.85,
        )
        punch_box.to_edge(DOWN, buff=0.35)
        punch_txt = Text(
            "Gravity is not a force — it is the geometry of spacetime itself",
            font_size=21, color=EINST_COL, weight=BOLD,
        )
        punch_txt.move_to(punch_box.get_center())
        self.play(Create(punch_box), Write(punch_txt), run_time=1.8)
        self.wait(3.0)
