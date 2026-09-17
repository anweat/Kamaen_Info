import { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import {
  RotateCcw,
  Layers3,
  Move3D,
  ArrowUpRight,
  Play,
  Pause,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import { scenes, type Voxel, type SceneSpec } from "../scenes";
import { href } from "../data";
export default function SceneViewer({
  sceneId = "impact",
  compact = false,
  scene,
}: {
  sceneId?: string;
  compact?: boolean;
  scene?: SceneSpec;
}) {
  const spec = scene || scenes.find((s) => s.id === sceneId) || scenes[0];
  const lastStep = spec.steps.length - 1;
  const maxLayer = Math.max(
    1,
    ...spec.voxels.map((v) => Math.ceil(v.position[1] + 0.5)),
  );
  const host = useRef<HTMLDivElement>(null);
  const [step, setStep] = useState(lastStep);
  const [explode, setExplode] = useState(false);
  const [layer, setLayer] = useState(maxLayer);
  const [selected, setSelected] = useState<Voxel | null>(null);
  const [reset, setReset] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [error, setError] = useState(false);
  useEffect(() => {
    if (!playing) return;
    const timer = setInterval(
      () =>
        setStep((s) => {
          if (s >= lastStep) {
            setPlaying(false);
            return s;
          }
          return s + 1;
        }),
      2400,
    );
    return () => clearInterval(timer);
  }, [playing, lastStep]);
  useEffect(() => {
    if (!host.current) return;
    const el = host.current;
    setError(false);
    let renderer: THREE.WebGLRenderer;
    try {
      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    } catch {
      setError(true);
      return;
    }
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    el.appendChild(renderer.domElement);
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(33, 1, 0.1, 100);
    camera.position.set(6, 5, 7);
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.target.set(0, 0.65, 0);
    controls.enableDamping = true;
    controls.minDistance = 4;
    controls.maxDistance = 15;
    controls.maxPolarAngle = Math.PI * 0.49;
    controls.enablePan = false;
    scene.add(new THREE.HemisphereLight("#b7ddeb", "#19232c", 2.6));
    const light = new THREE.DirectionalLight("#d8e5df", 3.6);
    light.position.set(3, 7, 4);
    scene.add(light);
    const grid = new THREE.GridHelper(12, 24, "#3b5b65", "#1d313e");
    grid.position.y = -0.55;
    scene.add(grid);
    // An original 16px voxel surface: neutral placeholder, not a Minecraft asset.
    const pixels = new Uint8Array(16 * 16 * 4);
    for (let i = 0; i < 256; i++) {
      const shade = 205 + ((i * 31 + Math.floor(i / 16) * 17) % 45);
      pixels.set([shade, shade, shade, 255], i * 4);
    }
    const surface = new THREE.DataTexture(pixels, 16, 16);
    surface.magFilter = THREE.NearestFilter;
    surface.minFilter = THREE.NearestFilter;
    surface.needsUpdate = true;
    surface.colorSpace = THREE.SRGBColorSpace;
    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const meshes: THREE.Mesh[] = [];
    const materials: THREE.Material[] = [];
    spec.voxels.forEach((voxel, index) => {
      if (voxel.step > step || voxel.position[1] > layer - 0.5) return;
      const mat = new THREE.MeshStandardMaterial({
        color: voxel.color,
        map: surface,
        roughness: 0.6,
        metalness: 0.18,
      });
      materials.push(mat);
      const mesh = new THREE.Mesh(geometry, mat);
      mesh.position.set(...voxel.position);
      if (explode) mesh.position.y += voxel.step * 0.55;
      mesh.scale.set(...(voxel.size || [0.94, 0.94, 0.94]));
      mesh.userData.index = index;
      scene.add(mesh);
      meshes.push(mesh);
      const edgeGeo = new THREE.EdgesGeometry(geometry);
      const edgeMat = new THREE.LineBasicMaterial({
        color: "#8da7b2",
        transparent: true,
        opacity: 0.23,
      });
      const edge = new THREE.LineSegments(edgeGeo, edgeMat);
      mesh.add(edge);
    });
    const resize = () => {
      const w = el.clientWidth,
        h = el.clientHeight;
      renderer.setSize(w, h);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
    };
    const ro = new ResizeObserver(resize);
    ro.observe(el);
    resize();
    let frame = 0;
    const render = () => {
      controls.update();
      renderer.render(scene, camera);
      frame = requestAnimationFrame(render);
    };
    render();
    const ray = new THREE.Raycaster();
    let down = [0, 0];
    const pointerDown = (e: PointerEvent) => {
      down = [e.clientX, e.clientY];
    };
    const pick = (e: PointerEvent) => {
      if (Math.hypot(e.clientX - down[0], e.clientY - down[1]) > 5) return;
      const box = el.getBoundingClientRect();
      ray.setFromCamera(
        new THREE.Vector2(
          ((e.clientX - box.left) / box.width) * 2 - 1,
          (-(e.clientY - box.top) / box.height) * 2 + 1,
        ),
        camera,
      );
      const hit = ray.intersectObjects(meshes, false)[0];
      if (hit) {
        meshes.forEach((mesh) => {
          const material = mesh.material as THREE.MeshStandardMaterial;
          material.emissive.set(mesh === hit.object ? "#265349" : "#000000");
        });
        setSelected(spec.voxels[hit.object.userData.index]);
      }
    };
    el.addEventListener("pointerdown", pointerDown);
    el.addEventListener("pointerup", pick);
    return () => {
      cancelAnimationFrame(frame);
      ro.disconnect();
      controls.dispose();
      el.removeEventListener("pointerdown", pointerDown);
      el.removeEventListener("pointerup", pick);
      geometry.dispose();
      surface.dispose();
      materials.forEach((m) => m.dispose());
      meshes.forEach((m) =>
        m.children.forEach((c) => {
          const edge = c as THREE.LineSegments;
          edge.geometry.dispose();
          (edge.material as THREE.Material).dispose();
        }),
      );
      grid.geometry.dispose();
      (grid.material as THREE.Material).dispose();
      renderer.dispose();
      renderer.domElement.remove();
    };
  }, [spec, step, explode, layer, reset]);
  return (
    <section
      className={`scene-viewer ${compact ? "compact" : ""}`}
      aria-label={spec.title}
    >
      <div className="scene-heading">
        <span>
          <span className="live-dot" /> 可交互结构示意
        </span>
        <span>
          {scene ? "文件场景" : sceneId === "rack" ? "R04 / 02" : "E1 / 01"}
        </span>
      </div>
      <div
        className="scene-canvas"
        ref={host}
        aria-label="三维结构：鼠标拖动旋转，滚轮缩放。下方部件列表提供键盘访问。"
      />
      {error && (
        <p className="scene-fallback">
          此浏览器暂不可用 WebGL，可通过步骤和部件列表阅读完整说明。
        </p>
      )}
      <div className="scene-caption">
        <Move3D size={14} /> 拖动旋转 · 滚轮缩放 · 点击部件
      </div>
      <div className="scene-tools">
        <button
          title="重置视角"
          aria-label="重置视角"
          onClick={() => setReset((r) => r + 1)}
        >
          <RotateCcw size={16} />
        </button>
        <button aria-pressed={explode} onClick={() => setExplode((e) => !e)}>
          <Layers3 size={16} /> {explode ? "合拢" : "拆解"}
        </button>
        <label>
          剖层{" "}
          <input
            aria-label="结构剖层"
            type="range"
            min="1"
            max={maxLayer}
            value={layer}
            onChange={(e) => setLayer(Number(e.target.value))}
          />
        </label>
        <span>
          {layer}/{maxLayer}
        </span>
      </div>
      {!compact && (
        <>
          <div className="scene-step">
            <div className="button-row">
              <button
                aria-label="上一步"
                disabled={step === 0}
                onClick={() => {
                  setPlaying(false);
                  setStep((s) => s - 1);
                }}
              >
                <ChevronLeft size={16} />
              </button>
              <button
                onClick={() => {
                  if (!playing) setStep(0);
                  setPlaying((p) => !p);
                }}
              >
                {playing ? <Pause size={15} /> : <Play size={15} />}{" "}
                {playing ? "暂停" : "播放步骤"}
              </button>
              <button
                aria-label="下一步"
                disabled={step >= lastStep}
                onClick={() => {
                  setPlaying(false);
                  setStep((s) => s + 1);
                }}
              >
                <ChevronRight size={16} />
              </button>
              <small>
                {step + 1} / {spec.steps.length}
              </small>
            </div>
            <h3>{spec.steps[step].title}</h3>
            <p>{spec.steps[step].text}</p>
          </div>
          <details className="part-list">
            <summary>部件清单与说明 · 键盘可访问</summary>
            {spec.voxels
              .filter(
                (v, i, a) => a.findIndex((x) => x.label === v.label) === i,
              )
              .map((v) => (
                <button key={v.label} onClick={() => setSelected(v)}>
                  {v.label}
                </button>
              ))}
          </details>
        </>
      )}
      {selected && (
        <div className="part-detail" role="status">
          <button className="close-text" onClick={() => setSelected(null)}>
            关闭
          </button>
          <strong>{selected.label}</strong>
          <p>{selected.detail}</p>
          {selected.ref && (
            <a href={href("items", selected.ref)}>
              查看关联条目 <ArrowUpRight size={13} />
            </a>
          )}
        </div>
      )}
    </section>
  );
}
