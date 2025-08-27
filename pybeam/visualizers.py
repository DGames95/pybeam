""" Visualizers for beam analysis results. """

from abc import ABC, abstractmethod
from pathlib import Path
import tempfile
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Arc


from .loads import PointMoment, PointForce, UniformDistributedLoad

from .analyze import BeamAnalyzer

class Visualizer(ABC):
    """ Abstract base class for visualizers, taking analysis and rendering it """
    @abstractmethod
    def render(self, analyzer):
        """ Render the analysis results """


# pylint: disable-all
# reason: this needs to be rewritten in general

class MatplotlibVisualizer(Visualizer):
    """ Visualizer using Matplotlib """
    def __init__(self,
                 show=True,
                 save=False,
                 save_folder=None,
                 fileformat="png",
                 filename_prefix="beam_analysis"):
        if save_folder is None:
            save_folder = tempfile.gettempdir()

        self.show = show
        self.save = save
        self.save_path = Path(save_folder)
        self.save_path.mkdir(parents=True, exist_ok=True)
        self.filename_prefix = filename_prefix
        self.fileformat = fileformat

    def render(self, analyzer: BeamAnalyzer):
        # Extract analysis results
        x = analyzer.points
        v = -analyzer.get_internal_shear()
        m = -analyzer.get_internal_moments()

        fig = plt.figure(figsize=(7, 8))
        gs = GridSpec(3, 1, height_ratios=[1, 1, 1], hspace=0.4)

        # 1) Load diagram
        ax_load = fig.add_subplot(gs[0])
        ax_load.plot([x[0], x[-1]], [0, 0], color='black', linewidth=4)

        # Draw Point Loads
        for load in analyzer.case.shear_loads:
            if isinstance(load, PointForce):
                pos = load.position * analyzer.length
                direction = 1 if load.magnitude > 0 else -1
                arrow_start = 0.6 * direction
                arrow_length = -0.5 * direction
                ax_load.arrow(pos, arrow_start, 0, arrow_length,
                        head_width=0.1 * analyzer.length / 10, head_length=0.1,
                        fc='red', ec='red')
                # Label the point load
                ax_load.text(pos, arrow_start + 0.2 * direction,
                        f'{load.magnitude:.1f} N',
                        color='red', ha='center', va='bottom' if direction < 0 else 'top',
                        fontsize=9)

        # --- draw normal (axial) point-loads ----------------------------------------
        for load in analyzer.case.axial_loads:
            if isinstance(load, PointForce):
                normal_force_x = load.position * analyzer.length           # application point along the beam
                direction = 1 if load.magnitude >= 0 else -1   # +1 → (tension), −1 ← (compression)

                # arrow geometry ------------------------------------------------------
                shaft_dx = 0.05 * analyzer.length * direction      # length of arrow shaft
                tail_x   = normal_force_x - shaft_dx                        # start so head ends at x
                tail_y   = 0                                   # on the beam axis
                head_w   = 0.1 * analyzer.length                  # arrow-head height (vertical)
                head_l   = 0.02 * analyzer.length                  # arrow-head length (horizontal)

                ax_load.arrow(tail_x, tail_y,        # tail of arrow
                        shaft_dx, 0,            # dX (horizontal), dY
                        head_width=head_w,
                        head_length=head_l,
                        fc='red', ec='red',
                        length_includes_head=True)

                # label slightly above the beam axis
                ax_load.text(normal_force_x,
                        tail_y + 0.06 * analyzer.length,
                        f'{load.magnitude:.1f} N',
                        color='red',
                        ha='center', va='bottom',
                        fontsize=9)
        
        for load in analyzer.case.point_moments:
            if isinstance(load, PointMoment):
                x_moment = load.position * analyzer.length
                m_moment = load.magnitude
                direction = 1 if m_moment < 0 else -1  # -1: clockwise, 1: counterclockwise

                # Set up arrow arc parameters
                radius = 0.5 * direction
                theta1, theta2 = (0, 270) if direction > 0 else (90, -180)  # degrees

                arc = Arc(
                    (x_moment, 0),                   # center
                    width=0.4, height=0.4,    # size of arc
                    angle=0,
                    theta1=theta1, theta2=theta2,
                    color='purple', linewidth=2
                )
                # ax_load.gca().add_patch(arc)

                # Arrowhead position (manually placed at the end of arc)
                head_dx = 0.05 * direction
                ax_load.arrow(x_moment * direction, 0.2,
                        dx=-head_dx, dy=0,
                        head_width=0.05, head_length=0.05,
                        fc='purple', ec='purple')

                # Label moment value
                ax_load.text(x_moment, 0.3 * direction,
                        f'M = {m_moment:.1f} Nm',
                        color='purple', ha='center',
                        va='bottom' if direction > 0 else 'top',
                        fontsize=9,
                        bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.7))


        # Draw Uniform Distributed Loads (as arrows)
        for load in analyzer.case.shear_loads:

            # --- Uniform Distributed Loads ---------------------------------------------
            if isinstance(load, UniformDistributedLoad):
                start = load.start * analyzer.length
                end   = load.end   * analyzer.length

                # High‑resolution abscissa in real beam coordinates
                x_dist = np.linspace(start, end, 100)

                # Constant load values (N/m) over that interval
                load_values = np.full_like(x_dist, load.w)

                # Scale to a 0.4‑height envelope so it matches the XFLR5 plot
                max_abs = np.max(np.abs(load_values)) or 1          # avoid divide‑by‑zero
                y_curve = load_values / max_abs * 0.1               # (+) up, (–) down

                # Filled patch + outline
                ax_load.fill_between(x_dist, 0, y_curve,
                                alpha=0.3, color='blue',
                                label='Weight')
                ax_load.plot(x_dist, y_curve, color='blue', linewidth=2)

                # Centre label (same style you already use)
                center_x = (start + end) / 2
                label_y  = y_curve[0] + (0.1 if y_curve[0] < 0 else -0.1)
                ax_load.text(center_x, label_y,
                        f'w = {load.w:.1f} N/m',
                        color='blue', ha='center',
                        va='top' if y_curve[0] < 0 else 'bottom',
                        fontsize=9,
                        bbox=dict(boxstyle="round,pad=0.3",
                                facecolor='white', alpha=0.7))

        ax_load.set_xlim(-0.1 * analyzer.length, 1.1 * analyzer.length)
        ax_load.set_ylim(-1, 1)
        ax_load.set_yticks([])
        ax_load.set_xlabel('Position (m)')
        ax_load.set_ylabel('Load Intensity')
        ax_load.grid(True, alpha=0.3)
        ax_load.legend()
        plt.tight_layout()

        # 2) Shear diagram
        ax_shear = fig.add_subplot(gs[1], sharex=ax_load)
        ax_shear.plot(x, v, 'b-', linewidth=2, label='Shear Force')
        ax_shear.fill_between(x, 0, v, alpha=0.3, color='blue')
        ax_shear.axhline(0, color='black', alpha=0.3)
        ax_shear.set_ylabel('Shear\nforce (N)')
        ax_shear.grid(True, alpha=0.3)
        ax_shear.legend()

        # 3) Moment diagram
        ax_moment = fig.add_subplot(gs[2], sharex=ax_shear)
        ax_moment.plot(x, m, 'r-', linewidth=2, label='Bending Moment')
        ax_moment.fill_between(x, 0, m, alpha=0.3, color='red')
        ax_moment.axhline(0, color='black', alpha=0.3)
        ax_moment.set_xlabel('Position (m)')
        ax_moment.set_ylabel('Bending\nmoment (N·m)')
        ax_moment.grid(True, alpha=0.3)
        ax_moment.legend()

        fig.tight_layout()

        if self.show:
            plt.show()


        full_path = str(self.save_path) \
                    + f"/{self.filename_prefix}_combined_diagrams.{str(self.fileformat)}"
        
        if self.save:
            fig.savefig(full_path,
                        format=self.fileformat,
                        dpi=300)
            print(f"Saved diagram to: {self.save_path}")
