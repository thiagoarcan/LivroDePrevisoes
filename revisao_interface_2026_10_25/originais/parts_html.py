# -*- coding: utf-8 -*-
HTML_CONTENT = """
  <!-- Header Bar -->
  <header class="app-header">
    <div class="header-left">
      <button id="btnToggleMobileMenu" class="btn-hamburger" title="Abrir Menu de Navegação" aria-label="Abrir Menu">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
      </button>

      <div class="header-brand">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M4 14a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v2a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-2z"></path>
          <path d="M6 12V8a6 6 0 0 1 12 0v4"></path>
          <circle cx="12" cy="15" r="1"></circle>
        </svg>
        <div>
          <h1>Caderno de Previsões</h1>
          <div class="subtitle">Dutos &bull; Sala de Controle</div>
        </div>
      </div>

      <!-- Active Console Selector in Header (Chosen once, persists across views and forms) -->
      <div class="header-console-box" title="Console selecionado. Ele permanece ativo para novos eventos sem necessidade de preenchimento repetido.">
        <label for="headerActiveConsole">Console ativo:</label>
        <select id="headerActiveConsole" class="header-console-select" aria-label="Console Operacional Ativo">
          <!-- Dynamically populated with consoles -->
        </select>
      </div>
    </div>

    <!-- Status Bar with Clock & Indicators -->
    <div class="header-status-bar">
      <div id="liveClock" class="clock-display" title="Horário Oficial da Operação">--:--:--</div>
      
      <span id="chipHeaderAudioWarning" class="status-pill warning" style="display: none;" title="Toque para iniciar e desbloquear o áudio de alarmes">
        &#9888; Áudio não iniciado
      </span>

      <span id="pillDB" class="status-pill ok" title="Estado do IndexedDB">
        <span class="indicator-dot">&bull;</span> DB: Pronto
      </span>
      
      <span id="pillAudio" class="status-pill warning" title="Clique para ativar o áudio no navegador">
        <span class="indicator-dot">&bull;</span> Áudio: Iniciar
      </span>

      <span id="pillNotif" class="status-pill" title="Permissão de Notificações do Navegador">
        <span class="indicator-dot">&bull;</span> Notif: Pendente
      </span>

      <!-- Prominent Test Notification Button in Header -->
      <button id="btnHeaderTestNotif" class="status-pill warning" title="Disparar teste de notificação do navegador">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
        <span>Testar Notificação</span>
      </button>

      <span id="pillBackup" class="status-pill" title="Data do último backup">
        <span class="indicator-dot">&bull;</span> Backup: Nunca
      </span>
    </div>

    <!-- Header Actions -->
    <div class="header-actions">
      <!-- Layout / ViewMode Quick Selector (Section 1.2) -->
      <div class="header-viewmode-box" title="Escolher modo de visualização (Automático ou Manual)">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg>
        <label for="selectHeaderViewMode">Visualização:</label>
        <select id="selectHeaderViewMode" class="header-viewmode-select" aria-label="Visualização da Interface">
          <option value="auto">Automática</option>
          <option value="compact">Compacta</option>
          <option value="mobile">Celular</option>
          <option value="tablet">Tablet</option>
          <option value="conventional">Monitor Convencional</option>
          <option value="widescreen">Widescreen</option>
          <option value="ultrawide">Ultrawide</option>
        </select>
      </div>

      <!-- Alarm Bell Button with Badge (Section 2.2) -->
      <button id="btnHeaderAlarmBell" class="btn-header-bell" title="Alertas e Alarmes Operacionais Ativos" aria-label="Alertas Ativos">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
        <span id="headerAlarmBadge" class="bell-badge" style="display: none;">0</span>
      </button>

      <!-- App Status Button -->
      <button id="btnHeaderAppStatus" class="btn btn-outline btn-icon" title="Status da Aplicação (Banco, Áudio, Notificações e Backup)" aria-label="Status da Aplicação">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
      </button>

      <button id="btnControllerBadge" class="btn btn-secondary btn-sm" title="Alterar identificação do controlador">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
        <span id="headerUserName">Usuário local</span>
      </button>

      <button id="btnToggleTheme" class="btn btn-outline btn-icon" title="Alternar Tema (Escuro / Claro / Industrial Alto Contraste)" aria-label="Alternar Tema">
        <svg id="themeIconSun" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
      </button>

      <button id="btnQuickAddEvent" class="btn btn-primary btn-sm" title="Adicionar nova previsão operacional">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
        <span>Nova Previsão</span>
      </button>
    </div>
  </header>

  <!-- Persistent Banners (Section 1.3, 3.2, 23) -->
  <div id="mobileActiveAlarmsBanner" class="persistent-banner alarm-banner" role="alert">
    <div style="display: flex; align-items: center; gap: 0.5rem;">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
      <span id="bannerActiveAlarmsText">2 alarmes aguardando ação</span>
    </div>
    <div style="display: flex; gap: 0.5rem;">
      <button id="btnBannerViewAlarms" class="btn btn-secondary btn-sm">Ver alarmes</button>
      <button id="btnBannerAckAll" class="btn btn-warning btn-sm">Reconhecer</button>
    </div>
  </div>

  <div id="backupOverdueBanner" class="persistent-banner backup-banner">
    <div style="display: flex; align-items: center; gap: 0.5rem;">
      <span>&#9888;</span>
      <span id="bannerBackupOverdueText">Último backup realizado há mais de 7 dias.</span>
    </div>
    <button id="btnBannerBackupNow" class="btn btn-warning btn-sm">Realizar backup agora</button>
  </div>

  <div id="viewModeWarningBanner" class="persistent-banner layout-banner">
    <div style="display: flex; align-items: center; gap: 0.5rem;">
      <span>&#9432;</span>
      <span id="bannerViewModeText">O modo de visualização manual escolhido excede a largura ideal desta tela.</span>
    </div>
    <button id="btnBannerResetAuto" class="btn btn-primary btn-sm">Voltar para Automático</button>
  </div>

  <!-- Mobile / Tablet Drawer Menu (Matches Wireframe Celular - 6. Menu Drawer) -->
  <div id="mobileDrawerOverlay" class="mobile-drawer-overlay"></div>
  <div id="appMobileDrawer" class="mobile-drawer">
  <div id="mobileDrawer" style="display:none;"></div>
    <div class="drawer-header">
      <div style="font-weight: 700; color: #38bdf8; display: flex; align-items: center; gap: 0.5rem;">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
        <div>
          <div>Previsões em Dutos</div>
          <div style="font-size: 0.7rem; color: var(--text-muted); font-weight: 600;">v1.1.0 &bull; Operação Offline</div>
        </div>
      </div>
      <button id="btnCloseMobileDrawer" class="modal-close" aria-label="Fechar Menu">&times;</button>
    </div>
    <div class="drawer-nav-items">
      <button class="mobile-nav-link drawer-item active" data-view="viewDashboard">
        <span>&#x1F3E0; Painel Principal</span>
        <span id="badgePendingDrawer" class="badge-count">0</span>
      </button>
      <button class="mobile-nav-link drawer-item" data-view="viewPendingEvents">
        <span>&#x1F552; Eventos Pendentes</span>
        <span id="badgePendingNavCountDrawer" class="badge-count">0</span>
      </button>
      <button class="mobile-nav-link drawer-item" data-view="viewNewEvent">
        <span>&#x2795; Nova Previsão</span>
      </button>
      <button class="mobile-nav-link drawer-item" data-view="viewCompletedEvents">
        <span>&#x2705; Eventos Concluídos</span>
      </button>
      <button class="mobile-nav-link drawer-item" data-view="viewCadastros">
        <span>&#x1F5C2; Cadastros Operacionais</span>
      </button>
      <button class="mobile-nav-link drawer-item" data-view="viewConfigAlerts">
        <span>&#x1F514; Configurações de Alertas</span>
      </button>
      <button class="mobile-nav-link drawer-item" data-view="viewConfigColors">
        <span>&#x1F3A8; Configurações de Cores</span>
      </button>
      <button class="mobile-nav-link drawer-item" data-view="viewBackup">
        <span>&#x1F4BE; Backup e Dados</span>
      </button>
      <button class="mobile-nav-link drawer-item" data-view="viewDiagnostic">
        <span>&#x1F4CA; Diagnóstico Técnico</span>
      </button>

      <div style="border-top: 1px solid var(--border-color); margin: 0.4rem 0; padding-top: 0.4rem;">
        <button type="button" id="btnDrawerAppStatus" class="drawer-item" style="width: 100%;">
          <span>&#9432; Status da Aplicação</span>
        </button>
        <button type="button" id="btnDrawerTheme" class="drawer-item" style="width: 100%;">
          <span id="labelDrawerTheme">&#x1F319; Tema (Escuro)</span>
        </button>
        <button type="button" id="btnDrawerUser" class="drawer-item" style="width: 100%;">
          <span id="labelDrawerUser">&#x1F464; Usuário: Operador</span>
        </button>
        <div style="padding: 0.4rem 0.9rem;">
          <label for="selectDrawerViewMode" style="font-size: 0.72rem; color: var(--text-muted); margin-bottom: 0.25rem;">Modo de Visualização:</label>
          <select id="selectDrawerViewMode" style="min-height: 36px; font-size: 0.8rem; padding: 0.25rem 0.5rem;">
            <option value="auto">Automática</option>
            <option value="compact">Compacta</option>
            <option value="mobile">Celular</option>
            <option value="tablet">Tablet</option>
            <option value="conventional">Monitor Convencional</option>
            <option value="widescreen">Widescreen</option>
            <option value="ultrawide">Ultrawide</option>
          </select>
        </div>
        <button type="button" id="btnDrawerCloseBottom" class="drawer-item" style="width: 100%; color: var(--text-muted);">
          <span>&#x2190; Sair / Fechar Menu</span>
        </button>
      </div>
    </div>
  </div>

  <!-- Desktop Navigation Bar -->
  <nav class="app-nav" role="tablist">
    <button class="nav-item active" data-view="viewDashboard" role="tab">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="9"></rect><rect x="14" y="3" width="7" height="5"></rect><rect x="14" y="12" width="7" height="9"></rect><rect x="3" y="16" width="7" height="5"></rect></svg>
      <span>Painel</span>
      <span id="badgePendingCount" class="badge-count">0</span>
    </button>

    <button class="nav-item" data-view="viewNewEvent" role="tab">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>
      <span id="navNewEventLabel">Novo Evento</span>
    </button>

    <button class="nav-item" data-view="viewPendingEvents" role="tab">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
      <span>Eventos Pendentes</span>
      <span id="badgePendingNavCount" class="badge-count">0</span>
    </button>

    <button class="nav-item" data-view="viewCompletedEvents" role="tab">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Eventos Concluídos</span>
    </button>

    <button class="nav-item" data-view="viewCadastros" role="tab">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
      <span>Cadastros Operacionais</span>
    </button>

    <button class="nav-item" data-view="viewConfigAlerts" role="tab">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
      <span>Configurações de Alertas</span>
    </button>

    <button class="nav-item" data-view="viewConfigColors" role="tab">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="13.5" cy="6.5" r=".5"></circle><circle cx="17.5" cy="10.5" r=".5"></circle><circle cx="8.5" cy="7.5" r=".5"></circle><circle cx="6.5" cy="12.5" r=".5"></circle><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.563-2.512 5.563-5.563C22 6.5 17.5 2 12 2z"></path></svg>
      <span>Configurações de Cores</span>
    </button>

    <button class="nav-item" data-view="viewBackup" role="tab">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
      <span>Backup e Dados</span>
    </button>

    <button class="nav-item" data-view="viewDiagnostic" role="tab">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>
      <span>Diagnóstico</span>
    </button>
  </nav>

  <!-- Legacy FAB button kept hidden in DOM; active FAB #fabAddEvent is integrated in bottom navigation -->
  <button id="btnFabNewEvent" class="fab-btn" title="Nova Previsão" aria-label="Nova Previsão">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
  </button>

  <!-- Main View Container -->
  <main class="app-main">
    
    <!-- ==================== VIEW 1: PAINEL ==================== -->
    <section id="viewDashboard" class="view-section active">
      <!-- Metric Cards (7 Metrics; 2-column grid on mobile) -->
      <div class="dashboard-metrics">
        <div class="metric-card" data-filter="all">
          <div class="metric-icon" style="background: rgba(2, 132, 199, 0.15); color: #38bdf8;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
          </div>
          <div class="metric-data">
            <div id="metricTotalPending" class="metric-value">0</div>
            <div class="metric-label">Pendentes</div>
          </div>
        </div>

        <div class="metric-card" data-filter="overdue">
          <div class="metric-icon" style="background: rgba(153, 27, 27, 0.2); color: #f87171;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
          </div>
          <div class="metric-data">
            <div id="metricOverdue" class="metric-value" style="color: #f87171;">0</div>
            <div class="metric-label">Atrasados</div>
          </div>
        </div>

        <div class="metric-card" data-filter="15min">
          <div class="metric-icon" style="background: rgba(220, 38, 38, 0.15); color: #ef4444;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
          </div>
          <div class="metric-data">
            <div id="metricNext15" class="metric-value" style="color: #ef4444;">0</div>
            <div class="metric-label">Próx. 15 min</div>
          </div>
        </div>

        <div class="metric-card" data-filter="30min">
          <div class="metric-icon" style="background: rgba(234, 88, 12, 0.15); color: #fb923c;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 14 14"></polyline></svg>
          </div>
          <div class="metric-data">
            <div id="metricNext30" class="metric-value" style="color: #fb923c;">0</div>
            <div class="metric-label">Próx. 30 min</div>
          </div>
        </div>

        <div class="metric-card" data-filter="60min">
          <div class="metric-icon" style="background: rgba(37, 99, 235, 0.15); color: #60a5fa;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
          </div>
          <div class="metric-data">
            <div id="metricNext60" class="metric-value" style="color: #60a5fa;">0</div>
            <div class="metric-label">Próx. 60 min</div>
          </div>
        </div>

        <div class="metric-card" data-filter="completed">
          <div class="metric-icon" style="background: rgba(22, 163, 74, 0.15); color: #4ade80;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
          </div>
          <div class="metric-data">
            <div id="metricCompletedToday" class="metric-value" style="color: #4ade80;">0</div>
            <div class="metric-label">Concluídos Hoje</div>
          </div>
        </div>

        <div class="metric-card" data-filter="unacknowledged">
          <div class="metric-icon" style="background: rgba(217, 119, 6, 0.15); color: #facc15;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
          </div>
          <div class="metric-data">
            <div id="metricUnacknowledged" class="metric-value" style="color: #facc15;">0</div>
            <div class="metric-label">Alarmes Ativos</div>
          </div>
        </div>
      </div>

      <!-- Highlight Grid: Spotlight (2/3 on tablet/wide) + Active Alarms Side Panel (1/3 on tablet/wide) -->
      <div class="dashboard-highlight-grid">
        <!-- Spotlight: Next Event -->
        <div id="spotlightCard" class="spotlight-card">
          <div class="spotlight-header">
            <div class="spotlight-badge">&starf; Próximo Evento Operacional</div>
            <span id="spotlightBadgeState" class="status-badge normal">Aguardando</span>
          </div>
          <div class="spotlight-body">
            <div>
              <div id="spotlightHierarchy" class="spotlight-path">Console &bull; Duto &bull; UO</div>
              <div id="spotlightDescription" class="spotlight-desc">Nenhum evento operacional pendente no momento.</div>
              <div id="spotlightNotes" style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.25rem;"></div>
            </div>
            <div class="spotlight-timer">
              <div id="spotlightTimeLeft" class="time-left">--:--</div>
              <div id="spotlightScheduledAt" class="sched-time">Horário Previsto: --:--</div>
            </div>
          </div>
          <div id="spotlightActions" style="display: flex; gap: 0.5rem; justify-content: flex-end; margin-top: 0.5rem; flex-wrap: wrap;">
            <!-- Dynamically filled -->
          </div>
        </div>

        <!-- Tablet / Widescreen Active Alarms & Overdue Side Panel (Wireframe Tablet - 1) -->
        <div id="tabletActiveAlarmsPanel" class="tablet-alarms-panel">
          <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">
            <strong style="font-size: 0.92rem; display: flex; align-items: center; gap: 0.4rem;">
              <span style="color: #ef4444;">&#9888;</span>
              <span>Alarmes Ativos (<span id="tabletAlarmsCount">0</span>)</span>
            </strong>
            <button type="button" class="btn btn-outline btn-sm" onclick="App.UI.navigateTo('viewPendingEvents')">Ver todos &rarr;</button>
          </div>
          <div id="tabletAlarmsList" style="display: flex; flex-direction: column; gap: 0.5rem; flex: 1; overflow-y: auto; max-height: 220px;">
            <div style="color: var(--text-muted); font-size: 0.82rem; padding: 1rem 0; text-align: center;">Nenhum alarme crítico ou atrasado no momento.</div>
          </div>
        </div>
      </div>

      <!-- Urgent / Overdue Quick List -->
      <div id="cardDashboardUrgent" class="card">
        <div class="card-header">
          <div>
            <div class="card-title">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
              <span>Eventos que Demandam Atenção Imediata</span>
            </div>
            <div class="card-subtitle">Eventos atrasados ou previstos para os próximos 30 minutos</div>
          </div>
          <button class="btn btn-outline btn-sm" onclick="App.UI.navigateTo('viewPendingEvents')">Ver Todos os Pendentes &rarr;</button>
        </div>

        <!-- Mobile Summarized Urgent Cards (Section 3.5) -->
        <div id="dashboardUrgentCards" class="dashboard-urgent-cards"></div>

        <!-- Tablet / Desktop Table -->
        <div class="table-responsive">
          <table class="data-table" id="tableDashboardUrgent">
            <thead>
              <tr>
                <th>Horário</th>
                <th>Situação</th>
                <th>Console / Duto</th>
                <th>UO / Equipamento / TAG</th>
                <th>Descrição da Atividade</th>
                <th style="text-align: right;">Ações</th>
              </tr>
            </thead>
            <tbody id="tbodyDashboardUrgent">
              <tr>
                <td colspan="6" style="text-align: center; color: var(--text-muted); padding: 1.5rem;">Nenhum evento urgente no momento.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- ==================== VIEW 2: NOVO EVENTO ==================== -->
    <section id="viewNewEvent" class="view-section">
      <div class="card">
        <div class="card-header">
          <div>
            <div id="formEventTitle" class="card-title">Cadastrar Previsão Operacional</div>
            <div class="card-subtitle" style="display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;">
              <span id="labelEventActiveConsole" class="active-console-tag" style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 0.25rem 0.6rem; border-radius: 4px; font-weight: 700;">Console Ativo: --</span>
              <strong id="labelActiveConsoleBadge" style="display:none;">--</strong>
              <span style="font-size: 0.8rem; color: var(--text-muted);">(Definido no seletor global do topo)</span>
            </div>
          </div>
          <button id="btnCancelEditEvent" class="btn btn-outline btn-sm" style="display: none;">Cancelar Edição</button>
        </div>

        <form id="formEvent" autocomplete="off">
          <input type="hidden" id="eventEditId" value="">
          <input type="hidden" id="eventConsoleId" value="">
          <input type="hidden" id="selectEventConsole" value="">
          
          <div class="form-grid">
            <!-- Cascading Dropdowns (Console is inherited from header) -->
            <div class="form-group">
              <label for="selectEventPipeline">Duto <span class="required">*</span></label>
              <select id="selectEventPipeline" required>
                <option value="">Carregando dutos do console...</option>
              </select>
              <div class="form-help">Dutos pertencentes ao console ativo</div>
            </div>

            <div class="form-group">
              <label for="selectEventUO">Unidade Operacional (UO) <span class="required">*</span></label>
              <select id="selectEventUO" required disabled>
                <option value="">Selecione primeiro o Duto...</option>
              </select>
              <div class="form-help">UOs conectadas ao duto selecionado</div>
            </div>

            <div class="form-group">
              <label for="selectEventEquipmentType">Tipo de Equipamento <span class="form-help">(opcional)</span></label>
              <select id="selectEventEquipmentType" disabled>
                <option value="">Geral da UO / Não aplicável</option>
              </select>
            </div>

            <div class="form-group">
              <label for="selectEventTag">TAG do Equipamento <span class="form-help">(opcional)</span></label>
              <select id="selectEventTag" disabled>
                <option value="">Selecione o Tipo primeiro...</option>
              </select>
            </div>

            <div class="form-group span-full" style="margin-top: -0.25rem; margin-bottom: 0.25rem;">
              <div id="cascadeStatusText" aria-live="polite" style="font-size: 0.78rem; color: #38bdf8; font-weight: 600;"></div>
            </div>

            <!-- Date and Time -->
            <div class="form-group">
              <label for="inputEventDate">Data do Evento <span class="required">*</span></label>
              <input type="date" id="inputEventDate" required>
            </div>

            <div class="form-group">
              <label for="inputEventTime">Hora do Evento (HH:mm) <span class="required">*</span></label>
              <input type="time" id="inputEventTime" required>
            </div>

            <div class="form-group">
              <label for="selectEventPriority">Prioridade</label>
              <select id="selectEventPriority">
                <option value="Normal">Normal</option>
                <option value="Alta">Alta</option>
                <option value="Crítica">Crítica</option>
                <option value="Baixa">Baixa</option>
              </select>
            </div>

            <!-- Description & Notes -->
            <div class="form-group span-full">
              <label for="inputEventDescription">Descrição da Atividade Operacional <span class="required">*</span></label>
              <input type="text" id="inputEventDescription" placeholder="Ex: Verificar o término do recebimento de MGO" required>
              <div class="form-help">Texto claro e direto da atividade a ser acompanhada</div>
            </div>

            <div class="form-group span-full">
              <label for="inputEventNotes">Observações e Recomendações Operacionais</label>
              <textarea id="inputEventNotes" rows="2" placeholder="Informações adicionais, alinhamento de válvulas, contatos, etc."></textarea>
            </div>

            <!-- Tablet Stylus Drawing Pad Toggle -->
            <div class="form-group span-full">
              <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
                <label>Desenho / Anotação com Caneta de Tablet (Opcional):</label>
                <div style="display: flex; gap: 0.4rem; align-items: center;">
                  <span id="stylusModeIndicator" style="font-size: 0.72rem; background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: 700; display: none;">Modo: Caneta (4px)</span>
                  <button type="button" id="btnToggleStylusCanvas" class="btn btn-outline btn-sm">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 19l7-7 3 3-7 7-3-3z"></path><path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"></path><path d="M2 2l7.586 7.586"></path><circle cx="11" cy="11" r="2"></circle></svg>
                    <span>Abrir Lousa para Caneta</span>
                  </button>
                </div>
              </div>

              <div id="boxStylusCanvas" class="stylus-canvas-container" style="display: none;">
                <div class="canvas-toolbar">
                  <div style="display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap;">
                    <label style="font-size: 0.75rem;">Cor:</label>
                    <input type="color" id="inputStylusStrokeColor" value="#38bdf8" style="width: 32px; height: 32px; padding: 1px;">
                    <input type="color" id="stylusColor" value="#38bdf8" style="display: none;">
                    <label style="font-size: 0.75rem; margin-left: 0.35rem;">Espessura:</label>
                    <select id="selectStylusStrokeWidth" style="width: auto; min-height: 32px; padding: 0.2rem 0.5rem; font-size: 0.75rem;">
                      <option value="2">Fina (2px)</option>
                      <option value="4" selected>Normal (4px)</option>
                      <option value="8">Grossa (8px)</option>
                    </select>
                    <select id="stylusWidth" style="display: none;"><option value="4" selected>4</option></select>
                    <button type="button" id="btnEraserStylusCanvas" class="btn btn-outline btn-sm">Borracha</button>
                    <button type="button" id="btnUndoStylusCanvas" class="btn btn-outline btn-sm" title="Desfazer último traço">↩ Desfazer</button>
                  </div>
                  <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                    <button type="button" id="btnFullscreenStylusCanvas" class="btn btn-outline btn-sm" title="Expandir lousa em tela cheia">⛶ Tela Cheia</button>
                    <button type="button" id="btnClearStylusCanvas" class="btn btn-outline btn-sm">Limpar</button>
                  </div>
                </div>
                <canvas id="stylusDrawingCanvas" class="stylus-canvas" width="600" height="220"></canvas>
                <div class="form-help" style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 0.35rem;">
                  <span>Desenhe alinhamentos, níveis de tanque ou anotações manuscritas diretamente com a caneta ou dedo.</span>
                  <span style="color: #38bdf8;">💡 Dica: Gire o celular para paisagem ou use Tela Cheia para mais espaço.</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Alarm Sub-Card -->
          <div class="card" style="margin-top: 1rem; background: var(--bg-app); border: 1px solid var(--border-color);">
            <div class="card-header" style="margin-bottom: 0.5rem;">
              <label class="form-checkbox" style="font-weight: 700; font-size: 0.95rem;">
                <input type="checkbox" id="checkEventAlarmActive" checked>
                <span>Ativar Alarme para esta Previsão</span>
              </label>
              <label class="form-checkbox" id="wrapperUseDefaultAlarm">
                <input type="checkbox" id="checkEventUseDefaultAlarm" checked>
                <span>Usar Configurações Padrão de Alerta</span>
              </label>
            </div>

            <div id="boxCustomAlarmSettings" class="form-grid" style="display: none; padding-top: 0.5rem;">
              <div class="form-group">
                <label for="inputEventAlarmLeadTime">Antecedência do Alarme (minutos)</label>
                <input type="number" id="inputEventAlarmLeadTime" min="0" max="1440" value="15">
                <div class="form-help">0 dispara exatamente no horário</div>
              </div>

              <div class="form-group">
                <label>Formas de Alerta do Evento</label>
                <div style="display: flex; flex-direction: column; gap: 0.35rem; margin-top: 0.35rem;">
                  <label class="form-checkbox">
                    <input type="checkbox" id="checkEventAlertSound" checked>
                    <span>Sinal Sonoro</span>
                  </label>
                  <label class="form-checkbox">
                    <input type="checkbox" id="checkEventAlertVisual" checked>
                    <span>Alerta Visual na Tela</span>
                  </label>
                  <label class="form-checkbox">
                    <input type="checkbox" id="checkEventAlertNotif">
                    <span>Notificação do Navegador</span>
                  </label>
                </div>
              </div>

              <div class="form-group">
                <label class="form-checkbox" style="margin-top: 0.5rem;">
                  <input type="checkbox" id="checkEventAlertRepeat" checked>
                  <span>Repetir Alerta até Reconhecimento</span>
                </label>
                <div style="display: flex; gap: 0.5rem; margin-top: 0.35rem;">
                  <div style="flex: 1;">
                    <label style="font-size: 0.72rem;">Intervalo (min)</label>
                    <input type="number" id="inputEventAlertRepeatInterval" min="1" max="60" value="2">
                  </div>
                  <div style="flex: 1;">
                    <label style="font-size: 0.72rem;">Máx Repetições</label>
                    <input type="number" id="inputEventAlertMaxRepeats" min="1" max="20" value="5">
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Bottom Form Actions: Option to keep Duto & UO for quick consecutive additions -->
          <div class="form-sticky-submit-bar" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.75rem; margin-top: 1.25rem;">
            <label class="form-checkbox" title="Ao salvar, o Duto e a UO permanecerão selecionados para facilitar cadastrar vários eventos no mesmo duto.">
              <input type="checkbox" id="checkKeepDutoUO" checked>
              <span><strong>Manter Duto e UO para próximas previsões</strong></span>
            </label>

            <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
              <button type="button" id="btnResetEventForm" class="btn btn-secondary">Limpar</button>
              
              <!-- Salvar e Inserir Outra Previsão neste Duto -->
              <button type="button" id="btnSubmitAndNew" class="btn btn-success" title="Salva e avança o horário mantendo o Duto e a UO">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                <span>Salvar e + Outra no Duto</span>
              </button>

              <button type="submit" id="btnSubmitEvent" class="btn btn-primary">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                <span id="btnSubmitEventText">Salvar Previsão</span>
              </button>
            </div>
          </div>
        </form>
      </div>
    </section>

    <!-- ==================== VIEW 3: EVENTOS PENDENTES ==================== -->
    <section id="viewPendingEvents" class="view-section">
      <!-- Toolbar -->
      <div class="events-toolbar">
        <div class="toolbar-primary">
          <div class="search-box">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            <input type="text" id="inputSearchPending" placeholder="Pesquisar por texto, duto, UO, TAG ou descrição...">
          </div>

          <div style="display: flex; align-items: center; gap: 0.45rem; flex-wrap: wrap;">
            <button id="btnToggleFilters" class="btn btn-outline btn-sm">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
              <span>Filtros</span>
              <span id="badgeActiveFiltersCount" class="nav-badge" style="display: none; background: #0284c7;">0</span>
            </button>

            <!-- Filter only active console toggle -->
            <label class="form-checkbox" style="font-size: 0.78rem; min-height: 32px;" title="Filtrar automaticamente pelo Console selecionado no cabeçalho">
              <input type="checkbox" id="checkFilterOnlyActiveConsole" checked>
              <span>Apenas Console Ativo (<strong id="labelActiveConsoleFilter">C04</strong>)</span>
            </label>

            <!-- View switch -->
            <div style="display: flex; border: 1px solid var(--border-color); border-radius: 6px; overflow: hidden;">
              <button id="btnViewCards" class="btn btn-secondary btn-sm" title="Visualização em Cartões" style="border-radius: 0;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
              </button>
              <button id="btnViewTable" class="btn btn-outline btn-sm" title="Visualização em Tabela Compacta" style="border-radius: 0;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>
              </button>
            </div>

            <div style="display: flex; align-items: center; gap: 0.35rem;">
              <label for="selectSortPending" style="font-size: 0.75rem; white-space: nowrap;">Ordenar:</label>
              <select id="selectSortPending" style="width: auto; min-height: 32px; padding: 0.2rem 0.5rem; font-size: 0.75rem;">
                <option value="cronologica">Cronológica (Padrão)</option>
                <option value="console">Console</option>
                <option value="duto">Duto</option>
                <option value="uo">UO</option>
                <option value="tag">TAG</option>
                <option value="prioridade">Prioridade</option>
              </select>
            </div>

            <button id="btnClearFilters" class="btn btn-outline btn-sm" title="Limpar todos os filtros">Limpar</button>
          </div>
        </div>

        <!-- Collapsible Advanced Filters / Mobile Filter Sheet -->
        <div id="filterDrawer" class="toolbar-filters" style="display: none;">
          <div class="span-full" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
            <strong style="font-size: 0.85rem; color: var(--text-main);">Filtros Avançados</strong>
            <button type="button" id="btnCloseFilterSheet" class="btn btn-outline btn-sm" style="padding: 0.2rem 0.5rem;">Fechar &times;</button>
          </div>
          <div class="form-group">
            <label style="font-size: 0.72rem;">Console</label>
            <select id="filterConsole" style="padding: 0.35rem; min-height: 32px;">
              <option value="">Todos os Consoles</option>
            </select>
          </div>
          <div class="form-group">
            <label style="font-size: 0.72rem;">Duto</label>
            <select id="filterPipeline" style="padding: 0.35rem; min-height: 32px;">
              <option value="">Todos os Dutos</option>
            </select>
          </div>
          <div class="form-group">
            <label style="font-size: 0.72rem;">UO</label>
            <select id="filterUO" style="padding: 0.35rem; min-height: 32px;">
              <option value="">Todas as UOs</option>
            </select>
          </div>
          <div class="form-group">
            <label style="font-size: 0.72rem;">Situação / Faixa</label>
            <select id="filterStatus" style="padding: 0.35rem; min-height: 32px;">
              <option value="">Todas as Situações</option>
              <option value="Atrasado">Atrasado</option>
              <option value="Crítico">Crítico</option>
              <option value="Urgente">Urgente</option>
              <option value="Atenção">Atenção</option>
              <option value="Monitoramento">Monitoramento</option>
              <option value="Normal">Normal</option>
            </select>
          </div>
          <div class="form-group">
            <label style="font-size: 0.72rem;">Alarme Ativo</label>
            <select id="filterAlarm" style="padding: 0.35rem; min-height: 32px;">
              <option value="">Todos</option>
              <option value="sim">Com Alarme</option>
              <option value="nao">Sem Alarme</option>
            </select>
          </div>
          <div class="form-group">
            <label style="font-size: 0.72rem;">Prioridade</label>
            <select id="filterPriority" style="padding: 0.35rem; min-height: 32px;">
              <option value="">Todas</option>
              <option value="Crítica">Crítica</option>
              <option value="Alta">Alta</option>
              <option value="Normal">Normal</option>
              <option value="Baixa">Baixa</option>
            </select>
          </div>
          <div class="form-group">
            <label style="font-size: 0.72rem;">Data De</label>
            <input type="date" id="filterDateFrom" style="padding: 0.2rem 0.4rem; font-size: 0.75rem; min-height: 32px;">
          </div>
          <div class="form-group">
            <label style="font-size: 0.72rem;">Data Até</label>
            <input type="date" id="filterDateTo" style="padding: 0.2rem 0.4rem; font-size: 0.75rem; min-height: 32px;">
          </div>
          <div class="span-full" style="display: flex; justify-content: flex-end; gap: 0.5rem; margin-top: 0.35rem;">
            <button type="button" id="btnSheetClearFilters" class="btn btn-secondary btn-sm">Limpar Filtros</button>
            <button type="button" id="btnSheetApplyFilters" class="btn btn-primary btn-sm">Aplicar Filtros</button>
          </div>
        </div>
      </div>

      <!-- Master-Detail Wrapper for Tablet Landscape / Ultrawide (Section 4.3) -->
      <div class="pending-master-detail-grid">
        <!-- Cards Container (Master List) -->
        <div id="containerPendingCards" class="events-container-cards">
          <!-- Rendered dynamically -->
        </div>

        <!-- Detail Side Pane (Visible on Tablet Landscape & Ultrawide) -->
        <aside id="pendingDetailPane" class="pending-detail-pane" aria-label="Detalhes do Evento Selecionado">
          <!-- Rendered dynamically by renderPendingDetailPane -->
        </aside>
      </div>

      <!-- Compact Table Container -->
      <div id="containerPendingTable" class="table-responsive" style="display: none;">
        <table class="data-table" id="tablePendingEvents">
          <thead>
            <tr>
              <th>Horário</th>
              <th>Tempo Restante</th>
              <th>Situação</th>
              <th>Console / Duto</th>
              <th>UO / Equipamento / TAG</th>
              <th>Descrição</th>
              <th>Alarme</th>
              <th style="text-align: right;">Ações</th>
            </tr>
          </thead>
          <tbody id="tbodyPendingEvents">
            <!-- Rendered dynamically -->
          </tbody>
        </table>
      </div>

      <div id="pendingEmptyMessage" style="display: none; text-align: center; padding: 3rem 1rem; color: var(--text-muted);">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="margin-bottom: 0.5rem;"><circle cx="12" cy="12" r="10"></circle><path d="M8 12h8"></path></svg>
        <div style="font-size: 1.1rem; font-weight: 700; color: var(--text-main);">Nenhuma previsão pendente encontrada</div>
        <div style="font-size: 0.85rem;">Não há eventos que correspondam aos filtros selecionados.</div>
      </div>
    </section>

    <!-- ==================== VIEW 4: EVENTOS CONCLUÍDOS ==================== -->
    <section id="viewCompletedEvents" class="view-section">
      <div class="events-toolbar">
        <div class="toolbar-primary">
          <div class="search-box">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            <input type="text" id="inputSearchCompleted" placeholder="Pesquisar em eventos concluídos...">
          </div>

          <div style="display: flex; gap: 0.5rem; align-items: center;">
            <button id="btnExportCompletedCSV" class="btn btn-outline btn-sm">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
              <span>Exportar CSV</span>
            </button>
          </div>
        </div>

        <div class="toolbar-filters">
          <div class="form-group">
            <label style="font-size: 0.72rem;">Console</label>
            <select id="filterCompletedConsole" style="padding: 0.35rem; min-height: 32px;">
              <option value="">Todos os Consoles</option>
            </select>
          </div>
          <div class="form-group">
            <label style="font-size: 0.72rem;">Duto</label>
            <select id="filterCompletedPipeline" style="padding: 0.35rem; min-height: 32px;">
              <option value="">Todos os Dutos</option>
            </select>
          </div>
          <div class="form-group">
            <label style="font-size: 0.72rem;">UO</label>
            <select id="filterCompletedUO" style="padding: 0.35rem; min-height: 32px;">
              <option value="">Todas as UOs</option>
            </select>
          </div>
          <div class="form-group">
            <label style="font-size: 0.72rem;">Situação Conclusão</label>
            <select id="filterCompletedTiming" style="padding: 0.35rem; min-height: 32px;">
              <option value="">Todas</option>
              <option value="antecedencia">Com Antecedência</option>
              <option value="atraso">Com Atraso</option>
              <option value="noprazo">Exato no Horário</option>
            </select>
          </div>
          <div class="form-group">
            <label style="font-size: 0.72rem;">Data Prevista De</label>
            <input type="date" id="filterCompletedDateFrom" style="padding: 0.2rem 0.4rem; font-size: 0.75rem; min-height: 32px;">
          </div>
          <div class="form-group">
            <label style="font-size: 0.72rem;">Data Prevista Até</label>
            <input type="date" id="filterCompletedDateTo" style="padding: 0.2rem 0.4rem; font-size: 0.75rem; min-height: 32px;">
          </div>
        </div>
      </div>

      <!-- Mobile Expandable Completed Cards Container (Section 12) -->
      <div id="containerCompletedCards" class="completed-cards-container"></div>

      <!-- Desktop / Tablet Completed Table (9 Columns) -->
      <div id="tableCompletedWrapper" class="table-responsive">
        <table class="data-table" id="tableCompletedEvents">
          <thead>
            <tr>
              <th>Horário Previsto</th>
              <th>Horário Conclusão</th>
              <th>Diferença Efetiva</th>
              <th>Console / Duto</th>
              <th>UO / Equipamento / TAG</th>
              <th>Descrição e Observação de Conclusão</th>
              <th>Controlador</th>
              <th>Alarmes</th>
              <th style="text-align: right;">Ações</th>
            </tr>
          </thead>
          <tbody id="tbodyCompletedEvents">
            <!-- Dynamically populated -->
          </tbody>
        </table>
      </div>
      <div id="completedEmptyMessage" style="display: none; text-align: center; padding: 3rem 1rem; color: var(--text-muted);">
        Nenhum evento concluído correspondente.
      </div>
    </section>

    <!-- =========================================================================
         VIEW 5: CADASTROS UNIFICADOS (TODOS NA MESMA TELA, SEM ESPAÇO MORTO)
         ========================================================================= -->
    <section id="viewCadastros" class="view-section">
      <div class="card" style="margin-bottom: 1rem;">
        <div class="card-header" style="margin-bottom: 0.5rem;">
          <div>
            <div class="card-title">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
              <span>Painel Geral da Estrutura Operacional</span>
            </div>
            <div class="card-subtitle">Cadastre e gerencie toda a hierarquia (Consoles, Dutos, UOs, Tipos e TAGs) em um único painel integrado</div>
          </div>
        </div>

        <!-- Category Selector Bar for Mobile / Tablet Drill-Down (Section 13) -->
        <div id="cadastrosCategoryBar" class="cadastros-category-bar">
          <button type="button" class="cadastros-category-btn active" data-cat="consoles" onclick="App.UI.switchCadastrosCategory('consoles')">
            <span>Consoles</span>
            <span id="catCountConsoles" class="cat-count">0</span>
          </button>
          <button type="button" class="cadastros-category-btn" data-cat="pipelines" onclick="App.UI.switchCadastrosCategory('pipelines')">
            <span>Dutos</span>
            <span id="catCountPipelines" class="cat-count">0</span>
          </button>
          <button type="button" class="cadastros-category-btn" data-cat="uos" onclick="App.UI.switchCadastrosCategory('uos')">
            <span>UOs</span>
            <span id="catCountUOs" class="cat-count">0</span>
          </button>
          <button type="button" class="cadastros-category-btn" data-cat="types" onclick="App.UI.switchCadastrosCategory('types')">
            <span>Tipos</span>
            <span id="catCountTypes" class="cat-count">0</span>
          </button>
          <button type="button" class="cadastros-category-btn" data-cat="tags" onclick="App.UI.switchCadastrosCategory('tags')">
            <span>TAGs</span>
            <span id="catCountTags" class="cat-count">0</span>
          </button>
          <button type="button" class="cadastros-category-btn" data-cat="all" onclick="App.UI.switchCadastrosCategory('all')">
            <span>Ver Todos</span>
          </button>
        </div>
      </div>

      <!-- 3-Column Unified Responsive Grid -->
      <div class="cadastros-unified-grid cadastros-hub-grid">
        
        <!-- PAINEL 1: CONSOLES & DUTOS -->
        <div class="cadastro-hub-card" id="hubCardConsolesPipelines" data-cat-group="consoles,pipelines">
          <div class="hub-header">
            <div class="hub-title" style="color: #38bdf8;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
              <span>1. Consoles & Dutos</span>
            </div>
          </div>

          <!-- SUB-SECTION: CONSOLES -->
          <div id="subSectionConsoles" data-cat-item="consoles">
            <!-- Form Console -->
            <form id="formConsole" style="background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 6px; padding: 0.75rem;">
              <input type="hidden" id="consoleEditId" value="">
              <label style="font-size: 0.78rem;">Adicionar / Editar Console:</label>
              <div style="display: flex; gap: 0.4rem; margin-top: 0.25rem;">
                <input type="text" id="inputConsoleName" placeholder="Ex: C04" required style="min-height: 36px; padding: 0.35rem 0.6rem;">
                <button type="submit" class="btn btn-primary btn-sm" id="btnSubmitConsole">Salvar</button>
                <button type="button" class="btn btn-secondary btn-sm" id="btnCancelConsoleEdit" style="display: none;">Cancelar</button>
              </div>
            </form>

            <!-- Consoles List -->
            <div style="margin-top: 0.5rem; margin-bottom: 0.75rem;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem; gap: 0.35rem; flex-wrap: wrap;">
                <strong style="font-size: 0.825rem;">Consoles (C02-C16):</strong>
                <div style="display: flex; gap: 0.3rem; align-items: center;">
                  <select id="filterActiveConsoles" style="width: auto; min-height: 28px; padding: 0.15rem 0.35rem; font-size: 0.72rem;">
                    <option value="all">Todos</option>
                    <option value="active">Ativos</option>
                    <option value="inactive">Inativos</option>
                  </select>
                  <input type="text" id="searchConsoles" placeholder="Buscar console..." style="width: 110px; min-height: 28px; padding: 0.2rem 0.4rem; font-size: 0.75rem;">
                </div>
              </div>
              <div class="hub-list-container" style="max-height: 130px;">
                <table id="tableConsoles" class="data-table" style="font-size: 0.8rem;">
                  <thead><tr><th>Console</th><th>Dutos</th><th>Situação</th><th style="text-align: right;">Ações</th></tr></thead>
                  <tbody id="tbodyConsoles"></tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- SUB-SECTION: PIPELINES -->
          <div id="subSectionPipelines" data-cat-item="pipelines">
            <!-- Form Duto (com atalho para criar UOs na hora) -->
            <form id="formPipeline" style="background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 6px; padding: 0.75rem;">
              <input type="hidden" id="pipelineEditId" value="">
              <div style="font-weight: 700; font-size: 0.85rem; margin-bottom: 0.5rem; color: #38bdf8;">Novo / Editar Duto:</div>
              
              <div class="form-group" style="margin-bottom: 0.5rem;">
                <label for="selectPipelineConsole">Console Responsável <span class="required">*</span></label>
                <select id="selectPipelineConsole" required style="min-height: 36px; padding: 0.35rem 0.6rem;">
                  <option value="">Selecione o Console...</option>
                </select>
              </div>

              <div class="form-group" style="margin-bottom: 0.5rem;">
                <label for="inputPipelineName">Nome do Duto <span class="required">*</span></label>
                <input type="text" id="inputPipelineName" placeholder="Ex: OSCAN, OSBRA" required style="min-height: 36px; padding: 0.35rem 0.6rem;">
              </div>

              <!-- UOs Selection + Inline UO Quick Adder -->
              <div class="form-group">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                  <label>UOs Vinculadas <span class="required">* (Mínimo 2 UOs)</span></label>
                </div>

                <!-- Inline Quick UO Adder inside Duto Form -->
                <div style="display: flex; gap: 0.35rem; margin-top: 0.25rem; margin-bottom: 0.35rem;">
                  <input type="text" id="inputInlineNewUO" placeholder="+ Digitar nova UO aqui..." style="min-height: 32px; padding: 0.25rem 0.5rem; font-size: 0.78rem;">
                  <button type="button" id="btnInlineAddUO" class="btn btn-secondary btn-sm" title="Criar UO imediatamente e disponibilizar na lista">+ Criar UO</button>
                </div>

                <div id="boxPipelineUOs" class="uo-selection-box">
                  <!-- Checkboxes populated dynamically -->
                </div>
                <div class="form-help">Selecione pelo menos duas UOs para este duto.</div>
              </div>

              <div style="display: flex; justify-content: flex-end; gap: 0.5rem; margin-top: 0.6rem;">
                <button type="button" class="btn btn-secondary btn-sm" id="btnCancelPipelineEdit" style="display: none;">Cancelar</button>
                <button type="submit" class="btn btn-primary btn-sm" id="btnSubmitPipeline">Salvar Duto</button>
              </div>
            </form>

            <!-- Dutos List -->
            <div style="margin-top: 0.5rem;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem; gap: 0.35rem; flex-wrap: wrap;">
                <strong style="font-size: 0.825rem;">Dutos Registrados:</strong>
                <div style="display: flex; gap: 0.3rem; align-items: center;">
                  <select id="filterActivePipelines" style="width: auto; min-height: 28px; padding: 0.15rem 0.35rem; font-size: 0.72rem;">
                    <option value="all">Todos</option>
                    <option value="active">Ativos</option>
                    <option value="inactive">Inativos</option>
                  </select>
                  <input type="text" id="searchPipelines" placeholder="Buscar duto..." style="width: 120px; min-height: 28px; padding: 0.2rem 0.4rem; font-size: 0.75rem;">
                </div>
              </div>
              <div class="hub-list-container">
                <table id="tablePipelines" class="data-table" style="font-size: 0.8rem;">
                  <thead><tr><th>Duto</th><th>Console</th><th>UOs</th><th>Situação</th><th style="text-align: right;">Ações</th></tr></thead>
                  <tbody id="tbodyPipelines"></tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <!-- PAINEL 2: UOS & TIPOS DE EQUIPAMENTOS -->
        <div class="cadastro-hub-card" id="hubCardUOsTypes" data-cat-group="uos,types">
          <div class="hub-header">
            <div class="hub-title" style="color: #4ade80;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
              <span>2. Unidades Operacionais (UOs) & Tipos</span>
            </div>
          </div>

          <!-- SUB-SECTION: UOs -->
          <div id="subSectionUOs" data-cat-item="uos">
            <!-- Form UO (Permite digitar UMA ou VÁRIAS UOs de uma vez separadas por vírgula ou linha) -->
            <form id="formUO" style="background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 6px; padding: 0.75rem;">
              <input type="hidden" id="uoEditId" value="">
              <label for="inputUOName" style="font-size: 0.78rem;">Cadastrar UOs (Digite uma ou várias separadas por vírgula):</label>
              <div style="display: flex; gap: 0.4rem; margin-top: 0.25rem;">
                <input type="text" id="inputUOName" placeholder="Ex: REFAP, TEDEP, REPLAN, TEBAR" required style="min-height: 36px; padding: 0.35rem 0.6rem;">
                <button type="submit" class="btn btn-primary btn-sm" id="btnSubmitUO">Salvar UO</button>
                <button type="button" class="btn btn-secondary btn-sm" id="btnCancelUOEdit" style="display: none;">Cancelar</button>
              </div>
              <div class="form-help">Você pode cadastrar várias UOs juntas digitando nomes separados por vírgula.</div>
            </form>

            <!-- UOs List -->
            <div style="margin-top: 0.5rem;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem; gap: 0.35rem; flex-wrap: wrap;">
                <strong style="font-size: 0.825rem;">UOs Cadastradas:</strong>
                <div style="display: flex; gap: 0.3rem; align-items: center;">
                  <select id="filterActiveUOs" style="width: auto; min-height: 28px; padding: 0.15rem 0.35rem; font-size: 0.72rem;">
                    <option value="all">Todos</option>
                    <option value="active">Ativos</option>
                    <option value="inactive">Inativos</option>
                  </select>
                  <input type="text" id="searchUOs" placeholder="Buscar UO..." style="width: 120px; min-height: 28px; padding: 0.2rem 0.4rem; font-size: 0.75rem;">
                </div>
              </div>
              <div class="hub-list-container" style="max-height: 140px;">
                <table id="tableUOs" class="data-table" style="font-size: 0.8rem;">
                  <thead><tr><th>Nome da UO</th><th>Dutos</th><th>Tipos</th><th>Situação</th><th style="text-align: right;">Ações</th></tr></thead>
                  <tbody id="tbodyUOs"></tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- SUB-SECTION: EQUIPMENT TYPES -->
          <div id="subSectionTypes" data-cat-item="types">
            <!-- Form Tipo de Equipamento -->
            <form id="formEquipmentType" style="background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 6px; padding: 0.75rem; margin-top: 0.5rem;">
              <input type="hidden" id="equipmentTypeEditId" value="">
              <div style="font-weight: 700; font-size: 0.85rem; margin-bottom: 0.4rem; color: #4ade80;">Novo Tipo de Equipamento:</div>
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.4rem;">
                <div class="form-group">
                  <label for="selectEquipmentTypeUO">UO Vinculada <span class="required">*</span></label>
                  <select id="selectEquipmentTypeUO" required style="min-height: 36px; padding: 0.2rem 0.5rem; font-size: 0.8rem;">
                    <option value="">Selecione a UO...</option>
                  </select>
                </div>
                <div class="form-group">
                  <label for="inputEquipmentTypeName">Tipo <span class="required">*</span></label>
                  <input type="text" id="inputEquipmentTypeName" placeholder="Ex: Tanque, Bomba" required style="min-height: 36px; padding: 0.2rem 0.5rem; font-size: 0.8rem;">
                </div>
              </div>
              <div style="display: flex; justify-content: flex-end; gap: 0.4rem; margin-top: 0.4rem;">
                <button type="button" class="btn btn-secondary btn-sm" id="btnCancelEquipmentTypeEdit" style="display: none;">Cancelar</button>
                <button type="submit" class="btn btn-primary btn-sm" id="btnSubmitEquipmentType">Salvar Tipo</button>
              </div>
            </form>

            <!-- Tipos List -->
            <div style="margin-top: 0.5rem;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem; gap: 0.35rem; flex-wrap: wrap;">
                <strong style="font-size: 0.825rem;">Tipos por UO:</strong>
                <div style="display: flex; gap: 0.3rem; align-items: center;">
                  <select id="filterActiveEquipmentTypes" style="width: auto; min-height: 28px; padding: 0.15rem 0.35rem; font-size: 0.72rem;">
                    <option value="all">Todos</option>
                    <option value="active">Ativos</option>
                    <option value="inactive">Inativos</option>
                  </select>
                  <input type="text" id="searchEquipmentTypes" placeholder="Buscar tipo..." style="width: 120px; min-height: 28px; padding: 0.2rem 0.4rem; font-size: 0.75rem;">
                </div>
              </div>
              <div class="hub-list-container" style="max-height: 140px;">
                <table id="tableEquipmentTypes" class="data-table" style="font-size: 0.8rem;">
                  <thead><tr><th>Tipo</th><th>UO</th><th>TAGs</th><th>Situação</th><th style="text-align: right;">Ações</th></tr></thead>
                  <tbody id="tbodyEquipmentTypes"></tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <!-- PAINEL 3: TAGS DE EQUIPAMENTOS -->
        <div class="cadastro-hub-card" id="hubCardTags" data-cat-group="tags" data-cat-item="tags">
          <div class="hub-header">
            <div class="hub-title" style="color: #fb923c;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path><line x1="7" y1="7" x2="7.01" y2="7"></line></svg>
              <span>3. TAGs de Equipamentos</span>
            </div>
          </div>

          <!-- Form TAG -->
          <form id="formEquipmentTag" style="background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 6px; padding: 0.75rem;">
            <input type="hidden" id="tagEditId" value="">
            <div style="font-weight: 700; font-size: 0.85rem; margin-bottom: 0.4rem; color: #fb923c;">Novo / Editar TAG:</div>
            
            <div class="form-group" style="margin-bottom: 0.4rem;">
              <label for="selectTagUO">Unidade Operacional (UO) <span class="required">*</span></label>
              <select id="selectTagUO" required style="min-height: 36px; padding: 0.2rem 0.5rem; font-size: 0.8rem;">
                <option value="">Selecione a UO...</option>
              </select>
            </div>

            <div class="form-group" style="margin-bottom: 0.4rem;">
              <label for="selectTagType">Tipo de Equipamento <span class="required">*</span></label>
              <select id="selectTagType" required disabled style="min-height: 36px; padding: 0.2rem 0.5rem; font-size: 0.8rem;">
                <option value="">Selecione primeiro a UO...</option>
              </select>
            </div>

            <div class="form-group">
              <label for="inputTagCode">Código do TAG <span class="required">*</span></label>
              <input type="text" id="inputTagCode" placeholder="Ex: TQ-804, BB-101A" required style="min-height: 36px; padding: 0.35rem 0.6rem;">
              <div class="form-help">Regra global: cada TAG pertence exclusivamente a uma única UO.</div>
            </div>

            <div style="display: flex; justify-content: flex-end; gap: 0.4rem; margin-top: 0.6rem;">
              <button type="button" class="btn btn-secondary btn-sm" id="btnCancelTagEdit" style="display: none;">Cancelar</button>
              <button type="submit" class="btn btn-primary btn-sm" id="btnSubmitTag">Salvar TAG</button>
            </div>
          </form>

          <!-- TAGs List -->
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem; gap: 0.35rem; flex-wrap: wrap;">
              <strong style="font-size: 0.825rem;">TAGs Registrados:</strong>
              <div style="display: flex; gap: 0.3rem; align-items: center;">
                <select id="filterActiveTags" style="width: auto; min-height: 28px; padding: 0.15rem 0.35rem; font-size: 0.72rem;">
                  <option value="all">Todos</option>
                  <option value="active">Ativos</option>
                  <option value="inactive">Inativos</option>
                </select>
                <input type="text" id="searchTags" data-alias="searchEquipmentTags" placeholder="Buscar TAG..." style="width: 120px; min-height: 28px; padding: 0.2rem 0.4rem; font-size: 0.75rem;">
              </div>
            </div>
            <div class="hub-list-container">
              <table id="tableEquipmentTags" class="data-table" style="font-size: 0.8rem;">
                <thead><tr><th>TAG</th><th>UO</th><th>Tipo</th><th>Situação</th><th style="text-align: right;">Ações</th></tr></thead>
                <tbody id="tbodyEquipmentTags"></tbody>
              </table>
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- ==================== VIEW 6: CONFIGURAÇÕES DE ALERTAS ==================== -->
    <section id="viewConfigAlerts" class="view-section">
      <!-- Notice on browser restrictions -->
      <div class="notice-banner">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink: 0; color: #38bdf8;"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
        <div>
          <strong style="color: var(--text-main);">Limitações do Ambiente de Navegador Web:</strong>
          <ul style="margin-left: 1.25rem; margin-top: 0.25rem; font-size: 0.8rem; line-height: 1.4;">
            <li>A aplicação precisa permanecer aberta em uma aba ativa para monitorar e executar os alarmes locais.</li>
            <li>Se o navegador for fechado, os alarmes não soarão em segundo plano sem a aplicação rodando.</li>
            <li>O navegador pode bloquear o áudio até que ocorra uma interação do usuário com a página (clique).</li>
            <li>Notificações do sistema operacional exigem que a permissão seja expressamente concedida pelo controlador.</li>
            <li>Políticas de segurança do sistema operacional e navegadores impedem maximização ou foco forçado de janelas.</li>
          </ul>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <div class="card-title">Parâmetros Gerais de Alarmes, Exibição e Notificações</div>
        </div>

        <form id="formAlertSettings">
          <div class="form-grid">
            <div class="form-group">
              <label for="inputSettingsUserName">Nome do Controlador neste Computador</label>
              <input type="text" id="inputSettingsUserName" placeholder="Usuário local">
              <div class="form-help">Utilizado para rastreabilidade nas auditorias e registros</div>
            </div>

            <div class="form-group">
              <label for="inputDefaultLeadTime">Antecedência Padrão dos Alarmes (minutos)</label>
              <input type="number" id="inputDefaultLeadTime" min="0" max="1440" value="15">
              <div class="form-help">Tempo prévio para alertar o controlador antes do horário</div>
            </div>

            <div class="form-group">
              <label for="selectSettingsViewMode">Modo de Exibição / Layout da Interface</label>
              <select id="selectSettingsViewMode">
                <option value="auto">Automático (Recomendado - Detecta a tela)</option>
                <option value="compact">Compacto (Alta Densidade Operacional)</option>
                <option value="mobile">Celular (320px a 767px)</option>
                <option value="tablet">Tablet (768px a 1199px)</option>
                <option value="conventional">Tela Convencional (1200px a 1599px)</option>
                <option value="widescreen">Widescreen (1600px a 2199px)</option>
                <option value="ultrawide">Ultrawide / Videowall (2200px+)</option>
              </select>
              <div class="form-help">Permite forçar um formato específico ou manter adaptação automática</div>
            </div>

            <div class="form-group">
              <label for="selectSettingsTheme">Tema Visual Operacional</label>
              <select id="selectSettingsTheme">
                <option value="dark">Tema 1: Controle Escuro (Padrão Noturno 24h)</option>
                <option value="light">Tema 2: Profissional Claro (Ambientes Iluminados)</option>
                <option value="industrial">Tema 3: Industrial Alto Contraste (Máxima Legibilidade)</option>
              </select>
              <div class="form-help">Contraste calibrado para turnos prolongados</div>
            </div>

            <div class="form-group">
              <label for="selectSoundType">Tipo de Sinal Sonoro</label>
              <select id="selectSoundType">
                <option value="chime">Chime Harmônico (Sutil e Melódico)</option>
                <option value="beep">Beep Duplo (Clássico)</option>
                <option value="siren">Sirene Operacional (Urgência)</option>
                <option value="blip">Blip Suave</option>
              </select>
            </div>

            <div class="form-group">
              <label for="rangeSoundVolume">Volume do Alarme: <span id="labelVolumeValue">80%</span></label>
              <input type="range" id="rangeSoundVolume" min="0" max="100" value="80" style="padding: 0;">
            </div>

            <!-- Toggles -->
            <div class="form-group span-full">
              <label style="margin-bottom: 0.5rem;">Canais e Formas de Alerta Ativos</label>
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 0.75rem;">
                <label class="form-checkbox">
                  <input type="checkbox" id="checkSettingSound" checked>
                  <span>Sinal Sonoro Local (Web Audio API)</span>
                </label>
                <label class="form-checkbox">
                  <input type="checkbox" id="checkSettingVisualModal" checked>
                  <span>Janela Modal Flutuante de Alerta</span>
                </label>
                <label class="form-checkbox">
                  <input type="checkbox" id="checkSettingHighlightCard" checked>
                  <span>Destaque Visual do Cartão na Lista</span>
                </label>
                <label class="form-checkbox">
                  <input type="checkbox" id="checkSettingPulsing" checked>
                  <span>Efeito Visual de Pulsação Luminosa</span>
                </label>
                <label class="form-checkbox">
                  <input type="checkbox" id="checkSettingChangeTitle" checked>
                  <span>Alteração Dinâmica do Título da Aba</span>
                </label>
                <label class="form-checkbox">
                  <input type="checkbox" id="checkSettingNotification">
                  <span>Notificação do Navegador (Web Notifications)</span>
                </label>
              </div>
            </div>

            <!-- Repetition Settings -->
            <div class="form-group span-full" style="border-top: 1px solid var(--border-color); padding-top: 1rem;">
              <label class="form-checkbox" style="font-weight: 700;">
                <input type="checkbox" id="checkSettingRepeat" checked>
                <span>Repetir Alarme até Reconhecimento</span>
              </label>
              <div style="display: flex; gap: 1rem; margin-top: 0.5rem; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 180px;">
                  <label for="inputSettingRepeatInterval">Intervalo de Repetição (minutos)</label>
                  <input type="number" id="inputSettingRepeatInterval" min="1" max="60" value="2">
                </div>
                <div style="flex: 1; min-width: 180px;">
                  <label for="inputSettingMaxRepeats">Número Máximo de Repetições</label>
                  <input type="number" id="inputSettingMaxRepeats" min="1" max="20" value="5">
                </div>
              </div>
            </div>
          </div>

          <!-- Test Actions Bar -->
          <div style="border-top: 1px solid var(--border-color); padding-top: 1.25rem; margin-top: 1.25rem; display: flex; gap: 0.6rem; flex-wrap: wrap; justify-content: space-between; align-items: center;">
            <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
              <button type="button" id="btnTestSound" class="btn btn-outline btn-sm">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>
                <span>Testar Som</span>
              </button>

              <button type="button" id="btnTestVisual" class="btn btn-outline btn-sm">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                <span>Testar Alerta Visual</span>
              </button>

              <button type="button" id="btnRequestNotifPermission" class="btn btn-outline btn-sm">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
                <span id="btnRequestNotifText">Permissão de Notificações</span>
              </button>

              <!-- Prominent Test Notification Button -->
              <button type="button" id="btnTestNotif" class="btn btn-warning btn-sm">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
                <span>Testar Notificação do Navegador</span>
              </button>
            </div>

            <div style="display: flex; gap: 0.5rem;">
              <button type="button" id="btnResetAlertSettings" class="btn btn-secondary btn-sm">Restaurar Padrões</button>
              <button type="submit" class="btn btn-primary btn-sm">Salvar Configurações</button>
            </div>
          </div>
        </form>
      </div>
    </section>

    <!-- ==================== VIEW 7: CONFIGURAÇÕES DE CORES ==================== -->
    <section id="viewConfigColors" class="view-section">
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">Classificação por Faixas de Tempo e Cores</div>
            <div class="card-subtitle">As faixas indicam a proximidade dos eventos. Intervalos são ordenados e contíguos sem sobreposições ou lacunas.</div>
          </div>
          <button id="btnResetColorRanges" class="btn btn-outline btn-sm">Restaurar Faixas Padrão</button>
        </div>

        <div class="notice-banner">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink: 0;"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
          <div>
            <strong>Condição "Atrasado" tratada separadamente:</strong> Todo evento cujo horário previsto já foi ultrapassado é automaticamente classificado como <strong>Atrasado (Vermelho Escuro)</strong> e priorizado no topo, independentemente das faixas de tempo futuro.
          </div>
        </div>

        <!-- Visual Preview Bar & Chain (Section 14) -->
        <div style="margin-top: 1rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
            <label style="font-weight: 700; font-size: 0.85rem;">Prévia Visual das Faixas de Tempo (0 a 60+ minutos):</label>
            <span id="colorChainPreview" style="font-size: 0.78rem; font-family: monospace; color: #38bdf8; font-weight: 700;">Encadeamento: 0 ─ 15 ─ 30 ─ 45 ─ 60 ─ Normal</span>
          </div>
          <div id="colorPreviewBar" class="color-preview-bar">
            <!-- Dynamically populated preview blocks -->
          </div>
        </div>

        <!-- Mobile Cards for Color Ranges (Section 14) -->
        <div id="containerColorRangeCards" class="color-range-cards"></div>

        <!-- Table of Ranges -->
        <div id="tableColorRangesWrapper" class="table-responsive" style="margin-top: 1rem;">
          <table class="data-table" id="tableColorRanges">
            <thead>
              <tr>
                <th>Nome da Faixa</th>
                <th>Amostra</th>
                <th>Limite Inicial (min)</th>
                <th>Limite Final (min)</th>
                <th>Piscar / Pulsar</th>
                <th>Sinal Sonoro</th>
                <th>Prioridade</th>
                <th style="text-align: right;">Ações</th>
              </tr>
            </thead>
            <tbody id="tbodyColorRanges">
              <!-- Dynamically populated -->
            </tbody>
          </table>
        </div>

        <!-- Add/Edit Color Range Form -->
        <div style="margin-top: 1.5rem; border-top: 1px solid var(--border-color); padding-top: 1.25rem;">
          <h4 id="titleFormRange" style="font-size: 0.95rem; font-weight: 700; margin-bottom: 0.75rem;">Editar / Nova Faixa de Tempo</h4>
          <form id="formColorRange">
            <input type="hidden" id="rangeEditId" value="">
            <div class="form-grid">
              <div class="form-group">
                <label for="inputRangeName">Nome da Faixa <span class="required">*</span></label>
                <input type="text" id="inputRangeName" placeholder="Ex: Crítico, Urgente" required>
              </div>

              <div class="form-group">
                <label for="inputRangeColor">Cor de Destaque <span class="required">*</span></label>
                <div style="display: flex; gap: 0.5rem; align-items: center;">
                  <input type="color" id="inputRangeColor" value="#dc2626" style="width: 50px; height: 38px; padding: 2px; cursor: pointer;">
                  <input type="text" id="inputRangeColorText" value="#dc2626" style="flex: 1;" required>
                </div>
              </div>

              <div class="form-group">
                <label for="inputRangeMin">Limite Inicial (minutos) <span class="required">*</span></label>
                <input type="number" id="inputRangeMin" min="0" max="99999" required>
              </div>

              <div class="form-group">
                <label for="inputRangeMax">Limite Final (minutos) <span class="required">*</span></label>
                <input type="number" id="inputRangeMax" min="1" max="999999" required>
              </div>

              <div class="form-group">
                <label for="inputRangePriority">Prioridade Visual (1 = Mais alta)</label>
                <input type="number" id="inputRangePriority" min="1" max="10" value="1" required>
              </div>

              <div class="form-group" style="justify-content: center;">
                <label class="form-checkbox">
                  <input type="checkbox" id="checkRangeBlink">
                  <span>Piscar / Pulsar Eventos nesta Faixa</span>
                </label>
                <label class="form-checkbox" style="margin-top: 0.35rem;">
                  <input type="checkbox" id="checkRangeSound">
                  <span>Emitir Alerta Sonoro nesta Faixa</span>
                </label>
              </div>
            </div>

            <div style="display: flex; justify-content: flex-end; gap: 0.5rem; margin-top: 1rem;">
              <button type="button" id="btnCancelRangeEdit" class="btn btn-secondary btn-sm" style="display: none;">Cancelar</button>
              <button type="submit" class="btn btn-primary btn-sm" id="btnSubmitRange">Salvar Faixa de Cor</button>
            </div>
          </form>
        </div>
      </div>
    </section>

    <!-- ==================== VIEW 8: BACKUP E DADOS ==================== -->
    <section id="viewBackup" class="view-section">
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">Backup Completo e Restauração de Dados</div>
            <div class="card-subtitle">Todos os cadastros, eventos, históricos e configurações em arquivo JSON</div>
          </div>
          <span id="labelLastBackupDate" style="font-size: 0.8rem; color: var(--text-muted);">Último backup: Nunca</span>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.25rem;">
          <!-- Export Section -->
          <div style="background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 8px; padding: 1.25rem;">
            <h4 style="font-size: 0.95rem; font-weight: 700; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.4rem;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
              <span>Exportar Backup do Sistema</span>
            </h4>
            <p style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 1rem;">
              Gera um arquivo JSON padronizado contendo todas as tabelas, configurações, consoles, dutos, UOs, TAGs e histórico completo.
            </p>
            <button id="btnExportJSON" class="btn btn-primary" style="width: 100%;">
              <span>Baixar Backup Completo (JSON)</span>
            </button>
          </div>

          <!-- Import Section -->
          <div style="background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 8px; padding: 1.25rem;">
            <h4 style="font-size: 0.95rem; font-weight: 700; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.4rem;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
              <span>Restaurar / Importar Backup</span>
            </h4>
            <p style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 0.75rem;">
              Selecione um arquivo JSON de backup para validar e carregar na base local.
            </p>
            <input type="file" id="inputImportBackupFile" accept=".json" style="margin-bottom: 0.75rem;">
            <div style="display: flex; gap: 0.5rem;">
              <button id="btnTriggerImportValidate" class="btn btn-secondary" style="flex: 1;" disabled>
                <span>Validar Arquivo</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Export CSV Section -->
        <div style="margin-top: 1.5rem; border-top: 1px solid var(--border-color); padding-top: 1.25rem;">
          <h4 style="font-size: 0.95rem; font-weight: 700; margin-bottom: 0.75rem;">Exportação de Relatórios em CSV (Excel)</h4>
          <p style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 1rem;">
            Arquivos CSV formatados para Microsoft Excel (separador ponto e vírgula, codificação UTF-8 com BOM e formatos brasileiros de data e hora).
          </p>
          <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
            <button id="btnExportCSVAllPending" class="btn btn-outline btn-sm">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
              <span>Eventos Pendentes (CSV)</span>
            </button>

            <button id="btnExportCSVAllCompleted" class="btn btn-outline btn-sm">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
              <span>Eventos Concluídos (CSV)</span>
            </button>

            <button id="btnExportCSVCadastros" class="btn btn-outline btn-sm">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
              <span>Estrutura Cadastral (CSV)</span>
            </button>
          </div>
        </div>

        <!-- Demonstration & Maintenance -->
        <div style="margin-top: 1.5rem; border-top: 1px solid var(--border-color); padding-top: 1.25rem;">
          <h4 style="font-size: 0.95rem; font-weight: 700; margin-bottom: 0.75rem;">Massa de Dados e Demonstração Operacional</h4>
          <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
            <button id="btnLoadDemoData" class="btn btn-secondary btn-sm">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
              <span>Carregar Dados de Demonstração</span>
            </button>

            <button id="btnWipeAllData" class="btn btn-danger btn-sm">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
              <span>Apagar Todos os Dados</span>
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== VIEW 9: DIAGNÓSTICO ==================== -->
    <section id="viewDiagnostic" class="view-section">
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">Diagnóstico Técnico da Aplicação</div>
            <div class="card-subtitle">Verificação da integridade do IndexedDB, APIs do navegador e logs internos</div>
          </div>
          <button id="btnCopyDiagnostic" class="btn btn-outline btn-sm">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
            <span>Copiar Diagnóstico</span>
          </button>
        </div>

        <div class="form-grid" style="margin-bottom: 1.25rem;">
          <div class="metric-card">
            <div class="metric-data">
              <div class="metric-value" id="diagAppVersion">v1.1.0</div>
              <div class="metric-label">Versão da Aplicação</div>
            </div>
          </div>
          <div class="metric-card">
            <div class="metric-data">
              <div class="metric-value" id="diagDBStatus">Online</div>
              <div class="metric-label">IndexedDB (Esquema v1)</div>
            </div>
          </div>
          <div class="metric-card">
            <div class="metric-data">
              <div class="metric-value" id="diagAudioStatus">Suspenso</div>
              <div class="metric-label">Web Audio API</div>
            </div>
          </div>
          <div class="metric-card">
            <div class="metric-data">
              <div class="metric-value" id="diagNotifStatus">Pendente</div>
              <div class="metric-label">Web Notifications</div>
            </div>
          </div>
        </div>

        <h4 style="font-size: 0.95rem; font-weight: 700; margin-bottom: 0.5rem;">Contagem de Registros por Coleção</h4>
        <div class="table-responsive" style="margin-bottom: 1.5rem;">
          <table class="data-table">
            <thead>
              <tr>
                <th>Coleção (Object Store)</th>
                <th>Finalidade</th>
                <th>Total Registros</th>
                <th>Ativos</th>
                <th>Inativos</th>
              </tr>
            </thead>
            <tbody id="tbodyDiagCollections">
              <!-- Dynamically populated -->
            </tbody>
          </table>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
          <h4 style="font-size: 0.95rem; font-weight: 700;">Log Interno de Erros e Eventos</h4>
          <button id="btnClearDiagLogs" class="btn btn-outline btn-sm">Limpar Logs</button>
        </div>
        <div class="table-responsive">
          <table class="data-table">
            <thead>
              <tr>
                <th>Data / Hora</th>
                <th>Contexto</th>
                <th>Mensagem</th>
                <th>Detalhes Técnicos</th>
              </tr>
            </thead>
            <tbody id="tbodyDiagLogs">
              <tr>
                <td colspan="4" style="text-align: center; color: var(--text-muted); padding: 1.5rem;">Nenhum erro registrado no sistema.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

  <!-- Barra de Navegação Inferior Fixa para Celular (Section 5.1) — único ponto de ação rápida (#fabAddEvent central) -->
  <nav id="mobileBottomNav" class="mobile-bottom-nav" aria-label="Navegação Rápida Mobile">
    <button type="button" class="bottom-nav-item active" data-target="viewDashboard">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="9"></rect><rect x="14" y="3" width="7" height="5"></rect><rect x="14" y="12" width="7" height="9"></rect><rect x="3" y="16" width="7" height="5"></rect></svg>
      <span>Painel</span>
    </button>
    <button type="button" class="bottom-nav-item" data-target="viewPendingEvents">
      <span id="badgeBottomNavPending" class="bottom-nav-badge">0</span>
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
      <span>Pendentes</span>
    </button>
    <button type="button" id="fabAddEvent" class="bottom-nav-fab" data-target="viewNewEvent" title="Nova Previsão Operacional" aria-label="Nova Previsão">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
    </button>
    <button type="button" id="btnBottomNavMore" class="bottom-nav-item">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="1"></circle><circle cx="19" cy="12" r="1"></circle><circle cx="5" cy="12" r="1"></circle></svg>
      <span>Mais</span>
    </button>
  </nav>

</main>

  <!-- ==================== MODALS ==================== -->

  <!-- Modal 1: Disparo de Alerta Operacional -->
  <div id="modalAlarmTrigger" class="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="modalAlarmTitle">
    <div class="modal-box alarm-modal-box">
      <div class="modal-header alarm-modal-header">
        <h3 id="modalAlarmTitle" style="color: #ffffff;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
          <span>ALERTA DE PREVISÃO OPERACIONAL!</span>
        </h3>
        <button class="modal-close" id="btnCloseAlarmModal" style="color: #ffffff;" aria-label="Fechar alerta">&times;</button>
      </div>
      <div class="modal-body">
        <div style="background: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444; padding: 0.85rem; border-radius: 4px; margin-bottom: 1rem;">
          <div id="alarmModalHierarchy" style="font-size: 0.85rem; font-weight: 700; color: #38bdf8;">CONSOLE | DUTO | UO | TAG</div>
          <div id="alarmModalDescription" style="font-size: 1.2rem; font-weight: 800; color: var(--text-main); margin-top: 0.35rem;">Descrição do Evento</div>
          <div id="alarmModalNotes" style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.35rem;">Observações</div>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 6px; padding: 0.75rem 1rem;">
          <div>
            <div style="font-size: 0.75rem; color: var(--text-muted);">Horário Previsto</div>
            <div id="alarmModalScheduledTime" style="font-size: 1.1rem; font-weight: 700; font-family: monospace;">--:--</div>
          </div>
          <div style="text-align: right;">
            <div style="font-size: 0.75rem; color: var(--text-muted);">Tempo Restante / Atraso</div>
            <div id="alarmModalCountdown" style="font-size: 1.2rem; font-weight: 800; color: #ef4444; font-family: monospace;">--</div>
          </div>
        </div>
      </div>
      <div class="modal-footer" style="flex-wrap: wrap;">
        <button id="btnAlarmAcknowledge" class="btn btn-warning">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg>
          <span>Reconhecer Alarme</span>
        </button>

        <button id="btnAlarmSnoozePrompt" class="btn btn-secondary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
          <span>Adiar...</span>
        </button>

        <button id="btnAlarmCompleteDirect" class="btn btn-success">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
          <span>Concluir Evento</span>
        </button>

        <button id="btnAlarmOpenDetails" class="btn btn-outline">Abrir Detalhes</button>
      </div>
    </div>
  </div>

  <!-- Modal 2: Adiar Alarme (Snooze Prompt) -->
  <div id="modalSnooze" class="modal-overlay" role="dialog" aria-modal="true">
    <div class="modal-box" style="max-width: 400px;">
      <div class="modal-header">
        <h3>Adiar Alarme Operacional</h3>
        <button class="modal-close" id="btnCloseSnoozeModal">&times;</button>
      </div>
      <div class="modal-body">
        <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 1rem;">
          Selecione por quantos minutos deseja adiar este alerta. Um novo horário de disparo será agendado.
        </p>
        <div style="display: flex; gap: 0.5rem; margin-bottom: 1rem;">
          <button class="btn btn-outline btn-sm btn-quick-snooze" data-min="5">5 min</button>
          <button class="btn btn-outline btn-sm btn-quick-snooze" data-min="10">10 min</button>
          <button class="btn btn-outline btn-sm btn-quick-snooze" data-min="15">15 min</button>
          <button class="btn btn-outline btn-sm btn-quick-snooze" data-min="30">30 min</button>
        </div>
        <div class="form-group">
          <label for="inputSnoozeMinutes">Ou informe a quantidade de minutos:</label>
          <input type="number" id="inputSnoozeMinutes" min="1" max="1440" value="5">
        </div>
      </div>
      <div class="modal-footer">
        <button id="btnCancelSnooze" class="btn btn-secondary">Cancelar</button>
        <button id="btnConfirmSnooze" class="btn btn-primary">Confirmar Adiamento</button>
      </div>
    </div>
  </div>

  <!-- Modal 3: Concluir Evento -->
  <div id="modalCompleteEvent" class="modal-overlay" role="dialog" aria-modal="true">
    <div class="modal-box">
      <div class="modal-header">
        <h3>Conclusão de Previsão Operacional</h3>
        <button class="modal-close" id="btnCloseCompleteModal">&times;</button>
      </div>
      <div class="modal-body">
        <div style="margin-bottom: 1rem;">
          <div id="completeModalEventDesc" style="font-weight: 700; font-size: 1.05rem;">Descrição da Atividade</div>
          <div id="completeModalHierarchy" style="font-size: 0.8rem; color: #38bdf8; margin-top: 0.2rem;">Console &bull; Duto &bull; UO</div>
        </div>

        <div style="background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 6px; padding: 0.75rem 1rem; margin-bottom: 1rem; display: flex; justify-content: space-between;">
          <div>
            <div style="font-size: 0.75rem; color: var(--text-muted);">Horário Previsto</div>
            <div id="completeModalScheduledTime" style="font-weight: 700; font-family: monospace;">--:--</div>
          </div>
          <div>
            <div style="font-size: 0.75rem; color: var(--text-muted);">Horário Efetivo</div>
            <div id="completeModalActualTime" style="font-weight: 700; font-family: monospace; color: #4ade80;">--:--</div>
          </div>
          <div>
            <div style="font-size: 0.75rem; color: var(--text-muted);">Diferença Calculada</div>
            <div id="completeModalTimeDiff" style="font-weight: 700;">--</div>
          </div>
        </div>

        <div class="form-group">
          <label for="inputCompleteNotes">Observações da Conclusão (Opcional)</label>
          <textarea id="inputCompleteNotes" rows="3" placeholder="Informações de encerramento, condições operacionais, alinhamentos finais..."></textarea>
        </div>
      </div>
      <div class="modal-footer">
        <button id="btnCancelCompleteModal" class="btn btn-secondary">Cancelar</button>
        <button id="btnConfirmCompleteModal" class="btn btn-success">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
          <span>Confirmar Conclusão</span>
        </button>
      </div>
    </div>
  </div>

  <!-- Modal 4: Reabrir Evento -->
  <div id="modalReopenEvent" class="modal-overlay" role="dialog" aria-modal="true">
    <div class="modal-box">
      <div class="modal-header">
        <h3>Reabrir Evento Operacional</h3>
        <button class="modal-close" id="btnCloseReopenModal">&times;</button>
      </div>
      <div class="modal-body">
        <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 1rem;">
          Esta ação retornará o evento para a lista de <strong>Eventos Pendentes</strong>. O histórico da conclusão anterior será preservado integralmente na auditoria.
        </p>

        <div id="boxReopenPastWarning" class="notice-banner warning" style="display: none;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
          <div>
            O horário previsto original deste evento já expirou. Você pode informar uma nova data e hora prevista para reativação do alarme:
          </div>
        </div>

        <div class="form-grid">
          <div class="form-group">
            <label for="inputReopenDate">Nova Data Prevista</label>
            <input type="date" id="inputReopenDate">
          </div>
          <div class="form-group">
            <label for="inputReopenTime">Nova Hora Prevista</label>
            <input type="time" id="inputReopenTime">
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button id="btnCancelReopenModal" class="btn btn-secondary">Cancelar</button>
        <button id="btnConfirmReopenModal" class="btn btn-warning">Confirmar Reabertura</button>
      </div>
    </div>
  </div>

  <!-- Modal 5: Detalhes do Evento & Histórico de Auditoria (Inclui desenho da caneta se houver) -->
  <div id="modalEventDetails" class="modal-overlay" role="dialog" aria-modal="true">
    <div class="modal-box modal-lg">
      <div class="modal-header">
        <h3>Detalhes da Previsão e Histórico de Auditoria</h3>
        <button class="modal-close" id="btnCloseDetailsModal">&times;</button>
      </div>
      <div class="modal-body">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.75rem; background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 8px; padding: 1rem; margin-bottom: 1.25rem;">
          <div>
            <div style="font-size: 0.72rem; color: var(--text-muted);">Console / Duto / UO</div>
            <div id="detailsModalPath" style="font-weight: 700; color: #38bdf8;">--</div>
          </div>
          <div>
            <div style="font-size: 0.72rem; color: var(--text-muted);">Equipamento / TAG</div>
            <div id="detailsModalEquipment" style="font-weight: 700;">--</div>
          </div>
          <div>
            <div style="font-size: 0.72rem; color: var(--text-muted);">Horário Previsto</div>
            <div id="detailsModalSchedule" style="font-weight: 700; font-family: monospace;">--</div>
          </div>
          <div>
            <div style="font-size: 0.72rem; color: var(--text-muted);">Situação Atual</div>
            <div id="detailsModalStatus" style="font-weight: 700;">--</div>
          </div>
          <div class="span-full">
            <div style="font-size: 0.72rem; color: var(--text-muted);">Descrição da Atividade</div>
            <div id="detailsModalDescription" style="font-weight: 600; color: var(--text-main);">--</div>
          </div>
          <div class="span-full" id="detailsModalNotesBox">
            <div style="font-size: 0.72rem; color: var(--text-muted);">Observações</div>
            <div id="detailsModalNotes" style="font-size: 0.85rem; color: var(--text-secondary); font-style: italic;">--</div>
          </div>
          <!-- Unified Stylus Drawing Container (Section 24 Item 10) -->
          <div class="span-full" id="detailsModalDrawingBox" data-alias="detailsStylusContainer" style="display: none;">
            <div style="font-size: 0.72rem; color: var(--text-muted); margin-bottom: 0.35rem;">Anotação Manuscrita / Desenho da Caneta:</div>
            <div id="detailsStylusContainer">
              <img id="detailsModalDrawingImg" src="" alt="Anotação com Caneta" style="max-width: 100%; border: 1px solid var(--border-color); border-radius: 6px; background: #0f172a;">
            </div>
          </div>
        </div>

        <h4 style="font-size: 0.95rem; font-weight: 700; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.4rem;">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 14 14"></polyline></svg>
          <span>Trilha de Auditoria e Rastreabilidade</span>
        </h4>
        <div id="detailsTimeline" class="timeline">
          <!-- Dynamically filled timeline items -->
        </div>
      </div>
      <div class="modal-footer">
        <button id="btnCloseDetailsModalBtn" class="btn btn-secondary">Fechar</button>
      </div>
    </div>
  </div>

  <!-- Modal 6: Confirmação Genérica Acessível -->
  <div id="modalConfirm" class="modal-overlay" role="dialog" aria-modal="true">
    <div class="modal-box" style="max-width: 440px;">
      <div class="modal-header">
        <h3 id="modalConfirmTitle">Confirmação</h3>
        <button class="modal-close" id="btnCloseConfirmModal">&times;</button>
      </div>
      <div class="modal-body">
        <p id="modalConfirmMessage" style="font-size: 0.875rem; color: var(--text-main); line-height: 1.5;">Mensagem de confirmação...</p>
      </div>
      <div class="modal-footer">
        <button id="btnCancelConfirm" class="btn btn-secondary">Cancelar</button>
        <button id="btnAcceptConfirm" class="btn btn-danger">Confirmar</button>
      </div>
    </div>
  </div>

  <!-- Modal 7: Dependência Operacional (Bloqueio de Exclusão) -->
  <div id="modalDependency" class="modal-overlay" role="dialog" aria-modal="true">
    <div class="modal-box">
      <div class="modal-header" style="background: rgba(217, 119, 6, 0.15); color: #fbbf24;">
        <h3>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
          <span id="modalDependencyTitle">Registro com Dependências</span>
        </h3>
        <button class="modal-close" id="btnCloseDependencyModal">&times;</button>
      </div>
      <div class="modal-body">
        <p id="modalDependencyDesc" style="font-size: 0.875rem; margin-bottom: 0.75rem;">
          Este registro não pode ser excluído fisicamente pois existem registros vinculados a ele na base de dados:
        </p>
        <ul id="modalDependencyList" style="margin-left: 1.25rem; font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 1rem;"></ul>
        <div class="notice-banner warning">
          Recomendação: Utilize a <strong>Inativação</strong> do registro. Registros inativos não aparecem para seleção em novos eventos, mas preservam o histórico de eventos passados e a integridade do sistema.
        </div>
      </div>
      <div class="modal-footer">
        <button id="btnCloseDependencyModalBtn" class="btn btn-secondary">Entendido</button>
        <button id="btnDependencyInactivate" class="btn btn-warning">Inativar Registro</button>
      </div>
    </div>
  </div>

  <!-- Modal 8: Resumo da Importação de Backup -->
  <div id="modalImportSummary" class="modal-overlay" role="dialog" aria-modal="true">
    <div class="modal-box">
      <div class="modal-header">
        <h3>Importação de Backup JSON</h3>
        <button class="modal-close" id="btnCloseImportSummaryModal">&times;</button>
      </div>
      <div class="modal-body">
        <p style="font-size: 0.875rem; margin-bottom: 0.75rem;">
          Arquivo validado com sucesso! Resumo dos dados encontrados no arquivo de backup:
        </p>
        <div id="importSummaryCounts" style="background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 6px; padding: 0.75rem; font-size: 0.825rem; margin-bottom: 1rem;"></div>
        
        <div class="form-group" style="margin-bottom: 1rem;">
          <label style="font-weight: 700;">Modo de Importação:</label>
          <div style="display: flex; flex-direction: column; gap: 0.5rem; margin-top: 0.35rem;">
            <label class="form-checkbox">
              <input type="radio" name="importMode" value="merge" checked>
              <span><strong>Mesclar Dados:</strong> Não duplica registros, atualiza pelo ID e versão, preserva dados existentes.</span>
            </label>
            <label class="form-checkbox">
              <input type="radio" name="importMode" value="replace">
              <span><strong>Substituir Tudo:</strong> Apaga os dados atuais e carrega o backup. Um backup preventivo será baixado automaticamente antes da substituição.</span>
            </label>
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button id="btnCancelImportSummary" class="btn btn-secondary">Cancelar</button>
        <button id="btnConfirmImportSummary" class="btn btn-primary">Executar Importação</button>
      </div>
    </div>
  </div>

  <!-- Modal 9: Folha de Ações Contextuais do Evento [⋯] (Section 8.3) -->
  <div id="modalEventActionSheet" class="modal-overlay" role="dialog" aria-modal="true">
    <div class="modal-box" style="max-width: 420px;">
      <div class="modal-header">
        <h3 id="actionSheetEventTitle" style="font-size: 0.95rem;">Ações da Previsão</h3>
        <button class="modal-close" id="btnCloseActionSheet">&times;</button>
      </div>
      <div class="modal-body" style="padding: 0.85rem;">
        <div id="actionSheetEventSubtitle" style="font-size: 0.78rem; color: #38bdf8; font-weight: 700; margin-bottom: 0.75rem;">--</div>
        <div class="action-sheet-list" id="actionSheetButtonsContainer">
          <!-- Dynamically populated contextual actions -->
        </div>
      </div>
    </div>
  </div>

  <!-- Modal 10: Status da Aplicação (Section 4.3) -->
  <div id="modalAppStatus" class="modal-overlay" role="dialog" aria-modal="true">
    <div class="modal-box" style="max-width: 460px;">
      <div class="modal-header">
        <h3>Status Operacional da Aplicação</h3>
        <button class="modal-close" id="btnCloseAppStatusModal">&times;</button>
      </div>
      <div class="modal-body">
        <div style="display: flex; flex-direction: column; gap: 0.65rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.65rem 0.85rem; background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 8px;">
            <div>
              <div style="font-size: 0.75rem; color: var(--text-muted);">Áudio Local (Web Audio API)</div>
              <div id="statusModalAudio" style="font-weight: 700; font-size: 0.9rem;">Aguardando interação</div>
            </div>
            <button type="button" id="btnStatusModalTestAudio" class="btn btn-outline btn-sm">Ativar / Testar Som</button>
          </div>

          <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.65rem 0.85rem; background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 8px;">
            <div>
              <div style="font-size: 0.75rem; color: var(--text-muted);">Notificações do Navegador</div>
              <div id="statusModalNotif" style="font-weight: 700; font-size: 0.9rem;">Não solicitado</div>
            </div>
            <button type="button" id="btnStatusModalTestNotif" class="btn btn-warning btn-sm">Permitir / Testar</button>
          </div>

          <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.65rem 0.85rem; background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 8px;">
            <div>
              <div style="font-size: 0.75rem; color: var(--text-muted);">Armazenamento Local (IndexedDB)</div>
              <div id="statusModalDB" style="font-weight: 700; font-size: 0.9rem; color: #4ade80;">Ativo (Persistência Local)</div>
            </div>
            <span class="status-badge normal">Online</span>
          </div>

          <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.65rem 0.85rem; background: var(--bg-app); border: 1px solid var(--border-color); border-radius: 8px;">
            <div>
              <div style="font-size: 0.75rem; color: var(--text-muted);">Último Backup Exportado</div>
              <div id="statusModalLastBackup" style="font-weight: 700; font-size: 0.9rem;">Nunca realizado</div>
            </div>
            <button type="button" class="btn btn-outline btn-sm" onclick="document.getElementById('modalAppStatus').classList.remove('active'); App.UI.navigateTo('viewBackup');">Backup</button>
          </div>
        </div>

        <div class="notice-banner" style="margin-top: 1rem; margin-bottom: 0; font-size: 0.78rem;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink: 0; color: #38bdf8;"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
          <span>Mantenha esta aba aberta para garantir o disparo contínuo dos alarmes locais no celular, tablet ou estação de trabalho.</span>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" id="btnCloseAppStatusFooter" class="btn btn-secondary">Fechar</button>
      </div>
    </div>
  </div>

  <!-- Toast Notification Container -->
  <div id="toastContainer" class="toast-container" aria-live="polite"></div>
"""
