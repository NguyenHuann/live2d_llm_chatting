const MODEL_JSON = '/static/live2d/14emu_sports02_t01/14emu_sports02_t01.model3.json';

const canvas = document.getElementById('live2dCanvas');

function waitForLive2D(cb, tries = 50) {
  const ok = (window.PIXI && PIXI.live2d && PIXI.live2d.Live2DModel);
  if (ok) return cb();
  if (tries <= 0) {
    console.error('[Live2D] pixi-live2d-display chưa tải? Kiểm tra thẻ <script> và mạng.');
    return;
  }
  setTimeout(() => waitForLive2D(cb, tries - 1), 100);
}

waitForLive2D(async () => {
  console.log('[Live2D] Libraries ready:', !!PIXI, !!PIXI.live2d);
  const Live2DModel = PIXI.live2d.Live2DModel;

  // Pixi app
  const app = new PIXI.Application({
    view: canvas,
    resizeTo: canvas.parentElement,
    antialias: true,
    backgroundAlpha: 0,
  });

  let model, analyser, audioCtx, sourceNode, mouthOpen = 0;

  const setMouthOpen = (v) => {
    if (!model) return;
    const ids = ['ParamMouthOpenY', 'ParamMouthForm', 'MouthOpen', 'ParamMouthSmile'];
    const core = model.internalModel.coreModel;
    ids.forEach(id => { try { core.setParameterValueById(id, v); } catch {} });
  };

  function fitModel(m) {
    const w = app.renderer.width, h = app.renderer.height;
    const scale = Math.min(w / (m.width || 1), h / (m.height || 1)) * 0.9;
    m.scale.set(scale);
    m.anchor.set(0.5, 1.0);          // anchor dưới cùng
    m.position.set(w * 0.5, h);      // đặt đúng sát đáy canvas
  }

  // 1) LOAD MODEL trước
  try {
    console.log('[Live2D] loading model:', MODEL_JSON);
    model = await Live2DModel.from(MODEL_JSON);
    console.log('[Live2D] model loaded');

    app.stage.addChild(model);
    fitModel(model);

    // render loop: áp miệng theo mouthOpen
    app.ticker.add(() => setMouthOpen(mouthOpen));

    // responsive
    window.addEventListener('resize', () => fitModel(model), { passive: true });
  } catch (e) {
    console.error('[Live2D] load error:', e);
    return;
  }

  // 2) ÁP DỤNG motion & expression SAU KHI LOAD
  try {
    await model.motion('w-happy-angry01'); // tên trong motions/
    console.log('[Live2D] motion mặc định: w-happy-angry01');
  } catch (e) {
    console.warn('[Live2D] không tìm thấy motion w-happy-angry01');
  }

  try {
    model.expression('face_smile_11');     // tên trong Expressions của .model3.json
    console.log('[Live2D] expression mặc định: face_smile_11');
  } catch (e) {
    console.warn('[Live2D] không tìm thấy expression face_smile_11');
  }

  // 3) LIP-SYNC từ <audio id="voice">
  const voice = document.getElementById('voice');
  if (voice) {
    const ensureCtx = () => {
      if (!audioCtx || audioCtx.state === 'closed') {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        sourceNode = audioCtx.createMediaElementSource(voice);
        analyser = audioCtx.createAnalyser();
        analyser.fftSize = 1024;
        analyser.smoothingTimeConstant = 0.6;
        sourceNode.connect(analyser);
        analyser.connect(audioCtx.destination);
        animateMouth();
        console.log('[Live2D] AudioContext ready');
      }
    };

    voice.addEventListener('play', async () => {
      ensureCtx();
      if (audioCtx && audioCtx.state === 'suspended') {
        try { await audioCtx.resume(); } catch {}
      }
    });

    const relax = () => { mouthOpen = Math.max(0, mouthOpen - 0.05); };
    voice.addEventListener('pause',  relax);
    voice.addEventListener('ended',  relax);

    function animateMouth() {
      if (!analyser) return;
      const data = new Uint8Array(analyser.fftSize);
      const tick = () => {
        if (analyser) {
          analyser.getByteTimeDomainData(data);
          let sum = 0;
          for (let i = 0; i < data.length; i++) {
            const v = (data[i] - 128) / 128; // -1..1
            sum += v * v;
          }
          const rms = Math.sqrt(sum / data.length);       // ~0..0.5
          const target = Math.min(1, Math.max(0, (rms - 0.02) * 6));
          const smooth = 0.35;
          mouthOpen = mouthOpen * (1 - smooth) + target * smooth;
        }
        requestAnimationFrame(tick);
      };
      tick();
    }
  }
});
