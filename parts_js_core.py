# -*- coding: utf-8 -*-
JS_CORE = """
window.App = window.App || {};

/* ==========================================================================
   1. CONFIGURAÇÕES E CONSTANTES
   ========================================================================== */
App.Config = {
  APP_VERSION: '1.2.0',
  DB_NAME: 'LivroPrevisoesDutosDB',
  DB_VERSION: 1,
  
  INITIAL_CONSOLES: [
    'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C10', 'C11', 'C14', 'C15', 'C16'
  ],

  DEFAULT_COLOR_RANGES: [
    { id: 'range_critico', name: 'Crítico', color: '#dc2626', minMinutes: 0, maxMinutes: 15, unit: 'min', priority: 1, blink: true, sound: true, active: true },
    { id: 'range_urgente', name: 'Urgente', color: '#ea580c', minMinutes: 15, maxMinutes: 30, unit: 'min', priority: 2, blink: false, sound: false, active: true },
    { id: 'range_atencao', name: 'Atenção', color: '#ca8a04', minMinutes: 30, maxMinutes: 45, unit: 'min', priority: 3, blink: false, sound: false, active: true },
    { id: 'range_monitor', name: 'Monitoramento', color: '#2563eb', minMinutes: 45, maxMinutes: 60, unit: 'min', priority: 4, blink: false, sound: false, active: true },
    { id: 'range_normal', name: 'Normal', color: '#16a34a', minMinutes: 60, maxMinutes: 999999, unit: 'min', priority: 5, blink: false, sound: false, active: true }
  ],

  DEFAULT_SETTINGS: {
    localUserName: 'Usuário local',
    soundEnabled: true,
    soundType: 'chime',
    soundVolume: 80,
    visualAlertEnabled: true,
    highlightCardEnabled: true,
    pulsingEnabled: true,
    changeTitleEnabled: true,
    notificationEnabled: false,
    repeatAlarm: true,
    repeatIntervalMinutes: 2,
    maxRepeats: 5,
    defaultLeadTimeMinutes: 15,
    theme: 'dark',
    viewMode: 'cards',
    responsiveLayoutMode: 'auto',
    backupReminderDays: 7,
    firstMobileNoticeShown: false,
    lastBackupAt: null,
    activeConsoleId: null,
    keepDutoUOPrefilled: true
  }
};

/* ==========================================================================
   2. UTILITÁRIOS E FORMATAÇÃO BRASILEIRA
   ========================================================================== */
App.Utils = {
  // Geração de UUID v4 padronizado para sincronização futura
  uuid: function() {
    if (typeof crypto !== 'undefined' && crypto.randomUUID) {
      return crypto.randomUUID();
    }
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  },

  // Limpeza de strings para comparações case-insensitive e trim
  cleanStr: function(str) {
    if (!str) return '';
    return str.toString().trim().toLowerCase();
  },

  // Escape de HTML contra XSS
  escapeHTML: function(str) {
    if (str === null || str === undefined) return '';
    return str.toString()
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  },

  // Formatação de data no padrão DD/MM/AAAA
  formatDate: function(dateStr) {
    if (!dateStr) return '--';
    const parts = dateStr.split('-');
    if (parts.length === 3) {
      return `${parts[2]}/${parts[1]}/${parts[0]}`;
    }
    const d = new Date(dateStr);
    if (isNaN(d.getTime())) return dateStr;
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    return `${day}/${month}/${year}`;
  },

  // Formatação de hora no padrão HH:mm
  formatTime: function(timeStr) {
    if (!timeStr) return '--';
    if (typeof timeStr === 'string' && timeStr.includes(':')) {
      return timeStr.substring(0, 5);
    }
    const d = new Date(timeStr);
    if (isNaN(d.getTime())) return timeStr;
    const hours = String(d.getHours()).padStart(2, '0');
    const minutes = String(d.getMinutes()).padStart(2, '0');
    return `${hours}:${minutes}`;
  },

  // Formatação combinada DD/MM/AAAA HH:mm
  formatDateTime: function(isoOrDateStr, timeStr) {
    if (!isoOrDateStr) return '--';
    if (timeStr) {
      return `${App.Utils.formatDate(isoOrDateStr)} ${App.Utils.formatTime(timeStr)}`;
    }
    const d = new Date(isoOrDateStr);
    if (isNaN(d.getTime())) return isoOrDateStr;
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    const hours = String(d.getHours()).padStart(2, '0');
    const minutes = String(d.getMinutes()).padStart(2, '0');
    return `${day}/${month}/${year} ${hours}:${minutes}`;
  },

  // Formatação descritiva de duração em português do Brasil
  formatDuration: function(totalSeconds) {
    const sec = Math.max(0, Math.floor(totalSeconds));
    const hours = Math.floor(sec / 3600);
    const minutes = Math.floor((sec % 3600) / 60);
    const seconds = sec % 60;

    if (hours > 0) {
      if (minutes > 0) {
        return `${hours} ${hours === 1 ? 'hora' : 'horas'} e ${minutes} ${minutes === 1 ? 'minuto' : 'minutos'}`;
      }
      return `${hours} ${hours === 1 ? 'hora' : 'horas'}`;
    }
    if (minutes > 0) {
      return `${minutes} ${minutes === 1 ? 'minuto' : 'minutos'}`;
    }
    return `${seconds} ${seconds === 1 ? 'segundo' : 'segundos'}`;
  },

  // Cálculo e texto de tempo restante ou tempo de atraso
  formatTimeRemaining: function(targetTimestamp) {
    if (!targetTimestamp) return { text: '--', diffSec: 0, isOverdue: false };
    const now = Date.now();
    const diffSec = Math.floor((targetTimestamp - now) / 1000);

    if (diffSec < 0) {
      const overdueSec = Math.abs(diffSec);
      return {
        text: `Atrasado há ${App.Utils.formatDuration(overdueSec)}`,
        diffSec: diffSec,
        isOverdue: true
      };
    } else {
      return {
        text: `Faltam ${App.Utils.formatDuration(diffSec)}`,
        diffSec: diffSec,
        isOverdue: false
      };
    }
  },

  // Formatação da diferença de tempo na conclusão
  formatDiffMinutes: function(diffMinutes) {
    if (diffMinutes === null || diffMinutes === undefined) return '--';
    const m = Math.round(diffMinutes);
    if (m > 0) return `Com atraso de ${m} min`;
    if (m < 0) return `Com antecedência de ${Math.abs(m)} min`;
    return 'Exatamente no horário';
  },

  // Escape para CSV padrão Excel (ponto e vírgula, com aspas se necessário)
  escapeCSV: function(value) {
    if (value === null || value === undefined) return '""';
    let str = value.toString();
    if (str.includes(';') || str.includes('"') || str.includes('\\n') || str.includes('\\r')) {
      str = '"' + str.replace(/"/g, '""') + '"';
    }
    return str;
  }
};

/* ==========================================================================
   3. CAMADA DE ÁUDIO (WEB AUDIO API LOCAL)
   ========================================================================== */
App.Audio = {
  ctx: null,
  isUnlocked: false,

  init: function() {
    if (!this.ctx && (window.AudioContext || window.webkitAudioContext)) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      this.ctx = new AudioCtx();
    }
    if (this.ctx && this.ctx.state === 'running') {
      this.isUnlocked = true;
    }
    this.updateStatusPill();
  },

  unlock: function() {
    if (!this.ctx) this.init();
    if (this.ctx && this.ctx.state !== 'running') {
      this.ctx.resume().then(() => {
        this.isUnlocked = true;
        this.updateStatusPill();
      }).catch(err => {
        console.warn('Erro ao desbloquear áudio:', err);
      });
    } else if (this.ctx && this.ctx.state === 'running') {
      this.isUnlocked = true;
      this.updateStatusPill();
    }
  },

  updateStatusPill: function() {
    const pill = document.getElementById('pillAudio');
    const mobileWarn = document.getElementById('chipHeaderAudioWarning');
    const statusModalEl = document.getElementById('statusModalAudio');
    const isReady = Boolean(this.isUnlocked && this.ctx && this.ctx.state === 'running');
    if (pill) {
      if (isReady) {
        pill.className = 'status-pill ok';
        pill.innerHTML = '<span class="indicator-dot">&bull;</span> Áudio: Ativo';
        pill.title = 'Áudio habilitado e operacional';
      } else {
        pill.className = 'status-pill warning';
        pill.innerHTML = '<span class="indicator-dot">&bull;</span> Áudio: Iniciar';
        pill.title = 'Clique em qualquer lugar da tela ou teste o som para habilitar o áudio do navegador';
      }
    }
    if (mobileWarn) {
      mobileWarn.style.display = isReady ? 'none' : 'inline-flex';
    }
    if (statusModalEl) {
      statusModalEl.innerHTML = isReady
        ? '<span style="color:#4ade80;">&#9679; Ativo e desbloqueado</span>'
        : '<span style="color:#fbbf24;">&#9888; Áudio não iniciado (Toque para ativar)</span>';
    }
  },

  play: function(type = 'chime', volumePercent = 80) {
    const requestedVolume = Number(volumePercent);
    if (!Number.isFinite(requestedVolume) || requestedVolume <= 0) return;
    this.unlock();
    if (!this.ctx) return;

    const gainNode = this.ctx.createGain();
    const masterVol = Math.max(0, Math.min(100, requestedVolume)) / 100 * 0.3; // safe gain ceiling
    gainNode.gain.setValueAtTime(masterVol, this.ctx.currentTime);
    gainNode.connect(this.ctx.destination);

    const now = this.ctx.currentTime;

    switch (type) {
      case 'beep':
        // Beep duplo 880Hz
        for (let i = 0; i < 2; i++) {
          const osc = this.ctx.createOscillator();
          const noteGain = this.ctx.createGain();
          osc.type = 'square';
          osc.frequency.setValueAtTime(880, now + (i * 0.18));
          
          noteGain.gain.setValueAtTime(0, now + (i * 0.18));
          noteGain.gain.linearRampToValueAtTime(masterVol, now + (i * 0.18) + 0.02);
          noteGain.gain.exponentialRampToValueAtTime(0.001, now + (i * 0.18) + 0.12);
          
          osc.connect(noteGain);
          noteGain.connect(this.ctx.destination);
          osc.start(now + (i * 0.18));
          osc.stop(now + (i * 0.18) + 0.14);
        }
        break;

      case 'siren':
        // Sirene de alerta urgente de duas frequências
        const sirenOsc = this.ctx.createOscillator();
        sirenOsc.type = 'sawtooth';
        sirenOsc.frequency.setValueAtTime(650, now);
        sirenOsc.frequency.linearRampToValueAtTime(950, now + 0.25);
        sirenOsc.frequency.linearRampToValueAtTime(650, now + 0.5);
        sirenOsc.frequency.linearRampToValueAtTime(950, now + 0.75);
        sirenOsc.frequency.linearRampToValueAtTime(650, now + 1.0);

        gainNode.gain.setValueAtTime(masterVol * 0.7, now);
        gainNode.gain.exponentialRampToValueAtTime(0.001, now + 1.1);

        sirenOsc.connect(gainNode);
        sirenOsc.start(now);
        sirenOsc.stop(now + 1.1);
        break;

      case 'blip':
        // Blip suave
        const blipOsc = this.ctx.createOscillator();
        blipOsc.type = 'sine';
        blipOsc.frequency.setValueAtTime(1046.5, now); // C6
        gainNode.gain.setValueAtTime(masterVol, now);
        gainNode.gain.exponentialRampToValueAtTime(0.001, now + 0.15);
        blipOsc.connect(gainNode);
        blipOsc.start(now);
        blipOsc.stop(now + 0.16);
        break;

      case 'chime':
      default:
        // Chime harmônico de 3 notas: C5 (523Hz), E5 (659Hz), G5 (784Hz)
        const notes = [523.25, 659.25, 783.99];
        notes.forEach((freq, idx) => {
          const osc = this.ctx.createOscillator();
          const noteGain = this.ctx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, now + (idx * 0.15));

          noteGain.gain.setValueAtTime(0, now + (idx * 0.15));
          noteGain.gain.linearRampToValueAtTime(masterVol, now + (idx * 0.15) + 0.03);
          noteGain.gain.exponentialRampToValueAtTime(0.001, now + (idx * 0.15) + 0.45);

          osc.connect(noteGain);
          noteGain.connect(this.ctx.destination);
          osc.start(now + (idx * 0.15));
          osc.stop(now + (idx * 0.15) + 0.5);
        });
        break;
    }
  }
};

/* ==========================================================================
   4. NOTIFICAÇÕES DO NAVEGADOR (WEB NOTIFICATIONS API)
   ========================================================================== */
App.Notifications = {
  isSupported: function() {
    return 'Notification' in window;
  },

  getPermissionState: function() {
    if (!this.isSupported()) return 'indisponivel';
    if (Notification.permission === 'granted') return 'concedida';
    if (Notification.permission === 'denied') return 'negada';
    return 'nao_solicitada';
  },

  updateStatusPill: function() {
    const pill = document.getElementById('pillNotif');
    const statusModalEl = document.getElementById('statusModalNotif');
    const state = this.getPermissionState();
    if (pill) {
      if (state === 'concedida') {
        pill.className = 'status-pill ok';
        pill.innerHTML = '<span class="indicator-dot">&bull;</span> Notif: Ativa';
        pill.title = 'Permissão de notificações concedida';
      } else if (state === 'negada') {
        pill.className = 'status-pill danger';
        pill.innerHTML = '<span class="indicator-dot">&bull;</span> Notif: Negada';
        pill.title = 'Permissão negada. É necessário autorizar nas configurações do navegador.';
      } else if (state === 'indisponivel') {
        pill.className = 'status-pill';
        pill.innerHTML = '<span class="indicator-dot">&bull;</span> Notif: Indisp.';
        pill.title = 'Notificações não suportadas neste ambiente';
      } else {
        pill.className = 'status-pill warning';
        pill.innerHTML = '<span class="indicator-dot">&bull;</span> Notif: Solicitar';
        pill.title = 'Clique para solicitar permissão de notificações do navegador';
      }
    }
    if (statusModalEl) {
      if (state === 'concedida') {
        statusModalEl.innerHTML = '<span style="color:#4ade80;">&#9679; Concedidas</span>';
      } else if (state === 'negada') {
        statusModalEl.innerHTML = '<span style="color:#f87171;">&#9679; Negadas pelo navegador</span>';
      } else if (state === 'indisponivel') {
        statusModalEl.innerHTML = '<span style="color:#94a3b8;">&#9679; Indisponíveis neste navegador</span>';
      } else {
        statusModalEl.innerHTML = '<span style="color:#fbbf24;">&#9888; Pendentes de autorização</span>';
      }
    }
  },

  requestPermission: async function() {
    if (!this.isSupported()) {
      App.UI.showToast('Web Notifications API não é suportada por este navegador.', 'warning');
      return false;
    }
    try {
      const permission = await Notification.requestPermission();
      this.updateStatusPill();
      if (permission === 'granted') {
        App.UI.showToast('Permissão para notificações concedida com sucesso!', 'success');
        return true;
      } else if (permission === 'denied') {
        App.UI.showToast('Permissão de notificações negada pelo usuário.', 'danger');
        return false;
      }
      return false;
    } catch (err) {
      console.error('Erro ao solicitar permissão de notificações:', err);
      return false;
    }
  },

  send: function(title, options = {}) {
    if (!this.isSupported() || Notification.permission !== 'granted') return null;
    try {
      const notif = new Notification(title, {
        badge: options.badge || '',
        body: options.body || '',
        tag: options.tag || 'previsao-dutos',
        requireInteraction: true,
        ...options
      });
      notif.onclick = function() {
        window.focus();
        this.close();
      };
      return notif;
    } catch (err) {
      console.warn('Falha ao disparar notificação nativa:', err);
      return null;
    }
  }
};

/* ==========================================================================
   5. CAMADA DE PERSISTÊNCIA LOCAL (INDEXEDDB)
   ========================================================================== */
App.DB = {
  db: null,

  open: function() {
    return new Promise((resolve, reject) => {
      if (this.db) {
        resolve(this.db);
        return;
      }

      const request = indexedDB.open(App.Config.DB_NAME, App.Config.DB_VERSION);

      request.onupgradeneeded = (event) => {
        const db = event.target.result;
        
        // 1. Consoles
        if (!db.objectStoreNames.contains('consoles')) {
          const store = db.createObjectStore('consoles', { keyPath: 'id' });
          store.createIndex('name', 'name', { unique: false });
          store.createIndex('active', 'active', { unique: false });
        }

        // 2. Dutos (Pipelines)
        if (!db.objectStoreNames.contains('pipelines')) {
          const store = db.createObjectStore('pipelines', { keyPath: 'id' });
          store.createIndex('consoleId', 'consoleId', { unique: false });
          store.createIndex('name', 'name', { unique: false });
          store.createIndex('active', 'active', { unique: false });
        }

        // 3. Unidades Operacionais (UOs)
        if (!db.objectStoreNames.contains('operationalUnits')) {
          const store = db.createObjectStore('operationalUnits', { keyPath: 'id' });
          store.createIndex('name', 'name', { unique: false });
          store.createIndex('active', 'active', { unique: false });
        }

        // 4. Relacionamento Muitos-para-Muitos Duto <-> UO
        if (!db.objectStoreNames.contains('pipelineOperationalUnits')) {
          const store = db.createObjectStore('pipelineOperationalUnits', { keyPath: 'id' });
          store.createIndex('pipelineId', 'pipelineId', { unique: false });
          store.createIndex('uoId', 'uoId', { unique: false });
        }

        // 5. Tipos de Equipamentos (vinculados à UO)
        if (!db.objectStoreNames.contains('equipmentTypes')) {
          const store = db.createObjectStore('equipmentTypes', { keyPath: 'id' });
          store.createIndex('uoId', 'uoId', { unique: false });
          store.createIndex('name', 'name', { unique: false });
          store.createIndex('active', 'active', { unique: false });
        }

        // 6. TAGs de Equipamentos (exclusivos por UO)
        if (!db.objectStoreNames.contains('equipmentTags')) {
          const store = db.createObjectStore('equipmentTags', { keyPath: 'id' });
          store.createIndex('uoId', 'uoId', { unique: false });
          store.createIndex('equipmentTypeId', 'equipmentTypeId', { unique: false });
          store.createIndex('tag', 'tag', { unique: false });
          store.createIndex('active', 'active', { unique: false });
        }

        // 7. Eventos / Previsões
        if (!db.objectStoreNames.contains('events')) {
          const store = db.createObjectStore('events', { keyPath: 'id' });
          store.createIndex('status', 'status', { unique: false });
          store.createIndex('scheduledAt', 'scheduledAt', { unique: false });
          store.createIndex('consoleId', 'consoleId', { unique: false });
          store.createIndex('pipelineId', 'pipelineId', { unique: false });
          store.createIndex('uoId', 'uoId', { unique: false });
          store.createIndex('active', 'active', { unique: false });
        }

        // 8. Histórico de Auditoria dos Eventos
        if (!db.objectStoreNames.contains('eventHistory')) {
          const store = db.createObjectStore('eventHistory', { keyPath: 'id' });
          store.createIndex('eventId', 'eventId', { unique: false });
          store.createIndex('timestamp', 'timestamp', { unique: false });
        }

        // 9. Faixas de Cores
        if (!db.objectStoreNames.contains('colorRanges')) {
          const store = db.createObjectStore('colorRanges', { keyPath: 'id' });
          store.createIndex('minMinutes', 'minMinutes', { unique: false });
          store.createIndex('priority', 'priority', { unique: false });
        }

        // 10. Configurações Globais
        if (!db.objectStoreNames.contains('settings')) {
          db.createObjectStore('settings', { keyPath: 'key' });
        }

        // 11. Logs Internos de Diagnóstico
        if (!db.objectStoreNames.contains('errorLogs')) {
          const store = db.createObjectStore('errorLogs', { keyPath: 'id' });
          store.createIndex('timestamp', 'timestamp', { unique: false });
        }
      };

      request.onsuccess = (event) => {
        this.db = event.target.result;
        resolve(this.db);
      };

      request.onerror = (event) => {
        console.error('Erro ao abrir IndexedDB:', event.target.error);
        reject(event.target.error);
      };
    });
  },

  // Inicialização de dados padrão (Consoles C02 a C16, Faixas de cores, Configurações)
  initDefaults: async function() {
    await this.open();
    
    // 1. Consoles Iniciais (Não duplicar se já existirem)
    const existingConsoles = await this.getAll('consoles');
    if (existingConsoles.length === 0) {
      const now = new Date().toISOString();
      for (const name of App.Config.INITIAL_CONSOLES) {
        await this.insert('consoles', {
          id: App.Utils.uuid(),
          name: name,
          active: true,
          createdAt: now,
          updatedAt: now,
          version: 1,
          synchronizationStatus: 'local-only'
        });
      }
    }

    // 2. Faixas de Cores Iniciais
    const existingRanges = await this.getAll('colorRanges');
    if (existingRanges.length === 0) {
      for (const range of App.Config.DEFAULT_COLOR_RANGES) {
        await this.insert('colorRanges', range);
      }
    }

    // 3. Configurações Iniciais
    const currentSettings = await this.get('settings', 'app_settings');
    const allConsolesNow = await this.getAll('consoles');
    const firstConsoleId = allConsolesNow.find(c => c.name === 'C04')?.id || allConsolesNow[0]?.id || null;

    if (!currentSettings) {
      await this.insert('settings', {
        key: 'app_settings',
        value: {
          ...App.Config.DEFAULT_SETTINGS,
          activeConsoleId: firstConsoleId
        }
      });
    } else if (!currentSettings.value.activeConsoleId && firstConsoleId) {
      currentSettings.value.activeConsoleId = firstConsoleId;
      await this.update('settings', currentSettings);
    }
  },

  // Operações genéricas de CRUD em promises
  insert: function(storeName, item) {
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([storeName], 'readwrite');
      const store = transaction.objectStore(storeName);
      const request = store.add(item);
      request.onsuccess = () => resolve(item);
      request.onerror = (e) => reject(e.target.error);
    });
  },

  get: function(storeName, key) {
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([storeName], 'readonly');
      const store = transaction.objectStore(storeName);
      const request = store.get(key);
      request.onsuccess = (e) => resolve(e.target.result || null);
      request.onerror = (e) => reject(e.target.error);
    });
  },

  getAll: function(storeName) {
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([storeName], 'readonly');
      const store = transaction.objectStore(storeName);
      const request = store.getAll();
      request.onsuccess = (e) => resolve(e.target.result || []);
      request.onerror = (e) => reject(e.target.error);
    });
  },

  update: function(storeName, item) {
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([storeName], 'readwrite');
      const store = transaction.objectStore(storeName);
      const request = store.put(item);
      request.onsuccess = () => resolve(item);
      request.onerror = (e) => reject(e.target.error);
    });
  },

  delete: function(storeName, key) {
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([storeName], 'readwrite');
      const store = transaction.objectStore(storeName);
      const request = store.delete(key);
      request.onsuccess = () => resolve(true);
      request.onerror = (e) => reject(e.target.error);
    });
  },

  clear: function(storeName) {
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([storeName], 'readwrite');
      const store = transaction.objectStore(storeName);
      const request = store.clear();
      request.onsuccess = () => resolve(true);
      request.onerror = (e) => reject(e.target.error);
    });
  },

  logError: async function(error, context = 'Geral') {
    try {
      if (!this.db) await this.open();
      const errItem = {
        id: App.Utils.uuid(),
        timestamp: new Date().toISOString(),
        context: context,
        message: error?.message || String(error),
        details: error?.stack || JSON.stringify(error) || ''
      };
      await this.insert('errorLogs', errItem);
    } catch (e) {
      console.error('Falha ao registrar log de erro interno:', e);
    }
  }
};
"""


# Transactional persistence and strict local calendar utilities.
JS_CORE += r"""
(() => {
  const U = App.Utils;
  U.localDateTime = function(date, time = '00:00') {
    if (typeof date !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(date) || typeof time !== 'string' || !/^\d{2}:\d{2}$/.test(time)) throw new Error('Data ou hora inválida.');
    const [y,m,d] = date.split('-').map(Number), [h,n] = time.split(':').map(Number);
    const value = new Date(y,m-1,d,h,n,0,0);
    if (y < 100 || value.getFullYear()!==y || value.getMonth()!==m-1 || value.getDate()!==d || value.getHours()!==h || value.getMinutes()!==n) throw new Error('Data ou hora inválida.');
    return value;
  };
  U.formatDate = function(value) {
    if (!value) return '--';
    let date;
    try { date = typeof value==='string' && /^\d{4}-\d{2}-\d{2}$/.test(value) ? U.localDateTime(value) : new Date(value); } catch (_) { return '--'; }
    if (!Number.isFinite(date.getTime())) return '--';
    return `${String(date.getDate()).padStart(2,'0')}/${String(date.getMonth()+1).padStart(2,'0')}/${date.getFullYear()}`;
  };
  U.formatTime = function(value) {
    if (!value) return '--';
    if (typeof value==='string' && /^([01]\d|2[0-3]):[0-5]\d$/.test(value)) return value;
    const date = new Date(value);
    return Number.isFinite(date.getTime()) ? `${String(date.getHours()).padStart(2,'0')}:${String(date.getMinutes()).padStart(2,'0')}` : '--';
  };
  U.formatDateTime = function(value, time) {
    if (!value) return '--';
    if (time !== undefined && time !== null && time !== '') return `${U.formatDate(value)} ${U.formatTime(time)}`;
    let date;
    try { date = typeof value==='string' && /^\d{4}-\d{2}-\d{2}$/.test(value) ? U.localDateTime(value) : new Date(value); } catch (_) { return '--'; }
    if (!Number.isFinite(date.getTime())) return '--';
    return `${U.formatDate(date)} ${U.formatTime(date)}`;
  };
  U.escapeCSV = function(value) {
    if (value===null || value===undefined) return '""';
    let text = String(value);
    if (typeof value==='string' && /^[\s]*[=+\-@\t\r]/.test(text)) text="'"+text;
    return /[;"\n\r]/.test(text) ? '"'+text.replace(/"/g,'""')+'"' : text;
  };
  App.DB.DATA_STORES = ['consoles','pipelines','operationalUnits','pipelineOperationalUnits','equipmentTypes','equipmentTags','events','eventHistory','colorRanges','settings'];
  // callback(draft, transaction) MUST be synchronous. Changed JSON record arrays are
  // replaced together; unchanged arrays issue no writes. Throws/abort roll everything back. Do not await
  // external work from callback: IndexedDB would close the transaction.
  App.DB.atomic = async function(names, callback) {
    await this.open();
    return new Promise((resolve,reject) => {
      const tx=this.db.transaction(names,'readwrite'), draft={}; let remaining=names.length, result, failure;
      tx.oncomplete=()=>resolve(result);
      tx.onabort=()=>reject(failure || tx.error || new Error('Transação cancelada.'));
      tx.onerror=()=>{ failure=tx.error; };
      for (const name of names) {
        const q=tx.objectStore(name).getAll();
        q.onsuccess=()=>{
          draft[name]=q.result;
          if (--remaining) return;
          try {
            const before=Object.fromEntries(names.map(store=>[store,JSON.stringify(draft[store])]));
            result=callback(draft,tx);
            if (result && typeof result.then==='function') throw new Error('Callback transacional deve ser síncrono.');
            for (const store of names) {
              if (JSON.stringify(draft[store])===before[store]) continue;
              const target=tx.objectStore(store); target.clear();
              for (const item of draft[store]) target.add(item);
            }
          } catch (err) { failure=err; tx.abort(); }
        };
      }
    });
  };
  App.DB.snapshot = async function(names=this.DATA_STORES) {
    await this.open();
    return new Promise((resolve,reject)=>{
      const tx=this.db.transaction(names,'readonly'), result={};
      tx.oncomplete=()=>resolve(result);
      tx.onabort=()=>reject(tx.error || new Error('Leitura cancelada.'));
      tx.onerror=()=>reject(tx.error);
      for (const name of names) { const q=tx.objectStore(name).getAll(); q.onsuccess=()=>{result[name]=q.result;}; }
    });
  };
  for (const [method,operation] of [['insert','add'],['update','put'],['delete','delete'],['clear','clear']]) {
    App.DB[method]=async function(name,item) {
      await this.open();
      return new Promise((resolve,reject)=>{
        const tx=this.db.transaction([name],'readwrite'); let failure;
        tx.oncomplete=()=>resolve(method==='insert'||method==='update' ? item : true);
        tx.onabort=()=>reject(failure || tx.error || new Error('Transação cancelada.'));
        tx.onerror=()=>{failure=tx.error;};
        try { tx.objectStore(name)[operation](...(method==='clear' ? [] : [item])); }
        catch(err) { failure=err; tx.abort(); }
      });
    };
  }
})();
"""
