# Localization

### Introduction
Localization package provides tools for multilateration and triangulation in `2D` and `3D`

### Installation
Use pip to install the package:
```
pip install localization
```
### Usage

Typical usage of the package is:

```python
import localization as lx
```
To initilaize new localization Project use:

```python
P=lx.Project(mode=<mode>,solver=<solver>)
```

Currently two modes are supported:
 - 2D
 - 3D

Also three solvers can be used:
 - LSE for least square error
 - LSE_GC for least square error with geometric constraints. Geometric constraints force the solutions to be in the intersection areas of all multilateration circles.

To add anchors to the project use:

```python
P.add_anchor(<name>,<loc>)
```

where name denote user provided label of the anchor and <loc> is the location of the anchor provided in tuple, e.g., (120,60).

To add target use:

```python
t,label=P.add_target()
```

t is the target object and label is the package provided label for the target.

Distance measurements must be added to target object like:

```python
t.add_measure(<anchore_lable>,<measured_distance>)
```

Finally running P.solve() will locate all targets. You can access the estimated location of the target t by t.loc.
t.loc is a point object. Point object `B` has `x`,`y`,`z` coordinates available by `B.x`, `B.y`, `B.z` respectively.

Here is a sample use of the package for three anchors and one target scenario:

```python
import localization as lx

P=lx.Project(mode='2D',solver='LSE')


P.add_anchor('anchore_A',(0,100))
P.add_anchor('anchore_B',(100,100))
P.add_anchor('anchore_C',(100,0))

t,label=P.add_target()

t.add_measure('anchore_A',50)
t.add_measure('anchore_B',50)
t.add_measure('anchore_C',50)

P.solve()

# Then the target location is:

t.loc
```
