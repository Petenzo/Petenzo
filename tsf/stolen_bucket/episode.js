// THE WAR OF THE BUCKET (Modena vs Bologna, 1325). Narration: SCRIPT.txt. Times come from words.json.
// Every cue is tied to a phrase of the voice-over, with a backup time in case the phrase is not found.
import * as THREE from 'three';
import { ground, road, house, tree, clouds, toon, mesh, TEX } from '../../engine/world.js';
import * as K from '../../engine/kit.js';
import { Actor } from '../../engine/actor.js';
import { outfit, SKINS } from '../../engine/chars.js';
import { animal } from '../../engine/animals.js';
import { puff, dust, sparkle, confetti, fall } from '../../engine/fx.js';
import { keys, creep, shake, prog, lerp, easeOut, smoother } from '../../engine/film.js';

export function build({ stage, words }) {
  const T = (phrase, backup) => words.phrase(phrase, 0, backup);
  const END = Math.max(words.last, 71.9) + 1.2;

  // ---------------------------------------------------------------- props
  const bucket = (s = 1) => {
    const g = new THREE.Group(), wood = toon('#9a6a3a'), iron = toon('#4a4e56');
    const body = mesh(new THREE.CylinderGeometry(0.22, 0.17, 0.34, 20), wood); body.position.y = 0.17; g.add(body);
    for (const y of [0.06, 0.28]) { const b = mesh(new THREE.TorusGeometry(y < 0.1 ? 0.18 : 0.215, 0.018, 6, 24), iron); b.rotation.x = Math.PI / 2; b.position.y = y; g.add(b); }
    const h = mesh(new THREE.TorusGeometry(0.21, 0.014, 6, 24, Math.PI), iron); h.position.y = 0.34; g.add(h);
    g.scale.setScalar(s); stage.add(g); return g;
  };
  const tower = (x, z, w, h, col = '#c9a27a', roof = null) => { // a stone tower with battlements
    const g = new THREE.Group(); g.position.set(x, 0, z);
    const m = mesh(new THREE.BoxGeometry(w, h, w), toon(col)); m.position.y = h / 2; g.add(m);
    for (let i = 0; i < 4; i++) for (let k = 0; k < 3; k++) { const c = mesh(new THREE.BoxGeometry(w / 5, w / 5, w / 5), toon(col)); const a = (k - 1) * w * 0.38; const p = [[a, w / 2], [a, -w / 2], [w / 2, a], [-w / 2, a]][i]; c.position.set(p[0], h + w / 10, p[1]); g.add(c); }
    if (roof) { const r = mesh(new THREE.ConeGeometry(w * 0.75, w * 1.1, 4), toon(roof)); r.rotation.y = Math.PI / 4; r.position.y = h + w * 0.55; g.add(r); }
    stage.add(g); return g;
  };
  const flag = (x, z, col, h = 6) => K.flagpole(stage, { x, z, h, col });

  // ---------------------------------------------------------------- sets
  ground(stage, { tex: 'grass', color: '#c8d890', size: 1400 }); clouds(stage, { n: 9 });

  // BATTLEFIELD near Zappolino (x = 0): rolling hills, a hilltop castle, a dirt road, cypress trees
  K.hills(stage, { z: -170, col: '#9fb070' });
  road(stage, { x: 0, z: 0, w: 4, len: 400, tex: 'sand', line: false, curb: false });
  const cyp = (x, z, s = 1) => { const g = new THREE.Group(); const c = mesh(new THREE.ConeGeometry(0.7 * s, 5 * s, 10), toon('#3f6a3a')); c.position.y = 2.6 * s; g.add(c); g.position.set(x, 0, z); stage.add(g); };
  for (const [x, z, s] of [[-14, -10, 1.1], [-16, -12, 0.9], [15, -14, 1.2], [18, -11, 1], [-26, 4, 1.2], [27, 2, 1.1], [-8, -26, 1], [9, -27, 1.1]]) cyp(x, z, s);
  const hill = mesh(new THREE.SphereGeometry(16, 24, 12), toon('#a9b878')); hill.scale.y = 0.35; hill.position.set(0, -1, -48); stage.add(hill);
  tower(-3.2, -46, 4, 9, '#c9a27a', '#a8483a'); tower(3.8, -46.5, 3.2, 7, '#c9a27a'); tower(0.4, -44, 6, 4.5, '#d4b48a');
  flag(-3.2, -46, '#2f5fa8', 13);

  // BOLOGNA'S WALLS AND GATE (x = 300)
  const brick = K.TEX2.bricks('#b5623b'); brick.repeat.set(12, 2);
  const wall = mesh(new THREE.BoxGeometry(70, 7, 2.4), toon('#ffffff', brick)); wall.position.set(300, 3.5, -10); stage.add(wall);
  for (let i = -17; i <= 17; i++) { const c = mesh(new THREE.BoxGeometry(1.1, 0.9, 2.4), toon('#b5623b')); c.position.set(300 + i * 2, 7.45, -10); stage.add(c); }
  tower(292.5, -10, 4.4, 10, '#b5623b'); tower(307.5, -10, 4.4, 10, '#b5623b');
  const arch = mesh(new THREE.PlaneGeometry(4.2, 5.2), toon('#1d1a1a')); arch.position.set(300, 2.6, -8.78); stage.add(arch);
  const door = mesh(new THREE.BoxGeometry(4.0, 5.0, 0.2), toon('#6a4428', TEX.planks())); door.position.set(300, 2.5, -8.7); stage.add(door);
  for (let i = 0; i < 9; i++) house(stage, { x: 270 + i * 7.5, z: -19, w: 6.5, d: 6, h: 11 + (i % 3) * 2, wall: ['#e8b070', '#d9925a', '#efc890'][i % 3], roof: '#a8483a', floors: 3, cols: 2, seed: i + 3, chimney: false });
  tower(318, -24, 3.5, 26, '#c08060'); tower(284, -26, 3, 22, '#b87858'); // Bologna's famous tall towers
  road(stage, { x: 300, z: 30, w: 4.2, len: 76, tex: 'cobble', line: false, curb: false });
  // the well
  const well = new THREE.Group(); well.position.set(304.5, 0, -3);
  { const ring = mesh(new THREE.CylinderGeometry(0.8, 0.85, 0.85, 20, 1, true), toon('#b8b0a0')); ring.position.y = 0.42; ring.material.side = THREE.DoubleSide; well.add(ring);
    const top = mesh(new THREE.TorusGeometry(0.8, 0.09, 6, 24), toon('#a8a090')); top.rotation.x = Math.PI / 2; top.position.y = 0.86; well.add(top);
    const inside = mesh(new THREE.CircleGeometry(0.78, 20), toon('#1a2a3a')); inside.rotation.x = -Math.PI / 2; inside.position.y = 0.5; well.add(inside);
    for (const sx of [-1, 1]) { const p = mesh(new THREE.BoxGeometry(0.12, 2.1, 0.12), toon('#7a5230')); p.position.set(sx * 0.9, 1.05, 0); well.add(p); }
    const bar = mesh(new THREE.CylinderGeometry(0.06, 0.06, 2.0, 8), toon('#7a5230')); bar.rotation.z = Math.PI / 2; bar.position.y = 2.0; well.add(bar);
    const rf = mesh(new THREE.ConeGeometry(1.4, 0.7, 4), toon('#a8483a')); rf.rotation.y = Math.PI / 4; rf.position.y = 2.45; well.add(rf); }
  stage.add(well);
  const rope = mesh(new THREE.CylinderGeometry(0.012, 0.012, 1, 6), toon('#d8c49a')); stage.add(rope);
  const B1 = bucket(1);  // THE bucket

  // TWO CITIES ON A MAP-LIKE PLAIN (x = -150)
  for (const [cx, col] of [[-157, '#2f5fa8'], [-143, '#b8302a']]) {
    const m = mesh(new THREE.SphereGeometry(5, 20, 10), toon('#b8c880')); m.scale.y = 0.3; m.position.set(cx, -0.5, -6); stage.add(m);
    for (let i = 0; i < 5; i++) house(stage, { x: cx - 2.6 + (i % 3) * 2.4, z: -6 - Math.floor(i / 3) * 2.4, w: 2, d: 2, h: 3.4, wall: '#efd0a0', roof: '#a8483a', floors: 1, cols: 1, seed: i + (cx > -150 ? 9 : 1), chimney: false });
    tower(cx + 1.2, -9.5, 1.3, 6, '#c9a27a', col === '#2f5fa8' ? '#2f5fa8' : '#a8483a'); flag(cx - 2.2, -3.5, col, 5);
  }
  road(stage, { x: -150, z: -4, w: 1.2, len: 12, rot: Math.PI / 2, tex: 'sand', line: false, curb: false });

  // POET'S STUDY (x = -300) and MODENA TOWER ROOM (x = -340)
  K.room(stage, { x: -300, z: 0, w: 7, d: 6, wall: '#e8d8b8', stripe: '#e0cfac', windowAt: 0.3 });
  K.table(stage, { x: -299.6, z: -1.3, w: 1.6, d: 0.8, col: '#6a4428' }); K.shelf(stage, { x: -302.3, z: -2.7, w: 1.3 });
  const candle = mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.22, 8), toon('#f4efe2')); candle.position.set(-299.1, 0.93, -1.4); stage.add(candle);
  const papers = mesh(new THREE.BoxGeometry(0.45, 0.05, 0.32), toon('#f4efe2')); papers.position.set(-299.9, 0.83, -1.3); stage.add(papers);
  K.room(stage, { x: -340, z: 0, w: 7, d: 6, wall: '#c9b89a', stripe: null, floor: 'tiles', windowAt: 0.5, door: false });
  const ped = mesh(new THREE.BoxGeometry(0.9, 1.05, 0.9), toon('#e8e0d0')); ped.position.set(-340, 0.525, -1.4); stage.add(ped);
  const rail = mesh(new THREE.BoxGeometry(2.4, 0.06, 0.06), toon('#c8a040')); rail.position.set(-340, 0.9, -0.3); stage.add(rail);
  for (const sx of [-1, 1]) { const p = mesh(new THREE.CylinderGeometry(0.04, 0.05, 0.9, 8), toon('#c8a040')); p.position.set(-340 + sx * 1.2, 0.45, -0.3); stage.add(p); }
  K.picture(stage, { x: -341.9, y: 2.2, z: -2.97, col: '#2f5fa8' }); K.picture(stage, { x: -338.1, y: 2.2, z: -2.97, col: '#e8c040' });
  const B2 = bucket(1.1); B2.position.set(-340, 1.05, -1.4);

  // ---------------------------------------------------------------- cast
  const red = { shirt: '#b8302a', pants: '#5a2420', shoes: '#3b2a20', hat: 'helmet', hatCol: '#a8aeb8' };
  const blue = { shirt: '#2f5fa8', pants: '#e8c040', shoes: '#3b2a20', hat: 'helmet', hatCol: '#a8aeb8' };
  const REDS = Array.from({ length: 30 }, (_, i) => stage.add(new Actor(outfit({ ...red, skin: SKINS[i % 4], build: i % 5 === 0 ? 'big' : 'adult' }), { seed: 10 + i })));
  const BLUES = Array.from({ length: 12 }, (_, i) => stage.add(new Actor(outfit({ ...blue, skin: SKINS[(i + 1) % 4], build: i % 4 === 0 ? 'tall' : 'adult' }), { seed: 50 + i })));
  const HERO = stage.add(new Actor(outfit({ ...blue, mustache: '#3b2a20', skin: SKINS[1] }), { seed: 71 }));   // the Modenese soldier who takes the bucket
  const RCAP = stage.add(new Actor(outfit({ ...red, hatCol: '#d8b040', mustache: '#2a1a14', badge: '#f2c230', build: 'big', skin: SKINS[0] }), { seed: 72 })); // Bologna commander
  const BNOB = stage.add(new Actor(outfit({ shirt: '#8a1f1f', pants: '#2a1a14', hat: 'beanie', hatCol: '#b8302a', skin: SKINS[0], mustache: '#5a3a2a', collar: '#f4efe2' }), { seed: 73 })); // Bologna noble
  const MNOB = stage.add(new Actor(outfit({ shirt: '#1f3f7a', pants: '#e8c040', hat: 'beanie', hatCol: '#2f5fa8', skin: SKINS[1], hair: '#2a1a14', collar: '#f4efe2' }), { seed: 74 }));   // Modena noble
  const POET = stage.add(new Actor(outfit({ shirt: '#5a3a6a', pants: '#2a2230', hairStyle: 'curly', hair: '#2a1a14', mustache: '#2a1a14', collar: '#f4efe2', skin: SKINS[1] }), { seed: 75 }));
  const HORSES = Array.from({ length: 4 }, (_, i) => stage.add(new Actor(animal('horse', { col: ['#8a5a3a', '#3b2a20', '#c8a070', '#f0ece4'][i] }), { seed: 80 + i, scale: 1 })));
  const ALL = [...REDS, ...BLUES, HERO, RCAP, BNOB, MNOB, POET, ...HORSES];
  const R = (i, k = 1) => { const v = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return v - Math.floor(v); };

  const reset = () => {
    for (const a of ALL) { a.g.visible = false; a.set({ pose: 'idle', expr: 'neutral', walk: null, flip: false, hop: 0, lean: 0, squash: 0, talk: false, hold: null, bubble: null }); a.g.position.y = 0; }
    B1.position.set(304.5, 1.05, -3); B1.rotation.set(0, 0, 0); door.position.y = 2.5; rope.visible = true;
  };
  const show = (a, x, z, o = {}) => { a.g.visible = true; a.at(x, 0, z).set(o); return a; };
  const lift = (a, b, up = 0.35) => { const p = a.g.position; b.position.set(p.x, a.top + up, p.z + 0.06); }; // bucket held over the head
  const army = (arr, n, x, z, cols, sp, o = {}) => { for (let i = 0; i < n; i++) { const c = i % cols, r = Math.floor(i / cols); show(arr[i], x + (c - (cols - 1) / 2) * sp + (R(i) - 0.5) * 0.3, z - r * sp * 0.9 + (R(i, 2) - 0.5) * 0.3, typeof o === 'function' ? o(i) : o); } };

  // ---------------------------------------------------------------- times (phrase, backup)
  const t = {
    prize: T("The winner's prize", 4.05), wooden: T('A wooden bucket', 5.56), neigh: T('Modena and Bologna were', 7.05), forty: T('about forty kilometres', 9.12),
    hated: T('And they hated', 11.16), pope: T('Bologna backed the Pope', 12.66), emperor: T('Modena backed the Emperor', 14.2), nov: T('That November', 16.06),
    thirty: T('around thirty thousand', 18.42), seven: T('Modena had about', 20.62), easy: T('Easy win', 22.98), wasnt: T("It wasn't", 24.01),
    castle: T('Near a castle', 25.22), charged: T('the Modenese charged', 27.16), hours: T('In about two hours', 28.79), broke: T("Bologna's giant army", 30.07),
    home: T('All the way home', 32.61), chased: T('The Modenese chased', 34.11), gold: T('They could have taken', 37.22), prisoners: T('Prisoners', 38.83),
    city: T('Maybe the whole city', 39.84), instead: T('Instead, they walked', 41.48), stole: T('And stole the bucket', 43.4), races: T('Then, the story goes', 44.96),
    horse: T('held horse races', 46.69), rub: T('Just to rub it in', 49.64), died: T('Around two thousand men', 51.26), nothing: T('And the war changed', 53.56),
    trophy: T('But the bucket went home', 55.88), poet: T('Three hundred years later', 58.75), called: T('called The Stolen Bucket', 62.78), never: T('Bologna never got', 64.8),
    today: T("It's still in Modena", 66.72), seven7: T('Seven centuries later', 68.74), famous: T('most famous bucket', 70.53),
  };

  // effects placed in the world at their moments
  sparkle(stage, { at: [304.5, 1.4, -3], t0: t.wooden + 0.1, n: 10, spread: 0.6, size: 0.25 });
  for (let k = 0; k < 6; k++) dust(stage, { at: [-3 + k * 1.2, 0.3, -6 + k * 0.6], t0: t.charged + 0.3 + k * 0.15, n: 8, size: 0.7, color: '#d8c49a' });
  for (let k = 0; k < 5; k++) dust(stage, { at: [0, 0.3, 2 - k * 4], t0: t.home + k * 0.3, n: 8, size: 0.6, color: '#d8c49a' });
  fall(stage, { at: [300, 3.4, 2], t0: t.gold + 0.15, color: '#d8a840', n: 40, area: [2.5, 1, 1.5], stagger: 1.3, size: 0.16, life: 1.2 });
  sparkle(stage, { at: [304.5, 2.4, -2.5], t0: t.stole + 0.45, n: 12, spread: 0.8, size: 0.3 });
  for (let k = 0; k < 8; k++) dust(stage, { at: [290 + k * 3, 0.3, -5.5], t0: t.horse + k * 0.25, n: 8, size: 0.7, color: '#d8c49a' });
  confetti(stage, { at: [0, 4, 0], t0: t.trophy + 0.2, n: 60, area: [8, 1, 4] });

  // ---------------------------------------------------------------- shots
  const S = [];
  const shot = (from, light, cam, update, extra = {}) => S.push({ from, light, cam, update: (tt, c) => { reset(); update(tt, c); }, ...extra });

  // 1. "In 1325, two Italian cities went to war."  two armies face each other across the road
  shot(0, 'day', keys([{ t: 0, pos: [0, 2.2, 10.5], look: [0, 1.3, -0.5], fov: 46 }, { t: t.prize, pos: [0, 1.6, 8.2], look: [0, 1.3, -0.5], fov: 46 }]), (tt) => {
    army(REDS, 12, 1.9, 0.5, 3, 0.85, (i) => ({ flip: true, expr: 'angry', pose: i % 4 === 0 && tt > 2.8 ? 'point' : 'idle' }));
    army(BLUES, 9, -1.9, 0.5, 3, 0.85, () => ({ expr: 'determined' }));
  }, { dof: () => ({ target: [0, 1.4, 0], cInf: 5 }) });
  // 2. "The winner's prize?"
  shot(t.prize, 'day', creep(() => ({ pos: [0.3, 1.55, 3.2], look: [0.1, 1.42, 0.2], fov: 40 }), t.prize, 0.04), () => {
    show(HERO, 0.1, 0.2, { pose: 'think', expr: 'worried', bubble: { kind: '?', t0: t.prize + 0.3 } });
  }, { dof: () => ({ target: [0.1, 1.45, 0.2], cInf: 10 }) });
  // 3. "A wooden bucket."
  shot(t.wooden, 'day', creep(() => ({ pos: [304.5, 1.55, -0.4], look: [304.5, 1.15, -3], fov: 40 }), t.wooden, 0.05), () => {
    rope.position.set(304.5, 1.7, -3); rope.scale.y = 0.6;
  }, { dof: () => ({ target: [304.5, 1.2, -3], cInf: 12 }) });
  // 4. "Modena and Bologna were neighbours, about forty kilometres apart."
  shot(t.neigh, 'day', keys([{ t: t.neigh, pos: [-150, 26, 32], look: [-150, 0, -7], fov: 50 }, { t: t.hated, pos: [-150, 20, 28], look: [-150, 0.5, -7], fov: 50 }]), () => {});
  // 5. "And they hated each other."
  shot(t.hated, 'day', creep(() => ({ pos: [0, 1.25, 5.6], look: [0, 1.15, 0.5], fov: 40 }), t.hated, 0.03), () => {
    show(MNOB, -0.7, 0.5, { pose: 'hips', expr: 'angry', bubble: { kind: 'anger', t0: t.hated + 0.4 } });
    show(BNOB, 0.7, 0.5, { pose: 'point', expr: 'angry', flip: true, bubble: { kind: 'anger', t0: t.hated + 0.7 } });
  }, { dof: () => ({ target: [0, 1.3, 0.5], cInf: 8 }) });
  // 6. "Bologna backed the Pope."
  shot(t.pope, 'day', creep(() => ({ pos: [1.0, 1.45, 4.6], look: [1.0, 1.35, 0.5], fov: 40 }), t.pope, 0.04), () => {
    show(BNOB, 0.7, 0.5, { pose: 'idle', expr: 'smug', hold: 'flag' });
  }, { dof: () => ({ target: [0.7, 1.4, 0.5], cInf: 10 }) });
  // 7. "Modena backed the Emperor."
  shot(t.emperor, 'day', creep(() => ({ pos: [-0.4, 1.45, 4.6], look: [-0.4, 1.35, 0.5], fov: 40 }), t.emperor, 0.04), () => {
    show(MNOB, -0.7, 0.5, { pose: 'idle', expr: 'smug', hold: 'flag' });
  }, { dof: () => ({ target: [-0.7, 1.4, 0.5], cInf: 10 }) });
  // 8. "That November, Bologna marched out with around thirty thousand soldiers."
  shot(t.nov, 'storm', keys([{ t: t.nov, pos: [9, 6, 14], look: [0, 1, -2], fov: 48 }, { t: t.seven, pos: [6, 3, 10], look: [0, 1.2, -2], fov: 46 }]), (tt) => {
    const z = 4 - (tt - t.nov) * 0.9;
    army(REDS, 30, 0, z, 5, 1.15, () => ({ walk: { speed: 1.8 }, expr: 'determined', flip: true }));
  });
  // 9. "Modena had about seven thousand."
  shot(t.seven, 'storm', creep(() => ({ pos: [-2.5, 1.7, 7.2], look: [-2.5, 1.2, 0.5], fov: 42 }), t.seven, 0.03), () => {
    army(BLUES, 6, -2.5, 0.8, 3, 1.0, (i) => ({ expr: 'worried', bubble: i === 1 ? { kind: 'sweat', t0: t.seven + 0.6 } : null }));
  });
  // 10. "Easy win."
  shot(t.easy, 'storm', creep(() => ({ pos: [0.2, 1.0, 3.6], look: [0.1, 1.55, 0.5], fov: 40 }), t.easy, 0.04), () => {
    show(RCAP, 0.1, 0.5, { pose: 'hips', expr: 'smug', flip: true, bubble: { kind: 'note', t0: t.easy + 0.2 } });
  }, { dof: () => ({ target: [0.1, 1.5, 0.5], cInf: 9 }) });
  // 11. "It wasn't."
  shot(t.wasnt, 'storm', () => ({ pos: [0.15, 1.62, 2.2], look: [0.1, 1.52, 0.5], fov: 38 }), () => {
    show(RCAP, 0.1, 0.5, { pose: 'scared', expr: 'shock', flip: true, bubble: { kind: '!', t0: t.wasnt + 0.2 } });
  }, { dof: () => ({ target: [0.1, 1.5, 0.5], cInf: 10 }), shake: shake([t.wasnt + 0.15], 0.03) });
  // 12. "Near a castle called Zappolino,"
  shot(t.castle, 'golden', keys([{ t: t.castle, pos: [6, 3, -10], look: [0, 5, -46], fov: 44 }, { t: t.charged, pos: [3, 2, -14], look: [0, 5, -46], fov: 42 }]), () => {});
  // 13. "the Modenese charged."
  shot(t.charged, 'golden', (tt) => ({ pos: [0.5, 0.6, 6 - (tt - t.charged) * 0.8], look: [0, 1.6, -4], fov: 46 }), (tt) => {
    const z = -6 + (tt - t.charged) * 4.2;
    army(BLUES, 12, 0, z, 4, 1.2, (i) => ({ walk: { speed: 3.4, run: true }, expr: 'determined', pose: 'arms_up' }));
    show(HERO, 0.4, z + 1.2, { walk: { speed: 3.4, run: true }, expr: 'determined', pose: 'point' });
  }, { shake: (tt) => Math.sin(tt * 31) * 0.015 });
  // 14. "In about two hours,"
  shot(t.hours, 'golden', creep(() => ({ pos: [2, 1.6, 9], look: [0, 1.2, 0], fov: 44 }), t.hours, 0.03), (tt) => {
    army(REDS, 12, 1, 0, 4, 1.1, (i) => ({ pose: 'scared', expr: 'shock', flip: true, bubble: i % 5 === 0 ? { kind: '!', t0: t.hours + R(i) * 0.6 } : null }));
  });
  // 15. "Bologna's giant army broke and ran."
  shot(t.broke, 'golden', () => ({ pos: [-10, 3.2, 10], look: [2, 1, -3], fov: 46 }), (tt) => {
    const u = Math.max(0, tt - t.broke - 0.8);
    army(REDS, 20, 2 + u * 3.5, -2, 5, 1.2, () => ({ walk: tt > t.broke + 0.8 ? { speed: 3.6, run: true } : null, pose: 'scared', expr: 'shock', flip: false }));
    army(BLUES, 8, -4 + u * 2.5, 0, 4, 1.2, () => ({ walk: { speed: 2.4 }, expr: 'grin', pose: 'arms_up' }));
  });
  // 16. "All the way home."  tracking the runners along the road
  shot(t.home, 'golden', (tt) => { const z = -(tt - t.home) * 5; return { pos: [5, 1.6, z + 4], look: [0, 1.2, z - 4], fov: 46 }; }, (tt) => {
    const z = -(tt - t.home) * 5;
    for (let i = 0; i < 6; i++) show(REDS[i], (i % 3 - 1) * 1.2, z - 4 - Math.floor(i / 3) * 1.4, { walk: { speed: 3.8, run: true }, pose: 'scared', expr: 'shock', flip: false });
  });
  // 17. "The Modenese chased them right up to the city gates."
  shot(t.chased, 'golden', keys([{ t: t.chased, pos: [300, 4, 22], look: [300, 3, -8], fov: 48 }, { t: t.gold, pos: [300, 2.4, 14], look: [300, 2.6, -8], fov: 46 }]), (tt) => {
    const u = prog(tt, t.chased, 2.4);
    for (let i = 0; i < 4; i++) show(REDS[i], 299 + i * 0.7, lerp(4, -8.4, easeOut(u)) - (i % 2), { walk: u < 1 ? { speed: 3.8, run: true } : null, pose: 'scared', expr: 'shock' });
    army(BLUES, 8, 300, lerp(14, 2, easeOut(prog(tt, t.chased + 0.4, 2.4))), 4, 1.1, () => ({ walk: { speed: 3, run: true }, expr: 'grin', pose: 'arms_up' }));
    door.position.y = tt > t.chased + 2.6 ? 2.5 : 7.5; // gate slams shut behind the last runner
  }, { shake: (tt) => (tt > t.chased + 2.6 && tt < t.chased + 2.9 ? 0.04 : 0) });
  // 18. "They could have taken gold."
  shot(t.gold, 'golden', creep(() => ({ pos: [300, 1.5, 5.2], look: [300, 1.5, 2], fov: 40 }), t.gold, 0.04), () => {
    show(HERO, 300, 2, { pose: 'arms_up', expr: 'grin', bubble: { kind: '$', t0: t.gold + 0.3 } });
  }, { dof: () => ({ target: [300, 1.5, 2], cInf: 10 }) });
  // 19. "Prisoners."
  shot(t.prisoners, 'golden', creep(() => ({ pos: [297.5, 1.5, 4.6], look: [298.2, 1.3, 1.2], fov: 40 }), t.prisoners, 0.04), () => {
    show(REDS[0], 297.7, 1.2, { pose: 'arms_up', expr: 'worried', bubble: 'sweat' }); show(BLUES[0], 298.8, 1.0, { pose: 'point', expr: 'smug', flip: true });
  }, { dof: () => ({ target: [298.2, 1.4, 1.2], cInf: 9 }) });
  // 20. "Maybe the whole city."
  shot(t.city, 'golden', keys([{ t: t.city, pos: [301.5, 0.6, 6], look: [300, 6, -12], fov: 50 }, { t: t.instead, pos: [301.5, 0.5, 4.5], look: [300, 7, -12], fov: 52 }]), () => {
    show(HERO, 301.2, 2.5, { pose: 'point', expr: 'grin', flip: true });
  });
  // 21. "Instead, they walked up to a well."
  shot(t.instead, 'golden', () => ({ pos: [307.2, 1.6, 4.4], look: [305.3, 1.15, -2.6], fov: 42 }), (tt) => {
    const u = prog(tt, t.instead, 1.6);
    show(HERO, lerp(309, 305.9, u), lerp(1, -2.4, u), { walk: u < 1 ? { speed: 1.6 } : null, expr: u < 1 ? 'neutral' : 'smile', flip: true, bubble: u >= 1 ? { kind: 'idea', t0: t.instead + 1.7 } : null });
    rope.position.set(304.5, 1.7, -3); rope.scale.y = 0.6;
  });
  // 22. "And stole the bucket."
  shot(t.stole, 'golden', creep(() => ({ pos: [305.4, 1.3, 1.6], look: [305.7, 1.6, -2.4], fov: 40 }), t.stole, 0.03), (tt) => {
    const up = tt > t.stole + 0.4;
    show(HERO, 305.9, -2.4, { pose: up ? 'arms_up' : 'idle', expr: up ? 'laugh' : 'smug', hop: up ? Math.max(0, Math.sin((tt - t.stole - 0.4) * 9)) * 0.12 : 0 });
    if (up) { lift(HERO, B1, 0.05); rope.visible = false; } else { rope.position.set(304.5, 1.7, -3); rope.scale.y = 0.6; }
  }, { dof: () => ({ target: [305.9, 1.6, -2.4], cInf: 9 }) });
  // 23. "Then, the story goes, they held horse races outside Bologna's walls."
  shot(t.races, 'day', (tt) => ({ pos: [292.5 + (tt - t.races) * 4.2, 1.2, 3.2], look: [293 + (tt - t.races) * 4.2, 1.3, -4.5], fov: 46 }), (tt) => {
    const u = tt - t.races;
    for (let i = 0; i < 4; i++) show(HORSES[i], 290.5 + u * 4.2 + i * 1.1, -3.6 - (i % 2) * 1.3, { walk: { speed: 3.6, run: true }, pose: 'run', expr: 'happy' });
  });
  // 24. "Just to rub it in."  angry Bolognese on top of their wall
  shot(t.rub, 'day', creep(() => ({ pos: [300, 8.9, -1.5], look: [300, 8.2, -9.6], fov: 42 }), t.rub, 0.03), () => {
    for (let i = 0; i < 4; i++) { show(REDS[i], 298.2 + i * 1.2, -9.6, { pose: i % 2 ? 'point' : 'hips', expr: 'angry', flip: i > 1, bubble: i === 1 ? { kind: 'anger', t0: t.rub + 0.2 } : i === 2 ? { kind: 'anger', t0: t.rub + 0.5 } : null }); REDS[i].g.position.y = 7; }
  });
  // 25. "Around two thousand men died that day."  quiet, empty field
  shot(t.died, 'storm', creep(() => ({ pos: [0, 1.2, 10], look: [0, 1.6, -10], fov: 44 }), t.died, 0.02), () => {}, { exposure: 0.9 });
  // 26. "And the war changed almost nothing."
  shot(t.nothing, 'day', creep(() => ({ pos: [0, 1.25, 5.6], look: [0, 1.15, 0.5], fov: 40 }), t.nothing, 0.03), () => {
    show(MNOB, -0.7, 0.5, { pose: 'shrug', expr: 'neutral' }); show(BNOB, 0.7, 0.5, { pose: 'shrug', expr: 'sad', flip: true, bubble: { kind: '...', t0: t.nothing + 0.5 } });
  }, { dof: () => ({ target: [0, 1.3, 0.5], cInf: 8 }) });
  // 27. "But the bucket went home to Modena as a trophy."  victory parade
  shot(t.trophy, 'golden', keys([{ t: t.trophy, pos: [0, 0.8, 7.2], look: [0, 2.0, 0], fov: 46 }, { t: t.poet, pos: [0, 0.6, 6.0], look: [0, 2.1, 0], fov: 46 }]), (tt) => {
    show(HERO, 0, 0, { pose: 'arms_up', expr: 'laugh', hop: Math.max(0, Math.sin(tt * 7)) * 0.1 }); lift(HERO, B1, 0.05);
    for (let i = 0; i < 8; i++) show(BLUES[i], (i % 4 - 1.5) * 1.3 + (i % 4 > 1 ? 0.6 : -0.6), -1.4 - Math.floor(i / 4) * 1.2, { pose: i % 2 ? 'cheer' : 'arms_up', expr: 'laugh', flip: i % 4 > 1 });
  });
  // 28. "Three hundred years later, a poet wrote a whole comic epic about it, called The Stolen Bucket."
  shot(t.poet, 'indoor', creep(() => ({ pos: [-300.1, 1.3, 3.4], look: [-300.1, 1.2, -1.6], fov: 40 }), t.poet, 0.03), (tt) => {
    show(POET, -300.3, -1.75, { pose: tt > t.called ? 'present' : 'think', expr: tt > t.called ? 'grin' : 'smug', hold: tt > t.called ? 'book' : null, bubble: { kind: 'idea', t0: t.poet + 1.2 } });
  }, { dof: () => ({ target: [-300.2, 1.4, -1.7], cInf: 9 }) });
  // 29. "Bologna never got it back."
  shot(t.never, 'day', creep(() => ({ pos: [0.7, 1.55, 3.0], look: [0.7, 1.4, 0.5], fov: 40 }), t.never, 0.04), () => {
    show(BNOB, 0.7, 0.5, { pose: 'shrug', expr: 'sad', flip: true, bubble: { kind: '...', t0: t.never + 0.3 } });
  }, { dof: () => ({ target: [0.7, 1.4, 0.5], cInf: 10 }) });
  // 30. "It's still in Modena today."
  shot(t.today, 'indoor', creep(() => ({ pos: [-340, 1.6, 3.4], look: [-340, 1.3, -1.4], fov: 42 }), t.today, 0.03), () => {});
  // 31. "Seven centuries later, it's the most famous bucket in Italy."
  shot(t.seven7, 'indoor', keys([{ t: t.seven7, pos: [-339.4, 1.4, 1.6], look: [-340, 1.25, -1.4], fov: 40 }, { t: END, pos: [-339.9, 1.33, 0.1], look: [-340, 1.25, -1.4], fov: 36 }]), (tt) => {
    B2.rotation.y = (tt - t.seven7) * 0.35;
  }, { dof: () => ({ target: [-340, 1.25, -1.4], cInf: 10 }) });

  return {
    duration: END,
    shots: S,
    flashes: [t.charged, t.stole + 0.4],
    hud: [
      { from: 0.15, to: t.prize - 0.05, text: '1325', y: 0.13, size: 170 },
      { from: t.wooden + 0.1, to: t.neigh - 0.05, text: 'A WOODEN BUCKET', y: 0.15, size: 84, bg: '#ffe066', anim: 'slide' },
      { from: t.neigh + 0.1, to: t.forty - 0.05, text: 'MODENA  vs  BOLOGNA', y: 0.14, size: 72, bg: '#ffffff' },
      { from: t.forty, to: t.hated - 0.05, count: [0, 40], suffix: ' KM', y: 0.14, size: 130 },
      { from: t.pope + 0.1, to: t.emperor - 0.05, text: 'TEAM POPE', y: 0.14, size: 100, bg: '#ffffff', color: '#b8302a' },
      { from: t.emperor + 0.1, to: t.nov - 0.05, text: 'TEAM EMPEROR', y: 0.14, size: 96, bg: '#ffe066', color: '#1f3f7a' },
      { from: t.thirty, to: t.seven - 0.05, count: [0, 30000], suffix: ' SOLDIERS', y: 0.14, size: 90, color: '#ffffff', bg: '#b8302a' },
      { from: t.seven + 0.4, to: t.easy - 0.05, count: [0, 7000], y: 0.14, size: 140, color: '#ffffff', bg: '#2f5fa8' },
      { from: t.easy + 0.1, to: t.wasnt - 0.05, text: 'EASY WIN?', y: 0.14, size: 110 },
      { from: t.castle + 0.3, to: t.charged - 0.05, text: 'ZAPPOLINO', y: 0.14, size: 110, bg: '#ffe066', anim: 'slide' },
      { from: t.hours + 0.1, to: t.broke - 0.05, text: '2 HOURS', y: 0.14, size: 140, anim: 'shake' },
      { from: t.gold + 0.2, to: t.prisoners - 0.05, text: 'GOLD?', y: 0.14, size: 120, color: '#ffd23a' },
      { from: t.prisoners + 0.1, to: t.city - 0.05, text: 'PRISONERS?', y: 0.14, size: 100 },
      { from: t.city + 0.1, to: t.instead - 0.05, text: 'THE CITY?', y: 0.14, size: 110 },
      { from: t.stole + 0.45, to: t.races - 0.05, text: 'STOLEN!', y: 0.14, size: 150, anim: 'shake', bg: '#ffe066' },
      { from: t.horse, to: t.rub - 0.05, text: 'HORSE RACES', y: 0.14, size: 100, bg: '#ffffff' },
      { from: t.died + 0.3, to: t.nothing - 0.05, text: 'ABOUT 2,000', sub: 'men died', y: 0.14, size: 110 },
      { from: t.trophy + 0.3, to: t.poet - 0.05, text: 'TROPHY', y: 0.14, size: 130, bg: '#ffe066' },
      { from: t.poet + 0.2, to: t.called - 0.05, text: '1622', y: 0.14, size: 150 },
      { from: t.called, to: t.never - 0.05, text: 'LA SECCHIA RAPITA', sub: '"The Stolen Bucket"', y: 0.14, size: 76, bg: '#ffffff' },
      { from: t.today + 0.2, to: t.seven7 - 0.05, text: 'MODENA, TODAY', y: 0.14, size: 90, bg: '#ffe066' },
      { from: t.seven7 + 0.1, to: END, text: '700 YEARS', y: 0.14, size: 130 },
    ],
    audio: {
      music: [{ at: 0, mood: 'epic' }, { at: t.prize, mood: 'quirky' }, { at: t.nov, mood: 'tension' }, { at: t.easy, mood: 'quirky' }, { at: t.wasnt, mood: 'stop' },
        { at: t.castle, mood: 'epic' }, { at: t.home, mood: 'upbeat' }, { at: t.gold, mood: 'sneaky' }, { at: t.stole + 0.4, mood: 'quirky' },
        { at: t.died, mood: 'sad', gain: 0.8 }, { at: t.trophy, mood: 'upbeat' }, { at: t.poet, mood: 'mystery' }, { at: t.never, mood: 'quirky', gain: 0.8 }, { at: t.seven7, mood: 'epic', gain: 0.8 }],
      sfx: [
        [0.2, 'boom'], [t.prize + 0.3, 'pop'], [t.wooden + 0.1, 'magic'], [t.forty, 'tick', { d: 1.2 }], [t.hated + 0.4, 'punch'], [t.hated + 0.7, 'punch'],
        [t.pope + 0.1, 'pop'], [t.emperor + 0.1, 'pop'], [t.nov + 0.2, 'footsteps', { d: 2.4, gain: 0.8 }], [t.thirty, 'drumroll', { d: 1.2 }],
        [t.seven + 0.6, 'gulp'], [t.easy + 0.2, 'ding'], [t.wasnt + 0.15, 'scratch'], [t.charged, 'crowd', { d: 1.4 }],
        [t.hours + 0.2, 'gasp'], [t.broke + 0.8, 'whoosh'], [t.home, 'footsteps', { d: 2, gain: 0.8 }], [t.chased + 2.6, 'thud'],
        [t.gold + 0.2, 'coin'], [t.prisoners + 0.1, 'boing'], [t.city + 0.1, 'riser', { d: 1.2 }], [t.instead, 'footsteps', { d: 1.5, gain: 0.6 }], [t.instead + 1.7, 'ding'],
        [t.stole + 0.45, 'cheer'], [t.horse, 'footsteps', { d: 2.5, gain: 0.9 }], [t.rub + 0.2, 'laugh'], [t.died + 0.2, 'wind', { d: 2.2, gain: 0.7 }],
        [t.nothing + 0.5, 'sadTrombone'], [t.trophy + 0.2, 'applause', { d: 2.4 }], [t.poet + 1.2, 'ding'], [t.called, 'paper'],
        [t.never + 0.3, 'wrong'], [t.today + 0.1, 'chime'], [t.seven7 + 0.1, 'magic'], [t.famous + 0.6, 'rimshot'],
      ],
    },
    captions: { highlightWords: ['bucket', 'war', 'Modena', 'Bologna', 'Pope', 'Emperor', "wasn't", 'charged', 'ran', 'stole', 'races', 'nothing', 'trophy', 'never', 'famous'] },
  };
}
