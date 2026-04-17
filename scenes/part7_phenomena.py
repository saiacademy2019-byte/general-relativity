"""
Part 7 — GR Phenomena
4 scenes:
  GPSTimeDilation       — how GR/SR clock corrections keep GPS accurate
  BlackHoles            — event horizon, geodesics, time dilation near horizon
  GravitationalWaves    — merging BHs, rippling spacetime, LIGO detection
  GravitationalLensing  — light bending, Einstein ring, Eddington 1919
"""
from manim import *
import numpy as np

CURV_COL     = "#F5D040"   # yellow
RIEMANN_COL  = "#C77DFF"   # purple
CHRISTOF_COL = "#50C878"   # green
EINST_COL    = "#FF6B6B"   # red
SCHWARZ_COL  = "#3ABEFF"   # cyan


# ══════════════════════════════════════════════════════════════════════════════
# Shared helper — clock icon
# ══════════════════════════════════════════════════════════════════════════════
def make_clock(center, radius=0.38, col=WHITE, hour_angle=PI/4):
    """Return a VGroup clock face with two hands."""
    face   = Circle(radius=radius, color=col, stroke_width=2)
    face.move_to(center)
    # hour hand (shorter)
    h_end  = center + radius * 0.5 * np.array([np.sin(hour_angle), np.cos(hour_angle), 0])
    hand_h = Line(center, h_end, color=col, stroke_width=2.5)
    # minute hand (longer, 90° offset)
    m_ang  = hour_angle + PI / 2
    m_end  = center + radius * 0.75 * np.array([np.sin(m_ang), np.cos(m_ang), 0])
    hand_m = Line(center, m_end, color=col, stroke_width=2)
    dot    = Dot(center, radius=0.05, color=col)
    return VGroup(face, hand_h, hand_m, dot)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 1 — GPSTimeDilation
# ══════════════════════════════════════════════════════════════════════════════
class GPSTimeDilation(Scene):
    def construct(self):
        title = Text("GPS and Gravitational Time Dilation", font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=1.5)

        # ── Earth ─────────────────────────────────────────────────────────────
        earth_pos = np.array([-3.8, -0.8, 0])
        earth = Circle(radius=0.75, fill_color=BLUE_E, fill_opacity=0.9,
                       stroke_color=WHITE, stroke_width=1.8)
        earth.move_to(earth_pos)
        earth_lbl = Text("Earth", font_size=17, color=WHITE)
        earth_lbl.next_to(earth, DOWN, buff=0.1)
        self.play(FadeIn(earth), FadeIn(earth_lbl), run_time=0.9)

        # Clock on Earth surface (bottom of earth)
        clock_earth = make_clock(earth_pos + DOWN * 1.25 + RIGHT * 0.15,
                                 radius=0.32, col=SCHWARZ_COL)
        clk_lbl_e = Text("Clock on\nEarth surface", font_size=15, color=SCHWARZ_COL,
                         line_spacing=1.2)
        clk_lbl_e.next_to(clock_earth, DOWN, buff=0.1)
        self.play(FadeIn(clock_earth), FadeIn(clk_lbl_e), run_time=0.8)

        # ── Orbit circle ──────────────────────────────────────────────────────
        orbit = Circle(radius=2.1, color=GRAY, stroke_width=1.2, stroke_opacity=0.5)
        orbit.move_to(earth_pos)
        self.play(Create(orbit), run_time=0.9)

        # Satellite dot
        sat_pos = earth_pos + np.array([2.1, 0, 0])
        satellite = Dot(sat_pos, radius=0.14, color=CURV_COL)
        sat_lbl = Text("GPS Satellite\n(altitude h ≈ 20 200 km)", font_size=15,
                       color=CURV_COL, line_spacing=1.2)
        sat_lbl.next_to(satellite, UP + RIGHT, buff=0.12)
        self.play(FadeIn(satellite), FadeIn(sat_lbl), run_time=0.8)

        # Clock on satellite
        clock_sat = make_clock(sat_pos + UP * 0.75 + RIGHT * 0.25,
                               radius=0.32, col=CURV_COL, hour_angle=-PI/6)
        self.play(FadeIn(clock_sat), run_time=0.7)

        # Satellite orbit animation (brief)
        self.play(
            Rotate(satellite, angle=TAU * 0.18, about_point=earth_pos),
            run_time=1.4,
        )
        self.wait(0.4)

        # ── Effects table ─────────────────────────────────────────────────────
        table_origin = np.array([1.5, 1.5, 0])
        rows = [
            ("GR effect (altitude):", "satellite clock runs FASTER", "+45.9 μs/day", GREEN),
            ("SR effect (speed):",    "satellite clock runs SLOWER", "−7.2 μs/day",  ORANGE),
            ("Net effect:",           "",                             "+38.4 μs/day", CURV_COL),
        ]
        row_h = 0.72
        for k, (label, desc, value, col) in enumerate(rows):
            y = table_origin[1] - k * row_h
            row_box = RoundedRectangle(
                width=7.8, height=row_h - 0.06, corner_radius=0.14,
                color=col, stroke_width=1.3,
                fill_color=BLACK, fill_opacity=0.55,
            )
            row_box.move_to(np.array([table_origin[0] + 0.7, y, 0]))

            t_lbl = Text(label, font_size=17, color=WHITE)
            t_lbl.move_to(row_box.get_left() + RIGHT * 1.55)
            t_desc = Text(desc, font_size=16, color=col)
            t_desc.move_to(row_box.get_center() + RIGHT * 0.1)
            t_val = Text(value, font_size=20, color=col, weight=BOLD)
            t_val.move_to(row_box.get_right() + LEFT * 0.95)

            self.play(
                Create(row_box), FadeIn(t_lbl), FadeIn(t_desc), FadeIn(t_val),
                run_time=0.85,
            )

        self.wait(0.8)

        # ── Consequence ───────────────────────────────────────────────────────
        conseq_box = RoundedRectangle(
            width=8.2, height=0.82, corner_radius=0.18,
            color=EINST_COL, stroke_width=1.8,
            fill_color="#200000", fill_opacity=0.75,
        )
        conseq_box.move_to(np.array([1.5, -1.95, 0]))
        conseq_txt = Text(
            "Without correction: GPS error grows by ~10 km per day",
            font_size=19, color=EINST_COL, weight=BOLD,
        )
        conseq_txt.move_to(conseq_box.get_center())
        self.play(Create(conseq_box), Write(conseq_txt), run_time=1.2)
        self.wait(0.8)

        # ── Punchline ─────────────────────────────────────────────────────────
        punch = Text(
            "GR is not just theory — it runs inside your phone's GPS",
            font_size=20, color=CURV_COL, weight=BOLD,
        )
        punch.to_edge(DOWN, buff=0.35)
        self.play(Write(punch), run_time=1.6)
        self.wait(3.0)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 2 — BlackHoles
# ══════════════════════════════════════════════════════════════════════════════
class BlackHoles(Scene):
    def construct(self):
        title = Text("Black Holes", font_size=40, weight=BOLD, color=EINST_COL)
        title.to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=1.5)

        bh_pos = np.array([-0.5, -0.3, 0])

        # ── ACT 1: Warped grid ────────────────────────────────────────────────
        grid = NumberPlane(
            x_range=[-7, 7, 1], y_range=[-5, 5, 1],
            x_length=14, y_length=9,
            background_line_style={
                "stroke_color":   BLUE_D,
                "stroke_opacity": 0.75,
                "stroke_width":   2.0,
            },
            axis_config={"stroke_opacity": 0},
        )
        self.play(Create(grid), run_time=1.5)

        ex, ey = bh_pos[0], bh_pos[1]

        def strong_warp(p):
            dp = np.array([p[0] - ex, p[1] - ey, 0])
            r  = np.linalg.norm(dp[:2])
            if r < 0.12:
                return np.array([ex, ey, 0])
            strength = 2.2
            factor   = r / (r + strength)
            new_xy   = np.array([ex, ey]) + dp[:2] * factor
            return np.array([new_xy[0], new_xy[1], p[2]])

        warped = grid.copy()
        warped.apply_function(strong_warp)
        self.play(Transform(grid, warped), run_time=2.5)

        # ── Black hole core ───────────────────────────────────────────────────
        core = Dot(bh_pos, radius=0.22, color=WHITE)
        core_lbl = Text("Massive collapsed star", font_size=16, color=WHITE)
        core_lbl.next_to(core, UP, buff=0.18)
        self.play(FadeIn(core), FadeIn(core_lbl), run_time=0.8)
        self.wait(0.4)

        # Glow effect
        for r_g, op in [(0.35, 0.35), (0.52, 0.2), (0.72, 0.1)]:
            glow = Circle(radius=r_g, color=WHITE, stroke_opacity=op, stroke_width=1)
            glow.move_to(bh_pos)
            self.add(glow)

        # ── Event horizon ─────────────────────────────────────────────────────
        eh_radius = 1.25
        event_horizon = DashedVMobject(
            Circle(radius=eh_radius, color=EINST_COL, stroke_width=2.5),
            num_dashes=22,
        )
        event_horizon.move_to(bh_pos)
        eh_lbl = Text("Event horizon  (r = 2GM/c²)", font_size=17, color=EINST_COL)
        eh_lbl.move_to(bh_pos + UP * (eh_radius + 0.35))
        self.play(Create(event_horizon), Write(eh_lbl), run_time=1.5)
        self.wait(0.6)

        # ── ACT 2: 3 arrows at different distances ────────────────────────────
        arrow_data = [
            # (position offset from bh_pos, direction vector, color, label, label_side)
            (np.array([ 3.2,  0.8, 0]), np.array([-0.5, -0.2, 0]), CHRISTOF_COL,
             "Far away — free to move any direction", RIGHT),
            (np.array([ 2.0, -0.5, 0]), np.array([-1.0,  0.1, 0]), CURV_COL,
             "Closer — gravity dominates", RIGHT),
            (np.array([ 1.28, 0.0, 0]), np.array([-1.0,  0.0, 0]), EINST_COL,
             "At horizon — only inward!", UP),
        ]
        for offset, direction, col, label, side in arrow_data:
            pos   = bh_pos + offset
            d_hat = direction / np.linalg.norm(direction)
            arr   = Arrow(pos, pos + d_hat * 0.7, color=col, buff=0,
                          stroke_width=3, max_tip_length_to_length_ratio=0.28)
            lbl   = Text(label, font_size=15, color=col)
            lbl.next_to(arr, side, buff=0.12)
            self.play(GrowArrow(arr), FadeIn(lbl), run_time=0.9)

        self.wait(0.8)

        # ── ACT 3: Two clocks — time dilation ────────────────────────────────
        # Clock near horizon (slow)
        near_pos = bh_pos + np.array([1.45, -0.9, 0])
        clk_near = make_clock(near_pos, radius=0.3, col=EINST_COL, hour_angle=0)
        clk_near_lbl = Text("Ticks very slowly", font_size=14, color=EINST_COL)
        clk_near_lbl.next_to(clk_near, DOWN, buff=0.1)

        # Clock far away (fast)
        far_pos = bh_pos + np.array([4.0, 1.8, 0])
        clk_far  = make_clock(far_pos, radius=0.3, col=CHRISTOF_COL, hour_angle=PI/3)
        clk_far_lbl = Text("Ticks normally", font_size=14, color=CHRISTOF_COL)
        clk_far_lbl.next_to(clk_far, UP, buff=0.1)

        self.play(FadeIn(clk_near), FadeIn(clk_near_lbl),
                  FadeIn(clk_far),  FadeIn(clk_far_lbl), run_time=1.0)

        # Rotate far clock hands faster (3 full rotations) while near rotates slightly
        self.play(
            Rotate(clk_far[1],  angle=TAU * 3,   about_point=far_pos,  run_time=3.0),
            Rotate(clk_near[1], angle=PI * 0.15,  about_point=near_pos, run_time=3.0),
        )
        self.wait(0.5)

        # ── Key labels ────────────────────────────────────────────────────────
        info_rows = [
            ("Inside: future always points toward singularity", RIEMANN_COL),
            ("Outside observer sees clock freeze at horizon",   GRAY),
        ]
        for k, (txt, col) in enumerate(info_rows):
            t = Text(txt, font_size=17, color=col)
            t.move_to(np.array([2.2, -2.6 + k * 0.52, 0]))
            self.play(FadeIn(t), run_time=0.7)

        # ── Punchline ─────────────────────────────────────────────────────────
        punch_box = RoundedRectangle(
            width=9.8, height=0.82, corner_radius=0.2,
            color=EINST_COL, stroke_width=2,
            fill_color="#200000", fill_opacity=0.85,
        )
        punch_box.to_edge(DOWN, buff=0.3)
        punch_txt = Text(
            "Not even light can escape — it follows geodesics that all point inward",
            font_size=19, color=EINST_COL, weight=BOLD,
        )
        punch_txt.move_to(punch_box.get_center())
        self.play(Create(punch_box), Write(punch_txt), run_time=1.8)
        self.wait(3.0)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 3 — GravitationalWaves
# ══════════════════════════════════════════════════════════════════════════════
class GravitationalWaves(Scene):
    def construct(self):
        title = Text("Gravitational Waves", font_size=40, weight=BOLD, color=RIEMANN_COL)
        title.to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=1.5)

        bh1_pos = np.array([-0.9, 0.4, 0])
        bh2_pos = np.array([ 0.9, 0.4, 0])

        # ── ACT 1: Two black holes orbiting each other ─────────────────────────
        bh1 = Dot(bh1_pos, radius=0.22, color=WHITE)
        bh2 = Dot(bh2_pos, radius=0.18, color=WHITE)

        # Labels
        bh1_lbl = Text("Black hole 1", font_size=14, color=GRAY)
        bh1_lbl.next_to(bh1, UP, buff=0.12)
        bh2_lbl = Text("Black hole 2", font_size=14, color=GRAY)
        bh2_lbl.next_to(bh2, DOWN, buff=0.12)

        orbit_center = np.array([0, 0.4, 0])
        orbit_r1 = 0.9
        orbit_r2 = 0.9

        self.play(FadeIn(bh1), FadeIn(bh2), FadeIn(bh1_lbl), FadeIn(bh2_lbl), run_time=0.9)

        # Orbit animation (few loops)
        self.play(
            Rotate(bh1, angle=TAU * 1.5, about_point=orbit_center, run_time=3.0),
            Rotate(bh2, angle=TAU * 1.5 + PI, about_point=orbit_center, run_time=3.0,
                   rate_func=linear),
            rate_func=linear,
        )

        # ── ACT 2: Ripple waves ───────────────────────────────────────────────
        ripple_center = orbit_center
        ripple_radii  = [1.2, 2.0, 2.9, 3.8]

        ripples = VGroup()
        for r in ripple_radii:
            ring = Circle(radius=r, color=RIEMANN_COL,
                          stroke_width=max(0.5, 2.2 - r * 0.35),
                          stroke_opacity=max(0.1, 0.8 - r * 0.18))
            ring.move_to(ripple_center)
            ripples.add(ring)

        self.play(*[Create(r) for r in ripples], run_time=2.0)

        # Animate ripples expanding and fading
        expanded = VGroup()
        for i, ring in enumerate(ripples):
            new_r = ripple_radii[i] + 1.4
            exp = ring.copy()
            exp.scale(new_r / ripple_radii[i])
            exp.set_stroke(opacity=0.0)
            expanded.add(exp)

        self.play(
            *[Transform(ripples[i], expanded[i]) for i in range(len(ripples))],
            run_time=2.5,
            rate_func=linear,
        )
        self.play(FadeOut(ripples), run_time=0.5)

        # Draw fresh visible ripples for context
        for k in range(3):
            new_set = VGroup()
            for r in [1.3, 2.1, 3.0]:
                ring = Circle(radius=r, color=RIEMANN_COL,
                              stroke_width=2.0 - r * 0.3,
                              stroke_opacity=0.7 - r * 0.15)
                ring.move_to(ripple_center)
                new_set.add(ring)
            self.play(*[Create(r) for r in new_set], run_time=0.7)
            self.play(FadeOut(new_set), run_time=0.5)

        # ── ACT 3: LIGO arms ──────────────────────────────────────────────────
        ligo_center = np.array([3.8, 0.4, 0])
        arm_len = 1.1

        ligo_lbl = Text("LIGO detector", font_size=18, color=SCHWARZ_COL, weight=BOLD)
        ligo_lbl.move_to(ligo_center + UP * 1.55)
        self.play(FadeIn(ligo_lbl), run_time=0.7)

        # Two perpendicular arms
        arm_h = Line(ligo_center + LEFT * arm_len, ligo_center + RIGHT * arm_len,
                     color=SCHWARZ_COL, stroke_width=3)
        arm_v = Line(ligo_center + DOWN * arm_len, ligo_center + UP * arm_len,
                     color=SCHWARZ_COL, stroke_width=3)
        ligo_dot = Dot(ligo_center, radius=0.09, color=WHITE)
        ligo_group = VGroup(arm_h, arm_v, ligo_dot)
        self.play(Create(arm_h), Create(arm_v), FadeIn(ligo_dot), run_time=0.9)

        # Animate: arm_h stretches, arm_v compresses, then swap — 3 cycles
        stretch_len = arm_len * 1.38
        compress_len = arm_len * 0.72

        for _ in range(3):
            # Stretch horizontal, compress vertical
            arm_h_stretched  = Line(
                ligo_center + LEFT  * stretch_len,
                ligo_center + RIGHT * stretch_len,
                color=SCHWARZ_COL, stroke_width=3,
            )
            arm_v_compressed = Line(
                ligo_center + DOWN  * compress_len,
                ligo_center + UP    * compress_len,
                color=SCHWARZ_COL, stroke_width=3,
            )
            self.play(
                Transform(arm_h, arm_h_stretched),
                Transform(arm_v, arm_v_compressed),
                run_time=0.42,
            )
            # Reverse
            arm_h_normal  = Line(
                ligo_center + LEFT  * arm_len,
                ligo_center + RIGHT * arm_len,
                color=SCHWARZ_COL, stroke_width=3,
            )
            arm_v_normal  = Line(
                ligo_center + DOWN  * arm_len,
                ligo_center + UP    * arm_len,
                color=SCHWARZ_COL, stroke_width=3,
            )
            self.play(
                Transform(arm_h, arm_h_normal),
                Transform(arm_v, arm_v_normal),
                run_time=0.42,
            )

        self.wait(0.5)

        # ── Historical note ───────────────────────────────────────────────────
        note1 = Text("September 14, 2015 — first detection by LIGO",
                     font_size=19, color=CURV_COL, weight=BOLD)
        note2 = Text("Two black holes, 1.3 billion light-years away, merged",
                     font_size=17, color=GRAY)
        note1.move_to(DOWN * 2.0)
        note2.next_to(note1, DOWN, buff=0.18)
        self.play(Write(note1), run_time=1.2)
        self.play(FadeIn(note2), run_time=0.9)
        self.wait(0.8)

        # ── Punchline ─────────────────────────────────────────────────────────
        punch_box = RoundedRectangle(
            width=9.8, height=0.82, corner_radius=0.2,
            color=RIEMANN_COL, stroke_width=2,
            fill_color="#0A000A", fill_opacity=0.88,
        )
        punch_box.to_edge(DOWN, buff=0.3)
        punch_txt = Text(
            "Spacetime itself was rippling — GR predicted this 100 years earlier",
            font_size=19, color=RIEMANN_COL, weight=BOLD,
        )
        punch_txt.move_to(punch_box.get_center())
        self.play(Create(punch_box), Write(punch_txt), run_time=1.8)
        self.wait(3.0)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 4 — GravitationalLensing
# ══════════════════════════════════════════════════════════════════════════════
class GravitationalLensing(Scene):

    def _draw_star(self, center, size=0.22, col=YELLOW):
        """Draw a simple 4-point star: X shape + small circle."""
        lines = VGroup()
        for angle in [0, PI/4, PI/2, 3*PI/4]:
            p1 = center + size * np.array([np.cos(angle), np.sin(angle), 0])
            p2 = center - size * np.array([np.cos(angle), np.sin(angle), 0])
            lines.add(Line(p1, p2, color=col, stroke_width=2))
        core = Circle(radius=size * 0.22, color=col, fill_color=col, fill_opacity=1)
        core.move_to(center)
        return VGroup(lines, core)

    def _draw_eye(self, center, col=WHITE):
        """Simple eye icon."""
        eye_outer = Ellipse(width=0.65, height=0.35, color=col, stroke_width=2)
        eye_outer.move_to(center)
        pupil = Circle(radius=0.1, color=col, fill_color=col, fill_opacity=1)
        pupil.move_to(center)
        return VGroup(eye_outer, pupil)

    def construct(self):
        title = Text("Gravitational Lensing", font_size=40, weight=BOLD, color=CURV_COL)
        title.to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=1.5)

        # ── Positions ─────────────────────────────────────────────────────────
        source_pos   = np.array([-5.5, 0.0, 0])
        lens_pos     = np.array([ 0.0, 0.0, 0])
        observer_pos = np.array([ 5.5, 0.0, 0])

        # ── Source: distant galaxy ─────────────────────────────────────────────
        source_star = self._draw_star(source_pos, size=0.28, col=YELLOW)
        source_lbl  = Text("Source\n(distant galaxy)", font_size=16, color=YELLOW,
                           line_spacing=1.2)
        source_lbl.next_to(source_star, DOWN, buff=0.2)
        self.play(FadeIn(source_star), FadeIn(source_lbl), run_time=0.9)

        # ── Lens: massive galaxy cluster ──────────────────────────────────────
        lens_outer = Circle(radius=0.52, color=ORANGE,
                            fill_color="#301000", fill_opacity=0.85, stroke_width=2.5)
        lens_outer.move_to(lens_pos)
        # Glow rings
        for r_g, op in [(0.72, 0.4), (0.98, 0.2), (1.28, 0.1)]:
            glow = Circle(radius=r_g, color=ORANGE, stroke_opacity=op, stroke_width=1.5)
            glow.move_to(lens_pos)
            self.add(glow)
        lens_lbl = Text("Lens\n(massive galaxy cluster)", font_size=16, color=ORANGE,
                        line_spacing=1.2)
        lens_lbl.next_to(lens_outer, DOWN, buff=0.35)
        self.play(FadeIn(lens_outer), FadeIn(lens_lbl), run_time=0.9)

        # ── Observer ──────────────────────────────────────────────────────────
        obs_eye = self._draw_eye(observer_pos)
        obs_lbl = Text("Observer", font_size=16, color=WHITE)
        obs_lbl.next_to(obs_eye, DOWN, buff=0.18)
        self.play(FadeIn(obs_eye), FadeIn(obs_lbl), run_time=0.7)

        # ── ACT 2: Curved light paths ─────────────────────────────────────────
        # Three rays bending around the lens:
        # upper ray bends downward around lens then back to observer
        # lower ray bends upward
        # slight middle ray (barely bends)

        def make_bent_ray(y_offset, curve_strength, col=YELLOW):
            """
            Approximate a bent light path with two arcs.
            Source → lens: arc curving toward x-axis
            Lens → observer: arc curving toward x-axis
            """
            start  = source_pos   + np.array([0, y_offset, 0])
            mid    = lens_pos     + np.array([-0.55, 0, 0])
            end    = observer_pos + np.array([0, y_offset * 0.15, 0])

            seg1 = CubicBezier(
                start,
                start   + RIGHT * 1.8 + UP * (-y_offset * 0.35),
                mid     + LEFT  * 1.0 + UP * ( y_offset * 0.1),
                mid,
                color=col, stroke_width=1.8, stroke_opacity=0.85,
            )
            mid_exit = lens_pos + np.array([0.55, 0, 0])
            seg2 = CubicBezier(
                mid_exit,
                mid_exit + RIGHT * 1.0 + UP * (-y_offset * 0.1),
                end      + LEFT  * 1.8 + UP * ( y_offset * 0.3),
                end,
                color=col, stroke_width=1.8, stroke_opacity=0.85,
            )
            return VGroup(seg1, seg2)

        ray_upper  = make_bent_ray( 0.75, 0.9, col=YELLOW)
        ray_lower  = make_bent_ray(-0.75, 0.9, col=YELLOW)
        ray_middle = make_bent_ray( 0.0,  0.2, col="#FFE080")

        self.play(Create(ray_upper),  run_time=1.2)
        self.play(Create(ray_lower),  run_time=1.2)
        self.play(Create(ray_middle), run_time=0.8)
        self.wait(0.5)

        # ── ACT 3: Apparent source positions (dashed lines) ───────────────────
        # From the observer, extend the ray direction backward
        apparent_top    = observer_pos + np.array([-4.0,  1.4, 0])
        apparent_bottom = observer_pos + np.array([-4.0, -1.4, 0])

        dash_top = DashedLine(observer_pos, apparent_top,
                              color=WHITE, stroke_width=1.2, stroke_opacity=0.55,
                              dash_length=0.18)
        dash_bot = DashedLine(observer_pos, apparent_bottom,
                              color=WHITE, stroke_width=1.2, stroke_opacity=0.55,
                              dash_length=0.18)

        app_lbl_t = Text("Apparent image 1", font_size=13, color=GRAY)
        app_lbl_t.next_to(apparent_top, UP, buff=0.08)
        app_lbl_b = Text("Apparent image 2", font_size=13, color=GRAY)
        app_lbl_b.next_to(apparent_bottom, DOWN, buff=0.08)

        self.play(Create(dash_top), Create(dash_bot), run_time=1.0)
        self.play(FadeIn(app_lbl_t), FadeIn(app_lbl_b), run_time=0.7)

        obs_note = Text("Observer sees multiple images —\nor an Einstein ring",
                        font_size=17, color=WHITE, line_spacing=1.2)
        obs_note.move_to(np.array([4.0, 1.8, 0]))
        self.play(Write(obs_note), run_time=1.2)
        self.wait(0.8)

        # ── ACT 4: Einstein ring diagram ──────────────────────────────────────
        # Show in top-right corner
        ring_center = np.array([3.5, 1.85, 0])
        er_panel = RoundedRectangle(
            width=3.2, height=2.2, corner_radius=0.2,
            color=CURV_COL, stroke_width=1.4,
            fill_color=BLACK, fill_opacity=0.7,
        )
        er_panel.move_to(ring_center)

        er_title = Text("Einstein Ring", font_size=16, color=CURV_COL, weight=BOLD)
        er_title.move_to(ring_center + UP * 0.75)

        ring_c    = ring_center + DOWN * 0.1
        er_ring   = Circle(radius=0.55, color=YELLOW, stroke_width=2.5)
        er_ring.move_to(ring_c)
        er_lens_c = Circle(radius=0.18, color=ORANGE,
                           fill_color="#301000", fill_opacity=0.9, stroke_width=2)
        er_lens_c.move_to(ring_c)

        er_note = Text("Perfect alignment\n→ full ring", font_size=13, color=GRAY,
                       line_spacing=1.1)
        er_note.move_to(ring_center + DOWN * 0.72)

        # Replace the obs_note with the panel
        self.play(
            FadeOut(obs_note),
            Create(er_panel),
            FadeIn(er_title),
            run_time=0.8,
        )
        self.play(Create(er_ring), FadeIn(er_lens_c), FadeIn(er_note), run_time=1.0)
        self.wait(0.8)

        # ── Historical note ───────────────────────────────────────────────────
        hist_box = RoundedRectangle(
            width=7.8, height=0.82, corner_radius=0.18,
            color=CHRISTOF_COL, stroke_width=1.5,
            fill_color=BLACK, fill_opacity=0.65,
        )
        hist_box.move_to(DOWN * 2.5)
        hist_txt = Text(
            "Eddington, 1919 — starlight bending around the Sun confirmed GR",
            font_size=18, color=CHRISTOF_COL, weight=BOLD,
        )
        hist_txt.move_to(hist_box.get_center())
        self.play(Create(hist_box), Write(hist_txt), run_time=1.4)
        self.wait(0.6)

        # ── Punchline ─────────────────────────────────────────────────────────
        punch_box = RoundedRectangle(
            width=9.8, height=0.82, corner_radius=0.2,
            color=CURV_COL, stroke_width=2,
            fill_color="#0A0A00", fill_opacity=0.88,
        )
        punch_box.to_edge(DOWN, buff=0.32)
        punch_txt = Text(
            "Light follows curved spacetime — mass bends the path of light itself",
            font_size=19, color=CURV_COL, weight=BOLD,
        )
        punch_txt.move_to(punch_box.get_center())
        self.play(Create(punch_box), Write(punch_txt), run_time=1.8)
        self.wait(3.0)
