"""Giang duong (lecture hall) of B1: curved, theatre-style, orchestra + balcony, on floor 3 in the middle.

The hall sits inside the fan-shaped central part of B1 (OSM building:part 1207082389: apex at the south,
curved lobby arc to the north). Seat rows are concentric arcs about the arc's centre C; the stage is the
apex end and has a curved back wall; a balcony deck covers the rear rows and carries three more rows.
Floor level = top of storey 2 (= floor 3); ceiling just under the roof of that part.
All coordinates are model metres (same frame as the exterior).
"""
import math

import bpy
from mathutils import Vector

from . import config
from .config import ENTRANCE_PART, level_top
from .materials import principled
from .meshkit import MB, collection, prism

WALL_T = 0.35
STAGE_H = 0.45
STAGE_DEPTH = 1.6      # platform depth in front of the board (m)
STAGE_MARGIN = 0.6     # platform extends this far past each end of the board (m)
FLOOR0 = 0.15          # top of the first seating row above the hall floor
ORCH_RISE = 0.12       # riser of the orchestra rows
R_STAGE = 3.2          # stage back wall sits this far (along the axis) past the apex
R_ROW0 = 12.3          # first orchestra row radius (from C)
ROW_T = 1.0            # tread depth
N_ORCH = 7
N_BAL = 5              # balcony rows: the deck overhangs most of the orchestra rows
BAL_RISE = 0.2
BAL_Z = 3.7            # balcony deck top above the hall floor
SLAB_T = 0.4
H_CEIL = 6.9
SEAT_W = 0.52
AISLE_ANG = math.radians(13)   # aisle centre-lines at +/- this angle from the axis
AISLE_W = 1.2


def make_auditorium_materials():
    principled('B1_AudWood', (0.30, 0.10, 0.04), 0.45)
    principled('B1_AudWoodLight', (0.62, 0.38, 0.17), 0.45)
    principled('B1_AudStageWood', (0.42, 0.17, 0.06), 0.4)       # glossy orange-brown stage boards
    principled('B1_AudFrame', (0.70, 0.70, 0.72), 0.3, 0.6)      # screen / board / door frames
    principled('B1_AudFloor', (0.50, 0.50, 0.49), 0.85)          # grey concrete floor
    principled('B1_AudWall', (0.80, 0.74, 0.62), 0.85)
    principled('B1_AudCeiling', (0.88, 0.88, 0.86), 0.9)
    principled('B1_AudBoard', (0.015, 0.05, 0.055), 0.45)        # blue-black chalkboard under the projection screen
    principled('B1_AudConcrete', (0.55, 0.55, 0.54), 0.9)        # balcony parapet
    principled('B1_AudGlass', (0.35, 0.45, 0.5), 0.1)
    principled('B1_AudSign', (0.05, 0.6, 0.2), 0.4, emission=((0.1, 0.9, 0.3), 2.0))
    principled('B1_AudSpeaker', (0.02, 0.02, 0.025), 0.6)
    principled('B1_AudScreen', (0.92, 0.92, 0.94), 0.5, emission=((0.9, 0.92, 0.95), 0.6))
    principled('B1_AudDoor', (0.40, 0.22, 0.10), 0.5)
    principled('B1_AudRail', (0.55, 0.56, 0.58), 0.3, 1.0)


def circumcenter(a, b, c):
    d = 2 * (a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y))
    ux = ((a.x ** 2 + a.y ** 2) * (b.y - c.y) + (b.x ** 2 + b.y ** 2) * (c.y - a.y) + (c.x ** 2 + c.y ** 2) * (a.y - b.y)) / d
    uy = ((a.x ** 2 + a.y ** 2) * (c.x - b.x) + (b.x ** 2 + b.y ** 2) * (a.x - c.x) + (c.x ** 2 + c.y ** 2) * (b.x - a.x)) / d
    return Vector((ux, uy))


class Fan:
    """Geometry of the fan: centre C, axis angle, inset side lines, helpers for polar placement."""

    def __init__(self, pts):
        self.A, self.E_e, self.E_w = pts[0], pts[1], pts[8]
        self.C = circumcenter(self.E_e, pts[4], self.E_w)
        self.R = (self.E_e - self.C).length
        m = (pts[4] + pts[5]) / 2 - self.C
        self.th0 = math.atan2(m.y, m.x)
        axis_pt = self.pol(self.R * 0.7, self.th0)
        self.lines = []
        for E in (self.E_e, self.E_w):
            d = (E - self.A).normalized()
            n = Vector((-d.y, d.x))
            if n.dot(axis_pt - self.A) < 0:
                n = -n
            self.lines.append((self.A + n * WALL_T, d))
        self.R_IN = self.R - WALL_T
        self.r_apex = (self.A - self.C).length
        self.R_CUT = self.r_apex + R_STAGE
        lo, hi = self.span(self.R_IN)          # centre the axis between the side walls so the hall is symmetric
        self.th0 += (lo + hi) / 2

    def pol(self, r, th):
        return Vector((self.C.x + r * math.cos(th), self.C.y + r * math.sin(th)))

    def edge_pt(self, k, r):
        p0, d = self.lines[k]
        b = d.dot(p0 - self.C)
        c = (p0 - self.C).length_squared - r * r
        s = -b + math.sqrt(max(b * b - c, 0.0))
        return p0 + d * s

    def rel(self, p):
        a = math.atan2(p.y - self.C.y, p.x - self.C.x) - self.th0
        return (a + math.pi) % (2 * math.pi) - math.pi

    def span(self, r):
        a, b = self.rel(self.edge_pt(0, r)), self.rel(self.edge_pt(1, r))
        return min(a, b), max(a, b)

    def arc(self, r, t0, t1, step=0.45):
        n = max(2, int(abs(t1 - t0) * r / step))
        return [self.pol(r, self.th0 + t0 + (t1 - t0) * i / n) for i in range(n + 1)]

    def ring(self, r0, r1):
        """Polygon of the annulus r0..r1 clipped by the inset side lines (edges run along the walls)."""
        lo1, hi1 = self.span(r1)
        lo0, hi0 = self.span(r0)
        return self.arc(r1, lo1, hi1) + self.arc(r0, hi0, lo0)

    def outline(self):
        lo_c, hi_c = self.span(self.R_CUT)
        lo_a, hi_a = self.span(self.R_IN)
        return (self.arc(self.R_IN, lo_a, hi_a) +             # curved rear wall, then side walls to the stage wall
                list(reversed(self.arc(self.R_CUT, lo_c, hi_c))))


def build_auditorium(root, info):
    make_auditorium_materials()
    part = info[ENTRANCE_PART]
    fan = Fan(part['pts'])
    z0 = level_top(2)               # hall floor = floor 3
    ztop = z0 + H_CEIL
    coll = collection(root, 'B1_Auditorium')
    th0, C = fan.th0, fan.C

    outline = fan.outline()
    cen = sum(outline, Vector((0, 0))) / len(outline)

    # ---------------- shell ----------------
    shell = MB('B1_AudShell')
    prism(shell, outline, z0 - 0.4, z0, 'B1_AudFloor')
    for i in range(N_ORCH):                         # stepped orchestra floor
        r0 = R_ROW0 + i * ROW_T
        prism(shell, fan.ring(r0, min(r0 + ROW_T, fan.R_IN)), z0, z0 + FLOOR0 + i * ORCH_RISE, 'B1_AudFloor')
    # walls (all outline edges), wood lower / cream upper, plus vertical battens
    n_edges = len(outline)
    for i in range(n_edges):
        a, b = outline[i], outline[(i + 1) % n_edges]
        if (b - a).length < 1e-3:
            continue
        e = b - a
        nrm = Vector((e.y, -e.x)).normalized()
        if nrm.dot(a - cen) < 0:
            nrm = -nrm
        prism(shell, [a, b, b + nrm * WALL_T, a + nrm * WALL_T], z0, ztop, 'B1_AudWall')
        prism(shell, [a, b, b - nrm * 0.06, a - nrm * 0.06], z0, z0 + 4.6, 'B1_AudWood')
        length = e.length
        u = e / length
        for k in range(int(length / 0.9)):
            s = 0.45 + k * 0.9
            prism(shell, [a + u * s, a + u * (s + 0.05), a + u * (s + 0.05) - nrm * 0.11, a + u * s - nrm * 0.11],
                  z0, z0 + 4.6, 'B1_AudWood')
    shell.build(coll)

    ceil = MB('B1_AudCeiling')
    prism(ceil, outline, ztop, ztop + 0.25, 'B1_AudCeiling')
    for k in range(1, 5):                           # ceiling beams (radial bands)
        r = fan.R_CUT + (fan.R_IN - fan.R_CUT) * k / 5
        prism(ceil, fan.ring(r - 0.2, r + 0.2), ztop - 0.35, ztop, 'B1_AudCeiling')
    ceil.build(coll)

    # ---------------- stage + front wall dressing ----------------
    stage = MB('B1_AudStage')
    # fan-shaped raised platform, narrower than the hall: the strips beside it (and the doors) stay at floor level
    lo_s, hi_s = fan.span(fan.R_CUT + 0.2)
    sa = min((2.3 + STAGE_MARGIN) / fan.R_CUT, -lo_s, hi_s) - 0.03   # just wider than the board
    r_front = fan.R_CUT + STAGE_DEPTH      # shallow strip against the board, not reaching into the hall

    def sector(r0, r1, t0, t1):
        return fan.arc(r1, t0, t1, 0.2) + fan.arc(r0, t1, t0, 0.2)

    prism(stage, sector(fan.R_CUT, r_front, -sa, sa), z0, z0 + STAGE_H, 'B1_AudStageWood')
    for ra, rb, hz in ((r_front, r_front + 0.3, 0.30), (r_front + 0.3, r_front + 0.6, 0.15)):
        prism(stage, sector(ra, rb, sa - 0.14, sa), z0, z0 + hz, 'B1_AudStageWood')                     # 2 steps
    pol = fan.pol
    stage.build(coll)

    front = MB('B1_AudFront')
    w = 2.0 / fan.R_CUT
    prism(front, fan.arc(fan.R_CUT + 0.17, -w, w, 0.2) + fan.arc(fan.R_CUT, w, -w, 0.2), z0 + STAGE_H + 2.7, z0 + STAGE_H + 6.2, 'B1_AudScreen')
    wf = 2.1 / fan.R_CUT      # screen frame
    prism(front, fan.arc(fan.R_CUT + 0.14, -wf, wf, 0.2) + fan.arc(fan.R_CUT, wf, -wf, 0.2), z0 + STAGE_H + 2.6, z0 + STAGE_H + 6.3, 'B1_AudFrame')
    w2 = 2.3 / fan.R_CUT      # whiteboard
    prism(front, fan.arc(fan.R_CUT + 0.15, -w2, w2, 0.2) + fan.arc(fan.R_CUT, w2, -w2, 0.2), z0 + STAGE_H + 0.7, z0 + STAGE_H + 2.4, 'B1_AudFrame')
    w3 = 2.2 / fan.R_CUT
    prism(front, fan.arc(fan.R_CUT + 0.18, -w3, w3, 0.2) + fan.arc(fan.R_CUT, w3, -w3, 0.2), z0 + STAGE_H + 0.78, z0 + STAGE_H + 2.32, 'B1_AudBoard')
    for sgn in (-1, 1):       # loudspeakers hung on the back wall beside the screen
        ang = 0.30 * sgn
        prism(front, [fan.pol(fan.R_CUT + 0.15, th0 + ang - 0.025), fan.pol(fan.R_CUT + 0.15, th0 + ang + 0.025),
                      fan.pol(fan.R_CUT + 0.6, th0 + ang + 0.025), fan.pol(fan.R_CUT + 0.6, th0 + ang - 0.025)],
              z0 + STAGE_H + 3.4, z0 + STAGE_H + 4.4, 'B1_AudSpeaker')
    for k, ed in enumerate((0, 1)):                 # side doors next to the stage
        a = fan.edge_pt(ed, fan.R_CUT + 1.0)
        b = fan.edge_pt(ed, fan.R_CUT + 2.1)
        inw = (cen - a)
        nin = Vector((-(b - a).y, (b - a).x)).normalized()
        if nin.dot(inw) < 0:
            nin = -nin
        prism(front, [a, b, b + nin * 0.1, a + nin * 0.1], z0, z0 + 2.1, 'B1_AudFrame')
        u = (b - a) / (b - a).length
        for s0, s1 in ((0.08, 0.52), (0.58, 1.02)):     # two glazed leaves
            prism(front, [a + u * s0, a + u * s1, a + u * s1 + nin * 0.13, a + u * s0 + nin * 0.13],
                  z0 + 0.1, z0 + 2.0, 'B1_AudGlass')
        c = (a + b) / 2
        prism(front, [c - u * 0.3, c + u * 0.3, c + u * 0.3 + nin * 0.12, c - u * 0.3 + nin * 0.12],
              z0 + 2.25, z0 + 2.45, 'B1_AudSign')                           # EXIT sign
    # faceted "diamond" wood panels above the stage doors, both side walls (as in the reference photo)
    TILE, DEPTH, PANEL_W = 0.8, 0.16, 3.2
    for ed in (0, 1):
        u = (fan.edge_pt(ed, fan.R_CUT + 6.2) - fan.edge_pt(ed, fan.R_CUT + 0.5)).normalized()
        cd = (fan.edge_pt(ed, fan.R_CUT + 1.0) + fan.edge_pt(ed, fan.R_CUT + 2.1)) / 2   # door centre
        a = cd - u * PANEL_W / 2                     # column of diamonds exactly above the door
        b = a + u * PANEL_W
        nin = Vector((-u.y, u.x))
        if nin.dot(cen - a) < 0:
            nin = -nin
        zb = z0 + 2.55
        for ci in range(int((b - a).length / TILE)):
            for ri in range(int((ztop - 0.4 - zb) / TILE)):
                p0, p1 = a + u * (ci * TILE), a + u * ((ci + 1) * TILE)
                za, zc = zb + ri * TILE, zb + (ri + 1) * TILE
                base = nin * 0.06
                pm = (p0 + p1) / 2 + nin * (0.06 + DEPTH)
                apex = (pm.x, pm.y, (za + zc) / 2)
                c = [(p0.x + base.x, p0.y + base.y, za), (p1.x + base.x, p1.y + base.y, za),
                     (p1.x + base.x, p1.y + base.y, zc), (p0.x + base.x, p0.y + base.y, zc)]
                for k in range(4):
                    front.face([c[k], c[(k + 1) % 4], apex], 'B1_AudWood', (nin.x, nin.y, 0.0))
    front.build(coll)

    # ---------------- seating ----------------
    desks, chairs = MB('B1_AudDesks'), MB('B1_AudChairs')

    def seat_row(r, zr, covered_by_aisles=True):
        """Desks + chairs for the row whose tread starts at radius r (chairs face the stage)."""
        lo, hi = fan.span(r + ROW_T * 0.5)
        lo += 0.35 / r
        hi -= 0.35 / r
        ah = AISLE_W / 2 / (r + 0.5)
        blocks = [(lo, -AISLE_ANG - ah), (-AISLE_ANG + ah, AISLE_ANG - ah), (AISLE_ANG + ah, hi)]
        for t0, t1 in blocks:
            if t1 - t0 < 0.05:
                continue
            # stage side is small r: the desk is the front part of the tread, the seat sits behind it
            ra, rb = r + 0.05, r + 0.45
            prism(desks, fan.arc(rb, t0, t1, 0.4) + fan.arc(ra, t1, t0, 0.4), zr + 0.72, zr + 0.76, 'B1_AudWoodLight')
            prism(desks, fan.arc(ra + 0.05, t0, t1, 0.4) + fan.arc(ra, t1, t0, 0.4), zr + 0.30, zr + 0.72, 'B1_AudWoodLight')
            cnt = int((t1 - t0) * (r + 0.3) / SEAT_W)
            if cnt < 1:
                continue
            dt = (t1 - t0) / cnt
            for i in range(cnt):
                s0, s1 = t0 + i * dt + 0.025 / r, t0 + (i + 1) * dt - 0.025 / r
                sm = (s0 + s1) / 2
                ds = 0.04 / r
                prism(chairs, [fan.pol(r + 0.90, th0 + s0), fan.pol(r + 0.90, th0 + s1), fan.pol(r + 0.50, th0 + s1),
                               fan.pol(r + 0.50, th0 + s0)], zr + 0.43, zr + 0.47, 'B1_AudWoodLight')     # seat
                prism(chairs, [fan.pol(r + 0.96, th0 + s0), fan.pol(r + 0.96, th0 + s1), fan.pol(r + 0.90, th0 + s1),
                               fan.pol(r + 0.90, th0 + s0)], zr + 0.47, zr + 0.98, 'B1_AudWoodLight')     # back rest, behind the sitter
                prism(chairs, [fan.pol(r + 0.80, th0 + sm - ds), fan.pol(r + 0.80, th0 + sm + ds), fan.pol(r + 0.60, th0 + sm + ds),
                               fan.pol(r + 0.60, th0 + sm - ds)], zr, zr + 0.43, 'B1_AudFrame')             # steel pedestal

    for i in range(N_ORCH):
        r = R_ROW0 + i * ROW_T
        if r + ROW_T > fan.R_IN + 0.01:
            break
        seat_row(r, z0 + FLOOR0 + i * ORCH_RISE)
    desks.build(coll)
    chairs.build(coll)

    # ---------------- balcony ----------------
    r_edge = fan.R_IN - N_BAL * ROW_T - 0.45     # front edge of the balcony deck
    bal = MB('B1_AudBalcony')
    prism(bal, fan.ring(r_edge, fan.R_IN), z0 + BAL_Z - SLAB_T, z0 + BAL_Z, 'B1_AudCeiling')           # deck slab
    prism(bal, fan.ring(r_edge - 0.05, r_edge + 0.12), z0 + BAL_Z, z0 + BAL_Z + 1.0, 'B1_AudConcrete')  # parapet
    prism(bal, fan.ring(r_edge - 0.05, r_edge + 0.12), z0 + BAL_Z + 1.0, z0 + BAL_Z + 1.06, 'B1_AudRail')
    prism(bal, fan.ring(r_edge - 0.05, r_edge + 0.25), z0 + BAL_Z - SLAB_T - 0.6, z0 + BAL_Z - SLAB_T + 0.01, 'B1_AudConcrete')  # fascia hanging below the deck
    rows_r0 = r_edge + 0.45
    for i in range(N_BAL):
        r = rows_r0 + i * ROW_T
        prism(bal, fan.ring(r, r + ROW_T), z0 + BAL_Z, z0 + BAL_Z + (i + 1) * BAL_RISE, 'B1_AudFloor')
    bal.build(coll)
    desks, chairs = MB('B1_AudBalDesks'), MB('B1_AudBalChairs')
    for i in range(N_BAL):
        seat_row(rows_r0 + i * ROW_T, z0 + BAL_Z + i * BAL_RISE)
    desks.build(coll)
    chairs.build(coll)

    # ---------------- lights ----------------
    lights = MB('B1_AudDownlights')
    for rf in (0.1, 0.3, 0.5, 0.7, 0.9):
        r = fan.R_CUT + (fan.R_IN - fan.R_CUT) * rf
        for ang in (-0.6, -0.3, 0.0, 0.3, 0.6):
            lo, hi = fan.span(r)
            if lo + 0.1 < ang < hi - 0.1:
                prism(lights, [fan.pol(r - 0.2, th0 + ang - 0.012 * 20 / r), fan.pol(r - 0.2, th0 + ang + 0.012 * 20 / r),
                               fan.pol(r + 0.2, th0 + ang + 0.012 * 20 / r), fan.pol(r + 0.2, th0 + ang - 0.012 * 20 / r)],
                      ztop - 0.04, ztop, 'B1_Downlight')
    lights.build(coll)

    for k, (r, z, size) in enumerate(((fan.R_CUT + 2.5, ztop - 0.5, 5), (14.0, ztop - 0.5, 8),
                                      (fan.R_IN - 2.0, z0 + BAL_Z + 3.0, 3),
                                      (fan.R_IN - 4.5, z0 + BAL_Z - 0.6, 3))):
        p = fan.pol(r, th0)
        ld = bpy.data.lights.new(f'B1_AudLight{k}', 'AREA')
        ld.energy, ld.shape, ld.size = 1800, 'SQUARE', size
        lo = bpy.data.objects.new(f'B1_AudLight{k}', ld)
        lo.location = (p.x, p.y, z)
        coll.objects.link(lo)

    # ---------------- cameras ----------------
    def cam(name, r, ang, z, tr, tang, tz, lens):
        cd = bpy.data.cameras.new(name)
        cd.lens = lens
        ob = bpy.data.objects.new(name, cd)
        p, t = fan.pol(r, th0 + ang), fan.pol(tr, th0 + tang)
        ob.location = (p.x, p.y, z)
        ob.rotation_euler = (Vector((t.x, t.y, tz)) - ob.location).to_track_quat('-Z', 'Y').to_euler()
        coll.objects.link(ob)

    cam('Cam_AudStage', fan.R_CUT + 1.2, -0.10, z0 + STAGE_H + 1.6, 18.0, 0.1, z0 + 3.2, 16)
    cam('Cam_AudBalcony', fan.R_IN - 0.9, 0.05, z0 + BAL_Z + 2.0, fan.R_CUT + 1.0, 0.0, z0 + 2.4, 16)
    cam('Cam_AudRear', 17.0, -0.45, z0 + 2.6, 14.0, 0.25, z0 + 6.0, 16)
    cam('Cam_AudBoard', 17.5, -0.35, z0 + 3.4, fan.R_CUT + 1.0, 0.05, z0 + 2.8, 22)
    cam('Cam_AudPlan', 14.5, 0.0, z0 + 44.0, 14.5, 0.0, z0, 38)
    return coll
