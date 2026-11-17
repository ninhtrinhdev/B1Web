"""Sanh B1 (tang 1) trong hinh quat duoi hoi truong, cung hai khoi ben (lop hoc, thang may, cau thang)
va phong kin phia sau dinh quat. Mat tien (kinh cong, cua vao) la phan F1 cua lobby.py.

Bo cuc theo docs/plans/b1_sanh_tang1.svg. Toa do thiet ke (X, d): X huong dong, d = khoang cach doc truc
tu dinh quat. Tran sanh = mat duoi san hoi truong (cao do 7.7 m).
"""
import math

import bpy
from mathutils import Vector

from .auditorium import Fan
from .config import ENTRANCE_PART, level_top
from .lobby import REC
from .materials import principled
from .meshkit import MB, collection, prism

T = 0.35                # day tuong ngoai
H = level_top(2) - 0.4  # tran sanh (cao do 7.7 m)
D_REC = 4.8             # mieng hom le tan
LINTEL = 3.6            # cao do dam cua hom / loi sang hanh lang
OPEN_S = (11.3, 14.5)   # doan lo sang hanh lang tren tuong ben (do dai tu p0)
WING_LEN = {0: 32.4, 1: 29.2}   # chieu dai khoi ben (m): k=0 canh dong, k=1 canh tay
WING_W, CORR, WH = 12.45, 3.0, 4.5
# (loai, s0, s1) tung gian cua hai khoi, tu phia dinh quat ra
BAYS = {0: [('stair', 0.6, 8.3), ('lift', 8.5, 12.4), ('room', 12.6, 16.2), ('room', 16.4, 24.2), ('room', 24.4, 32.1)],
        1: [('lift', 0.6, 7.5), ('room', 7.7, 14.6), ('room', 14.8, 21.7), ('room', 21.9, 28.9)]}


def make_sanh_materials():
    principled('B1_SanhWall', (0.86, 0.86, 0.84), 0.7)
    principled('B1_SanhJoint', (0.04, 0.04, 0.045), 0.6)
    principled('B1_SanhFloor', (0.12, 0.125, 0.13), 0.12, coat=0.6)
    principled('B1_SanhRed', (0.33, 0.12, 0.09), 0.14, coat=0.6)
    principled('B1_SanhGrey', (0.24, 0.25, 0.26), 0.14, coat=0.6)
    principled('B1_SanhConcrete', (0.90, 0.90, 0.88), 0.65)
    principled('B1_SanhSoffit', (0.20, 0.21, 0.23), 0.5)
    principled('B1_SanhCeiling', (0.84, 0.84, 0.82), 0.9)
    principled('B1_SanhDeskTop', (0.03, 0.03, 0.035), 0.3)
    principled('B1_SanhBand', (0.40, 0.41, 0.43), 0.35, 0.7)
    principled('B1_SanhPlant', (0.05, 0.22, 0.06), 0.8)


class Frame:
    """Toa do thiet ke (X, d) <-> toa do the gioi."""

    def __init__(self, fan):
        self.fan = fan
        self.ax = Vector((math.cos(fan.th0), math.sin(fan.th0)))
        self.rt = Vector((math.sin(fan.th0), -math.cos(fan.th0)))
        self.ya = self.loc(fan.A)[1]
        self.lines = []
        for p0, d in fan.lines:
            x, y = self.loc(p0)
            self.lines.append(((x, y - self.ya), (d.dot(self.rt), d.dot(self.ax))))

    def loc(self, p):
        v = p - self.fan.C
        return v.dot(self.rt), v.dot(self.ax)

    def w(self, x, d):
        return self.fan.C + self.rt * x + self.ax * (self.ya + d)

    def xl(self, k, d):
        (px, pd), (dx, dd) = self.lines[k]
        return px + dx * (d - pd) / dd

    def inside(self, x, d, m, r_max):
        if d < 1.0:
            return False
        lo, hi = sorted((self.xl(0, d), self.xl(1, d)))
        return lo + m * 1.4 < x < hi - m * 1.4 and math.hypot(x, self.ya + d) < r_max - m


def _pts(fr, pts):
    return [fr.w(x, d) for x, d in pts]


def _intersect(p, dp, q, dq):
    den = dp.x * (-dq.y) - dp.y * (-dq.x)
    t = ((q.x - p.x) * (-dq.y) - (q.y - p.y) * (-dq.x)) / den
    return p + dp * t


def build_sanh(parent, info):
    make_sanh_materials()
    fan = Fan(info[ENTRANCE_PART]['pts'])
    fr = Frame(fan)
    coll = collection(parent, 'B1_Sanh')
    th0, R, RI = fan.th0, fan.R, fan.R_IN
    R_GL = R + REC - 0.1            # mat kinh tang tret (lobby.py: lui vao 2.2 m sau duong cung)

    (e0, de), (w0, dw) = fan.lines
    ai = _intersect(e0, de, w0, dw)
    lo, hi = fan.span(RI)
    inner = [ai] + fan.arc(RI, lo, hi)

    # --- san, tran ---
    floor = MB('B1_SanhFloor')
    prism(floor, inner, -0.3, 0.0, 'B1_SanhFloor')
    floor.build(coll)
    ceil = MB('B1_SanhCeiling')
    prism(ceil, inner, H, H + 0.06, 'B1_SanhCeiling')
    ceil.build(coll)

    pat = MB('B1_SanhFloorPattern')
    step = 1.75
    for i in range(-4, 12):
        for j in range(-4, 12):
            cx, cd = (i - j) * step, 6.5 + (i + j) * step
            half = step * 0.78
            corners = [(cx - half, cd), (cx, cd + half), (cx + half, cd), (cx, cd - half)]
            if not all(fr.inside(x, d, 0.45, R_GL) for x, d in corners):
                continue
            mat = 'B1_SanhRed' if (i + j) % 3 == 0 else ('B1_SanhGrey' if (i + j) % 3 == 1 else None)
            if mat:
                prism(pat, _pts(fr, corners), 0.0, 0.012, mat, bottom=False)
    pat.build(coll)

    # --- tuong ben + khoi ben (hanh lang, lop hoc, thang may, cau thang) ---
    walls, joints, wing = MB('B1_SanhWalls'), MB('B1_SanhJoints'), MB('B1_SanhWings')
    cores = MB('B1_SanhCores')
    for k in (0, 1):
        p0, d = fan.lines[k]
        n_in = (p0 - fan.A).normalized()
        t_ai = (ai - p0).dot(d)
        s_end = (fan.edge_pt(k, RI) - p0).dot(d)
        pt = lambda s: p0 + d * s
        seg = lambda sa, sb, z0, z1: prism(walls, [pt(sa), pt(sb), pt(sb) - n_in * T, pt(sa) - n_in * T], z0, z1, 'B1_SanhWall')
        seg(t_ai, OPEN_S[0], 0, H)
        seg(OPEN_S[1], s_end, 0, H)
        seg(OPEN_S[0], OPEN_S[1], LINTEL, H)
        s = t_ai + 0.9
        while s < s_end - 0.3:
            if not (OPEN_S[0] - 0.05 < s < OPEN_S[1] + 0.05):
                prism(joints, [pt(s), pt(s + 0.025), pt(s + 0.025) + n_in * 0.012, pt(s) + n_in * 0.012], 0.0, H, 'B1_SanhJoint')
            s += 1.25
        for sa, sb in ((t_ai, OPEN_S[0]), (OPEN_S[1], s_end)):
            prism(joints, [pt(sa), pt(sb), pt(sb) + n_in * 0.012, pt(sa) + n_in * 0.012], 4.4, 4.425, 'B1_SanhJoint')

        L, O = WING_LEN[k], -n_in
        q3 = lambda s_, q_: p0 + d * s_ + O * (T + q_)
        quad = lambda sa, sb, qa, qb: [q3(sa, qa), q3(sb, qa), q3(sb, qb), q3(sa, qb)]
        prism(wing, quad(0.3, L - 0.3, 0, WING_W), -0.3, 0.0, 'B1_SanhFloor')
        prism(wing, quad(0.0, L, WING_W - 0.3, WING_W), 0.0, WH + 0.15, 'B1_SanhWall')       # tuong ngoai
        for sa, sb in ((0, 0.3), (L - 0.3, L)):
            prism(wing, quad(sa, sb, 0, WING_W), 0.0, WH + 0.15, 'B1_SanhWall')
        q0, q1 = CORR + 0.2, WING_W - 0.3
        prev = 0.3
        for kind, s0, s1 in BAYS[k]:
            sm = (s0 + s1) / 2
            prism(wing, quad(s1, s1 + 0.2, q0, q1), 0.0, WH + 0.15, 'B1_SanhWall')              # vach giua cac gian
            if kind != 'stair':
                prism(wing, quad(s0, s1, 0, q1 + 0.3), WH, WH + 0.15, 'B1_SanhCeiling')       # tran (cau thang thong tang)
            if kind == 'room':
                halfdoor = 0.65
            elif kind == 'lift':
                halfdoor = 0.0
            else:
                halfdoor = 0.8
            if halfdoor:
                for sa, sb, z0_, z1_ in ((prev, sm - halfdoor, 0.0, WH), (sm - halfdoor, sm + halfdoor, 2.2, WH)):
                    prism(wing, quad(sa, sb, CORR, CORR + 0.2), z0_, z1_, 'B1_SanhWall')
                prev = sm + halfdoor
            else:
                prism(wing, quad(prev, s1, CORR, CORR + 0.2), 0.0, WH, 'B1_SanhWall')
                prev = s1
            if kind == 'lift':
                for a1, a2 in ((s0 + 0.2, sm - 0.1), (sm + 0.1, s1 - 0.2)):
                    prism(cores, quad(a1, a2, q0 + 0.1, q0 + 2.3), 0.0, WH, 'B1_SanhWall')
                    mid = (a1 + a2) / 2
                    prism(cores, quad(mid - 0.55, mid + 0.55, CORR - 0.03, CORR), 0.0, 2.2, 'B1_Steel')
            elif kind == 'stair':
                n = 13
                rise = 2.25 / n
                qa, ql = q0 + 0.6, q0 + 3.6
                for i in range(n):
                    qs0, qs1 = qa + (ql - qa) * i / n, qa + (ql - qa) * (i + 1) / n
                    prism(cores, quad(sm - 1.1, sm + 1.1, qs0, qs1), 0.0, rise * (i + 1), 'B1_SanhConcrete')
                    for sg in (-1, 1):
                        a0, a1 = sm + sg * (1.1 + 2.8 * i / n), sm + sg * (1.1 + 2.8 * (i + 1) / n)
                        prism(cores, quad(min(a0, a1), max(a0, a1), ql, ql + 1.6), 0.0, 2.25 + rise * (i + 1), 'B1_SanhConcrete')
                prism(cores, quad(sm - 1.1, sm + 1.1, ql, ql + 1.6), 0.0, 2.25, 'B1_SanhConcrete')
        prism(wing, quad(prev, L - 0.3, CORR, CORR + 0.2), 0.0, WH, 'B1_SanhWall')
        prism(wing, quad(0.3, L - 0.3, 0, CORR), WH, WH + 0.15, 'B1_SanhCeiling')
    walls.build(coll)
    joints.build(coll)
    wing.build(coll)
    cores.build(coll)

    # --- phong kin phia sau dinh quat (hinh vuong 12.45 m ap hai khoi), cua sau o canh phia dong ---
    oe, ow = -(fan.lines[0][0] - fan.A).normalized(), -(fan.lines[1][0] - fan.A).normalized()
    a0 = fan.A
    sq = [a0, a0 + oe * WING_W, a0 + (oe + ow) * WING_W, a0 + ow * WING_W]
    rear = MB('B1_SanhRearRoom')
    prism(rear, sq, -0.3, 0.0, 'B1_SanhFloor')
    prism(rear, sq, WH, WH + 0.15, 'B1_SanhCeiling')
    ue = (sq[2] - sq[1]).normalized()
    m = sq[1] + ue * WING_W * 0.5
    door = (m - ue * 0.9, m + ue * 0.9)
    for pa, pb in ((sq[1], door[0]), (door[1], sq[2])):
        prism(rear, [pa, pb, pb + ow * 0.3, pa + ow * 0.3], 0.0, WH + 0.15, 'B1_SanhWall')
    prism(rear, [door[0], door[1], door[1] + ow * 0.3, door[0] + ow * 0.3], 2.2, WH + 0.15, 'B1_SanhWall')
    prism(rear, [door[0], door[1], door[1] + ow * 0.05, door[0] + ow * 0.05], 0.0, 2.2, 'B1_Steel')   # canh cua sau
    for pa, pb in ((sq[0], sq[1]), (sq[2], sq[3]), (sq[3], sq[0])):
        n_ = (pb - pa)
        nrm = Vector((n_.y, -n_.x)).normalized()
        if nrm.dot(sq[0] + (oe + ow) * WING_W * 0.5 - pa) > 0:
            nrm = -nrm
        prism(rear, [pa, pb, pb + nrm * 0.3, pa + nrm * 0.3], 0.0, WH + 0.15, 'B1_SanhWall')
    rear.build(coll)

    # --- hom le tan phia dinh quat: dam cua hom, hai khoi tuong, quay chu V ---
    rec = MB('B1_SanhReception')
    xe = lambda d_: max(fr.xl(0, d_), fr.xl(1, d_))
    xw = lambda d_: min(fr.xl(0, d_), fr.xl(1, d_))
    kw, ke = xw(D_REC), xe(D_REC)
    prism(rec, _pts(fr, [(kw, D_REC - 0.15), (ke, D_REC - 0.15), (ke, D_REC + 0.2), (kw, D_REC + 0.2)]), LINTEL, H, 'B1_SanhWall')
    for sx in (-1, 1):
        edge = kw if sx < 0 else ke
        inner_x = edge + sx * 1.5
        far_x = xw(D_REC + 1.2) if sx < 0 else xe(D_REC + 1.2)
        prism(rec, _pts(fr, [(edge, D_REC), (inner_x, D_REC), (inner_x, D_REC + 1.2), (far_x, D_REC + 1.2)]), 0.0, H, 'B1_SanhWall')
    prism(rec, [ai, fr.w(ke, D_REC), fr.w(kw, D_REC)], LINTEL - 0.06, LINTEL, 'B1_SanhSoffit')
    # tuong logo HUST sau quay
    prism(rec, _pts(fr, [(xw(1.7) + 0.05, 1.65), (xe(1.7) - 0.05, 1.65), (xe(1.7) - 0.05, 1.75), (xw(1.7) + 0.05, 1.75)]), 0.0, LINTEL - 0.06, 'B1_SanhWall')
    prism(rec, _pts(fr, [(-0.6, 1.6), (1.0, 1.6), (1.0, 1.65), (-0.6, 1.65)]), 1.7, 2.5, 'B1_SanhBand')
    # quay le tan chu V: hai canh song song hai canh thang cua quat, mui chu V huong ve dinh
    off0, off1 = 1.6, 2.4
    lines = []
    for k in (0, 1):
        p0, d = fan.lines[k]
        n_in = (p0 - fan.A).normalized()
        lines.append((p0 + n_in * off0, p0 + n_in * off1, d))
    tip0 = _intersect(lines[0][0], lines[0][2], lines[1][0], lines[1][2])
    tip1 = _intersect(lines[0][1], lines[0][2], lines[1][1], lines[1][2])
    s_arm = 3.1
    arm = lambda k, which, tip: tip + lines[k][2] * s_arm
    desk = [tip0, arm(0, 0, tip0), arm(0, 1, tip1), tip1, arm(1, 1, tip1), arm(1, 0, tip0)]
    prism(rec, desk, 0.0, 1.05, 'B1_SanhConcrete')
    prism(rec, desk, 1.05, 1.1, 'B1_SanhDeskTop')
    rec.build(coll)

    # --- ghe be tong chu V sat tuong kinh, phia tay cua vao ---
    xe_end, xw_end = fr.loc(fan.E_e)[0], fr.loc(fan.E_w)[0]
    ent_x = xw_end + 0.56 * (xe_end - xw_end)
    ent_rel = -math.asin(ent_x / RI)
    hg, pier = 1.9 / RI, 1.5 / RI

    def band(r0, r1, a0_, a1_):
        return fan.arc(r1, a0_, a1_, 0.3) + fan.arc(r0, a1_, a0_, 0.3)

    bench = MB('B1_SanhBench')
    b0 = ent_rel + hg + pier + 0.05
    b1 = b0 + 0.66
    bm = (b0 + b1) / 2
    for a0_, a1_ in ((b0, bm), (bm + 0.02, b1)):
        prism(bench, band(R_GL - 1.5, R_GL - 0.5, a0_, a1_), 0.0, 0.45, 'B1_SanhConcrete')
    bench.build(coll)

    plants = MB('B1_SanhPlants')
    for ang, r in ((ent_rel - hg - pier - 0.12, R_GL - 0.8), (ent_rel - hg - pier - 0.2, R_GL - 1.6)):
        c = fan.pol(r, th0 + ang)
        for a in range(0, 360, 45):
            tip = c + Vector((math.cos(math.radians(a)), math.sin(math.radians(a)))) * 0.55
            prism(plants, [c + Vector((0.04, 0)), c + Vector((0, 0.04)), tip], 0.9, 1.0, 'B1_SanhPlant')
        prism(plants, [c + Vector((0.3, 0)), c + Vector((0, 0.3)), c + Vector((-0.3, 0)), c + Vector((0, -0.3))], 0.0, 0.6, 'B1_SanhConcrete')
    plants.build(coll)

    # --- den, camera ---
    for i, (x, d_) in enumerate(((0.0, 6.5), (0.0, 11.0), (-1.0, 3.2))):
        p = fr.w(x, d_)
        ld = bpy.data.lights.new(f'B1_SanhLight{i}', 'AREA')
        ld.energy, ld.shape, ld.size = 700, 'SQUARE', 5
        lo_ = bpy.data.objects.new(f'B1_SanhLight{i}', ld)
        lo_.location = (p.x, p.y, H - 0.4 if i < 2 else LINTEL - 0.4)
        coll.objects.link(lo_)
    for k in (0, 1):                                    # den hanh lang hai khoi
        p0, d = fan.lines[k]
        n_in = (p0 - fan.A).normalized()
        for s_ in (6.0, 14.0, 22.0):
            p = p0 + d * s_ - n_in * (T + 1.5)
            ld = bpy.data.lights.new(f'B1_SanhWingLight{k}_{int(s_)}', 'AREA')
            ld.energy, ld.shape, ld.size = 120, 'SQUARE', 2
            lo_ = bpy.data.objects.new(ld.name, ld)
            lo_.location = (p.x, p.y, WH - 0.3)
            coll.objects.link(lo_)

    def cam(name, x, d_, z, tx, td, tz, lens):
        cd = bpy.data.cameras.new(name)
        cd.lens = lens
        ob = bpy.data.objects.new(name, cd)
        p, t = fr.w(x, d_), fr.w(tx, td)
        ob.location = (p.x, p.y, z)
        ob.rotation_euler = (Vector((t.x, t.y, tz)) - ob.location).to_track_quat('-Z', 'Y').to_euler()
        coll.objects.link(ob)

    cam('Cam_SanhEntry', ent_x, 12.0, 1.6, -0.8, 3.0, 1.2, 17)
    cam('Cam_SanhGlass', 0.5, 7.0, 1.6, -8.0, 12.0, 2.6, 17)
    p_c, d_c = fan.lines[0]
    n_c = (p_c - fan.A).normalized()
    a_, b_ = p_c + d_c * 2.0 - n_c * (T + 1.5), p_c + d_c * 26.0 - n_c * (T + 1.5)
    cd = bpy.data.cameras.new('Cam_SanhWing')
    cd.lens = 17
    cw = bpy.data.objects.new('Cam_SanhWing', cd)
    cw.location = (a_.x, a_.y, 1.6)
    cw.rotation_euler = (Vector((b_.x, b_.y, 1.7)) - cw.location).to_track_quat('-Z', 'Y').to_euler()
    coll.objects.link(cw)
    cam('Cam_SanhPlan', 0.0, 4.0, 62.0, 0.0, 4.0, 0.0, 30)
    return coll
