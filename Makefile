SHELL    = /bin/bash
VENV     = source .venv/bin/activate &&
SCENES   = scenes/part1_worldlines.py
SCENES2  = scenes/part2_geodesics.py
SCENES4  = scenes/part4_metric.py
SCENES5  = scenes/part5_curvature.py
# Manim Community low-quality output lands here
VDIR     = media/videos/part1_worldlines/480p15
VDIR2    = media/videos/part2_geodesics/480p15
VDIR4    = media/videos/part4_metric/480p15
VDIR5    = media/videos/part5_curvature/480p15

# Manim appends _ManimCE_vX.Y.Z to the filename — use wildcard to copy latest
cp_gif  = cp $(VDIR)/$(1)_ManimCE_*.gif   media/$(2).gif
cp_gif2 = cp $(VDIR2)/$(1)_ManimCE_*.gif  media/$(2).gif
cp_gif4 = cp $(VDIR4)/$(1)_ManimCE_*.gif  media/$(2).gif
cp_gif5 = cp $(VDIR5)/$(1)_ManimCE_*.gif  media/$(2).gif

# ── Render all Part 1 GIFs ──────────────────────────────────────────────────
gifs:
	$(VENV) manim -ql --format gif $(SCENES) SpacetimeGrid
	$(call cp_gif,SpacetimeGrid,spacetime_grid)
	$(VENV) manim -ql --format gif $(SCENES) WorldLine
	$(call cp_gif,WorldLine,world_line)
	$(VENV) manim -ql --format gif $(SCENES) AppleFalling
	$(call cp_gif,AppleFalling,apple_falling)
	$(VENV) manim -ql --format gif $(SCENES) RestMotion
	$(call cp_gif,RestMotion,rest_motion)

# ── Render all Part 2 GIFs ──────────────────────────────────────────────────
gifs-part2:
	$(VENV) manim -ql --format gif $(SCENES2) GeodesicConcept
	$(call cp_gif2,GeodesicConcept,geodesic_concept)
	$(VENV) manim -ql --format gif $(SCENES2) SatelliteSpacetime
	$(call cp_gif2,SatelliteSpacetime,satellite_spacetime)
	$(VENV) manim -ql --format gif $(SCENES2) CylinderStraightLine
	$(call cp_gif2,CylinderStraightLine,cylinder_straight_line)
	$(VENV) manim -ql --format gif $(SCENES2) ParallelTransport
	$(call cp_gif2,ParallelTransport,parallel_transport)
	$(VENV) manim -ql --format gif $(SCENES2) GeodesicMath
	$(call cp_gif2,GeodesicMath,geodesic_math)

# ── Render all Part 4 GIFs ──────────────────────────────────────────────────
gifs-part4:
	$(VENV) manim -ql --format gif $(SCENES4) MetricProblem
	$(call cp_gif4,MetricProblem,metric_problem)
	$(VENV) manim -ql --format gif $(SCENES4) MetricFlatGrid
	$(call cp_gif4,MetricFlatGrid,metric_flat_grid)
	$(VENV) manim -ql --format gif $(SCENES4) MetricTensor
	$(call cp_gif4,MetricTensor,metric_tensor)
	$(VENV) manim -ql --format gif $(SCENES4) MinkowskiMetric
	$(call cp_gif4,MinkowskiMetric,minkowski_metric)
	$(VENV) manim -ql --format gif $(SCENES4) MetricGravity
	$(call cp_gif4,MetricGravity,metric_gravity)

# ── High-quality versions ───────────────────────────────────────────────────
VDIR_HQ = media/videos/part1_worldlines/720p30
cp_gif_hq = cp $(VDIR_HQ)/$(1)_ManimCE_*.gif media/$(2).gif
gifs-hq:
	$(VENV) manim -qm --format gif $(SCENES) SpacetimeGrid
	$(call cp_gif_hq,SpacetimeGrid,spacetime_grid)
	$(VENV) manim -qm --format gif $(SCENES) WorldLine
	$(call cp_gif_hq,WorldLine,world_line)
	$(VENV) manim -qm --format gif $(SCENES) AppleFalling
	$(call cp_gif_hq,AppleFalling,apple_falling)
	$(VENV) manim -qm --format gif $(SCENES) RestMotion
	$(call cp_gif_hq,RestMotion,rest_motion)

# ── Interactive preview (opens a window) ───────────────────────────────────
# Usage: make preview SCENE=AppleFalling
preview:
	$(VENV) manim -p $(SCENES) $(SCENE)

# ── Build A4 PDF ────────────────────────────────────────────────────────────
pdf:
	pandoc notes.md -o notes.pdf --pdf-engine=xelatex

# ── Create venv (Python 3.11 required; manim is not stable on 3.13) ─────────
setup:
	/opt/homebrew/bin/python3.11 -m venv .venv
	source .venv/bin/activate && pip install --upgrade pip -q
	source .venv/bin/activate && pip install -r requirements.txt

# ── Render all Part 5 GIFs ──────────────────────────────────────────────────
gifs-part5:
	$(VENV) manim -ql --format gif $(SCENES5) CurvatureConcept
	$(call cp_gif5,CurvatureConcept,curvature_concept)
	$(VENV) manim -ql --format gif $(SCENES5) CurvatureAndRiemann
	$(call cp_gif5,CurvatureAndRiemann,curvature_and_riemann)
	$(VENV) manim -ql --format gif $(SCENES5) RicciAndScalar
	$(call cp_gif5,RicciAndScalar,ricci_and_scalar)
	$(VENV) manim -ql --format gif $(SCENES5) SchwarzschildMetric
	$(call cp_gif5,SchwarzschildMetric,schwarzschild_metric)

SCENES6  = scenes/part6_einstein_equation.py
SCENES7  = scenes/part7_phenomena.py
VDIR6    = media/videos/part6_einstein_equation/480p15
VDIR7    = media/videos/part7_phenomena/480p15
cp_gif6  = cp $(VDIR6)/$(1)_ManimCE_*.gif  media/$(2).gif
cp_gif7  = cp $(VDIR7)/$(1)_ManimCE_*.gif  media/$(2).gif

# ── Render all Part 6 GIFs ──────────────────────────────────────────────────
gifs-part6:
	$(VENV) manim -ql --format gif $(SCENES6) EinsteinEquationLabeled
	$(call cp_gif6,EinsteinEquationLabeled,einstein_equation_labeled)
	$(VENV) manim -ql --format gif $(SCENES6) EquivalencePrinciple
	$(call cp_gif6,EquivalencePrinciple,equivalence_principle)

# ── Render all Part 7 GIFs ──────────────────────────────────────────────────
gifs-part7:
	$(VENV) manim -ql --format gif $(SCENES7) GPSTimeDilation
	$(call cp_gif7,GPSTimeDilation,gps_time_dilation)
	$(VENV) manim -ql --format gif $(SCENES7) BlackHoles
	$(call cp_gif7,BlackHoles,black_holes)
	$(VENV) manim -ql --format gif $(SCENES7) GravitationalWaves
	$(call cp_gif7,GravitationalWaves,gravitational_waves)
	$(VENV) manim -ql --format gif $(SCENES7) GravitationalLensing
	$(call cp_gif7,GravitationalLensing,gravitational_lensing)

.PHONY: gifs gifs-part2 gifs-part4 gifs-part5 gifs-part6 gifs-part7 gifs-hq preview pdf setup
