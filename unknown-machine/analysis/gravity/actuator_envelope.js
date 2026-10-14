// Gravity sim: the unknown-machine joint actuator's torque-speed envelope, traced by a swarm of virtual actuators.
// Each particle is one actuator (Kollmorgen KBM-17H01-B00 + 5:1 planetary) started from rest against its own load
// (an arm/fan-like load, T = c * w^2, a different c per particle). The drive gives as much current as its current
// limit and the DC bus allow; the particle accelerates along the motor's limit curve and stops where it meets its
// load. Together the particles draw the envelope: x = output speed, y = output torque, z = output power.
// Three families: drive current limit (orange, knob), motor continuous rating 3.11 A (blue), motor peak 10.9 A (green).

export const meta = {
  title: 'Joint actuator torque-speed envelope',
  summary: 'Each point is one KBM-17H01-B00 + 5:1 planetary actuator spinning up against its own load. Together they trace the torque-speed limits: current-limited flat top, then the back-EMF voltage roll-off.',
  particleCount: 30000,
  particleCountOptions: [3000, 9000, 30000],
  dt: 0.0005,
  pointSize: 0.011,
  trail: 40,
  bloom: 1.0,
  camera: { position: [-0.9, 0.15, 3.4], target: [0, 0, 0] },
  params: [
    { key: 'bus', label: 'DC bus (V)', min: 48, max: 400, step: 1, default: 325 },
    { key: 'ilim', label: 'drive current limit (A rms)', min: 1, max: 10.9, step: 0.1, default: 5.9 },
    { key: 'ratio', label: 'gear ratio', min: 3, max: 10, step: 0.5, default: 5 },
    { key: 'eta', label: 'gear efficiency', min: 0.85, max: 0.99, step: 0.01, default: 0.97 },
    { key: 'jload', label: 'arm inertia at output (kg m^2)', min: 0.005, max: 0.2, step: 0.005, default: 0.05 },
    { key: 'cycle', label: 'restart every (s)', min: 0.2, max: 2, step: 0.05, default: 0.55 },
  ],
  doc: {
    about: 'Where the curves bend is the corner speed: below it the drive current limit sets the torque; above it the motor back-EMF uses up the bus voltage and torque falls to zero at the no-load speed. Peak output power sits at the corner.',
    howItWorks: 'Per particle: J dw/dt = Kt I(w) - T_load(w)/(N eta), with I(w) = min(I_limit, (V_avail - Ke w)/(sqrt(3) R_ph)) and V_avail = 0.95 V_bus / sqrt(2) (line-line rms, sine commutation). Output torque N eta Kt I, output speed w/N.',
    equations: [
      { label: 'voltage limit', latex: 'I_v(\\omega)=\\frac{0.95\\,V_{bus}/\\sqrt2-K_e\\,\\omega}{\\sqrt3\\,R_{ph}}' },
      { label: 'motor torque', latex: 'T_m=K_t\\,\\min(I_{lim},I_v)\\,(1-s)' },
      { label: 'output', latex: 'T_{out}=N\\eta T_m,\\quad \\omega_{out}=\\omega/N,\\quad P=T_{out}\\omega_{out}' },
    ],
    symbols: [
      { key: 'Kt', symbol: 'K_t', meaning: '0.681 N m/A rms (catalog p. 20)' },
      { key: 'Ke', symbol: 'K_e', meaning: '41.2 V rms/krpm line-line = 0.393 V s/rad' },
      { key: 'R', symbol: 'R_ph', meaning: '6.02 ohm line-line / 2' },
      { key: 's', symbol: 's', meaning: 'saturation: 0 up to 3.11 A, rising so 10.9 A gives the catalog 6.14 N m' },
    ],
    integrator: 'explicit Euler, dt = 0.5 ms (time constant of the voltage roll-off is about 40 ms)',
    mapping: 'output speed 0-1200 rpm -> x; output torque 0-30 N m -> y; output power 0-2.5 kW -> z (depth)',
    assumptions: 'Winding inductance, iron and friction losses, PWM dead time and field weakening are ignored; 5% of the bus is kept as control headroom; constant gear efficiency.',
    limitations: 'Peak values are short-term: at 5.9 A the copper loss is about 310 W, so the flat top is for seconds, not minutes. The continuous line is the catalog rating with the housing well cooled (bolted to metal).',
    references: [{ label: 'Kollmorgen KBM selection guide, p. 20', url: 'https://www.electromate.com/media/assets/catalog-library/pdfs/kollmorgen/Kollmorgen_KBM_Frameless_Motors_Catalog.pdf' }],
  },
};

export function create(ctx) {
  const { particleCount: n, positions: pos, colors: col, rng } = ctx;
  const KT = 0.681, KE = 41.2 * 60 / (2 * Math.PI) / 1000, RPH = 6.02 / 2, ICONT = 3.11, IPK = 10.9;
  const SAT = 1 - 6.14 / (KT * IPK);                 // torque lost to saturation at the catalog peak
  const JM = 2.0e-4;                                   // kg m^2 rotor + sun + carrier (estimate)
  const X = (rpm) => -2.2 + rpm / 1200 * 4.4, Y = (t) => -1.5 + t / 30 * 3.0, Z = (w) => -0.6 + w / 2500 * 1.2;

  const nAxis = Math.min(3000, Math.floor(n * 0.1));
  const nAct = n - nAxis;
  const w = new Float64Array(nAct), c = new Float64Array(nAct), fam = new Uint8Array(nAct);
  for (let i = 0; i < nAct; i++) {
    fam[i] = i % 3;                                    // 0 drive limit, 1 continuous, 2 motor peak
    c[i] = Math.exp(Math.log(3e-5) + rng() * (Math.log(5) - Math.log(3e-5)));   // N m s^2, load T_out = c w_out^2, log-spread
    // Same colours as motor-curves.png (validated dark palette): drive #d95926, continuous #3987e5, motor peak #199e70.
    col.set(fam[i] === 0 ? [0.851, 0.349, 0.149] : fam[i] === 1 ? [0.224, 0.529, 0.898] : [0.098, 0.620, 0.439], i * 3);
  }
  // Axes and grid: speed axis with ticks every 200 rpm, torque axis every 5 N m, faint grid points.
  let a = nAct;
  const put = (x, y, z, b) => { if (a < n) { pos.set([x, y, z], a * 3); col.set([b, b, b * 1.05], a * 3); a++; } };
  const axisN = Math.floor(nAxis * 0.3);
  for (let k = 0; k < axisN; k++) { put(X(1200 * k / axisN), Y(0), Z(0), 0.7); put(X(0), Y(30 * k / axisN), Z(0), 0.7); }
  for (let r = 200; r <= 1200; r += 200) for (let k = 0; k < 12; k++) put(X(r), Y(-0.6 + k * 0.05), Z(0), 0.85);
  for (let t = 5; t <= 30; t += 5) for (let k = 0; k < 12; k++) put(X(-12 + k * 1.0), Y(t), Z(0), 0.85);
  for (let r = 200; r <= 1200; r += 200) for (let t = 5; t <= 30; t += 5) put(X(r), Y(t), Z(0), 0.45);
  while (a < n) { put(X(0), Y(0), Z(0), 0.7); }

  let t = 0;
  const draw = (p, dt) => {
    const N = p.ratio, eta = p.eta, J = JM + p.jload / (N * N);
    const vav = 0.95 * p.bus / Math.SQRT2;
    for (let i = 0; i < nAct; i++) {
      const ilim = fam[i] === 0 ? p.ilim : fam[i] === 1 ? ICONT : IPK;
      const iv = (vav - KE * w[i]) / (Math.sqrt(3) * RPH);
      const I = Math.max(0, Math.min(ilim, iv));
      const s = I > ICONT ? SAT * (I - ICONT) / (IPK - ICONT) : 0;
      const tm = KT * I * (1 - s);
      const wo = w[i] / N;
      const tl = c[i] * wo * wo / (N * eta);
      const tout = tm * N * eta;
      const o = i * 3;
      pos[o] = X(wo * 60 / (2 * Math.PI));
      pos[o + 1] = Y(tout);
      pos[o + 2] = Z(tout * wo);
      w[i] = Math.max(0, w[i] + (tm - tl) / J * dt);
    }
  };
  draw(ctx.params, 0);

  return {
    step(dt, p) {
      t += dt;
      if (t > p.cycle) { t = 0; w.fill(0); }
      draw(p, dt);
    },
    observe() {
      return { t_s: t };
    },
  };
}
