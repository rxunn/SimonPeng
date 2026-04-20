import sys

with open("base.html", "r") as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if "// ---------- PEDESTALS (4 on moon surface) ----------" in line:
        start_idx = i
    if start_idx != -1 and i > start_idx:
        # Looking for the end of the IIFE "})();"
        if line.strip() == "})();":
            end_idx = i
            break

if start_idx != -1 and end_idx != -1:
    new_code = """  // ---------- LUNAR BASE INTERIOR & PEDESTALS ----------
  // 建立月球基地內部空間 (Base Group)
  const baseGroup = new THREE.Group();
  baseGroup.position.set(0, 80, 80); // 放置在月球朝向攝影機的表面附近
  scene.add(baseGroup);

  const floorMat = new THREE.MeshStandardMaterial({ 
    color: 0x18181c, roughness: 0.3, metalness: 0.7, side: THREE.DoubleSide 
  });
  const wallMat = new THREE.MeshStandardMaterial({ 
    color: 0x111115, roughness: 0.5, metalness: 0.6, side: THREE.DoubleSide 
  });

  // 基地空間尺寸: 寬160, 高60, 深260
  // 地板
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(160, 260), floorMat);
  floor.rotation.x = -Math.PI / 2;
  floor.position.y = 0;
  // 天花板
  const ceil = new THREE.Mesh(new THREE.PlaneGeometry(160, 260), wallMat);
  ceil.rotation.x = Math.PI / 2;
  ceil.position.y = 60;
  // 左牆
  const leftWall = new THREE.Mesh(new THREE.PlaneGeometry(260, 60), wallMat);
  leftWall.rotation.y = Math.PI / 2;
  leftWall.position.set(-80, 30, 0);
  // 右牆
  const rightWall = new THREE.Mesh(new THREE.PlaneGeometry(260, 60), wallMat);
  rightWall.rotation.y = -Math.PI / 2;
  rightWall.position.set(80, 30, 0);
  // 後牆
  const backWall = new THREE.Mesh(new THREE.PlaneGeometry(160, 60), wallMat);
  backWall.position.set(0, 30, -130);

  // 基地入口框架 (開口朝外)
  const frontLeft = new THREE.Mesh(new THREE.PlaneGeometry(40, 60), wallMat);
  frontLeft.position.set(-60, 30, 130); // 左門柱
  const frontRight = new THREE.Mesh(new THREE.PlaneGeometry(40, 60), wallMat);
  frontRight.position.set(60, 30, 130); // 右門柱
  const frontTop = new THREE.Mesh(new THREE.PlaneGeometry(80, 20), wallMat);
  frontTop.position.set(0, 50, 130);    // 門楣
  
  baseGroup.add(floor, ceil, leftWall, rightWall, backWall, frontLeft, frontRight, frontTop);

  // 基地內部光源 (製造陰影與層次感)
  const baseLight1 = new THREE.PointLight(0xfffbe6, 0.6, 200);
  baseLight1.position.set(0, 50, 40);
  baseGroup.add(baseLight1);
  const baseLight2 = new THREE.PointLight(0xc084fc, 0.4, 200);
  baseLight2.position.set(0, 50, -60);
  baseGroup.add(baseLight2);

  // ---------- 展示台 (4個縮小並放進基地角落) ----------
  const pedData = [
    { pos: [40, 0, 80],  color: 0xc084fc }, // P1 Personal (右前)
    { pos: [-40, 0, 20], color: 0xec4899 }, // P2 Apps (左中)
    { pos: [40, 0, -40], color: 0x22d3ee }, // P3 Videos (右後)
    { pos: [-40, 0, -100],color: 0xfbbf24 } // P4 Design (左深處)
  ];
  
  const pedestals = [];
  pedData.forEach((p, i) => {
    const group = new THREE.Group();
    group.position.set(p.pos[0], p.pos[1], p.pos[2]); // 基於室內 Base Group 的相對座標
    group.scale.set(0.7, 0.7, 0.7); // 縮小以適應室內尺度

    // Base cylinder
    const baseGeo = new THREE.CylinderGeometry(6, 7.5, 10, 32);
    const baseMat = new THREE.MeshStandardMaterial({
      color: 0x1a1628, metalness: 0.3, roughness: 0.6,
      emissive: new THREE.Color(p.color), emissiveIntensity: 0.15
    });
    const base = new THREE.Mesh(baseGeo, baseMat);
    base.position.y = 5;
    group.add(base);

    // Top disc
    const discGeo = new THREE.CylinderGeometry(7, 7, 0.8, 48);
    const discMat = new THREE.MeshStandardMaterial({
      color: new THREE.Color(p.color), emissive: new THREE.Color(p.color),
      emissiveIntensity: 1.0, metalness: 0.5, roughness: 0.3
    });
    const disc = new THREE.Mesh(discGeo, discMat);
    disc.position.y = 10.5;
    group.add(disc);

    // Rising beacon beam
    const beamGeo = new THREE.CylinderGeometry(0.8, 3, 40, 24, 1, true);
    const beamMat = new THREE.ShaderMaterial({
      uniforms: { uTime:{value:0}, uColor:{value:new THREE.Color(p.color)} },
      vertexShader: ` varying float vY; void main(){ vY = position.y; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); } `,
      fragmentShader: ` uniform float uTime; uniform vec3 uColor; varying float vY; void main(){ float t = (vY + 20.0) / 40.0; float a = pow(1.0 - t, 1.8) * (0.4 + 0.2 * sin(uTime * 2.0 + vY * 0.3)); gl_FragColor = vec4(uColor, a * 0.5); } `,
      transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide
    });
    const beam = new THREE.Mesh(beamGeo, beamMat);
    beam.position.y = 30;
    group.add(beam);

    // Floating halo ring
    const ringGeo = new THREE.RingGeometry(10, 12, 64);
    const ringMat = new THREE.MeshBasicMaterial({
      color: new THREE.Color(p.color), transparent: true, opacity: 0.4,
      blending: THREE.AdditiveBlending, side: THREE.DoubleSide, depthWrite: false
    });
    const ring = new THREE.Mesh(ringGeo, ringMat);
    ring.rotation.x = -Math.PI * 0.5;
    ring.position.y = 18;
    group.add(ring);

    // Point light
    const pl = new THREE.PointLight(p.color, 1.2, 50);
    pl.position.y = 14;
    group.add(pl);

    baseGroup.add(group);
    pedestals.push({ group, disc, beam, ring, light: pl });
  });

  // ---------- LIGHTS ----------
  // 大幅降低環境光，讓室內產生對比陰影感
  scene.add(new THREE.AmbientLight(0x2a2a3a, 0.15));
  const keyLight = new THREE.DirectionalLight(0xfffbe6, 0.5);
  keyLight.position.set(180, 120, 200); // 在室外
  scene.add(keyLight);
  const fillLight = new THREE.DirectionalLight(0xc084fc, 0.2);
  fillLight.position.set(-200, 80, -120);
  scene.add(fillLight);

  // ---------- CAMERA KEYFRAMES ============
  // 基地絕對座標為 y=80, z=80，入口絕對座標 z=210
  const keyframes = [
    // 0%: 深空 Intro
    { t: 0.00, pos: [0, 20, 800],   look: [0, 0, 0] },
    { t: 0.05, pos: [0, 50, 500],   look: [0, 30, 0] },
    
    // 10%~20%: 逼近月表與基地入口
    { t: 0.10, pos: [0, 95, 300],   look: [0, 95, 80] },
    { t: 0.15, pos: [0, 95, 230],   look: [0, 95, 80] }, // 到達入口正前方
    { t: 0.20, pos: [0, 95, 200],   look: [0, 95, 80] }, // 攝影機看向建築內部深處
    
    // 30%: 進入室內 (P1 Personal - 絕對座標 x: 40, z: 160)
    { t: 0.25, pos: [-10, 95, 180], look: [40, 88, 160] },
    { t: 0.30, pos: [-15, 95, 160], look: [40, 88, 160] },
    
    // 50%: P2 Apps (絕對座標 x: -40, z: 100)
    { t: 0.40, pos: [10, 95, 125],  look: [-40, 88, 100] },
    { t: 0.50, pos: [15, 95, 105],  look: [-40, 88, 100] },
    
    // 70%: P3 Videos (絕對座標 x: 40, z: 40)
    { t: 0.60, pos: [-10, 95, 65],  look: [40, 88, 40] },
    { t: 0.70, pos: [-15, 95, 45],  look: [40, 88, 40] },
    
    // 90%: P4 Design (絕對座標 x: -40, z: -20)
    { t: 0.80, pos: [10, 95, 5],    look: [-40, 88, -20] },
    { t: 0.90, pos: [15, 95, -15],  look: [-40, 88, -20] },
    
    // 100%: 總覽結束 (Pull-back Ending)
    { t: 0.95, pos: [0, 110, -30],  look: [0, 90, 80] },
    { t: 1.00, pos: [0, 125, -45],  look: [0, 80, 120] },
  ];

  function sampleKeyframes(t){
    if(t <= keyframes[0].t){ return { pos: keyframes[0].pos.slice(), look: keyframes[0].look.slice() }; }
    if(t >= keyframes[keyframes.length-1].t){ return { pos: keyframes[keyframes.length-1].pos.slice(), look: keyframes[keyframes.length-1].look.slice() }; }
    for(let i = 0; i < keyframes.length - 1; i++){
      const a = keyframes[i], b = keyframes[i+1];
      if(t >= a.t && t <= b.t){
        const u = (t - a.t) / (b.t - a.t);
        const e = u < 0.5 ? 2*u*u : 1 - Math.pow(-2*u + 2, 2) / 2; // Smooth Easing
        return {
          pos: [
            a.pos[0] + (b.pos[0] - a.pos[0]) * e,
            a.pos[1] + (b.pos[1] - a.pos[1]) * e,
            a.pos[2] + (b.pos[2] - a.pos[2]) * e,
          ],
          look: [
            a.look[0] + (b.look[0] - a.look[0]) * e,
            a.look[1] + (b.look[1] - a.look[1]) * e,
            a.look[2] + (b.look[2] - a.look[2]) * e,
          ]
        };
      }
    }
    return { pos: keyframes[0].pos.slice(), look: keyframes[0].look.slice() };
  }

  // ---------- MOUSE PARALLAX ----------
  let mx = 0, my = 0, tmx = 0, tmy = 0;
  window.addEventListener('pointermove', (e) => {
    tmx = (e.clientX / window.innerWidth - 0.5) * 2;
    tmy = (e.clientY / window.innerHeight - 0.5) * 2;
  }, {passive: true});

  // ---------- RENDER LOOP ----------
  const clock = new THREE.Clock();
  const camPos = new THREE.Vector3().copy(camera.position);
  const camLook = new THREE.Vector3(0, 0, 0);
  const tmpPos = new THREE.Vector3();
  const tmpLook = new THREE.Vector3();

  let firstFrameDone = false;

  function render(){
    const dt = Math.min(clock.getDelta(), 0.05);
    const t = clock.getElapsedTime();

    const total = document.documentElement.scrollHeight - window.innerHeight;
    const progress = total > 0 ? Math.min(1, Math.max(0, scrollY / total)) : 0;

    const kf = sampleKeyframes(progress);
    tmpPos.set(kf.pos[0], kf.pos[1], kf.pos[2]);
    tmpLook.set(kf.look[0], kf.look[1], kf.look[2]);

    mx += (tmx - mx) * 0.06;
    my += (tmy - my) * 0.06;
    tmpPos.x += mx * 6;
    tmpPos.y -= my * 4;

    camPos.lerp(tmpPos, 0.11);
    camLook.lerp(tmpLook, 0.11);
    camera.position.copy(camPos);
    camera.lookAt(camLook);

    // 注意：這裡移除了原本月球自轉的邏輯 (moon.rotation.y += ...)，確保基地錨定在固定位置不會移動出軌。

    farStars.material.uniforms.uTime.value = t * 0.55;
    midStars.material.uniforms.uTime.value = t;

    pedestals.forEach((p, i) => {
      const phase = t + i * 1.5;
      p.disc.material.emissiveIntensity = 0.9 + 0.4 * Math.sin(phase * 1.3);
      p.ring.rotation.z = phase * 0.3;
      p.ring.material.opacity = 0.3 + 0.15 * Math.sin(phase * 1.1);
      p.beam.material.uniforms.uTime.value = t;
      p.light.intensity = 1.0 + 0.5 * Math.sin(phase * 1.5);
    });

    farStars.rotation.y = t * 0.004;
    midStars.rotation.y = -t * 0.002;

    renderer.render(scene, camera);

    if(!firstFrameDone){
      firstFrameDone = true;
      setTimeout(() => {
        if(loadingScreen){
          loadingScreen.classList.add('hidden');
          setTimeout(() => loadingScreen.remove(), 900);
        }
      }, 600);
    }

    requestAnimationFrame(render);
  }

  if(!prefersReduced){
    requestAnimationFrame(render);
  } else {
    renderer.render(scene, camera);
    if(loadingScreen){ loadingScreen.classList.add('hidden'); setTimeout(() => loadingScreen.remove(), 900); }
  }
})();
"""
    new_lines = lines[:start_idx] + [new_code] + lines[end_idx+1:]
    with open("base.html", "w") as f:
        f.writelines(new_lines)
    print("Replaced successfully")
else:
    print(f"Failed to find indices. start: {start_idx}, end: {end_idx}")

