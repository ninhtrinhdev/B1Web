"""Ve so do mat bang sanh B1 (tang 1) thanh SVG, dung dung hinh quat cua hoi truong ben tren.

Chay tu thu muc goc repo:
    blender -b -P blender/tools/plan_lobby.py
Ra: docs/plans/b1_sanh_tang1.svg  (cua vao o phia duoi hinh, giong so do tham chieu).
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
B1_DIR = os.path.join(os.path.dirname(HERE), 'buildings', 'b1')
sys.path.insert(0, B1_DIR)

from b1.auditorium import Fan  # noqa: E402
from b1.config import B1_WAY, ENTRANCE_PART  # noqa: E402
from b1.osm import load_osm, make_projector  # noqa: E402
from b1.wings import load_parts  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'docs', 'plans', 'b1_sanh_tang1.svg')
S = 21.5            # pixel / m
W_T = 0.35          # tuong ngoai (m)
W = 1500

osm = load_osm(os.path.join(os.path.dirname(HERE), 'data', 'map.osm'))
proj = make_projector(osm[0], osm[1][B1_WAY]['refs'][:-1])
info = load_parts(osm, proj)
fan = Fan(info[ENTRANCE_PART]['pts'])

# ---- hinh hoc trong he cuc bo: goc = tam cung C, x huong dong, y doc theo truc (huong bac) ----
ax = (math.cos(fan.th0), math.sin(fan.th0))
rt = (math.sin(fan.th0), -math.cos(fan.th0))


def loc(p):
    d = p - fan.C
    return (d.x * rt[0] + d.y * rt[1], d.x * ax[0] + d.y * ax[1])


A, E, Wp = loc(fan.A), loc(fan.E_e), loc(fan.E_w)
R = fan.R
RI = R - W_T
YA = A[1]


def norm(v):
    l = math.hypot(*v)
    return (v[0] / l, v[1] / l)


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def add(a, b, k=1.0):
    return (a[0] + b[0] * k, a[1] + b[1] * k)


dE, dW = norm(sub(E, A)), norm(sub(Wp, A))
nE = (-dE[1], dE[0])   # phap tuyen vao trong (huong ve phia truc)
if nE[0] > 0:
    nE = (-nE[0], -nE[1])
nE = (-nE[0], -nE[1]) if (nE[0] * (dW[0]) + nE[1] * dW[1]) < 0 else nE
nW = (-dW[1], dW[0])
nW = (-nW[0], -nW[1]) if (nW[0] * dE[0] + nW[1] * dE[1]) < 0 else nW


def line_circle(p0, d, r):
    b = d[0] * p0[0] + d[1] * p0[1]
    c = p0[0] ** 2 + p0[1] ** 2 - r * r
    s = -b + math.sqrt(b * b - c)
    return add(p0, d, s)


E0, W0 = add(A, nE, W_T), add(A, nW, W_T)         # diem tren duong nghieng da thut vao
# giao hai duong thut vao -> dinh trong
den = dE[0] * (-dW[1]) - dE[1] * (-dW[0])
t = ((W0[0] - E0[0]) * (-dW[1]) - (W0[1] - E0[1]) * (-dW[0])) / den
AI = add(E0, dE, t)
E_in, W_in = line_circle(E0, dE, RI), line_circle(W0, dW, RI)
ang = lambda p: math.atan2(p[1], p[0])


def arc_pts(r, a0, a1, step=0.25):
    n = max(2, int(abs(a1 - a0) * r / step))
    return [(r * math.cos(a0 + (a1 - a0) * i / n), r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def outer_poly():
    e_o, w_o = E, Wp
    return [A] + arc_pts(R, ang(e_o), ang(w_o)) + []


outer = [A, E] + arc_pts(R, ang(E), ang(Wp))[1:-1] + [Wp]
inner = [AI, E_in] + arc_pts(RI, ang(E_in), ang(W_in))[1:-1] + [W_in]

# hai khoi lop hoc hinh chu nhat ap sat hai canh thang cua hinh quat (theo OSM: rong 12.45 m)
oE, oW = (-nE[0], -nE[1]), (-nW[0], -nW[1])
WB = 12.45
LB = {'E': 32.4, 'W': 29.2}
DIRS = {'E': (dE, oE), 'W': (dW, oW)}


def bp(k, s_, q):
    d_, o_ = DIRS[k]
    return (A[0] + d_[0] * s_ + o_[0] * q, A[1] + d_[1] * s_ + o_[1] * q)


_all = outer + [bp(k, s_, q) for k in 'EW' for s_, q in ((0, 0), (LB[k], 0), (LB[k], WB), (0, WB))]
REAR = [A, (A[0] + oE[0] * WB, A[1] + oE[1] * WB),
        (A[0] + (oE[0] + oW[0]) * WB, A[1] + (oE[1] + oW[1]) * WB), (A[0] + oW[0] * WB, A[1] + oW[1] * WB)]
_all += REAR
_xmin, _xmax = min(p[0] for p in _all), max(p[0] for p in _all)
_dmin, _dmax = min(p[1] for p in _all) - YA, max(p[1] for p in _all) - YA
OX = 750.0 + (_xmin + _xmax) / 2 * S
OY = 150.0 - _dmin * S
YB = OY + max(_dmax, 22.0) * S + 30
H = int(YB + 260)


def area(poly):
    return abs(sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
                   for i in range(len(poly)))) / 2


def X(x, y):          # xoay 180 do: cua vao o phia duoi, dong ben trai
    return OX - x * S


def Y(x, y):
    return OY + (y - YA) * S


def P(poly):
    return ' '.join(f'{X(*p):.1f},{Y(*p):.1f}' for p in poly)


NAVY, CREAM, BLUE, GREY = '#1f2d44', '#f6eedb', '#d6e8f7', '#e4e6ea'
svg = []


def add_svg(s):
    svg.append(s)


def poly(pts, fill, stroke='none', sw=1, extra=''):
    add_svg(f'<polygon points="{P(pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')


def line(a, b, stroke=NAVY, sw=2, dash=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    add_svg(f'<line x1="{X(*a):.1f}" y1="{Y(*a):.1f}" x2="{X(*b):.1f}" y2="{Y(*b):.1f}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


def text(x, y, s, size=15, bold=False, anchor='middle', fill='#111', px=False, rot=0):
    xx, yy = (x, y) if px else (X(x, y), Y(x, y))
    w = ' font-weight="700"' if bold else ''
    r = f' transform="rotate({rot} {xx:.1f} {yy:.1f})"' if rot else ''
    add_svg(f'<text x="{xx:.1f}" y="{yy:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{fill}"{w}{r}>{s}</text>')


def rect(x0, x1, d0, d1, fill, stroke=NAVY, sw=2):
    y0, y1 = YA + d0, YA + d1
    poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, stroke, sw)


def at(side, s):      # diem tren duong thut vao, s met tinh tu dinh
    return add(E0 if side == 'E' else W0, dE if side == 'E' else dW, s - (t if side == 'E' else 0) * 0)


# ---------------- khung ----------------
add_svg(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="Segoe UI, Arial, sans-serif">')
add_svg(f'<rect width="{W}" height="{H}" fill="#fbfbfc"/>')
for gx in range(0, W, 36):
    add_svg(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{H}" stroke="#eef0f3" stroke-width="1"/>')
for gy in range(0, H, 36):
    add_svg(f'<line x1="0" y1="{gy}" x2="{W}" y2="{gy}" stroke="#eef0f3" stroke-width="1"/>')

# ---------------- phong kin phia sau (sau dinh quat) ----------------
poly(REAR, NAVY)
poly([(A[0] + (r_[0] - A[0]) * 0.97 + 0.0, A[1] + (r_[1] - A[1]) * 0.97) for r_ in REAR], '#eceef2')
_c = (sum(p_[0] for p_ in REAR) / 4, sum(p_[1] for p_ in REAR) / 4)
text(_c[0], _c[1], 'Một phòng kín', 17, True, fill='#36445e')
text(_c[0], _c[1] + 0.9, '(≈ 155 m²)', 13, fill='#6a768d')
# cua sau tren canh ngoai phia dong
_a, _b = REAR[1], REAR[2]
_u = norm(sub(_b, _a))
_m = add(_a, _u, WB * 0.5)
poly([add(_m, _u, -0.9), add(_m, _u, 0.9), add(add(_m, _u, 0.9), oW, -0.45), add(add(_m, _u, -0.9), oW, -0.45)], '#eceef2')
add_svg(f'<path d="M {X(*add(_m, _u, -0.9)):.1f},{Y(*add(_m, _u, -0.9)):.1f} A {1.8 * S:.1f} {1.8 * S:.1f} 0 0 1 {X(*add(add(_m, _u, -0.9), oW, 1.8)):.1f},{Y(*add(add(_m, _u, -0.9), oW, 1.8)):.1f}" fill="none" stroke="#7a8aa5" stroke-width="1" stroke-dasharray="4 3"/>')
_t = add(_m, oE, 0)
_arrow_from = add(_m, (-oW[0], -oW[1]), 2.4)
line(_arrow_from, add(_m, (-oW[0], -oW[1]), 0.5), '#2a6fbf', 3)
text(*add(_arrow_from, (-oW[0], -oW[1]), 1.0), 'Cửa sau', 16, True, fill='#2a6fbf')

# ---------------- hai khoi: lop hoc, thang may, cau thang ----------------
CORR = 3.0
BAYS = {
    'E': [('stair', 0.6, 8.3, 'Cầu thang thẳng 2 hướng'), ('lift', 8.5, 12.4, 'Thang máy 1–2'),
          ('room', 12.6, 16.2, 'Lớp học 102'), ('room', 16.4, 24.2, 'Lớp học 103'), ('room', 24.4, 32.1, 'Lớp học 104')],
    'W': [('lift', 0.6, 7.5, 'Thang máy 3–4'), ('room', 7.7, 14.6, 'Lớp học 106'),
          ('room', 14.8, 21.7, 'Lớp học 107'), ('room', 21.9, 28.9, 'Lớp học 108')],
}
for k_ in 'EW':
    L_ = LB[k_]
    d_, o_ = DIRS[k_]
    poly([bp(k_, 0, 0), bp(k_, L_, 0), bp(k_, L_, WB), bp(k_, 0, WB)], NAVY)
    poly([bp(k_, 0.3, 0), bp(k_, L_ - 0.3, 0), bp(k_, L_ - 0.3, WB - 0.3), bp(k_, 0.3, WB - 0.3)], CREAM)
    poly([bp(k_, 0.3, CORR), bp(k_, L_ - 0.3, CORR), bp(k_, L_ - 0.3, CORR + 0.2), bp(k_, 0.3, CORR + 0.2)], NAVY)
    ang_s = math.degrees(math.atan2(d_[1] * S, -d_[0] * S))
    ang_s = ang_s - 180 if ang_s > 90 else (ang_s + 180 if ang_s < -90 else ang_s)
    for kind, s0, s1, lab in BAYS[k_]:
        sm = (s0 + s1) / 2
        q0, q1 = CORR + 0.2, WB - 0.3
        if kind == 'room':
            poly([bp(k_, s0, q0), bp(k_, s1, q0), bp(k_, s1, q1), bp(k_, s0, q1)], BLUE, NAVY, 1.5)
            poly([bp(k_, sm - 0.65, CORR - 0.02), bp(k_, sm + 0.65, CORR - 0.02), bp(k_, sm + 0.65, CORR + 0.22), bp(k_, sm - 0.65, CORR + 0.22)], CREAM)
            line(bp(k_, sm - 0.65, CORR + 0.1), bp(k_, sm - 0.65 + 0.2, CORR + 1.1), '#3a78c2', 2)
            c_ = bp(k_, sm, (q0 + q1) / 2)
            text(c_[0], c_[1], lab, 14, True, rot=ang_s)
        elif kind == 'lift':
            poly([bp(k_, s0, q0), bp(k_, s1, q0), bp(k_, s1, q1), bp(k_, s0, q1)], '#e7e9ee', NAVY, 1.5)
            for j_, (a1, a2) in enumerate(((s0 + 0.2, sm - 0.1), (sm + 0.1, s1 - 0.2))):
                poly([bp(k_, a1, q0 + 0.1), bp(k_, a2, q0 + 0.1), bp(k_, a2, q0 + 2.3), bp(k_, a1, q0 + 2.3)], '#d9dce2', '#8b93a3', 1.2)
                line(bp(k_, a1, q0 + 0.1), bp(k_, a2, q0 + 2.3), '#8b93a3', 1)
                line(bp(k_, a1, q0 + 2.3), bp(k_, a2, q0 + 0.1), '#8b93a3', 1)
            poly([bp(k_, sm - 0.8, CORR - 0.02), bp(k_, sm + 0.8, CORR - 0.02), bp(k_, sm + 0.8, CORR + 0.22), bp(k_, sm - 0.8, CORR + 0.22)], CREAM)
            c_ = bp(k_, sm, (q0 + q1) / 2 + 1.5)
            text(c_[0], c_[1], lab, 14, True, rot=ang_s)
        else:                                                          # cau thang thang, chia 2 huong
            poly([bp(k_, s0, q0), bp(k_, s1, q0), bp(k_, s1, q1), bp(k_, s0, q1)], '#f4f5f7', NAVY, 1.5)
            poly([bp(k_, sm - 0.8, CORR - 0.02), bp(k_, sm + 0.8, CORR - 0.02), bp(k_, sm + 0.8, CORR + 0.22), bp(k_, sm - 0.8, CORR + 0.22)], CREAM)

            def flight(sa, sb, qa, qb, along_q):
                poly([bp(k_, sa, qa), bp(k_, sb, qa), bp(k_, sb, qb), bp(k_, sa, qb)], '#fafafa', '#8b93a3', 1.2)
                n_st = 13
                for j_ in range(1, n_st):
                    t_ = j_ / n_st
                    if along_q:
                        line(bp(k_, sa, qa + (qb - qa) * t_), bp(k_, sb, qa + (qb - qa) * t_), '#9aa3b3', 1)
                    else:
                        line(bp(k_, sa + (sb - sa) * t_, qa), bp(k_, sa + (sb - sa) * t_, qb), '#9aa3b3', 1)
            q_land = q0 + 3.6
            flight(sm - 1.1, sm + 1.1, q0 + 0.6, q_land, True)                    # vế thẳng đi lên
            poly([bp(k_, sm - 1.1, q_land), bp(k_, sm + 1.1, q_land), bp(k_, sm + 1.1, q_land + 1.6), bp(k_, sm - 1.1, q_land + 1.6)], '#eceef2', '#8b93a3', 1.2)
            flight(sm - 1.1 - 2.8, sm - 1.1, q_land, q_land + 1.6, False)         # hai vế rẽ trái / phải
            flight(sm + 1.1, sm + 1.1 + 2.8, q_land, q_land + 1.6, False)
            c_ = bp(k_, sm, q1 - 0.9)
            text(c_[0], c_[1], 'Cầu thang', 13, True, rot=ang_s)
            text(*bp(k_, sm, q1 - 0.3), 'thẳng 2 hướng', 12, rot=ang_s)
    cc = bp(k_, L_ - 3.2, CORR / 2 + 0.05)
    text(cc[0], cc[1], 'Hành lang', 12, fill='#7a6a3a', rot=ang_s)
text(*bp('E', LB['E'] * 0.5, WB + 1.3), 'Khối cánh Đông', 14, True, fill='#36445e', rot=0)
text(*bp('W', LB['W'] * 0.5, WB + 1.3), 'Khối cánh Tây', 14, True, fill='#36445e', rot=0)

# ---------------- tuong va san ----------------
poly(outer, NAVY)
poly(inner, CREAM)

# cua so kinh doc cung (tru khoang cua vao)
ent_x = A[0] * 0 + (Wp[0] + 0.56 * (E[0] - Wp[0]))              # cua vao lech ve phia dong (ENTRY_F = 0.56)
ent_ang = math.asin(ent_x / RI) if False else math.atan2(math.sqrt(RI * RI - ent_x * ent_x), ent_x)
half_gap = 1.9 / RI
gap = (ent_ang - half_gap, ent_ang + half_gap)
rm = R - 2.3          # mat kinh tang tret lui vao 2.2 m sau duong cung (lobby.py)
poly(arc_pts(RI, ang(E_in), ang(W_in))[:] + arc_pts(R - 2.3, ang(W_in), ang(E_in)), '#fbfaf3', '#c9c3ad', 1, 'stroke-dasharray="5 4"')
for a0, a1 in ((ang(E_in) + 0.0, gap[0]), (gap[1], ang(W_in))):
    pts = arc_pts(rm, a0, a1, 0.2)
    d = 'M ' + ' L '.join(f'{X(*p):.1f},{Y(*p):.1f}' for p in pts)
    add_svg(f'<path d="{d}" fill="none" stroke="#7db8ea" stroke-width="5" stroke-dasharray="{3.2 * S:.0f} {0.45 * S:.0f}"/>')
# khoang cua vao: mo tuong
gp = arc_pts(R - W_T / 2, gap[0], gap[1], 0.1)
poly([(math.cos(gap[0]) * (R + 0.1), math.sin(gap[0]) * (R + 0.1))] + [(math.cos(a) * (R + 0.1), math.sin(a) * (R + 0.1))
                                                                           for a in (gap[0], gap[1])] +
     [(math.cos(gap[1]) * (RI - 0.1), math.sin(gap[1]) * (RI - 0.1)), (math.cos(gap[0]) * (RI - 0.1), math.sin(gap[0]) * (RI - 0.1))],
     CREAM)
for a in gap:
    add_svg(f'<circle cx="{X(R * math.cos(a), R * math.sin(a)):.1f}" cy="{Y(R * math.cos(a), R * math.sin(a)):.1f}" r="5" fill="{NAVY}"/>')

# cua kinh 4 canh o cong chinh (dong canh dong, dong canh tay)
RG_ = R - 2.3
pl, pr = (RG_ * math.cos(gap[0]), RG_ * math.sin(gap[0])), (RG_ * math.cos(gap[1]), RG_ * math.sin(gap[1]))
mid = ((pl[0] + pr[0]) / 2, (pl[1] + pr[1]) / 2)
line(pl, pr, '#3a78c2', 3)
for p in (pl, pr):
    inw = norm((-p[0], -p[1]))
    q = add(p, inw, 1.8)
    line(p, q, '#3a78c2', 2)
for p in (pl, pr):
    pts = arc_pts(1.8, 0, 1, 0.1)
add_svg(f'<path d="M {X(*pl):.1f},{Y(*pl):.1f} A {1.8 * S:.1f} {1.8 * S:.1f} 0 0 0 {X(*add(pl, norm((-pl[0], -pl[1])), 1.8)):.1f},{Y(*add(pl, norm((-pl[0], -pl[1])), 1.8)):.1f}" fill="none" stroke="#7a8aa5" stroke-width="1" stroke-dasharray="4 3"/>')
add_svg(f'<path d="M {X(*pr):.1f},{Y(*pr):.1f} A {1.8 * S:.1f} {1.8 * S:.1f} 0 0 1 {X(*add(pr, norm((-pr[0], -pr[1])), 1.8)):.1f},{Y(*add(pr, norm((-pr[0], -pr[1])), 1.8)):.1f}" fill="none" stroke="#7a8aa5" stroke-width="1" stroke-dasharray="4 3"/>')

# mai don xe (net dut, nam ngoai)
ca, cb = ent_ang - 0.17, ent_ang + 0.17
cpts = arc_pts(R + 0.4, ca, cb, 0.2) + arc_pts(R + 5.0, cb, ca, 0.2)
poly(cpts, 'none', '#6c7b93', 1.5, 'stroke-dasharray="7 5"')
text(R * 0 + (R + 3.2) * math.cos(ent_ang), (R + 3.2) * math.sin(ent_ang), 'Mái đón xe', 13, anchor='middle', fill='#51607a')

# ---------------- loi mo sang hanh lang hai canh ----------------
for side, d0 in (('E', 11.3), ('W', 11.3)):
    base, dr, nn = (E0, dE, nE) if side == 'E' else (W0, dW, nW)
    p0 = add(base, dr, d0)
    p1 = add(base, dr, d0 + 3.2)
    poly([add(p0, nn, -0.5), add(p1, nn, -0.5), add(p1, nn, 0.45), add(p0, nn, 0.45)], CREAM)
    line(add(add(p0, dr, 1.6), nn, 0.1), add(add(p0, dr, 1.6), nn, -1.4), '#2a6fbf', 2)

# ---------------- quay le tan o phia sau (hom sau sanh), thang may, thang bo ----------------
D_REC = 4.8          # mieng hom le tan (khoang cach tu dinh)
kx_w = W0[0] + dW[0] * ((YA + D_REC - W0[1]) / dW[1])
kx_e = E0[0] + dE[0] * ((YA + D_REC - E0[1]) / dE[1])
poly([AI, (kx_e, YA + D_REC), (kx_w, YA + D_REC)], '#e7e9ee', NAVY, 3)
poly([(kx_w + 0.3, YA + D_REC), (kx_w + 1.5, YA + D_REC), (kx_w + 1.5, YA + D_REC + 1.2), (kx_w + 0.3, YA + D_REC + 1.2)], NAVY, NAVY, 1)
poly([(kx_e - 0.3, YA + D_REC), (kx_e - 1.5, YA + D_REC), (kx_e - 1.5, YA + D_REC + 1.2), (kx_e - 0.3, YA + D_REC + 1.2)], NAVY, NAVY, 1)
# quay le tan chu V, hai canh song song hai canh thang cua quat
def _inter(p, dp, q, dq):
    den = dp[0] * (-dq[1]) - dp[1] * (-dq[0])
    t_ = ((q[0] - p[0]) * (-dq[1]) - (q[1] - p[1]) * (-dq[0])) / den
    return add(p, dp, t_)


_le0, _le1 = add(A, nE, 1.6), add(A, nE, 2.4)
_lw0, _lw1 = add(A, nW, 1.6), add(A, nW, 2.4)
_tip0, _tip1 = _inter(_le0, dE, _lw0, dW), _inter(_le1, dE, _lw1, dW)
_desk = [_tip0, add(_tip0, dE, 3.1), add(_tip1, dE, 3.1), _tip1, add(_tip1, dW, 3.1), add(_tip0, dW, 3.1)]
poly(_desk, '#f5f5f2', NAVY, 2.5)
text(*add(_tip1, dE, 0.0), 'Quầy lễ tân (chữ V)', 12, True, fill='#222', rot=0)
line((xw_ := kx_w + 0.9, YA + 1.55), (kx_e - 0.9, YA + 1.55), '#9aa3b3', 3)
text(0.0, YA + 1.15, 'Tường logo HUST', 11, fill='#6a768d')

# ghe be tong trang, hinh V, ap sat tuong kinh phia tay cua vao
bench_r0, bench_r1 = R - 2.3 - 1.5, R - 2.3 - 0.5
v = ang(W_in)
b_ang = (ent_ang + half_gap + 0.05, ent_ang + half_gap + 0.62)
seg = [b_ang[0], (b_ang[0] + b_ang[1]) / 2 + 0.07, b_ang[1] - 0.04]
for a0, a1 in ((b_ang[0] + 0.02, (b_ang[0] + b_ang[1]) / 2), ((b_ang[0] + b_ang[1]) / 2 + 0.02, b_ang[1])):
    poly(arc_pts(bench_r1, a0, a1, 0.2) + arc_pts(bench_r0, a1, a0, 0.2), '#dfe4ec', NAVY, 2)
text(-7.6, YA + 10.7, 'Ghế bê tông', 13, anchor='middle')

# nhan Sanh
text(0.8, YA + 8.6, 'Sảnh', 22, True)
add_svg(f'<g transform="translate({X(0.8, 0) - 28:.1f},{Y(0, YA + 8.6) - 52:.1f})" fill="none" stroke="#333" stroke-width="2">'
        '<circle cx="28" cy="8" r="6"/><path d="M16 26 q12 -18 24 0"/><circle cx="10" cy="14" r="4.5"/><circle cx="46" cy="14" r="4.5"/>'
        '<path d="M2 30 q6 -12 14 -6"/><path d="M54 30 q-6 -12 -14 -6"/></g>')
text(ent_x - 0.1, YA + 13.0 + 0.0, '', 1)

# nhan cua vao
ex, ey = (RI + 2.4) * math.cos(ent_ang), (RI + 2.4) * math.sin(ent_ang)
add_svg(f'<polygon points="{X(ex, ey) - 11:.1f},{Y(ex, ey) + 50:.1f} {X(ex, ey) + 11:.1f},{Y(ex, ey) + 50:.1f} {X(ex, ey):.1f},{Y(ex, ey) + 28:.1f}" fill="#2a6fbf"/>')
add_svg(f'<line x1="{X(ex, ey):.1f}" y1="{Y(ex, ey) + 50:.1f}" x2="{X(ex, ey):.1f}" y2="{Y(ex, ey) + 74:.1f}" stroke="#2a6fbf" stroke-width="7"/>')
text(X(ex, ey), Y(ex, ey) + 106, 'Cửa vào chính', 17, False, px=True)

# ghi chu giang duong tren
text(-0.6, YA + 8.4, 'Giảng đường (tầng 3–4)', 12, fill='#6a768d')
text(-0.6, YA + 9.0, 'nằm ngay phía trên', 12, fill='#6a768d')

# ---------------- kich thuoc ----------------
yb = YA + 18.6
x1c, x2c = E[0], Wp[0]
line((x1c, yb), (x2c, yb), '#51607a', 1.2)
for xx in (x1c, x2c):
    line((xx, yb - 0.25), (xx, yb + 0.25), '#51607a', 1.2)
    line((xx, E[1] if xx == x1c else Wp[1]), (xx, yb - 0.3), '#b8c0cf', 1, '4 4')
text((x1c + x2c) / 2, yb - 0.28, f'{math.hypot(E[0] - Wp[0], E[1] - Wp[1]):.1f} m (dây cung)', 13, fill='#51607a')

# ---------------- khung thong tin ----------------
add_svg('<rect x="20" y="24" width="470" height="58" rx="8" fill="#1f2d44"/>')
add_svg('<text x="40" y="62" font-size="28" font-weight="700" fill="#fff">Sơ đồ mặt bằng – Sảnh tầng 1</text>')
add_svg('<rect x="20" y="96" width="140" height="38" rx="6" fill="#e4e8ef"/>')
add_svg('<text x="90" y="122" font-size="19" font-weight="700" text-anchor="middle" fill="#2b3547">Tòa nhà B1</text>')
ia = area(inner)
add_svg(f'<rect x="20" y="{YB}" width="290" height="200" rx="8" fill="#f3f5f9" stroke="#d5dbe6"/>')
add_svg(f'<text x="36" y="{YB + 32}" font-size="19" font-weight="700" fill="#1f2d44">Thông tin chung</text>')
for i, (k, v) in enumerate((('Diện tích sảnh (trong tường):', f'{ia:.0f} m²'), ('Hình dạng:', 'quạt ≈ 92°'),
                            ('Chiều cao:', '≈ 8.1 m (thông tầng)'), ('Bán kính cung:', f'{R:.1f} m'),
                            ('Khối bên:', '2 khối, 6 lớp + lõi thang'))):
    add_svg(f'<text x="36" y="{YB + 62 + i * 25}" font-size="13.5" fill="#2b3547">{k}</text>')
    add_svg(f'<text x="296" y="{YB + 62 + i * 25}" font-size="13.5" font-weight="700" text-anchor="end" fill="#111">{v}</text>')

# la ban (N huong xuong vi so do xoay 180 do so voi ban do bac-len)
cx, cy = 1370, 80
add_svg(f'<circle cx="{cx}" cy="{cy}" r="40" fill="none" stroke="#1f2d44" stroke-width="2"/>')
add_svg(f'<polygon points="{cx - 9},{cy} {cx + 9},{cy} {cx},{cy + 40}" fill="#1f2d44"/>')
add_svg(f'<polygon points="{cx - 9},{cy} {cx + 9},{cy} {cx},{cy - 40}" fill="#9fb0c9"/>')
for lab, dx, dy in (('N', 0, 66), ('S', 0, -52), ('E', -58, 6), ('W', 58, 6)):
    add_svg(f'<text x="{cx + dx}" y="{cy + dy}" font-size="19" text-anchor="middle" fill="#1f2d44" font-weight="700">{lab}</text>')

# thuoc ty le
sx0, sy0 = 1230, 190
add_svg(f'<line x1="{sx0}" y1="{sy0}" x2="{sx0 + 10 * S}" y2="{sy0}" stroke="#1f2d44" stroke-width="2"/>')
for m in range(0, 11, 2):
    add_svg(f'<line x1="{sx0 + m * S}" y1="{sy0 - 7}" x2="{sx0 + m * S}" y2="{sy0 + 7}" stroke="#1f2d44" stroke-width="2"/>')
    add_svg(f'<text x="{sx0 + m * S}" y="{sy0 - 14}" font-size="14" text-anchor="middle">{m}</text>')
add_svg(f'<text x="{sx0 + 10 * S + 14}" y="{sy0 - 14}" font-size="14">m</text>')

# ---------------- danh sach phong + chu giai ----------------
add_svg(f'<rect x="330" y="{YB}" width="560" height="240" rx="8" fill="#f3f5f9" stroke="#d5dbe6"/>')
add_svg(f'<text x="350" y="{YB + 32}" font-size="19" font-weight="700" fill="#1f2d44">Danh sách khu vực</text>')
rows = (('Sảnh', 'Không gian chung, đón khách'), ('Cửa vào chính', 'Cửa kính 4 cánh, mái đón xe'),
        ('Quầy lễ tân', 'Hõm phía sau, tường logo HUST'), ('Ghế bê tông', 'Ghế V trắng sát tường kính'),
        ('Thang máy 1–2', 'Cánh Đông, cạnh hành lang'), ('Thang máy 3–4', 'Cánh Tây, sát sảnh'),
        ('Cầu thang thẳng 2 hướng', 'Cánh Đông, sát sảnh'), ('Lớp học', '102–104 (Đông), 106–108 (Tây)'),
        ('Một phòng kín', 'Phía sau đỉnh quạt, có cửa sau'))
for i, (a_, b_) in enumerate(rows):
    add_svg(f'<text x="350" y="{YB + 60 + i * 19}" font-size="13.5" fill="#222">{a_}</text>')
    add_svg(f'<text x="540" y="{YB + 60 + i * 19}" font-size="13.5" fill="#222">{b_}</text>')

add_svg(f'<rect x="910" y="{YB}" width="570" height="230" rx="8" fill="#f3f5f9" stroke="#d5dbe6"/>')
add_svg(f'<text x="930" y="{YB + 32}" font-size="19" font-weight="700" fill="#1f2d44">Chú giải</text>')
items = (('<rect x="0" y="-6" width="46" height="9" fill="#1f2d44"/>', 'Tường chính'),
         (f'<rect x="0" y="-8" width="46" height="14" fill="{CREAM}" stroke="#b9a974"/>', 'Sảnh, hành lang'),
         ('<rect x="0" y="-5" width="46" height="5" fill="#7db8ea"/>', 'Cửa sổ kính'),
         (f'<rect x="0" y="-8" width="46" height="14" fill="{BLUE}" stroke="#1f2d44"/>', 'Lớp học'),
         (f'<rect x="0" y="-8" width="46" height="14" fill="{GREY}" stroke="#1f2d44"/>', 'Thang máy'),
         ('<rect x="0" y="-8" width="46" height="14" fill="#fafafa" stroke="#8b93a3"/><line x1="12" y1="-8" x2="12" y2="6" stroke="#9aa3b3"/><line x1="24" y1="-8" x2="24" y2="6" stroke="#9aa3b3"/><line x1="36" y1="-8" x2="36" y2="6" stroke="#9aa3b3"/>', 'Thang bộ'),
         ('<rect x="0" y="-8" width="46" height="14" fill="#dfe4ec" stroke="#1f2d44"/>', 'Ghế bê tông'),
         ('<rect x="0" y="-8" width="46" height="14" fill="#f5f5f2" stroke="#1f2d44"/>', 'Quầy lễ tân'),
         ('<line x1="0" y1="0" x2="46" y2="0" stroke="#6c7b93" stroke-width="1.5" stroke-dasharray="7 5"/>', 'Mái đón xe (ngoài tường)'))
for i, (g, lab) in enumerate(items):
    cx0, cy0 = (930 if i < 5 else 1210), YB + 70 + (i % 5) * 30
    add_svg(f'<g transform="translate({cx0},{cy0})">{g}</g>')
    add_svg(f'<text x="{cx0 + 58}" y="{cy0 + 5}" font-size="13.5" fill="#222">{lab}</text>')

add_svg('</svg>')
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf-8').write('\n'.join(svg))
print('wrote', OUT, 'inner area', round(ia, 1), 'outer area', round(area(outer), 1))
