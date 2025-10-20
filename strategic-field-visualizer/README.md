# Strategic Field Visualizer

> **Visualizing the Strategic Field: From Abstract Rules to Living Patterns**

This repository contains code to generate visualizations of spatial evolutionary games, demonstrating how simple local rules give rise to complex emergent patterns in strategic interactions.

## 🎯 Key Visualizations

The code generates four fundamental patterns that reveal the "Strategic Field":

1. **Prisoner's Dilemma**: Cooperative cluster formation through spatial reciprocity
2. **Hawk-Dove**: Flickering equilibrium patterns in resource competition  
3. **Stag Hunt**: Cluster expansion dynamics showing critical mass effects
4. **Stag Hunt**: Coordination cascades above the tipping point

## 🚀 Quick Start

### Requirements
```bash
pip install numpy matplotlib imageio tqdm
```

### Generate All Visualizations
```python
python strategic_field_visualizer.py
```

This creates animated GIFs in the `visualizations/` directory showing the evolution of strategic patterns over time.

### Interactive Lab
Open `CA4.html` in your browser for an interactive exploration of the models with real-time parameter adjustment.

## 🧬 The Science

### Cellular Automaton Model
- **Grid**: 2D toroidal lattice (no edge effects)
- **Strategies**: Binary (Cooperate/Defect, Hawk/Dove, Stag/Hare)
- **Update Rule**: "Best takes over" - each cell adopts the strategy of its most successful neighbor
- **Neighborhood**: Moore (8 neighbors + self)

### Game Types

#### Prisoner's Dilemma
Models cooperation vs. defection with payoffs:
- **R** (Reward): Both cooperate
- **T** (Temptation): I defect, you cooperate  
- **P** (Punishment): Both defect
- **S** (Sucker): I cooperate, you defect

*Key insight*: Spatial structure allows cooperation to survive through cluster formation.

#### Hawk-Dove
Models conflict over resources:
- **V**: Value of resource
- **C**: Cost of fighting
- When V > C: Hawks dominate
- When V < C: Dynamic equilibrium with beautiful spiral patterns

#### Stag Hunt  
Models coordination and trust:
- **High reward** for mutual cooperation (hunting stag together)
- **Safe option** of individual action (hunting hare alone)
- Demonstrates tipping points and critical mass effects

## 🎨 Customization

### Create Your Own Visualization
```python
from strategic_field_visualizer import StrategicAutomaton

# Custom Prisoner's Dilemma
sim = StrategicAutomaton(
    grid_size=100,
    game_type='prisoner_clusters',
    initial_condition='random',
    initial_coop_density=0.3
)

sim.run_and_save_gif(
    frames=200,
    filename='my_simulation.gif',
    fps=15
)
```

### Available Parameters
- `grid_size`: Size of square grid (default: 150)
- `game_type`: `'prisoner_clusters'`, `'hawk_dove_spirals'`, `'stag_hunt'`
- `initial_condition`: `'random'`, `'split'`, `'clusters'`, `'invader'`
- `initial_coop_density`: Proportion of initial cooperators (0.0-1.0)

## 📊 Interactive Lab Features

The HTML lab (`CA4.html`) provides:
- **Real-time simulation** with asynchronous updates
- **Parameter adjustment** for all payoff values
- **Multiple scenarios** for each game type
- **Population dynamics** and productivity charts
- **Speed control** and noise adjustment
- **Educational tooltips** explaining each concept

## 🔬 Technical Details

### Synchronous vs. Asynchronous Models
- **Article GIFs**: Use synchronous updates (all cells update simultaneously) for classic crystalline patterns
- **Interactive Lab**: Uses asynchronous updates (one cell at a time) for more realistic, organic territories

### Performance Notes
- Grid sizes up to 200x200 run smoothly
- GIF generation is memory-intensive for long simulations
- Consider reducing `frames` or `grid_size` for faster generation

## 📚 Theoretical Background

This work builds on foundational research in:
- **Evolutionary Game Theory** (Maynard Smith & Price, 1973)
- **Spatial Games** (Nowak & May, 1992)  
- **Cellular Automata** (von Neumann, 1940s)
- **Complex Systems** (Wolfram, 2002)

### Key References
- Nowak, M. A., & May, R. M. (1992). "Evolutionary games and spatial chaos." *Nature*, 359.
- Axelrod, R. (1984). *The Evolution of Cooperation*.
- Maynard Smith, J., & Price, G. R. (1973). "The logic of animal conflict." *Nature*, 246.

## 🤝 Contributing

Contributions welcome! Areas for enhancement:
- Additional game types (Public Goods, Rock-Paper-Scissors)
- Alternative update rules (replicator dynamics, Moran process)
- Network topologies beyond 2D grids
- Performance optimizations

## 📄 License

MIT License - feel free to use for research, education, or commercial projects.

## 🎓 Educational Use

Perfect for:
- **Game Theory courses**: Visualizing abstract concepts
- **Complex Systems classes**: Demonstrating emergence
- **Research presentations**: Clear, compelling animations
- **Public outreach**: Making game theory accessible

---

*"We get macro-surprises despite complete micro-knowledge"* - Joshua Epstein
