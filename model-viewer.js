import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { FBXLoader } from "three/addons/loaders/FBXLoader.js";

const viewer = document.querySelector("[data-fbx-viewer]");

if (viewer) {
  const canvasHost = viewer.querySelector("[data-viewer-canvas]");
  const loadingMessage = viewer.querySelector(".viewer-loading");
  const status = viewer.querySelector("[data-viewer-status]");
  const progress = viewer.querySelector("[data-viewer-progress]");
  const resetButton = viewer.querySelector("[data-viewer-reset]");
  const wireframeButton = viewer.querySelector("[data-viewer-wireframe]");
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const showError = () => {
    viewer.classList.add("has-error");
    if (loadingMessage) {
      loadingMessage.classList.add("is-error");
      loadingMessage.textContent = "Modelul 3D nu s-a putut încărca. Reîncarcă pagina sau descarcă fișierul FBX.";
    }
    if (progress) progress.textContent = "Previzualizarea nu este disponibilă";
  };

  try {
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75));
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.15;
    canvasHost.append(renderer.domElement);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(34, 1, 0.01, 1000);
    scene.add(new THREE.HemisphereLight(0xf7eaff, 0x34232d, 2.1));

    const keyLight = new THREE.DirectionalLight(0xfff4f0, 3.0);
    keyLight.position.set(4, 7, 5);
    scene.add(keyLight);
    const fillLight = new THREE.DirectionalLight(0xc2d8ff, 1.35);
    fillLight.position.set(-5, 3, -4);
    scene.add(fillLight);
    const redRim = new THREE.PointLight(0xee3e59, 2.2, 12);
    redRim.position.set(-2, 2, 3);
    scene.add(redRim);

    const modelFrame = new THREE.Group();
    scene.add(modelFrame);
    let model = null;
    let wireframeEnabled = false;
    let initialFrameRotation = new THREE.Euler(0, 0, 0);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.065;
    controls.enablePan = false;
    controls.minPolarAngle = 0.24;
    controls.maxPolarAngle = Math.PI - 0.24;
    controls.autoRotate = !prefersReducedMotion;
    controls.autoRotateSpeed = 0.55;
    controls.addEventListener("start", () => { controls.autoRotate = false; });

    const grid = new THREE.GridHelper(8, 32, 0x77404a, 0x47343d);
    grid.material.transparent = true;
    grid.material.opacity = 0.32;
    scene.add(grid);

    const resizeViewer = () => {
      const width = Math.max(1, canvasHost.clientWidth);
      const height = Math.max(1, canvasHost.clientHeight);
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height, false);
    };

    const resizeObserver = new ResizeObserver(resizeViewer);
    resizeObserver.observe(canvasHost);
    window.addEventListener("resize", resizeViewer, { passive: true });
    resizeViewer();

    const loader = new FBXLoader();
    loader.load(
      viewer.dataset.modelSrc,
      (loadedModel) => {
        model = loadedModel;
        model.traverse((child) => {
          if (!child.isMesh) return;
          child.castShadow = true;
          child.receiveShadow = true;
          const materials = Array.isArray(child.material) ? child.material : [child.material];
          materials.forEach((material) => {
            if (!material) return;
            material.userData.originalWireframe = Boolean(material.wireframe);
            if ("roughness" in material && material.roughness > 0.95) material.roughness = 0.72;
            if ("metalness" in material && material.metalness > 0.9) material.metalness = 0.48;
            material.needsUpdate = true;
          });
        });

        const bounds = new THREE.Box3().setFromObject(model);
        const size = bounds.getSize(new THREE.Vector3());
        const center = bounds.getCenter(new THREE.Vector3());
        const longestSide = Math.max(size.x, size.y, size.z);
        if (!Number.isFinite(longestSide) || longestSide <= 0) throw new Error("Empty model");

        const scale = 3.7 / longestSide;
        modelFrame.position.copy(center).multiplyScalar(-scale);
        modelFrame.scale.setScalar(scale);
        modelFrame.add(model);
        initialFrameRotation = modelFrame.rotation.clone();
        grid.position.y = -(size.y * scale) / 2 - 0.045;

        const distanceForHeight = (size.y * scale) / (2 * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2))) * 1.22;
        const distanceForWidth = (size.x * scale) / (2 * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)) * Math.max(camera.aspect, 0.8)) * 1.12;
        const distance = Math.max(distanceForHeight, distanceForWidth, 4.1);
        camera.position.set(distance * 0.73, distance * 0.43, distance * 0.82);
        controls.target.set(0, 0, 0);
        controls.update();
        controls.saveState();

        if (loadingMessage) loadingMessage.hidden = true;
        if (progress) progress.textContent = "Model pregătit · rotește pentru explorare";
        viewer.classList.add("is-loaded");
      },
      (event) => {
        if (progress && event.total) progress.textContent = `Se încarcă · ${Math.round((event.loaded / event.total) * 100)}%`;
      },
      showError,
    );

    wireframeButton?.addEventListener("click", () => {
      if (!model) return;
      wireframeEnabled = !wireframeEnabled;
      wireframeButton.setAttribute("aria-pressed", String(wireframeEnabled));
      model.traverse((child) => {
        if (!child.isMesh) return;
        const materials = Array.isArray(child.material) ? child.material : [child.material];
        materials.forEach((material) => {
          if (material && "wireframe" in material) {
            material.wireframe = wireframeEnabled || material.userData.originalWireframe;
            material.needsUpdate = true;
          }
        });
      });
    });

    resetButton?.addEventListener("click", () => {
      modelFrame.rotation.copy(initialFrameRotation);
      controls.reset();
      controls.autoRotate = !prefersReducedMotion;
    });

    const render = () => {
      controls.update();
      renderer.render(scene, camera);
      window.requestAnimationFrame(render);
    };
    render();
  } catch (error) {
    console.error("CR Print 3D viewer setup failed:", error);
    showError();
  }
}
