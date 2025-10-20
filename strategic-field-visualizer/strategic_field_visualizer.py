"""
Strategic Field Visualizer
==========================

A clean implementation for generating visualizations of spatial evolutionary games
as described in "Visualizing the Strategic Field: From Abstract Rules to Living Patterns"

This code generates the four key visualizations:
1. Prisoner's Dilemma: Cooperative cluster formation
2. Hawk-Dove: Flickering equilibrium patterns  
3. Stag Hunt: Cluster expansion dynamics
4. Stag Hunt: Coordination cascade success

Author: Strategic Field Research
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import imageio.v2 as imageio
from tqdm import tqdm
import os
import io


class StrategicAutomaton:
    """
    Cellular automaton for spatial evolutionary games.
    
    Implements the "best takes over" update rule where each cell adopts
    the strategy of its most successful neighbor (including itself).
    """
    
    COOPERATE = 0
    DEFECT = 1
    
    def __init__(self, grid_size=150, game_type='prisoner_clusters', 
                 initial_condition='random', initial_coop_density=0.5, invader_size=5):
        """
        Initialize the strategic automaton.
        
        Args:
            grid_size: Size of the square grid
            game_type: Type of game ('prisoner_clusters', 'hawk_dove_spirals', 'stag_hunt')
            initial_condition: How to initialize ('random', 'split', 'clusters', 'invader')
            initial_coop_density: Proportion of initial cooperators (for random init)
            invader_size: Size of invader cluster (for invader init)
        """
        self.grid_size = grid_size
        self.game_type = game_type
        self.payoffs = self._get_payoffs(game_type)
        self.grid = self._initialize_grid(initial_condition, initial_coop_density, invader_size)
        # Blue for cooperators, orange for defectors
        self.cmap = mcolors.ListedColormap(['#1f77b4', '#ff7f0e'])
    
    def _initialize_grid(self, condition, density, invader_size):
        """Initialize the grid based on specified condition."""
        if condition == 'random':
            return np.random.choice([self.COOPERATE, self.DEFECT], 
                                  size=(self.grid_size, self.grid_size), 
                                  p=[density, 1 - density])
        
        elif condition == 'split':
            grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
            grid[:, self.grid_size // 2:] = self.DEFECT
            return grid
        
        elif condition == 'invader':
            grid = np.full((self.grid_size, self.grid_size), self.COOPERATE, dtype=int)
            center = self.grid_size // 2
            half_size = invader_size // 2
            grid[center - half_size : center + half_size + 1, 
                 center - half_size : center + half_size + 1] = self.DEFECT
            return grid
        
        elif condition == 'clusters':
            # Create initial clusters for stag hunt expansion
            grid = np.full((self.grid_size, self.grid_size), self.DEFECT, dtype=int)
            centers = [(30, 30), (120, 40), (70, 100), (40, 120)]
            for cy, cx in centers:
                for dy in range(-8, 9):
                    for dx in range(-8, 9):
                        if dy*dy + dx*dx <= 64:  # Circle
                            y, x = (cy + dy) % self.grid_size, (cx + dx) % self.grid_size
                            grid[y, x] = self.COOPERATE
            return grid
        
        else:
            raise ValueError(f"Invalid initial condition: {condition}")
    
    def _get_payoffs(self, game_type):
        """Get payoff matrix for specified game type."""
        if game_type == 'prisoner_clusters':
            # Weak PD parameters allowing stable cluster formation
            return {'R': 3, 'T': 3.1, 'P': 1, 'S': 0}
        
        elif game_type == 'hawk_dove_spirals':
            # V < C for flickering equilibrium patterns
            V, C = 3.5, 4.5
            return {'V/2': V/2, 'V': V, '0': 0, '(V-C)/2': (V-C)/2}
        
        elif game_type == 'stag_hunt':
            # Adjusted for visible expansion dynamics
            return {'Stag': 4, 'Hare': 2.5, 'Sucker': 0, 'BothHare': 1.5}
        
        else:
            raise ValueError(f"Invalid game type: {game_type}")
    
    def _get_fitness(self, y, x, current_grid):
        """Calculate fitness for cell at position (y, x)."""
        my_strategy = current_grid[y, x]
        score = 0
        p = self.payoffs
        
        # Sum payoffs from interactions with 8 neighbors
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy == 0 and dx == 0:
                    continue
                
                # Toroidal boundary conditions
                ny, nx = (y + dy) % self.grid_size, (x + dx) % self.grid_size
                neighbor_strategy = current_grid[ny, nx]
                
                # Calculate payoff based on game type
                if 'prisoner' in self.game_type:
                    if my_strategy == self.COOPERATE:
                        score += p['R'] if neighbor_strategy == self.COOPERATE else p['S']
                    else:
                        score += p['T'] if neighbor_strategy == self.COOPERATE else p['P']
                
                elif 'hawk_dove' in self.game_type:
                    if my_strategy == self.COOPERATE:  # Dove
                        score += p['V/2'] if neighbor_strategy == self.COOPERATE else p['0']
                    else:  # Hawk
                        score += p['V'] if neighbor_strategy == self.COOPERATE else p['(V-C)/2']
                
                elif 'stag_hunt' in self.game_type:
                    if my_strategy == self.COOPERATE:  # Stag Hunter
                        score += p['Stag'] if neighbor_strategy == self.COOPERATE else p['Sucker']
                    else:  # Hare Hunter
                        score += p['Hare'] if neighbor_strategy == self.COOPERATE else p['BothHare']
        
        return score
    
    def step(self):
        """Execute one time step using 'best takes over' rule."""
        # Calculate fitness for all cells
        fitness_grid = np.array([[self._get_fitness(y, x, self.grid) 
                                for x in range(self.grid_size)] 
                               for y in range(self.grid_size)])
        
        # Create new grid
        next_grid = self.grid.copy()
        
        # Each cell adopts strategy of fittest neighbor (including itself)
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                max_fitness = -np.inf
                best_strategy = -1
                
                # Check all neighbors including self
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        ny, nx = (y + dy) % self.grid_size, (x + dx) % self.grid_size
                        if fitness_grid[ny, nx] > max_fitness:
                            max_fitness = fitness_grid[ny, nx]
                            best_strategy = self.grid[ny, nx]
                
                next_grid[y, x] = best_strategy
        
        self.grid = next_grid
    
    def run_and_save_gif(self, frames, filename, final_pause_frames=0, fps=20):
        """
        Run simulation and save as animated GIF.
        
        Args:
            frames: Number of generations to simulate
            filename: Output filename
            final_pause_frames: Extra frames to pause at end
            fps: Frames per second for GIF
        """
        print(f"Generating {frames} frames for '{self.game_type}'...")
        images = []
        fig, ax = plt.subplots(figsize=(8, 8), dpi=150)
        
        for i in tqdm(range(frames), desc="Simulating"):
            self.step()
            ax.clear()
            ax.imshow(self.grid, cmap=self.cmap, interpolation='nearest')
            ax.set_title(f'{self.game_type.replace("_", " ").title()} - Generation {i+1}', 
                        fontsize=14)
            ax.set_xticks([])
            ax.set_yticks([])
            
            # Save frame
            fig.canvas.draw()
            buf = io.BytesIO()
            fig.savefig(buf, format='png', bbox_inches='tight')
            buf.seek(0)
            images.append(imageio.imread(buf))
            buf.close()
        
        # Add pause frames
        for _ in range(final_pause_frames):
            images.append(images[-1])
        
        plt.close(fig)
        
        print(f"Saving GIF to {filename}...")
        imageio.mimsave(filename, images, fps=fps)
        print(f"✓ Saved {filename}")


def generate_all_visualizations(output_dir='visualizations'):
    """Generate all four key visualizations for the article."""
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("🎬 Generating Strategic Field Visualizations")
    print("=" * 50)
    
    # 1. Prisoner's Dilemma: Cooperative Clusters
    print("\n1. Prisoner's Dilemma: Cooperative Cluster Formation")
    pd_sim = StrategicAutomaton(
        grid_size=150, 
        game_type='prisoner_clusters',
        initial_condition='random',
        initial_coop_density=0.5
    )
    pd_sim.run_and_save_gif(
        frames=150, 
        filename=f'{output_dir}/pd_cooperative_clusters.gif',
        final_pause_frames=40
    )
    
    # 2. Hawk-Dove: Flickering Equilibrium
    print("\n2. Hawk-Dove: Flickering Equilibrium Patterns")
    hd_sim = StrategicAutomaton(
        grid_size=200,
        game_type='hawk_dove_spirals', 
        initial_condition='random'
    )
    hd_sim.run_and_save_gif(
        frames=300,
        filename=f'{output_dir}/hd_flickering_equilibrium.gif'
    )
    
    # 3. Stag Hunt: Cluster Expansion
    print("\n3. Stag Hunt: Cluster Expansion Dynamics")
    sh_expansion = StrategicAutomaton(
        grid_size=150,
        game_type='stag_hunt',
        initial_condition='clusters'
    )
    sh_expansion.run_and_save_gif(
        frames=200,
        filename=f'{output_dir}/sh_cluster_expansion.gif',
        final_pause_frames=30,
        fps=10  # Slower for better visibility
    )
    
    # 4. Stag Hunt: Coordination Cascade Success
    print("\n4. Stag Hunt: Coordination Cascade Success")
    sh_success = StrategicAutomaton(
        grid_size=150,
        game_type='stag_hunt',
        initial_condition='random',
        initial_coop_density=0.52  # Above tipping point
    )
    sh_success.run_and_save_gif(
        frames=150,
        filename=f'{output_dir}/sh_coordination_cascade.gif',
        final_pause_frames=30,
        fps=10
    )
    
    print("\n" + "=" * 50)
    print("🎉 All visualizations generated successfully!")
    print(f"📁 Files saved in: {output_dir}/")


if __name__ == '__main__':
    generate_all_visualizations()
