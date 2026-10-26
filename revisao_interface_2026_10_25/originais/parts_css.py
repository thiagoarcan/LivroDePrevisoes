# -*- coding: utf-8 -*-
CSS_CONTENT = """
    :root {
      --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      --transition: 0.2s ease-in-out;
      
      /* Dark Theme (Default Operational Room) */
      --bg-app: #0b1120;
      --bg-surface: #1e293b;
      --bg-surface-hover: #283548;
      --bg-surface-active: #334155;
      --bg-elevated: #1e293b;
      --bg-surface-elevated: #1e293b;
      --border-color: #334155;
      --border-color-focus: #38bdf8;
      
      --text-main: #f8fafc;
      --text-secondary: #94a3b8;
      --text-muted: #64748b;
      
      --color-primary: #0284c7;
      --color-primary-hover: #0369a1;
      --color-success: #16a34a;
      --color-success-hover: #15803d;
      --color-warning: #d97706;
      --color-danger: #dc2626;
      --color-danger-hover: #b91c1c;
      --color-info: #2563eb;
      
      /* Operational Status Colors */
      --status-overdue-bg: #450a0a;
      --status-overdue-border: #991b1b;
      --status-overdue-text: #fecaca;
      
      --status-critico-bg: #7f1d1d;
      --status-critico-border: #dc2626;
      --status-critico-text: #fee2e2;
      
      --status-urgente-bg: #7c2d12;
      --status-urgente-border: #ea580c;
      --status-urgente-text: #ffedd5;
      
      --status-atencao-bg: #713f12;
      --status-atencao-border: #ca8a04;
      --status-atencao-text: #fef08a;
      
      --status-monitor-bg: #1e3a8a;
      --status-monitor-border: #2563eb;
      --status-monitor-text: #dbeafe;
      
      --status-normal-bg: #14532d;
      --status-normal-border: #16a34a;
      --status-normal-text: #dcfce7;
      
      --status-concluido-bg: #064e3b;
      --status-concluido-border: #059669;
      --status-concluido-text: #d1fae5;

      --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
      --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -2px rgba(0, 0, 0, 0.3);
      --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -4px rgba(0, 0, 0, 0.4);
    }

    body.theme-light {
      --bg-app: #f1f5f9;
      --bg-surface: #ffffff;
      --bg-surface-hover: #f8fafc;
      --bg-surface-active: #e2e8f0;
      --bg-elevated: #ffffff;
      --bg-surface-elevated: #ffffff;
      --border-color: #cbd5e1;
      --border-color-focus: #0284c7;
      
      --text-main: #0f172a;
      --text-secondary: #475569;
      --text-muted: #94a3b8;
      
      --color-primary: #0284c7;
      --color-primary-hover: #0369a1;
      
      --status-overdue-bg: #fee2e2;
      --status-overdue-border: #b91c1c;
      --status-overdue-text: #991b1b;
      
      --status-critico-bg: #fef2f2;
      --status-critico-border: #dc2626;
      --status-critico-text: #991b1b;
      
      --status-urgente-bg: #fff7ed;
      --status-urgente-border: #ea580c;
      --status-urgente-text: #c2410c;
      
      --status-atencao-bg: #fefce8;
      --status-atencao-border: #ca8a04;
      --status-atencao-text: #854d0e;
      
      --status-monitor-bg: #eff6ff;
      --status-monitor-border: #2563eb;
      --status-monitor-text: #1d4ed8;
      
      --status-normal-bg: #f0fdf4;
      --status-normal-border: #16a34a;
      --status-normal-text: #15803d;
      
      --status-concluido-bg: #ecfdf5;
      --status-concluido-border: #059669;
      --status-concluido-text: #065f46;

      --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
      --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
      --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
    }

    /* Tema 3 - Industrial (Alto Contraste para uso em campo / alta luminosidade) */
    body.theme-industrial {
      --bg-app: #000000;
      --bg-surface: #0a0a0a;
      --bg-surface-hover: #171717;
      --bg-surface-active: #262626;
      --bg-elevated: #0f0f0f;
      --bg-surface-elevated: #0f0f0f;
      --border-color: #525252;
      --border-color-focus: #facc15;
      
      --text-main: #ffffff;
      --text-secondary: #e5e5e5;
      --text-muted: #a3a3a3;
      
      --color-primary: #eab308;
      --color-primary-hover: #ca8a04;
      --color-success: #16a34a;
      --color-warning: #f59e0b;
      --color-danger: #ef4444;
      
      --status-overdue-bg: #7f1d1d;
      --status-overdue-border: #ff4d4d;
      --status-overdue-text: #ffffff;
      
      --status-critico-bg: #991b1b;
      --status-critico-border: #ff6666;
      --status-critico-text: #ffffff;
      
      --status-urgente-bg: #9a3412;
      --status-urgente-border: #fb923c;
      --status-urgente-text: #ffffff;
      
      --status-atencao-bg: #854d0e;
      --status-atencao-border: #facc15;
      --status-atencao-text: #ffffff;
      
      --status-monitor-bg: #1e40af;
      --status-monitor-border: #60a5fa;
      --status-monitor-text: #ffffff;
      
      --status-normal-bg: #166534;
      --status-normal-border: #4ade80;
      --status-normal-text: #ffffff;
    }
    body.theme-industrial .btn-primary {
      color: #000000;
      font-weight: 800;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
      font-family: var(--font-sans);
      background-color: var(--bg-app);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
      touch-action: manipulation;
      overflow-x: hidden;
    }

    /* Keyframes */
    @keyframes pulse-danger {
      0% { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.8); }
      70% { box-shadow: 0 0 0 10px rgba(220, 38, 38, 0); }
      100% { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0); }
    }
    @keyframes pulse-badge {
      0% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.65; transform: scale(1.05); }
      100% { opacity: 1; transform: scale(1); }
    }
    .pulsing-card { animation: pulse-danger 1.5s infinite; }
    .pulsing-badge { animation: pulse-badge 1s infinite; }

    @media (prefers-reduced-motion: reduce) {
      .pulsing-card, .pulsing-badge {
        animation: none !important;
      }
      .pulsing-card {
        outline: 2px solid #ef4444;
      }
      .pulsing-badge {
        border-width: 2px;
        text-decoration: underline;
      }
    }

    /* Header Bar */
    .app-header {
      background-color: var(--bg-surface);
      border-bottom: 1px solid var(--border-color);
      padding: 0.55rem 1rem;
      position: sticky;
      top: 0;
      z-index: 100;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.75rem;
      box-shadow: var(--shadow-sm);
    }

    .header-left {
      display: flex;
      align-items: center;
      gap: 0.6rem;
    }

    .btn-hamburger {
      display: none;
      background: none;
      border: 1px solid var(--border-color);
      border-radius: 6px;
      color: var(--text-main);
      padding: 0.4rem;
      cursor: pointer;
      align-items: center;
      justify-content: center;
    }

    .header-brand {
      display: flex;
      align-items: center;
      gap: 0.6rem;
    }
    .header-brand svg { color: var(--color-primary); flex-shrink: 0; }
    .header-brand h1 {
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text-main);
      letter-spacing: -0.01em;
      line-height: 1.2;
    }
    .header-brand .subtitle {
      font-size: 0.7rem;
      color: var(--text-secondary);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    /* Active Console Selector in Header */
    .header-console-box {
      display: flex;
      align-items: center;
      gap: 0.4rem;
      background: rgba(2, 132, 199, 0.12);
      border: 1.5px solid #0284c7;
      border-radius: 8px;
      padding: 0.25rem 0.6rem;
    }
    .header-console-box label {
      font-size: 0.75rem;
      font-weight: 800;
      color: #38bdf8;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      white-space: nowrap;
      margin: 0;
    }
    .header-console-select {
      background: transparent;
      border: none;
      color: var(--text-main);
      font-weight: 800;
      font-size: 0.95rem;
      cursor: pointer;
      padding: 0.1rem 0.2rem;
      outline: none;
    }
    .header-console-select option {
      background: var(--bg-surface);
      color: var(--text-main);
    }

    .header-status-bar {
      display: flex;
      align-items: center;
      gap: 0.45rem;
      flex-wrap: wrap;
    }

    .status-pill {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      padding: 0.22rem 0.55rem;
      border-radius: 9999px;
      font-size: 0.72rem;
      font-weight: 600;
      border: 1px solid var(--border-color);
      background: var(--bg-surface-active);
      color: var(--text-secondary);
      cursor: pointer;
      text-decoration: none;
      transition: all var(--transition);
      user-select: none;
    }
    .status-pill:hover { filter: brightness(1.15); }
    .status-pill.ok {
      border-color: rgba(22, 163, 74, 0.4);
      color: #4ade80;
      background: rgba(22, 163, 74, 0.1);
    }
    .status-pill.warning {
      border-color: rgba(217, 119, 6, 0.4);
      color: #fbbf24;
      background: rgba(217, 119, 6, 0.1);
    }
    .status-pill.danger {
      border-color: rgba(220, 38, 38, 0.4);
      color: #f87171;
      background: rgba(220, 38, 38, 0.1);
    }

    .clock-display {
      font-family: monospace;
      font-size: 0.92rem;
      font-weight: 700;
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.35);
      padding: 0.22rem 0.55rem;
      border-radius: 6px;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      white-space: nowrap;
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 0.45rem;
    }

    /* Navigation Bar */
    .app-nav {
      background-color: var(--bg-surface);
      border-bottom: 1px solid var(--border-color);
      padding: 0 1rem;
      display: flex;
      overflow-x: auto;
      gap: 0.25rem;
      scrollbar-width: thin;
    }
    .nav-item {
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      padding: 0.7rem 0.85rem;
      color: var(--text-secondary);
      font-size: 0.85rem;
      font-weight: 600;
      border-bottom: 3px solid transparent;
      cursor: pointer;
      white-space: nowrap;
      background: none;
      border-top: none;
      border-left: none;
      border-right: none;
      transition: all var(--transition);
      min-height: 42px;
    }
    .nav-item:hover {
      color: var(--text-main);
      background-color: var(--bg-surface-hover);
    }
    .nav-item.active {
      color: #38bdf8;
      border-bottom-color: #38bdf8;
      background-color: var(--bg-surface-hover);
    }
    .nav-item .badge-count {
      background-color: var(--bg-surface-active);
      color: var(--text-main);
      padding: 0.1rem 0.45rem;
      border-radius: 9999px;
      font-size: 0.7rem;
      font-weight: 700;
    }
    .nav-item.active .badge-count {
      background-color: #0284c7;
      color: #ffffff;
    }

    /* Mobile / Tablet Drawer Menu */
    .mobile-drawer-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(2px);
      z-index: 1050;
      display: none;
    }
    .mobile-drawer-overlay.active,
    .mobile-drawer-overlay.open { display: block; }

    .mobile-drawer {
      position: fixed;
      top: 0;
      left: 0;
      bottom: 0;
      width: 280px;
      max-width: 85vw;
      background: var(--bg-elevated);
      border-right: 1px solid var(--border-color);
      z-index: 1100;
      transform: translateX(-100%);
      transition: transform 0.25s ease-out;
      display: flex;
      flex-direction: column;
      box-shadow: var(--shadow-lg);
    }
    .mobile-drawer.active,
    .mobile-drawer.open { transform: translateX(0); }

    .drawer-header {
      padding: 1rem;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .drawer-nav-items {
      flex: 1;
      overflow-y: auto;
      padding: 0.5rem;
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
    }
    .drawer-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.75rem 0.9rem;
      border-radius: 6px;
      color: var(--text-secondary);
      font-weight: 600;
      font-size: 0.9rem;
      background: transparent;
      border: none;
      cursor: pointer;
      text-align: left;
      min-height: 48px;
    }
    .drawer-item:hover, .drawer-item.active {
      color: #38bdf8;
      background: var(--bg-surface-active);
    }

    /* Main Container */
    .app-main {
      flex: 1;
      padding: 1rem;
      max-width: 1650px;
      margin: 0 auto;
      width: 100%;
    }
    .view-section { display: none; }
    .view-section.active { display: block; }

    /* Buttons */
    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.4rem;
      padding: 0.5rem 0.9rem;
      font-size: 0.85rem;
      font-weight: 600;
      border-radius: 6px;
      border: 1px solid transparent;
      cursor: pointer;
      transition: all var(--transition);
      text-decoration: none;
      user-select: none;
      min-height: 40px;
    }
    .btn:focus-visible { outline: 2px solid var(--border-color-focus); outline-offset: 2px; }
    .btn:disabled { opacity: 0.5; cursor: not-allowed; }
    
    .btn-primary { background-color: var(--color-primary); color: #ffffff; }
    .btn-primary:hover:not(:disabled) { background-color: var(--color-primary-hover); }
    
    .btn-success { background-color: var(--color-success); color: #ffffff; }
    .btn-success:hover:not(:disabled) { background-color: var(--color-success-hover); }
    
    .btn-warning { background-color: var(--color-warning); color: #ffffff; }
    .btn-warning:hover:not(:disabled) { background-color: #b45309; }
    
    .btn-danger { background-color: var(--color-danger); color: #ffffff; }
    .btn-danger:hover:not(:disabled) { background-color: var(--color-danger-hover); }
    
    .btn-secondary {
      background-color: var(--bg-surface-active);
      color: var(--text-main);
      border-color: var(--border-color);
    }
    .btn-secondary:hover:not(:disabled) {
      background-color: var(--bg-surface-hover);
      border-color: var(--text-muted);
    }
    
    .btn-outline {
      background: transparent;
      border-color: var(--border-color);
      color: var(--text-secondary);
    }
    .btn-outline:hover:not(:disabled) {
      color: var(--text-main);
      background: var(--bg-surface-hover);
      border-color: var(--text-muted);
    }

    .btn-sm { padding: 0.28rem 0.55rem; font-size: 0.775rem; min-height: 32px; }
    .btn-icon { padding: 0.45rem; border-radius: 6px; min-width: 40px; }

    /* Floating Action Button (FAB) on mobile - kept hidden when bottom nav is used */
    .fab-btn {
      position: fixed;
      bottom: 1.5rem;
      right: 1.5rem;
      width: 56px;
      height: 56px;
      border-radius: 50%;
      background: #0284c7;
      color: #ffffff;
      box-shadow: var(--shadow-lg);
      border: none;
      display: none !important;
      align-items: center;
      justify-content: center;
      z-index: 900;
      cursor: pointer;
      transition: transform 0.2s;
    }
    .fab-btn:hover { transform: scale(1.08); background: #0369a1; }

    /* Cards */
    .card {
      background-color: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 1.15rem;
      box-shadow: var(--shadow-sm);
      margin-bottom: 1.15rem;
    }
    .card-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 0.85rem;
      padding-bottom: 0.65rem;
      border-bottom: 1px solid var(--border-color);
      flex-wrap: wrap;
      gap: 0.5rem;
    }
    .card-title {
      font-size: 1.05rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .card-subtitle { font-size: 0.8rem; color: var(--text-secondary); margin-top: 0.15rem; }

    /* Forms */
    .form-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 0.9rem;
    }
    .form-group { display: flex; flex-direction: column; gap: 0.35rem; }
    .form-group.span-full { grid-column: 1 / -1; }
    .form-group.span-2 { grid-column: span 2; }

    label {
      font-size: 0.825rem;
      font-weight: 600;
      color: var(--text-secondary);
      display: flex;
      align-items: center;
      gap: 0.25rem;
    }
    label .required { color: #ef4444; }

    input[type="text"],
    input[type="number"],
    input[type="date"],
    input[type="time"],
    select,
    textarea {
      background-color: var(--bg-app);
      border: 1px solid var(--border-color);
      border-radius: 6px;
      padding: 0.55rem 0.75rem;
      color: var(--text-main);
      font-family: inherit;
      font-size: 0.9rem;
      transition: border-color var(--transition);
      width: 100%;
      min-height: 42px;
    }
    textarea { min-height: 70px; }
    input:focus, select:focus, textarea:focus {
      outline: none;
      border-color: var(--border-color-focus);
      box-shadow: 0 0 0 1px var(--border-color-focus);
    }
    input:disabled, select:disabled, textarea:disabled {
      background-color: var(--bg-surface-active);
      color: var(--text-muted);
      cursor: not-allowed;
    }
    .form-checkbox {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      cursor: pointer;
      user-select: none;
      font-size: 0.85rem;
      color: var(--text-main);
      min-height: 38px;
    }
    .form-checkbox input[type="checkbox"] {
      width: 1.25rem;
      height: 1.25rem;
      accent-color: var(--color-primary);
      cursor: pointer;
    }
    .form-help { font-size: 0.75rem; color: var(--text-muted); }

    /* Status Badges (normalized and raw range_* keys) */
    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      padding: 0.22rem 0.55rem;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 700;
      border: 1px solid transparent;
      white-space: nowrap;
    }
    .status-badge.atrasado {
      background-color: var(--status-overdue-bg);
      border-color: var(--status-overdue-border);
      color: var(--status-overdue-text);
    }
    .status-badge.critico,
    .status-badge.range_critico {
      background-color: var(--status-critico-bg);
      border-color: var(--status-critico-border);
      color: var(--status-critico-text);
    }
    .status-badge.urgente,
    .status-badge.range_urgente {
      background-color: var(--status-urgente-bg);
      border-color: var(--status-urgente-border);
      color: var(--status-urgente-text);
    }
    .status-badge.atencao,
    .status-badge.range_atencao {
      background-color: var(--status-atencao-bg);
      border-color: var(--status-atencao-border);
      color: var(--status-atencao-text);
    }
    .status-badge.monitoramento,
    .status-badge.range_monitor {
      background-color: var(--status-monitor-bg);
      border-color: var(--status-monitor-border);
      color: var(--status-monitor-text);
    }
    .status-badge.normal,
    .status-badge.range_normal {
      background-color: var(--status-normal-bg);
      border-color: var(--status-normal-border);
      color: var(--status-normal-text);
    }
    .status-badge.concluido {
      background-color: var(--status-concluido-bg);
      border-color: var(--status-concluido-border);
      color: var(--status-concluido-text);
    }
    .status-badge.inativo {
      background-color: #334155;
      border-color: #475569;
      color: #94a3b8;
    }

    /* Dashboard Metrics */
    .dashboard-metrics {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 0.85rem;
      margin-bottom: 1.15rem;
    }
    .metric-card {
      background-color: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 0.85rem;
      display: flex;
      align-items: center;
      gap: 0.8rem;
      cursor: pointer;
      transition: transform var(--transition), border-color var(--transition);
      min-height: 72px;
    }
    .metric-card:hover {
      transform: translateY(-2px);
      border-color: var(--text-muted);
    }
    .metric-icon {
      width: 40px;
      height: 40px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
    .metric-data .metric-value {
      font-size: 1.5rem;
      font-weight: 800;
      line-height: 1.1;
    }
    .metric-data .metric-label {
      font-size: 0.72rem;
      color: var(--text-secondary);
      font-weight: 600;
    }

    /* Spotlight Card */
    .spotlight-card {
      background: linear-gradient(135deg, rgba(2, 132, 199, 0.15), rgba(15, 23, 42, 0.5));
      border: 2px solid #0284c7;
      border-radius: 10px;
      padding: 1.15rem;
      margin-bottom: 1.15rem;
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
    }
    .spotlight-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 0.5rem;
    }
    .spotlight-badge {
      background: #0284c7;
      color: #ffffff;
      padding: 0.2rem 0.6rem;
      border-radius: 4px;
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }
    .spotlight-body {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 1rem;
      align-items: center;
    }
    .spotlight-path {
      font-size: 0.85rem;
      font-weight: 700;
      color: #38bdf8;
      display: flex;
      align-items: center;
      gap: 0.4rem;
      flex-wrap: wrap;
    }
    .spotlight-desc {
      font-size: 1.15rem;
      font-weight: 700;
      margin-top: 0.25rem;
      color: var(--text-main);
    }
    .spotlight-timer {
      text-align: right;
      display: flex;
      flex-direction: column;
      align-items: flex-end;
    }
    .spotlight-timer .time-left {
      font-size: 1.35rem;
      font-weight: 800;
      font-family: monospace;
    }
    .spotlight-timer .sched-time {
      font-size: 0.8rem;
      color: var(--text-secondary);
    }

    /* Events Toolbar & Filter Drawer */
    .events-toolbar {
      background-color: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 0.75rem 1rem;
      margin-bottom: 1rem;
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
    }
    .toolbar-primary {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.75rem;
      flex-wrap: wrap;
    }
    .search-box {
      position: relative;
      flex: 1;
      min-width: 220px;
    }
    .search-box input { padding-left: 2.2rem; }
    .search-box svg {
      position: absolute;
      left: 0.75rem;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
    }
    .toolbar-filters {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
      gap: 0.6rem;
      padding-top: 0.75rem;
      border-top: 1px solid var(--border-color);
    }

    .events-container-cards {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
      gap: 0.9rem;
    }
    .event-card {
      background-color: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-left-width: 5px;
      border-radius: 8px;
      padding: 1rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 0.75rem;
      transition: transform var(--transition), box-shadow var(--transition);
    }
    .event-card:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
    }
    .event-card-header {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 0.5rem;
    }
    .event-hierarchy {
      font-size: 0.8rem;
      font-weight: 700;
      color: #38bdf8;
      display: flex;
      align-items: center;
      gap: 0.3rem;
      flex-wrap: wrap;
    }
    .event-tag-badge {
      background: rgba(56, 189, 248, 0.15);
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.4);
      padding: 0.1rem 0.4rem;
      border-radius: 4px;
      font-size: 0.75rem;
      font-weight: 700;
    }
    .event-card-body .event-desc {
      font-size: 0.95rem;
      font-weight: 600;
      color: var(--text-main);
      margin-bottom: 0.35rem;
    }
    .event-card-body .event-notes {
      font-size: 0.8rem;
      color: var(--text-secondary);
      font-style: italic;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    .event-card-meta {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-top: 0.5rem;
      border-top: 1px dashed var(--border-color);
      font-size: 0.8rem;
      color: var(--text-secondary);
    }
    .event-countdown { font-weight: 700; font-family: monospace; font-size: 0.875rem; }
    .event-card-actions {
      display: flex;
      align-items: center;
      justify-content: flex-end;
      gap: 0.35rem;
      flex-wrap: wrap;
    }

    /* Tables */
    .table-responsive {
      width: 100%;
      overflow-x: auto;
      border: 1px solid var(--border-color);
      border-radius: 8px;
      background-color: var(--bg-surface);
    }
    .data-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.85rem;
      text-align: left;
    }
    .data-table th, .data-table td {
      padding: 0.65rem 0.85rem;
      border-bottom: 1px solid var(--border-color);
    }
    .data-table th {
      background-color: var(--bg-surface-active);
      color: var(--text-secondary);
      font-weight: 700;
      text-transform: uppercase;
      font-size: 0.72rem;
      letter-spacing: 0.05em;
      position: sticky;
      top: 0;
      z-index: 10;
    }
    .data-table tbody tr { transition: background-color var(--transition); }
    .data-table tbody tr:hover { background-color: var(--bg-surface-hover); }

    /* ========================================================
       UNIFIED CADASTROS HUB (NO SEPARATE TABS, NO DEAD SPACE)
       ======================================================== */
    .cadastros-unified-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
      gap: 1rem;
      align-items: start;
    }
    .cadastro-hub-card {
      background-color: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 1rem;
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
    }
    .cadastro-hub-card .hub-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--border-color);
      padding-bottom: 0.5rem;
    }
    .cadastro-hub-card .hub-title {
      font-size: 0.95rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }
    .hub-list-container {
      max-height: 280px;
      overflow-y: auto;
      border: 1px solid var(--border-color);
      border-radius: 6px;
      background: var(--bg-app);
    }

    /* Tablet Stylus Canvas Drawing Pad */
    .stylus-canvas-container {
      border: 1px solid var(--border-color);
      border-radius: 8px;
      background: var(--bg-app);
      padding: 0.75rem;
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      margin-top: 0.75rem;
    }
    .canvas-toolbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 0.5rem;
    }
    .stylus-canvas {
      width: 100%;
      height: 180px;
      background: #ffffff;
      border-radius: 6px;
      cursor: crosshair;
      touch-action: none; /* Prevents scroll when drawing with stylus or touch */
    }

    /* Modals */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background-color: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(2px);
      z-index: 1000;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 1rem;
      overflow-y: auto;
    }
    .modal-overlay.active { display: flex; }
    .modal-box {
      background-color: var(--bg-elevated);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      width: 100%;
      max-width: 600px;
      box-shadow: var(--shadow-lg);
      display: flex;
      flex-direction: column;
      animation: modal-appear 0.2s ease-out;
      max-height: 90vh;
    }
    .modal-box.modal-lg { max-width: 880px; }
    @keyframes modal-appear {
      from { opacity: 0; transform: scale(0.96); }
      to { opacity: 1; transform: scale(1); }
    }
    .modal-header {
      padding: 0.9rem 1.15rem;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .modal-header h3 {
      font-size: 1.05rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .modal-close {
      background: none;
      border: none;
      color: var(--text-muted);
      font-size: 1.5rem;
      line-height: 1;
      cursor: pointer;
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      min-height: 36px;
      min-width: 36px;
    }
    .modal-close:hover { color: var(--text-main); background-color: var(--bg-surface-active); }
    .modal-body { padding: 1.15rem; overflow-y: auto; flex: 1; }
    .modal-footer {
      padding: 0.75rem 1.15rem;
      border-top: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: flex-end;
      gap: 0.5rem;
      background-color: var(--bg-surface);
      border-bottom-left-radius: 10px;
      border-bottom-right-radius: 10px;
      flex-wrap: wrap;
    }

    /* Alarm Trigger Modal */
    .alarm-modal-box { border: 2px solid #ef4444; box-shadow: 0 0 25px rgba(239, 68, 68, 0.45); }
    .alarm-modal-header { background-color: #7f1d1d; color: #ffffff; }

    /* Toast Notification Container */
    .toast-container {
      position: fixed;
      bottom: 1.5rem;
      right: 1.5rem;
      z-index: 2000;
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      max-width: 380px;
      pointer-events: none;
    }
    .toast {
      pointer-events: auto;
      background-color: var(--bg-elevated);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 0.75rem 1rem;
      box-shadow: var(--shadow-lg);
      display: flex;
      align-items: flex-start;
      gap: 0.75rem;
      font-size: 0.85rem;
      animation: toast-in 0.25s ease-out;
    }
    @keyframes toast-in {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .toast.toast-success { border-left: 4px solid var(--color-success); }
    .toast.toast-danger { border-left: 4px solid var(--color-danger); }
    .toast.toast-warning { border-left: 4px solid var(--color-warning); }
    .toast.toast-info { border-left: 4px solid var(--color-info); }

    /* Timeline */
    .timeline { position: relative; padding-left: 1.5rem; margin-top: 0.5rem; }
    .timeline::before {
      content: '';
      position: absolute;
      left: 6px;
      top: 4px;
      bottom: 4px;
      width: 2px;
      background-color: var(--border-color);
    }
    .timeline-item { position: relative; margin-bottom: 0.85rem; }
    .timeline-point {
      position: absolute;
      left: -1.5rem;
      top: 4px;
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background-color: #38bdf8;
      border: 2px solid var(--bg-surface);
    }
    .timeline-content {
      background-color: var(--bg-app);
      border: 1px solid var(--border-color);
      border-radius: 6px;
      padding: 0.6rem 0.8rem;
      font-size: 0.825rem;
    }
    .timeline-meta {
      display: flex;
      justify-content: space-between;
      color: var(--text-muted);
      font-size: 0.75rem;
      margin-bottom: 0.2rem;
    }
    .timeline-title { font-weight: 700; color: var(--text-main); }
    .timeline-desc { color: var(--text-secondary); margin-top: 0.2rem; }

    /* Color Preview Bar */
    .color-preview-bar {
      display: flex;
      height: 28px;
      border-radius: 6px;
      overflow: hidden;
      border: 1px solid var(--border-color);
      margin: 1rem 0;
    }
    .preview-segment {
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.72rem;
      font-weight: 700;
      color: #ffffff;
      text-shadow: 0 1px 2px rgba(0,0,0,0.8);
      white-space: nowrap;
      padding: 0 0.25rem;
    }

    /* Notice Banner */
    .notice-banner {
      background: rgba(2, 132, 199, 0.1);
      border: 1px solid rgba(2, 132, 199, 0.3);
      border-radius: 8px;
      padding: 0.85rem 1rem;
      margin-bottom: 1rem;
      display: flex;
      gap: 0.75rem;
      align-items: flex-start;
      font-size: 0.85rem;
      color: var(--text-secondary);
    }
    .notice-banner.warning {
      background: rgba(217, 119, 6, 0.1);
      border-color: rgba(217, 119, 6, 0.3);
      color: #fbbf24;
    }

    /* UO Multi-select Box in Pipeline Form */
    .uo-selection-box {
      border: 1px solid var(--border-color);
      border-radius: 6px;
      padding: 0.5rem;
      background: var(--bg-app);
      max-height: 160px;
      overflow-y: auto;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
      gap: 0.4rem;
    }

    /* =========================================================================
       UNIVERSAL RESPONSIVE ARCHITECTURE & MANUAL VIEW MODES
       Supports Auto breakpoints + manual overrides via body[data-layout-mode]
       ========================================================================= */

    /* Persistent Top Banners (Alarms, Backup Warning, Layout Usability Warning) */
    .persistent-banner {
      padding: 0.6rem 1rem;
      display: none;
      align-items: center;
      justify-content: space-between;
      gap: 0.75rem;
      flex-wrap: wrap;
      font-size: 0.85rem;
      font-weight: 600;
      border-bottom: 1px solid var(--border-color);
      z-index: 95;
    }
    .persistent-banner.active { display: flex; }
    .persistent-banner.alarm-banner {
      background: linear-gradient(90deg, #7f1d1d, #991b1b);
      color: #ffffff;
      border-bottom: 2px solid #ef4444;
      position: sticky;
      top: 52px;
      z-index: 98;
      box-shadow: var(--shadow-md);
    }
    .persistent-banner.backup-banner {
      background: rgba(217, 119, 6, 0.16);
      color: #fbbf24;
      border-bottom-color: rgba(217, 119, 6, 0.4);
    }
    .persistent-banner.layout-banner {
      background: rgba(2, 132, 199, 0.16);
      color: #38bdf8;
      border-bottom-color: rgba(2, 132, 199, 0.4);
    }

    /* Header Layout Selector & Alarm Bell */
    .header-viewmode-box {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      background: var(--bg-surface-active);
      border: 1px solid var(--border-color);
      border-radius: 6px;
      padding: 0.2rem 0.5rem;
      font-size: 0.75rem;
    }
    .header-viewmode-box label {
      font-size: 0.72rem;
      color: var(--text-secondary);
      margin: 0;
      white-space: nowrap;
    }
    .header-viewmode-select {
      background: transparent;
      border: none;
      color: var(--text-main);
      font-size: 0.78rem;
      font-weight: 700;
      padding: 0.1rem 0.25rem;
      min-height: 26px;
      width: auto;
      cursor: pointer;
    }
    .header-viewmode-select option {
      background: var(--bg-surface);
      color: var(--text-main);
    }

    .btn-header-bell {
      position: relative;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      background: var(--bg-surface-active);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      border-radius: 8px;
      min-width: 40px;
      min-height: 40px;
      padding: 0.4rem;
      cursor: pointer;
    }
    .btn-header-bell .bell-badge {
      position: absolute;
      top: -4px;
      right: -4px;
      background: #dc2626;
      color: #ffffff;
      font-size: 0.68rem;
      font-weight: 800;
      min-width: 18px;
      height: 18px;
      border-radius: 9999px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 0 4px;
      border: 2px solid var(--bg-surface);
    }

    /* Dashboard Highlight Grid (Spotlight + Active Alarms Side Panel for Tablet/Wide) */
    .dashboard-highlight-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 1rem;
      margin-bottom: 1.15rem;
    }
    .dashboard-highlight-grid .spotlight-card {
      margin-bottom: 0;
    }
    .tablet-alarms-panel {
      background-color: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 1rem;
      display: none;
      flex-direction: column;
      gap: 0.65rem;
    }
    .tablet-alarm-item {
      background: var(--bg-app);
      border: 1px solid var(--border-color);
      border-left: 4px solid #dc2626;
      border-radius: 6px;
      padding: 0.65rem 0.8rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.5rem;
      cursor: pointer;
      transition: background var(--transition);
    }
    .tablet-alarm-item:hover {
      background: var(--bg-surface-hover);
    }

    /* Dashboard Mobile Urgent Cards (Replaces wide table on mobile) */
    .dashboard-urgent-cards {
      display: none;
      flex-direction: column;
      gap: 0.75rem;
    }
    .urgent-mobile-card {
      background: var(--bg-app);
      border: 1px solid var(--border-color);
      border-left: 5px solid #dc2626;
      border-radius: 8px;
      padding: 0.85rem;
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }

    /* Pending Events Master-Detail Layout (Tablet, Widescreen, Ultrawide) */
    .pending-master-detail-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 1rem;
      align-items: start;
    }
    .pending-detail-pane {
      display: none;
      background-color: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 1.15rem;
      position: sticky;
      top: 72px;
      max-height: calc(100vh - 96px);
      overflow-y: auto;
      box-shadow: var(--shadow-md);
    }
    .event-card.selected-master-card {
      outline: 2px solid var(--border-color-focus);
      background-color: var(--bg-surface-hover);
    }
    .detail-pane-tabs {
      display: flex;
      gap: 0.35rem;
      border-bottom: 1px solid var(--border-color);
      margin: 0.75rem 0;
      padding-bottom: 0.4rem;
    }
    .detail-pane-tab {
      background: transparent;
      border: none;
      color: var(--text-secondary);
      font-weight: 700;
      font-size: 0.82rem;
      padding: 0.4rem 0.75rem;
      border-radius: 6px;
      cursor: pointer;
    }
    .detail-pane-tab.active {
      background: rgba(2, 132, 199, 0.18);
      color: #38bdf8;
    }

    /* Completed Events Expandable Cards (Mobile) */
    .completed-cards-container {
      display: none;
      flex-direction: column;
      gap: 0.75rem;
    }
    .completed-event-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-left: 4px solid var(--color-success);
      border-radius: 8px;
      padding: 0.9rem;
      display: flex;
      flex-direction: column;
      gap: 0.55rem;
    }
    .completed-card-extra {
      display: none;
      padding-top: 0.55rem;
      margin-top: 0.35rem;
      border-top: 1px dashed var(--border-color);
      font-size: 0.8rem;
      color: var(--text-secondary);
    }
    .completed-event-card.expanded .completed-card-extra {
      display: block;
    }

    /* Cadastros Category Selector (Mobile List & Tablet 2-Region) */
    .cadastros-category-bar {
      display: none;
      gap: 0.5rem;
      margin-bottom: 1rem;
      flex-wrap: wrap;
    }
    .cad-cat-btn {
      flex: 1;
      min-width: 140px;
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 0.75rem 1rem;
      color: var(--text-main);
      font-weight: 700;
      font-size: 0.88rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.5rem;
      cursor: pointer;
      min-height: 48px;
      transition: all var(--transition);
    }
    .cad-cat-btn.active {
      border-color: #0284c7;
      background: rgba(2, 132, 199, 0.15);
      color: #38bdf8;
    }
    .cad-cat-btn .cat-count {
      background: var(--bg-surface-active);
      color: var(--text-secondary);
      padding: 0.15rem 0.55rem;
      border-radius: 9999px;
      font-size: 0.75rem;
    }
    .cad-cat-btn.active .cat-count {
      background: #0284c7;
      color: #ffffff;
    }

    /* Color Ranges Cards (Mobile) & Chain Preview */
    .color-chain-preview {
      background: var(--bg-app);
      border: 1px dashed var(--border-color);
      border-radius: 6px;
      padding: 0.6rem 0.85rem;
      font-family: monospace;
      font-size: 0.85rem;
      font-weight: 700;
      color: #38bdf8;
      margin: 0.65rem 0;
      overflow-x: auto;
      white-space: nowrap;
    }
    .color-range-cards {
      display: none;
      flex-direction: column;
      gap: 0.75rem;
      margin-top: 0.85rem;
    }
    .color-range-card {
      background: var(--bg-app);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 0.85rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.75rem;
    }

    /* Fullscreen Stylus Lousa Mode */
    .stylus-canvas-container.fullscreen-lousa {
      position: fixed;
      inset: 0;
      z-index: 1500;
      margin: 0;
      border-radius: 0;
      padding: 1rem;
      background: var(--bg-surface);
      display: flex !important;
      flex-direction: column;
    }
    .stylus-canvas-container.fullscreen-lousa .stylus-canvas {
      flex: 1;
      height: auto !important;
    }

    /* Mobile Bottom Navigation Bar (Fixed, Safe-Area aware) */
    .mobile-bottom-nav {
      position: fixed;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: var(--bg-surface);
      border-top: 1px solid var(--border-color);
      padding: 0.35rem 0.5rem calc(0.35rem + env(safe-area-inset-bottom, 0px));
      display: none;
      align-items: center;
      justify-content: space-around;
      z-index: 950;
      box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.35);
    }
    .bottom-nav-btn {
      flex: 1;
      background: none;
      border: none;
      color: var(--text-secondary);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 0.2rem;
      font-size: 0.7rem;
      font-weight: 700;
      padding: 0.35rem 0.25rem;
      min-height: 48px;
      cursor: pointer;
      position: relative;
    }
    .bottom-nav-btn.active {
      color: #38bdf8;
    }
    .bottom-nav-btn .bottom-badge {
      position: absolute;
      top: 2px;
      right: calc(50% - 22px);
      background: #dc2626;
      color: #ffffff;
      font-size: 0.65rem;
      font-weight: 800;
      padding: 0 5px;
      border-radius: 9999px;
      min-width: 16px;
      height: 16px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
    }
    .mobile-fab {
      width: 52px;
      height: 52px;
      border-radius: 50%;
      background: var(--color-primary);
      color: #ffffff;
      border: 3px solid var(--bg-surface);
      box-shadow: var(--shadow-md);
      display: inline-flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transform: translateY(-10px);
      flex-shrink: 0;
    }
    body.theme-industrial .mobile-fab {
      color: #000000;
    }

    /* Quick Snooze Active Selection State (Not color-only, Section 7.2) */
    .btn-quick-snooze.selected-snooze {
      background-color: var(--color-primary);
      color: #ffffff;
      border-color: var(--border-color-focus);
      font-weight: 800;
      box-shadow: 0 0 0 2px var(--border-color-focus);
    }

    /* Action Sheet List Buttons (Mobile/Tablet Contextual Menu) */
    .action-sheet-list {
      display: flex;
      flex-direction: column;
      gap: 0.45rem;
    }
    .action-sheet-btn {
      width: 100%;
      min-height: 48px;
      justify-content: flex-start;
      padding: 0.7rem 1rem;
      font-size: 0.92rem;
      border-radius: 8px;
    }

    /* =========================================================================
       DENSITY MODE: COMPACT (Reduces paddings & card heights, keeps essentials)
       ========================================================================= */
    body.density-compact .card { padding: 0.75rem; margin-bottom: 0.75rem; }
    body.density-compact .metric-card { padding: 0.55rem 0.7rem; min-height: 54px; }
    body.density-compact .metric-data .metric-value { font-size: 1.2rem; }
    body.density-compact .event-card { padding: 0.65rem 0.8rem; gap: 0.45rem; }
    body.density-compact .data-table th,
    body.density-compact .data-table td { padding: 0.4rem 0.6rem; font-size: 0.78rem; }
    body.density-compact .form-help { display: none; }

    /* =========================================================================
       MODE 1: CELULAR (body[data-layout-mode="mobile"])
       ========================================================================= */
    body[data-layout-mode="mobile"] {
      padding-bottom: 76px;
    }
    body[data-layout-mode="mobile"] .app-nav { display: none !important; }
    body[data-layout-mode="mobile"] .btn-hamburger { display: inline-flex !important; min-width: 44px; min-height: 44px; }
    body[data-layout-mode="mobile"] .mobile-bottom-nav { display: flex !important; }
    body[data-layout-mode="mobile"] .header-brand h1 { font-size: 0.98rem; }
    body[data-layout-mode="mobile"] .header-brand .subtitle { display: none !important; }
    body[data-layout-mode="mobile"] #pillDB,
    body[data-layout-mode="mobile"] #pillNotif,
    body[data-layout-mode="mobile"] #pillBackup,
    body[data-layout-mode="mobile"] #btnHeaderTestNotif,
    body[data-layout-mode="mobile"] #btnControllerBadge,
    body[data-layout-mode="mobile"] #btnQuickAddEvent {
      display: none !important;
    }
    body[data-layout-mode="mobile"] .app-header {
      flex-wrap: wrap;
      padding: 0.45rem 0.75rem;
      gap: 0.4rem;
    }
    body[data-layout-mode="mobile"] .header-left {
      width: 100%;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 0.4rem;
    }
    body[data-layout-mode="mobile"] .header-console-box {
      order: 3;
      width: 100%;
      justify-content: space-between;
      padding: 0.35rem 0.75rem;
      min-height: 42px;
    }
    body[data-layout-mode="mobile"] .app-main {
      padding: 0.75rem 16px;
    }
    /* Mobile Dashboard Priority Order (Section 3.1):
       1. Spotlight -> 2. Urgent Cards -> 3. 2-Column Metrics */
    body[data-layout-mode="mobile"] #viewDashboard.active {
      display: flex;
      flex-direction: column;
    }
    body[data-layout-mode="mobile"] #viewDashboard .dashboard-highlight-grid { order: 1; }
    body[data-layout-mode="mobile"] #viewDashboard #cardDashboardUrgent { order: 2; }
    body[data-layout-mode="mobile"] #viewDashboard .dashboard-metrics {
      order: 3;
      grid-template-columns: repeat(2, 1fr);
      gap: 0.6rem;
    }
    body[data-layout-mode="mobile"] .spotlight-body { grid-template-columns: 1fr; }
    body[data-layout-mode="mobile"] .spotlight-timer {
      align-items: flex-start;
      text-align: left;
      margin-top: 0.25rem;
    }
    body[data-layout-mode="mobile"] .spotlight-timer .time-left { font-size: 1.65rem; }
    body[data-layout-mode="mobile"] #tableDashboardUrgent { display: none; }
    body[data-layout-mode="mobile"] .dashboard-urgent-cards { display: flex; }

    /* Mobile Pending Events */
    body[data-layout-mode="mobile"] .events-container-cards { grid-template-columns: 1fr; }
    body[data-layout-mode="mobile"] #filterDrawer.active-sheet {
      position: fixed;
      left: 0;
      right: 0;
      bottom: 0;
      z-index: 1200;
      background: var(--bg-elevated);
      border-top: 2px solid var(--border-color-focus);
      border-radius: 16px 16px 0 0;
      padding: 1rem 1rem calc(1rem + env(safe-area-inset-bottom, 0px));
      max-height: 85vh;
      overflow-y: auto;
      box-shadow: var(--shadow-lg);
      display: grid !important;
      grid-template-columns: 1fr;
    }

    /* Mobile Completed Events: Expandable Cards instead of 9-col Table */
    body[data-layout-mode="mobile"] #tableCompletedWrapper { display: none; }
    body[data-layout-mode="mobile"] .completed-cards-container { display: flex; }

    /* Mobile Cadastros: Category List + Single Active Category */
    body[data-layout-mode="mobile"] .cadastros-category-bar { display: flex; flex-direction: column; }
    body[data-layout-mode="mobile"] .cadastros-unified-grid { grid-template-columns: 1fr; }
    body[data-layout-mode="mobile"] .cadastro-hub-card[data-cad-hidden="true"] { display: none !important; }

    /* Mobile Color Ranges: Cards */
    body[data-layout-mode="mobile"] #tableColorRangesWrapper { display: none; }
    body[data-layout-mode="mobile"] .color-range-cards { display: flex; }

    /* Mobile Touch Ergonomics & Form Sticky Bar (Sections 5.5 & 20) */
    body[data-layout-mode="mobile"] input[type="text"],
    body[data-layout-mode="mobile"] input[type="number"],
    body[data-layout-mode="mobile"] input[type="date"],
    body[data-layout-mode="mobile"] input[type="time"],
    body[data-layout-mode="mobile"] select,
    body[data-layout-mode="mobile"] textarea {
      min-height: 48px;
      font-size: 16px;
    }
    body[data-layout-mode="mobile"] .btn {
      min-height: 46px;
    }
    body[data-layout-mode="mobile"] .form-sticky-submit-bar {
      position: sticky;
      bottom: calc(64px + env(safe-area-inset-bottom, 0px));
      background: var(--bg-surface);
      border-top: 1px solid var(--border-color);
      padding: 0.75rem;
      margin: 1rem -0.85rem -0.85rem;
      border-radius: 0 0 8px 8px;
      z-index: 50;
      box-shadow: 0 -4px 10px rgba(0, 0, 0, 0.25);
    }

    /* Mobile Modals: Fullscreen for Alarm & Details, Bottom Sheet for Snooze & Actions (Sections 7 & 19.1) */
    body[data-layout-mode="mobile"] #modalAlarmTrigger,
    body[data-layout-mode="mobile"] #modalEventDetails {
      padding: 0;
    }
    body[data-layout-mode="mobile"] #modalAlarmTrigger .modal-box,
    body[data-layout-mode="mobile"] #modalEventDetails .modal-box {
      max-width: 100vw;
      width: 100vw;
      height: 100dvh;
      max-height: 100dvh;
      border-radius: 0;
      justify-content: space-between;
    }
    body[data-layout-mode="mobile"] #modalAlarmTrigger .modal-footer {
      flex-direction: column;
      align-items: stretch;
      gap: 0.6rem;
      padding: 1rem 1.15rem calc(1rem + env(safe-area-inset-bottom, 0px));
    }
    body[data-layout-mode="mobile"] #modalAlarmTrigger .modal-footer .btn {
      width: 100%;
      min-height: 50px;
      font-size: 0.95rem;
    }
    body[data-layout-mode="mobile"] #modalSnooze,
    body[data-layout-mode="mobile"] #modalEventActionSheet {
      align-items: flex-end;
      padding: 0;
    }
    body[data-layout-mode="mobile"] #modalSnooze .modal-box,
    body[data-layout-mode="mobile"] #modalEventActionSheet .modal-box {
      max-width: 100vw;
      width: 100vw;
      border-radius: 16px 16px 0 0;
      padding-bottom: env(safe-area-inset-bottom, 0px);
    }

    /* =========================================================================
       MODE 2: TABLET (body[data-layout-mode="tablet"])
       ========================================================================= */
    body[data-layout-mode="tablet"] .btn-hamburger { display: inline-flex; min-width: 44px; min-height: 44px; }
    body[data-layout-mode="tablet"] .app-main { padding: 1.25rem 24px; }
    body[data-layout-mode="tablet"] .dashboard-metrics {
      grid-template-columns: repeat(auto-fit, minmax(145px, 1fr));
    }
    body[data-layout-mode="tablet"] .dashboard-highlight-grid {
      grid-template-columns: 1.75fr 1fr;
    }
    body[data-layout-mode="tablet"] .tablet-alarms-panel {
      display: flex;
    }
    body[data-layout-mode="tablet"] .pending-master-detail-grid {
      grid-template-columns: 1.15fr 1fr;
    }
    body[data-layout-mode="tablet"] .pending-detail-pane {
      display: block;
    }
    body[data-layout-mode="tablet"] .pending-master-detail-grid .events-container-cards {
      grid-template-columns: 1fr;
    }
    body[data-layout-mode="tablet"] .stylus-canvas {
      min-height: 280px;
    }
    body[data-layout-mode="tablet"] .cadastros-category-bar {
      display: flex;
    }
    body[data-layout-mode="tablet"] .cadastros-unified-grid {
      grid-template-columns: 1fr;
    }
    body[data-layout-mode="tablet"] .cadastro-hub-card[data-cad-hidden="true"] {
      display: none !important;
    }
    body[data-layout-mode="tablet"] input[type="text"],
    body[data-layout-mode="tablet"] input[type="number"],
    body[data-layout-mode="tablet"] input[type="date"],
    body[data-layout-mode="tablet"] input[type="time"],
    body[data-layout-mode="tablet"] select {
      min-height: 46px;
    }
    body[data-layout-mode="tablet"] .btn {
      min-height: 44px;
    }

    /* =========================================================================
       MODE 3, 4, 5: CONVENTIONAL, WIDESCREEN, ULTRAWIDE
       ========================================================================= */
    body[data-layout-mode="widescreen"] .app-main { max-width: 2100px; }
    body[data-layout-mode="widescreen"] .dashboard-highlight-grid,
    body[data-layout-mode="ultrawide"] .dashboard-highlight-grid {
      grid-template-columns: 2fr 1fr;
    }
    body[data-layout-mode="widescreen"] .tablet-alarms-panel,
    body[data-layout-mode="ultrawide"] .tablet-alarms-panel {
      display: flex;
    }
    body[data-layout-mode="widescreen"] #filterDrawer,
    body[data-layout-mode="ultrawide"] #filterDrawer {
      display: grid !important;
    }
    body[data-layout-mode="ultrawide"] .app-main { max-width: 100%; padding: 1.25rem 2rem; }
    body[data-layout-mode="ultrawide"] .pending-master-detail-grid {
      grid-template-columns: 1.6fr 1fr;
    }
    body[data-layout-mode="ultrawide"] .pending-detail-pane {
      display: block;
    }

    /* Fallback Native Media Queries when JS is initializing */
    @media (max-width: 767px) {
      .dashboard-metrics { grid-template-columns: repeat(2, 1fr); }
      .spotlight-body { grid-template-columns: 1fr; }
      .events-container-cards { grid-template-columns: 1fr; }
    }
    @media (max-width: 359px) {
      body[data-layout-mode="mobile"] .dashboard-metrics { grid-template-columns: 1fr; }
    }
"""
