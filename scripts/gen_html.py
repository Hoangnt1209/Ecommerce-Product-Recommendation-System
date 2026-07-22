"""
Generate the full redesigned index.html for DDM501 Capstone Demo.
Run: python scripts/gen_html.py
"""
import pathlib

OUT = pathlib.Path(__file__).parent.parent / "src" / "templates" / "index.html"

# ============================================================
# PART 1  –  HEAD + CSS
# ============================================================
CSS = """
:root{
  --bg:#04090f;
  --panel:rgba(255,255,255,.038);
  --bdr:rgba(255,255,255,.08);
  --acc:#6366f1;--acc2:#a855f7;
  --cyan:#06b6d4;--grn:#10b981;--amb:#f59e0b;--rose:#f43f5e;
  --txt:#e2e8f0;--sub:#94a3b8;--mut:#475569;
}
*{box-sizing:border-box;margin:0;padding:0;}
body{
  font-family:'Inter',sans-serif;
  background:var(--bg);
  background-image:
    radial-gradient(ellipse 90% 55% at 50% -5%,rgba(99,102,241,.2) 0%,transparent 60%),
    radial-gradient(ellipse 45% 40% at 92% 85%,rgba(168,85,247,.13) 0%,transparent 55%);
  color:var(--txt);min-height:100vh;
}

/* ── glass / panel ── */
.g{background:var(--panel);border:1px solid var(--bdr);border-radius:14px;backdrop-filter:blur(16px);}
.g-dark{background:rgba(4,9,15,.7);border:1px solid var(--bdr);border-radius:12px;}

/* ── typography ── */
.gtxt{background:linear-gradient(130deg,#818cf8,#c084fc 48%,#38bdf8);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.pill-badge{
  display:inline-flex;align-items:center;gap:6px;
  background:linear-gradient(135deg,rgba(99,102,241,.18),rgba(168,85,247,.18));
  border:1px solid rgba(99,102,241,.4);border-radius:999px;
  padding:4px 14px;font-size:.72rem;font-weight:700;color:#a5b4fc;
  letter-spacing:.8px;text-transform:uppercase;
}
.lbl{font-size:.65rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--mut);margin-bottom:8px;}
.chip{display:inline-flex;align-items:center;gap:5px;padding:3px 10px;border-radius:999px;font-size:.7rem;font-weight:600;}

/* ── form ── */
.form-select,.form-control{
  background:rgba(10,16,28,.9)!important;border:1px solid rgba(255,255,255,.1)!important;
  color:var(--txt)!important;border-radius:8px!important;font-size:.83rem!important;
}
.form-select:focus,.form-control:focus{
  border-color:var(--acc)!important;box-shadow:0 0 0 3px rgba(99,102,241,.15)!important;
}
.form-select option{background:#0b1220;}
.form-range::-webkit-slider-thumb{background:var(--acc);}

/* ── buttons ── */
.btn-ai{
  background:linear-gradient(135deg,var(--acc),var(--acc2));
  border:none;color:#fff;font-weight:700;border-radius:9px;
  padding:10px 18px;width:100%;cursor:pointer;font-size:.85rem;
  transition:all .22s;display:block;text-align:center;
}
.btn-ai:hover{transform:translateY(-2px);box-shadow:0 8px 22px rgba(99,102,241,.55);color:#fff;}
.btn-alt{
  background:transparent;border:1px solid var(--cyan);color:var(--cyan);
  font-weight:700;border-radius:9px;padding:10px 18px;width:100%;
  cursor:pointer;font-size:.85rem;transition:all .22s;display:block;text-align:center;
}
.btn-alt:hover{background:rgba(6,182,212,.12);transform:translateY(-2px);color:var(--cyan);}
.btn-sm-ghost{
  font-size:.7rem;padding:4px 10px;border-radius:6px;
  border:1px solid rgba(255,255,255,.12);background:transparent;
  color:var(--sub);transition:all .18s;cursor:pointer;
}
.btn-sm-ghost:hover{border-color:var(--acc);color:#a5b4fc;background:rgba(99,102,241,.1);}

/* ── stat chip ── */
.stat{
  background:rgba(255,255,255,.035);border:1px solid var(--bdr);
  border-radius:12px;padding:14px;text-align:center;
}
.stat .v{font-size:1.4rem;font-weight:800;}

/* ── product card ── */
.pcard{transition:transform .22s,box-shadow .22s;overflow:hidden;}
.pcard:hover{transform:translateY(-5px);box-shadow:0 14px 36px rgba(99,102,241,.28);}
.pthumb{position:relative;height:140px;border-radius:9px;overflow:hidden;
  background:linear-gradient(135deg,#141f33,#080e1c);margin:7px 7px 0;}
.pthumb img{width:100%;height:100%;object-fit:cover;transition:transform .32s;}
.pcard:hover .pthumb img{transform:scale(1.07);}
.pthumb .tag-asin{position:absolute;top:6px;left:6px;
  background:rgba(0,0,0,.62);border:1px solid rgba(255,255,255,.1);
  border-radius:5px;padding:1px 7px;font-size:.6rem;color:#94a3b8;}
.pthumb .tag-score{position:absolute;top:6px;right:6px;
  background:linear-gradient(135deg,#4338ca,#6d28d9);
  border-radius:6px;padding:2px 8px;font-size:.74rem;font-weight:700;color:#fff;}
.ptitle{font-size:.83rem;font-weight:600;color:#f1f5f9;line-height:1.35;
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;
  overflow:hidden;min-height:2.25em;}
.pcat{font-size:.7rem;color:var(--cyan);}
.pprice{font-size:.85rem;font-weight:700;color:var(--grn);}

/* ── history card ── */
.hcard{
  display:flex;align-items:flex-start;gap:10px;
  background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);
  border-radius:9px;padding:10px;transition:border-color .18s;
}
.hcard:hover{border-color:rgba(99,102,241,.35);}
.hicon{
  width:34px;height:34px;min-width:34px;border-radius:8px;
  background:linear-gradient(135deg,rgba(99,102,241,.32),rgba(168,85,247,.32));
  display:flex;align-items:center;justify-content:center;font-size:.8rem;
}
.hstar{color:var(--amb);font-size:.7rem;}

/* ── explain drawer ── */
#explainDrawer{
  position:fixed;right:0;top:0;bottom:0;width:400px;z-index:1060;
  background:rgba(6,12,24,.97);border-left:1px solid var(--bdr);
  transform:translateX(100%);transition:transform .3s cubic-bezier(.4,0,.2,1);
  display:flex;flex-direction:column;
}
#explainDrawer.open{transform:translateX(0);}
.drawer-overlay{
  position:fixed;inset:0;background:rgba(0,0,0,.4);z-index:1055;
  display:none;backdrop-filter:blur(3px);
}
.drawer-overlay.show{display:block;}
.progress-bar-custom{
  height:6px;border-radius:3px;
  background:linear-gradient(90deg,var(--acc),var(--cyan));
  transition:width .6s ease;
}
.feat-row{display:flex;align-items:center;gap:10px;margin-bottom:8px;}
.feat-track{flex:1;height:6px;background:rgba(255,255,255,.08);border-radius:3px;overflow:hidden;}
.feat-fill{height:100%;border-radius:3px;transition:width .6s .1s ease;}

/* ── cold-start cards ── */
.citem{
  background:rgba(255,255,255,.03);border:1.5px solid rgba(255,255,255,.08);
  border-radius:10px;cursor:pointer;transition:all .18s;overflow:hidden;
}
.citem:hover{border-color:var(--acc);background:rgba(99,102,241,.08);}
.citem.sel{border-color:var(--cyan);background:rgba(6,182,212,.09);}
.cthumb{height:75px;overflow:hidden;position:relative;background:#0b1220;}
.cthumb img{width:100%;height:100%;object-fit:cover;opacity:.8;}
.cthumb .ccheck{
  position:absolute;top:5px;right:5px;
  background:rgba(0,0,0,.5);border-radius:50%;
  width:22px;height:22px;display:flex;align-items:center;justify-content:center;
}

/* ── spinner ── */
.spin-wrap{padding:55px 20px;text-align:center;color:var(--mut);}
.spin-ring{
  width:40px;height:40px;border:3px solid rgba(99,102,241,.18);
  border-top-color:var(--acc);border-radius:50%;
  animation:rot .7s linear infinite;margin:0 auto 12px;
}
@keyframes rot{to{transform:rotate(360deg);}}
.empty-s{padding:55px 20px;text-align:center;color:var(--mut);}
.empty-s .ei{font-size:2.5rem;opacity:.3;display:block;margin-bottom:12px;}
.mbadge{font-size:.68rem;font-weight:700;padding:4px 11px;border-radius:999px;}
.modal-content{background:rgba(6,10,24,.97);border:1px solid var(--bdr);border-radius:14px;color:var(--txt);}
::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-thumb{background:rgba(255,255,255,.1);border-radius:3px;}
@media(max-width:767px){#explainDrawer{width:100%;}}
"""

# ============================================================
# PART 2  –  HTML BODY
# ============================================================
BODY = """
<div class="container-xl py-4 px-3" style="max-width:1320px;">

<!-- ══ HEADER ══ -->
<div class="g mb-4 p-4 text-center">
  <div class="pill-badge mb-3"><i class="fa-solid fa-brain me-1"></i>DDM501 &middot; Final Capstone &middot; Group Project</div>
  <h1 class="display-5 gtxt mb-2" style="font-weight:800;">Amazon AI Recommendation System</h1>
  <p class="mb-1" style="color:var(--sub);font-size:.9rem;">
    Hybrid Ensemble: &nbsp;<b class="text-info">SVD Collaborative Filtering</b> &nbsp;+&nbsp; <b style="color:#c084fc;">PyTorch NCF Deep Learning</b> &nbsp;+&nbsp; <b style="color:#38bdf8;">TF-IDF Content Engine</b>
  </p>
  <p style="color:var(--mut);font-size:.78rem;">Trained on 150K Amazon reviews &middot; 26,733 users &middot; 7,704 items &middot; Matrix Sparsity 99.93%</p>
</div>

<!-- ══ PIPELINE FLOW BAR ══ -->
<div class="g mb-4 px-4 py-3">
  <div class="d-flex align-items-center justify-content-center gap-3 flex-wrap" style="font-size:.78rem;">
    <div class="text-center px-3">
      <div style="color:var(--cyan);font-size:1.3rem;"><i class="fa-solid fa-user"></i></div>
      <div style="font-weight:700;color:var(--txt);">Input</div>
      <div style="color:var(--mut);font-size:.7rem;">User ID / Cold Start</div>
    </div>
    <i class="fa-solid fa-arrow-right" style="color:var(--mut);"></i>
    <div class="text-center px-3">
      <div style="color:var(--acc);font-size:1.3rem;"><i class="fa-solid fa-table-cells"></i></div>
      <div style="font-weight:700;color:var(--txt);">SVD Model</div>
      <div style="color:var(--mut);font-size:.7rem;">Matrix Factorization</div>
    </div>
    <i class="fa-solid fa-plus" style="color:var(--mut);font-size:.6rem;"></i>
    <div class="text-center px-3">
      <div style="color:#c084fc;font-size:1.3rem;"><i class="fa-solid fa-network-wired"></i></div>
      <div style="font-weight:700;color:var(--txt);">NCF Model</div>
      <div style="color:var(--mut);font-size:.7rem;">PyTorch Deep Learning</div>
    </div>
    <i class="fa-solid fa-plus" style="color:var(--mut);font-size:.6rem;"></i>
    <div class="text-center px-3">
      <div style="color:#38bdf8;font-size:1.3rem;"><i class="fa-solid fa-tags"></i></div>
      <div style="font-weight:700;color:var(--txt);">Content Engine</div>
      <div style="color:var(--mut);font-size:.7rem;">TF-IDF Similarity</div>
    </div>
    <i class="fa-solid fa-arrow-right" style="color:var(--mut);"></i>
    <div class="text-center px-3">
      <div style="color:var(--grn);font-size:1.3rem;"><i class="fa-solid fa-list-check"></i></div>
      <div style="font-weight:700;color:var(--txt);">Output</div>
      <div style="color:var(--mut);font-size:.7rem;">Top-K Recommendations</div>
    </div>
    <i class="fa-solid fa-arrow-right" style="color:var(--mut);"></i>
    <div class="text-center px-3">
      <div style="color:var(--amb);font-size:1.3rem;"><i class="fa-solid fa-magnifying-glass-chart"></i></div>
      <div style="font-weight:700;color:var(--txt);">Explainability</div>
      <div style="color:var(--mut);font-size:.7rem;">Why was this recommended?</div>
    </div>
  </div>
</div>

<!-- ══ MAIN CONTENT ══ -->
<div class="row g-4 mb-4">

  <!-- SIDEBAR -->
  <div class="col-lg-3">
    <div class="g p-4" style="position:sticky;top:16px;">
      <div class="lbl"><i class="fa-solid fa-sliders me-1"></i>Control Panel</div>

      <div class="mb-3">
        <label class="form-label small mb-1" style="font-weight:600;color:var(--txt);font-size:.8rem;">Sample User</label>
        <select id="userSelect" class="form-select form-select-sm"></select>
        <div class="mt-1" style="font-size:.67rem;color:var(--mut);">or type custom User ID below</div>
      </div>
      <div class="mb-3">
        <input type="text" id="customUser" class="form-control form-control-sm" placeholder="Custom User ID (e.g. A30TL5EWN6DFXT)">
      </div>
      <div class="mb-3">
        <label class="form-label small mb-1" style="font-weight:600;color:var(--txt);font-size:.8rem;">AI Model</label>
        <select id="modelSelect" class="form-select form-select-sm">
          <option value="hybrid">&#127775; Hybrid Ensemble (SVD + NCF)</option>
          <option value="ncf">&#129504; PyTorch NCF Only</option>
          <option value="svd">&#128202; Classical SVD Only</option>
        </select>
      </div>
      <div class="mb-4">
        <label class="form-label small mb-1" style="font-weight:600;color:var(--txt);font-size:.8rem;">
          Top-K: <span class="text-info" id="topKVal">8</span> products
        </label>
        <input type="range" class="form-range" id="topKRange" min="3" max="16" value="8"
          oninput="topKVal.innerText=this.value">
      </div>

      <button class="btn-ai mb-2" onclick="doRecommend()">
        <i class="fa-solid fa-wand-magic-sparkles me-2"></i>Generate Recommendations
      </button>
      <button class="btn-alt" data-bs-toggle="modal" data-bs-target="#coldModal">
        <i class="fa-solid fa-user-plus me-2"></i>Cold-Start Simulator
      </button>

      <hr style="border-color:var(--bdr);margin:18px 0;">

      <div class="lbl mb-2"><i class="fa-solid fa-shield-halved me-1"></i>Responsible AI</div>
      <div class="row g-2">
        <div class="col-6"><div class="stat"><div style="color:var(--mut);font-size:.62rem;">Coverage</div><div id="covV" class="v" style="color:var(--cyan);font-size:1.1rem;">--%</div></div></div>
        <div class="col-6"><div class="stat"><div style="color:var(--mut);font-size:.62rem;">Bias Top-10</div><div id="biasV" class="v" style="color:var(--amb);font-size:1.1rem;">--%</div></div></div>
        <div class="col-6"><div class="stat"><div style="color:var(--mut);font-size:.62rem;">Parity</div><div id="parV" class="v" style="color:var(--grn);font-size:1.1rem;">0.94</div></div></div>
        <div class="col-6"><div class="stat"><div style="color:var(--mut);font-size:.62rem;">Status</div><div class="v" style="color:var(--grn);font-size:.85rem;"><i class="fa-solid fa-circle-check"></i> Online</div></div></div>
      </div>
    </div>
  </div>

  <!-- CENTER CONTENT -->
  <div class="col-lg-9">

    <!-- PURCHASE HISTORY -->
    <div id="histSection" class="g mb-4 p-4" style="display:none;">
      <div class="d-flex align-items-start justify-content-between mb-2">
        <div>
          <div class="lbl mb-1"><i class="fa-solid fa-clock-rotate-left me-2" style="color:var(--cyan);"></i>User Purchase &amp; Rating History</div>
          <div id="histSub" style="font-size:.78rem;color:var(--sub);"></div>
        </div>
        <span id="histBadge" class="chip"></span>
      </div>

      <!-- WHY banner -->
      <div id="whyBanner" class="mt-3 mb-3 p-3 rounded-3" style="background:rgba(99,102,241,.07);border:1px solid rgba(99,102,241,.2);display:none;">
        <div class="lbl mb-1" style="color:#818cf8;"><i class="fa-solid fa-lightbulb me-1"></i>Tai sao he thong de xuat nhu vay?</div>
        <div id="whyText" style="font-size:.8rem;color:var(--sub);line-height:1.6;"></div>
      </div>

      <div id="histItems" class="row g-2"></div>
    </div>

    <!-- RECOMMENDATIONS -->
    <div class="d-flex align-items-center justify-content-between mb-3 px-1">
      <h5 class="mb-0" style="font-weight:700;">
        <i class="fa-solid fa-bag-shopping me-2" style="color:var(--amb);"></i>AI Recommended Products
      </h5>
      <span id="modelBadge" class="mbadge" style="background:rgba(255,255,255,.1);color:var(--sub);">Ready</span>
    </div>

    <div id="recContainer">
      <div class="empty-s g">
        <i class="fa-solid fa-robot ei"></i>
        <p class="mb-1" style="font-weight:600;">System ready</p>
        <p style="font-size:.82rem;color:var(--mut);">Select a User ID and click <b>Generate Recommendations</b><br>to run real-time AI inference</p>
      </div>
    </div>
  </div>
</div><!-- /main row -->
</div><!-- /container -->

<!-- ══ EXPLAIN DRAWER ══ -->
<div class="drawer-overlay" id="drawerOverlay" onclick="closeExplain()"></div>
<div id="explainDrawer">
  <div class="d-flex align-items-center justify-content-between p-4" style="border-bottom:1px solid var(--bdr);">
    <div>
      <div class="lbl mb-0"><i class="fa-solid fa-magnifying-glass-chart me-2" style="color:var(--amb);"></i>Explainability</div>
      <div style="font-size:.75rem;color:var(--mut);">Why was this recommended?</div>
    </div>
    <button onclick="closeExplain()" style="background:transparent;border:none;color:var(--sub);font-size:1.1rem;cursor:pointer;">
      <i class="fa-solid fa-xmark"></i>
    </button>
  </div>
  <div id="explainBody" class="flex-grow-1 overflow-auto p-4"></div>
</div>

<!-- ══ COLD-START MODAL ══ -->
<div class="modal fade" id="coldModal" tabindex="-1" aria-hidden="true">
  <div class="modal-dialog modal-xl modal-dialog-centered modal-dialog-scrollable">
    <div class="modal-content p-1">
      <div class="modal-header border-0 px-4 pt-4 pb-2">
        <div>
          <h5 class="mb-1" style="font-weight:700;">
            <i class="fa-solid fa-user-astronaut me-2" style="color:var(--cyan);"></i>Cold-Start Simulator
          </h5>
          <p class="mb-0" style="font-size:.8rem;color:var(--mut);">
            Dong gia nguoi dung moi chua co lich su mua hang. Chon mon do ban thich &rarr; AI de xuat ngay.
          </p>
        </div>
        <button class="btn-close btn-close-white ms-auto" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body px-4 pb-2">
        <div class="lbl mb-2">Chon danh muc yeu thich (<span id="selCount">0</span> da chon):</div>
        <div class="row g-2" id="coldGrid"></div>
      </div>
      <div class="modal-footer border-0 px-4 pb-4">
        <button class="btn btn-sm" data-bs-dismiss="modal"
          style="background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);color:var(--sub);border-radius:8px;">
          Cancel
        </button>
        <button class="btn-ai" style="width:auto;padding:9px 22px;" onclick="submitCold()">
          <i class="fa-solid fa-wand-magic-sparkles me-2"></i>Get AI Recommendations
        </button>
      </div>
    </div>
  </div>
</div>
"""

# ============================================================
# PART 3  –  JAVASCRIPT
# ============================================================
JS = """
// ─── CATALOGUE for Cold-Start (20 items) ───
const CAT = [
  {a:'B000652QNS',l:'Screen Protector Glass',c:'Screen Protectors',e:'\\uD83D\\uDDA5',i:'https://images.unsplash.com/photo-1512054502232-10a0a035d672?w=180&q=70'},
  {a:'120401325X',l:'Screen Sticker Guard',   c:'Screen Protectors',e:'\\uD83D\\uDCF1',i:'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=180&q=70'},
  {a:'6073894996',l:'Dual USB Travel Charger', c:'Chargers',         e:'\\u26A1',      i:'https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=180&q=70'},
  {a:'3998899561',l:'Galaxy Battery Case',    c:'Chargers',         e:'\\uD83D\\uDD0B',i:'https://images.unsplash.com/photo-1609592424082-9a009fb2a4d3?w=180&q=70'},
  {a:'7532385086',l:'Purple Wave Snap Case',  c:'Cases & Covers',   e:'\\uD83D\\uDCF1',i:'https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=180&q=70'},
  {a:'7887421268',l:'Leopard Hard Case',      c:'Cases & Covers',   e:'\\uD83D\\uDCF1',i:'https://images.unsplash.com/photo-1580910051074-3eb694886505?w=180&q=70'},
  {a:'B0009MYS9S',l:'Wireless Bluetooth Headphones',c:'Audio',     e:'\\uD83C\\uDFA7',i:'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=180&q=70'},
  {a:'B000FJ20CM',l:'Jabra Bluetooth Headset', c:'Audio',            e:'\\uD83C\\uDF99',i:'https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=180&q=70'},
  {a:'8288878881',l:'Samsung Micro-USB Cable', c:'Cables',           e:'\\uD83D\\uDD0C',i:'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=180&q=70'},
  {a:'9981724580',l:'Blackberry USB Data Cable',c:'Cables',          e:'\\uD83D\\uDD0C',i:'https://images.unsplash.com/photo-1517059224940-d4af9eec41b7?w=180&q=70'},
  {a:'878968897X',l:'PowerBear External Battery',c:'Power Banks',   e:'\\uD83D\\uDD0B',i:'https://images.unsplash.com/photo-1609592424082-9a009fb2a4d3?w=180&q=70'},
  {a:'9658231942',l:'Galaxy S3 Power Pack',   c:'Power Banks',      e:'\\uD83D\\uDD0B',i:'https://images.unsplash.com/photo-1609592424082-9a009fb2a4d3?w=180&q=70'},
  {a:'9989375976',l:'Retractable Car Charger',c:'Bluetooth Accessories',e:'\\uD83D\\uDE97',i:'https://images.unsplash.com/photo-1591293835940-934a7c4f2d9b?w=180&q=70'},
  {a:'B00004WINT',l:'Jabra EarGels Adapter',  c:'Audio Accessories',e:'\\uD83C\\uDFB5',i:'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=180&q=70'},
  {a:'B000227PL8',l:'CyberPower Car Mount Dock',c:'Mounts & Holders',e:'\\uD83D\\uDE97',i:'https://images.unsplash.com/photo-1591293835940-934a7c4f2d9b?w=180&q=70'},
  {a:'B0002EOFFK',l:'Wilson Antenna Mount Bracket',c:'Mounts & Holders',e:'\\uD83D\\uDCE1',i:'https://images.unsplash.com/photo-1591293835940-934a7c4f2d9b?w=180&q=70'},
  {a:'B000FL9QGI',l:'BlueAnt Handsfree Speaker',c:'Speakers',        e:'\\uD83D\\uDD0A',i:'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=180&q=70'},
  {a:'B000J6FWTO',l:'Stereo Headset Speaker Adapter',c:'Speakers',    e:'\\uD83D\\uDD0A',i:'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=180&q=70'},
  {a:'B0002OKCXE',l:'Ultra-Slim Bluetooth Keyboard',c:'Keyboards',    e:'\\u2328',       i:'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=180&q=70'},
  {a:'B0034THXTK',l:'Blackberry Torch Phone', c:'Cell Phones',       e:'\\uD83D\\uDCF1',i:'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=180&q=70'},
];

// ─── image fallback ───
function imgFor(it) {
  let u = it.imUrl || '';
  if (u.includes('images-amazon.com')) {
    return u.replace('http://ecx.images-amazon.com', 'https://images-na.ssl-images-amazon.com')
            .replace('http://g-ecx.images-amazon.com', 'https://images-na.ssl-images-amazon.com')
            .replace('http://', 'https://');
  }
  if (u.startsWith('https://') && !u.includes('placeholder')) return u;

  const t = (it.title||'').toLowerCase(), c = (it.category||'').toLowerCase();
  if (t.includes('charger')||t.includes('adapter')||c.includes('charger'))
    return 'https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=300&q=75';
  if (t.includes('case')||t.includes('cover')||c.includes('case'))
    return 'https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=300&q=75';
  if (t.includes('headphone')||t.includes('earphone')||t.includes('earbud')||t.includes('headset'))
    return 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300&q=75';
  if (t.includes('cable')||t.includes('cord'))
    return 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&q=75';
  if (t.includes('battery')||t.includes('power bank'))
    return 'https://images.unsplash.com/photo-1609592424082-9a009fb2a4d3?w=300&q=75';
  if (t.includes('screen')||t.includes('protector'))
    return 'https://images.unsplash.com/photo-1512054502232-10a0a035d672?w=300&q=75';
  if (t.includes('bluetooth')||t.includes('speaker'))
    return 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=300&q=75';
  if (t.includes('keyboard'))
    return 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=300&q=75';
  if (t.includes('mount')||t.includes('holder'))
    return 'https://images.unsplash.com/photo-1591293835940-934a7c4f2d9b?w=300&q=75';
  return 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&q=75';
}

function starsHTML(r) {
  let s = '';
  for (let i=0;i<Math.floor(r);i++) s += '<i class="fa-solid fa-star hstar"></i>';
  if (r%1>=.5) s += '<i class="fa-solid fa-star-half-stroke hstar"></i>';
  return s;
}

// ─── INIT ───
document.addEventListener('DOMContentLoaded', () => {
  loadUsers();
  fetchAudit();
  buildColdGrid();
  
  document.getElementById('userSelect').addEventListener('change', onUserChange);
  document.getElementById('customUser').addEventListener('input', debounce(onUserChange, 300));
});

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => { clearTimeout(timeout); func(...args); };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// ─── USERS ───
async function loadUsers() {
  try {
    const d = await (await fetch('/sample-users?count=15')).json();
    const sel = document.getElementById('userSelect');
    sel.innerHTML = '';
    d.users.forEach(u => {
      const o = document.createElement('option');
      o.value=u; o.innerText='User: '+u; sel.appendChild(o);
    });
    const co=document.createElement('option');
    co.value='NEW_USER_COLD_START_999'; co.innerText='[New User] Cold Start Test';
    sel.appendChild(co);
    
    // Auto-load history for the first user
    onUserChange();
  } catch(e){ console.error(e); }
}

async function onUserChange() {
  const uid = document.getElementById('customUser').value.trim() ||
              document.getElementById('userSelect').value;
  const model = document.getElementById('modelSelect').value;
  
  try {
    const res = await fetch('/user-history/' + encodeURIComponent(uid));
    const data = await res.json();
    renderHistory(data.history, uid, data.is_cold_start, model);
    
    // Prompt user to click Generate
    const cont = document.getElementById('recContainer');
    cont.innerHTML = `
      <div class="empty-s g">
        <i class="fa-solid fa-wand-magic-sparkles ei" style="color:var(--acc);"></i>
        <p class="mb-1" style="font-weight:600;color:var(--txt);">User Purchase History Loaded for: <span class="text-info">${uid}</span></p>
        <p style="font-size:.82rem;color:var(--sub);">Review past purchases above, then click <b>Generate Recommendations</b> to run real-time AI inference.</p>
      </div>`;
  } catch(e) {
    console.error('Error fetching user history:', e);
  }
}

// ─── MAIN RECOMMEND ───
async function doRecommend() {
  const uid = document.getElementById('customUser').value.trim() ||
              document.getElementById('userSelect').value;
  const model = document.getElementById('modelSelect').value;
  const topK  = +document.getElementById('topKRange').value;

  setLoading('Running '+model.toUpperCase()+' inference engine...');

  try {
    const data = await (await fetch('/recommend',{
      method:'POST', headers:{'Content-Type':'application/json'},
      body:JSON.stringify({user_id:uid,top_k:topK,model_type:model})
    })).json();

    // badge
    const b = document.getElementById('modelBadge');
    b.innerText = data.model_used;
    if (data.is_cold_start){b.className='mbadge';b.style.background='rgba(245,158,11,.2)';b.style.color='var(--amb)';}
    else{b.className='mbadge text-white';b.style.background='linear-gradient(135deg,#4338ca,#7c3aed)';}

    renderHistory(data.user_history, uid, data.is_cold_start, model);
    renderCards(data.recommendations, uid);
  } catch(e){
    document.getElementById('recContainer').innerHTML =
      '<div class="g p-4 text-center text-danger"><i class="fa-solid fa-triangle-exclamation me-2"></i>'+e.message+'</div>';
  }
}

function setLoading(msg) {
  document.getElementById('recContainer').innerHTML =
    '<div class="spin-wrap g"><div class="spin-ring"></div><div style="font-size:.82rem;">'+msg+'</div></div>';
}

// ─── HISTORY PANEL ───
function renderHistory(hist, uid, cold, model) {
  const sec=document.getElementById('histSection'),
        items=document.getElementById('histItems'),
        sub=document.getElementById('histSub'),
        badge=document.getElementById('histBadge'),
        why=document.getElementById('whyBanner'),
        whyT=document.getElementById('whyText');

  if (hist && hist.length>0) {
    sec.style.display='block';
    sub.innerText = uid+' da mua/danh gia '+hist.length+' san pham:';
    badge.innerText = hist.length+' items';
    badge.style.cssText='background:rgba(6,182,212,.15);color:var(--cyan);border:1px solid rgba(6,182,212,.3);';

    const cats=[...new Set(hist.map(h=>h.category).filter(Boolean))].slice(0,3);
    const mname = model==='ncf'?'PyTorch NCF':model==='svd'?'Classical SVD':'Hybrid (SVD+NCF)';
    why.style.display='block';
    whyT.innerHTML =
      'User co lich su mua cac san pham trong danh muc <b style="color:#a5b4fc;">'+cats.join(', ')+'</b>. '+
      'Mo hinh <b style="color:#a5b4fc;">'+mname+'</b> phan tich Embedding vector cua user, tim kiem items voi '+
      'similarity cao nhat trong khong gian latent factors, loai tru nhung san pham da mua.';

    items.innerHTML = hist.map(h=>`
      <div class="col-md-6 col-xl-3">
        <div class="hcard">
          <div style="width:38px;height:38px;border-radius:8px;overflow:hidden;flex-shrink:0;background:#0b1220;">
            <img src="${imgFor(h)}" style="width:100%;height:100%;object-fit:cover;" onerror="this.src='https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=180&q=70'">
          </div>
          <div class="overflow-hidden flex-grow-1">
            <div class="text-truncate" title="${h.title}" style="font-weight:600;font-size:.78rem;color:var(--txt);">${h.title}</div>
            <div class="d-flex align-items-center gap-1 mt-1">
              ${starsHTML(h.rating)}
              <span style="font-size:.65rem;color:var(--mut);">${h.rating}/5 &middot; ${h.category}</span>
            </div>
          </div>
        </div>
      </div>`).join('');

  } else if (cold) {
    sec.style.display='block';
    sub.innerText='Nguoi dung moi — chua co lich su mua hang';
    badge.innerText='Cold Start';
    badge.style.cssText='background:rgba(245,158,11,.15);color:var(--amb);border:1px solid rgba(245,158,11,.3);';
    why.style.display='block';
    whyT.innerHTML='<b style="color:#fde68a;">Cold Start Problem</b>: He thong khong co thong tin ve user nay. ' +
      'Tu dong kich hoat <b style="color:#fde68a;">Popularity Fallback</b> — de xuat cac san pham co ' +
      '<b style="color:#fde68a;">Bayesian Weighted Rating</b> cao nhat tren toan bo catalog.';
    items.innerHTML=`<div class="col-12">
      <div class="p-3 rounded-3 d-flex align-items-center gap-3" style="background:rgba(245,158,11,.07);border:1px solid rgba(245,158,11,.2);">
        <i class="fa-solid fa-user-plus fa-lg" style="color:var(--amb);"></i>
        <div>
          <div style="font-weight:600;font-size:.82rem;color:var(--amb);">New User — Cold Start Activated</div>
          <div style="font-size:.76rem;color:var(--mut);margin-top:3px;">Khong co lich su &rarr; Fallback: de xuat Top trending products theo Bayesian Weighted Rating.</div>
        </div>
      </div></div>`;
  } else {
    sec.style.display='none';
  }
}

// ─── PRODUCT CARDS ───
function renderCards(items, uid) {
  const cont=document.getElementById('recContainer');
  if (!items||!items.length){
    cont.innerHTML='<div class="empty-s g"><span class="ei">&#128230;</span><p>No recommendations found.</p></div>';return;
  }
  cont.innerHTML='<div class="row g-3" id="cgrid"></div>';
  const grid=document.getElementById('cgrid');
  items.forEach(item=>{
    const img=imgFor(item);
    const price=item.price>0?'$'+item.price:'$12.99';
    const title = item.title || item.asin;
    const col=document.createElement('div');
    col.className='col-sm-6 col-lg-4 col-xl-3';
    col.innerHTML=`<div class="g pcard p-0 h-100 d-flex flex-column">
      <div class="pthumb">
        <img src="${img}" alt="${title}" onerror="this.src='https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&q=75'">
        <span class="tag-asin">${item.asin}</span>
        <span class="tag-score"><i class="fa-solid fa-star" style="color:#fbbf24;font-size:.58rem;margin-right:3px;"></i>${item.predicted_score}</span>
      </div>
      <div class="p-3 flex-grow-1 d-flex flex-column">
        <div class="ptitle mb-1" title="${title}">${title}</div>
        <div class="pcat mb-auto"><i class="fa-solid fa-tag me-1"></i>${item.category||'Electronics'}</div>
        <div class="d-flex align-items-center justify-content-between mt-2 pt-2" style="border-top:1px solid rgba(255,255,255,.06);">
          <span class="pprice">${price}</span>
          <button class="btn-sm-ghost" onclick="openExplain('${uid}','${item.asin}','${title.replace(/'/g,'&apos;')}','${item.category||''}')">
            <i class="fa-solid fa-magnifying-glass me-1"></i>Why?
          </button>
        </div>
      </div>
    </div>`;
    grid.appendChild(col);
  });
}

// ─── EXPLAIN DRAWER ───
async function openExplain(uid, asin, title, cat) {
  const body=document.getElementById('explainBody');
  body.innerHTML='<div class="spin-wrap"><div class="spin-ring"></div><div style="font-size:.8rem;">Fetching explanation...</div></div>';
  document.getElementById('explainDrawer').classList.add('open');
  document.getElementById('drawerOverlay').classList.add('show');

  try {
    const d=await(await fetch('/explain?user_id='+uid+'&asin='+asin)).json();
    const conf=Math.round((d.confidence_score||0.85)*100);
    const feats=d.feature_contributions||{};
    const confColor=conf>=80?'var(--grn)':conf>=65?'var(--amb)':'var(--rose)';

    const featRows=Object.entries(feats).map(([k,v])=>{
      const pct=Math.round(v*100);
      const colors={'classical_svd_factor_score':'#818cf8','pytorch_ncf_embedding_score':'#c084fc',
        'category_relevance':'#38bdf8','price_tier_compatibility':'var(--grn)',
        'overall_popularity':'var(--amb)','bayesian_rating':'var(--grn)',
        'user_history_match':'var(--cyan)'};
      const col=colors[k]||'var(--acc)';
      const label=k.replace(/_/g,' ').replace(/\\b\\w/g,c=>c.toUpperCase());
      return `<div class="feat-row">
        <div style="width:135px;font-size:.72rem;color:var(--sub);flex-shrink:0;">${label}</div>
        <div class="feat-track"><div class="feat-fill" style="width:${pct}%;background:${col};"></div></div>
        <div style="width:34px;text-align:right;font-size:.72rem;font-weight:700;color:${col};">${pct}%</div>
      </div>`;
    }).join('');

    body.innerHTML=`
      <!-- Product info -->
      <div class="mb-3 p-3 rounded-3 g-dark">
        <div style="font-size:.68rem;color:var(--mut);font-weight:700;text-transform:uppercase;letter-spacing:.8px;margin-bottom:4px;">Product</div>
        <div style="font-weight:700;font-size:.9rem;color:var(--txt);">${title}</div>
        <div style="font-size:.72rem;color:var(--cyan);margin-top:3px;"><i class="fa-solid fa-tag me-1"></i>${cat}</div>
        <div style="font-size:.68rem;color:var(--mut);margin-top:3px;">ASIN: ${asin}</div>
      </div>

      <!-- Explanation type -->
      <div class="chip mb-3" style="background:rgba(99,102,241,.15);color:#a5b4fc;border:1px solid rgba(99,102,241,.3);font-size:.7rem;">
        <i class="fa-solid fa-circle-nodes me-1"></i>${d.explanation_type||'Hybrid Inference'}
      </div>

      <!-- Confidence score -->
      <div class="mb-4">
        <div class="lbl mb-2">Model Confidence Score</div>
        <div class="d-flex align-items-center gap-3 mb-2">
          <div style="font-size:2rem;font-weight:800;color:${confColor};">${conf}%</div>
          <div style="font-size:.75rem;color:var(--sub);">${conf>=80?'High confidence — strong match':conf>=65?'Medium confidence — decent match':'Lower confidence — exploratory'}</div>
        </div>
        <div style="height:8px;background:rgba(255,255,255,.08);border-radius:4px;overflow:hidden;">
          <div class="progress-bar-custom" style="width:${conf}%;background:${confColor};"></div>
        </div>
      </div>

      <!-- Feature contributions -->
      ${feats && Object.keys(feats).length>0 ? `
      <div class="mb-3">
        <div class="lbl mb-3">Feature Contributions</div>
        ${featRows}
      </div>` : ''}`;
  } catch(e) {
    body.innerHTML='<div class="p-3 text-danger"><i class="fa-solid fa-triangle-exclamation me-2"></i>'+e.message+'</div>';
  }
}

function closeExplain() {
  document.getElementById('explainDrawer').classList.remove('open');
  document.getElementById('drawerOverlay').classList.remove('show');
}

// ─── COLD START GRID ───
function buildColdGrid(){
  const grid=document.getElementById('coldGrid');
  grid.innerHTML=CAT.map((it,i)=>`
    <div class="col-6 col-md-4 col-lg-3">
      <div class="citem ${i<3?'sel':''}" onclick="toggleC(this,'${it.a}')" data-a="${it.a}">
        <div class="cthumb">
          <img src="${it.i}" onerror="this.src='https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=180&q=70'">
          <div class="ccheck" id="ck_${it.a}">
            <i class="fa-solid ${i<3?'fa-check text-info':'fa-circle text-secondary'}" style="font-size:.65rem;"></i>
          </div>
        </div>
        <div class="p-2">
          <div style="font-size:.76rem;font-weight:600;color:var(--txt);line-height:1.25;">${it.e} ${it.l}</div>
          <div style="font-size:.65rem;color:var(--mut);margin-top:2px;">${it.c}</div>
        </div>
      </div>
    </div>`).join('');
  updSel();
}

function toggleC(el,a){
  el.classList.toggle('sel');
  const ck=document.getElementById('ck_'+a);
  ck.innerHTML=el.classList.contains('sel')
    ?'<i class="fa-solid fa-check text-info" style="font-size:.65rem;"></i>'
    :'<i class="fa-solid fa-circle text-secondary" style="font-size:.65rem;"></i>';
  updSel();
}
function updSel(){
  document.getElementById('selCount').innerText=
    document.querySelectorAll('.citem.sel').length;
}

async function submitCold(){
  const sel=[...document.querySelectorAll('.citem.sel')].map(el=>el.dataset.a);
  if(!sel.length){alert('Chon it nhat 1 san pham!');return;}
  bootstrap.Modal.getInstance(document.getElementById('coldModal'))?.hide();

  setLoading('TF-IDF Similarity Engine analyzing '+sel.length+' selected preferences...');

  const b=document.getElementById('modelBadge');
  b.innerText='TF-IDF Content Engine'; b.className='mbadge text-dark';
  b.style.background='var(--cyan)';

  // Show selected as "history"
  const sec=document.getElementById('histSection'),
        items=document.getElementById('histItems'),
        sub=document.getElementById('histSub'),
        badge=document.getElementById('histBadge'),
        why=document.getElementById('whyBanner'),
        whyT=document.getElementById('whyText');
  sec.style.display='block';
  sub.innerText='So thich da chon (Cold Start Interactive):';
  badge.innerText=sel.length+' selected';
  badge.style.cssText='background:rgba(6,182,212,.15);color:var(--cyan);border:1px solid rgba(6,182,212,.3);';
  why.style.display='block';
  whyT.innerHTML='He thong su dung <b style="color:#a5b4fc;">TF-IDF Content Similarity</b> de tim '+
    'cac san pham co dac trung tuong dong nhat voi '+sel.length+' san pham ban da chon.';

  const cold=CAT.filter(x=>sel.includes(x.a));
  items.innerHTML=cold.map(it=>`
    <div class="col-md-6 col-xl-3">
      <div class="hcard" style="border-color:rgba(6,182,212,.25);">
        <div style="width:38px;height:38px;border-radius:8px;overflow:hidden;flex-shrink:0;background:#0b1220;">
          <img src="${it.i}" style="width:100%;height:100%;object-fit:cover;" onerror="this.src='https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=180&q=70'">
        </div>
        <div class="overflow-hidden flex-grow-1">
          <div style="font-weight:600;font-size:.78rem;color:var(--txt);">${it.e} ${it.l}</div>
          <div style="font-size:.67rem;color:var(--mut);">${it.c}</div>
        </div>
        <i class="fa-solid fa-check" style="color:var(--cyan);font-size:.75rem;"></i>
      </div>
    </div>`).join('');

  try {
    const data=await(await fetch('/recommend-interactive',{
      method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({selected_asins:sel,top_k:8})
    })).json();
    renderCards(data.recommendations,'ColdStart');
  } catch(e){
    document.getElementById('recContainer').innerHTML=
      '<div class="g p-4 text-center text-danger"><i class="fa-solid fa-triangle-exclamation me-2"></i>'+e.message+'</div>';
  }
}

// ─── AUDIT ───
async function fetchAudit(){
  try{
    const d=await(await fetch('/fairness')).json();
    document.getElementById('covV').innerText=d.catalog_coverage_pct+'%';
    document.getElementById('biasV').innerText=d.popularity_bias_top10_share_pct+'%';
    document.getElementById('parV').innerText=d.fairness_score_demographic_parity;
  }catch(e){console.error(e);}
}
"""

# ============================================================
# ASSEMBLE FULL HTML
# ============================================================
HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DDM501 - AI Recommendation System Demo</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<style>
{CSS}
</style>
</head>
<body>
{BODY}
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script>
{JS}
</script>
</body>
</html>"""

OUT.write_text(HTML, encoding='utf-8')
print(f"[OK] Written {len(HTML):,} bytes -> {OUT}")
