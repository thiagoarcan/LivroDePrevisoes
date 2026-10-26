# -*- coding: utf-8 -*-
CSS_CONTENT = """
/* Unified component system. Width belongs to the workspace; reading length belongs to each region. */
:root { --font-sans: 'Segoe UI', system-ui, sans-serif; --bg-app:#101719; --bg-surface:#192326; --bg-surface-hover:#233236; --bg-surface-active:#2c4145; --bg-elevated:var(--bg-surface); --bg-surface-elevated:var(--bg-surface); --text-main:#f0f5f3; --text-secondary:#c0ceca; --text-muted:#a8bdb6; --border-color:#657d75; --border-color-focus:#84d8c2; --color-primary:#1c7460; --color-primary-hover:#175e4e; --primary-text:#fff; --color-success:#237245; --color-danger:#b92e3d; --color-warning:#f3bd53; --color-info:#99dfcc; --warning-text:#201700; --status-overdue-bg:#45202a; --status-overdue-text:#ffcad0; --status-overdue-border:#fb8392; --status-critico-bg:#45202a; --status-critico-text:#ffcad0; --status-urgente-bg:#482c1d; --status-urgente-text:#ffd1ad; --status-atencao-bg:#40351b; --status-atencao-text:#ffe4a3; --status-monitor-bg:#203655; --status-monitor-text:#c4deff; --status-normal-bg:#163d32; --status-normal-text:#b8efda; --status-concluido-bg:#163d32; --status-concluido-text:#b8efda; --radius-sm:6px; --sidebar-width:232px; --app-header-height:84px; --transition:160ms ease; color-scheme:dark; }
body.theme-light { --bg-app:#f0f3ef; --bg-surface:#fff; --bg-surface-hover:#f1f6f3; --bg-surface-active:#e0eee7; --text-main:#1b3029; --text-secondary:#445d52; --text-muted:#52695e; --border-color:#7b9489; --border-color-focus:#17664f; --color-primary:#17664f; --color-primary-hover:#104d3b; --color-info:#17664f; --status-overdue-bg:#ffebee; --status-overdue-text:#8c1d32; --status-critico-bg:#ffebee; --status-critico-text:#8c1d32; --status-urgente-bg:#fff0e3; --status-urgente-text:#8a3d08; --status-atencao-bg:#fff4d2; --status-atencao-text:#705000; --status-monitor-bg:#eaf2ff; --status-monitor-text:#18467f; --status-normal-bg:#e4f5ed; --status-normal-text:#17553d; --status-concluido-bg:#e4f5ed; --status-concluido-text:#17553d; color-scheme:light; }
body.theme-industrial { --bg-app:#000; --bg-surface:#101010; --bg-surface-hover:#242424; --bg-surface-active:#333; --text-main:#fff; --text-secondary:#e2e2e2; --text-muted:#c9c9c9; --border-color:#8a8a8a; --border-color-focus:#ffdb44; --color-primary:#ffdb44; --color-primary-hover:#e8bd20; --primary-text:#111; --color-info:#ffe274; }
* { box-sizing:border-box; }
html { font-size:16px; scroll-padding-top:calc(var(--app-header-height) + 60px); }
body { --bg-elevated:var(--bg-surface); --bg-surface-elevated:var(--bg-surface); margin:0; font-family:var(--font-sans); font-size:1rem; line-height:1.45; background:var(--bg-app); color:var(--text-main); }
button,input,select,textarea { font:inherit; }
button { cursor:pointer; }
button:disabled { opacity:.55; cursor:not-allowed; }
button,select,input,textarea { max-inline-size:100%; }
button { overflow-wrap:anywhere; }
svg { flex-shrink:0; vertical-align:middle; }
img,canvas { max-width:100%; }
p,h1,h2,h3,h4 { margin:0 0 .6rem; }
h2,h3,h4 { line-height:1.3; }
small,.form-help,.card-subtitle { font-size:.875rem; color:var(--text-secondary); }
.form-help { margin-top:.3rem; }
.card-subtitle { max-width:80ch; }
a { color:var(--color-info); }
:focus-visible { outline:3px solid var(--border-color-focus); outline-offset:3px; }
[hidden] { display:none!important; }
.skip-link { position:fixed; top:-100px; left:1rem; z-index:2100; padding:.8rem; background:var(--bg-surface); }
.skip-link:focus { top:8px; }
.app-header { position:sticky; top:0; z-index:100; display:flex; align-items:center; gap:1rem; padding:.7rem 1.25rem; border-bottom:1px solid var(--line-subtle); background:var(--bg-surface); min-width:0; }
.app-header { padding-top:max(.7rem,env(safe-area-inset-top)); }
.header-left,.header-actions,.header-status-bar { display:flex; align-items:center; gap:.6rem; min-width:0; flex-wrap:wrap; }
.header-left { flex:1; }
.header-brand { display:flex; align-items:center; gap:.6rem; }
.header-brand h1 { margin:0; font-size:1rem; white-space:nowrap; }
.header-brand .subtitle { font-size:.875rem; color:var(--text-muted); }
.header-console-box { display:flex; align-items:center; gap:.5rem; }
.header-console-box label { white-space:nowrap; }
.header-console-select { width:180px; }
.header-status-bar { gap:.35rem; }
.header-status-bar #chipHeaderAudioWarning { min-height:44px; border-radius:7px; align-items:center; }
.header-status-bar .status-pill { display:none; }
.clock-display { font-variant-numeric:tabular-nums; font-weight:650; font-size:1rem; white-space:nowrap; }
.header-viewmode-box { display:flex; align-items:center; gap:.4rem; }
.header-viewmode-box label { display:none; }
.header-viewmode-select { width:165px; font-size:.875rem; }
.btn-hamburger { display:none; }
.btn-header-bell,.btn-hamburger { position:relative; background:var(--bg-surface); color:var(--text-main); border:1px solid var(--border-color); border-radius:8px; min-width:44px; min-height:44px; align-items:center; justify-content:center; }
.bell-badge,.badge-count,.cat-count,.bottom-nav-badge,.nav-badge { display:inline-flex; align-items:center; justify-content:center; font-size:.875rem; font-weight:700; border-radius:20px; min-width:1.5rem; padding:.1rem .4rem; background:var(--bg-surface-active); color:var(--text-main); }
.bell-badge { position:absolute; right:-5px; top:-5px; background:var(--color-danger); color:#fff; }
.app-nav { position:fixed; left:0; top:var(--app-header-height); bottom:0; width:var(--sidebar-width); display:flex; flex-direction:column; align-items:stretch; padding:1.25rem .75rem; gap:.35rem; border-right:1px solid var(--line-subtle); background:var(--bg-nav); z-index:80; overflow-y:auto; }
.nav-item,.drawer-item { display:flex; gap:.7rem; align-items:center; text-align:left; border:1px solid transparent; border-radius:7px; color:var(--text-secondary); background:transparent; font-size:.875rem; font-weight:600; padding:.75rem .6rem; min-height:48px; }
.nav-item .badge-count { margin-left:auto; }
.nav-item.active,.drawer-item.active { background:var(--bg-surface-active); color:var(--text-main); border-color:var(--line-subtle); font-weight:750; }
.nav-item:hover,.drawer-item:hover { background:var(--bg-surface-hover); color:var(--text-main); }
.app-main { margin-left:var(--sidebar-width); padding:1.5rem clamp(1rem,2vw,2.5rem) 2.5rem; width:calc(100% - var(--sidebar-width)); max-width:none; min-width:0; }
.view-section { display:none; min-width:0; }
.view-section.active { display:block; }
.view-heading { grid-column:1/-1; font-size:clamp(1.35rem,1.1rem + .6vw,1.85rem); font-weight:650; letter-spacing:-.025em; margin:0 0 .65rem; line-height:1.25; text-wrap:balance; }
.view-section>* { min-width:0; }
.persistent-banner { display:none; gap:.75rem; align-items:center; justify-content:space-between; padding:.55rem 1rem; margin-left:var(--sidebar-width); border-bottom:1px solid var(--border-color); font-size:.875rem; }
.persistent-banner.active { display:flex; }
.alarm-banner { position:sticky; top:var(--app-header-height); z-index:101; background:var(--status-overdue-bg); color:var(--status-overdue-text); }
.backup-banner,.layout-banner { background:var(--bg-surface); color:var(--text-secondary); }
.persistent-banner>div { min-width:0; flex-wrap:wrap; }
.runtime-notice { margin:1rem; padding:1rem; border:1px solid var(--border-color); border-radius:8px; background:var(--bg-surface); font-size:.875rem; }
.btn { display:inline-flex; justify-content:center; align-items:center; gap:.45rem; min-height:44px; border:1px solid transparent; border-radius:7px; padding:.55rem .9rem; font-size:.875rem; line-height:1.3; font-weight:650; text-decoration:none; white-space:normal; }
.btn-primary { background:var(--color-primary); color:var(--primary-text); }
.btn-primary:hover { background:var(--color-primary-hover); }
.btn-success { background:var(--color-success); color:#fff; }
.btn-danger { background:var(--color-danger); color:#fff; }
.btn-warning { background:var(--color-warning); color:var(--warning-text); }
.btn-secondary { background:var(--bg-surface-active); color:var(--text-main); border-color:var(--border-color); }
.btn-outline { background:transparent; color:var(--text-main); border-color:var(--border-color); }
.btn-outline:hover { background:var(--bg-surface-hover); }
.btn-icon { width:44px; min-width:44px; padding:.5rem; }
.btn-sm { padding:.45rem .65rem; }
.fab-btn { display:none; }
.card,.context-panel,.cadastro-hub-card,.pending-detail-pane { background:var(--bg-surface); border:1px solid var(--line-subtle); border-radius:12px; padding:1.25rem; min-width:0; align-self:start; }
.card-header { display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:.75rem; margin-bottom:1.1rem; padding-bottom:1rem; border-bottom:1px solid var(--line-subtle); }
.card-title { display:flex; gap:.6rem; align-items:center; font-size:1.075rem; font-weight:650; letter-spacing:-.015em; }
.context-panel h2 { font-size:1rem; margin-bottom:1rem; }
.context-panel h3 { font-size:.9rem; margin-top:1.2rem; }
.context-panel p { max-width:75ch; overflow-wrap:anywhere; }
.context-panel ul { margin:.6rem 0; padding:0; list-style:none; }
.context-panel li { border-bottom:1px solid var(--border-color); padding:.7rem 0; }
.context-panel li:last-child { border-bottom:0; }
.context-panel dl { margin:0; }
.context-panel dt { color:var(--text-secondary); font-size:.875rem; }
.context-panel dd { margin:0 0 .65rem; font-weight:600; overflow-wrap:anywhere; }
.context-count-row { display:grid; grid-template-columns:minmax(0,1fr) auto; gap:.75rem; align-items:center; }
.context-count-row meter { grid-column:1/-1; width:100%; height:.6rem; }
.context-event { text-align:left; display:block; width:100%; border:0; border-radius:6px; padding:.6rem; background:transparent; color:var(--text-main); }
.context-event:hover,.context-event[aria-pressed=true] { background:var(--bg-surface-active); }
.context-event small { display:block; margin-top:.3rem; }
.context-actions { display:flex; gap:.5rem; flex-wrap:wrap; margin-top:1rem; }
.form-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr)); gap:1rem; }
.form-group { display:flex; flex-direction:column; gap:.35rem; min-width:0; }
.span-full { grid-column:1/-1; }
.span-2 { grid-column:span 2; }
label,.control-label { display:block; font-size:.875rem; font-weight:600; color:var(--text-secondary); }
label .required { color:var(--status-overdue-text); }
input:not([type=checkbox]):not([type=radio]),select,textarea { width:100%; min-width:0; min-height:44px; padding:.6rem .7rem; color:var(--text-main); background:var(--bg-app); border:1px solid var(--border-color); border-radius:6px; }
input[type=color] { width:54px!important; padding:4px!important; }
input[type=range] { padding:0; accent-color:var(--color-primary); }
textarea { resize:vertical; min-height:90px; }
input:disabled,select:disabled,textarea:disabled { background:var(--bg-surface-active); color:var(--text-muted); }
.form-checkbox { display:flex; align-items:center; gap:.6rem; min-height:44px; color:var(--text-main); cursor:pointer; }
input[type=checkbox],input[type=radio] { width:20px; height:20px; flex:0 0 auto; accent-color:var(--color-primary); }
fieldset { min-width:0; margin:0; padding:1rem; border:1px solid var(--border-color); border-radius:8px; }
legend { padding:0 .5rem; font-size:.95rem; font-weight:700; }
.event-form-sections { display:grid; gap:1rem; grid-template-columns:1fr 1fr; }
.event-fieldset { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.85rem; }
.fieldset-atividade,.fieldset-lousa { grid-column:1/-1; }
.event-fieldset>.form-group:only-of-type,.event-fieldset>.card-header,.event-fieldset>#boxCustomAlarmSettings { grid-column:1/-1; }
#formEvent>.event-fieldset { margin-top:1rem; }
.optional-group { grid-column:1/-1; }
summary { cursor:pointer; font-weight:650; padding:.7rem 0; min-height:44px; }
.form-sticky-submit-bar { position:static; bottom:0; z-index:40; padding:1rem 0 .25rem; border-top:1px solid var(--border-color); background:var(--bg-surface); }
.form-sticky-submit-bar>.form-checkbox { flex:1 1 100%; }
.dashboard-metrics { display:grid; grid-template-columns:repeat(7,minmax(0,1fr)); gap:.65rem; margin-bottom:1rem; }
.dashboard-overview,.dashboard-context-stack { display:contents; }
.dashboard-overview>.context-panel { width:100%; }
.metric-card { display:flex; gap:.7rem; align-items:center; min-width:0; border:1px solid var(--line-subtle); border-radius:8px; padding:.85rem; background:var(--bg-surface); color:var(--text-main); text-align:left; }
.metric-card[data-filter]:hover { border-color:var(--border-color-focus); }
.metric-icon { display:flex; align-items:center; justify-content:center; width:34px; height:34px; border-radius:7px; color:var(--text-main); flex-shrink:0; }
.metric-value { font-size:1.65rem; font-weight:650; line-height:1.15; font-variant-numeric:tabular-nums; letter-spacing:-.035em; }
.metric-label { font-size:.875rem; color:var(--text-secondary); margin-top:.25rem; }
.dashboard-highlight-grid { display:grid; grid-template-columns:minmax(0,1.6fr) minmax(0,1fr); gap:1rem; align-items:start; }
.spotlight-card { background:var(--bg-surface); border:1px solid var(--border-color-focus); border-radius:12px; padding:1.5rem; min-width:0; }
.spotlight-header { display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:.7rem; margin-bottom:.85rem; }
.spotlight-badge { font-size:.875rem; font-weight:700; }
.spotlight-body { display:flex; flex-direction:column; gap:.85rem; }
.spotlight-path { font-size:.875rem; color:var(--text-secondary); }
.spotlight-desc { font-size:clamp(1.1rem,1rem + .35vw,1.4rem); font-weight:650; line-height:1.4; margin-top:.65rem; max-width:75ch; overflow-wrap:anywhere; }
.spotlight-timer { border-top:1px solid var(--border-color); padding-top:.7rem; }
.time-left { font-size:clamp(1.7rem,1.3rem + 1vw,2.6rem); font-weight:650; letter-spacing:-.035em; color:var(--text-main); font-variant-numeric:tabular-nums; }
.sched-time { font-size:.875rem; color:var(--text-secondary); }
.tablet-alarms-panel { display:block; border:1px solid var(--line-subtle); border-radius:12px; padding:1rem; background:var(--bg-surface); min-width:0; }
.dashboard-urgent-cards { display:none; }
#cardDashboardUrgent { margin-top:1rem; }
#dashboardSelectedDetail,#dashboardContextPanel { margin-top:1rem; }
.status-badge { display:inline-flex; align-items:center; gap:.3rem; border-radius:5px; padding:.25rem .45rem; background:var(--bg-surface-active); color:var(--text-main); font-size:.875rem; font-weight:650; white-space:normal; }
.status-badge.overdue,.status-badge.atrasado { background:var(--status-overdue-bg); color:var(--status-overdue-text); }
.status-badge.critico { background:var(--status-critico-bg); color:var(--status-critico-text); }
.status-badge.urgente { background:var(--status-urgente-bg); color:var(--status-urgente-text); }
.status-badge.atencao { background:var(--status-atencao-bg); color:var(--status-atencao-text); }
.status-badge.normal,.status-badge.concluido { background:var(--status-normal-bg); color:var(--status-normal-text); }
.status-pill { padding:.3rem .5rem; border:1px solid var(--border-color); border-radius:30px; font-size:.875rem; color:var(--text-main); background:var(--bg-surface); }
.status-pill.warning { color:var(--status-atencao-text); background:var(--status-atencao-bg); }
.status-pill.ok { color:var(--status-normal-text); background:var(--status-normal-bg); }
#statusModalAudio>span { color:var(--text-main)!important; }
.events-toolbar { padding:1.1rem; border:1px solid var(--line-subtle); border-radius:12px; background:var(--bg-surface); margin-bottom:1rem; }
.toolbar-primary { display:flex; gap:.8rem; align-items:center; flex-wrap:wrap; }
.toolbar-primary>div { min-width:0; }
.toolbar-primary>div:not(.search-box) { flex-wrap:wrap; }
.search-box { flex:1 1 260px; min-width:0; position:relative; }
.search-box>svg { position:absolute; left:.7rem; bottom:.9rem; }
.search-box input { padding-left:2.3rem!important; }
.toolbar-filters { display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,170px),1fr)); gap:.8rem; margin-top:.9rem; }
.pending-master-detail-grid { display:grid; grid-template-columns:minmax(0,1.7fr) minmax(280px,1fr); gap:1rem; align-items:start; }
.pending-master { min-width:0; }
.pending-detail-pane { position:sticky; top:calc(var(--app-header-height) + 64px); max-height:calc(100dvh - var(--app-header-height) - 80px); overflow:auto; }
.pending-detail-pane>div { min-width:0; flex-wrap:wrap; }
.detail-navigation,.events-pagination { display:flex; align-items:center; justify-content:space-between; gap:.6rem; flex-wrap:wrap; margin:.65rem 0; font-size:.875rem; }
.events-container-cards { display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,310px),1fr)); gap:1rem; align-items:start; }
.event-card,.completed-event-card,.color-range-card { min-width:0; background:var(--bg-surface); border:1px solid var(--line-subtle); border-left:1px solid var(--border-color-focus); border-radius:12px; padding:1.1rem; overflow-wrap:anywhere; }
.event-card-header,.event-card-footer { display:flex; justify-content:space-between; gap:.5rem; flex-wrap:wrap; }
.event-card-header { margin-bottom:.7rem; }
.event-card-desc,.event-description { font-weight:600; margin:.75rem 0; }
.event-countdown { color:var(--text-main); font-variant-numeric:tabular-nums; }
.event-card.selected-master-card { outline:2px solid var(--border-color-focus); outline-offset:-2px; }
.event-card-footer { border-top:1px solid var(--border-color); padding-top:.75rem; margin-top:.75rem; }
.table-responsive,.hub-list-container { overflow:auto; min-width:0; max-width:100%; border:1px solid var(--border-color); border-radius:7px; background:var(--bg-surface); }
.data-table { border-collapse:collapse; width:100%; font-size:.875rem; }
.data-table th { text-align:left; background:var(--bg-surface-hover); color:var(--text-secondary); font-size:.8125rem; font-weight:700; }
.data-table th,.data-table td { padding:.8rem .85rem; border-bottom:1px solid var(--line-subtle); vertical-align:top; overflow-wrap:normal; word-break:normal; }
.data-table tbody tr:hover { background:var(--bg-surface-hover); }
.data-table td:last-child { min-width:80px; }
#tableDashboardUrgent { min-width:840px; }
#tableDashboardUrgent td:last-child { min-width:190px; }
#tablePendingEvents { min-width:960px; }
#tableCompletedEvents { min-width:1180px; }
.data-table td:first-child { min-width:110px; }
.data-table td:last-child { white-space:normal!important; }
.hub-list-container .data-table { min-width:700px; }
.hub-list-container .data-table th:first-child,.hub-list-container .data-table td:first-child { min-width:150px; }
.hub-list-container .data-table td:last-child { min-width:180px; }
.hub-list-container .status-badge { white-space:nowrap; }
#tableEquipmentTags { min-width:850px; }
#tableColorRanges { min-width:900px; }
#tableDiagCollections { min-width:700px; }
#tableDiagCollections :is(th,td):first-child { min-width:180px; }
#tableDiagCollections :is(th,td):nth-child(2) { min-width:250px; }
#tableDiagCollections :is(th,td):nth-child(n+3) { min-width:80px; white-space:nowrap; }
#tableDiagLogs { min-width:720px; }
#tableDiagLogs td:nth-child(n+3) { overflow-wrap:anywhere; }
.table-scroll-hint { font-size:.875rem; color:var(--text-secondary); margin:.4rem 0; }
.table-responsive:focus-visible,.hub-list-container:focus-visible { outline-offset:2px; }
.data-table .btn { margin:.15rem; }
.completed-cards-container { display:none; flex-direction:column; gap:.7rem; }
.completed-card-details { padding-top:.75rem; margin-top:.5rem; border-top:1px solid var(--border-color); }
.completed-workspace { min-width:0; }
.completed-filters { margin-top:.6rem; border-top:1px solid var(--border-color); }
.completed-filters summary { display:list-item; }
.filter-scope { display:inline; margin-left:.75rem; font-size:.875rem; font-weight:400; color:var(--text-secondary); }
#completedContextPanel,#completedDetailPane { margin-top:1rem; }
.cadastros-category-bar { display:flex; gap:.5rem; flex-wrap:wrap; }
.cadastros-category-btn { display:flex; align-items:center; gap:.5rem; min-height:48px; border:1px solid var(--border-color); border-radius:7px; padding:.6rem .9rem; background:var(--bg-surface); color:var(--text-main); }
.cadastros-category-btn.active { background:var(--bg-surface-active); border-color:var(--border-color-focus); }
.cadastros-unified-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,550px),1fr)); gap:1rem; align-items:start; }
.cadastro-hub-card { display:flex; flex-direction:column; gap:1rem; }
.hub-header { padding-bottom:.75rem; border-bottom:1px solid var(--border-color); }
.hub-title { display:flex; align-items:center; gap:.5rem; font-weight:700; }
.catalog-category { display:grid; grid-template-columns:minmax(0,1.4fr) minmax(0,1fr); gap:1rem; align-items:start; }
.catalog-list { grid-column:1; grid-row:1; }
.catalog-editor { grid-column:2; grid-row:1; min-width:0; }
.catalog-editor>div { flex-wrap:wrap; }
.catalog-editor input[type=text] { flex:1 1 160px; }
.catalog-new { margin-bottom:.7rem; }
.catalog-back { display:none; }
.hub-list-container { max-height:540px; }
#hubCardTags { display:grid; grid-template-columns:minmax(0,1.4fr) minmax(0,1fr); }
#hubCardTags>.hub-header { grid-column:1/-1; }
#hubCardTags>.catalog-list,#hubCardTags>.catalog-editor { grid-row:2; }
.uo-selection-box { display:grid; gap:.3rem; max-height:240px; overflow:auto; border:1px solid var(--border-color); padding:.5rem; border-radius:6px; }
.uo-selection-box label { display:flex; gap:.6rem; min-height:44px; align-items:center; }
.settings-group { padding:0 1rem 1rem; border:1px solid var(--border-color); border-radius:7px; }
.settings-group>.form-group { margin-bottom:.8rem; }
.settings-group>.btn { margin:.2rem; }
.settings-group .form-group>div[style*="display: grid"] { display:flex!important; flex-wrap:wrap; }
.color-workspace { display:grid; grid-template-columns:minmax(0,1.5fr) minmax(0,1fr); gap:1rem; align-items:start; }
.color-workspace>.card-header,.color-workspace>.notice-banner,.color-workspace>div:has(#colorPreviewBar) { grid-column:1/-1; }
.color-workspace>#tableColorRangesWrapper { grid-column:1; }
.range-editor { grid-column:2; grid-row:4/span 2; }
.color-preview-bar { display:flex; flex-wrap:wrap; gap:.3rem; margin-top:.75rem; }
.color-preview-bar>div { min-width:90px; padding:.6rem; flex:1; }
.color-range-cards { display:none; flex-direction:column; gap:.6rem; }
.color-range-card { display:flex; align-items:center; justify-content:space-between; gap:.7rem; }
#rangeLivePreview { border-left:5px solid var(--draft-range-color,var(--border-color-focus)); }
.notice-banner { display:flex; gap:.6rem; background:var(--bg-surface-active); border:1px solid var(--border-color); border-radius:7px; padding:.85rem; font-size:.875rem; color:var(--text-main); }
.notice-banner>p { margin:0; }
.backup-workspace { display:grid; grid-template-columns:minmax(0,2fr) minmax(0,1fr); gap:1rem; }
.backup-workspace>.card-header { grid-column:1/-1; }
.backup-operations { grid-column:1; display:grid; grid-template-columns:1fr 1fr; gap:1rem; align-items:start; }
#backupSelectedFileName { overflow-wrap:anywhere; margin-bottom:.75rem; }
#backupContextPanel { grid-column:2; grid-row:2/span 2; }
.maintenance-panel { grid-column:1/-1; }
.diagnostic-workspace { display:grid; grid-template-columns:minmax(220px,.7fr) minmax(0,1.2fr) minmax(0,1.5fr); gap:1rem; align-items:start; }
.diagnostic-workspace>* { min-width:0; }
.diagnostic-workspace>.card-header { grid-column:1/-1; }
.diagnostic-status { grid-template-columns:1fr; }
.diagnostic-status .metric-value { font-size:1.1rem; }
.diagnostic-logs .data-table { table-layout:fixed; }
.diagnostic-logs pre { white-space:pre-wrap; overflow-wrap:anywhere; }
.stylus-canvas-container { background:var(--bg-app); padding:.75rem; border:1px solid var(--border-color); border-radius:7px; }
.canvas-toolbar { display:flex; justify-content:space-between; gap:.7rem; flex-wrap:wrap; margin-bottom:.7rem; }
.canvas-toolbar label:is([for=stylusColor],[for=stylusWidth],:not([for])) { display:none; }
.canvas-toolbar #selectStylusStrokeWidth { width:auto; }
.stylus-canvas { display:block; width:100%; height:auto; min-height:0; aspect-ratio:1200/440; background:#fff; border-radius:5px; touch-action:none; }
.fullscreen-lousa { position:fixed; inset:0; z-index:1500; margin:0; border-radius:0; overflow:auto; display:flex!important; flex-direction:column; padding:1rem; }
.fullscreen-lousa .stylus-canvas { flex:none; align-self:center; max-width:min(100%,calc((100dvh - 150px)*1200/440)); }
.fullscreen-lousa .canvas-toolbar { position:sticky; top:0; z-index:2; background:var(--bg-app); padding:.5rem 0; }
.modal-overlay { position:fixed; inset:0; z-index:1000; display:none; align-items:center; justify-content:center; padding:1rem; background:rgb(0 0 0/.72); }
.modal-overlay.active { display:flex; }
.modal-box { min-width:0; width:100%; max-width:560px; max-height:calc(100vh - 2rem); max-height:calc(100dvh - 2rem); border:1px solid var(--border-color); border-radius:12px; background:var(--bg-elevated); display:flex; flex-direction:column; box-shadow:0 12px 50px rgb(0 0 0/.35); }
.modal-box.modal-lg { max-width:880px; }
.modal-header { display:flex; align-items:center; justify-content:space-between; gap:.5rem; padding:.85rem 1rem; border-bottom:1px solid var(--border-color); flex:0 0 auto; }
.modal-header h3 { font-size:1.1rem; margin:0; }
.modal-close { display:flex; align-items:center; justify-content:center; min-width:44px; min-height:44px; border:0; border-radius:6px; background:transparent; color:var(--text-main); font-size:1.6rem; }
.modal-body { padding:1rem; min-height:0; overflow:auto; overflow-wrap:anywhere; flex:1 1 auto; }
.modal-footer { display:flex; justify-content:flex-end; gap:.5rem; padding:.8rem 1rem; flex-wrap:wrap; border-top:1px solid var(--border-color); flex:0 0 auto; }
.alarm-modal-box { border:2px solid var(--status-overdue-border); }
.alarm-modal-header { color:var(--status-overdue-text); background:var(--status-overdue-bg); }
.action-sheet-list { display:flex; flex-direction:column; gap:.5rem; }
.action-sheet-destructive { margin-top:.75rem; padding-top:1rem; border-top:1px solid var(--border-color); }
.action-sheet-destructive h4 { font-size:.875rem; color:var(--text-secondary); }
.snooze-quick-btn.active { outline:2px solid var(--border-color-focus); }
.toast-container { position:fixed; right:1rem; bottom:1rem; z-index:1800; width:min(420px,calc(100vw - 2rem)); pointer-events:none; }
.toast { pointer-events:auto; margin-top:.5rem; border:1px solid var(--border-color); border-left:4px solid var(--color-info); border-radius:8px; background:var(--bg-surface); color:var(--text-main); padding:1rem; box-shadow:0 4px 22px #0004; }
.toast.error { border-left-color:var(--color-danger); }
.toast-close { float:right; background:none; border:none; color:var(--text-main); }
.timeline-item { padding:.8rem 0 .8rem 1rem; border-left:2px solid var(--border-color); position:relative; }
.timeline-meta { display:flex; gap:.5rem; justify-content:space-between; font-size:.875rem; color:var(--text-secondary); }
.timeline-title { font-weight:650; }
.timeline-desc { font-size:.875rem; overflow-wrap:anywhere; }
.mobile-drawer-overlay { display:none; position:fixed; inset:0; background:#0009; z-index:900; }
.mobile-drawer-overlay.active { display:block; }
.mobile-drawer { position:fixed; inset:0 auto 0 0; width:min(340px,92vw); height:100vh; height:100dvh; z-index:950; transform:translateX(-105%); visibility:hidden; background:var(--bg-surface); padding:1rem; overflow:auto; }
.mobile-drawer.open { transform:translateX(0); visibility:visible; }
.drawer-header { display:flex; justify-content:space-between; align-items:center; gap:.5rem; border-bottom:1px solid var(--border-color); padding-bottom:.8rem; }
.drawer-nav-items { display:flex; flex-direction:column; gap:.3rem; padding-top:.8rem; }
.drawer-item { width:100%; justify-content:space-between; }
.mobile-bottom-nav { display:none; }
.pulsing-card,.pulsing-badge { animation:alarm-pulse 2s ease-in-out infinite; }
@keyframes alarm-pulse { 50% { box-shadow:0 0 0 2px var(--status-overdue-border); } }
.disable-pulsing .pulsing-card,.disable-pulsing .pulsing-badge { animation:none; }
.disable-highlight .event-card { box-shadow:none; }
.density-compact .card,.density-compact .context-panel,.density-compact .event-card { padding:.8rem; }
.density-compact .data-table td,.density-compact .data-table th { padding:.45rem .6rem; }


/* Operational console: surface hierarchy and interaction tokens. */
:root { --line-subtle:#364a43; --bg-nav:#141e20; --radius-panel:12px; --space-section:1.5rem; }
body.theme-light { --line-subtle:#cddbd3; --bg-nav:#e7eee8; }
body.theme-industrial { --line-subtle:#8a8a8a; --bg-nav:#101010; }
::selection { background:var(--bg-surface-active); color:var(--text-main); }
* { scrollbar-width:thin; scrollbar-color:var(--border-color) var(--bg-app); }
input,textarea { caret-color:var(--border-color-focus); }
a { text-underline-offset:.2em; }
.header-brand>svg { color:var(--color-info); width:30px; height:30px; }
.header-brand h1 { letter-spacing:-.025em; font-weight:700; }
.header-brand .subtitle { font-size:.75rem; margin-top:.15rem; }
.header-console-box { padding-left:1rem; border-left:1px solid var(--line-subtle); }
.clock-display { font-size:.875rem; font-weight:500; color:var(--text-secondary); }
.nav-item svg { width:19px; height:19px; }
.nav-item[data-view=viewCadastros],.nav-item[data-view=viewBackup] { margin-top:1.25rem; }
.nav-item.active svg { color:var(--color-info); }
.nav-item .badge-count { border-radius:5px; font-size:.75rem; }
.btn,.nav-item,.drawer-item,.metric-card,.context-event { transition:background-color var(--transition),border-color var(--transition),color var(--transition); }
.btn:active:not(:disabled) { transform:translateY(1px); }
.btn-secondary { background:var(--bg-surface-hover); }
.btn-outline { border-color:var(--border-color); }
.persistent-banner.backup-banner { background:var(--bg-app); border-color:var(--line-subtle); }
#backupOverdueBanner>div { flex-wrap:nowrap!important; }
#backupOverdueBanner>div>span:first-child { flex:0 0 18px; }
.backup-banner .btn-warning { background:transparent; color:var(--text-main); border-color:var(--border-color); }
.context-panel { background:var(--bg-nav); }
.context-panel h2 { font-size:1rem; letter-spacing:-.015em; }
.context-panel h3 { line-height:1.5; }
.context-panel dd { padding-bottom:.65rem; margin-bottom:.65rem; border-bottom:1px solid var(--line-subtle); }
.context-panel li { border-color:var(--line-subtle); }
.context-panel dt { margin-bottom:.25rem; }
.spotlight-badge { display:flex; gap:.5rem; align-items:center; color:var(--color-info); }
.spotlight-timer { margin-top:.25rem; padding-top:1rem; border-color:var(--line-subtle); }
#spotlightActions { padding-top:.75rem; }
.spotlight-path { line-height:1.6; }
.event-card-footer { border-color:var(--line-subtle); }
.data-table { font-variant-numeric:tabular-nums; }
.table-responsive,.hub-list-container { border-color:var(--line-subtle); border-radius:8px; }
.data-table tbody tr:nth-child(even) { background:color-mix(in srgb,var(--bg-surface-hover) 45%,transparent); }
.data-table tbody tr:hover { background:var(--bg-surface-hover); }
.event-fieldset,.settings-group { border-color:var(--line-subtle); border-radius:10px; padding:1.15rem; }
.event-fieldset legend,.settings-group legend { color:var(--color-info); }
.form-group { gap:.5rem; }
input:not([type=checkbox]):not([type=radio]):focus,select:focus,textarea:focus { border-color:var(--border-color-focus); }
.optional-group { border-top:1px solid var(--line-subtle); padding-top:.3rem; }
.modal-header,.modal-footer { padding:1.1rem 1.25rem; border-color:var(--line-subtle); }
.modal-body { padding:1.25rem; }
.modal-box { border:0; border-radius:14px; box-shadow:0 20px 64px rgb(0 0 0/.35); }
.alarm-modal-box { border:2px solid var(--status-overdue-border); }
.cadastros-category-btn { border-radius:8px; }
.cadastros-category-btn.active { background:var(--bg-surface-active); }
@media (min-width:1400px) and (max-width:1919px) {
 body[data-layout-mode=conventional] #dashboardOverview .dashboard-metrics { grid-template-columns:repeat(7,minmax(0,1fr)); }
 body[data-layout-mode=conventional] .dashboard-metrics .metric-card { flex-direction:column; align-items:flex-start; gap:.45rem; }
 body[data-layout-mode=conventional] .dashboard-metrics .metric-icon { display:none; }
}
@media (hover:hover) {
 .metric-card[data-filter]:hover { background:var(--bg-surface-hover); }
 .btn-header-bell:hover,.modal-close:hover { background:var(--bg-surface-active); }
}
@media (max-width:767px) {
 #backupOverdueBanner { gap:.6rem; }
 #backupOverdueBanner>div { flex:1 1 160px; font-size:.8125rem; }
 #backupOverdueBanner>.btn { flex:0 0 auto; padding:.5rem; font-size:.8125rem; }
 .header-console-box { padding-left:0; border:0; }
 .view-heading { font-size:1.4rem; }
 .nav-item[data-view=viewCadastros],.nav-item[data-view=viewBackup] { margin-top:.5rem; }
 .modal-body { padding:1rem; }
 .modal-header,.modal-footer { padding:.85rem 1rem; }
 .event-fieldset { padding:.85rem; }
 .context-panel { padding:1rem; }
 .mobile-bottom-nav { box-shadow:0 -8px 24px rgb(0 0 0/.12); }
 .bottom-nav-item.active { border-color:transparent; }
}

/* Five tiers. Physical narrow safeguard always takes priority over a forced desktop mode. */
body[data-layout-mode=conventional] #viewDashboard.active { display:grid; grid-template-columns:minmax(0,2fr) minmax(280px,1fr); gap:1rem; }
body[data-layout-mode=conventional] .dashboard-metrics { grid-column:1/-1; grid-row:2; }
body[data-layout-mode=conventional] .dashboard-highlight-grid { grid-column:1/-1; grid-row:3; }
body[data-layout-mode=conventional] #cardDashboardUrgent { grid-column:1; grid-row:4; }
body[data-layout-mode=conventional] #dashboardSelectedDetail { grid-column:2; grid-row:4; }
body[data-layout-mode=conventional] #dashboardContextPanel { grid-column:1/-1; grid-row:5; }
body[data-layout-mode=conventional] #dashboardContextPanel .context-columns { display:grid; grid-template-columns:1fr 1fr; gap:2rem; }
body[data-layout-mode=conventional] .dashboard-metrics { grid-template-columns:repeat(4,minmax(0,1fr)); }
body[data-layout-mode=conventional] .diagnostic-workspace { grid-template-columns:minmax(0,1.1fr) minmax(0,1fr); }
body[data-layout-mode=conventional] .diagnostic-status { grid-column:1/-1; grid-template-columns:repeat(4,minmax(0,1fr)); }
body[data-layout-mode=conventional] .diagnostic-logs { grid-column:2; grid-row:3; }
body:is([data-layout-mode=widescreen],[data-layout-mode=ultrawide]) #viewDashboard.active { display:grid; grid-template-columns:minmax(0,.85fr) minmax(0,2.1fr) minmax(0,.85fr); gap:1rem; align-items:start; }
body:is([data-layout-mode=widescreen],[data-layout-mode=ultrawide]) .dashboard-metrics { grid-column:1/-1; margin:0; }
body:is([data-layout-mode=widescreen],[data-layout-mode=ultrawide]) .dashboard-highlight-grid { grid-column:1; grid-row:2; display:flex; flex-direction:column; }
body:is([data-layout-mode=widescreen],[data-layout-mode=ultrawide]) .dashboard-highlight-grid>* { width:100%; }
body:is([data-layout-mode=widescreen],[data-layout-mode=ultrawide]) #cardDashboardUrgent { grid-column:2; grid-row:2; margin:0; }
body:is([data-layout-mode=widescreen],[data-layout-mode=ultrawide]) #dashboardContextPanel { margin:0; }
body:is([data-layout-mode=widescreen],[data-layout-mode=ultrawide]) #dashboardSelectedDetail { margin:0; }
body[data-layout-mode=widescreen] #dashboardContextStack { grid-column:3; grid-row:2; display:flex; flex-direction:column; gap:1rem; }
body:is([data-layout-mode=widescreen],[data-layout-mode=ultrawide]) #dashboardOverview { display:flex; flex-direction:column; gap:1rem; }
body:is([data-layout-mode=widescreen],[data-layout-mode=ultrawide]) #dashboardOverview .dashboard-metrics { grid-template-columns:repeat(2,minmax(0,1fr)); margin:0; }
body[data-layout-mode=ultrawide] #viewDashboard.active { grid-template-columns:minmax(0,1fr) minmax(0,1.6fr) minmax(0,1fr) minmax(0,1fr); }
body[data-layout-mode=ultrawide] #dashboardSelectedDetail { grid-column:3; grid-row:2; }
body[data-layout-mode=ultrawide] #dashboardContextPanel { grid-column:4; }
body[data-layout-mode=ultrawide] #dashboardOverview { grid-column:4; grid-row:2; }
body[data-layout-mode=ultrawide] #dashboardOverview #dashboardContextPanel { margin:0; }
body[data-layout-mode=ultrawide] #viewDashboard .dashboard-highlight-grid,body[data-layout-mode=ultrawide] #viewDashboard #cardDashboardUrgent,body[data-layout-mode=ultrawide] #viewDashboard #dashboardSelectedDetail { grid-row:2; }
body[data-layout-mode=conventional] #viewNewEvent.active { display:grid; grid-template-columns:minmax(0,2fr) minmax(280px,1fr); gap:1rem; align-items:start; }
body[data-layout-mode=conventional] #viewNewEvent>.card { grid-row:2/span 2; }
body[data-layout-mode=conventional] #viewCadastros.active { display:grid; grid-template-columns:minmax(0,2.5fr) minmax(280px,1fr); gap:1rem; align-items:start; }
body[data-layout-mode=conventional] #viewCadastros>.card { grid-column:1/-1; }
body:is([data-layout-mode=widescreen],[data-layout-mode=ultrawide]) #viewNewEvent.active { display:grid; grid-template-columns:minmax(0,1.65fr) minmax(0,1fr); gap:1rem; align-items:start; }
body:is([data-layout-mode=widescreen],[data-layout-mode=ultrawide]) #viewNewEvent>.card { grid-row:2/span 2; }
body:is([data-layout-mode=widescreen],[data-layout-mode=ultrawide]) #formEvent .fieldset-atividade { grid-column:1; }
body:is([data-layout-mode=widescreen],[data-layout-mode=ultrawide]) #formEvent .fieldset-lousa { grid-column:2; }
body[data-layout-mode=ultrawide] #viewNewEvent.active { grid-template-columns:minmax(0,1.8fr) minmax(0,1fr) minmax(0,1fr); }
body:is([data-layout-mode=widescreen],[data-layout-mode=ultrawide]) .pending-master-detail-grid { grid-template-columns:minmax(0,1.7fr) minmax(0,1fr) minmax(0,.8fr); }
body:is([data-layout-mode=widescreen],[data-layout-mode=ultrawide]) #viewCompletedEvents.active { display:grid; grid-template-columns:minmax(0,2fr) minmax(0,1fr); gap:1rem; }
body:is([data-layout-mode=widescreen],[data-layout-mode=ultrawide]) #viewCompletedEvents>.events-toolbar { grid-column:1/-1; }
body:is([data-layout-mode=widescreen],[data-layout-mode=ultrawide]) .completed-workspace { grid-column:1; grid-row:3/span 3; }
body[data-layout-mode=ultrawide] #viewCompletedEvents.active { grid-template-columns:minmax(0,2.3fr) minmax(0,1fr) minmax(0,1fr); }
body[data-layout-mode=ultrawide] #completedDetailPane { grid-column:3; grid-row:3; }
body:is([data-layout-mode=widescreen],[data-layout-mode=ultrawide]) #viewConfigAlerts.active { display:grid; grid-template-columns:minmax(0,2fr) minmax(0,1fr); gap:1rem; }
body:is([data-layout-mode=widescreen],[data-layout-mode=ultrawide]) #viewConfigAlerts>.notice-banner { grid-column:1/-1; grid-row:2; align-self:start; }
body:is([data-layout-mode=widescreen],[data-layout-mode=ultrawide]) #viewConfigAlerts>.notice-banner ul { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.3rem 2rem; max-width:140ch; }
body:is([data-layout-mode=widescreen],[data-layout-mode=ultrawide]) #viewConfigAlerts>.card { grid-column:1; grid-row:3; }
body:is([data-layout-mode=widescreen],[data-layout-mode=ultrawide]) #settingsPreviewPanel { grid-column:2; grid-row:3; }
body[data-layout-mode=widescreen] #formAlertSettings>.form-grid { grid-template-columns:repeat(2,minmax(0,1fr)); }
body[data-layout-mode=ultrawide] #formAlertSettings>.form-grid { grid-template-columns:repeat(3,minmax(0,1fr)); }
body:is([data-layout-mode=widescreen],[data-layout-mode=ultrawide]) #viewCadastros.active { display:grid; grid-template-columns:minmax(0,2.7fr) minmax(0,1fr); gap:1rem; }
body:is([data-layout-mode=widescreen],[data-layout-mode=ultrawide]) #viewCadastros>.card { grid-column:1/-1; }
body[data-layout-mode=ultrawide] .color-workspace { grid-template-columns:minmax(0,1.7fr) minmax(0,1fr) minmax(0,1fr); }
body[data-layout-mode=ultrawide] #rangeLivePreview { grid-column:3; grid-row:4; }
body:is([data-layout-mode=mobile],[data-layout-mode=tablet]) .app-nav { display:none; }
body:is([data-layout-mode=mobile],[data-layout-mode=tablet]) .btn-hamburger { display:inline-flex; }
body:is([data-layout-mode=mobile],[data-layout-mode=tablet]) .app-main { margin-left:0; width:100%; }
body:is([data-layout-mode=mobile],[data-layout-mode=tablet]) .persistent-banner { margin-left:0; }
body:is([data-layout-mode=mobile],[data-layout-mode=tablet]) #btnQuickAddEvent,body:is([data-layout-mode=mobile],[data-layout-mode=tablet]) #btnControllerBadge { display:none; }
body[data-layout-mode=tablet] .app-header { display:grid; grid-template-columns:minmax(0,1fr) auto; }
body[data-layout-mode=tablet] .header-left { grid-column:1; grid-row:1; }
body[data-layout-mode=tablet] .header-actions { grid-column:2; grid-row:1; }
body[data-layout-mode=tablet] .header-status-bar { grid-column:1/-1; grid-row:2; }
body[data-layout-mode=tablet] .dashboard-metrics { grid-template-columns:repeat(4,minmax(0,1fr)); }
body[data-layout-mode=tablet] #viewDashboard.active { display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1fr); gap:1rem; }
body[data-layout-mode=tablet] #viewDashboard .dashboard-metrics { grid-row:2; grid-column:1/-1; margin:0; }
body[data-layout-mode=tablet] #viewDashboard .dashboard-highlight-grid { grid-row:3; grid-column:1/-1; }
body[data-layout-mode=tablet] #cardDashboardUrgent { grid-row:4; grid-column:1/-1; }
body[data-layout-mode=tablet] .dashboard-highlight-grid { grid-template-columns:minmax(0,1.35fr) minmax(0,1fr); }
body[data-layout-mode=tablet] .app-main { padding:1rem; }
body[data-layout-mode=tablet] .form-sticky-submit-bar { position:sticky; }
body[data-layout-mode=tablet] .header-brand .subtitle { display:none; }
body[data-layout-mode=tablet] .header-console-box label { display:none; }
body[data-layout-mode=tablet] .diagnostic-workspace { grid-template-columns:minmax(0,1fr) minmax(0,1fr); }
body[data-layout-mode=tablet] .diagnostic-logs { grid-column:1/-1; }
body[data-layout-mode=tablet] .backup-workspace { grid-template-columns:1fr; }
body[data-layout-mode=tablet] #backupContextPanel { grid-column:1; grid-row:auto; }
body[data-layout-mode=tablet] .pending-master-detail-grid { grid-template-columns:minmax(0,1.2fr) minmax(0,1fr); }
body:is([data-layout-mode=mobile],[data-layout-mode=tablet]) input:not([type=checkbox]):not([type=radio]),body:is([data-layout-mode=mobile],[data-layout-mode=tablet]) select,body:is([data-layout-mode=mobile],[data-layout-mode=tablet]) textarea { min-height:48px; }
body:is([data-layout-mode=mobile],[data-layout-mode=tablet]) .btn-primary,body:is([data-layout-mode=mobile],[data-layout-mode=tablet]) .btn-success { min-height:48px; }
body:is([data-layout-mode=mobile],[data-layout-mode=tablet]) .cadastro-hub-card[data-cad-hidden=true] { display:none; }
@media (max-width:1199px) {
 .header-viewmode-box { display:none; } .header-brand .subtitle { display:none; }
 .app-header { flex-wrap:wrap; }
 .header-status-bar { flex-basis:100%; order:3; }
}
/* Landscape tablet has enough usable width for an 80px rail and two working regions. */
@media (min-width:1000px) and (orientation:landscape) {
 body[data-layout-mode=tablet] { --sidebar-width:80px; }
 body[data-layout-mode=tablet] .app-nav { display:flex; padding:.6rem .5rem; }
 body[data-layout-mode=tablet] .app-nav .nav-item { position:relative; min-height:52px; justify-content:center; padding:.6rem; }
 body[data-layout-mode=tablet] .app-nav .nav-item>svg { width:22px; height:22px; }
 body[data-layout-mode=tablet] .app-nav .nav-item>span:not(.badge-count) { position:absolute; width:1px; height:1px; padding:0; margin:-1px; clip-path:inset(50%); overflow:hidden; white-space:nowrap; }
 body[data-layout-mode=tablet] .app-nav .badge-count { position:absolute; top:0; right:0; min-width:18px; padding:0 .25rem; font-size:.75rem; }
 body[data-layout-mode=tablet] .app-main { margin-left:var(--sidebar-width); width:calc(100% - var(--sidebar-width)); }
 body[data-layout-mode=tablet] .persistent-banner { margin-left:var(--sidebar-width); }
 body[data-layout-mode=tablet] #formEvent .event-form-sections { grid-template-columns:repeat(2,minmax(0,1fr)); align-items:start; }
 body[data-layout-mode=tablet] #formEvent .fieldset-atividade { grid-column:1; grid-row:2; }
 body[data-layout-mode=tablet] #formEvent .fieldset-lousa { grid-column:2; grid-row:2; }
}
@media (min-width:768px) and (max-width:1199px) {
 body:is([data-layout-mode=conventional],[data-layout-mode=widescreen],[data-layout-mode=ultrawide]) #viewDashboard.active { display:block; }
 body:is([data-layout-mode=conventional],[data-layout-mode=widescreen],[data-layout-mode=ultrawide]) #viewDashboard>* { margin-bottom:1rem; }
 body:is([data-layout-mode=conventional],[data-layout-mode=widescreen],[data-layout-mode=ultrawide]) #dashboardOverview { display:contents; }
 body:is([data-layout-mode=conventional],[data-layout-mode=widescreen],[data-layout-mode=ultrawide]) #dashboardContextStack { display:contents; }
 body:is([data-layout-mode=conventional],[data-layout-mode=widescreen],[data-layout-mode=ultrawide]) #dashboardOverview .dashboard-metrics { grid-template-columns:repeat(2,minmax(0,1fr)); }
}
@media (min-width:768px) and (max-width:1000px) { .header-brand h1 { font-size:.9rem; } .event-form-sections { grid-template-columns:1fr; } }

body:is([data-layout-mode=mobile],.layout-narrow) { --sidebar-width:0px; }
body:is([data-layout-mode=mobile],.layout-narrow) .app-header { padding:.5rem .65rem; gap:.4rem; display:grid; grid-template-columns:minmax(0,1fr) auto; }
body:is([data-layout-mode=mobile],.layout-narrow) .app-header { padding-top:max(.5rem,env(safe-area-inset-top)); }
body:is([data-layout-mode=mobile],.layout-narrow) .app-header { padding-left:max(.65rem,env(safe-area-inset-left)); padding-right:max(.65rem,env(safe-area-inset-right)); }
body:is([data-layout-mode=mobile],.layout-narrow) .header-left { display:grid; grid-template-columns:44px minmax(0,1fr); gap:.35rem .6rem; }
body:is([data-layout-mode=mobile],.layout-narrow) .header-brand h1 { font-size:.9rem; white-space:normal; }
body:is([data-layout-mode=mobile],.layout-narrow) .header-brand>svg,body:is([data-layout-mode=mobile],.layout-narrow) .subtitle { display:none; }
body:is([data-layout-mode=mobile],.layout-narrow) .header-console-box { grid-column:1/-1; display:flex; }
body:is([data-layout-mode=mobile],.layout-narrow) .header-console-box label { font-size:.875rem; }
body:is([data-layout-mode=mobile],.layout-narrow) #headerActiveConsole { width:100%; flex:1; min-height:44px; }
body:is([data-layout-mode=mobile],.layout-narrow) .header-actions { gap:.3rem; flex-direction:column; }
body:is([data-layout-mode=mobile],.layout-narrow) .header-left { grid-column:1; grid-row:1; }
body:is([data-layout-mode=mobile],.layout-narrow) .header-actions { grid-column:2; grid-row:1; }
body:is([data-layout-mode=mobile],.layout-narrow) .header-status-bar { display:flex; grid-column:1/-1; grid-row:2; gap:.35rem; }
body:is([data-layout-mode=mobile],.layout-narrow) .clock-display { font-size:.875rem; }
body:is([data-layout-mode=mobile],.layout-narrow) .header-viewmode-box,body:is([data-layout-mode=mobile],.layout-narrow) #btnControllerBadge,body:is([data-layout-mode=mobile],.layout-narrow) #btnQuickAddEvent,body:is([data-layout-mode=mobile],.layout-narrow) #btnToggleTheme,body:is([data-layout-mode=mobile],.layout-narrow) .app-nav { display:none; }
body:is([data-layout-mode=mobile],.layout-narrow) .event-action-secondary { display:none; }
body:is([data-layout-mode=mobile],.layout-narrow) .btn-hamburger { display:inline-flex; }
body:is([data-layout-mode=mobile],.layout-narrow) .app-main { margin:0; width:100%; padding:1rem .65rem calc(90px + env(safe-area-inset-bottom)); }
body:is([data-layout-mode=mobile],.layout-narrow) .view-section.active { display:flex!important; flex-direction:column; gap:.85rem; }
body:is([data-layout-mode=mobile],.layout-narrow) .view-section>* { width:100%; }
body:is([data-layout-mode=mobile],.layout-narrow) .dashboard-highlight-grid { display:flex; flex-direction:column; gap:.85rem; order:1; }
body:is([data-layout-mode=mobile],.layout-narrow) .view-heading { order:-1; }
body:is([data-layout-mode=mobile],.layout-narrow) .dashboard-metrics { grid-template-columns:repeat(2,minmax(0,1fr)); gap:.5rem; order:3; margin:0; }
body:is([data-layout-mode=mobile],.layout-narrow) #dashboardOverview { display:contents; }
body:is([data-layout-mode=mobile],.layout-narrow) #cardDashboardUrgent { order:2; }
body:is([data-layout-mode=mobile],.layout-narrow) #dashboardContextPanel,body:is([data-layout-mode=mobile],.layout-narrow) #dashboardSelectedDetail { order:4; }
body:is([data-layout-mode=mobile],.layout-narrow) :is(#dashboardSelectedDetail,#dashboardContextPanel,#pendingContextPanel,#completedDetailPane,#eventDraftSummary,#eventRelatedList,#settingsPreviewPanel) { display:none; }
body:is([data-layout-mode=mobile],.layout-narrow) .metric-card { padding:.7rem; }
body:is([data-layout-mode=mobile],.layout-narrow) .metric-icon { display:none; }
body:is([data-layout-mode=mobile],.layout-narrow) .spotlight-card { padding:1rem; }
body:is([data-layout-mode=mobile],.layout-narrow) .time-left { font-size:1.8rem; }
body:is([data-layout-mode=mobile],.layout-narrow) .persistent-banner { margin:0; flex-wrap:wrap; padding:.5rem .65rem; }
body:is([data-layout-mode=mobile],.layout-narrow) .alarm-banner>div:first-child { flex:1 1 100%; }
body:is([data-layout-mode=mobile],.layout-narrow) #tableDashboardUrgent { display:none; }
body:is([data-layout-mode=mobile],.layout-narrow) #cardDashboardUrgent>.table-responsive { display:none; }
body:is([data-layout-mode=mobile],.layout-narrow) .dashboard-urgent-cards { display:flex; flex-direction:column; gap:.6rem; }
body:is([data-layout-mode=mobile],.layout-narrow) .pending-master-detail-grid,body:is([data-layout-mode=mobile],.layout-narrow) .event-form-sections,body:is([data-layout-mode=mobile],.layout-narrow) .event-fieldset { grid-template-columns:1fr; }
body:is([data-layout-mode=mobile],.layout-narrow) .pending-detail-pane { display:none; }
body:is([data-layout-mode=mobile],.layout-narrow) .events-container-cards { grid-template-columns:1fr; }
body:is([data-layout-mode=mobile],.layout-narrow) .events-toolbar,body:is([data-layout-mode=mobile],.layout-narrow) .card,body:is([data-layout-mode=mobile],.layout-narrow) .cadastro-hub-card { padding:.85rem; }
body:is([data-layout-mode=mobile],.layout-narrow) .form-grid { grid-template-columns:1fr; }
body:is([data-layout-mode=mobile],.layout-narrow) .span-2 { grid-column:auto; }
body:is([data-layout-mode=mobile],.layout-narrow) .form-sticky-submit-bar { bottom:calc(72px + env(safe-area-inset-bottom)); padding:.5rem 0; position:sticky; }
body:is([data-layout-mode=mobile],.layout-narrow) .form-sticky-submit-bar>div { width:100%; }
body:is([data-layout-mode=mobile],.layout-narrow) .form-sticky-submit-bar .btn { flex:1 1 40%; }
body:is([data-layout-mode=mobile],.layout-narrow) .mobile-bottom-nav { position:fixed; bottom:0; left:0; right:0; z-index:110; display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); align-items:center; padding:.35rem max(.35rem,env(safe-area-inset-right)) calc(.35rem + env(safe-area-inset-bottom)) max(.35rem,env(safe-area-inset-left)); background:var(--bg-surface); border-top:1px solid var(--border-color); }
.bottom-nav-item,.bottom-nav-fab { position:relative; min-height:54px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:.25rem; background:transparent; border:1px solid transparent; border-radius:7px; color:var(--text-secondary); font-size:.75rem; }
.bottom-nav-item.active { color:var(--text-main); border-color:var(--border-color-focus); background:var(--bg-surface-active); }
.bottom-nav-fab { background:var(--color-primary); color:var(--primary-text); min-height:52px; margin:0 .3rem; }
.bottom-nav-badge { position:absolute; top:-4px; right:0; font-size:.7rem; padding:0 .25rem; background:var(--color-danger); color:#fff; }
body:is([data-layout-mode=mobile],.layout-narrow) #filterDrawer.active-sheet { display:grid!important; position:fixed; inset:auto 0 0; max-height:calc(100dvh - 16px); overflow:auto; z-index:1050; padding:1rem; margin:0; border:1px solid var(--border-color); border-radius:12px 12px 0 0; box-shadow:0 -10px 0 100vmax #0009; background:var(--bg-surface); grid-template-columns:1fr; }
body:is([data-layout-mode=mobile],.layout-narrow) .color-workspace,body:is([data-layout-mode=mobile],.layout-narrow) .backup-workspace,body:is([data-layout-mode=mobile],.layout-narrow) .backup-operations,body:is([data-layout-mode=mobile],.layout-narrow) .diagnostic-workspace { display:flex; flex-direction:column; gap:1rem; }
body:is([data-layout-mode=mobile],.layout-narrow) :is(.color-workspace,.backup-workspace,.backup-operations,.diagnostic-workspace)>* { width:100%; }
body:is([data-layout-mode=mobile],.layout-narrow) #tableColorRangesWrapper { display:none; }
body:is([data-layout-mode=mobile],.layout-narrow) .color-range-cards { display:flex; }
body:is([data-layout-mode=mobile],.layout-narrow) .cadastros-unified-grid { display:block; }
body:is([data-layout-mode=mobile],.layout-narrow) .cadastro-hub-card { margin-bottom:1rem; }
body:is([data-layout-mode=mobile],.layout-narrow) .catalog-category,body:is([data-layout-mode=mobile],.layout-narrow) #hubCardTags { display:flex; flex-direction:column; }
body:is([data-layout-mode=mobile],.layout-narrow) .catalog-category>* { width:100%; }
body:is([data-layout-mode=mobile],.layout-narrow) .catalog-list { order:0; }
body:is([data-layout-mode=mobile],.layout-narrow) .catalog-editor { order:1; }
body:is([data-layout-mode=mobile],.layout-narrow) .catalog-back { display:inline-flex; margin-bottom:.75rem; }
body:is([data-layout-mode=mobile],.layout-narrow) .catalog-category[data-editor-open=false]>.catalog-editor { display:none; }
body:is([data-layout-mode=mobile],.layout-narrow) .catalog-category[data-editor-open=true]>.catalog-list { display:none; }
body:is([data-layout-mode=mobile],.layout-narrow) .cadastros-category-bar { display:grid; grid-template-columns:1fr 1fr; }
body:is([data-layout-mode=mobile],.layout-narrow) .cadastros-category-btn { justify-content:space-between; }
body:is([data-layout-mode=mobile],.layout-narrow) .modal-overlay { padding:.5rem; }
body:is([data-layout-mode=mobile],.layout-narrow) .modal-box { max-height:calc(100dvh - 1rem); }
body:is([data-layout-mode=mobile],.layout-narrow) #modalImportSummary { align-items:flex-end; }
body:is([data-layout-mode=mobile],.layout-narrow) #modalImportSummary .modal-box { border-radius:12px 12px 0 0; }
body:is([data-layout-mode=mobile],.layout-narrow) .modal-footer .btn { flex:1 1 40%; }
body:is([data-layout-mode=mobile],.layout-narrow) input:not([type=checkbox]):not([type=radio]),body:is([data-layout-mode=mobile],.layout-narrow) select,body:is([data-layout-mode=mobile],.layout-narrow) textarea { min-height:48px; font-size:1rem; }
body:is([data-layout-mode=mobile],.layout-narrow) .btn-primary,body:is([data-layout-mode=mobile],.layout-narrow) .btn-success { min-height:48px; }
.keyboard-open .mobile-bottom-nav { display:none!important; }
.keyboard-open .form-sticky-submit-bar { position:static; }
@media (prefers-reduced-motion:reduce) { *,*::before,*::after { animation-duration:0s!important; transition-duration:0s!important; scroll-behavior:auto!important; } }
@media print { .app-header,.app-nav,.mobile-bottom-nav,.persistent-banner { display:none!important; } .app-main { margin:0; width:100%; } }

"""
