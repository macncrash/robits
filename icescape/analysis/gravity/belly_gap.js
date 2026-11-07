/**
 * Kinematic belly clearance. Not a dynamics solve.
 *
 * Both wheels stay on a sine ridge. The hull pitches with the axles and the
 * skid is a straight line 68 mm below them. observe() reports the gap.
 * Particles draw the ice, the two wheels and the hull. Y is up. 1 unit = 1 m.
 * The rover stays centred and the ridge scrolls.
 */
export const meta = {
  title: 'Icescape belly gap',
  summary: 'Side view of the rover on a sine ridge. The gap under the skid is computed, not simulated.',
  particleCount: 8000,
  dt: 0.016,
  params: [
    { key: 'ampMm', label: 'ridge mm', min: 0, max: 400, step: 10, default: 150 },
    { key: 'waveM', label: 'wavelength m', min: 1.5, max: 8, step: 0.1, default: 3 },
    { key: 'speed', label: 'speed m/s', min: 0, max: 1.5, step: 0.05, default: 0.6 },
  ],
  camera: { position: [0.1, 0.7, 4.2], target: [0, 0.45, 0], fov: 32 },
  pointSize: 0.012,
  doc: {
    about: 'Whether the icescape hull strikes a rounded ridge.',
    howItWorks: 'The axles sit one wheel radius above the sine, along the surface normal. The skid is 68 mm below the axle line. The gap is the smallest difference between the skid and the ice.',
    equations: [
      { label: 'axle height', latex: 'z = h + R\\sqrt{1+(dh/dx)^2}' },
    ],
    assumptions: [
      'No suspension travel. The CAD swing is plus or minus 6 degrees, about 40 mm, and is not added.',
      'The skid runs from 0.38 m behind the rear axle to 0.14 m ahead of the front axle.',
      'A strike is a negative gap. The wheels are not allowed to leave the surface.',
    ],
    limitations: [
      'This does not model sink into snow, wheel slip, or a sharp block of ice.',
      'The picture is particles. The number is the kinematics.',
    ],
    integrator: 'sampled, not integrated',
    mapping: '1 unit = 1 m. The rover stays centred and the ridge scrolls.',
  },
};

const R = 0.34;
const WB = 1.28;
const DROP = 0.068;
const BELLY_REAR = 0.38;
const BELLY_FRONT = 0.14;

export function create(ctx) {
  const n = ctx.particleCount;
  const pos = ctx.positions;
  const col = ctx.colors;
  const nGround = Math.floor(n * 0.42);
  const nWheels = Math.floor(n * 0.28);
  const nBody = n - nGround - nWheels;
  const halfWheels = Math.floor(nWheels / 2);
  let x = 0;
  let gap = 0.272;
  let pitch = 0;

  function h(s, amp, k) {
    return amp * Math.sin(k * s);
  }
  function hp(s, amp, k) {
    return amp * k * Math.cos(k * s);
  }

  return {
    step(dt, p) {
      const amp = p.ampMm / 1000;
      const k = (2 * Math.PI) / p.waveM;
      x += p.speed * dt;
      const x1 = x - WB / 2;
      const x2 = x + WB / 2;
      const z1 = h(x1, amp, k) + R * Math.sqrt(1 + hp(x1, amp, k) ** 2);
      const z2 = h(x2, amp, k) + R * Math.sqrt(1 + hp(x2, amp, k) ** 2);
      pitch = Math.atan2(z2 - z1, WB);
      const c = Math.cos(pitch);
      const s = Math.sin(pitch);
      let worst = 1e9;
      const span = WB + BELLY_FRONT + BELLY_REAR;
      for (let i = 0; i <= 40; i++) {
        const t = -BELLY_REAR + span * (i / 40);
        const bx = x1 + t * c;
        const bz = z1 + t * s - DROP * c;
        const d = bz - h(bx, amp, k);
        if (d < worst) worst = d;
      }
      gap = worst;
      const struck = gap < 0;

      for (let i = 0; i < nGround; i++) {
        const u = (i / nGround - 0.5) * 6;
        const o = i * 3;
        pos[o] = u;
        pos[o + 1] = h(x + u, amp, k);
        pos[o + 2] = ((i * 17) % 9) * 0.012 - 0.05;
        col[o] = 0.62;
        col[o + 1] = 0.82;
        col[o + 2] = 0.95;
      }

      for (let i = 0; i < nWheels; i++) {
        const rear = i < halfWheels;
        const j = rear ? i : i - halfWheels;
        const count = rear ? halfWheels : nWheels - halfWheels;
        const a = (j / count) * Math.PI * 2;
        const o = (nGround + i) * 3;
        const cx = rear ? -WB / 2 : WB / 2;
        const cz = rear ? z1 : z2;
        pos[o] = cx + Math.cos(a) * R;
        pos[o + 1] = cz + Math.sin(a) * R;
        pos[o + 2] = rear ? -0.04 : 0.04;
        col[o] = 0.75;
        col[o + 1] = 0.88;
        col[o + 2] = 0.98;
      }

      const rows = 12;
      for (let i = 0; i < nBody; i++) {
        const coln = i % 48;
        const row = Math.floor(i / 48) % rows;
        const t = -BELLY_REAR + span * (coln / 47);
        const lift = row / (rows - 1);
        const o = (nGround + nWheels + i) * 3;
        pos[o] = -WB / 2 + t * c;
        pos[o + 1] = z1 + t * s - DROP * c + lift * 0.42;
        pos[o + 2] = ((i * 13) % 5) * 0.01 - 0.02;
        const nose = t > WB + 0.02 && lift > 0.55 && lift < 0.75;
        const low = lift < 0.12;
        if (nose) {
          col[o] = 0.55;
          col[o + 1] = 0.95;
          col[o + 2] = 1;
        } else if (low) {
          col[o] = struck ? 0.95 : 0.8;
          col[o + 1] = struck ? 0.25 : 0.92;
          col[o + 2] = struck ? 0.15 : 1;
        } else {
          col[o] = 0.22;
          col[o + 1] = 0.26;
          col[o + 2] = 0.32;
        }
      }
    },
    observe() {
      return {
        gapMm: Math.round(gap * 1000),
        pitchDeg: Math.round((pitch * 180) / Math.PI * 10) / 10,
        strike: gap < 0 ? 1 : 0,
      };
    },
  };
}
