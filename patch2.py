import sys

with open("base.html", "r") as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if "// ---------- LUNAR BASE INTERIOR & PEDESTALS ----------" in line:
        start_idx = i
    if start_idx != -1 and i > start_idx:
        if line.strip() == "})();":
            end_idx = i
            break

if start_idx != -1 and end_idx != -1:
    new_code = """  // ---------- LUNAR BASE INTERIOR & PEDESTALS ----------
  // 隱藏原生 HTML 排版，只保留資料作為 3D 全息圖源
  document.querySelectorAll('.scene .bento-grid').forEach(el => {
    el.style.opacity = '0';
    el.style.pointerEvents = 'none';
  });

  // 建立月球基地內部空間 (Base Group)
  const baseGroup = new THREE.Group();
  baseGroup.position.set(0, 80, 80); 
  scene.add(baseGroup);

  const floorMat = new THREE.MeshStandardMaterial({ 
    color: 0x18181c, roughness: 0.3, metalness: 0.7, side: THREE.DoubleSide 
  });
  const wallMat = new THREE.MeshStandardMaterial({ 
    color: 0x111115, roughness: 0.5, metalness: 0.6, side: THREE.DoubleSide 
  });

  const floor = new THREE.Mesh(new THREE.PlaneGeometry(160, 260), floorMat);
  floor.rotation.x = -Math.PI / 2; floor.position.y = 0;
  const ceil = new THREE.Mesh(new THREE.PlaneGeometry(160, 260), wallMat);
  ceil.rotation.x = Math.PI / 2; ceil.position.y = 60;
  const leftWall = new THREE.Mesh(new THREE.PlaneGeometry(260, 60), wallMat);
  leftWall.rotation.y = Math.PI / 2; leftWall.position.set(-80, 30, 0);
  const rightWall = new THREE.Mesh(new THREE.PlaneGeometry(260, 60), wallMat);
  rightWall.rotation.y = -Math.PI / 2; rightWall.position.set(80, 30, 0);
  const backWall = new THREE.Mesh(new THREE.PlaneGeometry(160, 60), wallMat);
  backWall.position.set(0, 30, -130);

  const frontLeft = new THREE.Mesh(new THREE.PlaneGeometry(40, 60), wallMat);
  frontLeft.position.set(-60, 30, 130); 
  const frontRight = new THREE.Mesh(new THREE.PlaneGeometry(40, 60), wallMat);
  frontRight.position.set(60, 30, 130); 
  const frontTop = new THREE.Mesh(new THREE.PlaneGeometry(80, 20), wallMat);
  frontTop.position.set(0, 50, 130);    

  baseGroup.add(floor, ceil, leftWall, rightWall, backWall, frontLeft, frontRight, frontTop);

  const baseLight1 = new THREE.PointLight(0xfffbe6, 0.6, 200);
  baseLight1.position.set(0, 50, 40);
  baseGroup.add(baseLight1);
  const baseLight2 = new THREE.PointLight(0xc084fc, 0.4, 200);
  baseLight2.position.set(0, 50, -60);
  baseGroup.add(baseLight2);

  // ---------- 全息投影資料萃取與旋轉門 ----------
  const texLoader = new THREE.TextureLoader();
  const interactableMeshes = [];
  const carousels = [];

  function buildHoloCarousel(groupId, pedestalGroup) {
    const cards = document.querySelectorAll(`#${groupId} .work-card`);
    if(cards.length === 0) return;
    
    // 建立旋轉中心與迴圈
    const carouselGroup = new THREE.Group();
    carouselGroup.position.y = 22; // 懸浮在展示台上
    pedestalGroup.add(carouselGroup);
    carousels.push(carouselGroup);

    const radius = Math.max(12, cards.length * 2.8);
    
    cards.forEach((card, i) => {
      const theta = (i / cards.length) * Math.PI * 2;
      const x = Math.sin(theta) * radius;
      const z = Math.cos(theta) * radius;

      let texture;
      const videoSrc = card.dataset.video;
      const imageSrc = card.dataset.image;

      if(videoSrc) {
        const vid = document.createElement('video');
        vid.src = videoSrc; vid.crossOrigin = "anonymous"; vid.loop = true; vid.muted = true; vid.playsInline = true;
        vid.play().catch(()=>{});
        texture = new THREE.VideoTexture(vid);
        texture.colorSpace = THREE.SRGBColorSpace;
      } else if(imageSrc) {
        texture = texLoader.load(imageSrc);
        texture.colorSpace = THREE.SRGBColorSpace;
      }

      const planeGeo = new THREE.PlaneGeometry(16, 9);
      const planeMat = new THREE.MeshBasicMaterial({
        map: texture, transparent: true, opacity: 0.6,
        blending: THREE.AdditiveBlending, side: THREE.DoubleSide
      });
      const plane = new THREE.Mesh(planeGeo, planeMat);
      
      plane.position.set(x, 0, z);
      // 卡牌向外延展角度 - 面向中心
      plane.rotation.y = theta;
      
      plane.userData = { videoSrc, imageSrc, originalScale: new THREE.Vector3(1,1,1) };
      carouselGroup.add(plane);
      interactableMeshes.push(plane);
    });
  }

  // ---------- 展示台 ----------
  const pedData = [
    { id: 'scene-1', pos: [40, 0, 80],  color: 0xc084fc }, // P1 
    { id: 'scene-2', pos: [-40, 0, 20], color: 0xec4899 }, // P2
    { id: 'scene-3', pos: [40, 0, -40], color: 0x22d3ee }, // P3
    { id: 'scene-4', pos: [-40, 0, -100],color: 0xfbbf24 } // P4
  ];
  
  const pedestals = [];
  pedData.forEach((p, i) => {
    const group = new THREE.Group();
    group.position.set(p.pos[0], p.pos[1], p.pos[2]); 
    group.scale.set(0.65, 0.65, 0.65); // 稍微縮小為主

    buildHoloCarousel(p.id, group);

    const baseGeo = new THREE.CylinderGeometry(6, 7.5, 10, 32);
    const baseMat = new THREE.MeshStandardMaterial({
      color: 0x1a1628, metalness: 0.3, roughness: 0.6,
      emissive: new THREE.Color(p.color), emissiveIntensity: 0.15
    });
    const base = new THREE.Mesh(baseGeo, baseMat);
    base.position.y = 5;
    group.add(base);

    const discGeo = new THREE.CylinderGeometry(7, 7, 0.8, 48);
    const discMat = new THREE.MeshStandardMaterial({
      color: new THREE.Color(p.color), emissive: new THREE.Color(p.color),
      emissiveIntensity: 0.8, metalness: 0.5, roughness: 0.3
    });
    const disc = new THREE.Mesh(discGeo, discMat);
    disc.position.y = 10.5;
    group.add(disc);

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

    const ringGeo = new THREE.RingGeometry(10, 12, 64);
    const ringMat = new THREE.MeshBasicMaterial({
      color: new THREE.Color(p.color), transparent: true, opacity: 0.4,
      blending: THREE.AdditiveBlending, side: THREE.DoubleSide, depthWrite: false
    });
    const ring = new THREE.Mesh(ringGeo, ringMat);
    ring.rotation.x = -Math.PI * 0.5;
    ring.position.y = 18;
    group.add(ring);

    const pl = new THREE.PointLight(p.color, 1.2, 50);
    pl.position.y = 14;
    group.add(pl);

    baseGroup.add(group);
    pedestals.push({ group, disc, beam, ring, light: pl });
  });

  scene.add(new THREE.AmbientLight(0x2a2a3a, 0.15));
  const keyLight = new THREE.DirectionalLight(0xfffbe6, 0.5);
  keyLight.position.set(180, 120, 200); 
  scene.add(keyLight);
  const fillLight = new THREE.DirectionalLight(0xc084fc, 0.2);
  fillLight.position.set(-200, 80, -120);
  scene.add(fillLight);

  // ---------- CAMERA KEYFRAMES ============
  const keyframes = [
    // 0%: 深空 Intro 遙望月球
    { t: 0.00, pos: [0, 20, 1500],  look: [0, 0, 0] },
    
    // 10%: 外圍軌道 (開始看到月球曲面)
    { t: 0.10, pos: [-400, 150, 500], look: [0, 40, 0] },
    
    // 20%: 低空掠過表面 (從側邊飛向基地，帶入建築物全景感)
    { t: 0.20, pos: [-150, 110, 280], look: [0, 100, 150] },
    
    // 25%: 到達基地入口正前方
    { t: 0.25, pos: [0, 95, 260],   look: [0, 95, 80] }, 

    // 30%: 進入室內 (P1 Personal)
    { t: 0.30, pos: [-10, 95, 180], look: [40, 88, 160] },
    { t: 0.35, pos: [-15, 95, 160], look: [40, 88, 160] },
    
    // 50%: P2 Apps
    { t: 0.45, pos: [10, 95, 125],  look: [-40, 88, 100] },
    { t: 0.55, pos: [15, 95, 105],  look: [-40, 88, 100] },
    
    // 70%: P3 Videos
    { t: 0.65, pos: [-10, 95, 75],  look: [40, 88, 40] },
    { t: 0.75, pos: [-15, 95, 55],  look: [40, 88, 40] },
    
    // 90%: P4 Design
    { t: 0.85, pos: [10, 95, 20],   look: [-40, 88, -20] },
    { t: 0.95, pos: [15, 95, 0],    look: [-40, 88, -20] },
    
    // 100%: 總覽結束
    { t: 1.00, pos: [0, 125, -45],  look: [0, 80, 120] },
  ];

  function sampleKeyframes(t){
    if(t <= keyframes[0].t){ return { pos: keyframes[0].pos.slice(), look: keyframes[0].look.slice() }; }
    if(t >= keyframes[keyframes.length-1].t){ return { pos: keyframes[keyframes.length-1].pos.slice(), look: keyframes[keyframes.length-1].look.slice() }; }
    for(let i = 0; i < keyframes.length - 1; i++){
      const a = keyframes[i], b = keyframes[i+1];
      if(t >= a.t && t <= b.t){
        const u = (t - a.t) / (b.t - a.t);
        const e = u < 0.5 ? 2*u*u : 1 - Math.pow(-2*u + 2, 2) / 2;
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

  // ---------- MOUSE & RAYCASTER INTERACTION ----------
  const raycaster = new THREE.Raycaster();
  const mouse = new THREE.Vector2(-9999, -9999);
  let mx = 0, my = 0, tmx = 0, tmy = 0;

  window.addEventListener('pointermove', (e) => {
    mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
    tmx = (e.clientX / window.innerWidth - 0.5) * 2;
    tmy = (e.clientY / window.innerHeight - 0.5) * 2;
  }, {passive: true});

  window.addEventListener('click', () => {
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(interactableMeshes, false);
    if(intersects.length > 0) {
      const data = intersects[0].object.userData;
      if(data.videoSrc) {
        modalVideo.src = data.videoSrc;
        videoModal.classList.add('open');
        modalVideo.play().catch(()=>{});
      } else if(data.imageSrc) {
        modalImage.src = data.imageSrc;
        imageModal.classList.add('open');
      }
    }
  });

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

    // 星空與打光
    farStars.material.uniforms.uTime.value = t * 0.55;
    midStars.material.uniforms.uTime.value = t;
    farStars.rotation.y = t * 0.004;
    midStars.rotation.y = -t * 0.002;

    pedestals.forEach((p, i) => {
      const phase = t + i * 1.5;
      p.disc.material.emissiveIntensity = 0.9 + 0.4 * Math.sin(phase * 1.3);
      p.ring.rotation.z = phase * 0.3;
      p.ring.material.opacity = 0.3 + 0.15 * Math.sin(phase * 1.1);
      p.beam.material.uniforms.uTime.value = t;
      p.light.intensity = 1.0 + 0.5 * Math.sin(phase * 1.5);
    });

    // 旋轉門卡牌互動邏輯
    carousels.forEach(c => c.rotation.y -= dt * 0.2); // 持續緩慢自轉

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(interactableMeshes, false);
    const hoveredMesh = intersects.length > 0 ? intersects[0].object : null;

    interactableMeshes.forEach(mesh => {
      if(mesh === hoveredMesh) {
        mesh.scale.lerp(new THREE.Vector3(1.25, 1.25, 1.25), 0.15); // 放大
        mesh.material.opacity += (1.0 - mesh.material.opacity) * 0.15; // 變亮
      } else {
        mesh.scale.lerp(mesh.userData.originalScale, 0.1); // 歸位
        mesh.material.opacity += (0.6 - mesh.material.opacity) * 0.1; // 變暗半透明
      }
    });

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

