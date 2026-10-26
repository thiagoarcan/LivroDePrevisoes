# -*- coding: utf-8 -*-
HTML_CONTENT = """
<a class="skip-link" href="#mainContent">
 Ir para conteúdo
</a>
<!-- Lucide Waypoints and TriangleAlert icon license:
ISC License

Copyright (c) 2026 Lucide Icons and Contributors

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

---

The following Lucide icons are derived from the Feather project:

airplay, alert-circle, alert-octagon, alert-triangle, aperture, arrow-down-circle, arrow-down-left, arrow-down-right, arrow-down, arrow-left-circle, arrow-left, arrow-right-circle, arrow-right, arrow-up-circle, arrow-up-left, arrow-up-right, arrow-up, at-sign, calendar, cast, check, chevron-down, chevron-left, chevron-right, chevron-up, chevrons-down, chevrons-left, chevrons-right, chevrons-up, circle, clipboard, clock, code, columns, command, compass, corner-down-left, corner-down-right, corner-left-down, corner-left-up, corner-right-down, corner-right-up, corner-up-left, corner-up-right, crosshair, database, divide-circle, divide-square, dollar-sign, download, external-link, feather, frown, hash, headphones, help-circle, info, italic, key, layout, life-buoy, link-2, link, loader, lock, log-in, log-out, maximize, meh, minimize, minimize-2, minus-circle, minus-square, minus, monitor, moon, more-horizontal, more-vertical, move, music, navigation-2, navigation, octagon, pause-circle, percent, plus-circle, plus-square, plus, power, radio, rss, search, server, share, shopping-bag, sidebar, smartphone, smile, square, table-2, tablet, target, terminal, trash-2, trash, triangle, tv, type, upload, x-circle, x-octagon, x-square, x, zoom-in, zoom-out

The MIT License (MIT) (for the icons listed above)

Copyright (c) 2013-present Cole Bemis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

-->
<!-- Header Bar -->
<header class="app-header">
 <div class="header-left">
  <button aria-label="Abrir Menu" class="btn-hamburger" id="btnToggleMobileMenu" title="Abrir Menu de Navegação" type="button">
   <svg aria-hidden="true" fill="none" focusable="false" height="20" stroke="currentColor" stroke-width="2.5" viewbox="0 0 24 24" width="20">
    <line x1="3" x2="21" y1="12" y2="12">
    </line>
    <line x1="3" x2="21" y1="6" y2="6">
    </line>
    <line x1="3" x2="21" y1="18" y2="18">
    </line>
   </svg>
  </button>
  <div class="header-brand">
   <svg aria-hidden="true" focusable="false" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m10.586 5.414-5.172 5.172"/><path d="m18.586 13.414-5.172 5.172"/><path d="M6 12h12"/><circle cx="12" cy="20" r="2"/><circle cx="12" cy="4" r="2"/><circle cx="20" cy="12" r="2"/><circle cx="4" cy="12" r="2"/></svg>
   <div>
    <h1>
     Caderno de Previsões
    </h1>
    <div class="subtitle">
     Dutos • Sala de Controle
    </div>
   </div>
  </div>
  <!-- Active Console Selector in Header (Chosen once, persists across views and forms) -->
  <div class="header-console-box" title="Console selecionado. Ele permanece ativo para novos eventos sem necessidade de preenchimento repetido.">
   <label for="headerActiveConsole">
    Console ativo:
   </label>
   <select aria-label="Console Operacional Ativo" class="header-console-select" id="headerActiveConsole">
    <!-- Dynamically populated with consoles -->
   </select>
  </div>
 </div>
 <!-- Status Bar with Clock & Indicators -->
 <div class="header-status-bar">
  <div class="clock-display" id="liveClock" title="Horário Oficial da Operação">
   --:--:--
  </div>
  <button class="status-pill warning" id="chipHeaderAudioWarning" style="display: none" title="Toque para iniciar e desbloquear o áudio de alarmes" type="button">
   <svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg> Áudio não iniciado
  </button>
  <span class="status-pill ok" id="pillDB" title="Estado do IndexedDB">
   <span class="indicator-dot">
    •
   </span>
   DB: Pronto
  </span>
  <button class="status-pill warning" id="pillAudio" title="Clique para ativar o áudio no navegador" type="button">
   <span class="indicator-dot">
    •
   </span>
   Áudio: Iniciar
  </button>
  <button class="status-pill" id="pillNotif" title="Permissão de Notificações do Navegador" type="button">
   <span class="indicator-dot">
    •
   </span>
   Notif: Pendente
  </button>
  <!-- Prominent Test Notification Button in Header -->
  <button class="status-pill warning" id="btnHeaderTestNotif" title="Disparar teste de notificação do navegador" type="button">
   <svg aria-hidden="true" fill="none" focusable="false" height="12" stroke="currentColor" stroke-width="2.5" viewbox="0 0 24 24" width="12">
    <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9">
    </path>
    <path d="M13.73 21a2 2 0 0 1-3.46 0">
    </path>
   </svg>
   <span>
    Testar Notificação
   </span>
  </button>
  <span class="status-pill" id="pillBackup" title="Data do último backup">
   <span class="indicator-dot">
    •
   </span>
   Backup: Nunca
  </span>
 </div>
 <!-- Header Actions -->
 <div class="header-actions">
  <!-- Layout / ViewMode Quick Selector (Section 1.2) -->
  <div class="header-viewmode-box" title="Escolher modo de visualização (Automático ou Manual)">
   <svg aria-hidden="true" fill="none" focusable="false" height="14" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="14">
    <rect height="18" rx="2" width="18" x="3" y="3">
    </rect>
    <line x1="3" x2="21" y1="9" y2="9">
    </line>
    <line x1="9" x2="9" y1="21" y2="9">
    </line>
   </svg>
   <label for="selectHeaderViewMode">
    Visualização:
   </label>
   <select aria-label="Visualização da Interface" class="header-viewmode-select" id="selectHeaderViewMode">
    <option value="auto">
     Automática
    </option>
    <option value="compact">
     Compacta
    </option>
    <option value="mobile">
     Celular
    </option>
    <option value="tablet">
     Tablet
    </option>
    <option value="conventional">
     Monitor Convencional
    </option>
    <option value="widescreen">
     Widescreen
    </option>
    <option value="ultrawide">
     Ultrawide
    </option>
   </select>
  </div>
  <!-- Alarm Bell Button with Badge (Section 2.2) -->
  <button aria-label="Alertas Ativos" class="btn-header-bell" id="btnHeaderAlarmBell" title="Alertas e Alarmes Operacionais Ativos" type="button">
   <svg aria-hidden="true" fill="none" focusable="false" height="18" stroke="currentColor" stroke-width="2.2" viewbox="0 0 24 24" width="18">
    <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9">
    </path>
    <path d="M13.73 21a2 2 0 0 1-3.46 0">
    </path>
   </svg>
   <span class="bell-badge" id="headerAlarmBadge" style="display: none">
    0
   </span>
  </button>
  <!-- App Status Button -->
  <button aria-label="Status da Aplicação" class="btn btn-outline btn-icon" id="btnHeaderAppStatus" title="Status da Aplicação (Banco, Áudio, Notificações e Backup)" type="button">
   <svg aria-hidden="true" fill="none" focusable="false" height="16" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="16">
    <circle cx="12" cy="12" r="10">
    </circle>
    <line x1="12" x2="12" y1="16" y2="12">
    </line>
    <line x1="12" x2="12.01" y1="8" y2="8">
    </line>
   </svg>
  </button>
  <button class="btn btn-secondary btn-sm" id="btnControllerBadge" title="Alterar identificação do controlador" type="button">
   <svg aria-hidden="true" fill="none" focusable="false" height="14" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="14">
    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2">
    </path>
    <circle cx="12" cy="7" r="4">
    </circle>
   </svg>
   <span id="headerUserName">
    Usuário local
   </span>
  </button>
  <button aria-label="Alternar Tema" class="btn btn-outline btn-icon" id="btnToggleTheme" title="Alternar Tema (Escuro / Claro / Industrial Alto Contraste)" type="button">
   <svg aria-hidden="true" fill="none" focusable="false" height="16" id="themeIconSun" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="16">
    <circle cx="12" cy="12" r="5">
    </circle>
    <line x1="12" x2="12" y1="1" y2="3">
    </line>
    <line x1="12" x2="12" y1="21" y2="23">
    </line>
    <line x1="4.22" x2="5.64" y1="4.22" y2="5.64">
    </line>
    <line x1="18.36" x2="19.78" y1="18.36" y2="19.78">
    </line>
    <line x1="1" x2="3" y1="12" y2="12">
    </line>
    <line x1="21" x2="23" y1="12" y2="12">
    </line>
    <line x1="4.22" x2="5.64" y1="19.78" y2="18.36">
    </line>
    <line x1="18.36" x2="19.78" y1="5.64" y2="4.22">
    </line>
   </svg>
  </button>
  <button class="btn btn-primary btn-sm" id="btnQuickAddEvent" title="Adicionar nova previsão operacional" type="button">
   <svg aria-hidden="true" fill="none" focusable="false" height="15" stroke="currentColor" stroke-width="2.5" viewbox="0 0 24 24" width="15">
    <line x1="12" x2="12" y1="5" y2="19">
    </line>
    <line x1="5" x2="19" y1="12" y2="12">
    </line>
   </svg>
   <span>
    Nova Previsão
   </span>
  </button>
 </div>
</header>
<!-- Persistent Banners (Section 1.3, 3.2, 23) -->
<div class="persistent-banner alarm-banner" id="mobileActiveAlarmsBanner" role="alert">
 <div style="display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap">
  <svg aria-hidden="true" fill="none" focusable="false" height="20" stroke="currentColor" stroke-width="2.5" viewbox="0 0 24 24" width="20">
   <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z">
   </path>
   <line x1="12" x2="12" y1="9" y2="13">
   </line>
   <line x1="12" x2="12.01" y1="17" y2="17">
   </line>
  </svg>
  <span id="bannerActiveAlarmsText">
   2 alarmes aguardando ação
  </span>
 </div>
 <div style="display: flex; gap: 0.5rem; flex-wrap: wrap">
  <button class="btn btn-secondary btn-sm" id="btnBannerViewAlarms" type="button">
   Ver alarmes
  </button>
  <button class="btn btn-warning btn-sm" id="btnBannerAckAll" type="button">
   Reconhecer
  </button>
 </div>
</div>
<div class="persistent-banner backup-banner" id="backupOverdueBanner">
 <div style="display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap">
  <span>
   <svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>
  </span>
  <span id="bannerBackupOverdueText">
   Último backup realizado há mais de 7 dias.
  </span>
 </div>
 <button class="btn btn-warning btn-sm" id="btnBannerBackupNow" type="button">
  Abrir backup
 </button>
</div>
<div class="persistent-banner layout-banner" id="viewModeWarningBanner">
 <div style="display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap">
  <span>
   ⓘ
  </span>
  <span id="bannerViewModeText">
   O modo de visualização manual escolhido excede a largura ideal desta tela.
  </span>
 </div>
 <button class="btn btn-primary btn-sm" id="btnBannerResetAuto" type="button">
  Voltar para Automático
 </button>
</div>
<!-- Mobile / Tablet Drawer Menu (Matches Wireframe Celular - 6. Menu Drawer) -->
<div class="mobile-drawer-overlay" id="mobileDrawerOverlay">
</div>
<div class="mobile-drawer" id="appMobileDrawer">
 <div id="mobileDrawer" style="display: none">
 </div>
 <div class="drawer-header">
  <div style="font-weight: 700; display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap">
   <svg aria-hidden="true" fill="none" focusable="false" height="20" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="20">
    <circle cx="12" cy="12" r="10">
    </circle>
    <polyline points="12 6 12 12 16 14">
    </polyline>
   </svg>
   <div>
    <div>
     Previsões em Dutos
    </div>
    <div style="color: var(--text-muted); font-weight: 600">
     <span data-app-version></span> • Operação Offline
    </div>
   </div>
  </div>
  <button aria-label="Fechar Menu" class="modal-close" id="btnCloseMobileDrawer" type="button">
   ×
  </button>
 </div>
 <div class="drawer-nav-items">
  <button class="mobile-nav-link drawer-item active" data-view="viewDashboard" type="button">
   <span>
    🏠 Painel Principal
   </span>
   <span class="badge-count" id="badgePendingDrawer">
    0
   </span>
  </button>
  <button class="mobile-nav-link drawer-item" data-view="viewPendingEvents" type="button">
   <span>
    🕒 Eventos Pendentes
   </span>
   <span class="badge-count" id="badgePendingNavCountDrawer">
    0
   </span>
  </button>
  <button class="mobile-nav-link drawer-item" data-view="viewNewEvent" type="button">
   <span>
    ➕ Nova Previsão
   </span>
  </button>
  <button class="mobile-nav-link drawer-item" data-view="viewCompletedEvents" type="button">
   <span>
    ✅ Eventos Concluídos
   </span>
  </button>
  <button class="mobile-nav-link drawer-item" data-view="viewCadastros" type="button">
   <span>
    🗂 Cadastros Operacionais
   </span>
  </button>
  <button class="mobile-nav-link drawer-item" data-view="viewConfigAlerts" type="button">
   <span>
    🔔 Configurações de Alertas
   </span>
  </button>
  <button class="mobile-nav-link drawer-item" data-view="viewConfigColors" type="button">
   <span>
    🎨 Configurações de Cores
   </span>
  </button>
  <button class="mobile-nav-link drawer-item" data-view="viewBackup" type="button">
   <span>
    💾 Backup e Dados
   </span>
  </button>
  <button class="mobile-nav-link drawer-item" data-view="viewDiagnostic" type="button">
   <span>
    📊 Diagnóstico Técnico
   </span>
  </button>
  <div style="border-top: 1px solid var(--border-color); margin: 0.4rem 0; padding-top: 0.4rem">
   <button class="drawer-item" id="btnDrawerAppStatus" style="width: 100%" type="button">
    <span>
     ⓘ Status da Aplicação
    </span>
   </button>
   <button class="drawer-item" id="btnDrawerTheme" style="width: 100%" type="button">
    <span id="labelDrawerTheme">
     🌙 Tema (Escuro)
    </span>
   </button>
   <button class="drawer-item" id="btnDrawerUser" style="width: 100%" type="button">
    <span id="labelDrawerUser">
     👤 Usuário: Operador
    </span>
   </button>
   <div style="padding: 0.4rem 0.9rem">
    <label for="selectDrawerViewMode" style="color: var(--text-muted); margin-bottom: 0.25rem">
     Modo de Visualização:
    </label>
    <select id="selectDrawerViewMode" style="padding: 0.25rem 0.5rem">
     <option value="auto">
      Automática
     </option>
     <option value="compact">
      Compacta
     </option>
     <option value="mobile">
      Celular
     </option>
     <option value="tablet">
      Tablet
     </option>
     <option value="conventional">
      Monitor Convencional
     </option>
     <option value="widescreen">
      Widescreen
     </option>
     <option value="ultrawide">
      Ultrawide
     </option>
    </select>
   </div>
   <button class="drawer-item" id="btnDrawerCloseBottom" style="width: 100%; color: var(--text-muted)" type="button">
    <span>
     ← Sair / Fechar Menu
    </span>
   </button>
  </div>
 </div>
</div>
<!-- Desktop Navigation Bar -->
<nav aria-label="Navegação principal" class="app-nav">
 <button class="nav-item active" data-view="viewDashboard" type="button">
  <svg aria-hidden="true" fill="none" focusable="false" height="16" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="16">
   <rect height="9" width="7" x="3" y="3">
   </rect>
   <rect height="5" width="7" x="14" y="3">
   </rect>
   <rect height="9" width="7" x="14" y="12">
   </rect>
   <rect height="5" width="7" x="3" y="16">
   </rect>
  </svg>
  <span>
   Painel
  </span>
  <span class="badge-count" id="badgePendingCount">
   0
  </span>
 </button>
 <button class="nav-item" data-view="viewNewEvent" type="button">
  <svg aria-hidden="true" fill="none" focusable="false" height="16" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="16">
   <circle cx="12" cy="12" r="10">
   </circle>
   <line x1="12" x2="12" y1="8" y2="16">
   </line>
   <line x1="8" x2="16" y1="12" y2="12">
   </line>
  </svg>
  <span id="navNewEventLabel">
   Novo Evento
  </span>
 </button>
 <button class="nav-item" data-view="viewPendingEvents" type="button">
  <svg aria-hidden="true" fill="none" focusable="false" height="16" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="16">
   <circle cx="12" cy="12" r="10">
   </circle>
   <polyline points="12 6 12 12 16 14">
   </polyline>
  </svg>
  <span>
   Eventos Pendentes
  </span>
  <span class="badge-count" id="badgePendingNavCount">
   0
  </span>
 </button>
 <button class="nav-item" data-view="viewCompletedEvents" type="button">
  <svg aria-hidden="true" fill="none" focusable="false" height="16" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="16">
   <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14">
   </path>
   <polyline points="22 4 12 14.01 9 11.01">
   </polyline>
  </svg>
  <span>
   Eventos Concluídos
  </span>
 </button>
 <button class="nav-item" data-view="viewCadastros" type="button">
  <svg aria-hidden="true" fill="none" focusable="false" height="16" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="16">
   <polygon points="12 2 2 7 12 12 22 7 12 2">
   </polygon>
   <polyline points="2 17 12 22 22 17">
   </polyline>
   <polyline points="2 12 12 17 22 12">
   </polyline>
  </svg>
  <span>
   Cadastros Operacionais
  </span>
 </button>
 <button class="nav-item" data-view="viewConfigAlerts" type="button">
  <svg aria-hidden="true" fill="none" focusable="false" height="16" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="16">
   <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9">
   </path>
   <path d="M13.73 21a2 2 0 0 1-3.46 0">
   </path>
  </svg>
  <span>
   Configurações de Alertas
  </span>
 </button>
 <button class="nav-item" data-view="viewConfigColors" type="button">
  <svg aria-hidden="true" fill="none" focusable="false" height="16" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="16">
   <circle cx="13.5" cy="6.5" r=".5">
   </circle>
   <circle cx="17.5" cy="10.5" r=".5">
   </circle>
   <circle cx="8.5" cy="7.5" r=".5">
   </circle>
   <circle cx="6.5" cy="12.5" r=".5">
   </circle>
   <path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.563-2.512 5.563-5.563C22 6.5 17.5 2 12 2z">
   </path>
  </svg>
  <span>
   Configurações de Cores
  </span>
 </button>
 <button class="nav-item" data-view="viewBackup" type="button">
  <svg aria-hidden="true" fill="none" focusable="false" height="16" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="16">
   <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4">
   </path>
   <polyline points="7 10 12 15 17 10">
   </polyline>
   <line x1="12" x2="12" y1="15" y2="3">
   </line>
  </svg>
  <span>
   Backup e Dados
  </span>
 </button>
 <button class="nav-item" data-view="viewDiagnostic" type="button">
  <svg aria-hidden="true" fill="none" focusable="false" height="16" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="16">
   <path d="M22 12h-4l-3 9L9 3l-3 9H2">
   </path>
  </svg>
  <span>
   Diagnóstico
  </span>
 </button>
</nav>
<!-- Legacy FAB button kept hidden in DOM; active FAB #fabAddEvent is integrated in bottom navigation -->
<button aria-label="Nova Previsão" class="fab-btn" id="btnFabNewEvent" title="Nova Previsão" type="button">
 <svg aria-hidden="true" fill="none" focusable="false" height="24" stroke="currentColor" stroke-width="2.5" viewbox="0 0 24 24" width="24">
  <line x1="12" x2="12" y1="5" y2="19">
  </line>
  <line x1="5" x2="19" y1="12" y2="12">
  </line>
 </svg>
</button>
<!-- Main View Container -->
<main class="app-main" id="mainContent" tabindex="-1">
 <!-- ==================== VIEW 1: PAINEL ==================== -->
 <section aria-labelledby="viewDashboardHeading" class="view-section active" id="viewDashboard">
  <h2 class="view-heading" id="viewDashboardHeading">
   Painel operacional
  </h2>
  <!-- Metric Cards (7 Metrics; 2-column grid on mobile) -->
  <!-- Highlight Grid: Spotlight (2/3 on tablet/wide) + Active Alarms Side Panel (1/3 on tablet/wide) -->
  <div class="dashboard-highlight-grid">
   <!-- Spotlight: Next Event -->
   <div class="spotlight-card" id="spotlightCard">
    <div class="spotlight-header">
     <div class="spotlight-badge">
      Próximo evento operacional
     </div>
     <span class="status-badge normal" id="spotlightBadgeState">
      Aguardando
     </span>
    </div>
    <div class="spotlight-body">
     <div>
      <div class="spotlight-path" id="spotlightHierarchy">
       Console • Duto • UO
      </div>
      <div class="spotlight-desc" id="spotlightDescription">
       Nenhum evento operacional pendente no momento.
      </div>
      <div id="spotlightNotes" style="color: var(--text-secondary); margin-top: 0.25rem">
      </div>
     </div>
     <div class="spotlight-timer">
      <div class="time-left" id="spotlightTimeLeft">
       --:--
      </div>
      <div class="sched-time" id="spotlightScheduledAt">
       Horário Previsto: --:--
      </div>
     </div>
    </div>
    <div id="spotlightActions" style="display: flex; gap: 0.5rem; justify-content: flex-end; margin-top: 0.5rem; flex-wrap: wrap">
     <!-- Dynamically filled -->
    </div>
   </div>
   <!-- Tablet / Widescreen Active Alarms & Overdue Side Panel (Wireframe Tablet - 1) -->
   <div class="tablet-alarms-panel" id="tabletActiveAlarmsPanel">
    <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem; flex-wrap: wrap">
     <strong style="display: flex; align-items: center; gap: 0.4rem">
      <span>
       <svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>
      </span>
      <span>
       Alarmes Ativos (
       <span id="tabletAlarmsCount">
        0
       </span>
       )
      </span>
     </strong>
     <button class="btn btn-outline btn-sm" onclick="App.UI.navigateTo('viewPendingEvents')" type="button">
      Ver todos →
     </button>
    </div>
    <div id="tabletAlarmsList" style="display: flex; flex-direction: column; gap: 0.5rem; flex: 1; overflow-y: auto; flex-wrap: wrap">
     <div style="color: var(--text-muted); padding: 1rem 0; text-align: center">
      Nenhum alarme crítico ou atrasado no momento.
     </div>
    </div>
   </div>
  </div>
  <!-- Urgent / Overdue Quick List -->
  <div class="card" id="cardDashboardUrgent">
   <div class="card-header">
    <div>
     <div class="card-title">
      <svg aria-hidden="true" fill="none" focusable="false" height="18" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="18">
       <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2">
       </polygon>
      </svg>
      <span>
       Eventos que Demandam Atenção Imediata
      </span>
     </div>
     <div class="card-subtitle">
      Eventos atrasados ou previstos para os próximos 30 minutos
     </div>
    </div>
    <button class="btn btn-outline btn-sm" onclick="App.UI.navigateTo('viewPendingEvents')" type="button">
     Ver Todos os Pendentes →
    </button>
   </div>
   <!-- Mobile Summarized Urgent Cards (Section 3.5) -->
   <div class="dashboard-urgent-cards" id="dashboardUrgentCards">
   </div>
   <!-- Tablet / Desktop Table -->
   <p class="table-scroll-hint" hidden="">
    Deslize a tabela ou use as setas do teclado para consultar as demais colunas.
   </p>
   <div aria-label="Eventos urgentes — tabela com rolagem horizontal" class="table-responsive" data-scroll-table="" role="region" tabindex="0">
    <table class="data-table" id="tableDashboardUrgent">
     <thead>
      <tr>
       <th>
        Horário
       </th>
       <th>
        Situação
       </th>
       <th>
        Console / Duto
       </th>
       <th>
        UO / Equipamento / TAG
       </th>
       <th>
        Descrição da Atividade
       </th>
       <th style="text-align: right">
        Ações
       </th>
      </tr>
     </thead>
     <tbody id="tbodyDashboardUrgent">
      <tr>
       <td colspan="6" style="text-align: center; color: var(--text-muted); padding: 1.5rem">
        Nenhum evento urgente no momento.
       </td>
      </tr>
     </tbody>
    </table>
   </div>
  </div>
  <div class="dashboard-context-stack" id="dashboardContextStack">
   <div class="dashboard-overview" id="dashboardOverview">
    <aside aria-label="Panorama do console" class="context-panel" id="dashboardContextPanel">
     <h2>
      Panorama do console
     </h2>
    </aside>
    <div class="dashboard-metrics">
     <button class="metric-card" data-filter="all" type="button">
      <div class="metric-icon" style="background: rgba(2, 132, 199, 0.15)">
       <svg aria-hidden="true" fill="none" focusable="false" height="22" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="22">
        <circle cx="12" cy="12" r="10">
        </circle>
        <polyline points="12 6 12 12 16 14">
        </polyline>
       </svg>
      </div>
      <div class="metric-data">
       <div class="metric-value" id="metricTotalPending">
        0
       </div>
       <div class="metric-label">
        Pendentes
       </div>
      </div>
     </button>
     <button class="metric-card" data-filter="overdue" type="button">
      <div class="metric-icon" style="background: rgba(153, 27, 27, 0.2)">
       <svg aria-hidden="true" fill="none" focusable="false" height="22" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="22">
        <circle cx="12" cy="12" r="10">
        </circle>
        <line x1="12" x2="12" y1="8" y2="12">
        </line>
        <line x1="12" x2="12.01" y1="16" y2="16">
        </line>
       </svg>
      </div>
      <div class="metric-data">
       <div class="metric-value" id="metricOverdue">
        0
       </div>
       <div class="metric-label">
        Atrasados
       </div>
      </div>
     </button>
     <button class="metric-card" data-filter="15min" type="button">
      <div class="metric-icon" style="background: rgba(220, 38, 38, 0.15)">
       <svg aria-hidden="true" fill="none" focusable="false" height="22" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="22">
        <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2">
        </polygon>
       </svg>
      </div>
      <div class="metric-data">
       <div class="metric-value" id="metricNext15">
        0
       </div>
       <div class="metric-label">
        Próx. 15 min
       </div>
      </div>
     </button>
     <button class="metric-card" data-filter="30min" type="button">
      <div class="metric-icon" style="background: rgba(234, 88, 12, 0.15)">
       <svg aria-hidden="true" fill="none" focusable="false" height="22" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="22">
        <circle cx="12" cy="12" r="10">
        </circle>
        <polyline points="12 6 12 12 14 14">
        </polyline>
       </svg>
      </div>
      <div class="metric-data">
       <div class="metric-value" id="metricNext30">
        0
       </div>
       <div class="metric-label">
        Próx. 30 min
       </div>
      </div>
     </button>
     <button class="metric-card" data-filter="60min" type="button">
      <div class="metric-icon" style="background: rgba(37, 99, 235, 0.15)">
       <svg aria-hidden="true" fill="none" focusable="false" height="22" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="22">
        <circle cx="12" cy="12" r="10">
        </circle>
        <polyline points="12 6 12 12 16 14">
        </polyline>
       </svg>
      </div>
      <div class="metric-data">
       <div class="metric-value" id="metricNext60">
        0
       </div>
       <div class="metric-label">
        Próx. 60 min
       </div>
      </div>
     </button>
     <button class="metric-card" data-filter="completed" type="button">
      <div class="metric-icon" style="background: rgba(22, 163, 74, 0.15)">
       <svg aria-hidden="true" fill="none" focusable="false" height="22" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="22">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14">
        </path>
        <polyline points="22 4 12 14.01 9 11.01">
        </polyline>
       </svg>
      </div>
      <div class="metric-data">
       <div class="metric-value" id="metricCompletedToday">
        0
       </div>
       <div class="metric-label">
        Concluídos Hoje
       </div>
      </div>
     </button>
     <button class="metric-card" data-filter="unacknowledged" type="button">
      <div class="metric-icon" style="background: rgba(217, 119, 6, 0.15)">
       <svg aria-hidden="true" fill="none" focusable="false" height="22" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="22">
        <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9">
        </path>
        <path d="M13.73 21a2 2 0 0 1-3.46 0">
        </path>
       </svg>
      </div>
      <div class="metric-data">
       <div class="metric-value" id="metricUnacknowledged">
        0
       </div>
       <div class="metric-label">
        Alarmes Ativos
       </div>
      </div>
     </button>
    </div>
   </div>
   <aside aria-label="Evento em foco" class="context-panel" id="dashboardSelectedDetail">
    <h2>
     Evento em foco
    </h2>
   </aside>
  </div>
 </section>
 <!-- ==================== VIEW 2: NOVO EVENTO ==================== -->
 <section aria-labelledby="viewNewEventHeading" class="view-section" id="viewNewEvent">
  <h2 class="view-heading" id="viewNewEventHeading">
   Nova previsão
  </h2>
  <div class="card">
   <div class="card-header">
    <div>
     <div class="card-title" id="formEventTitle">
      Cadastrar Previsão Operacional
     </div>
     <div class="card-subtitle" style="display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap">
      <span class="active-console-tag" id="labelEventActiveConsole" style="background: rgba(56, 189, 248, 0.15); padding: 0.25rem 0.6rem; border-radius: 4px; font-weight: 700">
       Console Ativo: --
      </span>
      <strong id="labelActiveConsoleBadge" style="display: none">
       --
      </strong>
      <span style="color: var(--text-muted)">
       (Definido no seletor global do topo)
      </span>
     </div>
    </div>
    <button class="btn btn-outline btn-sm" id="btnCancelEditEvent" style="display: none" type="button">
     Cancelar Edição
    </button>
   </div>
   <form autocomplete="off" id="formEvent">
    <input id="eventEditId" type="hidden" value=""/>
    <input id="eventConsoleId" type="hidden" value=""/>
    <input id="selectEventConsole" type="hidden" value=""/>
    <div class="event-form-sections">
     <!-- Cascading Dropdowns (Console is inherited from header) -->
     <!-- Date and Time -->
     <!-- Description & Notes -->
     <!-- Tablet Stylus Drawing Pad Toggle -->
     <fieldset class="event-fieldset fieldset-localizacao">
      <legend>
       Localização
      </legend>
      <div class="form-group">
       <label for="selectEventPipeline">
        Duto
        <span class="required">
         *
        </span>
       </label>
       <select id="selectEventPipeline" required="">
        <option value="">
         Carregando dutos do console...
        </option>
       </select>
       <div class="form-help">
        Dutos pertencentes ao console ativo
       </div>
      </div>
      <div class="form-group">
       <label for="selectEventUO">
        Unidade Operacional (UO)
        <span class="required">
         *
        </span>
       </label>
       <select disabled="" id="selectEventUO" required="">
        <option value="">
         Selecione primeiro o Duto...
        </option>
       </select>
       <div class="form-help">
        UOs conectadas ao duto selecionado
       </div>
      </div>
      <div class="form-group">
       <label for="selectEventEquipmentType">
        Tipo de Equipamento
        <span class="form-help">
         (opcional)
        </span>
       </label>
       <select disabled="" id="selectEventEquipmentType">
        <option value="">
         Geral da UO / Não aplicável
        </option>
       </select>
      </div>
      <div class="form-group">
       <label for="selectEventTag">
        TAG do Equipamento
        <span class="form-help">
         (opcional)
        </span>
       </label>
       <select disabled="" id="selectEventTag">
        <option value="">
         Selecione o Tipo primeiro...
        </option>
       </select>
      </div>
      <div class="form-group span-full" style="margin-top: -0.25rem; margin-bottom: 0.25rem">
       <div aria-live="polite" id="cascadeStatusText" style="font-weight: 600">
       </div>
      </div>
     </fieldset>
     <fieldset class="event-fieldset fieldset-programacao">
      <legend>
       Programação
      </legend>
      <div class="form-group">
       <label for="inputEventDate">
        Data do Evento
        <span class="required">
         *
        </span>
       </label>
       <input id="inputEventDate" required="" type="date"/>
      </div>
      <div class="form-group">
       <label for="inputEventTime">
        Hora do Evento (HH:mm)
        <span class="required">
         *
        </span>
       </label>
       <input id="inputEventTime" required="" type="time"/>
      </div>
      <div class="form-group">
       <label for="selectEventPriority">
        Prioridade
       </label>
       <select id="selectEventPriority">
        <option value="Normal">
         Normal
        </option>
        <option value="Alta">
         Alta
        </option>
        <option value="Crítica">
         Crítica
        </option>
        <option value="Baixa">
         Baixa
        </option>
       </select>
      </div>
     </fieldset>
     <fieldset class="event-fieldset fieldset-atividade">
      <legend>
       Atividade
      </legend>
      <div class="form-group span-full">
       <label for="inputEventDescription">
        Descrição da Atividade Operacional
        <span class="required">
         *
        </span>
       </label>
       <textarea id="inputEventDescription" placeholder="Ex: Verificar o término do recebimento de MGO" required="" rows="3"></textarea>
       <div class="form-help">
        Texto claro e direto da atividade a ser acompanhada
       </div>
      </div>
      <details class="optional-group">
       <summary>
        Observações e recomendações
       </summary>
       <div class="form-group span-full">
        <label for="inputEventNotes">
         Observações e Recomendações Operacionais
        </label>
        <textarea id="inputEventNotes" placeholder="Informações adicionais, alinhamento de válvulas, contatos, etc." rows="2"></textarea>
       </div>
      </details>
     </fieldset>
     <fieldset class="event-fieldset fieldset-lousa">
      <legend>
       Lousa
      </legend>
      <div class="form-group span-full">
       <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem">
        <label>
         Desenho / Anotação com Caneta de Tablet (Opcional):
        </label>
        <div style="display: flex; gap: 0.4rem; align-items: center; flex-wrap: wrap">
         <span id="stylusModeIndicator" style="background: rgba(56, 189, 248, 0.15); padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: 700; display: none">
          Modo: Caneta (4px)
         </span>
         <button class="btn btn-outline btn-sm" id="btnToggleStylusCanvas" type="button">
          <svg aria-hidden="true" fill="none" focusable="false" height="14" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="14">
           <path d="M12 19l7-7 3 3-7 7-3-3z">
           </path>
           <path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z">
           </path>
           <path d="M2 2l7.586 7.586">
           </path>
           <circle cx="11" cy="11" r="2">
           </circle>
          </svg>
          <span>
           Abrir Lousa para Caneta
          </span>
         </button>
        </div>
       </div>
       <div class="stylus-canvas-container" id="boxStylusCanvas" style="display: none">
        <div class="canvas-toolbar">
         <div style="display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap">
          <label for="inputStylusStrokeColor">
           Cor:
          </label>
          <input id="inputStylusStrokeColor" style="padding: 1px" type="color" value="#38bdf8"/>
          <label class="control-label" for="stylusColor">
           Cor da caneta (compatibilidade)
          </label>
          <input id="stylusColor" style="display: none" type="color" value="#38bdf8"/>
          <label style="margin-left: 0.35rem">
           Espessura:
          </label>
          <label class="control-label" for="selectStylusStrokeWidth">
           Espessura da caneta
          </label>
          <select id="selectStylusStrokeWidth" style="padding: 0.2rem 0.5rem">
           <option value="2">
            Fina (2px)
           </option>
           <option selected="" value="4">
            Normal (4px)
           </option>
           <option value="8">
            Grossa (8px)
           </option>
          </select>
          <label class="control-label" for="stylusWidth">
           Espessura da caneta (compatibilidade)
          </label>
          <select id="stylusWidth" style="display: none">
           <option selected="" value="4">
            4
           </option>
          </select>
          <button class="btn btn-outline btn-sm" id="btnEraserStylusCanvas" type="button">
           Borracha
          </button>
          <button class="btn btn-outline btn-sm" id="btnUndoStylusCanvas" title="Desfazer último traço" type="button">
           ↩ Desfazer
          </button>
         </div>
         <div style="display: flex; gap: 0.5rem; flex-wrap: wrap">
          <button class="btn btn-outline btn-sm" id="btnFullscreenStylusCanvas" title="Expandir lousa em tela cheia" type="button">
           ⛶ Tela Cheia
          </button>
          <button class="btn btn-outline btn-sm" id="btnClearStylusCanvas" type="button">
           Limpar
          </button>
         </div>
        </div>
        <canvas class="stylus-canvas" height="440" id="stylusDrawingCanvas" width="1200">
        </canvas>
        <div class="form-help" style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 0.35rem">
         <span>
          Desenhe alinhamentos, níveis de tanque ou anotações manuscritas diretamente com a caneta ou dedo.
         </span>
         <span>
          💡 Dica: Gire o celular para paisagem ou use Tela Cheia para mais espaço.
         </span>
        </div>
       </div>
      </div>
     </fieldset>
    </div>
    <!-- Alarm Sub-Card -->
    <fieldset class="event-fieldset" style="margin-top: 1rem; background: var(--bg-app); border: 1px solid var(--border-color)">
     <legend>
      Alarme
     </legend>
     <div class="card-header" style="margin-bottom: 0.5rem">
      <label class="form-checkbox" style="font-weight: 700">
       <input checked="" id="checkEventAlarmActive" type="checkbox"/>
       <span>
        Ativar Alarme para esta Previsão
       </span>
      </label>
      <label class="form-checkbox" id="wrapperUseDefaultAlarm">
       <input checked="" id="checkEventUseDefaultAlarm" type="checkbox"/>
       <span>
        Usar Configurações Padrão de Alerta
       </span>
      </label>
     </div>
     <div class="form-grid" id="boxCustomAlarmSettings" style="display: none; padding-top: 0.5rem">
      <div class="form-group">
       <label for="inputEventAlarmLeadTime">
        Antecedência do Alarme (minutos)
       </label>
       <input id="inputEventAlarmLeadTime" max="1440" min="0" type="number" value="15"/>
       <div class="form-help">
        0 dispara exatamente no horário
       </div>
      </div>
      <div class="form-group">
       <label>
        Formas de Alerta do Evento
       </label>
       <div style="display: flex; flex-direction: column; gap: 0.35rem; margin-top: 0.35rem; flex-wrap: wrap">
        <label class="form-checkbox">
         <input checked="" id="checkEventAlertSound" type="checkbox"/>
         <span>
          Sinal Sonoro
         </span>
        </label>
        <label class="form-checkbox">
         <input checked="" id="checkEventAlertVisual" type="checkbox"/>
         <span>
          Alerta Visual na Tela
         </span>
        </label>
        <label class="form-checkbox">
         <input id="checkEventAlertNotif" type="checkbox"/>
         <span>
          Notificação do Navegador
         </span>
        </label>
       </div>
      </div>
      <div class="form-group">
       <label class="form-checkbox" style="margin-top: 0.5rem">
        <input checked="" id="checkEventAlertRepeat" type="checkbox"/>
        <span>
         Repetir Alerta até Reconhecimento
        </span>
       </label>
       <div style="display: flex; gap: 0.5rem; margin-top: 0.35rem; flex-wrap: wrap">
        <div style="flex: 1">
         <label for="inputEventAlertRepeatInterval">
          Intervalo (min)
         </label>
         <input id="inputEventAlertRepeatInterval" max="60" min="1" type="number" value="2"/>
        </div>
        <div style="flex: 1">
         <label for="inputEventAlertMaxRepeats">
          Máx Repetições
         </label>
         <input id="inputEventAlertMaxRepeats" max="20" min="1" type="number" value="5"/>
        </div>
       </div>
      </div>
     </div>
    </fieldset>
    <!-- Bottom Form Actions: Option to keep Duto & UO for quick consecutive additions -->
    <label class="form-checkbox" title="Ao salvar, o Duto e a UO permanecerão selecionados para facilitar cadastrar vários eventos no mesmo duto.">
     <input checked="" id="checkKeepDutoUO" type="checkbox"/>
     <span>
      <strong>
       Manter Duto e UO para próximas previsões
      </strong>
     </span>
    </label>
    <button class="btn btn-secondary event-reset-action" id="btnResetEventForm" type="button">
     Limpar
    </button>
    <div class="form-sticky-submit-bar" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.75rem; margin-top: 1.25rem">
     <div style="display: flex; gap: 0.5rem; flex-wrap: wrap">
      <!-- Salvar e Inserir Outra Previsão neste Duto -->
      <button class="btn btn-success" id="btnSubmitAndNew" title="Salva e avança o horário mantendo o Duto e a UO" type="button">
       <svg aria-hidden="true" fill="none" focusable="false" height="16" stroke="currentColor" stroke-width="2.5" viewbox="0 0 24 24" width="16">
        <line x1="12" x2="12" y1="5" y2="19">
        </line>
        <line x1="5" x2="19" y1="12" y2="12">
        </line>
       </svg>
       <span>
        Salvar e + Outra no Duto
       </span>
      </button>
      <button class="btn btn-primary" id="btnSubmitEvent" type="submit">
       <svg aria-hidden="true" fill="none" focusable="false" height="16" stroke="currentColor" stroke-width="2.5" viewbox="0 0 24 24" width="16">
        <polyline points="20 6 9 17 4 12">
        </polyline>
       </svg>
       <span id="btnSubmitEventText">
        Salvar Previsão
       </span>
      </button>
     </div>
    </div>
   </form>
  </div>
  <aside aria-label="Prévia não salva" class="context-panel" id="eventDraftSummary">
   <h2>
    Prévia não salva
   </h2>
  </aside>
  <aside aria-label="Previsões relacionadas" class="context-panel" id="eventRelatedList">
   <h2>
    Previsões relacionadas
   </h2>
  </aside>
 </section>
 <!-- ==================== VIEW 3: EVENTOS PENDENTES ==================== -->
 <section aria-labelledby="viewPendingEventsHeading" class="view-section" id="viewPendingEvents">
  <h2 class="view-heading" id="viewPendingEventsHeading">
   Eventos pendentes
  </h2>
  <!-- Toolbar -->
  <div class="events-toolbar">
   <div class="toolbar-primary">
    <div class="search-box">
     <svg aria-hidden="true" fill="none" focusable="false" height="16" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="16">
      <circle cx="11" cy="11" r="8">
      </circle>
      <line x1="21" x2="16.65" y1="21" y2="16.65">
      </line>
     </svg>
     <label class="control-label" for="inputSearchPending">
      Pesquisar por texto, duto, UO, TAG ou descrição...
     </label>
     <input id="inputSearchPending" placeholder="Pesquisar por texto, duto, UO, TAG ou descrição..." type="text"/>
    </div>
    <div style="display: flex; align-items: center; gap: 0.45rem; flex-wrap: wrap">
     <button class="btn btn-outline btn-sm" id="btnToggleFilters" type="button">
      <svg aria-hidden="true" fill="none" focusable="false" height="14" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="14">
       <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3">
       </polygon>
      </svg>
      <span>
       Filtros
      </span>
      <span class="nav-badge" id="badgeActiveFiltersCount" style="display: none; background: #0284c7">
       0
      </span>
     </button>
     <!-- Filter only active console toggle -->
     <label class="form-checkbox" title="Filtrar automaticamente pelo Console selecionado no cabeçalho">
      <input checked="" id="checkFilterOnlyActiveConsole" type="checkbox"/>
      <span>
       Apenas Console Ativo (
       <strong id="labelActiveConsoleFilter">
        C04
       </strong>
       )
      </span>
     </label>
     <!-- View switch -->
     <div style="display: flex; border: 1px solid var(--border-color); border-radius: 6px; overflow: hidden; flex-wrap: wrap">
      <button class="btn btn-secondary btn-sm" id="btnViewCards" style="border-radius: 0" title="Visualização em Cartões" type="button">
       <svg aria-hidden="true" fill="none" focusable="false" height="14" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="14">
        <rect height="7" width="7" x="3" y="3">
        </rect>
        <rect height="7" width="7" x="14" y="3">
        </rect>
        <rect height="7" width="7" x="14" y="14">
        </rect>
        <rect height="7" width="7" x="3" y="14">
        </rect>
       </svg>
      </button>
      <button class="btn btn-outline btn-sm" id="btnViewTable" style="border-radius: 0" title="Visualização em Tabela Compacta" type="button">
       <svg aria-hidden="true" fill="none" focusable="false" height="14" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="14">
        <line x1="8" x2="21" y1="6" y2="6">
        </line>
        <line x1="8" x2="21" y1="12" y2="12">
        </line>
        <line x1="8" x2="21" y1="18" y2="18">
        </line>
        <line x1="3" x2="3.01" y1="6" y2="6">
        </line>
        <line x1="3" x2="3.01" y1="12" y2="12">
        </line>
        <line x1="3" x2="3.01" y1="18" y2="18">
        </line>
       </svg>
      </button>
     </div>
     <div style="display: flex; align-items: center; gap: 0.35rem; flex-wrap: wrap">
      <label for="selectSortPending" style="white-space: nowrap">
       Ordenar:
      </label>
      <select id="selectSortPending" style="padding: 0.2rem 0.5rem">
       <option value="cronologica">
        Cronológica (Padrão)
       </option>
       <option value="console">
        Console
       </option>
       <option value="duto">
        Duto
       </option>
       <option value="uo">
        UO
       </option>
       <option value="tag">
        TAG
       </option>
       <option value="prioridade">
        Prioridade
       </option>
      </select>
     </div>
     <button class="btn btn-outline btn-sm" id="btnClearFilters" title="Limpar todos os filtros" type="button">
      Limpar
     </button>
    </div>
   </div>
   <!-- Collapsible Advanced Filters / Mobile Filter Sheet -->
   <div class="toolbar-filters" id="filterDrawer" style="display: none">
    <div class="span-full" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem; flex-wrap: wrap">
     <strong style="color: var(--text-main)">
      Filtros Avançados
     </strong>
     <button class="btn btn-outline btn-sm" id="btnCloseFilterSheet" style="padding: 0.2rem 0.5rem" type="button">
      Fechar ×
     </button>
    </div>
    <div class="form-group">
     <label for="filterConsole">
      Console
     </label>
     <select id="filterConsole" style="padding: 0.35rem">
      <option value="">
       Todos os Consoles
      </option>
     </select>
    </div>
    <div class="form-group">
     <label for="filterPipeline">
      Duto
     </label>
     <select id="filterPipeline" style="padding: 0.35rem">
      <option value="">
       Todos os Dutos
      </option>
     </select>
    </div>
    <div class="form-group">
     <label for="filterUO">
      UO
     </label>
     <select id="filterUO" style="padding: 0.35rem">
      <option value="">
       Todas as UOs
      </option>
     </select>
    </div>
    <div class="form-group">
     <label for="filterStatus">
      Situação / Faixa
     </label>
     <select id="filterStatus" style="padding: 0.35rem">
      <option value="">
       Todas as Situações
      </option>
      <option value="Atrasado">
       Atrasado
      </option>
      <option value="Crítico">
       Crítico
      </option>
      <option value="Urgente">
       Urgente
      </option>
      <option value="Atenção">
       Atenção
      </option>
      <option value="Monitoramento">
       Monitoramento
      </option>
      <option value="Normal">
       Normal
      </option>
     </select>
    </div>
    <div class="form-group">
     <label for="filterAlarm">
      Alarme Ativo
     </label>
     <select id="filterAlarm" style="padding: 0.35rem">
      <option value="">
       Todos
      </option>
      <option value="sim">
       Com Alarme
      </option>
      <option value="nao">
       Sem Alarme
      </option>
     </select>
    </div>
    <div class="form-group">
     <label for="filterPriority">
      Prioridade
     </label>
     <select id="filterPriority" style="padding: 0.35rem">
      <option value="">
       Todas
      </option>
      <option value="Crítica">
       Crítica
      </option>
      <option value="Alta">
       Alta
      </option>
      <option value="Normal">
       Normal
      </option>
      <option value="Baixa">
       Baixa
      </option>
     </select>
    </div>
    <div class="form-group">
     <label for="filterDateFrom">
      Data De
     </label>
     <input id="filterDateFrom" style="padding: 0.2rem 0.4rem" type="date"/>
    </div>
    <div class="form-group">
     <label for="filterDateTo">
      Data Até
     </label>
     <input id="filterDateTo" style="padding: 0.2rem 0.4rem" type="date"/>
    </div>
    <div class="span-full" style="display: flex; justify-content: flex-end; gap: 0.5rem; margin-top: 0.35rem; flex-wrap: wrap">
     <button class="btn btn-secondary btn-sm" id="btnSheetClearFilters" type="button">
      Limpar Filtros
     </button>
     <button class="btn btn-primary btn-sm" id="btnSheetApplyFilters" type="button">
      Aplicar Filtros
     </button>
    </div>
   </div>
  </div>
  <!-- Master-Detail Wrapper for Tablet Landscape / Ultrawide (Section 4.3) -->
  <div class="pending-master-detail-grid">
   <!-- Cards Container (Master List) -->
   <div class="pending-master">
    <div class="events-container-cards" id="containerPendingCards">
     <!-- Rendered dynamically -->
    </div>
    <p class="table-scroll-hint" hidden="">
     Deslize a tabela ou use as setas do teclado para consultar as demais colunas.
    </p>
    <div aria-label="Eventos pendentes — tabela com rolagem horizontal" class="table-responsive" data-scroll-table="" id="containerPendingTable" role="region" style="display: none" tabindex="0">
     <table class="data-table" id="tablePendingEvents">
      <thead>
       <tr>
        <th>
         Horário
        </th>
        <th>
         Tempo Restante
        </th>
        <th>
         Situação
        </th>
        <th>
         Console / Duto
        </th>
        <th>
         UO / Equipamento / TAG
        </th>
        <th>
         Descrição
        </th>
        <th>
         Alarme
        </th>
        <th style="text-align: right">
         Ações
        </th>
       </tr>
      </thead>
      <tbody id="tbodyPendingEvents">
       <!-- Rendered dynamically -->
      </tbody>
     </table>
    </div>
   </div>
   <!-- Detail Side Pane (Visible on Tablet Landscape & Ultrawide) -->
   <aside aria-label="Detalhes do Evento Selecionado" class="pending-detail-pane" id="pendingDetailPane">
    <!-- Rendered dynamically by renderPendingDetailPane -->
   </aside>
   <aside aria-label="Contexto da seleção" class="context-panel" id="pendingContextPanel">
    <h2>
     Contexto da seleção
    </h2>
   </aside>
  </div>
  <!-- Compact Table Container -->
  <div id="pendingEmptyMessage" style="display: none; text-align: center; padding: 3rem 1rem; color: var(--text-muted)">
   <svg aria-hidden="true" fill="none" focusable="false" height="48" stroke="currentColor" stroke-width="1.5" style="margin-bottom: 0.5rem" viewbox="0 0 24 24" width="48">
    <circle cx="12" cy="12" r="10">
    </circle>
    <path d="M8 12h8">
    </path>
   </svg>
   <div style="font-weight: 700; color: var(--text-main)">
    Nenhuma previsão pendente encontrada
   </div>
   <div>
    Não há eventos que correspondam aos filtros selecionados.
   </div>
  </div>
 </section>
 <!-- ==================== VIEW 4: EVENTOS CONCLUÍDOS ==================== -->
 <section aria-labelledby="viewCompletedEventsHeading" class="view-section" id="viewCompletedEvents">
  <h2 class="view-heading" id="viewCompletedEventsHeading">
   Eventos concluídos
  </h2>
  <div class="events-toolbar">
   <div class="toolbar-primary">
    <div class="search-box">
     <svg aria-hidden="true" fill="none" focusable="false" height="16" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="16">
      <circle cx="11" cy="11" r="8">
      </circle>
      <line x1="21" x2="16.65" y1="21" y2="16.65">
      </line>
     </svg>
     <label class="control-label" for="inputSearchCompleted">
      Pesquisar em eventos concluídos...
     </label>
     <input id="inputSearchCompleted" placeholder="Pesquisar em eventos concluídos..." type="text"/>
    </div>
    <div style="display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap">
     <button class="btn btn-outline btn-sm" id="btnExportCompletedCSV" type="button">
      <svg aria-hidden="true" fill="none" focusable="false" height="14" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="14">
       <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4">
       </path>
       <polyline points="7 10 12 15 17 10">
       </polyline>
       <line x1="12" x2="12" y1="15" y2="3">
       </line>
      </svg>
      <span>
       Exportar CSV
      </span>
     </button>
    </div>
   </div>
   <details class="completed-filters" id="completedFilters">
    <summary>
     Filtros
     <span class="filter-scope" id="completedFiltersSummary">
      Todos os concluídos
     </span>
    </summary>
    <div class="toolbar-filters">
     <div class="form-group">
      <label for="filterCompletedConsole">
       Console
      </label>
      <select id="filterCompletedConsole" style="padding: 0.35rem">
       <option value="">
        Todos os Consoles
       </option>
      </select>
     </div>
     <div class="form-group">
      <label for="filterCompletedPipeline">
       Duto
      </label>
      <select id="filterCompletedPipeline" style="padding: 0.35rem">
       <option value="">
        Todos os Dutos
       </option>
      </select>
     </div>
     <div class="form-group">
      <label for="filterCompletedUO">
       UO
      </label>
      <select id="filterCompletedUO" style="padding: 0.35rem">
       <option value="">
        Todas as UOs
       </option>
      </select>
     </div>
     <div class="form-group">
      <label for="filterCompletedTiming">
       Situação Conclusão
      </label>
      <select id="filterCompletedTiming" style="padding: 0.35rem">
       <option value="">
        Todas
       </option>
       <option value="antecedencia">
        Com Antecedência
       </option>
       <option value="atraso">
        Com Atraso
       </option>
       <option value="noprazo">
        Exato no Horário
       </option>
      </select>
     </div>
     <div class="form-group">
      <label for="filterCompletedDateFrom">
       Data Prevista De
      </label>
      <input id="filterCompletedDateFrom" style="padding: 0.2rem 0.4rem" type="date"/>
     </div>
     <div class="form-group">
      <label for="filterCompletedDateTo">
       Data Prevista Até
      </label>
      <input id="filterCompletedDateTo" style="padding: 0.2rem 0.4rem" type="date"/>
     </div>
    </div>
   </details>
  </div>
  <!-- Mobile Expandable Completed Cards Container (Section 12) -->
  <div class="completed-workspace">
   <div class="completed-cards-container" id="containerCompletedCards">
   </div>
   <p class="table-scroll-hint" hidden="">
    Deslize a tabela ou use as setas do teclado para consultar as demais colunas.
   </p>
   <div aria-label="Eventos concluídos — tabela com rolagem horizontal" class="table-responsive" data-scroll-table="" id="tableCompletedWrapper" role="region" tabindex="0">
    <table class="data-table" id="tableCompletedEvents">
     <thead>
      <tr>
       <th>
        Horário Previsto
       </th>
       <th>
        Horário Conclusão
       </th>
       <th>
        Diferença Efetiva
       </th>
       <th>
        Console / Duto
       </th>
       <th>
        UO / Equipamento / TAG
       </th>
       <th>
        Descrição e Observação de Conclusão
       </th>
       <th>
        Controlador
       </th>
       <th>
        Alarmes
       </th>
       <th style="text-align: right">
        Ações
       </th>
      </tr>
     </thead>
     <tbody id="tbodyCompletedEvents">
      <!-- Dynamically populated -->
     </tbody>
    </table>
   </div>
   <div id="completedEmptyMessage" style="display: none; text-align: center; padding: 3rem 1rem; color: var(--text-muted)">
    Nenhum evento concluído correspondente.
   </div>
  </div>
  <!-- Desktop / Tablet Completed Table (9 Columns) -->
  <aside aria-label="Resumo dos concluídos" class="context-panel" id="completedContextPanel">
   <h2>
    Resumo dos concluídos
   </h2>
  </aside>
  <aside aria-label="Conclusão selecionada" class="context-panel" id="completedDetailPane">
   <h2>
    Conclusão selecionada
   </h2>
  </aside>
 </section>
 <!-- =========================================================================
         VIEW 5: CADASTROS UNIFICADOS (TODOS NA MESMA TELA, SEM ESPAÇO MORTO)
         ========================================================================= -->
 <section aria-labelledby="viewCadastrosHeading" class="view-section" id="viewCadastros">
  <h2 class="view-heading" id="viewCadastrosHeading">
   Cadastros operacionais
  </h2>
  <div class="card" style="margin-bottom: 1rem">
   <div class="card-header" style="margin-bottom: 0.5rem">
    <div>
     <div class="card-title">
      <svg aria-hidden="true" fill="none" focusable="false" height="20" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="20">
       <polygon points="12 2 2 7 12 12 22 7 12 2">
       </polygon>
       <polyline points="2 17 12 22 22 17">
       </polyline>
       <polyline points="2 12 12 17 22 12">
       </polyline>
      </svg>
      <span>
       Painel Geral da Estrutura Operacional
      </span>
     </div>
     <div class="card-subtitle">
      Cadastre e gerencie toda a hierarquia (Consoles, Dutos, UOs, Tipos e TAGs) em um único painel integrado
     </div>
    </div>
   </div>
   <!-- Category Selector Bar for Mobile / Tablet Drill-Down (Section 13) -->
   <div class="cadastros-category-bar" id="cadastrosCategoryBar">
    <button class="cadastros-category-btn active" data-cat="consoles" onclick="App.UI.switchCadastrosCategory('consoles')" type="button">
     <span>
      Consoles
     </span>
     <span class="cat-count" id="catCountConsoles">
      0
     </span>
    </button>
    <button class="cadastros-category-btn" data-cat="pipelines" onclick="App.UI.switchCadastrosCategory('pipelines')" type="button">
     <span>
      Dutos
     </span>
     <span class="cat-count" id="catCountPipelines">
      0
     </span>
    </button>
    <button class="cadastros-category-btn" data-cat="uos" onclick="App.UI.switchCadastrosCategory('uos')" type="button">
     <span>
      UOs
     </span>
     <span class="cat-count" id="catCountUOs">
      0
     </span>
    </button>
    <button class="cadastros-category-btn" data-cat="types" onclick="App.UI.switchCadastrosCategory('types')" type="button">
     <span>
      Tipos
     </span>
     <span class="cat-count" id="catCountTypes">
      0
     </span>
    </button>
    <button class="cadastros-category-btn" data-cat="tags" onclick="App.UI.switchCadastrosCategory('tags')" type="button">
     <span>
      TAGs
     </span>
     <span class="cat-count" id="catCountTags">
      0
     </span>
    </button>
    <button class="cadastros-category-btn" data-cat="all" onclick="App.UI.switchCadastrosCategory('all')" type="button">
     <span>
      Ver Todos
     </span>
    </button>
   </div>
  </div>
  <!-- 3-Column Unified Responsive Grid -->
  <div class="cadastros-unified-grid cadastros-hub-grid">
   <!-- PAINEL 1: CONSOLES & DUTOS -->
   <div class="cadastro-hub-card" data-cat-group="consoles,pipelines" id="hubCardConsolesPipelines">
    <div class="hub-header">
     <div class="hub-title">
      <svg aria-hidden="true" fill="none" focusable="false" height="18" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="18">
       <rect height="14" rx="2" ry="2" width="20" x="2" y="3">
       </rect>
       <line x1="8" x2="16" y1="21" y2="21">
       </line>
       <line x1="12" x2="12" y1="17" y2="21">
       </line>
      </svg>
      <span>
       1. Consoles &amp; Dutos
      </span>
     </div>
    </div>
    <!-- SUB-SECTION: CONSOLES -->
    <div class="catalog-category" data-cat-item="consoles" data-editor-open="false" id="subSectionConsoles">
     <!-- Form Console -->
     <form class="catalog-editor" id="formConsole" style="background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 6px; padding: 0.75rem">
      <button class="btn btn-outline catalog-back" data-catalog-back="formConsole" type="button">
       Voltar à lista
      </button>
      <input id="consoleEditId" type="hidden" value=""/>
      <label>
       Adicionar / Editar Console:
      </label>
      <div style="display: flex; gap: 0.4rem; margin-top: 0.25rem; flex-wrap: wrap">
       <label class="control-label" for="inputConsoleName">
        Nome do console
       </label>
       <input id="inputConsoleName" placeholder="Ex: C04" required="" style="padding: 0.35rem 0.6rem" type="text"/>
       <button class="btn btn-primary btn-sm" id="btnSubmitConsole" type="submit">
        Salvar
       </button>
       <button class="btn btn-secondary btn-sm" id="btnCancelConsoleEdit" style="display: none" type="button">
        Cancelar
       </button>
      </div>
     </form>
     <!-- Consoles List -->
     <div class="catalog-list" style="margin-top: 0.5rem; margin-bottom: 0.75rem">
      <button class="btn btn-outline catalog-new" data-catalog-new="formConsole" type="button">
       Novo registro
      </button>
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem; gap: 0.35rem; flex-wrap: wrap">
       <strong>
        Consoles (C02-C16):
       </strong>
       <div style="display: flex; gap: 0.3rem; align-items: center; flex-wrap: wrap">
        <label class="control-label" for="filterActiveConsoles">
         Situação dos consoles
        </label>
        <select id="filterActiveConsoles" style="padding: 0.15rem 0.35rem">
         <option value="all">
          Todos
         </option>
         <option value="active">
          Ativos
         </option>
         <option value="inactive">
          Inativos
         </option>
        </select>
        <label class="control-label" for="searchConsoles">
         Buscar console...
        </label>
        <input id="searchConsoles" placeholder="Buscar console..." style="padding: 0.2rem 0.4rem" type="text"/>
       </div>
      </div>
      <p class="table-scroll-hint" hidden="">
       Deslize a tabela ou use as setas do teclado para consultar as demais colunas.
      </p>
      <div aria-label="Consoles — tabela com rolagem horizontal" class="hub-list-container" data-scroll-table="" role="region" tabindex="0">
       <table class="data-table" id="tableConsoles">
        <thead>
         <tr>
          <th>
           Console
          </th>
          <th>
           Dutos
          </th>
          <th>
           Situação
          </th>
          <th style="text-align: right">
           Ações
          </th>
         </tr>
        </thead>
        <tbody id="tbodyConsoles">
        </tbody>
       </table>
      </div>
     </div>
    </div>
    <!-- SUB-SECTION: PIPELINES -->
    <div class="catalog-category" data-cat-item="pipelines" data-editor-open="false" id="subSectionPipelines">
     <!-- Form Duto (com atalho para criar UOs na hora) -->
     <form class="catalog-editor" id="formPipeline" style="background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 6px; padding: 0.75rem">
      <button class="btn btn-outline catalog-back" data-catalog-back="formPipeline" type="button">
       Voltar à lista
      </button>
      <input id="pipelineEditId" type="hidden" value=""/>
      <div style="font-weight: 700; margin-bottom: 0.5rem">
       Novo / Editar Duto:
      </div>
      <div class="form-group" style="margin-bottom: 0.5rem">
       <label for="selectPipelineConsole">
        Console Responsável
        <span class="required">
         *
        </span>
       </label>
       <select id="selectPipelineConsole" required="" style="padding: 0.35rem 0.6rem">
        <option value="">
         Selecione o Console...
        </option>
       </select>
      </div>
      <div class="form-group" style="margin-bottom: 0.5rem">
       <label for="inputPipelineName">
        Nome do Duto
        <span class="required">
         *
        </span>
       </label>
       <input id="inputPipelineName" placeholder="Ex: OSCAN, OSBRA" required="" style="padding: 0.35rem 0.6rem" type="text"/>
      </div>
      <!-- UOs Selection + Inline UO Quick Adder -->
      <div class="form-group">
       <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap">
        <label>
         UOs Vinculadas
         <span class="required">
          * (Mínimo 2 UOs)
         </span>
        </label>
       </div>
       <!-- Inline Quick UO Adder inside Duto Form -->
       <div style="display: flex; gap: 0.35rem; margin-top: 0.25rem; margin-bottom: 0.35rem; flex-wrap: wrap">
        <label class="control-label" for="inputInlineNewUO">
         Nova UO para o duto
        </label>
        <input id="inputInlineNewUO" placeholder="+ Digitar nova UO aqui..." style="padding: 0.25rem 0.5rem" type="text"/>
        <button class="btn btn-secondary btn-sm" id="btnInlineAddUO" title="Criar UO imediatamente e disponibilizar na lista" type="button">
         + Criar UO
        </button>
       </div>
       <div class="uo-selection-box" id="boxPipelineUOs">
        <!-- Checkboxes populated dynamically -->
       </div>
       <div class="form-help">
        Selecione pelo menos duas UOs para este duto.
       </div>
      </div>
      <div style="display: flex; justify-content: flex-end; gap: 0.5rem; margin-top: 0.6rem; flex-wrap: wrap">
       <button class="btn btn-secondary btn-sm" id="btnCancelPipelineEdit" style="display: none" type="button">
        Cancelar
       </button>
       <button class="btn btn-primary btn-sm" id="btnSubmitPipeline" type="submit">
        Salvar Duto
       </button>
      </div>
     </form>
     <!-- Dutos List -->
     <div class="catalog-list" style="margin-top: 0.5rem">
      <button class="btn btn-outline catalog-new" data-catalog-new="formPipeline" type="button">
       Novo registro
      </button>
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem; gap: 0.35rem; flex-wrap: wrap">
       <strong>
        Dutos Registrados:
       </strong>
       <div style="display: flex; gap: 0.3rem; align-items: center; flex-wrap: wrap">
        <label class="control-label" for="filterActivePipelines">
         Situação dos dutos
        </label>
        <select id="filterActivePipelines" style="padding: 0.15rem 0.35rem">
         <option value="all">
          Todos
         </option>
         <option value="active">
          Ativos
         </option>
         <option value="inactive">
          Inativos
         </option>
        </select>
        <label class="control-label" for="searchPipelines">
         Buscar duto...
        </label>
        <input id="searchPipelines" placeholder="Buscar duto..." style="padding: 0.2rem 0.4rem" type="text"/>
       </div>
      </div>
      <p class="table-scroll-hint" hidden="">
       Deslize a tabela ou use as setas do teclado para consultar as demais colunas.
      </p>
      <div aria-label="Dutos — tabela com rolagem horizontal" class="hub-list-container" data-scroll-table="" role="region" tabindex="0">
       <table class="data-table" id="tablePipelines">
        <thead>
         <tr>
          <th>
           Duto
          </th>
          <th>
           Console
          </th>
          <th>
           UOs
          </th>
          <th>
           Situação
          </th>
          <th style="text-align: right">
           Ações
          </th>
         </tr>
        </thead>
        <tbody id="tbodyPipelines">
        </tbody>
       </table>
      </div>
     </div>
    </div>
   </div>
   <!-- PAINEL 2: UOS & TIPOS DE EQUIPAMENTOS -->
   <div class="cadastro-hub-card" data-cat-group="uos,types" id="hubCardUOsTypes">
    <div class="hub-header">
     <div class="hub-title">
      <svg aria-hidden="true" fill="none" focusable="false" height="18" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="18">
       <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z">
       </path>
       <polyline points="9 22 9 12 15 12 15 22">
       </polyline>
      </svg>
      <span>
       2. Unidades Operacionais (UOs) &amp; Tipos
      </span>
     </div>
    </div>
    <!-- SUB-SECTION: UOs -->
    <div class="catalog-category" data-cat-item="uos" data-editor-open="false" id="subSectionUOs">
     <!-- Form UO (Permite digitar UMA ou VÁRIAS UOs de uma vez separadas por vírgula ou linha) -->
     <form class="catalog-editor" id="formUO" style="background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 6px; padding: 0.75rem">
      <button class="btn btn-outline catalog-back" data-catalog-back="formUO" type="button">
       Voltar à lista
      </button>
      <input id="uoEditId" type="hidden" value=""/>
      <label for="inputUOName">
       Cadastrar UOs (Digite uma ou várias separadas por vírgula):
      </label>
      <div style="display: flex; gap: 0.4rem; margin-top: 0.25rem; flex-wrap: wrap">
       <input id="inputUOName" placeholder="Ex: REFAP, TEDEP, REPLAN, TEBAR" required="" style="padding: 0.35rem 0.6rem" type="text"/>
       <button class="btn btn-primary btn-sm" id="btnSubmitUO" type="submit">
        Salvar UO
       </button>
       <button class="btn btn-secondary btn-sm" id="btnCancelUOEdit" style="display: none" type="button">
        Cancelar
       </button>
      </div>
      <div class="form-help">
       Você pode cadastrar várias UOs juntas digitando nomes separados por vírgula.
      </div>
     </form>
     <!-- UOs List -->
     <div class="catalog-list" style="margin-top: 0.5rem">
      <button class="btn btn-outline catalog-new" data-catalog-new="formUO" type="button">
       Novo registro
      </button>
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem; gap: 0.35rem; flex-wrap: wrap">
       <strong>
        UOs Cadastradas:
       </strong>
       <div style="display: flex; gap: 0.3rem; align-items: center; flex-wrap: wrap">
        <label class="control-label" for="filterActiveUOs">
         Situação das UOs
        </label>
        <select id="filterActiveUOs" style="padding: 0.15rem 0.35rem">
         <option value="all">
          Todos
         </option>
         <option value="active">
          Ativos
         </option>
         <option value="inactive">
          Inativos
         </option>
        </select>
        <label class="control-label" for="searchUOs">
         Buscar UO...
        </label>
        <input id="searchUOs" placeholder="Buscar UO..." style="padding: 0.2rem 0.4rem" type="text"/>
       </div>
      </div>
      <p class="table-scroll-hint" hidden="">
       Deslize a tabela ou use as setas do teclado para consultar as demais colunas.
      </p>
      <div aria-label="Unidades operacionais — tabela com rolagem horizontal" class="hub-list-container" data-scroll-table="" role="region" tabindex="0">
       <table class="data-table" id="tableUOs">
        <thead>
         <tr>
          <th>
           Nome da UO
          </th>
          <th>
           Dutos
          </th>
          <th>
           Tipos
          </th>
          <th>
           Situação
          </th>
          <th style="text-align: right">
           Ações
          </th>
         </tr>
        </thead>
        <tbody id="tbodyUOs">
        </tbody>
       </table>
      </div>
     </div>
    </div>
    <!-- SUB-SECTION: EQUIPMENT TYPES -->
    <div class="catalog-category" data-cat-item="types" data-editor-open="false" id="subSectionTypes">
     <!-- Form Tipo de Equipamento -->
     <form class="catalog-editor" id="formEquipmentType" style="background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 6px; padding: 0.75rem; margin-top: 0.5rem">
      <button class="btn btn-outline catalog-back" data-catalog-back="formEquipmentType" type="button">
       Voltar à lista
      </button>
      <input id="equipmentTypeEditId" type="hidden" value=""/>
      <div style="font-weight: 700; margin-bottom: 0.4rem">
       Novo Tipo de Equipamento:
      </div>
      <div style="display: grid; gap: 0.4rem">
       <div class="form-group">
        <label for="selectEquipmentTypeUO">
         UO Vinculada
         <span class="required">
          *
         </span>
        </label>
        <select id="selectEquipmentTypeUO" required="" style="padding: 0.2rem 0.5rem">
         <option value="">
          Selecione a UO...
         </option>
        </select>
       </div>
       <div class="form-group">
        <label for="inputEquipmentTypeName">
         Tipo
         <span class="required">
          *
         </span>
        </label>
        <input id="inputEquipmentTypeName" placeholder="Ex: Tanque, Bomba" required="" style="padding: 0.2rem 0.5rem" type="text"/>
       </div>
      </div>
      <div style="display: flex; justify-content: flex-end; gap: 0.4rem; margin-top: 0.4rem; flex-wrap: wrap">
       <button class="btn btn-secondary btn-sm" id="btnCancelEquipmentTypeEdit" style="display: none" type="button">
        Cancelar
       </button>
       <button class="btn btn-primary btn-sm" id="btnSubmitEquipmentType" type="submit">
        Salvar Tipo
       </button>
      </div>
     </form>
     <!-- Tipos List -->
     <div class="catalog-list" style="margin-top: 0.5rem">
      <button class="btn btn-outline catalog-new" data-catalog-new="formEquipmentType" type="button">
       Novo registro
      </button>
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem; gap: 0.35rem; flex-wrap: wrap">
       <strong>
        Tipos por UO:
       </strong>
       <div style="display: flex; gap: 0.3rem; align-items: center; flex-wrap: wrap">
        <label class="control-label" for="filterActiveEquipmentTypes">
         Situação dos tipos
        </label>
        <select id="filterActiveEquipmentTypes" style="padding: 0.15rem 0.35rem">
         <option value="all">
          Todos
         </option>
         <option value="active">
          Ativos
         </option>
         <option value="inactive">
          Inativos
         </option>
        </select>
        <label class="control-label" for="searchEquipmentTypes">
         Buscar tipo...
        </label>
        <input id="searchEquipmentTypes" placeholder="Buscar tipo..." style="padding: 0.2rem 0.4rem" type="text"/>
       </div>
      </div>
      <p class="table-scroll-hint" hidden="">
       Deslize a tabela ou use as setas do teclado para consultar as demais colunas.
      </p>
      <div aria-label="Tipos de equipamentos — tabela com rolagem horizontal" class="hub-list-container" data-scroll-table="" role="region" tabindex="0">
       <table class="data-table" id="tableEquipmentTypes">
        <thead>
         <tr>
          <th>
           Tipo
          </th>
          <th>
           UO
          </th>
          <th>
           TAGs
          </th>
          <th>
           Situação
          </th>
          <th style="text-align: right">
           Ações
          </th>
         </tr>
        </thead>
        <tbody id="tbodyEquipmentTypes">
        </tbody>
       </table>
      </div>
     </div>
    </div>
   </div>
   <!-- PAINEL 3: TAGS DE EQUIPAMENTOS -->
   <div class="cadastro-hub-card catalog-category" data-cat-group="tags" data-cat-item="tags" data-editor-open="false" id="hubCardTags">
    <div class="hub-header">
     <div class="hub-title">
      <svg aria-hidden="true" fill="none" focusable="false" height="18" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="18">
       <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z">
       </path>
       <line x1="7" x2="7.01" y1="7" y2="7">
       </line>
      </svg>
      <span>
       3. TAGs de Equipamentos
      </span>
     </div>
    </div>
    <!-- Form TAG -->
    <form class="catalog-editor" id="formEquipmentTag" style="background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 6px; padding: 0.75rem">
     <button class="btn btn-outline catalog-back" data-catalog-back="formEquipmentTag" type="button">
      Voltar à lista
     </button>
     <input id="tagEditId" type="hidden" value=""/>
     <div style="font-weight: 700; margin-bottom: 0.4rem">
      Novo / Editar TAG:
     </div>
     <div class="form-group" style="margin-bottom: 0.4rem">
      <label for="selectTagUO">
       Unidade Operacional (UO)
       <span class="required">
        *
       </span>
      </label>
      <select id="selectTagUO" required="" style="padding: 0.2rem 0.5rem">
       <option value="">
        Selecione a UO...
       </option>
      </select>
     </div>
     <div class="form-group" style="margin-bottom: 0.4rem">
      <label for="selectTagType">
       Tipo de Equipamento
       <span class="required">
        *
       </span>
      </label>
      <select disabled="" id="selectTagType" required="" style="padding: 0.2rem 0.5rem">
       <option value="">
        Selecione primeiro a UO...
       </option>
      </select>
     </div>
     <div class="form-group">
      <label for="inputTagCode">
       Código do TAG
       <span class="required">
        *
       </span>
      </label>
      <input id="inputTagCode" placeholder="Ex: TQ-804, BB-101A" required="" style="padding: 0.35rem 0.6rem" type="text"/>
      <div class="form-help">
       Regra global: cada TAG pertence exclusivamente a uma única UO.
      </div>
     </div>
     <div style="display: flex; justify-content: flex-end; gap: 0.4rem; margin-top: 0.6rem; flex-wrap: wrap">
      <button class="btn btn-secondary btn-sm" id="btnCancelTagEdit" style="display: none" type="button">
       Cancelar
      </button>
      <button class="btn btn-primary btn-sm" id="btnSubmitTag" type="submit">
       Salvar TAG
      </button>
     </div>
    </form>
    <!-- TAGs List -->
    <div class="catalog-list">
     <button class="btn btn-outline catalog-new" data-catalog-new="formEquipmentTag" type="button">
      Novo registro
     </button>
     <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem; gap: 0.35rem; flex-wrap: wrap">
      <strong>
       TAGs Registrados:
      </strong>
      <div style="display: flex; gap: 0.3rem; align-items: center; flex-wrap: wrap">
       <label class="control-label" for="filterActiveTags">
        Situação das TAGs
       </label>
       <select id="filterActiveTags" style="padding: 0.15rem 0.35rem">
        <option value="all">
         Todos
        </option>
        <option value="active">
         Ativos
        </option>
        <option value="inactive">
         Inativos
        </option>
       </select>
       <label class="control-label" for="searchTags">
        Buscar TAG...
       </label>
       <input data-alias="searchEquipmentTags" id="searchTags" placeholder="Buscar TAG..." style="padding: 0.2rem 0.4rem" type="text"/>
      </div>
     </div>
     <p class="table-scroll-hint" hidden="">
      Deslize a tabela ou use as setas do teclado para consultar as demais colunas.
     </p>
     <div aria-label="TAGs de equipamentos — tabela com rolagem horizontal" class="hub-list-container" data-scroll-table="" role="region" tabindex="0">
      <table class="data-table" id="tableEquipmentTags">
       <thead>
        <tr>
         <th>
          TAG
         </th>
         <th>
          UO
         </th>
         <th>
          Tipo
         </th>
         <th>
          Situação
         </th>
         <th style="text-align: right">
          Ações
         </th>
        </tr>
       </thead>
       <tbody id="tbodyEquipmentTags">
       </tbody>
      </table>
     </div>
    </div>
   </div>
  </div>
  <aside aria-label="Vínculos do registro" class="context-panel" id="cadastrosRelationsPanel">
   <h2>
    Vínculos do registro
   </h2>
  </aside>
 </section>
 <!-- ==================== VIEW 6: CONFIGURAÇÕES DE ALERTAS ==================== -->
 <section aria-labelledby="viewConfigAlertsHeading" class="view-section" id="viewConfigAlerts">
  <h2 class="view-heading" id="viewConfigAlertsHeading">
   Configurações de alertas
  </h2>
  <!-- Notice on browser restrictions -->
  <div class="notice-banner">
   <svg aria-hidden="true" fill="none" focusable="false" height="24" stroke="currentColor" stroke-width="2" style="flex-shrink: 0" viewbox="0 0 24 24" width="24">
    <circle cx="12" cy="12" r="10">
    </circle>
    <line x1="12" x2="12" y1="16" y2="12">
    </line>
    <line x1="12" x2="12.01" y1="8" y2="8">
    </line>
   </svg>
   <div>
    <strong style="color: var(--text-main)">
     Limitações do Ambiente de Navegador Web:
    </strong>
    <ul style="margin-left: 1.25rem; margin-top: 0.25rem; line-height: 1.4">
     <li>
      A aplicação precisa permanecer aberta em uma aba ativa para monitorar e executar os alarmes locais.
     </li>
     <li>
      Se o navegador for fechado, os alarmes não soarão em segundo plano sem a aplicação rodando.
     </li>
     <li>
      O navegador pode bloquear o áudio até que ocorra uma interação do usuário com a página (clique).
     </li>
     <li>
      Notificações do sistema operacional exigem que a permissão seja expressamente concedida pelo controlador.
     </li>
     <li>
      Políticas de segurança do sistema operacional e navegadores impedem maximização ou foco forçado de janelas.
     </li>
    </ul>
   </div>
  </div>
  <div class="card">
   <div class="card-header">
    <div class="card-title">
     Parâmetros Gerais de Alarmes, Exibição e Notificações
    </div>
   </div>
   <form id="formAlertSettings">
    <div class="form-grid">
     <!-- Toggles -->
     <!-- Repetition Settings -->
     <details class="settings-group" open="">
      <summary>
       Antecedência e repetição
      </summary>
      <div class="form-group">
       <label for="inputDefaultLeadTime">
        Antecedência Padrão dos Alarmes (minutos)
       </label>
       <input id="inputDefaultLeadTime" max="1440" min="0" type="number" value="15"/>
       <div class="form-help">
        Tempo prévio para alertar o controlador antes do horário
       </div>
      </div>
      <div class="form-group span-full" style="border-top: 1px solid var(--border-color); padding-top: 1rem">
       <label class="form-checkbox" style="font-weight: 700">
        <input checked="" id="checkSettingRepeat" type="checkbox"/>
        <span>
         Repetir Alarme até Reconhecimento
        </span>
       </label>
       <div style="display: flex; gap: 1rem; margin-top: 0.5rem; flex-wrap: wrap">
        <div style="flex: 1">
         <label for="inputSettingRepeatInterval">
          Intervalo de Repetição (minutos)
         </label>
         <input id="inputSettingRepeatInterval" max="60" min="1" type="number" value="2"/>
        </div>
        <div style="flex: 1">
         <label for="inputSettingMaxRepeats">
          Número Máximo de Repetições
         </label>
         <input id="inputSettingMaxRepeats" max="20" min="1" type="number" value="5"/>
        </div>
       </div>
      </div>
     </details>
     <details class="settings-group" open="">
      <summary>
       Som e volume
      </summary>
      <div class="form-group">
       <label for="selectSoundType">
        Tipo de Sinal Sonoro
       </label>
       <select id="selectSoundType">
        <option value="chime">
         Chime Harmônico (Sutil e Melódico)
        </option>
        <option value="beep">
         Beep Duplo (Clássico)
        </option>
        <option value="siren">
         Sirene Operacional (Urgência)
        </option>
        <option value="blip">
         Blip Suave
        </option>
       </select>
      </div>
      <div class="form-group">
       <label for="rangeSoundVolume">
        Volume do Alarme:
        <span id="labelVolumeValue">
         80%
        </span>
       </label>
       <input id="rangeSoundVolume" max="100" min="0" style="padding: 0" type="range" value="80"/>
      </div>
      <button class="btn btn-outline btn-sm" id="btnTestSound" type="button">
       <svg aria-hidden="true" fill="none" focusable="false" height="14" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="14">
        <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5">
        </polygon>
        <path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07">
        </path>
       </svg>
       <span>
        Testar Som
       </span>
      </button>
     </details>
     <details class="settings-group" open="">
      <summary>
       Aparência e layout
      </summary>
      <div class="form-group">
       <label for="selectSettingsViewMode">
        Modo de Exibição / Layout da Interface
       </label>
       <select id="selectSettingsViewMode">
        <option value="auto">
         Automático (Recomendado - Detecta a tela)
        </option>
        <option value="compact">
         Compacto (Alta Densidade Operacional)
        </option>
        <option value="mobile">
         Celular (320px a 767px)
        </option>
        <option value="tablet">
         Tablet (768px a 1199px)
        </option>
        <option value="conventional">
         Monitor convencional (1200–1919 px)
        </option>
        <option value="widescreen">
         Widescreen (1920–2559 px)
        </option>
        <option value="ultrawide">
         Ultrawide (2560 px ou mais)
        </option>
       </select>
       <div class="form-help">
        Permite forçar um formato específico ou manter adaptação automática
       </div>
      </div>
      <div class="form-group">
       <label for="selectSettingsTheme">
        Tema Visual Operacional
       </label>
       <select id="selectSettingsTheme">
        <option value="dark">
         Tema 1: Controle Escuro (Padrão Noturno 24h)
        </option>
        <option value="light">
         Tema 2: Profissional Claro (Ambientes Iluminados)
        </option>
        <option value="industrial">
         Tema 3: Industrial Alto Contraste (Máxima Legibilidade)
        </option>
       </select>
       <div class="form-help">
        Contraste calibrado para turnos prolongados
       </div>
      </div>
     </details>
     <details class="settings-group" open="">
      <summary>
       Canais de alerta
      </summary>
      <div class="form-group span-full">
       <label style="margin-bottom: 0.5rem">
        Canais e Formas de Alerta Ativos
       </label>
       <div style="display: grid; gap: 0.75rem">
        <label class="form-checkbox">
         <input checked="" id="checkSettingSound" type="checkbox"/>
         <span>
          Sinal Sonoro Local (Web Audio API)
         </span>
        </label>
        <label class="form-checkbox">
         <input checked="" id="checkSettingVisualModal" type="checkbox"/>
         <span>
          Janela Modal Flutuante de Alerta
         </span>
        </label>
        <label class="form-checkbox">
         <input checked="" id="checkSettingHighlightCard" type="checkbox"/>
         <span>
          Destaque Visual do Cartão na Lista
         </span>
        </label>
        <label class="form-checkbox">
         <input checked="" id="checkSettingPulsing" type="checkbox"/>
         <span>
          Efeito Visual de Pulsação Luminosa
         </span>
        </label>
        <label class="form-checkbox">
         <input checked="" id="checkSettingChangeTitle" type="checkbox"/>
         <span>
          Alteração Dinâmica do Título da Aba
         </span>
        </label>
        <label class="form-checkbox">
         <input id="checkSettingNotification" type="checkbox"/>
         <span>
          Notificação do Navegador (Web Notifications)
         </span>
        </label>
       </div>
      </div>
      <button class="btn btn-outline btn-sm" id="btnTestVisual" type="button">
       <svg aria-hidden="true" fill="none" focusable="false" height="14" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="14">
        <circle cx="12" cy="12" r="10">
        </circle>
        <line x1="12" x2="12" y1="8" y2="12">
        </line>
        <line x1="12" x2="12.01" y1="16" y2="16">
        </line>
       </svg>
       <span>
        Testar Alerta Visual
       </span>
      </button>
      <button class="btn btn-outline btn-sm" id="btnRequestNotifPermission" type="button">
       <svg aria-hidden="true" fill="none" focusable="false" height="14" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="14">
        <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9">
        </path>
        <path d="M13.73 21a2 2 0 0 1-3.46 0">
        </path>
       </svg>
       <span id="btnRequestNotifText">
        Permissão de Notificações
       </span>
      </button>
      <button class="btn btn-warning btn-sm" id="btnTestNotif" type="button">
       <svg aria-hidden="true" fill="none" focusable="false" height="14" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="14">
        <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9">
        </path>
        <path d="M13.73 21a2 2 0 0 1-3.46 0">
        </path>
       </svg>
       <span>
        Testar Notificação do Navegador
       </span>
      </button>
     </details>
     <details class="settings-group" open="">
      <summary>
       Nome do Controlador neste Computador
      </summary>
      <div class="form-group">
       <label for="inputSettingsUserName">
        Nome do Controlador neste Computador
       </label>
       <input id="inputSettingsUserName" placeholder="Usuário local" type="text"/>
       <div class="form-help">
        Utilizado para rastreabilidade nas auditorias e registros
       </div>
      </div>
     </details>
     <div class="form-group">
      <label for="inputBackupReminderDays">
       Lembrar backup após (dias)
      </label>
      <input id="inputBackupReminderDays" max="3650" min="1" type="number" value="7"/>
     </div>
    </div>
    <!-- Test Actions Bar -->
    <div style="border-top: 1px solid var(--border-color); padding-top: 1.25rem; margin-top: 1.25rem; display: flex; gap: 0.6rem; flex-wrap: wrap; justify-content: space-between; align-items: center">
     <div style="display: flex; gap: 0.5rem; flex-wrap: wrap">
      <!-- Prominent Test Notification Button -->
     </div>
     <div style="display: flex; gap: 0.5rem; flex-wrap: wrap">
      <button class="btn btn-secondary btn-sm" id="btnResetAlertSettings" type="button">
       Restaurar Padrões
      </button>
      <button class="btn btn-primary btn-sm" type="submit">
       Salvar Configurações
      </button>
     </div>
    </div>
   </form>
  </div>
  <aside aria-label="Prévia das preferências" class="context-panel" id="settingsPreviewPanel">
   <h2>
    Prévia das preferências
   </h2>
  </aside>
 </section>
 <!-- ==================== VIEW 7: CONFIGURAÇÕES DE CORES ==================== -->
 <section aria-labelledby="viewConfigColorsHeading" class="view-section" id="viewConfigColors">
  <h2 class="view-heading" id="viewConfigColorsHeading">
   Faixas de tempo e cores
  </h2>
  <div class="card color-workspace">
   <div class="card-header">
    <div>
     <div class="card-title">
      Classificação por Faixas de Tempo e Cores
     </div>
     <div class="card-subtitle">
      As faixas indicam a proximidade dos eventos. Intervalos são ordenados e contíguos sem sobreposições ou lacunas.
     </div>
    </div>
    <button class="btn btn-outline btn-sm" id="btnResetColorRanges" type="button">
     Restaurar Faixas Padrão
    </button>
   </div>
   <div class="notice-banner">
    <svg aria-hidden="true" fill="none" focusable="false" height="20" stroke="currentColor" stroke-width="2" style="flex-shrink: 0" viewbox="0 0 24 24" width="20">
     <circle cx="12" cy="12" r="10">
     </circle>
     <line x1="12" x2="12" y1="8" y2="12">
     </line>
     <line x1="12" x2="12.01" y1="16" y2="16">
     </line>
    </svg>
    <div>
     <strong>
      Condição "Atrasado" tratada separadamente:
     </strong>
     Todo evento cujo horário previsto já foi ultrapassado é automaticamente classificado como
     <strong>
      Atrasado (Vermelho Escuro)
     </strong>
     e priorizado no topo, independentemente das faixas de tempo futuro.
    </div>
   </div>
   <!-- Visual Preview Bar & Chain (Section 14) -->
   <div style="margin-top: 1rem">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem">
     <label style="font-weight: 700">
      Prévia Visual das Faixas de Tempo (0 a 60+ minutos):
     </label>
     <span id="colorChainPreview" style="font-weight: 700">
      Encadeamento: 0 ─ 15 ─ 30 ─ 45 ─ 60 ─ Normal
     </span>
    </div>
    <div class="color-preview-bar" id="colorPreviewBar">
     <!-- Dynamically populated preview blocks -->
    </div>
   </div>
   <!-- Mobile Cards for Color Ranges (Section 14) -->
   <div class="color-range-cards" id="containerColorRangeCards">
   </div>
   <!-- Table of Ranges -->
   <p class="table-scroll-hint" hidden="">
    Deslize a tabela ou use as setas do teclado para consultar as demais colunas.
   </p>
   <div aria-label="Faixas de tempo — tabela com rolagem horizontal" class="table-responsive" data-scroll-table="" id="tableColorRangesWrapper" role="region" style="margin-top: 1rem" tabindex="0">
    <table class="data-table" id="tableColorRanges">
     <thead>
      <tr>
       <th>
        Nome da Faixa
       </th>
       <th>
        Amostra
       </th>
       <th>
        Limite Inicial (min)
       </th>
       <th>
        Limite Final (min)
       </th>
       <th>
        Piscar / Pulsar
       </th>
       <th>
        Sinal Sonoro
       </th>
       <th>
        Prioridade
       </th>
       <th style="text-align: right">
        Ações
       </th>
      </tr>
     </thead>
     <tbody id="tbodyColorRanges">
      <!-- Dynamically populated -->
     </tbody>
    </table>
   </div>
   <!-- Add/Edit Color Range Form -->
   <div class="range-editor" style="margin-top: 1.5rem; border-top: 1px solid var(--border-color); padding-top: 1.25rem">
    <h4 id="titleFormRange" style="font-weight: 700; margin-bottom: 0.75rem">
     Editar / Nova Faixa de Tempo
    </h4>
    <form id="formColorRange">
     <input id="rangeEditId" type="hidden" value=""/>
     <div class="form-grid">
      <div class="form-group">
       <label for="inputRangeName">
        Nome da Faixa
        <span class="required">
         *
        </span>
       </label>
       <input id="inputRangeName" placeholder="Ex: Crítico, Urgente" required="" type="text"/>
      </div>
      <div class="form-group">
       <label for="inputRangeColor">
        Cor de Destaque
        <span class="required">
         *
        </span>
       </label>
       <div style="display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap">
        <input id="inputRangeColor" style="padding: 2px; cursor: pointer" type="color" value="#dc2626"/>
        <label class="control-label" for="inputRangeColorText">
         Código hexadecimal da cor
        </label>
        <input id="inputRangeColorText" required="" style="flex: 1" type="text" value="#dc2626"/>
       </div>
      </div>
      <div class="form-group">
       <label for="inputRangeMin">
        Limite Inicial (minutos)
        <span class="required">
         *
        </span>
       </label>
       <input id="inputRangeMin" max="99999" min="0" required="" type="number"/>
      </div>
      <div class="form-group">
       <label for="inputRangeMax">
        Limite Final (minutos)
        <span class="required">
         *
        </span>
       </label>
       <input id="inputRangeMax" max="999999" min="1" required="" type="number"/>
      </div>
      <div class="form-group">
       <label for="inputRangePriority">
        Prioridade Visual (1 = Mais alta)
       </label>
       <input id="inputRangePriority" max="10" min="1" required="" type="number" value="1"/>
      </div>
      <div class="form-group" style="justify-content: center">
       <label class="form-checkbox">
        <input id="checkRangeBlink" type="checkbox"/>
        <span>
         Piscar / Pulsar Eventos nesta Faixa
        </span>
       </label>
       <label class="form-checkbox" style="margin-top: 0.35rem">
        <input id="checkRangeSound" type="checkbox"/>
        <span>
         Emitir Alerta Sonoro nesta Faixa
        </span>
       </label>
      </div>
     </div>
     <div style="display: flex; justify-content: flex-end; gap: 0.5rem; margin-top: 1rem; flex-wrap: wrap">
      <button class="btn btn-secondary btn-sm" id="btnCancelRangeEdit" style="display: none" type="button">
       Cancelar
      </button>
      <button class="btn btn-primary btn-sm" id="btnSubmitRange" type="submit">
       Salvar Faixa de Cor
      </button>
     </div>
    </form>
   </div>
   <aside aria-label="Exemplo de aparência" class="context-panel" id="rangeLivePreview">
    <h2>
     Exemplo de aparência
    </h2>
   </aside>
  </div>
 </section>
 <!-- ==================== VIEW 8: BACKUP E DADOS ==================== -->
 <section aria-labelledby="viewBackupHeading" class="view-section" id="viewBackup">
  <h2 class="view-heading" id="viewBackupHeading">
   Backup e dados
  </h2>
  <div class="card backup-workspace">
   <div class="card-header">
    <div>
     <div class="card-title">
      Backup Completo e Restauração de Dados
     </div>
     <div class="card-subtitle">
      Todos os cadastros, eventos, históricos e configurações em arquivo JSON
     </div>
    </div>
    <span id="labelLastBackupDate" style="color: var(--text-muted)">
     Último backup: Nunca
    </span>
   </div>
   <div class="backup-operations">
    <!-- Export Section -->
    <div style="background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 8px; padding: 1.25rem">
     <h4 style="font-weight: 700; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.4rem">
      <svg aria-hidden="true" fill="none" focusable="false" height="18" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="18">
       <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4">
       </path>
       <polyline points="7 10 12 15 17 10">
       </polyline>
       <line x1="12" x2="12" y1="15" y2="3">
       </line>
      </svg>
      <span>
       Exportar Backup do Sistema
      </span>
     </h4>
     <p style="color: var(--text-secondary); margin-bottom: 1rem">
      Gera um arquivo JSON padronizado contendo todas as tabelas, configurações, consoles, dutos, UOs, TAGs e histórico completo.
     </p>
     <button class="btn btn-primary" id="btnExportJSON" style="width: 100%" type="button">
      <span>
       Baixar Backup Completo (JSON)
      </span>
     </button>
    </div>
    <!-- Import Section -->
    <div style="background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 8px; padding: 1.25rem">
     <h4 style="font-weight: 700; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.4rem">
      <svg aria-hidden="true" fill="none" focusable="false" height="18" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="18">
       <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4">
       </path>
       <polyline points="17 8 12 3 7 8">
       </polyline>
       <line x1="12" x2="12" y1="3" y2="15">
       </line>
      </svg>
      <span>
       Restaurar / Importar Backup
      </span>
     </h4>
     <p style="color: var(--text-secondary); margin-bottom: 0.75rem">
      Selecione um arquivo JSON de backup para validar e carregar na base local.
     </p>
     <label class="control-label" for="inputImportBackupFile">
      Arquivo de backup JSON
     </label>
     <input accept=".json" id="inputImportBackupFile" style="margin-bottom: 0.75rem" type="file"/>
     <p aria-live="polite" class="form-help" id="backupSelectedFileName">
      Nenhum arquivo selecionado.
     </p>
     <div style="display: flex; gap: 0.5rem; flex-wrap: wrap">
      <button class="btn btn-secondary" disabled="" id="btnTriggerImportValidate" style="flex: 1" type="button">
       <span>
        Validar Arquivo
       </span>
      </button>
     </div>
    </div>
   </div>
   <!-- Export CSV Section -->
   <div style="margin-top: 1.5rem; border-top: 1px solid var(--border-color); padding-top: 1.25rem">
    <h4 style="font-weight: 700; margin-bottom: 0.75rem">
     Exportação de Relatórios em CSV (Excel)
    </h4>
    <p style="color: var(--text-secondary); margin-bottom: 1rem">
     Arquivos CSV formatados para Microsoft Excel (separador ponto e vírgula, codificação UTF-8 com BOM e formatos brasileiros de data e hora).
    </p>
    <div style="display: flex; gap: 0.75rem; flex-wrap: wrap">
     <button class="btn btn-outline btn-sm" id="btnExportCSVAllPending" type="button">
      <svg aria-hidden="true" fill="none" focusable="false" height="14" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="14">
       <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z">
       </path>
       <polyline points="14 2 14 8 20 8">
       </polyline>
      </svg>
      <span>
       Eventos Pendentes (CSV)
      </span>
     </button>
     <button class="btn btn-outline btn-sm" id="btnExportCSVAllCompleted" type="button">
      <svg aria-hidden="true" fill="none" focusable="false" height="14" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="14">
       <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z">
       </path>
       <polyline points="14 2 14 8 20 8">
       </polyline>
      </svg>
      <span>
       Eventos Concluídos (CSV)
      </span>
     </button>
     <button class="btn btn-outline btn-sm" id="btnExportCSVCadastros" type="button">
      <svg aria-hidden="true" fill="none" focusable="false" height="14" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="14">
       <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z">
       </path>
       <polyline points="14 2 14 8 20 8">
       </polyline>
      </svg>
      <span>
       Estrutura Cadastral (CSV)
      </span>
     </button>
    </div>
   </div>
   <!-- Demonstration & Maintenance -->
   <div class="maintenance-panel" style="margin-top: 1.5rem; border-top: 1px solid var(--border-color); padding-top: 1.25rem">
    <h4 style="font-weight: 700; margin-bottom: 0.75rem">
     Massa de Dados e Demonstração Operacional
    </h4>
    <div style="display: flex; gap: 0.75rem; flex-wrap: wrap">
     <button class="btn btn-secondary btn-sm" id="btnLoadDemoData" type="button">
      <svg aria-hidden="true" fill="none" focusable="false" height="14" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="14">
       <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20">
       </path>
       <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z">
       </path>
      </svg>
      <span>
       Carregar Dados de Demonstração
      </span>
     </button>
     <button class="btn btn-danger btn-sm" id="btnWipeAllData" type="button">
      <svg aria-hidden="true" fill="none" focusable="false" height="14" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="14">
       <polyline points="3 6 5 6 21 6">
       </polyline>
       <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2">
       </path>
      </svg>
      <span>
       Apagar Todos os Dados
      </span>
     </button>
    </div>
   </div>
   <aside aria-label="Estado da base local" class="context-panel" id="backupContextPanel">
    <h2>
     Estado da base local
    </h2>
   </aside>
  </div>
 </section>
 <!-- ==================== VIEW 9: DIAGNÓSTICO ==================== -->
 <section aria-labelledby="viewDiagnosticHeading" class="view-section" id="viewDiagnostic">
  <h2 class="view-heading" id="viewDiagnosticHeading">
   Diagnóstico
  </h2>
  <div class="card diagnostic-workspace">
   <div class="card-header">
    <div>
     <div class="card-title">
      Diagnóstico Técnico da Aplicação
     </div>
     <div class="card-subtitle">
      Verificação da integridade do IndexedDB, APIs do navegador e logs internos
     </div>
    </div>
    <button class="btn btn-outline btn-sm" id="btnCopyDiagnostic" type="button">
     <svg aria-hidden="true" fill="none" focusable="false" height="14" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="14">
      <rect height="13" rx="2" ry="2" width="13" x="9" y="9">
      </rect>
      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1">
      </path>
     </svg>
     <span>
      Copiar Diagnóstico
     </span>
    </button>
   </div>
   <div class="form-grid diagnostic-status" style="margin-bottom: 1.25rem">
    <div class="metric-card">
     <div class="metric-data">
      <div class="metric-value" id="diagAppVersion">
       —
      </div>
      <div class="metric-label">
       Versão da Aplicação
      </div>
     </div>
    </div>
    <div class="metric-card">
     <div class="metric-data">
      <div class="metric-value" id="diagDBStatus">
       Online
      </div>
      <div class="metric-label">
       IndexedDB (Esquema v1)
      </div>
     </div>
    </div>
    <div class="metric-card">
     <div class="metric-data">
      <div class="metric-value" id="diagAudioStatus">
       Suspenso
      </div>
      <div class="metric-label">
       Web Audio API
      </div>
     </div>
    </div>
    <div class="metric-card">
     <div class="metric-data">
      <div class="metric-value" id="diagNotifStatus">
       Pendente
      </div>
      <div class="metric-label">
       Web Notifications
      </div>
     </div>
    </div>
   </div>
   <section class="diagnostic-collections">
    <h4 style="font-weight: 700; margin-bottom: 0.5rem">
     Contagem de Registros por Coleção
    </h4>
    <p class="table-scroll-hint" hidden="">
     Deslize a tabela ou use as setas do teclado para consultar as demais colunas.
    </p>
    <div aria-label="Coleções locais — tabela com rolagem horizontal" class="table-responsive" data-scroll-table="" role="region" style="margin-bottom: 1.5rem" tabindex="0">
     <table class="data-table" id="tableDiagCollections">
      <thead>
       <tr>
        <th>
         Coleção (Object Store)
        </th>
        <th>
         Finalidade
        </th>
        <th>
         Total Registros
        </th>
        <th>
         Ativos
        </th>
        <th>
         Inativos
        </th>
       </tr>
      </thead>
      <tbody id="tbodyDiagCollections">
       <!-- Dynamically populated -->
      </tbody>
     </table>
    </div>
   </section>
   <section class="diagnostic-logs">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; flex-wrap: wrap">
     <h4 style="font-weight: 700">
      Log Interno de Erros e Eventos
     </h4>
     <button class="btn btn-outline btn-sm" id="btnClearDiagLogs" type="button">
      Limpar Logs
     </button>
    </div>
    <p class="table-scroll-hint" hidden="">
     Deslize a tabela ou use as setas do teclado para consultar as demais colunas.
    </p>
    <div aria-label="Logs de diagnóstico — tabela com rolagem horizontal" class="table-responsive" data-scroll-table="" role="region" tabindex="0">
     <table class="data-table" id="tableDiagLogs">
      <thead>
       <tr>
        <th>
         Data / Hora
        </th>
        <th>
         Contexto
        </th>
        <th>
         Mensagem
        </th>
        <th>
         Detalhes Técnicos
        </th>
       </tr>
      </thead>
      <tbody id="tbodyDiagLogs">
       <tr>
        <td colspan="4" style="text-align: center; color: var(--text-muted); padding: 1.5rem">
         Nenhum erro registrado no sistema.
        </td>
       </tr>
      </tbody>
     </table>
    </div>
   </section>
  </div>
 </section>
 <!-- Barra de Navegação Inferior Fixa para Celular (Section 5.1) — único ponto de ação rápida (#fabAddEvent central) -->
 <nav aria-label="Navegação Rápida Mobile" class="mobile-bottom-nav" id="mobileBottomNav">
  <button class="bottom-nav-item active" data-target="viewDashboard" type="button">
   <svg aria-hidden="true" fill="none" focusable="false" height="20" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="20">
    <rect height="9" width="7" x="3" y="3">
    </rect>
    <rect height="5" width="7" x="14" y="3">
    </rect>
    <rect height="9" width="7" x="14" y="12">
    </rect>
    <rect height="5" width="7" x="3" y="16">
    </rect>
   </svg>
   <span>
    Painel
   </span>
  </button>
  <button class="bottom-nav-item" data-target="viewPendingEvents" type="button">
   <span class="bottom-nav-badge" id="badgeBottomNavPending">
    0
   </span>
   <svg aria-hidden="true" fill="none" focusable="false" height="20" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="20">
    <circle cx="12" cy="12" r="10">
    </circle>
    <polyline points="12 6 12 12 16 14">
    </polyline>
   </svg>
   <span>
    Pendentes
   </span>
  </button>
  <button aria-label="Nova Previsão" class="bottom-nav-fab" data-target="viewNewEvent" id="fabAddEvent" title="Nova Previsão Operacional" type="button">
   <svg aria-hidden="true" fill="none" focusable="false" height="24" stroke="currentColor" stroke-width="2.5" viewbox="0 0 24 24" width="24">
    <line x1="12" x2="12" y1="5" y2="19">
    </line>
    <line x1="5" x2="19" y1="12" y2="12">
    </line>
   </svg>
   <span>
    Novo
   </span>
  </button>
  <button class="bottom-nav-item" id="btnBottomNavMore" type="button">
   <svg aria-hidden="true" fill="none" focusable="false" height="20" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="20">
    <circle cx="12" cy="12" r="1">
    </circle>
    <circle cx="19" cy="12" r="1">
    </circle>
    <circle cx="5" cy="12" r="1">
    </circle>
   </svg>
   <span>
    Mais
   </span>
  </button>
 </nav>
</main>
<!-- ==================== MODALS ==================== -->
<!-- Modal 1: Disparo de Alerta Operacional -->
<div aria-labelledby="modalAlarmTitle" aria-modal="true" class="modal-overlay" id="modalAlarmTrigger" role="dialog">
 <div class="modal-box alarm-modal-box">
  <div class="modal-header alarm-modal-header">
   <h3 id="modalAlarmTitle">
    <svg aria-hidden="true" fill="none" focusable="false" height="22" stroke="currentColor" stroke-width="2.5" viewbox="0 0 24 24" width="22">
     <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2">
     </polygon>
    </svg>
    <span>
     ALERTA DE PREVISÃO OPERACIONAL!
    </span>
   </h3>
   <button aria-label="Fechar ALERTA DE PREVISÃO OPERACIONAL!" class="modal-close" id="btnCloseAlarmModal" type="button">
    ×
   </button>
  </div>
  <div class="modal-body">
   <div style="background: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444; padding: 0.85rem; border-radius: 4px; margin-bottom: 1rem">
    <div id="alarmModalHierarchy" style="font-weight: 700">
     CONSOLE | DUTO | UO | TAG
    </div>
    <div id="alarmModalDescription" style="font-weight: 800; color: var(--text-main); margin-top: 0.35rem">
     Descrição do Evento
    </div>
    <div id="alarmModalNotes" style="color: var(--text-secondary); margin-top: 0.35rem">
     Observações
    </div>
   </div>
   <div style="display: flex; justify-content: space-between; align-items: center; background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 6px; padding: 0.75rem 1rem; flex-wrap: wrap">
    <div>
     <div style="color: var(--text-muted)">
      Horário Previsto
     </div>
     <div id="alarmModalScheduledTime" style="font-weight: 700">
      --:--
     </div>
    </div>
    <div style="text-align: right">
     <div style="color: var(--text-muted)">
      Tempo Restante / Atraso
     </div>
     <div id="alarmModalCountdown" style="font-weight: 800">
      --
     </div>
    </div>
   </div>
  </div>
  <div class="modal-footer" style="flex-wrap: wrap">
   <button class="btn btn-warning" id="btnAlarmAcknowledge" type="button">
    <svg aria-hidden="true" fill="none" focusable="false" height="16" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="16">
     <polyline points="20 6 9 17 4 12">
     </polyline>
    </svg>
    <span>
     Reconhecer Alarme
    </span>
   </button>
   <button class="btn btn-secondary" id="btnAlarmSnoozePrompt" type="button">
    <svg aria-hidden="true" fill="none" focusable="false" height="16" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="16">
     <circle cx="12" cy="12" r="10">
     </circle>
     <polyline points="12 6 12 12 16 14">
     </polyline>
    </svg>
    <span>
     Adiar...
    </span>
   </button>
   <button class="btn btn-success" id="btnAlarmCompleteDirect" type="button">
    <svg aria-hidden="true" fill="none" focusable="false" height="16" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="16">
     <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14">
     </path>
     <polyline points="22 4 12 14.01 9 11.01">
     </polyline>
    </svg>
    <span>
     Concluir Evento
    </span>
   </button>
   <button class="btn btn-outline" id="btnAlarmOpenDetails" type="button">
    Abrir Detalhes
   </button>
  </div>
 </div>
</div>
<!-- Modal 2: Adiar Alarme (Snooze Prompt) -->
<div aria-labelledby="modalSnoozeHeading" aria-modal="true" class="modal-overlay" id="modalSnooze" role="dialog">
 <div class="modal-box">
  <div class="modal-header">
   <h3 id="modalSnoozeHeading">
    Adiar Alarme Operacional
   </h3>
   <button aria-label="Fechar Adiar Alarme Operacional" class="modal-close" id="btnCloseSnoozeModal" type="button">
    ×
   </button>
  </div>
  <div class="modal-body">
   <p style="color: var(--text-secondary); margin-bottom: 1rem">
    Selecione por quantos minutos deseja adiar este alerta. Um novo horário de disparo será agendado.
   </p>
   <div style="display: flex; gap: 0.5rem; margin-bottom: 1rem; flex-wrap: wrap">
    <button class="btn btn-outline btn-sm btn-quick-snooze" data-min="5" type="button">
     5 min
    </button>
    <button class="btn btn-outline btn-sm btn-quick-snooze" data-min="10" type="button">
     10 min
    </button>
    <button class="btn btn-outline btn-sm btn-quick-snooze" data-min="15" type="button">
     15 min
    </button>
    <button class="btn btn-outline btn-sm btn-quick-snooze" data-min="30" type="button">
     30 min
    </button>
   </div>
   <div class="form-group">
    <label for="inputSnoozeMinutes">
     Ou informe a quantidade de minutos:
    </label>
    <input id="inputSnoozeMinutes" max="1440" min="1" type="number" value="5"/>
   </div>
  </div>
  <div class="modal-footer">
   <button class="btn btn-secondary" id="btnCancelSnooze" type="button">
    Cancelar
   </button>
   <button class="btn btn-primary" id="btnConfirmSnooze" type="button">
    Confirmar Adiamento
   </button>
  </div>
 </div>
</div>
<!-- Modal 3: Concluir Evento -->
<div aria-labelledby="modalCompleteEventHeading" aria-modal="true" class="modal-overlay" id="modalCompleteEvent" role="dialog">
 <div class="modal-box">
  <div class="modal-header">
   <h3 id="modalCompleteEventHeading">
    Conclusão de Previsão Operacional
   </h3>
   <button aria-label="Fechar Conclusão de Previsão Operacional" class="modal-close" id="btnCloseCompleteModal" type="button">
    ×
   </button>
  </div>
  <div class="modal-body">
   <div style="margin-bottom: 1rem">
    <div id="completeModalEventDesc" style="font-weight: 700">
     Descrição da Atividade
    </div>
    <div id="completeModalHierarchy" style="margin-top: 0.2rem">
     Console • Duto • UO
    </div>
   </div>
   <div style="background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 6px; padding: 0.75rem 1rem; margin-bottom: 1rem; display: flex; justify-content: space-between; flex-wrap: wrap">
    <div>
     <div style="color: var(--text-muted)">
      Horário Previsto
     </div>
     <div id="completeModalScheduledTime" style="font-weight: 700">
      --:--
     </div>
    </div>
    <div>
     <div style="color: var(--text-muted)">
      Horário Efetivo
     </div>
     <div id="completeModalActualTime" style="font-weight: 700">
      --:--
     </div>
    </div>
    <div>
     <div style="color: var(--text-muted)">
      Diferença Calculada
     </div>
     <div id="completeModalTimeDiff" style="font-weight: 700">
      --
     </div>
    </div>
   </div>
   <div class="form-group">
    <label for="inputCompleteNotes">
     Observações da Conclusão (Opcional)
    </label>
    <textarea id="inputCompleteNotes" placeholder="Informações de encerramento, condições operacionais, alinhamentos finais..." rows="3"></textarea>
   </div>
  </div>
  <div class="modal-footer">
   <button class="btn btn-secondary" id="btnCancelCompleteModal" type="button">
    Cancelar
   </button>
   <button class="btn btn-success" id="btnConfirmCompleteModal" type="button">
    <svg aria-hidden="true" fill="none" focusable="false" height="16" stroke="currentColor" stroke-width="2.5" viewbox="0 0 24 24" width="16">
     <polyline points="20 6 9 17 4 12">
     </polyline>
    </svg>
    <span>
     Confirmar Conclusão
    </span>
   </button>
  </div>
 </div>
</div>
<!-- Modal 4: Reabrir Evento -->
<div aria-labelledby="modalReopenEventHeading" aria-modal="true" class="modal-overlay" id="modalReopenEvent" role="dialog">
 <div class="modal-box">
  <div class="modal-header">
   <h3 id="modalReopenEventHeading">
    Reabrir Evento Operacional
   </h3>
   <button aria-label="Fechar Reabrir Evento Operacional" class="modal-close" id="btnCloseReopenModal" type="button">
    ×
   </button>
  </div>
  <div class="modal-body">
   <p style="color: var(--text-secondary); margin-bottom: 1rem">
    Esta ação retornará o evento para a lista de
    <strong>
     Eventos Pendentes
    </strong>
    . O histórico da conclusão anterior será preservado integralmente na auditoria.
   </p>
   <div class="notice-banner warning" id="boxReopenPastWarning" style="display: none">
    <svg aria-hidden="true" fill="none" focusable="false" height="20" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="20">
     <circle cx="12" cy="12" r="10">
     </circle>
     <line x1="12" x2="12" y1="8" y2="12">
     </line>
     <line x1="12" x2="12.01" y1="16" y2="16">
     </line>
    </svg>
    <div>
     O horário previsto original deste evento já expirou. Você pode informar uma nova data e hora prevista para reativação do alarme:
    </div>
   </div>
   <div class="form-grid">
    <div class="form-group">
     <label for="inputReopenDate">
      Nova Data Prevista
     </label>
     <input id="inputReopenDate" type="date"/>
    </div>
    <div class="form-group">
     <label for="inputReopenTime">
      Nova Hora Prevista
     </label>
     <input id="inputReopenTime" type="time"/>
    </div>
   </div>
  </div>
  <div class="modal-footer">
   <button class="btn btn-secondary" id="btnCancelReopenModal" type="button">
    Cancelar
   </button>
   <button class="btn btn-warning" id="btnConfirmReopenModal" type="button">
    Confirmar Reabertura
   </button>
  </div>
 </div>
</div>
<!-- Modal 5: Detalhes do Evento & Histórico de Auditoria (Inclui desenho da caneta se houver) -->
<div aria-labelledby="modalEventDetailsHeading" aria-modal="true" class="modal-overlay" id="modalEventDetails" role="dialog">
 <div class="modal-box modal-lg">
  <div class="modal-header">
   <h3 id="modalEventDetailsHeading">
    Detalhes da Previsão e Histórico de Auditoria
   </h3>
   <button aria-label="Fechar Detalhes da Previsão e Histórico de Auditoria" class="modal-close" id="btnCloseDetailsModal" type="button">
    ×
   </button>
  </div>
  <div class="modal-body">
   <div style="display: grid; gap: 0.75rem; background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 8px; padding: 1rem; margin-bottom: 1.25rem">
    <div>
     <div style="color: var(--text-muted)">
      Console / Duto / UO
     </div>
     <div id="detailsModalPath" style="font-weight: 700">
      --
     </div>
    </div>
    <div>
     <div style="color: var(--text-muted)">
      Equipamento / TAG
     </div>
     <div id="detailsModalEquipment" style="font-weight: 700">
      --
     </div>
    </div>
    <div>
     <div style="color: var(--text-muted)">
      Horário Previsto
     </div>
     <div id="detailsModalSchedule" style="font-weight: 700">
      --
     </div>
    </div>
    <div>
     <div style="color: var(--text-muted)">
      Situação Atual
     </div>
     <div id="detailsModalStatus" style="font-weight: 700">
      --
     </div>
    </div>
    <div class="span-full">
     <div style="color: var(--text-muted)">
      Descrição da Atividade
     </div>
     <div id="detailsModalDescription" style="font-weight: 600; color: var(--text-main)">
      --
     </div>
    </div>
    <div class="span-full" id="detailsModalNotesBox">
     <div style="color: var(--text-muted)">
      Observações
     </div>
     <div id="detailsModalNotes" style="color: var(--text-secondary); font-style: italic">
      --
     </div>
    </div>
    <!-- Unified Stylus Drawing Container (Section 24 Item 10) -->
    <div class="span-full" data-alias="detailsStylusContainer" id="detailsModalDrawingBox" style="display: none">
     <div style="color: var(--text-muted); margin-bottom: 0.35rem">
      Anotação Manuscrita / Desenho da Caneta:
     </div>
     <div id="detailsStylusContainer">
      <img alt="Anotação com Caneta" id="detailsModalDrawingImg" src="" style="border: 1px solid var(--border-color); border-radius: 6px; background: #0f172a"/>
     </div>
    </div>
   </div>
   <h4 style="font-weight: 700; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.4rem">
    <svg aria-hidden="true" fill="none" focusable="false" height="16" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="16">
     <circle cx="12" cy="12" r="10">
     </circle>
     <polyline points="12 6 12 12 14 14">
     </polyline>
    </svg>
    <span>
     Trilha de Auditoria e Rastreabilidade
    </span>
   </h4>
   <div class="timeline" id="detailsTimeline">
    <!-- Dynamically filled timeline items -->
   </div>
  </div>
  <div class="modal-footer">
   <button class="btn btn-secondary" id="btnCloseDetailsModalBtn" type="button">
    Fechar
   </button>
  </div>
 </div>
</div>
<!-- Modal 6: Confirmação Genérica Acessível -->
<div aria-labelledby="modalConfirmTitle" aria-modal="true" class="modal-overlay" id="modalConfirm" role="dialog">
 <div class="modal-box">
  <div class="modal-header">
   <h3 id="modalConfirmTitle">
    Confirmação
   </h3>
   <button aria-label="Fechar Confirmação" class="modal-close" id="btnCloseConfirmModal" type="button">
    ×
   </button>
  </div>
  <div class="modal-body">
   <p id="modalConfirmMessage" style="color: var(--text-main); line-height: 1.5">
    Mensagem de confirmação...
   </p>
  </div>
  <div class="modal-footer">
   <button class="btn btn-secondary" id="btnCancelConfirm" type="button">
    Cancelar
   </button>
   <button class="btn btn-danger" id="btnAcceptConfirm" type="button">
    Confirmar
   </button>
  </div>
 </div>
</div>
<!-- Modal 7: Dependência Operacional (Bloqueio de Exclusão) -->
<div aria-labelledby="modalDependencyHeading" aria-modal="true" class="modal-overlay" id="modalDependency" role="dialog">
 <div class="modal-box">
  <div class="modal-header" style="background: rgba(217, 119, 6, 0.15)">
   <h3 id="modalDependencyHeading">
    <svg aria-hidden="true" fill="none" focusable="false" height="20" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="20">
     <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z">
     </path>
     <line x1="12" x2="12" y1="9" y2="13">
     </line>
     <line x1="12" x2="12.01" y1="17" y2="17">
     </line>
    </svg>
    <span id="modalDependencyTitle">
     Registro com Dependências
    </span>
   </h3>
   <button aria-label="Fechar Registro com Dependências" class="modal-close" id="btnCloseDependencyModal" type="button">
    ×
   </button>
  </div>
  <div class="modal-body">
   <p id="modalDependencyDesc" style="margin-bottom: 0.75rem">
    Este registro não pode ser excluído fisicamente pois existem registros vinculados a ele na base de dados:
   </p>
   <ul id="modalDependencyList" style="margin-left: 1.25rem; color: var(--text-secondary); margin-bottom: 1rem">
   </ul>
   <div class="notice-banner warning">
    <p>
     Recomendação: Utilize a
     <strong>
      Inativação
     </strong>
     do registro. Registros inativos não aparecem para seleção em novos eventos, mas preservam o histórico de eventos passados e a integridade do sistema.
    </p>
   </div>
  </div>
  <div class="modal-footer">
   <button class="btn btn-secondary" id="btnCloseDependencyModalBtn" type="button">
    Entendido
   </button>
   <button class="btn btn-warning" id="btnDependencyInactivate" type="button">
    Inativar Registro
   </button>
  </div>
 </div>
</div>
<!-- Modal 8: Resumo da Importação de Backup -->
<div aria-labelledby="modalImportSummaryHeading" aria-modal="true" class="modal-overlay" id="modalImportSummary" role="dialog">
 <div class="modal-box">
  <div class="modal-header">
   <h3 id="modalImportSummaryHeading">
    Importação de Backup JSON
   </h3>
   <button aria-label="Fechar Importação de Backup JSON" class="modal-close" id="btnCloseImportSummaryModal" type="button">
    ×
   </button>
  </div>
  <div class="modal-body">
   <p style="margin-bottom: 0.75rem">
    Arquivo validado com sucesso! Resumo dos dados encontrados no arquivo de backup:
   </p>
   <div id="importSummaryCounts" style="background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 6px; padding: 0.75rem; margin-bottom: 1rem">
   </div>
   <div class="form-group" style="margin-bottom: 1rem">
    <label style="font-weight: 700">
     Modo de Importação:
    </label>
    <div style="display: flex; flex-direction: column; gap: 0.5rem; margin-top: 0.35rem; flex-wrap: wrap">
     <label class="form-checkbox">
      <input checked="" name="importMode" type="radio" value="merge"/>
      <span>
       <strong>
        Mesclar Dados:
       </strong>
       Não duplica registros, atualiza pelo ID e versão, preserva dados existentes.
      </span>
     </label>
     <label class="form-checkbox">
      <input name="importMode" type="radio" value="replace"/>
      <span>
       <strong>
        Substituir Tudo:
       </strong>
       Apaga os dados atuais e carrega o backup. Um backup preventivo será baixado automaticamente antes da substituição.
      </span>
     </label>
    </div>
   </div>
  </div>
  <div class="modal-footer">
   <button class="btn btn-secondary" id="btnCancelImportSummary" type="button">
    Cancelar
   </button>
   <button class="btn btn-primary" id="btnConfirmImportSummary" type="button">
    Executar Importação
   </button>
  </div>
 </div>
</div>
<!-- Modal 9: Folha de Ações Contextuais do Evento [⋯] (Section 8.3) -->
<div aria-labelledby="actionSheetEventTitle" aria-modal="true" class="modal-overlay" id="modalEventActionSheet" role="dialog">
 <div class="modal-box">
  <div class="modal-header">
   <h3 id="actionSheetEventTitle">
    Ações da Previsão
   </h3>
   <button aria-label="Fechar Ações da Previsão" class="modal-close" id="btnCloseActionSheet" type="button">
    ×
   </button>
  </div>
  <div class="modal-body" style="padding: 0.85rem">
   <div id="actionSheetEventSubtitle" style="font-weight: 700; margin-bottom: 0.75rem">
    --
   </div>
   <div class="action-sheet-list" id="actionSheetButtonsContainer">
    <!-- Dynamically populated contextual actions -->
   </div>
  </div>
 </div>
</div>
<!-- Modal 10: Status da Aplicação (Section 4.3) -->
<div aria-labelledby="modalAppStatusHeading" aria-modal="true" class="modal-overlay" id="modalAppStatus" role="dialog">
 <div class="modal-box">
  <div class="modal-header">
   <h3 id="modalAppStatusHeading">
    Status Operacional da Aplicação
   </h3>
   <button aria-label="Fechar Status Operacional da Aplicação" class="modal-close" id="btnCloseAppStatusModal" type="button">
    ×
   </button>
  </div>
  <div class="modal-body">
   <div style="display: flex; flex-direction: column; gap: 0.65rem; flex-wrap: wrap">
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.65rem 0.85rem; background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 8px; flex-wrap: wrap">
     <div>
      <div style="color: var(--text-muted)">
       Áudio Local (Web Audio API)
      </div>
      <div id="statusModalAudio" style="font-weight: 700">
       Aguardando interação
      </div>
     </div>
     <button class="btn btn-outline btn-sm" id="btnStatusModalTestAudio" type="button">
      Ativar / Testar Som
     </button>
    </div>
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.65rem 0.85rem; background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 8px; flex-wrap: wrap">
     <div>
      <div style="color: var(--text-muted)">
       Notificações do Navegador
      </div>
      <div id="statusModalNotif" style="font-weight: 700">
       Não solicitado
      </div>
     </div>
     <button class="btn btn-warning btn-sm" id="btnStatusModalTestNotif" type="button">
      Permitir / Testar
     </button>
    </div>
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.65rem 0.85rem; background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 8px; flex-wrap: wrap">
     <div>
      <div style="color: var(--text-muted)">
       Armazenamento Local (IndexedDB)
      </div>
      <div id="statusModalDB" style="font-weight: 700">
       Ativo (Persistência Local)
      </div>
     </div>
     <span class="status-badge normal">
      Online
     </span>
    </div>
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.65rem 0.85rem; background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 8px; flex-wrap: wrap">
     <div>
      <div style="color: var(--text-muted)">
       Último Backup Exportado
      </div>
      <div id="statusModalLastBackup" style="font-weight: 700">
       Nunca realizado
      </div>
     </div>
     <button class="btn btn-outline btn-sm" onclick="document.getElementById('modalAppStatus').classList.remove('active'); App.UI.navigateTo('viewBackup');" type="button">
      Backup
     </button>
    </div>
   </div>
   <div class="notice-banner" style="margin-top: 1rem; margin-bottom: 0">
    <svg aria-hidden="true" fill="none" focusable="false" height="18" stroke="currentColor" stroke-width="2" style="flex-shrink: 0" viewbox="0 0 24 24" width="18">
     <circle cx="12" cy="12" r="10">
     </circle>
     <line x1="12" x2="12" y1="16" y2="12">
     </line>
     <line x1="12" x2="12.01" y1="8" y2="8">
     </line>
    </svg>
    <span>
     Mantenha esta aba aberta para garantir o disparo contínuo dos alarmes locais no celular, tablet ou estação de trabalho.
    </span>
   </div>
  </div>
  <div class="modal-footer">
   <button class="btn btn-secondary" id="btnCloseAppStatusFooter" type="button">
    Fechar
   </button>
  </div>
 </div>
</div>
<!-- Toast Notification Container -->
<div aria-live="polite" class="toast-container" id="toastContainer">
</div>

"""
