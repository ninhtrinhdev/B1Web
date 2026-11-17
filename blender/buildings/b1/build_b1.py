"""Build the exterior of HUST building B1 in Blender from an OpenStreetMap export.

Footprint and per-part heights come from OSM (way 184021007 + its building:part ways);
facade articulation follows the reference photos in the project root. The model is
assembled from the modules in ./b1 (wings, lobby, tower, rooftop, context, scene),
each piece landing in its own object/collection under "B1_OSM".

Run headless from the repository root (Windows and Linux alike):
    blender -b blender/buildings/b1/B1.blend -P blender/buildings/b1/build_b1.py
    (optional: -- path/to/map.osm ; default is blender/data/map.osm)
Re-running rebuilds only the "B1_OSM" collection and reloads the b1 package.
"""
import os
import sys

import bpy

# When pasted into Blender's text editor __file__ is missing: fall back to the folder of the open .blend.
HERE = os.path.dirname(os.path.abspath(globals().get('__file__') or bpy.data.filepath))
OSM_PATH = globals().get('OSM_PATH') or os.path.join(HERE, '..', '..', 'data', 'map.osm')
if '--' in sys.argv and len(sys.argv) > sys.argv.index('--') + 1 and sys.argv[sys.argv.index('--') + 1].endswith('.osm'):
    OSM_PATH = sys.argv[sys.argv.index('--') + 1]

if HERE not in sys.path:
    sys.path.insert(0, HERE)
for name in [m for m in sys.modules if m == 'b1' or m.startswith('b1.')]:
    del sys.modules[name]

from b1.main import run  # noqa: E402

run(OSM_PATH)
