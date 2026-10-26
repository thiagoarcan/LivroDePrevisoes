

window.App = window.App || {};

/* ==========================================================================
   1. CONFIGURAÇÕES E CONSTANTES
   ========================================================================== */
App.Config = {
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
    if (str.includes(';') || str.includes('"') || str.includes('\n') || str.includes('\r')) {
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
    this.unlock();
    if (!this.ctx) return;

    const gainNode = this.ctx.createGain();
    const masterVol = Math.max(0, Math.min(100, volumePercent)) / 100 * 0.3; // safe gain ceiling
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



/* ==========================================================================
   6. CAMADA DE REGRAS DE NEGÓCIO E SERVIÇOS OPERACIONAIS
   ========================================================================== */
App.Service = {
  
  // Obter configurações atuais
  getSettings: async function() {
    const item = await App.DB.get('settings', 'app_settings');
    return item ? item.value : { ...App.Config.DEFAULT_SETTINGS };
  },

  // Salvar configurações
  saveSettings: async function(newSettings) {
    await App.DB.update('settings', {
      key: 'app_settings',
      value: newSettings
    });
    return newSettings;
  },

  // --------------------------------------------------------------------------
  // CONSOLES
  // --------------------------------------------------------------------------
  saveConsole: async function(data) {
    const name = (data.name || '').trim();
    if (!name) throw new Error('O nome do console é obrigatório.');

    const allConsoles = await App.DB.getAll('consoles');
    const existing = allConsoles.find(c => App.Utils.cleanStr(c.name) === App.Utils.cleanStr(name) && c.id !== data.id);
    if (existing) throw new Error(`Já existe um console cadastrado com o nome "${name}".`);

    const now = new Date().toISOString();
    if (data.id) {
      const current = await App.DB.get('consoles', data.id);
      if (!current) throw new Error('Console não encontrado.');
      const updated = {
        ...current,
        name: name,
        updatedAt: now,
        version: (current.version || 1) + 1
      };
      await App.DB.update('consoles', updated);
      return updated;
    } else {
      const created = {
        id: App.Utils.uuid(),
        name: name,
        active: true,
        createdAt: now,
        updatedAt: now,
        version: 1,
        synchronizationStatus: 'local-only'
      };
      await App.DB.insert('consoles', created);
      return created;
    }
  },

  deleteConsole: async function(id) {
    // 1. Checar se existem dutos vinculados
    const allPipelines = await App.DB.getAll('pipelines');
    const linkedPipelines = allPipelines.filter(p => p.consoleId === id);

    // 2. Checar se existem eventos vinculados
    const allEvents = await App.DB.getAll('events');
    const linkedEvents = allEvents.filter(e => e.consoleId === id);

    if (linkedPipelines.length > 0 || linkedEvents.length > 0) {
      const reasons = [];
      if (linkedPipelines.length > 0) reasons.push(`${linkedPipelines.length} duto(s) vinculado(s)`);
      if (linkedEvents.length > 0) reasons.push(`${linkedEvents.length} evento(s) no histórico`);
      const error = new Error(`Não é possível excluir o console: possui ${reasons.join(' e ')}.`);
      error.isDependencyError = true;
      error.dependencies = reasons;
      error.targetStore = 'consoles';
      error.targetId = id;
      throw error;
    }

    await App.DB.delete('consoles', id);
    return true;
  },

  toggleConsoleActive: async function(id) {
    const item = await App.DB.get('consoles', id);
    if (!item) throw new Error('Console não encontrado.');
    item.active = !item.active;
    item.updatedAt = new Date().toISOString();
    item.version = (item.version || 1) + 1;
    await App.DB.update('consoles', item);
    return item;
  },

  // --------------------------------------------------------------------------
  // DUTOS (PIPELINES)
  // --------------------------------------------------------------------------
  savePipeline: async function(data) {
    const name = (data.name || '').trim();
    const consoleId = data.consoleId;
    const uoIds = Array.isArray(data.uoIds) ? data.uoIds : [];

    if (!name) throw new Error('O nome do duto é obrigatório.');
    if (!consoleId) throw new Error('O console responsável é obrigatório.');

    // REGRA FUNDAMENTAL: Todo duto deve possuir no mínimo 2 UOs vinculadas
    if (uoIds.length < 2) {
      throw new Error('O duto deve estar associado a no mínimo 2 Unidades Operacionais (UOs).');
    }

    const allPipelines = await App.DB.getAll('pipelines');
    const existing = allPipelines.find(p => p.consoleId === consoleId && App.Utils.cleanStr(p.name) === App.Utils.cleanStr(name) && p.id !== data.id);
    if (existing) throw new Error(`Já existe um duto com o nome "${name}" vinculado a este console.`);

    const now = new Date().toISOString();
    let pipelineId = data.id;

    if (pipelineId) {
      const current = await App.DB.get('pipelines', pipelineId);
      if (!current) throw new Error('Duto não encontrado.');
      const updated = {
        ...current,
        name: name,
        consoleId: consoleId,
        updatedAt: now,
        version: (current.version || 1) + 1
      };
      await App.DB.update('pipelines', updated);
    } else {
      pipelineId = App.Utils.uuid();
      const created = {
        id: pipelineId,
        name: name,
        consoleId: consoleId,
        active: true,
        createdAt: now,
        updatedAt: now,
        version: 1,
        synchronizationStatus: 'local-only'
      };
      await App.DB.insert('pipelines', created);
    }

    // Atualizar junction table pipelineOperationalUnits
    const allLinks = await App.DB.getAll('pipelineOperationalUnits');
    for (const link of allLinks) {
      if (link.pipelineId === pipelineId) {
        await App.DB.delete('pipelineOperationalUnits', link.id);
      }
    }

    for (const uoId of uoIds) {
      await App.DB.insert('pipelineOperationalUnits', {
        id: App.Utils.uuid(),
        pipelineId: pipelineId,
        uoId: uoId,
        createdAt: now,
        version: 1,
        synchronizationStatus: 'local-only'
      });
    }

    return await App.DB.get('pipelines', pipelineId);
  },

  deletePipeline: async function(id) {
    const allEvents = await App.DB.getAll('events');
    const linkedEvents = allEvents.filter(e => e.pipelineId === id);

    if (linkedEvents.length > 0) {
      const error = new Error(`Não é possível excluir o duto: possui ${linkedEvents.length} evento(s) associado(s).`);
      error.isDependencyError = true;
      error.dependencies = [`${linkedEvents.length} evento(s) no histórico`];
      error.targetStore = 'pipelines';
      error.targetId = id;
      throw error;
    }

    // Remover junction links
    const allLinks = await App.DB.getAll('pipelineOperationalUnits');
    for (const link of allLinks) {
      if (link.pipelineId === id) {
        await App.DB.delete('pipelineOperationalUnits', link.id);
      }
    }

    await App.DB.delete('pipelines', id);
    return true;
  },

  togglePipelineActive: async function(id) {
    const item = await App.DB.get('pipelines', id);
    if (!item) throw new Error('Duto não encontrado.');
    item.active = !item.active;
    item.updatedAt = new Date().toISOString();
    item.version = (item.version || 1) + 1;
    await App.DB.update('pipelines', item);
    return item;
  },

  // --------------------------------------------------------------------------
  // UNIDADES OPERACIONAIS (UOs)
  // --------------------------------------------------------------------------
  saveUO: async function(data) {
    const name = (data.name || '').trim();
    if (!name) throw new Error('O nome da UO é obrigatório.');

    const allUOs = await App.DB.getAll('operationalUnits');
    const existing = allUOs.find(u => App.Utils.cleanStr(u.name) === App.Utils.cleanStr(name) && u.id !== data.id);
    if (existing) throw new Error(`Já existe uma UO cadastrada com o nome "${name}".`);

    const now = new Date().toISOString();
    if (data.id) {
      const current = await App.DB.get('operationalUnits', data.id);
      if (!current) throw new Error('UO não encontrada.');
      const updated = {
        ...current,
        name: name,
        updatedAt: now,
        version: (current.version || 1) + 1
      };
      await App.DB.update('operationalUnits', updated);
      return updated;
    } else {
      const created = {
        id: App.Utils.uuid(),
        name: name,
        active: true,
        createdAt: now,
        updatedAt: now,
        version: 1,
        synchronizationStatus: 'local-only'
      };
      await App.DB.insert('operationalUnits', created);
      return created;
    }
  },

  // Cadastro em lote de UOs (separadas por vírgula, ponto e vírgula ou quebra de linha)
  saveUOBatch: async function(namesString) {
    if (!namesString || !namesString.trim()) {
      throw new Error('Informe o nome de ao menos uma Unidade Operacional (UO).');
    }
    const rawNames = namesString.split(/[,;\n\r]+/).map(s => s.trim()).filter(Boolean);
    if (rawNames.length === 0) {
      throw new Error('Nenhum nome de UO válido identificado.');
    }
    const allUOs = await App.DB.getAll('operationalUnits');
    const createdList = [];
    const existingList = [];

    for (const name of rawNames) {
      const match = allUOs.find(u => App.Utils.cleanStr(u.name) === App.Utils.cleanStr(name));
      if (match) {
        if (!match.active) {
          match.active = true;
          match.updatedAt = new Date().toISOString();
          await App.DB.update('operationalUnits', match);
        }
        existingList.push(match);
      } else {
        const created = await this.saveUO({ name: name });
        createdList.push(created);
        allUOs.push(created);
      }
    }
    return { created: createdList, existing: existingList, all: [...createdList, ...existingList] };
  },

  deleteUO: async function(id) {
    const allLinks = await App.DB.getAll('pipelineOperationalUnits');
    const linkedPipelines = allLinks.filter(l => l.uoId === id);

    const allTypes = await App.DB.getAll('equipmentTypes');
    const linkedTypes = allTypes.filter(t => t.uoId === id);

    const allTags = await App.DB.getAll('equipmentTags');
    const linkedTags = allTags.filter(t => t.uoId === id);

    const allEvents = await App.DB.getAll('events');
    const linkedEvents = allEvents.filter(e => e.uoId === id);

    if (linkedPipelines.length > 0 || linkedTypes.length > 0 || linkedTags.length > 0 || linkedEvents.length > 0) {
      const reasons = [];
      if (linkedPipelines.length > 0) reasons.push(`${linkedPipelines.length} duto(s) associado(s)`);
      if (linkedTypes.length > 0) reasons.push(`${linkedTypes.length} tipo(s) de equipamento`);
      if (linkedTags.length > 0) reasons.push(`${linkedTags.length} TAG(s) cadastrado(s)`);
      if (linkedEvents.length > 0) reasons.push(`${linkedEvents.length} evento(s) no histórico`);
      
      const error = new Error(`Não é possível excluir a UO: possui dependências ativas.`);
      error.isDependencyError = true;
      error.dependencies = reasons;
      error.targetStore = 'operationalUnits';
      error.targetId = id;
      throw error;
    }

    await App.DB.delete('operationalUnits', id);
    return true;
  },

  toggleUOActive: async function(id) {
    const item = await App.DB.get('operationalUnits', id);
    if (!item) throw new Error('UO não encontrada.');
    item.active = !item.active;
    item.updatedAt = new Date().toISOString();
    item.version = (item.version || 1) + 1;
    await App.DB.update('operationalUnits', item);
    return item;
  },

  // --------------------------------------------------------------------------
  // TIPOS DE EQUIPAMENTOS
  // --------------------------------------------------------------------------
  saveEquipmentType: async function(data) {
    const name = (data.name || '').trim();
    const uoId = data.uoId;
    if (!name) throw new Error('O nome do tipo de equipamento é obrigatório.');
    if (!uoId) throw new Error('A UO vinculada é obrigatória.');

    const allTypes = await App.DB.getAll('equipmentTypes');
    const existing = allTypes.find(t => t.uoId === uoId && App.Utils.cleanStr(t.name) === App.Utils.cleanStr(name) && t.id !== data.id);
    if (existing) throw new Error(`Já existe um tipo "${name}" cadastrado nesta UO.`);

    const now = new Date().toISOString();
    if (data.id) {
      const current = await App.DB.get('equipmentTypes', data.id);
      if (!current) throw new Error('Tipo de equipamento não encontrado.');
      const updated = {
        ...current,
        name: name,
        uoId: uoId,
        updatedAt: now,
        version: (current.version || 1) + 1
      };
      await App.DB.update('equipmentTypes', updated);
      return updated;
    } else {
      const created = {
        id: App.Utils.uuid(),
        name: name,
        uoId: uoId,
        active: true,
        createdAt: now,
        updatedAt: now,
        version: 1,
        synchronizationStatus: 'local-only'
      };
      await App.DB.insert('equipmentTypes', created);
      return created;
    }
  },

  deleteEquipmentType: async function(id) {
    const allTags = await App.DB.getAll('equipmentTags');
    const linkedTags = allTags.filter(t => t.equipmentTypeId === id);

    const allEvents = await App.DB.getAll('events');
    const linkedEvents = allEvents.filter(e => e.equipmentTypeId === id);

    if (linkedTags.length > 0 || linkedEvents.length > 0) {
      const reasons = [];
      if (linkedTags.length > 0) reasons.push(`${linkedTags.length} TAG(s) cadastrado(s)`);
      if (linkedEvents.length > 0) reasons.push(`${linkedEvents.length} evento(s) no histórico`);
      const error = new Error('Não é possível excluir o tipo de equipamento.');
      error.isDependencyError = true;
      error.dependencies = reasons;
      error.targetStore = 'equipmentTypes';
      error.targetId = id;
      throw error;
    }

    await App.DB.delete('equipmentTypes', id);
    return true;
  },

  toggleEquipmentTypeActive: async function(id) {
    const item = await App.DB.get('equipmentTypes', id);
    if (!item) throw new Error('Tipo não encontrado.');
    item.active = !item.active;
    item.updatedAt = new Date().toISOString();
    item.version = (item.version || 1) + 1;
    await App.DB.update('equipmentTypes', item);
    return item;
  },

  // --------------------------------------------------------------------------
  // TAGS DE EQUIPAMENTOS (REGRA GLOBAL DE UNICIDADE POR UO)
  // --------------------------------------------------------------------------
  saveEquipmentTag: async function(data) {
    const tag = (data.tag || '').trim();
    const uoId = data.uoId;
    const equipmentTypeId = data.equipmentTypeId;

    if (!tag) throw new Error('O código do TAG é obrigatório.');
    if (!uoId) throw new Error('A UO é obrigatória.');
    if (!equipmentTypeId) throw new Error('O tipo de equipamento é obrigatório.');

    // REGRA FUNDAMENTAL: Cada TAG pertence exclusivamente a UMA UO em todo o sistema!
    const allTags = await App.DB.getAll('equipmentTags');
    const existingGlobal = allTags.find(t => App.Utils.cleanStr(t.tag) === App.Utils.cleanStr(tag) && t.id !== data.id);

    if (existingGlobal) {
      if (existingGlobal.uoId !== uoId) {
        const uoList = await App.DB.getAll('operationalUnits');
        const conflictUO = uoList.find(u => u.id === existingGlobal.uoId);
        const conflictUOName = conflictUO ? conflictUO.name : 'outra UO';
        throw new Error(`O TAG ${tag} já está cadastrado na UO ${conflictUOName} e não pode ser associado a outra UO.`);
      } else {
        throw new Error(`O TAG ${tag} já está cadastrado nesta UO.`);
      }
    }

    const now = new Date().toISOString();
    if (data.id) {
      const current = await App.DB.get('equipmentTags', data.id);
      if (!current) throw new Error('TAG não encontrado.');
      const updated = {
        ...current,
        tag: tag,
        uoId: uoId,
        equipmentTypeId: equipmentTypeId,
        updatedAt: now,
        version: (current.version || 1) + 1
      };
      await App.DB.update('equipmentTags', updated);
      return updated;
    } else {
      const created = {
        id: App.Utils.uuid(),
        tag: tag,
        uoId: uoId,
        equipmentTypeId: equipmentTypeId,
        active: true,
        createdAt: now,
        updatedAt: now,
        version: 1,
        synchronizationStatus: 'local-only'
      };
      await App.DB.insert('equipmentTags', created);
      return created;
    }
  },

  deleteEquipmentTag: async function(id) {
    const allEvents = await App.DB.getAll('events');
    const linkedEvents = allEvents.filter(e => e.tagId === id);

    if (linkedEvents.length > 0) {
      const error = new Error(`Não é possível excluir o TAG: possui ${linkedEvents.length} evento(s) no histórico.`);
      error.isDependencyError = true;
      error.dependencies = [`${linkedEvents.length} evento(s) no histórico`];
      error.targetStore = 'equipmentTags';
      error.targetId = id;
      throw error;
    }

    await App.DB.delete('equipmentTags', id);
    return true;
  },

  toggleEquipmentTagActive: async function(id) {
    const item = await App.DB.get('equipmentTags', id);
    if (!item) throw new Error('TAG não encontrado.');
    item.active = !item.active;
    item.updatedAt = new Date().toISOString();
    item.version = (item.version || 1) + 1;
    await App.DB.update('equipmentTags', item);
    return item;
  },

  // --------------------------------------------------------------------------
  // EVENTOS (PREVISÕES OPERACIONAIS)
  // --------------------------------------------------------------------------
  saveEvent: async function(data) {
    // Validações obrigatórias
    if (!data.consoleId) throw new Error('O Console é obrigatório.');
    if (!data.pipelineId) throw new Error('O Duto é obrigatório.');
    if (!data.uoId) throw new Error('A UO é obrigatória.');
    if (!data.scheduledDate) throw new Error('A data do evento é obrigatória.');
    if (!data.scheduledTime) throw new Error('A hora do evento é obrigatória.');
    if (!data.description || !data.description.trim()) throw new Error('A descrição da atividade é obrigatória.');

    const leadTime = parseInt(data.alarmMinutesBefore, 10);
    if (data.hasAlarm && (isNaN(leadTime) || leadTime < 0)) {
      throw new Error('A antecedência do alarme deve ser igual ou superior a 0 minutos.');
    }

    // Montar scheduledAt em timestamp local confiável
    const [year, month, day] = data.scheduledDate.split('-').map(Number);
    const [hours, minutes] = data.scheduledTime.split(':').map(Number);
    const scheduledDateObj = new Date(year, month - 1, day, hours, minutes, 0, 0);
    if (isNaN(scheduledDateObj.getTime())) {
      throw new Error('Data ou hora inválida.');
    }
    const scheduledAt = scheduledDateObj.toISOString();

    const settings = await this.getSettings();
    const localUser = settings.localUserName || 'Usuário local';
    const now = new Date().toISOString();

    if (data.id) {
      // Edição
      const current = await App.DB.get('events', data.id);
      if (!current) throw new Error('Evento não encontrado para edição.');

      // Registrar campos alterados no histórico
      const changes = [];
      if (current.scheduledDate !== data.scheduledDate || current.scheduledTime !== data.scheduledTime) {
        changes.push(`Horário alterado de ${App.Utils.formatDateTime(current.scheduledDate, current.scheduledTime)} para ${App.Utils.formatDateTime(data.scheduledDate, data.scheduledTime)}`);
      }
      if (current.description !== data.description) {
        changes.push(`Descrição alterada`);
      }
      if (current.hasAlarm !== data.hasAlarm) {
        changes.push(data.hasAlarm ? 'Alarme ativado' : 'Alarme desativado');
      }

      const updated = {
        ...current,
        consoleId: data.consoleId,
        pipelineId: data.pipelineId,
        uoId: data.uoId,
        equipmentTypeId: data.equipmentTypeId || null,
        tagId: data.tagId || null,
        scheduledDate: data.scheduledDate,
        scheduledTime: data.scheduledTime,
        scheduledAt: scheduledAt,
        description: data.description.trim(),
        notes: (data.notes || '').trim(),
        stylusDrawing: data.stylusDrawing !== undefined ? data.stylusDrawing : (current.stylusDrawing || null),
        priority: data.priority || 'Normal',
        hasAlarm: !!data.hasAlarm,
        useDefaultAlarmSettings: !!data.useDefaultAlarmSettings,
        alarmMinutesBefore: leadTime || 0,
        alarmAudio: data.alarmAudio !== undefined ? !!data.alarmAudio : true,
        alarmVisual: data.alarmVisual !== undefined ? !!data.alarmVisual : true,
        alarmNotification: !!data.alarmNotification,
        alarmRepeat: !!data.alarmRepeat,
        alarmRepeatInterval: parseInt(data.alarmRepeatInterval, 10) || 2,
        alarmMaxRepeats: parseInt(data.alarmMaxRepeats, 10) || 5,
        updatedAt: now,
        version: (current.version || 1) + 1
      };

      // Se a data mudou, recalcula alarme
      if (current.scheduledAt !== scheduledAt) {
        updated.alarmState = 'idle';
        updated.alarmSnoozedUntil = null;
      }

      await App.DB.update('events', updated);

      // Registrar no histórico
      await this.logEventHistory({
        eventId: updated.id,
        action: 'edicao',
        description: changes.length > 0 ? changes.join('; ') : 'Evento atualizado',
        previousValue: JSON.stringify(current),
        newValue: JSON.stringify(updated),
        localUser: localUser
      });

      return updated;
    } else {
      // Criação
      const newEvent = {
        id: App.Utils.uuid(),
        consoleId: data.consoleId,
        pipelineId: data.pipelineId,
        uoId: data.uoId,
        equipmentTypeId: data.equipmentTypeId || null,
        tagId: data.tagId || null,
        scheduledDate: data.scheduledDate,
        scheduledTime: data.scheduledTime,
        scheduledAt: scheduledAt,
        description: data.description.trim(),
        notes: (data.notes || '').trim(),
        stylusDrawing: data.stylusDrawing || null,
        priority: data.priority || 'Normal',
        status: 'pendente',
        hasAlarm: !!data.hasAlarm,
        useDefaultAlarmSettings: !!data.useDefaultAlarmSettings,
        alarmMinutesBefore: leadTime || 0,
        alarmAudio: data.alarmAudio !== undefined ? !!data.alarmAudio : true,
        alarmVisual: data.alarmVisual !== undefined ? !!data.alarmVisual : true,
        alarmNotification: !!data.alarmNotification,
        alarmRepeat: !!data.alarmRepeat,
        alarmRepeatInterval: parseInt(data.alarmRepeatInterval, 10) || 2,
        alarmMaxRepeats: parseInt(data.alarmMaxRepeats, 10) || 5,
        alarmState: 'idle',
        alarmSnoozedUntil: null,
        alarmTriggerCount: 0,
        lastAlarmTriggeredAt: null,
        completedAt: null,
        completedTimeDiffMinutes: null,
        completionNote: '',
        active: true,
        createdAt: now,
        updatedAt: now,
        version: 1,
        synchronizationStatus: 'local-only'
      };

      await App.DB.insert('events', newEvent);

      // Registrar auditoria de criação
      await this.logEventHistory({
        eventId: newEvent.id,
        action: 'criacao',
        description: `Previsão criada para ${App.Utils.formatDateTime(newEvent.scheduledDate, newEvent.scheduledTime)}`,
        previousValue: null,
        newValue: JSON.stringify(newEvent),
        localUser: localUser
      });

      return newEvent;
    }
  },

  completeEvent: async function(id, completionNote = '') {
    const event = await App.DB.get('events', id);
    if (!event) throw new Error('Evento não encontrado.');

    const now = new Date();
    const completedAt = now.toISOString();
    const scheduledTime = new Date(event.scheduledAt).getTime();
    const actualTime = now.getTime();
    const diffMinutes = (actualTime - scheduledTime) / 60000;

    const settings = await this.getSettings();
    const localUser = settings.localUserName || 'Usuário local';

    event.status = 'concluido';
    event.completedAt = completedAt;
    event.completedTimeDiffMinutes = diffMinutes;
    event.completionNote = (completionNote || '').trim();
    event.alarmState = 'acknowledged'; // cancela qualquer alarme
    event.updatedAt = completedAt;
    event.version = (event.version || 1) + 1;

    await App.DB.update('events', event);

    await this.logEventHistory({
      eventId: event.id,
      action: 'conclusao',
      description: `Evento concluído (${App.Utils.formatDiffMinutes(diffMinutes)}). ${event.completionNote ? 'Nota: ' + event.completionNote : ''}`,
      previousValue: 'pendente',
      newValue: 'concluido',
      localUser: localUser
    });

    return event;
  },

  reopenEvent: async function(id, newDate, newTime) {
    const event = await App.DB.get('events', id);
    if (!event) throw new Error('Evento não encontrado.');

    const settings = await this.getSettings();
    const localUser = settings.localUserName || 'Usuário local';
    const now = new Date().toISOString();

    const previousCompletionDetails = {
      completedAt: event.completedAt,
      diffMinutes: event.completedTimeDiffMinutes,
      completionNote: event.completionNote
    };

    event.status = 'pendente';
    event.completedAt = null;
    event.completedTimeDiffMinutes = null;
    event.alarmState = 'idle';
    event.alarmSnoozedUntil = null;
    event.updatedAt = now;
    event.version = (event.version || 1) + 1;

    // Se nova data/hora fornecida
    if (newDate && newTime) {
      event.scheduledDate = newDate;
      event.scheduledTime = newTime;
      const [year, month, day] = newDate.split('-').map(Number);
      const [hours, minutes] = newTime.split(':').map(Number);
      event.scheduledAt = new Date(year, month - 1, day, hours, minutes, 0, 0).toISOString();
    }

    await App.DB.update('events', event);

    await this.logEventHistory({
      eventId: event.id,
      action: 'reabertura',
      description: `Evento reaberto. Dados de conclusão anterior preservados no histórico. Novo horário previsto: ${App.Utils.formatDateTime(event.scheduledDate, event.scheduledTime)}`,
      previousValue: JSON.stringify(previousCompletionDetails),
      newValue: 'pendente',
      localUser: localUser
    });

    return event;
  },

  getCloneDataForEvent: async function(id) {
    const event = await App.DB.get('events', id);
    if (!event) throw new Error('Evento não encontrado para duplicação.');

    const targetDate = new Date(Date.now() + 30 * 60000);
    const y = targetDate.getFullYear();
    const m = String(targetDate.getMonth() + 1).padStart(2, '0');
    const d = String(targetDate.getDate()).padStart(2, '0');
    const hh = String(targetDate.getHours()).padStart(2, '0');
    const mm = String(targetDate.getMinutes()).padStart(2, '0');

    return {
      consoleId: event.consoleId,
      pipelineId: event.pipelineId,
      uoId: event.uoId,
      equipmentTypeId: event.equipmentTypeId,
      tagId: event.tagId,
      scheduledDate: `${y}-${m}-${d}`,
      scheduledTime: `${hh}:${mm}`,
      priority: event.priority || 'Normal',
      description: event.description,
      notes: event.notes || '',
      hasAlarm: event.hasAlarm,
      useDefaultAlarmSettings: event.useDefaultAlarmSettings,
      alarmMinutesBefore: event.alarmMinutesBefore,
      alarmAudio: event.alarmAudio,
      alarmVisual: event.alarmVisual,
      alarmNotification: event.alarmNotification,
      alarmRepeat: event.alarmRepeat,
      alarmRepeatInterval: event.alarmRepeatInterval,
      alarmMaxRepeats: event.alarmMaxRepeats,
      stylusDrawing: event.stylusDrawing || null
    };
  },

  deleteEvent: async function(id) {
    const event = await App.DB.get('events', id);
    if (!event) throw new Error('Evento não encontrado.');

    // Excluir histórico associado
    const allHistory = await App.DB.getAll('eventHistory');
    for (const h of allHistory) {
      if (h.eventId === id) {
        await App.DB.delete('eventHistory', h.id);
      }
    }

    await App.DB.delete('events', id);
    return true;
  },

  snoozeAlarm: async function(eventId, minutes) {
    const event = await App.DB.get('events', eventId);
    if (!event) throw new Error('Evento não encontrado.');

    const snoozeMins = parseInt(minutes, 10) || 5;
    const snoozeUntil = Date.now() + (snoozeMins * 60000);

    const settings = await this.getSettings();
    const localUser = settings.localUserName || 'Usuário local';

    event.alarmState = 'snoozed';
    event.alarmSnoozedUntil = snoozeUntil;
    event.updatedAt = new Date().toISOString();
    await App.DB.update('events', event);

    await this.logEventHistory({
      eventId: event.id,
      action: 'adiamento',
      description: `Alarme adiado por ${snoozeMins} minutos (novo disparo previsto para ${App.Utils.formatTime(new Date(snoozeUntil))})`,
      previousValue: 'disparado',
      newValue: 'adiado',
      localUser: localUser
    });

    return event;
  },

  acknowledgeAlarm: async function(eventId) {
    const event = await App.DB.get('events', eventId);
    if (!event) throw new Error('Evento não encontrado.');

    const settings = await this.getSettings();
    const localUser = settings.localUserName || 'Usuário local';

    event.alarmState = 'acknowledged';
    event.updatedAt = new Date().toISOString();
    await App.DB.update('events', event);

    await this.logEventHistory({
      eventId: event.id,
      action: 'reconhecimento',
      description: 'Alarme reconhecido pelo controlador. Som e repetições interrompidos.',
      previousValue: 'disparado',
      newValue: 'reconhecido',
      localUser: localUser
    });

    return event;
  },

  logEventHistory: async function(record) {
    const item = {
      id: App.Utils.uuid(),
      eventId: record.eventId,
      action: record.action,
      timestamp: new Date().toISOString(),
      description: record.description || '',
      previousValue: record.previousValue || null,
      newValue: record.newValue || null,
      localUser: record.localUser || 'Usuário local'
    };
    await App.DB.insert('eventHistory', item);
    return item;
  },

  // --------------------------------------------------------------------------
  // FAIXAS DE CORES E VALIDAÇÃO DE NÃO-SOBREPOSIÇÃO
  // --------------------------------------------------------------------------
  getColorRanges: async function() {
    const ranges = await App.DB.getAll('colorRanges');
    return ranges.sort((a, b) => a.minMinutes - b.minMinutes);
  },

  validateColorRanges: function(ranges) {
    if (!ranges || ranges.length === 0) {
      throw new Error('Deve haver pelo menos uma faixa de cor cadastrada.');
    }

    // Ordenar por limite inicial crescente
    const sorted = [...ranges].sort((a, b) => a.minMinutes - b.minMinutes);

    // 1. Cada faixa individual deve ter min < max
    for (const r of sorted) {
      if (r.minMinutes >= r.maxMinutes) {
        throw new Error(`A faixa "${r.name}" possui limite final (${r.maxMinutes} min) menor ou igual ao inicial (${r.minMinutes} min).`);
      }
    }

    // 2. A primeira faixa deve iniciar em 0 minutos
    if (sorted[0].minMinutes !== 0) {
      throw new Error(`A primeira faixa ("${sorted[0].name}") deve iniciar exatamente em 0 minutos.`);
    }

    // 3. Verificar lacunas e sobreposições contíguas
    for (let i = 1; i < sorted.length; i++) {
      const prev = sorted[i - 1];
      const curr = sorted[i];

      if (curr.minMinutes < prev.maxMinutes) {
        throw new Error(`Existe sobreposição entre os intervalos das faixas "${prev.name}" (termina em ${prev.maxMinutes} min) e "${curr.name}" (inicia em ${curr.minMinutes} min).`);
      }

      if (curr.minMinutes > prev.maxMinutes) {
        throw new Error(`Existe uma lacuna entre os intervalos das faixas "${prev.name}" (termina em ${prev.maxMinutes} min) e "${curr.name}" (inicia em ${curr.minMinutes} min).`);
      }
    }

    return sorted;
  },

  saveColorRange: async function(data) {
    const name = (data.name || '').trim();
    const color = (data.color || '').trim();
    const minM = parseInt(data.minMinutes, 10);
    const maxM = parseInt(data.maxMinutes, 10);
    const priority = parseInt(data.priority, 10) || 1;

    if (!name) throw new Error('O nome da faixa é obrigatório.');
    if (!color) throw new Error('A cor da faixa é obrigatória.');
    if (isNaN(minM) || isNaN(maxM) || minM < 0) {
      throw new Error('Limites inicial e final devem ser números válidos maiores ou iguais a zero.');
    }

    const currentRanges = await App.DB.getAll('colorRanges');
    let candidateRanges;

    if (data.id) {
      candidateRanges = currentRanges.map(r => r.id === data.id ? {
        ...r,
        name: name,
        color: color,
        minMinutes: minM,
        maxMinutes: maxM,
        priority: priority,
        blink: !!data.blink,
        sound: !!data.sound,
        active: true
      } : r);
    } else {
      const newRange = {
        id: App.Utils.uuid(),
        name: name,
        color: color,
        minMinutes: minM,
        maxMinutes: maxM,
        priority: priority,
        blink: !!data.blink,
        sound: !!data.sound,
        active: true
      };
      candidateRanges = [...currentRanges, newRange];
    }

    // Valida a consistência do conjunto completo antes de salvar
    this.validateColorRanges(candidateRanges);

    // Salvar todas as faixas validadas
    await App.DB.clear('colorRanges');
    for (const r of candidateRanges) {
      await App.DB.insert('colorRanges', r);
    }

    return true;
  },

  deleteColorRange: async function(id) {
    const currentRanges = await App.DB.getAll('colorRanges');
    if (currentRanges.length <= 1) {
      throw new Error('O sistema deve manter pelo menos uma faixa de classificação ativa.');
    }

    const remaining = currentRanges.filter(r => r.id !== id);
    // Validação de lacunas após remoção
    this.validateColorRanges(remaining);

    await App.DB.delete('colorRanges', id);
    return true;
  },

  resetColorRanges: async function() {
    await App.DB.clear('colorRanges');
    for (const r of App.Config.DEFAULT_COLOR_RANGES) {
      await App.DB.insert('colorRanges', r);
    }
    return true;
  },

  normalizeRangeKey: function(rawId, name) {
    const idStr = (rawId || '').toLowerCase();
    const nameStr = (name || '').toLowerCase();
    if (idStr.includes('critico') || nameStr.includes('crítico') || nameStr.includes('critico')) return 'critico';
    if (idStr.includes('urgente') || nameStr.includes('urgente')) return 'urgente';
    if (idStr.includes('atencao') || nameStr.includes('atenção') || nameStr.includes('atencao')) return 'atencao';
    if (idStr.includes('monitor') || nameStr.includes('monitor')) return 'monitoramento';
    if (idStr.includes('normal') || nameStr.includes('normal')) return 'normal';
    return rawId || 'normal';
  },

  getRangeIcon: function(normKey) {
    switch (normKey) {
      case 'atrasado': return '⏱';
      case 'critico': return '⚠';
      case 'urgente': return '⚡';
      case 'atencao': return '🔔';
      case 'monitoramento': return '👁';
      default: return '●';
    }
  },

  // Classificar um evento na faixa adequada
  classifyEvent: function(event, colorRanges) {
    const now = Date.now();
    const scheduledTime = new Date(event.scheduledAt).getTime();
    const diffMs = scheduledTime - now;
    const diffMinutes = diffMs / 60000;

    // Regra: "Atrasado" é tratado separadamente das faixas de tempo futuro
    if (diffMs < 0) {
      return {
        key: 'atrasado',
        rawKey: 'atrasado',
        icon: '⏱',
        name: 'Atrasado',
        color: '#991b1b',
        bgColor: 'var(--status-overdue-bg)',
        borderColor: 'var(--status-overdue-border)',
        textColor: 'var(--status-overdue-text)',
        blink: true,
        sound: true,
        priority: 0,
        isOverdue: true
      };
    }

    // Buscar na cadeia de faixas futuras
    const activeRanges = [...colorRanges].sort((a, b) => a.minMinutes - b.minMinutes);
    for (const r of activeRanges) {
      if (diffMinutes >= r.minMinutes && diffMinutes < r.maxMinutes) {
        const normKey = this.normalizeRangeKey(r.id, r.name);
        return {
          key: normKey,
          rawKey: r.id,
          icon: this.getRangeIcon(normKey),
          name: r.name,
          color: r.color,
          bgColor: `rgba(${App.Service.hexToRgb(r.color)}, 0.15)`,
          borderColor: r.color,
          textColor: r.color,
          blink: r.blink,
          sound: r.sound,
          priority: r.priority,
          isOverdue: false
        };
      }
    }

    // Fallback caso ultrapasse o maior limite
    const last = activeRanges[activeRanges.length - 1];
    const normKey = this.normalizeRangeKey(last.id, last.name);
    return {
      key: normKey,
      rawKey: last.id,
      icon: this.getRangeIcon(normKey),
      name: last.name,
      color: last.color,
      bgColor: `rgba(${App.Service.hexToRgb(last.color)}, 0.15)`,
      borderColor: last.color,
      textColor: last.color,
      blink: last.blink,
      sound: last.sound,
      priority: last.priority,
      isOverdue: false
    };
  },

  hexToRgb: function(hex) {
    let c = hex.replace('#', '');
    if (c.length === 3) c = c.split('').map(x => x + x).join('');
    const num = parseInt(c, 16);
    return `${(num >> 16) & 255}, ${(num >> 8) & 255}, ${num & 255}`;
  },

  // --------------------------------------------------------------------------
  // DADOS DE DEMONSTRAÇÃO
  // --------------------------------------------------------------------------
  loadDemoData: async function() {
    const now = new Date();
    const isoNow = now.toISOString();

    // 1. Garantir Consoles C04, C08, C10
    const consoles = await App.DB.getAll('consoles');
    let c04 = consoles.find(c => c.name === 'C04');
    let c08 = consoles.find(c => c.name === 'C08');
    let c10 = consoles.find(c => c.name === 'C10');

    if (!c04) {
      c04 = { id: App.Utils.uuid(), name: 'C04', active: true, createdAt: isoNow, updatedAt: isoNow, version: 1, synchronizationStatus: 'local-only' };
      await App.DB.insert('consoles', c04);
    }
    if (!c08) {
      c08 = { id: App.Utils.uuid(), name: 'C08', active: true, createdAt: isoNow, updatedAt: isoNow, version: 1, synchronizationStatus: 'local-only' };
      await App.DB.insert('consoles', c08);
    }
    if (!c10) {
      c10 = { id: App.Utils.uuid(), name: 'C10', active: true, createdAt: isoNow, updatedAt: isoNow, version: 1, synchronizationStatus: 'local-only' };
      await App.DB.insert('consoles', c10);
    }

    // 2. Criar UOs
    const uoRefap = { id: App.Utils.uuid(), name: 'REFAP', active: true, createdAt: isoNow, updatedAt: isoNow, version: 1, synchronizationStatus: 'local-only' };
    const uoTedep = { id: App.Utils.uuid(), name: 'TEDEP', active: true, createdAt: isoNow, updatedAt: isoNow, version: 1, synchronizationStatus: 'local-only' };
    const uoReplan = { id: App.Utils.uuid(), name: 'REPLAN', active: true, createdAt: isoNow, updatedAt: isoNow, version: 1, synchronizationStatus: 'local-only' };
    const uoTebar = { id: App.Utils.uuid(), name: 'TEBAR', active: true, createdAt: isoNow, updatedAt: isoNow, version: 1, synchronizationStatus: 'local-only' };

    await App.DB.insert('operationalUnits', uoRefap);
    await App.DB.insert('operationalUnits', uoTedep);
    await App.DB.insert('operationalUnits', uoReplan);
    await App.DB.insert('operationalUnits', uoTebar);

    // 3. Criar Dutos com pelo menos 2 UOs cada
    const dutoOscan = { id: App.Utils.uuid(), name: 'OSCAN', consoleId: c04.id, active: true, createdAt: isoNow, updatedAt: isoNow, version: 1, synchronizationStatus: 'local-only' };
    const dutoOsbra = { id: App.Utils.uuid(), name: 'OSBRA', consoleId: c08.id, active: true, createdAt: isoNow, updatedAt: isoNow, version: 1, synchronizationStatus: 'local-only' };
    const dutoDtcs = { id: App.Utils.uuid(), name: 'DTCS', consoleId: c10.id, active: true, createdAt: isoNow, updatedAt: isoNow, version: 1, synchronizationStatus: 'local-only' };

    await App.DB.insert('pipelines', dutoOscan);
    await App.DB.insert('pipelines', dutoOsbra);
    await App.DB.insert('pipelines', dutoDtcs);

    // Links duto <-> UOs
    await App.DB.insert('pipelineOperationalUnits', { id: App.Utils.uuid(), pipelineId: dutoOscan.id, uoId: uoRefap.id, createdAt: isoNow, version: 1, synchronizationStatus: 'local-only' });
    await App.DB.insert('pipelineOperationalUnits', { id: App.Utils.uuid(), pipelineId: dutoOscan.id, uoId: uoTedep.id, createdAt: isoNow, version: 1, synchronizationStatus: 'local-only' });

    await App.DB.insert('pipelineOperationalUnits', { id: App.Utils.uuid(), pipelineId: dutoOsbra.id, uoId: uoReplan.id, createdAt: isoNow, version: 1, synchronizationStatus: 'local-only' });
    await App.DB.insert('pipelineOperationalUnits', { id: App.Utils.uuid(), pipelineId: dutoOsbra.id, uoId: uoTebar.id, createdAt: isoNow, version: 1, synchronizationStatus: 'local-only' });

    await App.DB.insert('pipelineOperationalUnits', { id: App.Utils.uuid(), pipelineId: dutoDtcs.id, uoId: uoReplan.id, createdAt: isoNow, version: 1, synchronizationStatus: 'local-only' });
    await App.DB.insert('pipelineOperationalUnits', { id: App.Utils.uuid(), pipelineId: dutoDtcs.id, uoId: uoTedep.id, createdAt: isoNow, version: 1, synchronizationStatus: 'local-only' });

    // 4. Tipos de Equipamentos por UO
    const tipoTanqueRefap = { id: App.Utils.uuid(), name: 'Tanque', uoId: uoRefap.id, active: true, createdAt: isoNow, updatedAt: isoNow, version: 1, synchronizationStatus: 'local-only' };
    const tipoBombaRefap = { id: App.Utils.uuid(), name: 'Bomba', uoId: uoRefap.id, active: true, createdAt: isoNow, updatedAt: isoNow, version: 1, synchronizationStatus: 'local-only' };
    const tipoEsferaReplan = { id: App.Utils.uuid(), name: 'Esfera', uoId: uoReplan.id, active: true, createdAt: isoNow, updatedAt: isoNow, version: 1, synchronizationStatus: 'local-only' };
    const tipoValvulaTedep = { id: App.Utils.uuid(), name: 'Válvula de Controle', uoId: uoTedep.id, active: true, createdAt: isoNow, updatedAt: isoNow, version: 1, synchronizationStatus: 'local-only' };

    await App.DB.insert('equipmentTypes', tipoTanqueRefap);
    await App.DB.insert('equipmentTypes', tipoBombaRefap);
    await App.DB.insert('equipmentTypes', tipoEsferaReplan);
    await App.DB.insert('equipmentTypes', tipoValvulaTedep);

    // 5. TAGs (Cada um em apenas uma UO)
    const tagTq804 = { id: App.Utils.uuid(), tag: 'TQ-804', uoId: uoRefap.id, equipmentTypeId: tipoTanqueRefap.id, active: true, createdAt: isoNow, updatedAt: isoNow, version: 1, synchronizationStatus: 'local-only' };
    const tagBb101A = { id: App.Utils.uuid(), tag: 'BB-101A', uoId: uoRefap.id, equipmentTypeId: tipoBombaRefap.id, active: true, createdAt: isoNow, updatedAt: isoNow, version: 1, synchronizationStatus: 'local-only' };
    const tagEs201 = { id: App.Utils.uuid(), tag: 'ES-201', uoId: uoReplan.id, equipmentTypeId: tipoEsferaReplan.id, active: true, createdAt: isoNow, updatedAt: isoNow, version: 1, synchronizationStatus: 'local-only' };
    const tagPcv301 = { id: App.Utils.uuid(), tag: 'PCV-301', uoId: uoTedep.id, equipmentTypeId: tipoValvulaTedep.id, active: true, createdAt: isoNow, updatedAt: isoNow, version: 1, synchronizationStatus: 'local-only' };

    await App.DB.insert('equipmentTags', tagTq804);
    await App.DB.insert('equipmentTags', tagBb101A);
    await App.DB.insert('equipmentTags', tagEs201);
    await App.DB.insert('equipmentTags', tagPcv301);

    // 6. Eventos Operacionais Demonstrativos
    const helperMakeDate = (offsetMinutes) => {
      const d = new Date(now.getTime() + offsetMinutes * 60000);
      const y = d.getFullYear();
      const m = String(d.getMonth() + 1).padStart(2, '0');
      const day = String(d.getDate()).padStart(2, '0');
      const h = String(d.getHours()).padStart(2, '0');
      const min = String(d.getMinutes()).padStart(2, '0');
      return {
        date: `${y}-${m}-${day}`,
        time: `${h}:${min}`,
        iso: d.toISOString()
      };
    };

    // Evento 1: Atrasado há 12 min
    const tOverdue = helperMakeDate(-12);
    await this.saveEvent({
      consoleId: c04.id,
      pipelineId: dutoOscan.id,
      uoId: uoRefap.id,
      equipmentTypeId: tipoBombaRefap.id,
      tagId: tagBb101A.id,
      scheduledDate: tOverdue.date,
      scheduledTime: tOverdue.time,
      description: 'Verificar alinhamento e término de partida da bomba BB-101A',
      notes: 'Confirmar pressão de sucção e vazão nominal.',
      priority: 'Crítica',
      hasAlarm: true,
      alarmMinutesBefore: 15
    });

    // Evento 2: Crítico (faltam 8 min)
    const tCrit = helperMakeDate(8);
    await this.saveEvent({
      consoleId: c04.id,
      pipelineId: dutoOscan.id,
      uoId: uoRefap.id,
      equipmentTypeId: tipoTanqueRefap.id,
      tagId: tagTq804.id,
      scheduledDate: tCrit.date,
      scheduledTime: tCrit.time,
      description: 'Verificar o término do recebimento de MGO no TQ-804',
      notes: 'Monitorar nível máximo seguro de 85% e preparar fechamento de válvula.',
      priority: 'Alta',
      hasAlarm: true,
      alarmMinutesBefore: 15
    });

    // Evento 3: Urgente (faltam 22 min)
    const tUrg = helperMakeDate(22);
    await this.saveEvent({
      consoleId: c08.id,
      pipelineId: dutoOsbra.id,
      uoId: uoReplan.id,
      equipmentTypeId: tipoEsferaReplan.id,
      tagId: tagEs201.id,
      scheduledDate: tUrg.date,
      scheduledTime: tUrg.time,
      description: 'Acompanhar transferência de GLP para a esfera ES-201',
      notes: 'Vazão prevista de 180 m³/h.',
      priority: 'Normal',
      hasAlarm: true,
      alarmMinutesBefore: 15
    });

    // Evento 4: Monitoramento (faltam 50 min)
    const tMon = helperMakeDate(50);
    await this.saveEvent({
      consoleId: c10.id,
      pipelineId: dutoDtcs.id,
      uoId: uoTedep.id,
      equipmentTypeId: tipoValvulaTedep.id,
      tagId: tagPcv301.id,
      scheduledDate: tMon.date,
      scheduledTime: tMon.time,
      description: 'Ajuste de controle de contrapressão na PCV-301',
      notes: 'Ajuste fino de setpoint para amortecimento de transiente.',
      priority: 'Normal',
      hasAlarm: true,
      alarmMinutesBefore: 15
    });

    // Evento 5: Normal (faltam 150 min / 2h30)
    const tNorm = helperMakeDate(150);
    await this.saveEvent({
      consoleId: c04.id,
      pipelineId: dutoOscan.id,
      uoId: uoTedep.id,
      scheduledDate: tNorm.date,
      scheduledTime: tNorm.time,
      description: 'Chegada estimada de PIG raspador no recebedor de TEDEP',
      notes: 'Aviso prévio à equipe de manutenção para abertura de câmara.',
      priority: 'Baixa',
      hasAlarm: true,
      alarmMinutesBefore: 30
    });

    // Evento 6: Concluído há 40 min
    const tComp = helperMakeDate(-40);
    const evComp = await this.saveEvent({
      consoleId: c08.id,
      pipelineId: dutoOsbra.id,
      uoId: uoTebar.id,
      scheduledDate: tComp.date,
      scheduledTime: tComp.time,
      description: 'Abertura de manifold de recebimento de Diesel S10',
      notes: 'Operação concluída conforme procedimento operacional padrão.',
      priority: 'Normal',
      hasAlarm: true,
      alarmMinutesBefore: 15
    });
    await this.completeEvent(evComp.id, 'Manifold aberto e estanqueidade confirmada sem anomalias.');

    return true;
  },

  // --------------------------------------------------------------------------
  // LIMPEZA TOTAL DA BASE
  // --------------------------------------------------------------------------
  clearAllData: async function() {
    const stores = [
      'consoles', 'pipelines', 'operationalUnits', 'pipelineOperationalUnits',
      'equipmentTypes', 'equipmentTags', 'events', 'eventHistory', 'errorLogs'
    ];
    for (const store of stores) {
      await App.DB.clear(store);
    }
    // Re-semear consoles iniciais e faixas padrão
    await App.DB.initDefaults();
    return true;
  }
};

/* ==========================================================================
   7. MOTOR DE ALARMES E MONITORAMENTO CONTÍNUO
   ========================================================================== */
App.AlarmEngine = {
  intervalId: null,
  activeAlertEventId: null,
  titleBlinkState: false,
  originalTitle: document.title,

  start: function() {
    if (this.intervalId) clearInterval(this.intervalId);
    this.intervalId = setInterval(() => this.tick(), 1000);
  },

  stop: function() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
  },

  tick: async function() {
    // 1. Atualizar relógio oficial da sala de controle
    const now = new Date();
    const liveClock = document.getElementById('liveClock');
    if (liveClock) {
      const day = String(now.getDate()).padStart(2, '0');
      const month = String(now.getMonth() + 1).padStart(2, '0');
      const year = now.getFullYear();
      const hours = String(now.getHours()).padStart(2, '0');
      const minutes = String(now.getMinutes()).padStart(2, '0');
      const seconds = String(now.getSeconds()).padStart(2, '0');
      liveClock.textContent = `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
    }

    // 2. Atualizar contadores de tempo restante nos cartões e tabela visíveis
    App.UI.updateLiveTimers();

    // 3. Avaliar alarmes de eventos pendentes
    try {
      const allEvents = await App.DB.getAll('events');
      const pendingEvents = allEvents.filter(e => e.status === 'pendente' && e.active !== false);
      const settings = await App.Service.getSettings();
      const colorRanges = await App.Service.getColorRanges();

      const nowTime = Date.now();
      let hasActiveFiringAlarm = false;

      for (const ev of pendingEvents) {
        if (!ev.hasAlarm) continue;

        // Determinar antecedência (específica do evento ou padrão geral)
        const leadMins = ev.useDefaultAlarmSettings ? (settings.defaultLeadTimeMinutes || 15) : (ev.alarmMinutesBefore || 0);
        const scheduledTime = new Date(ev.scheduledAt).getTime();
        const alarmTargetTime = scheduledTime - (leadMins * 60000);

        // Se estiver adiado e ainda dentro do período de adiamento, não disparar
        if (ev.alarmSnoozedUntil && nowTime < ev.alarmSnoozedUntil) {
          continue;
        }

        // Se o alarme foi reconhecido para este ciclo, não disparar novamente a menos que repita
        if (ev.alarmState === 'acknowledged') {
          continue;
        }

        // Verificar se atingiu o momento do alarme
        if (nowTime >= alarmTargetTime) {
          const repeatEnabled = ev.useDefaultAlarmSettings ? settings.repeatAlarm : ev.alarmRepeat;
          const repeatInterval = (ev.useDefaultAlarmSettings ? settings.repeatIntervalMinutes : ev.alarmRepeatInterval) || 2;
          const maxRepeats = (ev.useDefaultAlarmSettings ? settings.maxRepeats : ev.alarmMaxRepeats) || 5;

          const lastTriggered = ev.lastAlarmTriggeredAt ? new Date(ev.lastAlarmTriggeredAt).getTime() : 0;
          const repeatsCount = ev.alarmTriggerCount || 0;

          // Deve disparar se:
          // a) Nunca disparou ainda (alarmState === 'idle')
          // b) Ou estava adiado e o tempo de adiamento expirou
          // c) Ou repetição habilitada, não excedeu máximo e passou o intervalo
          const isFirstTrigger = ev.alarmState === 'idle' || !ev.lastAlarmTriggeredAt;
          const isSnoozeExpired = ev.alarmSnoozedUntil && nowTime >= ev.alarmSnoozedUntil;
          const isRepeatTime = repeatEnabled && (repeatsCount < maxRepeats) && (nowTime - lastTriggered >= repeatInterval * 60000);

          if (isFirstTrigger || isSnoozeExpired || isRepeatTime) {
            hasActiveFiringAlarm = true;
            await this.fireAlarm(ev, settings, colorRanges, isRepeatTime);
          }
        }
      }

      // Alternar título da aba caso haja alarme disparando
      if (hasActiveFiringAlarm && settings.changeTitleEnabled) {
        this.titleBlinkState = !this.titleBlinkState;
        document.title = this.titleBlinkState ? '⚠️ ALARME OPERACIONAL!' : 'Caderno de Previsões';
      } else if (!hasActiveFiringAlarm && document.title.includes('ALARME')) {
        document.title = this.originalTitle;
      }

    } catch (err) {
      console.error('Erro no ciclo do AlarmEngine:', err);
    }
  },

  fireAlarm: async function(event, settings, colorRanges, isRepeat = false) {
    const nowIso = new Date().toISOString();
    event.alarmState = 'triggered';
    event.lastAlarmTriggeredAt = nowIso;
    event.alarmTriggerCount = (event.alarmTriggerCount || 0) + 1;
    event.alarmSnoozedUntil = null;
    await App.DB.update('events', event);

    // Formas de alerta
    const soundActive = event.useDefaultAlarmSettings ? settings.soundEnabled : event.alarmAudio;
    const visualActive = event.useDefaultAlarmSettings ? settings.visualAlertEnabled : event.alarmVisual;
    const notifActive = event.useDefaultAlarmSettings ? settings.notificationEnabled : event.alarmNotification;

    // 1. Sinal Sonoro Local
    if (soundActive) {
      App.Audio.play(settings.soundType || 'chime', settings.soundVolume || 80);
    }

    // 2. Alerta Visual Modal
    if (visualActive) {
      App.UI.showAlarmModal(event);
    }

    // 3. Notificação do Navegador
    if (notifActive && App.Notifications.getPermissionState() === 'concedida') {
      const uos = await App.DB.getAll('operationalUnits');
      const pipelines = await App.DB.getAll('pipelines');
      const consoles = await App.DB.getAll('consoles');
      const tags = await App.DB.getAll('equipmentTags');

      const uo = uos.find(u => u.id === event.uoId);
      const pipe = pipelines.find(p => p.id === event.pipelineId);
      const con = consoles.find(c => c.id === event.consoleId);
      const tag = tags.find(t => t.id === event.tagId);

      const pathStr = `${con ? con.name : ''} | ${pipe ? pipe.name : ''} | ${uo ? uo.name : ''} ${tag ? '| ' + tag.tag : ''}`;
      App.Notifications.send(`Previsão Operacional: ${event.description}`, {
        body: `${pathStr}\nHorário: ${App.Utils.formatDateTime(event.scheduledDate, event.scheduledTime)}`,
        tag: `alarm-${event.id}`
      });
    }

    // Registrar no histórico de auditoria
    await App.Service.logEventHistory({
      eventId: event.id,
      action: 'disparo_alarme',
      description: `Alarme disparado (${isRepeat ? 'Repetição ' + event.alarmTriggerCount : 'Disparo Inicial'}). Canais acionados: ${soundActive ? 'Som ' : ''}${visualActive ? 'Modal ' : ''}${notifActive ? 'Notificação' : ''}`,
      previousValue: 'aguardando',
      newValue: 'disparado',
      localUser: 'Sistema de Alarme'
    });

    // Atualizar UI
    App.UI.renderPendingEvents();
    App.UI.renderDashboard();
  }
};

/* ==========================================================================
   8. CAMADA DE BACKUP, IMPORTAÇÃO, EXPORTAÇÃO E CSV
   ========================================================================== */
App.Backup = {
  
  // Exportar JSON completo
  exportJSON: async function() {
    const backupObj = {
      application: 'Controle de Previsões em Dutos',
      schemaVersion: 1,
      exportedAt: new Date().toISOString(),
      data: {
        consoles: await App.DB.getAll('consoles'),
        pipelines: await App.DB.getAll('pipelines'),
        operationalUnits: await App.DB.getAll('operationalUnits'),
        pipelineOperationalUnits: await App.DB.getAll('pipelineOperationalUnits'),
        equipmentTypes: await App.DB.getAll('equipmentTypes'),
        equipmentTags: await App.DB.getAll('equipmentTags'),
        events: await App.DB.getAll('events'),
        eventHistory: await App.DB.getAll('eventHistory'),
        colorRanges: await App.DB.getAll('colorRanges'),
        settings: await App.DB.getAll('settings')
      }
    };

    const jsonStr = JSON.stringify(backupObj, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json;charset=utf-8' });
    const nowStr = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
    const fileName = `backup_previsoes_dutos_${nowStr}.json`;

    this.downloadBlob(blob, fileName);

    // Atualizar data do último backup
    const settings = await App.Service.getSettings();
    settings.lastBackupAt = new Date().toISOString();
    await App.Service.saveSettings(settings);
    App.UI.updateBackupPill(settings.lastBackupAt);

    App.UI.showToast('Backup JSON exportado com sucesso!', 'success');
  },

  // Validar arquivo ou string de backup JSON
  validateBackupFile: async function(fileOrString) {
    if (typeof fileOrString === 'string') {
      return this.validateBackupData(fileOrString);
    }
    if (fileOrString && typeof fileOrString.text === 'function') {
      const text = await fileOrString.text();
      return this.validateBackupData(text);
    }
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (ev) => {
        try {
          resolve(this.validateBackupData(ev.target.result));
        } catch (err) {
          reject(err);
        }
      };
      reader.onerror = () => reject(new Error('Falha ao ler o arquivo de backup selecionado.'));
      reader.readAsText(fileOrString, 'UTF-8');
    });
  },

  // Validar arquivo de backup JSON
  validateBackupData: function(jsonString) {
    let parsed;
    try {
      parsed = JSON.parse(jsonString);
    } catch (e) {
      throw new Error('O arquivo selecionado não contém um formato JSON válido.');
    }

    if (!parsed || typeof parsed !== 'object') {
      throw new Error('Conteúdo do arquivo de backup inválido.');
    }

    if (parsed.schemaVersion !== 1 && parsed.schemaVersion !== '1') {
      throw new Error(`Versão de esquema incompatível: esperado 1, recebido "${parsed.schemaVersion}".`);
    }

    if (!parsed.data || typeof parsed.data !== 'object') {
      throw new Error('A seção de dados do arquivo de backup está ausente.');
    }

    const requiredKeys = ['consoles', 'pipelines', 'operationalUnits', 'events'];
    for (const key of requiredKeys) {
      if (!Array.isArray(parsed.data[key])) {
        throw new Error(`A coleção obrigatória "${key}" não foi encontrada no backup.`);
      }
    }

    return parsed;
  },

  // Importar backup (Modos 'replace' ou 'merge')
  importJSON: async function(backupObject, mode = 'merge') {
    const data = backupObject.data;

    if (mode === 'replace') {
      // 1. Criar backup automático preventivo antes da substituição
      await this.exportJSON();

      // 2. Limpar todas as tabelas
      const stores = [
        'consoles', 'pipelines', 'operationalUnits', 'pipelineOperationalUnits',
        'equipmentTypes', 'equipmentTags', 'events', 'eventHistory', 'colorRanges', 'settings'
      ];
      for (const s of stores) {
        await App.DB.clear(s);
      }

      // 3. Restaurar dados diretamente
      for (const s of stores) {
        const items = data[s] || [];
        for (const item of items) {
          await App.DB.insert(s, item);
        }
      }
    } else {
      // Modo Mesclar (Merge): compara por ID, preservando registros mais recentes sem duplicar
      const stores = [
        'consoles', 'pipelines', 'operationalUnits', 'pipelineOperationalUnits',
        'equipmentTypes', 'equipmentTags', 'events', 'eventHistory', 'colorRanges', 'settings'
      ];

      for (const s of stores) {
        const newItems = data[s] || [];
        const existingItems = await App.DB.getAll(s);
        const existingMap = new Map(existingItems.map(item => [item.id || item.key, item]));

        for (const item of newItems) {
          const key = item.id || item.key;
          if (existingMap.has(key)) {
            // Comparar updatedAt e version
            const current = existingMap.get(key);
            const currentVer = current.version || 0;
            const newVer = item.version || 0;
            if (newVer >= currentVer) {
              await App.DB.update(s, item);
            }
          } else {
            await App.DB.insert(s, item);
          }
        }
      }
    }

    return true;
  },

  // --------------------------------------------------------------------------
  // EXPORTAÇÃO CSV COMPATÍVEL COM EXCEL (UTF-8 COM BOM, PONTO E VÍRGULA)
  // --------------------------------------------------------------------------
  exportCSV: async function(type = 'pending') {
    const BOM = '\uFEFF';
    let csvRows = [];
    let fileName = '';

    // Normaliza os tipos ('pendente' -> 'pending', 'concluido' -> 'completed', 'master' -> 'cadastros')
    let normType = type;
    if (type === 'pendente') normType = 'pending';
    if (type === 'concluido') normType = 'completed';
    if (type === 'master') normType = 'cadastros';
    if (type === 'todos') normType = 'all';

    const consoles = await App.DB.getAll('consoles');
    const pipelines = await App.DB.getAll('pipelines');
    const uos = await App.DB.getAll('operationalUnits');
    const types = await App.DB.getAll('equipmentTypes');
    const tags = await App.DB.getAll('equipmentTags');

    const consoleMap = new Map(consoles.map(c => [c.id, c.name]));
    const pipeMap = new Map(pipelines.map(p => [p.id, p.name]));
    const uoMap = new Map(uos.map(u => [u.id, u.name]));
    const typeMap = new Map(types.map(t => [t.id, t.name]));
    const tagMap = new Map(tags.map(t => [t.id, t.tag]));

    if (normType === 'pending' || normType === 'completed' || normType === 'all') {
      const allEvents = await App.DB.getAll('events');
      const filtered = normType === 'all'
        ? allEvents.filter(e => e.active !== false)
        : allEvents.filter(e => normType === 'pending' ? e.status === 'pendente' : e.status === 'concluido');

      const headers = [
        'ID', 'Situação', 'Console', 'Duto', 'UO', 'Tipo de Equipamento', 'TAG',
        'Data Prevista', 'Hora Prevista', 'Descrição', 'Observações', 'Alarme Ativo',
        'Antecedência (min)', 'Data Conclusão', 'Hora Conclusão', 'Diferença Efetiva',
        'Observação Conclusão', 'Data Criação', 'Data Atualização'
      ];
      csvRows.push(headers.join(';'));

      for (const ev of filtered) {
        const row = [
          App.Utils.escapeCSV(ev.id),
          App.Utils.escapeCSV(ev.status === 'concluido' ? 'Concluído' : 'Pendente'),
          App.Utils.escapeCSV(consoleMap.get(ev.consoleId) || ''),
          App.Utils.escapeCSV(pipeMap.get(ev.pipelineId) || ''),
          App.Utils.escapeCSV(uoMap.get(ev.uoId) || ''),
          App.Utils.escapeCSV(typeMap.get(ev.equipmentTypeId) || ''),
          App.Utils.escapeCSV(tagMap.get(ev.tagId) || ''),
          App.Utils.escapeCSV(App.Utils.formatDate(ev.scheduledDate)),
          App.Utils.escapeCSV(App.Utils.formatTime(ev.scheduledTime)),
          App.Utils.escapeCSV(ev.description || ''),
          App.Utils.escapeCSV(ev.notes || ''),
          App.Utils.escapeCSV(ev.hasAlarm ? 'Sim' : 'Não'),
          App.Utils.escapeCSV(ev.alarmMinutesBefore || 0),
          App.Utils.escapeCSV(ev.completedAt ? App.Utils.formatDate(ev.completedAt) : ''),
          App.Utils.escapeCSV(ev.completedAt ? App.Utils.formatTime(ev.completedAt) : ''),
          App.Utils.escapeCSV(App.Utils.formatDiffMinutes(ev.completedTimeDiffMinutes)),
          App.Utils.escapeCSV(ev.completionNote || ''),
          App.Utils.escapeCSV(App.Utils.formatDateTime(ev.createdAt)),
          App.Utils.escapeCSV(App.Utils.formatDateTime(ev.updatedAt))
        ];
        csvRows.push(row.join(';'));
      }

      fileName = normType === 'pending'
        ? 'previsoes_pendentes.csv'
        : (normType === 'completed' ? 'previsoes_concluidas.csv' : 'previsoes_todas.csv');

    } else if (normType === 'cadastros') {
      const headers = ['Tipo de Registro', 'ID', 'Nome / Código', 'Console / UO Vinculada', 'Situação', 'Data Criação'];
      csvRows.push(headers.join(';'));

      consoles.forEach(c => {
        csvRows.push(['Console', App.Utils.escapeCSV(c.id), App.Utils.escapeCSV(c.name), '-', c.active ? 'Ativo' : 'Inativo', App.Utils.formatDateTime(c.createdAt)].join(';'));
      });
      pipelines.forEach(p => {
        csvRows.push(['Duto', App.Utils.escapeCSV(p.id), App.Utils.escapeCSV(p.name), App.Utils.escapeCSV(consoleMap.get(p.consoleId) || ''), p.active ? 'Ativo' : 'Inativo', App.Utils.formatDateTime(p.createdAt)].join(';'));
      });
      uos.forEach(u => {
        csvRows.push(['UO', App.Utils.escapeCSV(u.id), App.Utils.escapeCSV(u.name), '-', u.active ? 'Ativo' : 'Inativo', App.Utils.formatDateTime(u.createdAt)].join(';'));
      });
      types.forEach(t => {
        csvRows.push(['Tipo Equipamento', App.Utils.escapeCSV(t.id), App.Utils.escapeCSV(t.name), App.Utils.escapeCSV(uoMap.get(t.uoId) || ''), t.active ? 'Ativo' : 'Inativo', App.Utils.formatDateTime(t.createdAt)].join(';'));
      });
      tags.forEach(t => {
        csvRows.push(['TAG', App.Utils.escapeCSV(t.id), App.Utils.escapeCSV(t.tag), App.Utils.escapeCSV(uoMap.get(t.uoId) || ''), t.active ? 'Ativo' : 'Inativo', App.Utils.formatDateTime(t.createdAt)].join(';'));
      });

      fileName = 'estrutura_cadastral_dutos.csv';
    }

    const csvContent = BOM + csvRows.join('\r\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    this.downloadBlob(blob, fileName);
    App.UI.showToast(`Relatório CSV gerado: ${fileName}`, 'success');
  },

  downloadBlob: function(blob, fileName) {
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }
};



/* ==========================================================================
   9. CAMADA DE INTERFACE COM O USUÁRIO (UI CONTROLLER)
   ========================================================================== */
App.UI = {
  currentView: 'viewDashboard',
  viewMode: 'cards', // 'cards' ou 'table' para lista de pendentes
  responsiveLayoutMode: 'auto', // 'auto', 'compact', 'mobile', 'tablet', 'conventional', 'widescreen', 'ultrawide'
  activePendingEvents: [],
  selectedEventForAction: null,
  selectedDetailEventId: null,
  selectedDetailTab: 'details', // 'details', 'notes', 'history'
  activeConsoleId: null,
  currentCadastrosCategory: 'consoles',

  // Stylus / Caneta
  stylusCanvas: null,
  stylusCtx: null,
  stylusIsDrawing: false,
  stylusHasDrawing: false,
  stylusIsEraser: false,
  stylusDrawingData: null,
  stylusHistory: [],
  stylusActivePointerType: null,

  init: async function() {
    this.bindGlobalEvents();
    this.bindNavEvents();
    this.bindFormEvents();
    this.bindFilterEvents();
    this.bindModalEvents();

    // Carregar preferências e estado inicial
    const settings = await App.Service.getSettings();
    this.applyTheme(settings.theme || 'dark');

    // Modo de visualização da lista (cards vs table)
    if (settings.viewMode === 'cards' || settings.viewMode === 'table') {
      this.viewMode = settings.viewMode;
    } else {
      this.viewMode = 'cards';
    }
    this.updateViewModeUI();

    // Modo de Layout Responsivo Universal (Auto / Compacto / Celular / Tablet / Convencional / Widescreen / Ultrawide)
    this.responsiveLayoutMode = settings.responsiveLayoutMode || (
      ['auto', 'compact', 'mobile', 'tablet', 'conventional', 'widescreen', 'ultrawide'].includes(settings.viewMode)
        ? settings.viewMode
        : 'auto'
    );
    this.applyResponsiveLayoutMode(this.responsiveLayoutMode, false);

    window.addEventListener('resize', () => {
      this.handleViewportResize();
    });

    document.getElementById('headerUserName').textContent = settings.localUserName || 'Usuário local';
    const inputUser = document.getElementById('inputSettingsUserName');
    if (inputUser) inputUser.value = settings.localUserName || 'Usuário local';

    this.updateBackupPill(settings.lastBackupAt);
    App.Notifications.updateStatusPill();
    App.Audio.init();

    // Inicializar Console Global no Cabeçalho
    this.activeConsoleId = settings.activeConsoleId || null;
    await this.initHeaderConsole();

    // Inicializar Drawer Mobile & Stylus Pad
    this.initMobileDrawer();
    this.initStylusPad();

    // Iniciar na tela Painel
    await this.renderDashboard();
    App.AlarmEngine.start();
  },

  // --------------------------------------------------------------------------
  // ARQUITETURA RESPONSIVA UNIVERSAL E TEMAS VISUAIS (SEÇÕES 2, 16 E 24)
  // --------------------------------------------------------------------------
  getEffectiveViewportTier: function(mode) {
    const m = mode || this.responsiveLayoutMode || 'auto';
    if (['mobile', 'tablet', 'conventional', 'widescreen', 'ultrawide'].includes(m)) {
      return m;
    }
    const w = window.innerWidth || 1280;
    if (w < 768) return 'mobile';
    if (w < 1200) return 'tablet';
    if (w < 1600) return 'conventional';
    if (w < 2200) return 'widescreen';
    return 'ultrawide';
  },

  applyResponsiveLayoutMode: async function(mode, persist = true) {
    const validModes = ['auto', 'compact', 'mobile', 'tablet', 'conventional', 'widescreen', 'ultrawide'];
    const cleanMode = validModes.includes(mode) ? mode : 'auto';
    this.responsiveLayoutMode = cleanMode;

    document.body.classList.remove('density-compact');
    document.body.removeAttribute('data-layout-mode');

    if (cleanMode === 'compact') {
      document.body.classList.add('density-compact');
      const tier = this.getEffectiveViewportTier('auto');
      document.body.setAttribute('data-layout-mode', tier);
    } else if (cleanMode === 'auto') {
      // Em modo auto, também expomos o tier efetivo caso útil, mas deixamos as media queries livres
      const tier = this.getEffectiveViewportTier('auto');
      if (tier === 'widescreen' || tier === 'ultrawide') {
        document.body.setAttribute('data-layout-mode', tier);
      }
    } else {
      document.body.setAttribute('data-layout-mode', cleanMode);
    }

    // Sincronizar todos os seletores de modo de exibição
    ['selectHeaderViewMode', 'selectDrawerViewMode', 'selectSettingsViewMode'].forEach(id => {
      const sel = document.getElementById(id);
      if (sel && sel.value !== cleanMode) sel.value = cleanMode;
    });

    this.checkViewModeUsabilityWarning();

    // Ajustar exibição padrão de Cadastros conforme tier
    const effTier = this.getEffectiveViewportTier(cleanMode);
    if (effTier === 'mobile' || effTier === 'tablet') {
      this.switchCadastrosCategory(this.currentCadastrosCategory || 'consoles');
    } else {
      this.switchCadastrosCategory('all');
    }

    if (persist) {
      const settings = await App.Service.getSettings();
      settings.responsiveLayoutMode = cleanMode;
      await App.Service.saveSettings(settings);
    }

    if (this.currentView === 'viewPendingEvents') {
      this.renderPendingDetailPane();
    }
  },

  checkViewModeUsabilityWarning: function() {
    const banner = document.getElementById('viewModeWarningBanner');
    const textEl = document.getElementById('viewModeWarningText');
    if (!banner) return;

    const w = window.innerWidth || 1280;
    const m = this.responsiveLayoutMode;
    let warnMsg = null;

    if ((m === 'ultrawide' || m === 'widescreen' || m === 'conventional') && w < 768) {
      warnMsg = `O modo "${m.toUpperCase()}" foi forçado em uma tela estreita (${w}px). Algumas colunas podem exigir rolagem lateral.`;
    } else if (m === 'ultrawide' && w < 1200) {
      warnMsg = `O modo "ULTRAWIDE" foi selecionado em uma tela de ${w}px. Para melhor leitura, recomenda-se o modo Automático.`;
    } else if (m === 'mobile' && w >= 1600) {
      warnMsg = `O modo "CELULAR" está ativo em um monitor amplo (${w}px).`;
    }

    if (warnMsg) {
      if (textEl) textEl.textContent = warnMsg;
      banner.style.display = 'flex';
    } else {
      banner.style.display = 'none';
    }
  },

  handleViewportResize: function() {
    if (this.responsiveLayoutMode === 'auto' || this.responsiveLayoutMode === 'compact') {
      const tier = this.getEffectiveViewportTier('auto');
      if (this.responsiveLayoutMode === 'compact' || tier === 'widescreen' || tier === 'ultrawide') {
        document.body.setAttribute('data-layout-mode', tier);
      } else {
        document.body.removeAttribute('data-layout-mode');
      }
    }
    this.checkViewModeUsabilityWarning();
  },

  applyTheme: function(themeName) {
    document.body.classList.remove('theme-light', 'theme-industrial');
    let cleanTheme = 'dark';
    if (themeName === 'light') {
      document.body.classList.add('theme-light');
      cleanTheme = 'light';
    } else if (themeName === 'industrial') {
      document.body.classList.add('theme-industrial');
      cleanTheme = 'industrial';
    }

    const selTheme = document.getElementById('selectSettingsTheme');
    if (selTheme) selTheme.value = cleanTheme;

    const labelMap = {
      dark: 'Controle Escuro',
      light: 'Profissional Claro',
      industrial: 'Industrial Alto Contraste'
    };
    const btnDrawerTheme = document.getElementById('btnDrawerTheme');
    if (btnDrawerTheme) {
      btnDrawerTheme.textContent = `Alternar Tema (${labelMap[cleanTheme]})`;
    }
    const btnHeaderTheme = document.getElementById('btnToggleTheme');
    if (btnHeaderTheme) {
      btnHeaderTheme.title = `Tema Atual: ${labelMap[cleanTheme]} (Clique para alternar entre os 3 temas)`;
    }
  },

  cycleTheme: async function() {
    const settings = await App.Service.getSettings();
    const order = ['dark', 'light', 'industrial'];
    const curIdx = order.indexOf(settings.theme || 'dark');
    const nextTheme = order[(curIdx + 1) % order.length];
    settings.theme = nextTheme;
    await App.Service.saveSettings(settings);
    this.applyTheme(nextTheme);
    const names = { dark: 'Controle Escuro', light: 'Profissional Claro', industrial: 'Industrial Alto Contraste' };
    this.showToast(`Tema visual alterado para: ${names[nextTheme]}`, 'info');
  },

  updateBackupPill: function(lastBackupAt) {
    const pill = document.getElementById('pillBackup');
    const labelDate = document.getElementById('labelLastBackupDate');
    const statusModalBackup = document.getElementById('statusModalLastBackup');
    const overdueBanner = document.getElementById('backupOverdueBanner');
    const overdueText = document.getElementById('backupOverdueText');

    if (lastBackupAt) {
      const dt = App.Utils.formatDateTime(lastBackupAt);
      const daysDiff = Math.floor((Date.now() - new Date(lastBackupAt).getTime()) / (1000 * 60 * 60 * 24));
      if (pill) {
        pill.className = daysDiff > 7 ? 'status-pill warn' : 'status-pill ok';
        pill.innerHTML = `<span class="indicator-dot">&bull;</span> Backup: ${App.Utils.formatDate(lastBackupAt)}`;
      }
      if (labelDate) labelDate.textContent = `Último backup: ${dt}`;
      if (statusModalBackup) statusModalBackup.textContent = `${dt} (${daysDiff === 0 ? 'Hoje' : 'há ' + daysDiff + ' dia(s)'})`;

      if (overdueBanner) {
        if (daysDiff > 7) {
          if (overdueText) overdueText.textContent = `Último backup local realizado há ${daysDiff} dias (${App.Utils.formatDate(lastBackupAt)}). Recomenda-se exportar novo backup.`;
          overdueBanner.style.display = 'flex';
        } else {
          overdueBanner.style.display = 'none';
        }
      }
    } else {
      if (pill) {
        pill.className = 'status-pill warn';
        pill.innerHTML = `<span class="indicator-dot">&bull;</span> Backup: Nunca`;
      }
      if (labelDate) labelDate.textContent = `Último backup: Nunca`;
      if (statusModalBackup) statusModalBackup.textContent = `Nunca realizado`;
      if (overdueBanner) {
        if (overdueText) overdueText.textContent = `Backup local ainda não foi realizado neste dispositivo. Exporte um backup preventivo regularmente.`;
        overdueBanner.style.display = 'flex';
      }
    }
  },

  // --------------------------------------------------------------------------
  // CONSOLE GLOBAL NO CABEÇALHO
  // --------------------------------------------------------------------------
  initHeaderConsole: async function() {
    const selectHeader = document.getElementById('headerActiveConsole');
    const consoles = await App.DB.getAll('consoles');
    consoles.sort((a, b) => a.name.localeCompare(b.name));

    if (consoles.length > 0) {
      if (!this.activeConsoleId || !consoles.find(c => c.id === this.activeConsoleId)) {
        const c04 = consoles.find(c => c.name === 'C04');
        this.activeConsoleId = c04 ? c04.id : consoles[0].id;
      }
    }

    if (selectHeader) {
      selectHeader.innerHTML = consoles.map(c => `
        <option value="${c.id}" ${c.id === this.activeConsoleId ? 'selected' : ''}>
          Console: ${App.Utils.escapeHTML(c.name)}${c.active ? '' : ' (Inativo)'}
        </option>
      `).join('');

      if (!selectHeader.dataset.bound) {
        selectHeader.dataset.bound = 'true';
        selectHeader.addEventListener('change', async (e) => {
          this.activeConsoleId = e.target.value;
          const settings = await App.Service.getSettings();
          settings.activeConsoleId = this.activeConsoleId;
          await App.Service.saveSettings(settings);

          await this.syncActiveConsoleUI();
          const selName = selectHeader.options[selectHeader.selectedIndex]?.text.replace('Console: ', '') || '';
          this.showToast(`Console ativo alterado para ${selName}`, 'info');

          if (this.currentView === 'viewPendingEvents') {
            await this.renderPendingEvents();
          } else if (this.currentView === 'viewNewEvent') {
            await this.initNewEventCombos();
          } else if (this.currentView === 'viewDashboard') {
            await this.renderDashboard();
          }
        });
      }
    }

    await this.syncActiveConsoleUI();
  },

  syncActiveConsoleUI: async function() {
    const consoles = await App.DB.getAll('consoles');
    const activeConsole = consoles.find(c => c.id === this.activeConsoleId);
    const name = activeConsole ? activeConsole.name : 'Não selecionado';

    const labelEvent = document.getElementById('labelEventActiveConsole');
    if (labelEvent) labelEvent.textContent = `Console Ativo: ${name}`;

    const labelBadge = document.getElementById('labelActiveConsoleBadge');
    if (labelBadge) labelBadge.textContent = name;

    const inputConsole = document.getElementById('eventConsoleId');
    if (inputConsole) inputConsole.value = this.activeConsoleId || '';

    const selectEventConsole = document.getElementById('selectEventConsole');
    if (selectEventConsole) selectEventConsole.value = this.activeConsoleId || '';

    const labelFilter = document.getElementById('labelActiveConsoleFilter');
    if (labelFilter) labelFilter.textContent = name;
  },

  // --------------------------------------------------------------------------
  // MENU RETRÁTIL MOBILE & TABLET (DRAWER) E NAVEGAÇÃO INFERIOR
  // --------------------------------------------------------------------------
  initMobileDrawer: function() {
    const drawer = document.getElementById('appMobileDrawer');
    const overlay = document.getElementById('mobileDrawerOverlay');
    const btnOpen = document.getElementById('btnToggleMobileMenu');
    const btnClose = document.getElementById('btnCloseMobileDrawer');
    const fab = document.getElementById('fabAddEvent');
    const btnBottomMore = document.getElementById('btnBottomNavMore');

    const openDrawer = () => {
      drawer?.classList.add('open', 'active');
      overlay?.classList.add('open', 'active');
    };

    const closeDrawer = () => {
      drawer?.classList.remove('open', 'active');
      overlay?.classList.remove('open', 'active');
    };

    btnOpen?.addEventListener('click', openDrawer);
    btnBottomMore?.addEventListener('click', openDrawer);
    btnClose?.addEventListener('click', closeDrawer);
    overlay?.addEventListener('click', closeDrawer);

    document.querySelectorAll('#appMobileDrawer .mobile-nav-link').forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetView = link.getAttribute('data-view');
        if (targetView) {
          closeDrawer();
          if (targetView === 'viewNewEvent') this.resetEventForm();
          this.navigateTo(targetView);
        }
      });
    });

    // Botões da Barra de Navegação Inferior Fixa (#mobileBottomNav)
    document.querySelectorAll('#mobileBottomNav .bottom-nav-item[data-target]').forEach(btn => {
      btn.addEventListener('click', () => {
        const targetView = btn.getAttribute('data-target');
        if (targetView) {
          closeDrawer();
          this.navigateTo(targetView);
        }
      });
    });

    fab?.addEventListener('click', () => {
      closeDrawer();
      this.resetEventForm();
      this.navigateTo('viewNewEvent');
    });

    // Botões de Status da Aplicação no Drawer e no Header
    const openStatusModal = () => {
      closeDrawer();
      this.openAppStatusModal();
    };
    document.getElementById('btnDrawerAppStatus')?.addEventListener('click', openStatusModal);
    document.getElementById('btnHeaderAppStatus')?.addEventListener('click', openStatusModal);

    // Alternar Tema pelo Drawer
    document.getElementById('btnDrawerTheme')?.addEventListener('click', () => {
      this.cycleTheme();
    });
  },

  openAppStatusModal: async function() {
    const settings = await App.Service.getSettings();
    this.updateBackupPill(settings.lastBackupAt);
    App.Audio.updateStatusPill();
    App.Notifications.updateStatusPill();
    document.getElementById('modalAppStatus')?.classList.add('active');
  },

  // --------------------------------------------------------------------------
  // CANETA / STYLUS / DESENHO MANUAL (COM DESFAZER, TELA CHEIA E PALM REJECTION)
  // --------------------------------------------------------------------------
  initStylusPad: function() {
    const canvas = document.getElementById('stylusDrawingCanvas');
    const btnToggle = document.getElementById('btnToggleStylusCanvas');
    const boxCanvas = document.getElementById('boxStylusCanvas');
    const btnClear = document.getElementById('btnClearStylusCanvas');
    const btnEraser = document.getElementById('btnEraserStylusCanvas');
    const btnUndo = document.getElementById('btnUndoStylusCanvas');
    const btnFullscreen = document.getElementById('btnFullscreenStylusCanvas');
    const inputColor = document.getElementById('inputStylusStrokeColor');
    const selectWidth = document.getElementById('selectStylusStrokeWidth');
    const modeIndicator = document.getElementById('stylusModeIndicator');

    if (!canvas) return;
    this.stylusCanvas = canvas;
    this.stylusCtx = canvas.getContext('2d');
    this.stylusHistory = [];

    const updateModeIndicator = () => {
      if (!modeIndicator) return;
      const w = selectWidth?.value || '4';
      if (this.stylusIsEraser) {
        modeIndicator.textContent = 'Modo: Borracha (18px)';
        modeIndicator.style.color = '#fbbf24';
      } else {
        modeIndicator.textContent = `Modo: Caneta (${w}px)`;
        modeIndicator.style.color = inputColor?.value || '#38bdf8';
      }
    };

    btnToggle?.addEventListener('click', () => {
      const isHidden = boxCanvas.style.display === 'none' || !boxCanvas.style.display;
      boxCanvas.style.display = isHidden ? 'block' : 'none';
      if (modeIndicator) modeIndicator.style.display = isHidden ? 'inline-block' : 'none';
      btnToggle.classList.toggle('active', isHidden);
      updateModeIndicator();
    });

    inputColor?.addEventListener('input', updateModeIndicator);
    selectWidth?.addEventListener('change', updateModeIndicator);

    const pushHistorySnapshot = () => {
      try {
        const snapshot = canvas.toDataURL('image/png');
        this.stylusHistory.push(snapshot);
        if (this.stylusHistory.length > 25) this.stylusHistory.shift();
      } catch (err) {}
    };

    const getPos = (e) => {
      const rect = canvas.getBoundingClientRect();
      return {
        x: (e.clientX - rect.left) * (canvas.width / rect.width),
        y: (e.clientY - rect.top) * (canvas.height / rect.height)
      };
    };

    canvas.addEventListener('pointerdown', (e) => {
      // Prioridade para caneta stylus (rejeição básica de palma se já estiver usando pen)
      if (this.stylusIsDrawing && this.stylusActivePointerType === 'pen' && e.pointerType === 'touch') {
        return;
      }
      pushHistorySnapshot();
      this.stylusActivePointerType = e.pointerType;
      try { canvas.setPointerCapture(e.pointerId); } catch(err) {}
      this.stylusIsDrawing = true;
      this.stylusHasDrawing = true;
      const pos = getPos(e);
      this.stylusCtx.beginPath();
      this.stylusCtx.moveTo(pos.x, pos.y);

      let baseWidth = parseInt(selectWidth?.value || '4', 10);
      if (e.pointerType === 'pen' && e.pressure && e.pressure > 0) {
        baseWidth = Math.max(1.5, baseWidth * (0.5 + e.pressure));
      }

      this.stylusCtx.lineCap = 'round';
      this.stylusCtx.lineJoin = 'round';
      if (this.stylusIsEraser) {
        this.stylusCtx.globalCompositeOperation = 'destination-out';
        this.stylusCtx.lineWidth = 18;
      } else {
        this.stylusCtx.globalCompositeOperation = 'source-over';
        this.stylusCtx.lineWidth = baseWidth;
        this.stylusCtx.strokeStyle = inputColor?.value || '#38bdf8';
      }
    });

    canvas.addEventListener('pointermove', (e) => {
      if (!this.stylusIsDrawing) return;
      if (this.stylusActivePointerType === 'pen' && e.pointerType === 'touch') return;
      const pos = getPos(e);
      this.stylusCtx.lineTo(pos.x, pos.y);
      this.stylusCtx.stroke();
    });

    const stopDrawing = (e) => {
      if (this.stylusIsDrawing) {
        this.stylusIsDrawing = false;
        this.stylusActivePointerType = null;
        try { canvas.releasePointerCapture(e.pointerId); } catch(err) {}
        this.stylusDrawingData = canvas.toDataURL('image/png');
      }
    };

    canvas.addEventListener('pointerup', stopDrawing);
    canvas.addEventListener('pointercancel', stopDrawing);
    canvas.addEventListener('pointerleave', stopDrawing);

    // Desfazer último traço (Undo)
    btnUndo?.addEventListener('click', () => {
      if (!this.stylusHistory || this.stylusHistory.length === 0) {
        this.clearStylusPad(true);
        return;
      }
      const prevDataUrl = this.stylusHistory.pop();
      this.stylusCtx.globalCompositeOperation = 'source-over';
      this.stylusCtx.clearRect(0, 0, canvas.width, canvas.height);
      if (prevDataUrl) {
        const img = new Image();
        img.onload = () => {
          this.stylusCtx.drawImage(img, 0, 0, canvas.width, canvas.height);
          this.stylusDrawingData = canvas.toDataURL('image/png');
        };
        img.src = prevDataUrl;
      } else {
        this.stylusHasDrawing = false;
        this.stylusDrawingData = null;
      }
    });

    // Tela Cheia para Lousa
    btnFullscreen?.addEventListener('click', () => {
      const isFull = boxCanvas.classList.toggle('fullscreen-lousa');
      btnFullscreen.textContent = isFull ? '✕ Concluir Tela Cheia' : '⛶ Tela Cheia';
      btnFullscreen.classList.toggle('btn-primary', isFull);
      btnFullscreen.classList.toggle('btn-outline', !isFull);
    });

    // Limpar Lousa (com confirmação se houver traços)
    btnClear?.addEventListener('click', () => {
      if (this.stylusHasDrawing) {
        this.showConfirmModal('Limpar Anotação Manuscrita', 'Deseja apagar todo o desenho atual da lousa?', () => {
          this.clearStylusPad(true);
        });
      } else {
        this.clearStylusPad(true);
      }
    });

    btnEraser?.addEventListener('click', () => {
      this.stylusIsEraser = !this.stylusIsEraser;
      btnEraser.classList.toggle('btn-secondary', this.stylusIsEraser);
      btnEraser.classList.toggle('btn-outline', !this.stylusIsEraser);
      btnEraser.textContent = this.stylusIsEraser ? 'Modo Caneta' : 'Borracha';
      updateModeIndicator();
    });
  },

  clearStylusPad: function(resetHistory = true) {
    if (this.stylusCanvas && this.stylusCtx) {
      this.stylusCtx.globalCompositeOperation = 'source-over';
      this.stylusCtx.clearRect(0, 0, this.stylusCanvas.width, this.stylusCanvas.height);
      this.stylusHasDrawing = false;
      this.stylusDrawingData = null;
      if (resetHistory) this.stylusHistory = [];
    }
    const box = document.getElementById('boxStylusCanvas');
    if (box) box.classList.remove('fullscreen-lousa');
    const btnFull = document.getElementById('btnFullscreenStylusCanvas');
    if (btnFull) {
      btnFull.textContent = '⛶ Tela Cheia';
      btnFull.classList.remove('btn-primary');
      btnFull.classList.add('btn-outline');
    }
  },

  getStylusData: function() {
    if (!this.stylusHasDrawing || !this.stylusCanvas) {
      return this.stylusDrawingData || null;
    }
    return this.stylusCanvas.toDataURL('image/png');
  },

  loadStylusData: function(dataUrl) {
    this.clearStylusPad(true);
    if (!dataUrl) return;
    this.stylusDrawingData = dataUrl;
    this.stylusHasDrawing = true;
    const img = new Image();
    img.onload = () => {
      if (this.stylusCtx && this.stylusCanvas) {
        this.stylusCtx.globalCompositeOperation = 'source-over';
        this.stylusCtx.drawImage(img, 0, 0, this.stylusCanvas.width, this.stylusCanvas.height);
      }
    };
    img.src = dataUrl;
    const box = document.getElementById('boxStylusCanvas');
    if (box) box.style.display = 'block';
    const ind = document.getElementById('stylusModeIndicator');
    if (ind) ind.style.display = 'inline-block';
  },

  // --------------------------------------------------------------------------
  // ATUALIZAÇÃO CENTRALIZADA DE LISTAS DE UOS (SINCRONIZAÇÃO EM TEMPO REAL)
  // --------------------------------------------------------------------------
  refreshAllMasterDataDropdowns: async function() {
    const uos = await App.DB.getAll('operationalUnits');
    const activeUOs = uos.filter(u => u.active).sort((a, b) => a.name.localeCompare(b.name));

    // 1. Dutos UO checkboxes
    const boxUOs = document.getElementById('boxPipelineUOs');
    if (boxUOs) {
      const checkedValues = Array.from(boxUOs.querySelectorAll('input[type="checkbox"]:checked')).map(cb => cb.value);
      boxUOs.innerHTML = activeUOs.map(u => `
        <label class="form-checkbox" style="font-size: 0.8rem;">
          <input type="checkbox" value="${u.id}" ${checkedValues.includes(u.id) ? 'checked' : ''}>
          <span>${App.Utils.escapeHTML(u.name)}</span>
        </label>
      `).join('');
    }

    // 2. Tipo de Equipamento UO select (Resolve: Mesmo cadastrando as UOs, elas não aparecem no tipo de equipamento)
    const selEquipUO = document.getElementById('selectEquipmentTypeUO');
    if (selEquipUO) {
      const curVal = selEquipUO.value;
      selEquipUO.innerHTML = '<option value="">Selecione a UO...</option>' + 
        activeUOs.map(u => `<option value="${u.id}" ${u.id === curVal ? 'selected' : ''}>${App.Utils.escapeHTML(u.name)}</option>`).join('');
    }

    // 3. TAG UO select
    const selTagUO = document.getElementById('selectTagUO');
    if (selTagUO) {
      const curVal = selTagUO.value;
      selTagUO.innerHTML = '<option value="">Selecione a UO...</option>' + 
        activeUOs.map(u => `<option value="${u.id}" ${u.id === curVal ? 'selected' : ''}>${App.Utils.escapeHTML(u.name)}</option>`).join('');
    }

    // 4. Filtros de UO
    const fillFilter = (id) => {
      const el = document.getElementById(id);
      if (el) {
        const curVal = el.value;
        el.innerHTML = '<option value="">Todas as UOs</option>' + 
          activeUOs.map(u => `<option value="${u.id}" ${u.id === curVal ? 'selected' : ''}>${App.Utils.escapeHTML(u.name)}</option>`).join('');
      }
    };
    fillFilter('filterUO');
    fillFilter('filterCompletedUO');
  },

  // --------------------------------------------------------------------------
  // NAVEGAÇÃO ENTRE VISÕES E SELETORES GLOBAIS
  // --------------------------------------------------------------------------
  bindNavEvents: function() {
    const navButtons = document.querySelectorAll('.app-nav .nav-item');
    navButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const targetView = btn.getAttribute('data-view');
        this.navigateTo(targetView);
      });
    });

    document.getElementById('btnQuickAddEvent')?.addEventListener('click', () => {
      this.resetEventForm();
      this.navigateTo('viewNewEvent');
    });

    // Seletores de Modo de Exibição (Header, Drawer e Configurações)
    ['selectHeaderViewMode', 'selectDrawerViewMode', 'selectSettingsViewMode'].forEach(id => {
      document.getElementById(id)?.addEventListener('change', (e) => {
        this.applyResponsiveLayoutMode(e.target.value, true);
      });
    });

    // Botão Voltar para Automático no banner de aviso de usabilidade
    document.getElementById('btnBannerResetAuto')?.addEventListener('click', () => {
      this.applyResponsiveLayoutMode('auto', true);
      this.showToast('Modo de exibição restaurado para Automático.', 'info');
    });

    // Seletor de Tema Visual nas Configurações
    document.getElementById('selectSettingsTheme')?.addEventListener('change', async (e) => {
      const newTheme = e.target.value;
      const settings = await App.Service.getSettings();
      settings.theme = newTheme;
      await App.Service.saveSettings(settings);
      this.applyTheme(newTheme);
    });

    // Sino de Alarmes no Header Mobile/Tablet
    document.getElementById('btnHeaderAlarmBell')?.addEventListener('click', () => {
      this.navigateTo('viewPendingEvents', () => {
        const fAlarm = document.getElementById('filterAlarm');
        if (fAlarm) fAlarm.value = 'sim';
        this.renderPendingEvents();
      });
    });

    // Mudar usuário local
    document.getElementById('btnControllerBadge')?.addEventListener('click', async () => {
      const settings = await App.Service.getSettings();
      const currentName = settings.localUserName || 'Usuário local';
      const newName = prompt('Informe o nome do controlador neste computador:', currentName);
      if (newName !== null) {
        settings.localUserName = newName.trim() || 'Usuário local';
        await App.Service.saveSettings(settings);
        document.getElementById('headerUserName').textContent = settings.localUserName;
        const inpUser = document.getElementById('inputSettingsUserName');
        if (inpUser) inpUser.value = settings.localUserName;
        this.showToast(`Identificação atualizada: ${settings.localUserName}`, 'info');
      }
    });

    // Alternar Tema (Cicla entre os 3 Temas: Escuro -> Claro -> Industrial Alto Contraste)
    document.getElementById('btnToggleTheme')?.addEventListener('click', () => {
      this.cycleTheme();
    });

    // Métrica cards clicáveis no dashboard
    document.querySelectorAll('.dashboard-metrics .metric-card').forEach(card => {
      card.addEventListener('click', () => {
        const filter = card.getAttribute('data-filter');
        if (filter === 'completed') {
          this.navigateTo('viewCompletedEvents');
        } else {
          this.navigateTo('viewPendingEvents', () => {
            if (filter === 'overdue') {
              document.getElementById('filterStatus').value = 'Atrasado';
            } else if (filter === 'unacknowledged') {
              document.getElementById('filterAlarm').value = 'sim';
            }
            this.renderPendingEvents();
          });
        }
      });
    });
  },

  navigateTo: async function(viewId, callback) {
    document.querySelectorAll('.app-nav .nav-item').forEach(b => {
      b.classList.toggle('active', b.getAttribute('data-view') === viewId);
    });

    document.querySelectorAll('#appMobileDrawer .mobile-nav-link').forEach(b => {
      b.classList.toggle('active', b.getAttribute('data-view') === viewId);
    });

    document.querySelectorAll('#mobileBottomNav .bottom-nav-item[data-target]').forEach(b => {
      b.classList.toggle('active', b.getAttribute('data-target') === viewId);
    });

    document.querySelectorAll('.view-section').forEach(sec => {
      sec.classList.toggle('active', sec.id === viewId);
    });

    this.currentView = viewId;

    if (viewId === 'viewDashboard') {
      await this.renderDashboard();
    } else if (viewId === 'viewPendingEvents') {
      await this.renderPendingEvents();
    } else if (viewId === 'viewCompletedEvents') {
      await this.renderCompletedEvents();
    } else if (viewId === 'viewCadastros') {
      await this.renderCadastros();
    } else if (viewId === 'viewConfigAlerts') {
      await this.renderConfigAlerts();
    } else if (viewId === 'viewConfigColors') {
      await this.renderConfigColors();
    } else if (viewId === 'viewDiagnostic') {
      await this.renderDiagnostic();
    } else if (viewId === 'viewNewEvent') {
      await this.initNewEventCombos();
    }

    if (callback) callback();
  },

  // --------------------------------------------------------------------------
  // FORMULÁRIO DE EVENTOS E COMBOBOXES ENCADEADOS
  // --------------------------------------------------------------------------
  initNewEventCombos: async function() {
    const editId = document.getElementById('eventEditId').value;
    if (!editId) {
      if (!document.getElementById('inputEventDate').value) {
        const now = new Date();
        now.setHours(now.getHours() + 1);
        const y = now.getFullYear();
        const m = String(now.getMonth() + 1).padStart(2, '0');
        const d = String(now.getDate()).padStart(2, '0');
        const hh = String(now.getHours()).padStart(2, '0');
        const mm = String(now.getMinutes()).padStart(2, '0');
        document.getElementById('inputEventDate').value = `${y}-${m}-${d}`;
        document.getElementById('inputEventTime').value = `${hh}:${mm}`;
      }
    }

    await this.syncActiveConsoleUI();
    const consoleId = this.activeConsoleId;

    const keepDutoUO = document.getElementById('checkKeepDutoUO')?.checked;
    const currentPipeId = keepDutoUO ? document.getElementById('selectEventPipeline').value : null;
    const currentUoId = keepDutoUO ? document.getElementById('selectEventUO').value : null;

    await this.loadPipelineOptions(consoleId, 'selectEventPipeline', currentPipeId);
    if (currentPipeId) {
      await this.loadUOOptions(currentPipeId, 'selectEventUO', currentUoId);
    }
  },

  loadConsoleOptions: async function(selectId, selectedId = null, includeInactiveId = null) {
    const select = document.getElementById(selectId);
    if (!select) return;
    const consoles = await App.DB.getAll('consoles');
    consoles.sort((a, b) => a.name.localeCompare(b.name));

    select.innerHTML = '<option value="">Selecione o Console...</option>';
    for (const c of consoles) {
      if (c.active || c.id === includeInactiveId) {
        const opt = document.createElement('option');
        opt.value = c.id;
        opt.textContent = c.name + (c.active ? '' : ' (Inativo)');
        if (c.id === selectedId) opt.selected = true;
        select.appendChild(opt);
      }
    }
  },

  loadPipelineOptions: async function(consoleId, selectId, selectedId = null, includeInactiveId = null) {
    const select = document.getElementById(selectId);
    if (!select) return;

    if (!consoleId) {
      select.innerHTML = '<option value="">Console não definido no topo...</option>';
      select.disabled = true;
      return;
    }

    const pipelines = await App.DB.getAll('pipelines');
    const filtered = pipelines.filter(p => p.consoleId === consoleId);
    filtered.sort((a, b) => a.name.localeCompare(b.name));

    select.innerHTML = '<option value="">Selecione o Duto...</option>';
    for (const p of filtered) {
      if (p.active || p.id === includeInactiveId) {
        const opt = document.createElement('option');
        opt.value = p.id;
        opt.textContent = p.name + (p.active ? '' : ' (Inativo)');
        if (p.id === selectedId) opt.selected = true;
        select.appendChild(opt);
      }
    }
    select.disabled = false;
  },

  loadUOOptions: async function(pipelineId, selectId, selectedId = null, includeInactiveId = null) {
    const select = document.getElementById(selectId);
    if (!select) return;

    if (!pipelineId) {
      select.innerHTML = '<option value="">Selecione primeiro o Duto...</option>';
      select.disabled = true;
      return;
    }

    const links = await App.DB.getAll('pipelineOperationalUnits');
    const uoIds = links.filter(l => l.pipelineId === pipelineId).map(l => l.uoId);

    const allUOs = await App.DB.getAll('operationalUnits');
    const filtered = allUOs.filter(u => uoIds.includes(u.id));
    filtered.sort((a, b) => a.name.localeCompare(b.name));

    select.innerHTML = '<option value="">Selecione a UO...</option>';
    for (const u of filtered) {
      if (u.active || u.id === includeInactiveId) {
        const opt = document.createElement('option');
        opt.value = u.id;
        opt.textContent = u.name + (u.active ? '' : ' (Inativo)');
        if (u.id === selectedId) opt.selected = true;
        select.appendChild(opt);
      }
    }
    select.disabled = false;
  },

  loadEquipmentTypeOptions: async function(uoId, selectId, selectedId = null, includeInactiveId = null) {
    const select = document.getElementById(selectId);
    if (!select) return;

    if (!uoId) {
      select.innerHTML = '<option value="">Geral da UO / Não aplicável</option>';
      select.disabled = true;
      return;
    }

    const types = await App.DB.getAll('equipmentTypes');
    const filtered = types.filter(t => t.uoId === uoId);
    filtered.sort((a, b) => a.name.localeCompare(b.name));

    select.innerHTML = '<option value="">Geral da UO / Não aplicável</option>';
    for (const t of filtered) {
      if (t.active || t.id === includeInactiveId) {
        const opt = document.createElement('option');
        opt.value = t.id;
        opt.textContent = t.name + (t.active ? '' : ' (Inativo)');
        if (t.id === selectedId) opt.selected = true;
        select.appendChild(opt);
      }
    }
    select.disabled = false;
  },

  loadEquipmentTagOptions: async function(uoId, typeId, selectId, selectedId = null, includeInactiveId = null) {
    const select = document.getElementById(selectId);
    if (!select) return;

    if (!uoId || !typeId) {
      select.innerHTML = '<option value="">Selecione o Tipo primeiro...</option>';
      select.disabled = true;
      return;
    }

    const tags = await App.DB.getAll('equipmentTags');
    const filtered = tags.filter(t => t.uoId === uoId && t.equipmentTypeId === typeId);
    filtered.sort((a, b) => a.tag.localeCompare(b.tag));

    select.innerHTML = '<option value="">Selecione o TAG...</option>';
    for (const t of filtered) {
      if (t.active || t.id === includeInactiveId) {
        const opt = document.createElement('option');
        opt.value = t.id;
        opt.textContent = t.tag + (t.active ? '' : ' (Inativo)');
        if (t.id === selectedId) opt.selected = true;
        select.appendChild(opt);
      }
    }
    select.disabled = false;
  },

  // --------------------------------------------------------------------------
  // BINDING DE FORMULÁRIOS
  // --------------------------------------------------------------------------
  bindFormEvents: function() {
    const selPipeline = document.getElementById('selectEventPipeline');
    const selUO = document.getElementById('selectEventUO');
    const selType = document.getElementById('selectEventEquipmentType');
    const selTag = document.getElementById('selectEventTag');
    const cascadeStatus = document.getElementById('cascadeStatusText');

    selPipeline?.addEventListener('change', async () => {
      const pipelineId = selPipeline.value;
      await this.loadUOOptions(pipelineId, 'selectEventUO');
      selType.innerHTML = '<option value="">Geral da UO / Não aplicável</option>';
      selType.disabled = true;
      selTag.innerHTML = '<option value="">Selecione o Tipo primeiro...</option>';
      selTag.disabled = true;
      if (cascadeStatus) {
        const uoCount = Math.max(0, selUO.options.length - 1);
        cascadeStatus.textContent = pipelineId ? `✓ ${uoCount} UO(s) carregada(s) para o duto selecionado.` : '';
      }
    });

    selUO?.addEventListener('change', async () => {
      const uoId = selUO.value;
      await this.loadEquipmentTypeOptions(uoId, 'selectEventEquipmentType');
      selTag.innerHTML = '<option value="">Selecione o Tipo primeiro...</option>';
      selTag.disabled = true;
      if (cascadeStatus) {
        const typeCount = Math.max(0, selType.options.length - 1);
        cascadeStatus.textContent = uoId ? `✓ ${typeCount} Tipo(s) de equipamento disponível(is) na UO.` : '';
      }
    });

    selType?.addEventListener('change', async () => {
      const uoId = selUO.value;
      const typeId = selType.value;
      await this.loadEquipmentTagOptions(uoId, typeId, 'selectEventTag');
      if (cascadeStatus) {
        const tagCount = Math.max(0, selTag.options.length - 1);
        cascadeStatus.textContent = typeId ? `✓ ${tagCount} TAG(s) disponível(is) para o tipo selecionado.` : '';
      }
    });

    // Toggle de configurações customizadas de alarme
    const chkAlarmActive = document.getElementById('checkEventAlarmActive');
    const chkUseDefault = document.getElementById('checkEventUseDefaultAlarm');
    const boxCustomAlarm = document.getElementById('boxCustomAlarmSettings');
    const wrapUseDefault = document.getElementById('wrapperUseDefaultAlarm');

    const updateAlarmFieldsVisibility = () => {
      if (!chkAlarmActive.checked) {
        wrapUseDefault.style.display = 'none';
        boxCustomAlarm.style.display = 'none';
      } else {
        wrapUseDefault.style.display = 'flex';
        boxCustomAlarm.style.display = chkUseDefault.checked ? 'none' : 'grid';
      }
    };

    chkAlarmActive?.addEventListener('change', updateAlarmFieldsVisibility);
    chkUseDefault?.addEventListener('change', updateAlarmFieldsVisibility);

    // Submissão do Evento (Normal e "Salvar e Inserir Outra neste Duto")
    const saveEventHandler = async (continueOnPipeline = false) => {
      const btn = continueOnPipeline ? document.getElementById('btnSubmitAndNew') : document.getElementById('btnSubmitEvent');
      if (btn) btn.disabled = true;

      try {
        const editId = document.getElementById('eventEditId').value;
        const consoleId = this.activeConsoleId || document.getElementById('eventConsoleId').value;
        if (!consoleId) {
          throw new Error('Selecione um Console Operacional no topo da tela.');
        }

        const scheduledTimeVal = document.getElementById('inputEventTime').value;

        const eventData = {
          id: editId || undefined,
          consoleId: consoleId,
          pipelineId: selPipeline.value,
          uoId: selUO.value,
          equipmentTypeId: selType.value || null,
          tagId: selTag.value || null,
          scheduledDate: document.getElementById('inputEventDate').value,
          scheduledTime: scheduledTimeVal,
          priority: document.getElementById('selectEventPriority').value,
          description: document.getElementById('inputEventDescription').value,
          notes: document.getElementById('inputEventNotes').value,
          stylusDrawing: this.getStylusData(),
          hasAlarm: chkAlarmActive.checked,
          useDefaultAlarmSettings: chkUseDefault.checked,
          alarmMinutesBefore: document.getElementById('inputEventAlarmLeadTime').value,
          alarmAudio: document.getElementById('checkEventAlertSound').checked,
          alarmVisual: document.getElementById('checkEventAlertVisual').checked,
          alarmNotification: document.getElementById('checkEventAlertNotif').checked,
          alarmRepeat: document.getElementById('checkEventAlertRepeat').checked,
          alarmRepeatInterval: document.getElementById('inputEventAlertRepeatInterval').value,
          alarmMaxRepeats: document.getElementById('inputEventAlertMaxRepeats').value
        };

        await App.Service.saveEvent(eventData);

        if (continueOnPipeline) {
          this.showToast('Previsão salva com sucesso! Pronto para nova previsão no duto.', 'success');
          if (scheduledTimeVal && scheduledTimeVal.includes(':')) {
            const [hh, mm] = scheduledTimeVal.split(':').map(Number);
            let totalM = (hh * 60 + mm + 30) % 1440;
            const newH = String(Math.floor(totalM / 60)).padStart(2, '0');
            const newM = String(totalM % 60).padStart(2, '0');
            document.getElementById('inputEventTime').value = `${newH}:${newM}`;
          }
          document.getElementById('inputEventDescription').value = '';
          document.getElementById('inputEventNotes').value = '';
          document.getElementById('eventEditId').value = '';
          this.clearStylusPad();
          document.getElementById('inputEventDescription').focus();
        } else {
          this.showToast(editId ? 'Previsão operacional atualizada!' : 'Previsão operacional cadastrada!', 'success');
          const keepDutoUO = document.getElementById('checkKeepDutoUO')?.checked;
          if (!keepDutoUO) {
            this.resetEventForm();
          } else {
            document.getElementById('inputEventDescription').value = '';
            document.getElementById('inputEventNotes').value = '';
            document.getElementById('eventEditId').value = '';
            this.clearStylusPad();
          }
          this.navigateTo('viewPendingEvents');
        }
      } catch (err) {
        this.showToast(err.message, 'danger');
      } finally {
        if (btn) btn.disabled = false;
      }
    };

    const formEvent = document.getElementById('formEvent');
    formEvent?.addEventListener('submit', async (e) => {
      e.preventDefault();
      await saveEventHandler(false);
    });

    document.getElementById('btnSubmitAndNew')?.addEventListener('click', async (e) => {
      e.preventDefault();
      await saveEventHandler(true);
    });

    document.getElementById('btnResetEventForm')?.addEventListener('click', () => {
      this.resetEventForm();
    });

    document.getElementById('btnCancelEditEvent')?.addEventListener('click', () => {
      this.resetEventForm();
      this.navigateTo('viewPendingEvents');
    });

    // Submissões de Cadastros
    this.bindCadastrosForms();

    // Configurações de Alertas, Exibição e Tema
    const formAlerts = document.getElementById('formAlertSettings');
    formAlerts?.addEventListener('submit', async (e) => {
      e.preventDefault();
      try {
        const settings = await App.Service.getSettings();
        settings.localUserName = document.getElementById('inputSettingsUserName').value.trim() || 'Usuário local';
        settings.defaultLeadTimeMinutes = parseInt(document.getElementById('inputDefaultLeadTime').value, 10) || 15;
        settings.soundType = document.getElementById('selectSoundType').value;
        settings.soundVolume = parseInt(document.getElementById('rangeSoundVolume').value, 10) || 80;
        settings.soundEnabled = document.getElementById('checkSettingSound').checked;
        settings.visualAlertEnabled = document.getElementById('checkSettingVisualModal').checked;
        settings.highlightCardEnabled = document.getElementById('checkSettingHighlightCard').checked;
        settings.pulsingEnabled = document.getElementById('checkSettingPulsing').checked;
        settings.changeTitleEnabled = document.getElementById('checkSettingChangeTitle').checked;
        settings.notificationEnabled = document.getElementById('checkSettingNotification').checked;
        settings.repeatAlarm = document.getElementById('checkSettingRepeat').checked;
        settings.repeatIntervalMinutes = parseInt(document.getElementById('inputSettingRepeatInterval').value, 10) || 2;
        settings.maxRepeats = parseInt(document.getElementById('inputSettingMaxRepeats').value, 10) || 5;

        const selViewMode = document.getElementById('selectSettingsViewMode');
        if (selViewMode) {
          settings.responsiveLayoutMode = selViewMode.value;
          await this.applyResponsiveLayoutMode(selViewMode.value, false);
        }

        const selTheme = document.getElementById('selectSettingsTheme');
        if (selTheme) {
          settings.theme = selTheme.value;
          this.applyTheme(selTheme.value);
        }

        await App.Service.saveSettings(settings);
        document.getElementById('headerUserName').textContent = settings.localUserName;
        this.showToast('Configurações salvas com sucesso!', 'success');
      } catch (err) {
        this.showToast(err.message, 'danger');
      }
    });

    // Volume Slider
    document.getElementById('rangeSoundVolume')?.addEventListener('input', (e) => {
      document.getElementById('labelVolumeValue').textContent = `${e.target.value}%`;
    });

    // Testes de Alertas
    const triggerSoundTest = () => {
      const type = document.getElementById('selectSoundType')?.value || 'chime';
      const vol = parseInt(document.getElementById('rangeSoundVolume')?.value || '80', 10);
      App.Audio.unlock();
      App.Audio.play(type, vol);
      this.showToast(`Sinal sonoro "${type}" executado.`, 'info');
    };
    document.getElementById('btnTestSound')?.addEventListener('click', triggerSoundTest);
    document.getElementById('btnStatusModalTestAudio')?.addEventListener('click', triggerSoundTest);

    document.getElementById('btnTestVisual')?.addEventListener('click', () => {
      this.showAlarmModal({
        id: 'test-event',
        description: 'Verificar término do recebimento de Diesel S10 (Evento de Teste)',
        notes: 'Alerta visual de demonstração do sistema.',
        scheduledDate: new Date().toISOString().substring(0, 10),
        scheduledTime: App.Utils.formatTime(new Date()),
        scheduledAt: new Date(Date.now() + 600000).toISOString()
      }, true);
    });

    document.getElementById('btnRequestNotifPermission')?.addEventListener('click', async () => {
      await App.Notifications.requestPermission();
    });

    // Botões de Testar Notificação do Navegador (No Topo, Modal Status e Configurações)
    const runNotifTest = async () => {
      App.Audio.unlock();
      App.Audio.play('chime');
      const perm = App.Notifications.getPermissionState();
      if (perm !== 'concedida') {
        const granted = await App.Notifications.requestPermission();
        if (!granted) {
          this.showToast('Permissão de notificação negada ou não concedida no navegador.', 'warning');
          return;
        }
      }
      const sent = App.Notifications.send('Teste de Alerta Operacional', {
        body: 'Notificação do navegador validada com sucesso! Caderno de Previsões em Dutos.'
      });
      if (sent) {
        this.showToast('Notificação do navegador disparada com sucesso!', 'success');
      } else {
        this.showToast('Notificação não enviada. Verifique as permissões do navegador.', 'warning');
      }
    };

    document.getElementById('btnHeaderTestNotif')?.addEventListener('click', runNotifTest);
    document.getElementById('btnTestNotif')?.addEventListener('click', runNotifTest);
    document.getElementById('btnStatusModalTestNotif')?.addEventListener('click', runNotifTest);

    document.getElementById('btnResetAlertSettings')?.addEventListener('click', async () => {
      this.showConfirmModal('Restaurar Configurações', 'Deseja restaurar as configurações padrão de alerta?', async () => {
        await App.Service.saveSettings({ ...App.Config.DEFAULT_SETTINGS });
        this.applyTheme('dark');
        await this.applyResponsiveLayoutMode('auto', false);
        await this.renderConfigAlerts();
        this.showToast('Configurações padrão restauradas.', 'success');
      });
    });

    // Faixas de Cores
    const formColorRange = document.getElementById('formColorRange');
    const inputColor = document.getElementById('inputRangeColor');
    const inputColorText = document.getElementById('inputRangeColorText');
    inputColor?.addEventListener('input', () => { inputColorText.value = inputColor.value; });
    inputColorText?.addEventListener('input', () => { inputColor.value = inputColorText.value; });

    formColorRange?.addEventListener('submit', async (e) => {
      e.preventDefault();
      try {
        const id = document.getElementById('rangeEditId').value;
        const data = {
          id: id || undefined,
          name: document.getElementById('inputRangeName').value,
          color: inputColor.value,
          minMinutes: parseInt(document.getElementById('inputRangeMin').value, 10),
          maxMinutes: parseInt(document.getElementById('inputRangeMax').value, 10),
          priority: parseInt(document.getElementById('inputRangePriority').value, 10),
          blink: document.getElementById('checkRangeBlink').checked,
          sound: document.getElementById('checkRangeSound').checked
        };
        await App.Service.saveColorRange(data);
        this.showToast('Faixa de cor salva com sucesso!', 'success');
        this.resetRangeForm();
        await this.renderConfigColors();
      } catch (err) {
        this.showToast(err.message, 'danger');
      }
    });

    document.getElementById('btnCancelRangeEdit')?.addEventListener('click', () => {
      this.resetRangeForm();
    });

    document.getElementById('btnResetColorRanges')?.addEventListener('click', () => {
      this.showConfirmModal('Restaurar Cores Padrão', 'Deseja restaurar as faixas de cores para o padrão de fábrica?', async () => {
        await App.Service.resetColorRanges();
        await this.renderConfigColors();
        this.showToast('Faixas de cores restauradas para o padrão.', 'success');
      });
    });

    // Backup & Exportação (Unificado para todos os IDs do HTML e Legados — Seção 24 Item 5)
    const handleExportJSON = async () => {
      try {
        await App.Backup.exportJSON();
        const settings = await App.Service.getSettings();
        this.updateBackupPill(settings.lastBackupAt);
        this.showToast('Backup JSON exportado com sucesso!', 'success');
      } catch (err) {
        this.showToast('Erro ao exportar backup: ' + err.message, 'danger');
      }
    };
    document.getElementById('btnExportJSON')?.addEventListener('click', handleExportJSON);
    document.getElementById('btnExportBackup')?.addEventListener('click', handleExportJSON);

    const fileInput = document.getElementById('inputImportBackupFile') || document.getElementById('fileInputRestore');
    const btnValidateImport = document.getElementById('btnTriggerImportValidate');

    fileInput?.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (btnValidateImport) {
        btnValidateImport.disabled = !file;
      }
    });

    const handleValidateFile = async () => {
      const file = fileInput?.files?.[0];
      if (!file) {
        this.showToast('Selecione um arquivo JSON de backup primeiro.', 'warning');
        return;
      }
      try {
        const parsed = await App.Backup.validateBackupFile(file);
        this.showImportSummaryModal(parsed);
      } catch (err) {
        this.showToast(err.message, 'danger');
      }
    };
    btnValidateImport?.addEventListener('click', handleValidateFile);
    document.getElementById('btnTriggerRestore')?.addEventListener('click', () => fileInput?.click());

    // Exportações CSV (Pendentes, Concluídos, Cadastros e Todos — Seção 24 Item 6)
    const handleExportPendingCSV = async () => { await App.Backup.exportCSV('pendente'); };
    const handleExportCompletedCSV = async () => { await App.Backup.exportCSV('concluido'); };
    const handleExportCadastrosCSV = async () => { await App.Backup.exportCSV('cadastros'); };
    const handleExportAllCSV = async () => { await App.Backup.exportCSV('todos'); };

    document.getElementById('btnExportCSVAllPending')?.addEventListener('click', handleExportPendingCSV);
    document.getElementById('btnExportPendingCSV')?.addEventListener('click', handleExportPendingCSV);
    document.getElementById('btnExportCSVAllCompleted')?.addEventListener('click', handleExportCompletedCSV);
    document.getElementById('btnExportCompletedCSV')?.addEventListener('click', handleExportCompletedCSV);
    document.getElementById('btnExportCSVCadastros')?.addEventListener('click', handleExportCadastrosCSV);
    document.getElementById('btnExportAllEventsCSV')?.addEventListener('click', handleExportAllCSV);

    // Carregar Dados de Demonstração
    document.getElementById('btnLoadDemoData')?.addEventListener('click', () => {
      this.showConfirmModal(
        'Carregar Dados de Demonstração',
        'Deseja recarregar os dados operacionais de demonstração (Consoles C02-C16, Dutos, UOs, TAGs e Eventos de exemplo)?',
        async () => {
          await App.Service.clearAllData();
          this.showToast('Massa de dados de demonstração carregada com sucesso!', 'success');
          await this.initHeaderConsole();
          await this.renderDashboard();
        }
      );
    });

    document.getElementById('btnWipeAllData')?.addEventListener('click', () => {
      this.showConfirmModal(
        'APAGAR TODOS OS DADOS',
        'ATENÇÃO: Esta ação apagará permanentemente todos os eventos, cadastros e históricos locais. Deseja realmente prosseguir?',
        async () => {
          await App.Service.clearAllData();
          this.showToast('Todos os dados foram apagados e a base reiniciada.', 'warning');
          await this.renderDashboard();
        }
      );
    });

    // Diagnóstico
    document.getElementById('btnCopyDiagnostic')?.addEventListener('click', async () => {
      const diagData = await this.getDiagnosticReport();
      navigator.clipboard.writeText(JSON.stringify(diagData, null, 2)).then(() => {
        this.showToast('Relatório de diagnóstico copiado para a área de transferência!', 'success');
      }).catch(err => {
        this.showToast('Falha ao copiar diagnóstico: ' + err.message, 'danger');
      });
    });

    document.getElementById('btnClearDiagLogs')?.addEventListener('click', async () => {
      await App.DB.clear('errorLogs');
      await this.renderDiagnostic();
      this.showToast('Logs de diagnóstico limpos.', 'info');
    });
  },

  resetEventForm: function() {
    document.getElementById('eventEditId').value = '';
    document.getElementById('formEvent').reset();
    document.getElementById('formEventTitle').textContent = 'Cadastrar Previsão Operacional';
    document.getElementById('btnSubmitEventText').textContent = 'Salvar Previsão';
    document.getElementById('btnCancelEditEvent').style.display = 'none';
    document.getElementById('navNewEventLabel').textContent = 'Novo Evento';

    const selPipeline = document.getElementById('selectEventPipeline');
    const selUO = document.getElementById('selectEventUO');
    const selType = document.getElementById('selectEventEquipmentType');
    const selTag = document.getElementById('selectEventTag');

    selPipeline.innerHTML = '<option value="">Selecione o Duto...</option>';
    selUO.innerHTML = '<option value="">Selecione primeiro o Duto...</option>';
    selUO.disabled = true;
    selType.innerHTML = '<option value="">Geral da UO / Não aplicável</option>';
    selType.disabled = true;
    selTag.innerHTML = '<option value="">Selecione o Tipo primeiro...</option>';
    selTag.disabled = true;

    document.getElementById('boxCustomAlarmSettings').style.display = 'none';
    document.getElementById('wrapperUseDefaultAlarm').style.display = 'flex';
    this.clearStylusPad();
  },

  editEvent: async function(eventId) {
    const event = await App.DB.get('events', eventId);
    if (!event) return;

    this.resetEventForm();
    document.getElementById('eventEditId').value = event.id;
    document.getElementById('formEventTitle').textContent = 'Editar Previsão Operacional';
    document.getElementById('btnSubmitEventText').textContent = 'Atualizar Previsão';
    document.getElementById('btnCancelEditEvent').style.display = 'inline-flex';
    document.getElementById('navNewEventLabel').textContent = 'Editar Evento';

    // Ajusta console se for diferente
    if (event.consoleId && event.consoleId !== this.activeConsoleId) {
      this.activeConsoleId = event.consoleId;
      const selHeader = document.getElementById('headerActiveConsole');
      if (selHeader) selHeader.value = event.consoleId;
      await this.syncActiveConsoleUI();
    }

    await this.loadPipelineOptions(event.consoleId, 'selectEventPipeline', event.pipelineId, event.pipelineId);
    await this.loadUOOptions(event.pipelineId, 'selectEventUO', event.uoId, event.uoId);
    await this.loadEquipmentTypeOptions(event.uoId, 'selectEventEquipmentType', event.equipmentTypeId, event.equipmentTypeId);
    await this.loadEquipmentTagOptions(event.uoId, event.equipmentTypeId, 'selectEventTag', event.tagId, event.tagId);

    document.getElementById('inputEventDate').value = event.scheduledDate;
    document.getElementById('inputEventTime').value = event.scheduledTime;
    document.getElementById('selectEventPriority').value = event.priority || 'Normal';
    document.getElementById('inputEventDescription').value = event.description;
    document.getElementById('inputEventNotes').value = event.notes || '';

    const chkAlarm = document.getElementById('checkEventAlarmActive');
    const chkDefault = document.getElementById('checkEventUseDefaultAlarm');
    chkAlarm.checked = event.hasAlarm;
    chkDefault.checked = event.useDefaultAlarmSettings;

    document.getElementById('inputEventAlarmLeadTime').value = event.alarmMinutesBefore || 15;
    document.getElementById('checkEventAlertSound').checked = event.alarmAudio !== false;
    document.getElementById('checkEventAlertVisual').checked = event.alarmVisual !== false;
    document.getElementById('checkEventAlertNotif').checked = !!event.alarmNotification;
    document.getElementById('checkEventAlertRepeat').checked = !!event.alarmRepeat;
    document.getElementById('inputEventAlertRepeatInterval').value = event.alarmRepeatInterval || 2;
    document.getElementById('inputEventAlertMaxRepeats').value = event.alarmMaxRepeats || 5;

    document.getElementById('boxCustomAlarmSettings').style.display = (!event.hasAlarm || event.useDefaultAlarmSettings) ? 'none' : 'grid';
    document.getElementById('wrapperUseDefaultAlarm').style.display = event.hasAlarm ? 'flex' : 'none';

    if (event.stylusDrawing) {
      this.loadStylusData(event.stylusDrawing);
    }

    this.navigateTo('viewNewEvent');
  },

  duplicateEvent: async function(eventId) {
    try {
      const clone = await App.Service.getCloneDataForEvent(eventId);
      this.resetEventForm();

      if (clone.consoleId && clone.consoleId !== this.activeConsoleId) {
        this.activeConsoleId = clone.consoleId;
        const selHeader = document.getElementById('headerActiveConsole');
        if (selHeader) selHeader.value = clone.consoleId;
        await this.syncActiveConsoleUI();
      }

      await this.loadPipelineOptions(clone.consoleId, 'selectEventPipeline', clone.pipelineId);
      await this.loadUOOptions(clone.pipelineId, 'selectEventUO', clone.uoId);
      await this.loadEquipmentTypeOptions(clone.uoId, 'selectEventEquipmentType', clone.equipmentTypeId);
      await this.loadEquipmentTagOptions(clone.uoId, clone.equipmentTypeId, 'selectEventTag', clone.tagId);

      document.getElementById('inputEventDate').value = clone.scheduledDate;
      document.getElementById('inputEventTime').value = clone.scheduledTime;
      document.getElementById('selectEventPriority').value = clone.priority || 'Normal';
      document.getElementById('inputEventDescription').value = clone.description;
      document.getElementById('inputEventNotes').value = clone.notes || '';

      const chkAlarm = document.getElementById('checkEventAlarmActive');
      const chkDefault = document.getElementById('checkEventUseDefaultAlarm');
      chkAlarm.checked = clone.hasAlarm;
      chkDefault.checked = clone.useDefaultAlarmSettings;

      document.getElementById('inputEventAlarmLeadTime').value = clone.alarmMinutesBefore || 15;
      document.getElementById('checkEventAlertSound').checked = clone.alarmAudio !== false;
      document.getElementById('checkEventAlertVisual').checked = clone.alarmVisual !== false;
      document.getElementById('checkEventAlertNotif').checked = !!clone.alarmNotification;
      document.getElementById('checkEventAlertRepeat').checked = !!clone.alarmRepeat;
      document.getElementById('inputEventAlertRepeatInterval').value = clone.alarmRepeatInterval || 2;
      document.getElementById('inputEventAlertMaxRepeats').value = clone.alarmMaxRepeats || 5;

      document.getElementById('boxCustomAlarmSettings').style.display = (!clone.hasAlarm || clone.useDefaultAlarmSettings) ? 'none' : 'grid';
      document.getElementById('wrapperUseDefaultAlarm').style.display = clone.hasAlarm ? 'flex' : 'none';

      if (clone.stylusDrawing) {
        this.loadStylusData(clone.stylusDrawing);
      }

      this.navigateTo('viewNewEvent');
      this.showToast('Dados duplicados! Ajuste o horário ou informações conforme necessário.', 'info');
    } catch (err) {
      this.showToast(err.message, 'danger');
    }
  },

  // --------------------------------------------------------------------------
  // BINDING DE FILTROS E EVENTOS DE BUSCA
  // --------------------------------------------------------------------------
  bindFilterEvents: function() {
    const inputSearch = document.getElementById('inputSearchPending');
    const btnToggle = document.getElementById('btnToggleFilters');
    const filterDrawer = document.getElementById('filterDrawer');
    const btnClear = document.getElementById('btnClearFilters');
    const selectSort = document.getElementById('selectSortPending');
    const chkConsoleOnly = document.getElementById('checkFilterOnlyActiveConsole');

    inputSearch?.addEventListener('input', () => this.renderPendingEvents());
    selectSort?.addEventListener('change', () => this.renderPendingEvents());
    chkConsoleOnly?.addEventListener('change', () => this.renderPendingEvents());

    btnToggle?.addEventListener('click', () => {
      const isVisible = filterDrawer.style.display !== 'none';
      filterDrawer.style.display = isVisible ? 'none' : 'grid';
      btnToggle.classList.toggle('btn-secondary', !isVisible);
    });

    document.getElementById('btnCloseFilterSheet')?.addEventListener('click', () => {
      if (filterDrawer) filterDrawer.style.display = 'none';
      btnToggle?.classList.remove('btn-secondary');
    });

    document.getElementById('btnSheetApplyFilters')?.addEventListener('click', () => {
      if (filterDrawer) filterDrawer.style.display = 'none';
      btnToggle?.classList.remove('btn-secondary');
      this.renderPendingEvents();
    });

    document.getElementById('btnSheetClearFilters')?.addEventListener('click', () => {
      btnClear?.click();
      if (filterDrawer) filterDrawer.style.display = 'none';
      btnToggle?.classList.remove('btn-secondary');
    });

    const filterInputs = [
      'filterConsole', 'filterPipeline', 'filterUO', 'filterStatus',
      'filterAlarm', 'filterPriority', 'filterDateFrom', 'filterDateTo'
    ];
    filterInputs.forEach(id => {
      document.getElementById(id)?.addEventListener('change', () => this.renderPendingEvents());
    });

    btnClear?.addEventListener('click', () => {
      if (inputSearch) inputSearch.value = '';
      if (selectSort) selectSort.value = 'cronologica';
      filterInputs.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = '';
      });
      this.renderPendingEvents();
    });

    // Alternador de Visualização (Cartões vs Tabela Compacta)
    document.getElementById('btnViewCards')?.addEventListener('click', async () => {
      this.viewMode = 'cards';
      this.updateViewModeUI();
      const settings = await App.Service.getSettings();
      settings.viewMode = 'cards';
      await App.Service.saveSettings(settings);
    });

    document.getElementById('btnViewTable')?.addEventListener('click', async () => {
      this.viewMode = 'table';
      this.updateViewModeUI();
      const settings = await App.Service.getSettings();
      settings.viewMode = 'table';
      await App.Service.saveSettings(settings);
    });

    // Filtros de Eventos Concluídos
    document.getElementById('inputSearchCompleted')?.addEventListener('input', () => this.renderCompletedEvents());
    ['filterCompletedConsole', 'filterCompletedPipeline', 'filterCompletedUO', 'filterCompletedTiming', 'filterCompletedDateFrom', 'filterCompletedDateTo'].forEach(id => {
      document.getElementById(id)?.addEventListener('change', () => this.renderCompletedEvents());
    });
  },

  updateViewModeUI: function() {
    const btnCards = document.getElementById('btnViewCards');
    const btnTable = document.getElementById('btnViewTable');
    const containerCards = document.getElementById('containerPendingCards');
    const containerTable = document.getElementById('containerPendingTable');

    if (this.viewMode === 'cards') {
      btnCards?.classList.replace('btn-outline', 'btn-secondary');
      btnTable?.classList.replace('btn-secondary', 'btn-outline');
      if (containerCards) containerCards.style.display = 'grid';
      if (containerTable) containerTable.style.display = 'none';
    } else {
      btnTable?.classList.replace('btn-outline', 'btn-secondary');
      btnCards?.classList.replace('btn-secondary', 'btn-outline');
      if (containerCards) containerCards.style.display = 'none';
      if (containerTable) containerTable.style.display = 'block';
    }
  },

  // --------------------------------------------------------------------------
  // RENDERIZAÇÃO: PAINEL PRINCIPAL (DASHBOARD)
  // --------------------------------------------------------------------------
  renderDashboard: async function() {
    const allEvents = await App.DB.getAll('events');
    const colorRanges = await App.Service.getColorRanges();
    const consoles = await App.DB.getAll('consoles');
    const pipelines = await App.DB.getAll('pipelines');
    const uos = await App.DB.getAll('operationalUnits');
    const tags = await App.DB.getAll('equipmentTags');

    const consoleMap = new Map(consoles.map(c => [c.id, c.name]));
    const pipeMap = new Map(pipelines.map(p => [p.id, p.name]));
    const uoMap = new Map(uos.map(u => [u.id, u.name]));
    const tagMap = new Map(tags.map(t => [t.id, t.tag]));

    const pending = allEvents.filter(e => e.status === 'pendente' && e.active !== false);
    const completed = allEvents.filter(e => e.status === 'concluido' && e.active !== false);

    // Métricas
    const nowTime = Date.now();
    let overdueCount = 0;
    let next15Count = 0;
    let next30Count = 0;
    let next60Count = 0;
    let unackAlarmsCount = 0;

    for (const ev of pending) {
      const scheduledTime = new Date(ev.scheduledAt).getTime();
      const diffMs = scheduledTime - nowTime;
      const diffMins = diffMs / 60000;

      if (diffMs < 0) {
        overdueCount++;
      } else if (diffMins <= 15) {
        next15Count++;
      } else if (diffMins <= 30) {
        next30Count++;
      } else if (diffMins <= 60) {
        next60Count++;
      }

      if (ev.alarmState === 'triggered') {
        unackAlarmsCount++;
      }
    }

    // Concluídos hoje
    const todayStr = new Date().toISOString().substring(0, 10);
    const completedTodayCount = completed.filter(e => e.completedAt && e.completedAt.startsWith(todayStr)).length;

    // Atualizar Contadores
    document.getElementById('metricTotalPending').textContent = pending.length;
    document.getElementById('metricOverdue').textContent = overdueCount;
    document.getElementById('metricNext15').textContent = next15Count;
    document.getElementById('metricNext30').textContent = next30Count;
    document.getElementById('metricNext60').textContent = next60Count;
    document.getElementById('metricCompletedToday').textContent = completedTodayCount;
    document.getElementById('metricUnacknowledged').textContent = unackAlarmsCount;

    // Atualizar Todos os Badges de Pendentes (Fix #4 da Seção 24)
    ['badgePendingCount', 'badgePendingNavCount', 'badgePendingDrawer', 'badgePendingNavCountDrawer', 'badgeBottomNavPending'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.textContent = pending.length;
    });

    // Atualizar Sino de Alarme no Cabeçalho e Banner Persistente Mobile
    const headerBell = document.getElementById('btnHeaderAlarmBell');
    const headerAlarmBadge = document.getElementById('headerAlarmBadge');
    if (headerAlarmBadge) {
      headerAlarmBadge.textContent = unackAlarmsCount;
      headerAlarmBadge.style.display = unackAlarmsCount > 0 ? 'inline-block' : 'none';
    }
    if (headerBell) {
      headerBell.classList.toggle('has-active-alarm', unackAlarmsCount > 0);
    }

    const mobileAlarmsBanner = document.getElementById('mobileActiveAlarmsBanner');
    const mobileAlarmsText = document.getElementById('mobileActiveAlarmsText');
    if (mobileAlarmsBanner) {
      if (unackAlarmsCount > 0) {
        mobileAlarmsBanner.style.display = 'flex';
        if (mobileAlarmsText) {
          mobileAlarmsText.textContent = `${unackAlarmsCount} Alarme(s) Ativo(s) Não Reconhecido(s)`;
        }
      } else {
        mobileAlarmsBanner.style.display = 'none';
      }
    }

    // Ordenar pendentes cronologicamente para Spotlight e Urgentes
    pending.sort((a, b) => new Date(a.scheduledAt).getTime() - new Date(b.scheduledAt).getTime());

    // Painel Lateral de Alarmes Ativos (Tablet)
    const tabletAlarmsList = document.getElementById('tabletAlarmsList');
    const badgeTabletAlarms = document.getElementById('badgeTabletAlarmsCount');
    const activeAlarmEvents = pending.filter(e => e.alarmState === 'triggered' || (new Date(e.scheduledAt).getTime() - nowTime) / 60000 <= 15);
    if (badgeTabletAlarms) badgeTabletAlarms.textContent = activeAlarmEvents.length;
    if (tabletAlarmsList) {
      if (activeAlarmEvents.length === 0) {
        tabletAlarmsList.innerHTML = `<div style="color: var(--text-muted); font-size: 0.82rem; text-align: center; padding: 1rem;">Nenhum alarme crítico disparado no momento.</div>`;
      } else {
        tabletAlarmsList.innerHTML = activeAlarmEvents.slice(0, 4).map(ev => {
          const cl = App.Service.classifyEvent(ev, colorRanges);
          const tInfo = App.Utils.formatTimeRemaining(new Date(ev.scheduledAt).getTime());
          return `
            <div style="padding: 0.6rem; border-radius: var(--radius-sm); background: rgba(0,0,0,0.2); border-left: 3px solid ${cl.color}; margin-bottom: 0.5rem;">
              <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem; margin-bottom: 0.25rem;">
                <strong>${App.Utils.escapeHTML(consoleMap.get(ev.consoleId) || '')} &bull; ${App.Utils.escapeHTML(uoMap.get(ev.uoId) || '')}</strong>
                <span style="color: ${cl.color}; font-weight: 700;">${tInfo.text}</span>
              </div>
              <div style="font-size: 0.82rem; font-weight: 600; margin-bottom: 0.4rem;">${App.Utils.escapeHTML(ev.description)}</div>
              <div style="display: flex; gap: 0.35rem; flex-wrap: wrap;">
                ${ev.alarmState === 'triggered' ? `<button class="btn btn-warning btn-sm" style="padding: 0.2rem 0.5rem; font-size: 0.72rem;" onclick="App.UI.acknowledgeAlarm('${ev.id}')">Reconhecer</button>` : ''}
                <button class="btn btn-secondary btn-sm" style="padding: 0.2rem 0.5rem; font-size: 0.72rem;" onclick="App.UI.showSnoozeModal('${ev.id}')">Adiar 5m</button>
                <button class="btn btn-success btn-sm" style="padding: 0.2rem 0.5rem; font-size: 0.72rem;" onclick="App.UI.showCompleteModal('${ev.id}')">Concluir</button>
              </div>
            </div>
          `;
        }).join('');
      }
    }

    // Spotlight: Próximo Evento (dando preferência ao console ativo se houver)
    const spotlightTarget = (this.activeConsoleId ? pending.find(e => e.consoleId === this.activeConsoleId) : null) || pending[0];

    const spDesc = document.getElementById('spotlightDescription');
    const spPath = document.getElementById('spotlightHierarchy');
    const spBadge = document.getElementById('spotlightBadgeState');
    const spTimeLeft = document.getElementById('spotlightTimeLeft');
    const spSched = document.getElementById('spotlightScheduledAt');
    const spActions = document.getElementById('spotlightActions');
    const spNotes = document.getElementById('spotlightNotes');

    if (spotlightTarget) {
      const classification = App.Service.classifyEvent(spotlightTarget, colorRanges);
      const timerInfo = App.Utils.formatTimeRemaining(new Date(spotlightTarget.scheduledAt).getTime());

      spDesc.textContent = spotlightTarget.description;
      spNotes.textContent = spotlightTarget.notes ? `Observações: ${spotlightTarget.notes}` : '';
      spPath.innerHTML = `
        <span>${App.Utils.escapeHTML(consoleMap.get(spotlightTarget.consoleId) || '')}</span> &bull; 
        <span>${App.Utils.escapeHTML(pipeMap.get(spotlightTarget.pipelineId) || '')}</span> &bull; 
        <span>${App.Utils.escapeHTML(uoMap.get(spotlightTarget.uoId) || '')}</span>
        ${spotlightTarget.tagId ? `<span class="event-tag-badge">${App.Utils.escapeHTML(tagMap.get(spotlightTarget.tagId) || '')}</span>` : ''}
      `;

      spBadge.className = `status-badge ${classification.key} ${classification.blink ? 'pulsing-badge' : ''}`;
      spBadge.textContent = `${classification.icon || ''} ${classification.name}`.trim();

      spTimeLeft.textContent = timerInfo.text;
      spTimeLeft.style.color = classification.color;
      spSched.textContent = `Previsto: ${App.Utils.formatDateTime(spotlightTarget.scheduledDate, spotlightTarget.scheduledTime)}`;

      spActions.innerHTML = `
        ${spotlightTarget.alarmState === 'triggered' ? `<button class="btn btn-warning btn-sm" onclick="App.UI.acknowledgeAlarm('${spotlightTarget.id}')">Reconhecer Alarme</button>` : ''}
        <button class="btn btn-success btn-sm" onclick="App.UI.showCompleteModal('${spotlightTarget.id}')">Concluir</button>
        <button class="btn btn-secondary btn-sm" onclick="App.UI.editEvent('${spotlightTarget.id}')">Editar</button>
        <button class="btn btn-outline btn-sm" onclick="App.UI.duplicateEvent('${spotlightTarget.id}')">+ Duplicar</button>
        <button class="btn btn-outline btn-sm" onclick="App.UI.showDetailsModal('${spotlightTarget.id}')">Detalhes</button>
        <button class="btn btn-outline btn-sm" onclick="App.UI.openEventActionSheet('${spotlightTarget.id}')" title="Mais ações">&#x22EF; Mais</button>
      `;
    } else {
      spDesc.textContent = 'Nenhuma previsão operacional pendente no momento.';
      spNotes.textContent = '';
      spPath.textContent = 'Console • Duto • UO';
      spBadge.className = 'status-badge normal';
      spBadge.textContent = '● Sem Pendências';
      spTimeLeft.textContent = '--:--';
      spTimeLeft.style.color = 'inherit';
      spSched.textContent = 'Horário Previsto: --:--';
      spActions.innerHTML = '';
    }

    // Tabela rápida e Cards Mobile de urgentes (< 30 min ou atrasados)
    const urgentEvents = pending.filter(e => {
      const diffMins = (new Date(e.scheduledAt).getTime() - nowTime) / 60000;
      return diffMins <= 30;
    });

    const urgentCardsContainer = document.getElementById('dashboardUrgentCards');
    if (urgentCardsContainer) {
      if (urgentEvents.length === 0) {
        urgentCardsContainer.innerHTML = `<div style="text-align: center; color: var(--text-muted); padding: 1.25rem; font-size: 0.85rem;">Nenhum evento urgente no momento.</div>`;
      } else {
        urgentCardsContainer.innerHTML = urgentEvents.slice(0, 5).map(ev => {
          const cl = App.Service.classifyEvent(ev, colorRanges);
          const timerInfo = App.Utils.formatTimeRemaining(new Date(ev.scheduledAt).getTime());
          const conName = consoleMap.get(ev.consoleId) || '';
          const pipeName = pipeMap.get(ev.pipelineId) || '';
          const uoName = uoMap.get(ev.uoId) || '';
          const tagName = tagMap.get(ev.tagId) || '';
          return `
            <div class="event-card ${cl.blink ? 'pulsing-card' : ''}" style="border-left-color: ${cl.color}; margin-bottom: 0.65rem;">
              <div class="event-card-header">
                <div class="event-hierarchy">
                  <span>${App.Utils.escapeHTML(conName)}</span> &bull;
                  <span>${App.Utils.escapeHTML(pipeName)}</span> &bull;
                  <span>${App.Utils.escapeHTML(uoName)}</span>
                  ${tagName ? `<span class="event-tag-badge">${App.Utils.escapeHTML(tagName)}</span>` : ''}
                </div>
                <span class="status-badge ${cl.key} ${cl.blink ? 'pulsing-badge' : ''}">${cl.icon || ''} ${cl.name}</span>
              </div>
              <div class="event-desc" style="margin: 0.4rem 0;">${App.Utils.escapeHTML(ev.description)}</div>
              <div class="event-card-meta">
                <span><strong>${App.Utils.formatDateTime(ev.scheduledDate, ev.scheduledTime)}</strong></span>
                <span class="event-countdown" style="color: ${cl.color};" data-timestamp="${new Date(ev.scheduledAt).getTime()}">${timerInfo.text}</span>
              </div>
              <div class="event-card-actions" style="margin-top: 0.6rem;">
                ${ev.alarmState === 'triggered' ? `<button class="btn btn-warning btn-sm" onclick="App.UI.acknowledgeAlarm('${ev.id}')">Reconhecer</button>` : ''}
                <button class="btn btn-success btn-sm" onclick="App.UI.showCompleteModal('${ev.id}')">&#x2713; Concluir</button>
                <button class="btn btn-outline btn-sm" onclick="App.UI.openEventActionSheet('${ev.id}')">&#x22EF;</button>
              </div>
            </div>
          `;
        }).join('') + `
          <div style="text-align: center; margin-top: 0.5rem;">
            <button class="btn btn-outline btn-sm" style="width: 100%; justify-content: center;" onclick="App.UI.navigateTo('viewPendingEvents')">
              Ver todos os eventos pendentes (${pending.length})
            </button>
          </div>
        `;
      }
    }

    const tbodyUrgent = document.getElementById('tbodyDashboardUrgent');
    if (urgentEvents.length === 0) {
      tbodyUrgent.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--text-muted); padding: 1.5rem;">Nenhum evento urgente no momento.</td></tr>`;
    } else {
      tbodyUrgent.innerHTML = urgentEvents.map(ev => {
        const classification = App.Service.classifyEvent(ev, colorRanges);
        const timerInfo = App.Utils.formatTimeRemaining(new Date(ev.scheduledAt).getTime());
        const conName = consoleMap.get(ev.consoleId) || '';
        const pipeName = pipeMap.get(ev.pipelineId) || '';
        const uoName = uoMap.get(ev.uoId) || '';
        const tagName = tagMap.get(ev.tagId) || '-';

        return `
          <tr class="${classification.isOverdue ? 'row-overdue' : ''}">
            <td><strong>${App.Utils.formatDateTime(ev.scheduledDate, ev.scheduledTime)}</strong></td>
            <td>
              <span class="status-badge ${classification.key} ${classification.blink ? 'pulsing-badge' : ''}">
                ${classification.icon || ''} ${classification.name} &bull; ${timerInfo.text}
              </span>
            </td>
            <td>${App.Utils.escapeHTML(conName)} / ${App.Utils.escapeHTML(pipeName)}</td>
            <td>${App.Utils.escapeHTML(uoName)} ${tagName !== '-' ? `<span class="event-tag-badge">${App.Utils.escapeHTML(tagName)}</span>` : ''}</td>
            <td>${App.Utils.escapeHTML(ev.description)}</td>
            <td style="text-align: right; white-space: nowrap;">
              <button class="btn btn-success btn-sm" onclick="App.UI.showCompleteModal('${ev.id}')">Concluir</button>
              <button class="btn btn-secondary btn-sm" onclick="App.UI.editEvent('${ev.id}')">Editar</button>
              <button class="btn btn-outline btn-sm" onclick="App.UI.duplicateEvent('${ev.id}')">+ Duplicar</button>
            </td>
          </tr>
        `;
      }).join('');
    }
  },

  // --------------------------------------------------------------------------
  // RENDERIZAÇÃO: EVENTOS PENDENTES (CARDS, TABELA E MASTER-DETAIL TABLET)
  // --------------------------------------------------------------------------
  renderPendingEvents: async function() {
    const allEvents = await App.DB.getAll('events');
    const colorRanges = await App.Service.getColorRanges();
    const consoles = await App.DB.getAll('consoles');
    const pipelines = await App.DB.getAll('pipelines');
    const uos = await App.DB.getAll('operationalUnits');
    const types = await App.DB.getAll('equipmentTypes');
    const tags = await App.DB.getAll('equipmentTags');

    const consoleMap = new Map(consoles.map(c => [c.id, c.name]));
    const pipeMap = new Map(pipelines.map(p => [p.id, p.name]));
    const uoMap = new Map(uos.map(u => [u.id, u.name]));
    const typeMap = new Map(types.map(t => [t.id, t.name]));
    const tagMap = new Map(tags.map(t => [t.id, t.tag]));

    this.populateFilterDropdowns(consoles, pipelines, uos);

    let events = allEvents.filter(e => e.status === 'pendente' && e.active !== false);

    // Filtro pelo console ativo do cabeçalho se marcado
    const chkConsoleOnly = document.getElementById('checkFilterOnlyActiveConsole')?.checked;
    if (chkConsoleOnly && this.activeConsoleId) {
      events = events.filter(e => e.consoleId === this.activeConsoleId);
    }

    // 1. Filtro textual
    const searchText = App.Utils.cleanStr(document.getElementById('inputSearchPending')?.value);
    if (searchText) {
      events = events.filter(e => {
        const desc = App.Utils.cleanStr(e.description);
        const notes = App.Utils.cleanStr(e.notes);
        const con = App.Utils.cleanStr(consoleMap.get(e.consoleId));
        const pipe = App.Utils.cleanStr(pipeMap.get(e.pipelineId));
        const uo = App.Utils.cleanStr(uoMap.get(e.uoId));
        const tag = App.Utils.cleanStr(tagMap.get(e.tagId));
        return desc.includes(searchText) || notes.includes(searchText) || con.includes(searchText) || pipe.includes(searchText) || uo.includes(searchText) || tag.includes(searchText);
      });
    }

    // 2. Filtros avançados
    const fConsole = document.getElementById('filterConsole')?.value;
    const fPipe = document.getElementById('filterPipeline')?.value;
    const fUO = document.getElementById('filterUO')?.value;
    const fStatus = document.getElementById('filterStatus')?.value;
    const fAlarm = document.getElementById('filterAlarm')?.value;
    const fPriority = document.getElementById('filterPriority')?.value;
    const fDateFrom = document.getElementById('filterDateFrom')?.value;
    const fDateTo = document.getElementById('filterDateTo')?.value;

    // Contar filtros ativos para o badge do botão Filtros
    const activeFiltersCount = [fConsole, fPipe, fUO, fStatus, fAlarm, fPriority, fDateFrom, fDateTo].filter(Boolean).length;
    const badgeFilters = document.getElementById('badgeActiveFiltersCount');
    if (badgeFilters) {
      badgeFilters.textContent = activeFiltersCount;
      badgeFilters.style.display = activeFiltersCount > 0 ? 'inline-block' : 'none';
    }

    if (fConsole) events = events.filter(e => e.consoleId === fConsole);
    if (fPipe) events = events.filter(e => e.pipelineId === fPipe);
    if (fUO) events = events.filter(e => e.uoId === fUO);
    if (fPriority) events = events.filter(e => e.priority === fPriority);
    if (fAlarm === 'sim') events = events.filter(e => e.hasAlarm);
    if (fAlarm === 'nao') events = events.filter(e => !e.hasAlarm);
    if (fDateFrom) events = events.filter(e => e.scheduledDate >= fDateFrom);
    if (fDateTo) events = events.filter(e => e.scheduledDate <= fDateTo);

    if (fStatus) {
      events = events.filter(e => {
        const cl = App.Service.classifyEvent(e, colorRanges);
        return App.Utils.cleanStr(cl.name) === App.Utils.cleanStr(fStatus);
      });
    }

    // 3. Ordenação
    const sortMode = document.getElementById('selectSortPending')?.value || 'cronologica';
    if (sortMode === 'cronologica') {
      events.sort((a, b) => new Date(a.scheduledAt).getTime() - new Date(b.scheduledAt).getTime());
    } else if (sortMode === 'console') {
      events.sort((a, b) => (consoleMap.get(a.consoleId) || '').localeCompare(consoleMap.get(b.consoleId) || ''));
    } else if (sortMode === 'duto') {
      events.sort((a, b) => (pipeMap.get(a.pipelineId) || '').localeCompare(pipeMap.get(b.pipelineId) || ''));
    } else if (sortMode === 'uo') {
      events.sort((a, b) => (uoMap.get(a.uoId) || '').localeCompare(uoMap.get(b.uoId) || ''));
    } else if (sortMode === 'tag') {
      events.sort((a, b) => (tagMap.get(a.tagId) || '').localeCompare(tagMap.get(b.tagId) || ''));
    } else if (sortMode === 'prioridade') {
      const prioOrder = { 'Crítica': 1, 'Alta': 2, 'Normal': 3, 'Baixa': 4 };
      events.sort((a, b) => (prioOrder[a.priority] || 99) - (prioOrder[b.priority] || 99));
    }

    this.activePendingEvents = events;

    const cardsContainer = document.getElementById('containerPendingCards');
    const tbodyTable = document.getElementById('tbodyPendingEvents');
    const emptyMsg = document.getElementById('pendingEmptyMessage');

    if (events.length === 0) {
      cardsContainer.innerHTML = '';
      tbodyTable.innerHTML = '';
      emptyMsg.style.display = 'block';
      this.renderPendingDetailPane(null);
      return;
    }
    emptyMsg.style.display = 'none';

    if (!this.selectedDetailEventId || !events.some(e => e.id === this.selectedDetailEventId)) {
      this.selectedDetailEventId = events[0].id;
    }

    // Renderizar Cartões
    cardsContainer.innerHTML = events.map(ev => {
      const cl = App.Service.classifyEvent(ev, colorRanges);
      const timerInfo = App.Utils.formatTimeRemaining(new Date(ev.scheduledAt).getTime());
      const conName = consoleMap.get(ev.consoleId) || '';
      const pipeName = pipeMap.get(ev.pipelineId) || '';
      const uoName = uoMap.get(ev.uoId) || '';
      const tagName = tagMap.get(ev.tagId) || '';

      const isFiring = ev.alarmState === 'triggered';
      const isSnoozed = ev.alarmState === 'snoozed';
      const isAck = ev.alarmState === 'acknowledged';
      const isSelected = ev.id === this.selectedDetailEventId;

      return `
        <div class="event-card ${cl.blink || isFiring ? 'pulsing-card' : ''} ${isSelected ? 'selected-master-card' : ''}" data-event-id="${ev.id}" style="border-left-color: ${cl.color}; cursor: pointer;" onclick="if(!event.target.closest('button')) App.UI.selectPendingDetailEvent('${ev.id}')">
          <div>
            <div class="event-card-header">
              <div class="event-hierarchy">
                <span>${App.Utils.escapeHTML(conName)}</span> &bull; 
                <span>${App.Utils.escapeHTML(pipeName)}</span> &bull; 
                <span>${App.Utils.escapeHTML(uoName)}</span>
                ${tagName ? `<span class="event-tag-badge">${App.Utils.escapeHTML(tagName)}</span>` : ''}
              </div>
              <span class="status-badge ${cl.key} ${cl.blink ? 'pulsing-badge' : ''}">${cl.icon || ''} ${cl.name}</span>
            </div>

            <div class="event-card-body" style="margin-top: 0.5rem;">
              <div class="event-desc">${App.Utils.escapeHTML(ev.description)}</div>
              ${ev.notes ? `<div class="event-notes">${App.Utils.escapeHTML(ev.notes)}</div>` : ''}
              ${ev.stylusDrawing ? `
                <div style="margin-top: 0.4rem;">
                  <button class="btn btn-outline btn-sm" style="font-size: 0.72rem; padding: 0.2rem 0.5rem;" onclick="App.UI.showDetailsModal('${ev.id}')">
                    &#x270E; Possui Anotação / Esboço
                  </button>
                </div>
              ` : ''}
            </div>
          </div>

          <div>
            <div class="event-card-meta">
              <div>
                <span style="font-weight: 700;">${App.Utils.formatDateTime(ev.scheduledDate, ev.scheduledTime)}</span>
                ${ev.priority !== 'Normal' ? `<span style="margin-left: 0.4rem; font-size: 0.72rem; color: #fbbf24;">[${ev.priority}]</span>` : ''}
              </div>
              <div class="event-countdown" style="color: ${cl.color};" data-timestamp="${new Date(ev.scheduledAt).getTime()}">
                ${timerInfo.text}
              </div>
            </div>

            <div class="event-card-actions" style="margin-top: 0.75rem; flex-wrap: wrap;">
              ${isFiring ? `
                <button class="btn btn-warning btn-sm" onclick="App.UI.acknowledgeAlarm('${ev.id}')">Reconhecer</button>
                <button class="btn btn-secondary btn-sm" onclick="App.UI.showSnoozeModal('${ev.id}')">Adiar</button>
              ` : ''}
              ${isAck ? `<span style="font-size: 0.72rem; color: #4ade80; margin-right: auto;">Alarme reconhecido</span>` : ''}
              ${isSnoozed ? `<span style="font-size: 0.72rem; color: #fbbf24; margin-right: auto;">Adiado</span>` : ''}

              <button class="btn btn-success btn-sm" onclick="App.UI.showCompleteModal('${ev.id}')" title="Concluir evento">Concluir</button>
              <button class="btn btn-secondary btn-sm" onclick="App.UI.editEvent('${ev.id}')" title="Editar evento">Editar</button>
              <button class="btn btn-outline btn-sm" onclick="App.UI.duplicateEvent('${ev.id}')" title="Duplicar evento para outro horário">+ Duplicar</button>
              <button class="btn btn-outline btn-sm" onclick="App.UI.showDetailsModal('${ev.id}')" title="Ver detalhes e histórico">Detalhes</button>
              <button class="btn btn-outline btn-sm" onclick="App.UI.deleteEvent('${ev.id}')" title="Excluir evento">&times;</button>
              <button class="btn btn-outline btn-sm btn-card-more-actions" onclick="App.UI.openEventActionSheet('${ev.id}')" title="Mais ações">&#x22EF;</button>
            </div>
          </div>
        </div>
      `;
    }).join('');

    // Renderizar Tabela Compacta
    tbodyTable.innerHTML = events.map(ev => {
      const cl = App.Service.classifyEvent(ev, colorRanges);
      const timerInfo = App.Utils.formatTimeRemaining(new Date(ev.scheduledAt).getTime());
      const conName = consoleMap.get(ev.consoleId) || '';
      const pipeName = pipeMap.get(ev.pipelineId) || '';
      const uoName = uoMap.get(ev.uoId) || '';
      const tagName = tagMap.get(ev.tagId) || '-';

      return `
        <tr class="${cl.isOverdue ? 'row-overdue' : ''}">
          <td style="white-space: nowrap;"><strong>${App.Utils.formatDateTime(ev.scheduledDate, ev.scheduledTime)}</strong></td>
          <td style="white-space: nowrap;"><span class="event-countdown" style="color: ${cl.color}; font-weight: 700;" data-timestamp="${new Date(ev.scheduledAt).getTime()}">${timerInfo.text}</span></td>
          <td><span class="status-badge ${cl.key}">${cl.icon || ''} ${cl.name}</span></td>
          <td>${App.Utils.escapeHTML(conName)} / ${App.Utils.escapeHTML(pipeName)}</td>
          <td>${App.Utils.escapeHTML(uoName)} ${tagName !== '-' ? `<span class="event-tag-badge">${App.Utils.escapeHTML(tagName)}</span>` : ''}</td>
          <td>${App.Utils.escapeHTML(ev.description)}</td>
          <td style="font-size: 0.75rem;">${ev.hasAlarm ? (ev.alarmState === 'triggered' ? '<span style="color: #ef4444; font-weight: 700;">Disparado</span>' : 'Ativo') : 'Inativo'}</td>
          <td style="text-align: right; white-space: nowrap;">
            ${ev.alarmState === 'triggered' ? `<button class="btn btn-warning btn-sm" onclick="App.UI.acknowledgeAlarm('${ev.id}')">Reconhecer</button>` : ''}
            <button class="btn btn-success btn-sm" onclick="App.UI.showCompleteModal('${ev.id}')">Concluir</button>
            <button class="btn btn-secondary btn-sm" onclick="App.UI.editEvent('${ev.id}')">Editar</button>
            <button class="btn btn-outline btn-sm" onclick="App.UI.duplicateEvent('${ev.id}')">+ Duplicar</button>
            <button class="btn btn-outline btn-sm" onclick="App.UI.showDetailsModal('${ev.id}')">Detalhes</button>
            <button class="btn btn-outline btn-sm" onclick="App.UI.deleteEvent('${ev.id}')">&times;</button>
          </td>
        </tr>
      `;
    }).join('');

    // Renderizar Painel Master-Detail (Tablet)
    await this.renderPendingDetailPane(this.selectedDetailEventId);
  },

  selectPendingDetailEvent: async function(eventId, tab = 'detalhes') {
    this.selectedDetailEventId = eventId;
    this.selectedDetailTab = tab;
    document.querySelectorAll('#containerPendingCards .event-card').forEach(card => {
      card.classList.toggle('selected-master-card', card.getAttribute('data-event-id') === eventId);
    });
    await this.renderPendingDetailPane(eventId, tab);
  },

  renderPendingDetailPane: async function(eventId, tab) {
    const pane = document.getElementById('pendingDetailPane');
    if (!pane) return;
    if (!eventId) {
      pane.innerHTML = `<div class="detail-pane-empty" style="color: var(--text-muted); text-align: center; padding: 2rem;">Selecione uma previsão na lista ao lado para visualizar detalhes, esboço manual e histórico de auditoria.</div>`;
      return;
    }

    const ev = await App.DB.get('events', eventId);
    if (!ev) return;

    const activeTab = tab || this.selectedDetailTab || 'detalhes';
    const consoles = await App.DB.getAll('consoles');
    const pipelines = await App.DB.getAll('pipelines');
    const uos = await App.DB.getAll('operationalUnits');
    const types = await App.DB.getAll('equipmentTypes');
    const tags = await App.DB.getAll('equipmentTags');
    const colorRanges = await App.Service.getColorRanges();

    const con = consoles.find(c => c.id === ev.consoleId);
    const pipe = pipelines.find(p => p.id === ev.pipelineId);
    const uo = uos.find(u => u.id === ev.uoId);
    const type = types.find(t => t.id === ev.equipmentTypeId);
    const tag = tags.find(t => t.id === ev.tagId);
    const cl = App.Service.classifyEvent(ev, colorRanges);
    const timerInfo = App.Utils.formatTimeRemaining(new Date(ev.scheduledAt).getTime());

    let tabContentHtml = '';
    if (activeTab === 'detalhes') {
      tabContentHtml = `
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-bottom: 1rem; font-size: 0.84rem;">
          <div>
            <div style="font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase;">Hierarquia</div>
            <div style="font-weight: 700;">${App.Utils.escapeHTML(con ? con.name : '')} / ${App.Utils.escapeHTML(pipe ? pipe.name : '')} / ${App.Utils.escapeHTML(uo ? uo.name : '')}</div>
          </div>
          <div>
            <div style="font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase;">Equipamento / TAG</div>
            <div style="font-weight: 700;">${App.Utils.escapeHTML(type ? type.name : 'Geral')} ${tag ? '(' + App.Utils.escapeHTML(tag.tag) + ')' : ''}</div>
          </div>
          <div>
            <div style="font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase;">Horário Previsto</div>
            <div style="font-weight: 700;">${App.Utils.formatDateTime(ev.scheduledDate, ev.scheduledTime)}</div>
          </div>
          <div>
            <div style="font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase;">Prioridade / Alarme</div>
            <div style="font-weight: 700;">${ev.priority} &bull; ${ev.hasAlarm ? (ev.leadTimeMinutes + ' min antes') : 'Sem alarme'}</div>
          </div>
        </div>
        <div style="margin-bottom: 0.85rem;">
          <div style="font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.25rem;">Descrição da Previsão</div>
          <div style="font-size: 0.95rem; font-weight: 600; background: rgba(0,0,0,0.2); padding: 0.65rem; border-radius: var(--radius-sm);">${App.Utils.escapeHTML(ev.description)}</div>
        </div>
        <div>
          <div style="font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.25rem;">Observações</div>
          <div style="font-size: 0.85rem; color: var(--text-secondary); background: rgba(0,0,0,0.15); padding: 0.65rem; border-radius: var(--radius-sm);">${App.Utils.escapeHTML(ev.notes || 'Sem observações complementares.')}</div>
        </div>
      `;
    } else if (activeTab === 'anotacoes') {
      tabContentHtml = ev.stylusDrawing ? `
        <div style="text-align: center; background: rgba(0,0,0,0.3); padding: 0.75rem; border-radius: var(--radius-sm); border: 1px solid var(--border-color);">
          <img src="${ev.stylusDrawing}" alt="Esboço Manual" style="max-width: 100%; max-height: 260px; border-radius: 4px;">
        </div>
      ` : `<div style="color: var(--text-muted); font-size: 0.85rem; text-align: center; padding: 1.5rem;">Nenhum esboço ou anotação manual registrada para este evento.</div>`;
    } else if (activeTab === 'historico') {
      const allHistory = await App.DB.getAll('eventHistory');
      const eventHist = allHistory.filter(h => h.eventId === eventId).sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());
      tabContentHtml = eventHist.length === 0 ? `<div style="color: var(--text-muted); font-size: 0.85rem;">Nenhum histórico encontrado.</div>` : `
        <div class="audit-timeline" style="max-height: 260px; overflow-y: auto;">
          ${eventHist.map(h => `
            <div class="timeline-item">
              <div class="timeline-point"></div>
              <div class="timeline-content">
                <div class="timeline-meta">
                  <span>${App.Utils.formatDateTime(h.timestamp)}</span>
                  <span><strong>${App.Utils.escapeHTML(h.localUser)}</strong></span>
                </div>
                <div class="timeline-title">${App.Utils.escapeHTML(h.action.toUpperCase())}</div>
                <div class="timeline-desc">${App.Utils.escapeHTML(h.description)}</div>
              </div>
            </div>
          `).join('')}
        </div>
      `;
    }

    pane.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 0.65rem; margin-bottom: 0.75rem;">
        <span class="status-badge ${cl.key}">${cl.icon || ''} ${cl.name}</span>
        <span class="event-countdown" style="color: ${cl.color}; font-weight: 800; font-size: 1rem;" data-timestamp="${new Date(ev.scheduledAt).getTime()}">${timerInfo.text}</span>
      </div>
      <div style="display: flex; gap: 0.4rem; margin-bottom: 0.85rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">
        <button class="btn ${activeTab === 'detalhes' ? 'btn-secondary' : 'btn-outline'} btn-sm" onclick="App.UI.selectPendingDetailEvent('${ev.id}', 'detalhes')">Detalhes</button>
        <button class="btn ${activeTab === 'anotacoes' ? 'btn-secondary' : 'btn-outline'} btn-sm" onclick="App.UI.selectPendingDetailEvent('${ev.id}', 'anotacoes')">Anotações</button>
        <button class="btn ${activeTab === 'historico' ? 'btn-secondary' : 'btn-outline'} btn-sm" onclick="App.UI.selectPendingDetailEvent('${ev.id}', 'historico')">Histórico</button>
      </div>
      <div style="margin-bottom: 1rem;">
        ${tabContentHtml}
      </div>
      <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; border-top: 1px solid var(--border-color); padding-top: 0.75rem;">
        <button class="btn btn-success btn-sm" onclick="App.UI.showCompleteModal('${ev.id}')">&#x2713; Concluir</button>
        <button class="btn btn-secondary btn-sm" onclick="App.UI.editEvent('${ev.id}')">Editar</button>
        <button class="btn btn-outline btn-sm" onclick="App.UI.duplicateEvent('${ev.id}')">+ Duplicar</button>
        <button class="btn btn-outline btn-sm" onclick="App.UI.deleteEvent('${ev.id}')">Excluir</button>
      </div>
    `;
  },

  openEventActionSheet: async function(eventId) {
    const ev = await App.DB.get('events', eventId);
    if (!ev) return;
    this.selectedEventForAction = ev;

    const titleEl = document.getElementById('actionSheetEventTitle');
    const container = document.getElementById('actionSheetButtonsContainer');
    const modal = document.getElementById('modalEventActionSheet');
    if (!container || !modal) return;

    if (titleEl) titleEl.textContent = ev.description;

    const closeSheet = "document.getElementById('modalEventActionSheet').classList.remove('active');";
    container.innerHTML = `
      ${ev.status === 'pendente' ? `
        <button class="btn btn-success" style="width: 100%; justify-content: flex-start;" onclick="${closeSheet} App.UI.showCompleteModal('${ev.id}')">&#x2713; Concluir Evento</button>
        ${ev.alarmState === 'triggered' ? `<button class="btn btn-warning" style="width: 100%; justify-content: flex-start;" onclick="${closeSheet} App.UI.acknowledgeAlarm('${ev.id}')">&#x1F514; Reconhecer Alarme</button>` : ''}
        <button class="btn btn-secondary" style="width: 100%; justify-content: flex-start;" onclick="${closeSheet} App.UI.showSnoozeModal('${ev.id}')">&#x23F1; Adiar Alarme (5 / 10 / 15 min)</button>
        <button class="btn btn-secondary" style="width: 100%; justify-content: flex-start;" onclick="${closeSheet} App.UI.editEvent('${ev.id}')">&#x270E; Editar Previsão</button>
      ` : `
        <button class="btn btn-secondary" style="width: 100%; justify-content: flex-start;" onclick="${closeSheet} App.UI.showReopenModal('${ev.id}')">&#x21BA; Reabrir Previsão</button>
      `}
      <button class="btn btn-outline" style="width: 100%; justify-content: flex-start;" onclick="${closeSheet} App.UI.duplicateEvent('${ev.id}')">+ Duplicar para Novo Horário</button>
      <button class="btn btn-outline" style="width: 100%; justify-content: flex-start;" onclick="${closeSheet} App.UI.showDetailsModal('${ev.id}')">&#x1F4CB; Ver Detalhes e Auditoria</button>
      <button class="btn btn-danger" style="width: 100%; justify-content: flex-start;" onclick="${closeSheet} App.UI.deleteEvent('${ev.id}')">&times; Excluir Previsão</button>
    `;

    modal.classList.add('active');
  },

  updateLiveTimers: function() {
    const countdownEls = document.querySelectorAll('.event-countdown[data-timestamp]');
    countdownEls.forEach(el => {
      const ts = parseInt(el.getAttribute('data-timestamp'), 10);
      if (ts) {
        const info = App.Utils.formatTimeRemaining(ts);
        el.textContent = info.text;
      }
    });

    const spotlightTs = document.getElementById('spotlightTimeLeft');
    if (spotlightTs && this.activePendingEvents.length > 0) {
      const nextEv = this.activePendingEvents[0];
      const info = App.Utils.formatTimeRemaining(new Date(nextEv.scheduledAt).getTime());
      spotlightTs.textContent = info.text;
    }
  },

  populateFilterDropdowns: function(consoles, pipelines, uos) {
    const fill = (id, list, key = 'name') => {
      const sel = document.getElementById(id);
      if (sel && sel.options.length <= 1) {
        list.forEach(item => {
          const opt = document.createElement('option');
          opt.value = item.id;
          opt.textContent = item[key];
          sel.appendChild(opt);
        });
      }
    };
    fill('filterConsole', consoles);
    fill('filterPipeline', pipelines);
    fill('filterUO', uos);
    fill('filterCompletedConsole', consoles);
    fill('filterCompletedPipeline', pipelines);
    fill('filterCompletedUO', uos);
  },

  // --------------------------------------------------------------------------
  // RENDERIZAÇÃO: EVENTOS CONCLUÍDOS (9 COLUNAS + CARDS EXPANSÍVEIS MOBILE)
  // --------------------------------------------------------------------------
  renderCompletedEvents: async function() {
    const allEvents = await App.DB.getAll('events');
    const consoles = await App.DB.getAll('consoles');
    const pipelines = await App.DB.getAll('pipelines');
    const uos = await App.DB.getAll('operationalUnits');
    const types = await App.DB.getAll('equipmentTypes');
    const tags = await App.DB.getAll('equipmentTags');

    const consoleMap = new Map(consoles.map(c => [c.id, c.name]));
    const pipeMap = new Map(pipelines.map(p => [p.id, p.name]));
    const uoMap = new Map(uos.map(u => [u.id, u.name]));
    const tagMap = new Map(tags.map(t => [t.id, t.tag]));

    let completed = allEvents.filter(e => e.status === 'concluido' && e.active !== false);

    const searchText = App.Utils.cleanStr(document.getElementById('inputSearchCompleted')?.value);
    if (searchText) {
      completed = completed.filter(e => {
        return App.Utils.cleanStr(e.description).includes(searchText) ||
               App.Utils.cleanStr(e.notes).includes(searchText) ||
               App.Utils.cleanStr(e.completionNote).includes(searchText) ||
               App.Utils.cleanStr(consoleMap.get(e.consoleId)).includes(searchText) ||
               App.Utils.cleanStr(pipeMap.get(e.pipelineId)).includes(searchText) ||
               App.Utils.cleanStr(uoMap.get(e.uoId)).includes(searchText) ||
               App.Utils.cleanStr(tagMap.get(e.tagId)).includes(searchText);
      });
    }

    const fConsole = document.getElementById('filterCompletedConsole')?.value;
    const fPipe = document.getElementById('filterCompletedPipeline')?.value;
    const fUO = document.getElementById('filterCompletedUO')?.value;
    const fTiming = document.getElementById('filterCompletedTiming')?.value;
    const fDateFrom = document.getElementById('filterCompletedDateFrom')?.value;
    const fDateTo = document.getElementById('filterCompletedDateTo')?.value;

    if (fConsole) completed = completed.filter(e => e.consoleId === fConsole);
    if (fPipe) completed = completed.filter(e => e.pipelineId === fPipe);
    if (fUO) completed = completed.filter(e => e.uoId === fUO);
    if (fDateFrom) completed = completed.filter(e => e.scheduledDate >= fDateFrom);
    if (fDateTo) completed = completed.filter(e => e.scheduledDate <= fDateTo);

    // Fix #7 da Seção 24: Harmonizar filtro de pontualidade (antecedencia/antecipado, noprazo/pontual, atraso/atrasado)
    if (fTiming) {
      completed = completed.filter(e => {
        const diff = e.completedTimeDiffMinutes || 0;
        if (fTiming === 'antecedencia' || fTiming === 'antecipado') return diff < -1;
        if (fTiming === 'noprazo' || fTiming === 'pontual') return Math.abs(diff) <= 1;
        if (fTiming === 'atraso' || fTiming === 'atrasado') return diff > 1;
        return true;
      });
    }

    completed.sort((a, b) => new Date(b.completedAt || b.scheduledAt).getTime() - new Date(a.completedAt || a.scheduledAt).getTime());

    const tbody = document.getElementById('tbodyCompletedEvents');
    const cardsContainer = document.getElementById('containerCompletedCards');
    const emptyMsg = document.getElementById('completedEmptyMessage');

    if (completed.length === 0) {
      if (tbody) tbody.innerHTML = '';
      if (cardsContainer) cardsContainer.innerHTML = '';
      if (emptyMsg) emptyMsg.style.display = 'block';
      return;
    }
    if (emptyMsg) emptyMsg.style.display = 'none';

    // Renderizar Cards Expansíveis para Mobile (Seção 12.6 / Fix #11)
    if (cardsContainer) {
      cardsContainer.innerHTML = completed.map(ev => {
        const conName = consoleMap.get(ev.consoleId) || '';
        const pipeName = pipeMap.get(ev.pipelineId) || '';
        const uoName = uoMap.get(ev.uoId) || '';
        const tagName = tagMap.get(ev.tagId) || '-';
        const schedStr = App.Utils.formatDateTime(ev.scheduledDate, ev.scheduledTime);
        const compStr = App.Utils.formatDateTime(ev.completedAt);
        const diffStr = App.Utils.formatDiffMinutes(ev.completedTimeDiffMinutes);
        const controllerName = ev.completedBy || ev.createdBy || 'Usuário local';
        const alarmSummary = ev.alarmTriggerCount ? `${ev.alarmTriggerCount} disparo(s)` : (ev.hasAlarm ? 'Ativo (0 disparos)' : 'Sem alarme');

        return `
          <div class="completed-event-card" onclick="if(!event.target.closest('button')) this.classList.toggle('expanded')">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
              <span class="status-badge concluido">&#x2713; Concluído</span>
              <span style="font-size: 0.78rem; font-weight: 700;">${diffStr}</span>
            </div>
            <div style="font-size: 0.78rem; color: var(--text-secondary); margin-bottom: 0.25rem;">
              <strong>${App.Utils.escapeHTML(conName)}</strong> &bull; ${App.Utils.escapeHTML(pipeName)} &bull; ${App.Utils.escapeHTML(uoName)}
              ${tagName !== '-' ? `<span class="event-tag-badge">${App.Utils.escapeHTML(tagName)}</span>` : ''}
            </div>
            <div style="font-weight: 700; font-size: 0.92rem; margin-bottom: 0.35rem;">${App.Utils.escapeHTML(ev.description)}</div>
            <div style="display: flex; justify-content: space-between; font-size: 0.76rem; color: var(--text-muted);">
              <span>Prev: ${schedStr}</span>
              <span>Conc: <strong>${compStr}</strong></span>
            </div>
            <div class="completed-card-details">
              ${ev.completionNote ? `<div style="margin-bottom: 0.35rem;"><strong>Obs. Conclusão:</strong> ${App.Utils.escapeHTML(ev.completionNote)}</div>` : ''}
              <div style="margin-bottom: 0.35rem;"><strong>Controlador:</strong> ${App.Utils.escapeHTML(controllerName)} &bull; <strong>Alarmes:</strong> ${alarmSummary}</div>
              <div style="display: flex; gap: 0.4rem; flex-wrap: wrap; margin-top: 0.5rem;">
                <button class="btn btn-outline btn-sm" onclick="App.UI.showReopenModal('${ev.id}')">Reabrir</button>
                <button class="btn btn-outline btn-sm" onclick="App.UI.duplicateEvent('${ev.id}')">+ Duplicar</button>
                <button class="btn btn-outline btn-sm" onclick="App.UI.showDetailsModal('${ev.id}')">Detalhes</button>
                <button class="btn btn-outline btn-sm" onclick="App.UI.deleteEvent('${ev.id}')">&times;</button>
              </div>
            </div>
          </div>
        `;
      }).join('');
    }

    // Fix #11 da Seção 24: Renderizar as 9 colunas completas na tabela de concluídos
    tbody.innerHTML = completed.map(ev => {
      const conName = consoleMap.get(ev.consoleId) || '';
      const pipeName = pipeMap.get(ev.pipelineId) || '';
      const uoName = uoMap.get(ev.uoId) || '';
      const tagName = tagMap.get(ev.tagId) || '-';

      const schedStr = App.Utils.formatDateTime(ev.scheduledDate, ev.scheduledTime);
      const compStr = App.Utils.formatDateTime(ev.completedAt);
      const diffStr = App.Utils.formatDiffMinutes(ev.completedTimeDiffMinutes);
      const controllerName = ev.completedBy || ev.createdBy || 'Usuário local';
      const alarmSummary = ev.alarmTriggerCount ? `${ev.alarmTriggerCount}x` : (ev.hasAlarm ? 'Ativo' : 'Sem alarme');

      return `
        <tr>
          <td style="white-space: nowrap;">${schedStr}</td>
          <td style="white-space: nowrap;"><strong>${compStr}</strong></td>
          <td style="white-space: nowrap;">${diffStr}</td>
          <td>${App.Utils.escapeHTML(conName)} / ${App.Utils.escapeHTML(pipeName)}</td>
          <td>${App.Utils.escapeHTML(uoName)} ${tagName !== '-' ? `<span class="event-tag-badge">${App.Utils.escapeHTML(tagName)}</span>` : ''}</td>
          <td>
            <div>${App.Utils.escapeHTML(ev.description)}</div>
            ${ev.completionNote ? `<div style="font-size: 0.75rem; color: #94a3b8; font-style: italic;">Justificativa: ${App.Utils.escapeHTML(ev.completionNote)}</div>` : ''}
          </td>
          <td style="white-space: nowrap; font-size: 0.8rem;">${App.Utils.escapeHTML(controllerName)}</td>
          <td style="white-space: nowrap; font-size: 0.78rem;">${alarmSummary}</td>
          <td style="text-align: right; white-space: nowrap;">
            <button class="btn btn-outline btn-sm" onclick="App.UI.showReopenModal('${ev.id}')">Reabrir</button>
            <button class="btn btn-outline btn-sm" onclick="App.UI.duplicateEvent('${ev.id}')">+ Duplicar</button>
            <button class="btn btn-outline btn-sm" onclick="App.UI.showDetailsModal('${ev.id}')">Detalhes</button>
            <button class="btn btn-outline btn-sm" onclick="App.UI.deleteEvent('${ev.id}')">&times;</button>
          </td>
        </tr>
      `;
    }).join('');
  },

  // --------------------------------------------------------------------------
  // RENDERIZAÇÃO: HUB UNIFICADO DE CADASTROS (SEM ESPAÇO MORTO + DRILL-DOWN)
  // --------------------------------------------------------------------------
  renderCadastros: async function() {
    await this.refreshAllMasterDataDropdowns();
    await this.renderConsolesTable();
    await this.renderPipelinesTable();
    await this.renderUOsTable();
    await this.renderEquipmentTypesTable();
    await this.renderEquipmentTagsTable();
  },

  switchCadastrosCategory: function(category) {
    this.activeCadastrosCategory = category;
    document.querySelectorAll('#cadastrosCategoryBar .cadastros-category-btn').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-cat') === category);
    });

    const card1 = document.getElementById('hubCardConsolesPipelines');
    const card2 = document.getElementById('hubCardUOsTypes');
    const card3 = document.getElementById('hubCardTags');
    const subConsoles = document.getElementById('subSectionConsoles');
    const subPipelines = document.getElementById('subSectionPipelines');
    const subUOs = document.getElementById('subSectionUOs');
    const subTypes = document.getElementById('subSectionTypes');

    if (category === 'all') {
      [card1, card2, card3, subConsoles, subPipelines, subUOs, subTypes].forEach(el => {
        if (el) el.style.display = '';
      });
      return;
    }

    if (card1) card1.style.display = (category === 'consoles' || category === 'pipelines') ? '' : 'none';
    if (subConsoles) subConsoles.style.display = category === 'consoles' ? '' : 'none';
    if (subPipelines) subPipelines.style.display = category === 'pipelines' ? '' : 'none';

    if (card2) card2.style.display = (category === 'uos' || category === 'types') ? '' : 'none';
    if (subUOs) subUOs.style.display = category === 'uos' ? '' : 'none';
    if (subTypes) subTypes.style.display = category === 'types' ? '' : 'none';

    if (card3) card3.style.display = category === 'tags' ? '' : 'none';
  },

  bindCadastrosForms: function() {
    // 1. Console Form
    const formConsole = document.getElementById('formConsole');
    formConsole?.addEventListener('submit', async (e) => {
      e.preventDefault();
      try {
        const id = document.getElementById('consoleEditId').value;
        const name = document.getElementById('inputConsoleName').value;
        await App.Service.saveConsole({ id: id || undefined, name });
        this.showToast('Console salvo com sucesso!', 'success');
        document.getElementById('consoleEditId').value = '';
        formConsole.reset();
        document.getElementById('btnCancelConsoleEdit').style.display = 'none';
        document.getElementById('btnSubmitConsole').textContent = 'Salvar Console';
        await this.initHeaderConsole();
        await this.renderConsolesTable();
      } catch (err) {
        this.showToast(err.message, 'danger');
      }
    });

    document.getElementById('btnCancelConsoleEdit')?.addEventListener('click', () => {
      document.getElementById('consoleEditId').value = '';
      formConsole.reset();
      document.getElementById('btnCancelConsoleEdit').style.display = 'none';
      document.getElementById('btnSubmitConsole').textContent = 'Salvar Console';
    });

    // 2. Pipeline Form & Adição Rápida Inline de UO
    const formPipeline = document.getElementById('formPipeline');
    formPipeline?.addEventListener('submit', async (e) => {
      e.preventDefault();
      try {
        const id = document.getElementById('pipelineEditId').value;
        const name = document.getElementById('inputPipelineName').value;
        const consoleId = document.getElementById('selectPipelineConsole').value;
        const uoCheckboxes = document.querySelectorAll('#boxPipelineUOs input[type="checkbox"]:checked');
        const uoIds = Array.from(uoCheckboxes).map(cb => cb.value);

        await App.Service.savePipeline({ id: id || undefined, name, consoleId, uoIds });
        this.showToast('Duto salvo com sucesso!', 'success');
        document.getElementById('pipelineEditId').value = '';
        formPipeline.reset();
        document.getElementById('btnCancelPipelineEdit').style.display = 'none';
        document.getElementById('btnSubmitPipeline').textContent = 'Salvar Duto';
        await this.renderPipelinesTable();
      } catch (err) {
        this.showToast(err.message, 'danger');
      }
    });

    document.getElementById('btnCancelPipelineEdit')?.addEventListener('click', () => {
      document.getElementById('pipelineEditId').value = '';
      formPipeline.reset();
      document.getElementById('btnCancelPipelineEdit').style.display = 'none';
      document.getElementById('btnSubmitPipeline').textContent = 'Salvar Duto';
    });

    // Botão Inline de Adição Rápida de UO dentro da criação do Duto
    document.getElementById('btnInlineAddUO')?.addEventListener('click', async () => {
      const input = document.getElementById('inputInlineNewUO');
      const val = input ? input.value.trim() : '';
      if (!val) {
        this.showToast('Informe o nome da UO para criar.', 'warning');
        return;
      }
      try {
        const result = await App.Service.saveUOBatch(val);
        input.value = '';
        await this.refreshAllMasterDataDropdowns();
        await this.renderUOsTable();

        // Marcar as UOs criadas/encontradas no formulário de duto
        result.all.forEach(u => {
          const cb = document.querySelector(`#boxPipelineUOs input[type="checkbox"][value="${u.id}"]`);
          if (cb) cb.checked = true;
        });

        const createdCount = result.created.length;
        this.showToast(`${createdCount > 0 ? createdCount + ' UO(s) adicionada(s)' : 'UO(s) confirmada(s)'} e vinculada(s) ao duto!`, 'success');
      } catch (err) {
        this.showToast(err.message, 'danger');
      }
    });

    // Filtro de checkboxes de UO no form de duto
    document.getElementById('inputFilterUOCheckboxes')?.addEventListener('input', (e) => {
      const q = App.Utils.cleanStr(e.target.value);
      document.querySelectorAll('#boxPipelineUOs label').forEach(lbl => {
        lbl.style.display = App.Utils.cleanStr(lbl.textContent).includes(q) ? 'flex' : 'none';
      });
    });

    // 3. UO Form (com suporte a LOTE separado por vírgula)
    const formUO = document.getElementById('formUO');
    formUO?.addEventListener('submit', async (e) => {
      e.preventDefault();
      try {
        const id = document.getElementById('uoEditId').value;
        const nameVal = document.getElementById('inputUOName').value;

        if (id) {
          // Edição de UO única
          await App.Service.saveUO({ id: id, name: nameVal });
          this.showToast('UO atualizada com sucesso!', 'success');
        } else {
          // Criação (suporta lote por vírgula, ex: REFAP, TEDEP)
          const result = await App.Service.saveUOBatch(nameVal);
          const total = result.created.length;
          this.showToast(total > 1 ? `${total} UOs cadastradas com sucesso!` : 'UO salva com sucesso!', 'success');
        }

        document.getElementById('uoEditId').value = '';
        formUO.reset();
        document.getElementById('btnCancelUOEdit').style.display = 'none';
        document.getElementById('btnSubmitUO').textContent = 'Salvar UO';

        // Atualização imediata em toda a aplicação (inclusive Tipos de Equipamentos!)
        await this.refreshAllMasterDataDropdowns();
        await this.renderUOsTable();
        await this.renderPipelinesTable();
      } catch (err) {
        this.showToast(err.message, 'danger');
      }
    });

    document.getElementById('btnCancelUOEdit')?.addEventListener('click', () => {
      document.getElementById('uoEditId').value = '';
      formUO.reset();
      document.getElementById('btnCancelUOEdit').style.display = 'none';
      document.getElementById('btnSubmitUO').textContent = 'Salvar UO';
    });

    // 4. Equipment Type Form
    const formType = document.getElementById('formEquipmentType');
    formType?.addEventListener('submit', async (e) => {
      e.preventDefault();
      try {
        const id = document.getElementById('equipmentTypeEditId').value;
        const uoId = document.getElementById('selectEquipmentTypeUO').value;
        const name = document.getElementById('inputEquipmentTypeName').value;
        await App.Service.saveEquipmentType({ id: id || undefined, uoId, name });
        this.showToast('Tipo de equipamento salvo com sucesso!', 'success');
        document.getElementById('equipmentTypeEditId').value = '';
        formType.reset();
        document.getElementById('btnCancelEquipmentTypeEdit').style.display = 'none';
        document.getElementById('btnSubmitEquipmentType').textContent = 'Salvar Tipo';
        await this.renderEquipmentTypesTable();
      } catch (err) {
        this.showToast(err.message, 'danger');
      }
    });

    document.getElementById('btnCancelEquipmentTypeEdit')?.addEventListener('click', () => {
      document.getElementById('equipmentTypeEditId').value = '';
      formType.reset();
      document.getElementById('btnCancelEquipmentTypeEdit').style.display = 'none';
      document.getElementById('btnSubmitEquipmentType').textContent = 'Salvar Tipo';
    });

    // 5. Equipment Tag Form
    const formTag = document.getElementById('formEquipmentTag');
    const selTagUO = document.getElementById('selectTagUO');
    const selTagType = document.getElementById('selectTagType');

    selTagUO?.addEventListener('change', async () => {
      const uoId = selTagUO.value;
      await this.loadEquipmentTypeOptions(uoId, 'selectTagType');
    });

    formTag?.addEventListener('submit', async (e) => {
      e.preventDefault();
      try {
        const id = document.getElementById('tagEditId').value;
        const uoId = selTagUO.value;
        const equipmentTypeId = selTagType.value;
        const tag = document.getElementById('inputTagCode').value;

        await App.Service.saveEquipmentTag({ id: id || undefined, uoId, equipmentTypeId, tag });
        this.showToast('TAG de equipamento salvo com sucesso!', 'success');
        document.getElementById('tagEditId').value = '';
        formTag.reset();
        selTagType.innerHTML = '<option value="">Selecione primeiro a UO...</option>';
        selTagType.disabled = true;
        document.getElementById('btnCancelTagEdit').style.display = 'none';
        document.getElementById('btnSubmitTag').textContent = 'Salvar TAG';
        await this.renderEquipmentTagsTable();
      } catch (err) {
        this.showToast(err.message, 'danger');
      }
    });

    document.getElementById('btnCancelTagEdit')?.addEventListener('click', () => {
      document.getElementById('tagEditId').value = '';
      formTag.reset();
      selTagType.innerHTML = '<option value="">Selecione primeiro a UO...</option>';
      selTagType.disabled = true;
      document.getElementById('btnCancelTagEdit').style.display = 'none';
      document.getElementById('btnSubmitTag').textContent = 'Salvar TAG';
    });

    // Buscas nas tabelas de cadastros
    document.getElementById('searchConsoles')?.addEventListener('input', () => this.renderConsolesTable());
    document.getElementById('filterActiveConsoles')?.addEventListener('change', () => this.renderConsolesTable());
    document.getElementById('searchPipelines')?.addEventListener('input', () => this.renderPipelinesTable());
    document.getElementById('filterActivePipelines')?.addEventListener('change', () => this.renderPipelinesTable());
    document.getElementById('searchUOs')?.addEventListener('input', () => this.renderUOsTable());
    document.getElementById('filterActiveUOs')?.addEventListener('change', () => this.renderUOsTable());
    document.getElementById('searchEquipmentTypes')?.addEventListener('input', () => this.renderEquipmentTypesTable());
    document.getElementById('filterActiveEquipmentTypes')?.addEventListener('change', () => this.renderEquipmentTypesTable());
    document.getElementById('searchTags')?.addEventListener('input', () => this.renderEquipmentTagsTable());
    document.getElementById('filterActiveTags')?.addEventListener('change', () => this.renderEquipmentTagsTable());
  },

  renderConsolesTable: async function() {
    const consoles = await App.DB.getAll('consoles');
    const pipelines = await App.DB.getAll('pipelines');

    const catCount = document.getElementById('catCountConsoles');
    if (catCount) catCount.textContent = consoles.filter(c => c.active !== false).length;

    const q = App.Utils.cleanStr(document.getElementById('searchConsoles')?.value);
    const activeFilter = document.getElementById('filterActiveConsoles')?.value || 'active';

    let filtered = consoles;
    if (q) filtered = filtered.filter(c => App.Utils.cleanStr(c.name).includes(q));
    if (activeFilter === 'active') filtered = filtered.filter(c => c.active);
    if (activeFilter === 'inactive') filtered = filtered.filter(c => !c.active);

    filtered.sort((a, b) => a.name.localeCompare(b.name));

    const tbody = document.getElementById('tbodyConsoles');
    tbody.innerHTML = filtered.map(c => {
      const pipeCount = pipelines.filter(p => p.consoleId === c.id).length;
      return `
        <tr>
          <td><strong>${App.Utils.escapeHTML(c.name)}</strong></td>
          <td>${pipeCount} duto(s)</td>
          <td><span class="status-badge ${c.active ? 'normal' : 'inativo'}">${c.active ? 'Ativo' : 'Inativo'}</span></td>
          <td style="text-align: right; white-space: nowrap;">
            <button class="btn btn-outline btn-sm" onclick="App.UI.editConsole('${c.id}')">Editar</button>
            <button class="btn btn-outline btn-sm" onclick="App.UI.toggleConsoleActive('${c.id}')">${c.active ? 'Inativar' : 'Ativar'}</button>
            <button class="btn btn-outline btn-sm" onclick="App.UI.deleteConsole('${c.id}')">&times;</button>
          </td>
        </tr>
      `;
    }).join('');
  },

  renderPipelinesTable: async function() {
    const pipelines = await App.DB.getAll('pipelines');
    const consoles = await App.DB.getAll('consoles');
    const links = await App.DB.getAll('pipelineOperationalUnits');
    const uos = await App.DB.getAll('operationalUnits');

    const catCount = document.getElementById('catCountPipelines');
    if (catCount) catCount.textContent = pipelines.filter(p => p.active !== false).length;

    const consoleMap = new Map(consoles.map(c => [c.id, c.name]));
    const uoMap = new Map(uos.map(u => [u.id, u.name]));

    await this.loadConsoleOptions('selectPipelineConsole');

    const q = App.Utils.cleanStr(document.getElementById('searchPipelines')?.value);
    const activeFilter = document.getElementById('filterActivePipelines')?.value || 'active';

    let filtered = pipelines;
    if (q) filtered = filtered.filter(p => App.Utils.cleanStr(p.name).includes(q));
    if (activeFilter === 'active') filtered = filtered.filter(p => p.active);
    if (activeFilter === 'inactive') filtered = filtered.filter(p => !p.active);

    filtered.sort((a, b) => a.name.localeCompare(b.name));

    const tbody = document.getElementById('tbodyPipelines');
    tbody.innerHTML = filtered.map(p => {
      const uoNames = links.filter(l => l.pipelineId === p.id).map(l => uoMap.get(l.uoId)).filter(Boolean).join(', ') || 'Nenhuma';
      return `
        <tr>
          <td><strong>${App.Utils.escapeHTML(p.name)}</strong></td>
          <td>${App.Utils.escapeHTML(consoleMap.get(p.consoleId) || '-')}</td>
          <td style="font-size: 0.8rem; color: var(--text-secondary);">${App.Utils.escapeHTML(uoNames)}</td>
          <td><span class="status-badge ${p.active ? 'normal' : 'inativo'}">${p.active ? 'Ativo' : 'Inativo'}</span></td>
          <td style="text-align: right; white-space: nowrap;">
            <button class="btn btn-outline btn-sm" onclick="App.UI.editPipeline('${p.id}')">Editar</button>
            <button class="btn btn-outline btn-sm" onclick="App.UI.togglePipelineActive('${p.id}')">${p.active ? 'Inativar' : 'Ativar'}</button>
            <button class="btn btn-outline btn-sm" onclick="App.UI.deletePipeline('${p.id}')">&times;</button>
          </td>
        </tr>
      `;
    }).join('');
  },

  renderUOsTable: async function() {
    const uos = await App.DB.getAll('operationalUnits');
    const pipelines = await App.DB.getAll('pipelines');
    const links = await App.DB.getAll('pipelineOperationalUnits');
    const types = await App.DB.getAll('equipmentTypes');

    const catCount = document.getElementById('catCountUOs');
    if (catCount) catCount.textContent = uos.filter(u => u.active !== false).length;

    const pipeMap = new Map(pipelines.map(p => [p.id, p.name]));

    const q = App.Utils.cleanStr(document.getElementById('searchUOs')?.value);
    const activeFilter = document.getElementById('filterActiveUOs')?.value || 'active';

    let filtered = uos;
    if (q) filtered = filtered.filter(u => App.Utils.cleanStr(u.name).includes(q));
    if (activeFilter === 'active') filtered = filtered.filter(u => u.active);
    if (activeFilter === 'inactive') filtered = filtered.filter(u => !u.active);

    filtered.sort((a, b) => a.name.localeCompare(b.name));

    const tbody = document.getElementById('tbodyUOs');
    tbody.innerHTML = filtered.map(u => {
      const connectedPipes = links.filter(l => l.uoId === u.id).map(l => pipeMap.get(l.pipelineId)).filter(Boolean).join(', ') || 'Nenhum';
      const typeCount = types.filter(t => t.uoId === u.id).length;
      return `
        <tr>
          <td><strong>${App.Utils.escapeHTML(u.name)}</strong></td>
          <td style="font-size: 0.8rem; color: var(--text-secondary);">${App.Utils.escapeHTML(connectedPipes)}</td>
          <td>${typeCount} tipo(s)</td>
          <td><span class="status-badge ${u.active ? 'normal' : 'inativo'}">${u.active ? 'Ativo' : 'Inativo'}</span></td>
          <td style="text-align: right; white-space: nowrap;">
            <button class="btn btn-outline btn-sm" onclick="App.UI.editUO('${u.id}')">Editar</button>
            <button class="btn btn-outline btn-sm" onclick="App.UI.toggleUOActive('${u.id}')">${u.active ? 'Inativar' : 'Ativar'}</button>
            <button class="btn btn-outline btn-sm" onclick="App.UI.deleteUO('${u.id}')">&times;</button>
          </td>
        </tr>
      `;
    }).join('');
  },

  renderEquipmentTypesTable: async function() {
    const types = await App.DB.getAll('equipmentTypes');
    const uos = await App.DB.getAll('operationalUnits');
    const tags = await App.DB.getAll('equipmentTags');

    const catCount = document.getElementById('catCountTypes');
    if (catCount) catCount.textContent = types.filter(t => t.active !== false).length;

    const uoMap = new Map(uos.map(u => [u.id, u.name]));

    const q = App.Utils.cleanStr(document.getElementById('searchEquipmentTypes')?.value);
    const activeFilter = document.getElementById('filterActiveEquipmentTypes')?.value || 'active';

    let filtered = types;
    if (q) filtered = filtered.filter(t => App.Utils.cleanStr(t.name).includes(q));
    if (activeFilter === 'active') filtered = filtered.filter(t => t.active);
    if (activeFilter === 'inactive') filtered = filtered.filter(t => !t.active);

    filtered.sort((a, b) => a.name.localeCompare(b.name));

    const tbody = document.getElementById('tbodyEquipmentTypes');
    tbody.innerHTML = filtered.map(t => {
      const tagCount = tags.filter(tg => tg.equipmentTypeId === t.id).length;
      return `
        <tr>
          <td><strong>${App.Utils.escapeHTML(t.name)}</strong></td>
          <td>${App.Utils.escapeHTML(uoMap.get(t.uoId) || '-')}</td>
          <td>${tagCount} TAG(s)</td>
          <td><span class="status-badge ${t.active ? 'normal' : 'inativo'}">${t.active ? 'Ativo' : 'Inativo'}</span></td>
          <td style="text-align: right; white-space: nowrap;">
            <button class="btn btn-outline btn-sm" onclick="App.UI.editEquipmentType('${t.id}')">Editar</button>
            <button class="btn btn-outline btn-sm" onclick="App.UI.toggleEquipmentTypeActive('${t.id}')">${t.active ? 'Inativar' : 'Ativar'}</button>
            <button class="btn btn-outline btn-sm" onclick="App.UI.deleteEquipmentType('${t.id}')">&times;</button>
          </td>
        </tr>
      `;
    }).join('');
  },

  renderEquipmentTagsTable: async function() {
    const tags = await App.DB.getAll('equipmentTags');
    const types = await App.DB.getAll('equipmentTypes');
    const uos = await App.DB.getAll('operationalUnits');

    const catCount = document.getElementById('catCountTags');
    if (catCount) catCount.textContent = tags.filter(t => t.active !== false).length;

    const uoMap = new Map(uos.map(u => [u.id, u.name]));
    const typeMap = new Map(types.map(t => [t.id, t.name]));

    const q = App.Utils.cleanStr(document.getElementById('searchTags')?.value);
    const activeFilter = document.getElementById('filterActiveTags')?.value || 'active';

    let filtered = tags;
    if (q) filtered = filtered.filter(t => App.Utils.cleanStr(t.tag).includes(q));
    if (activeFilter === 'active') filtered = filtered.filter(t => t.active);
    if (activeFilter === 'inactive') filtered = filtered.filter(t => !t.active);

    filtered.sort((a, b) => a.tag.localeCompare(b.tag));

    const tbody = document.getElementById('tbodyEquipmentTags');
    tbody.innerHTML = filtered.map(t => {
      return `
        <tr>
          <td><strong>${App.Utils.escapeHTML(t.tag)}</strong></td>
          <td>${App.Utils.escapeHTML(uoMap.get(t.uoId) || '-')}</td>
          <td>${App.Utils.escapeHTML(typeMap.get(t.equipmentTypeId) || '-')}</td>
          <td><span class="status-badge ${t.active ? 'normal' : 'inativo'}">${t.active ? 'Ativo' : 'Inativo'}</span></td>
          <td style="text-align: right; white-space: nowrap;">
            <button class="btn btn-outline btn-sm" onclick="App.UI.editEquipmentTag('${t.id}')">Editar</button>
            <button class="btn btn-outline btn-sm" onclick="App.UI.toggleEquipmentTagActive('${t.id}')">${t.active ? 'Inativar' : 'Ativar'}</button>
            <button class="btn btn-outline btn-sm" onclick="App.UI.deleteEquipmentTag('${t.id}')">&times;</button>
          </td>
        </tr>
      `;
    }).join('');
  },

  // --------------------------------------------------------------------------
  // AÇÕES CRUD DE CADASTROS (EDIT, INACTIVATE, DELETE)
  // --------------------------------------------------------------------------
  editConsole: async function(id) {
    const c = await App.DB.get('consoles', id);
    if (!c) return;
    document.getElementById('consoleEditId').value = c.id;
    document.getElementById('inputConsoleName').value = c.name;
    document.getElementById('btnCancelConsoleEdit').style.display = 'inline-flex';
    document.getElementById('btnSubmitConsole').textContent = 'Atualizar Console';
  },

  toggleConsoleActive: async function(id) {
    try {
      await App.Service.toggleConsoleActive(id);
      await this.initHeaderConsole();
      await this.renderConsolesTable();
    } catch (err) {
      this.showToast(err.message, 'danger');
    }
  },

  deleteConsole: async function(id) {
    this.showConfirmModal('Excluir Console', 'Deseja realmente excluir este console?', async () => {
      try {
        await App.Service.deleteConsole(id);
        this.showToast('Console excluído com sucesso.', 'info');
        await this.initHeaderConsole();
        await this.renderConsolesTable();
      } catch (err) {
        if (err.isDependencyError) {
          this.showDependencyModal('Console com Dependências', err.dependencies, async () => {
            await App.Service.toggleConsoleActive(id);
            this.showToast('Console inativado.', 'info');
            await this.initHeaderConsole();
            await this.renderConsolesTable();
          });
        } else {
          this.showToast(err.message, 'danger');
        }
      }
    });
  },

  editPipeline: async function(id) {
    const p = await App.DB.get('pipelines', id);
    if (!p) return;
    document.getElementById('pipelineEditId').value = p.id;
    document.getElementById('inputPipelineName').value = p.name;
    document.getElementById('selectPipelineConsole').value = p.consoleId;

    const links = await App.DB.getAll('pipelineOperationalUnits');
    const linkedUoIds = links.filter(l => l.pipelineId === p.id).map(l => l.uoId);

    document.querySelectorAll('#boxPipelineUOs input[type="checkbox"]').forEach(cb => {
      cb.checked = linkedUoIds.includes(cb.value);
    });

    document.getElementById('btnCancelPipelineEdit').style.display = 'inline-flex';
    document.getElementById('btnSubmitPipeline').textContent = 'Atualizar Duto';
  },

  togglePipelineActive: async function(id) {
    try {
      await App.Service.togglePipelineActive(id);
      await this.renderPipelinesTable();
    } catch (err) {
      this.showToast(err.message, 'danger');
    }
  },

  deletePipeline: async function(id) {
    this.showConfirmModal('Excluir Duto', 'Deseja realmente excluir este duto?', async () => {
      try {
        await App.Service.deletePipeline(id);
        this.showToast('Duto excluído com sucesso.', 'info');
        await this.renderPipelinesTable();
      } catch (err) {
        if (err.isDependencyError) {
          this.showDependencyModal('Duto com Dependências', err.dependencies, async () => {
            await App.Service.togglePipelineActive(id);
            this.showToast('Duto inativado.', 'info');
            await this.renderPipelinesTable();
          });
        } else {
          this.showToast(err.message, 'danger');
        }
      }
    });
  },

  editUO: async function(id) {
    const u = await App.DB.get('operationalUnits', id);
    if (!u) return;
    document.getElementById('uoEditId').value = u.id;
    document.getElementById('inputUOName').value = u.name;
    document.getElementById('btnCancelUOEdit').style.display = 'inline-flex';
    document.getElementById('btnSubmitUO').textContent = 'Atualizar UO';
  },

  toggleUOActive: async function(id) {
    try {
      await App.Service.toggleUOActive(id);
      await this.refreshAllMasterDataDropdowns();
      await this.renderUOsTable();
    } catch (err) {
      this.showToast(err.message, 'danger');
    }
  },

  deleteUO: async function(id) {
    this.showConfirmModal('Excluir UO', 'Deseja realmente excluir esta Unidade Operacional?', async () => {
      try {
        await App.Service.deleteUO(id);
        this.showToast('UO excluída com sucesso.', 'info');
        await this.refreshAllMasterDataDropdowns();
        await this.renderUOsTable();
      } catch (err) {
        if (err.isDependencyError) {
          this.showDependencyModal('UO com Dependências', err.dependencies, async () => {
            await App.Service.toggleUOActive(id);
            this.showToast('UO inativada com sucesso.', 'info');
            await this.refreshAllMasterDataDropdowns();
            await this.renderUOsTable();
          });
        } else {
          this.showToast(err.message, 'danger');
        }
      }
    });
  },

  editEquipmentType: async function(id) {
    const t = await App.DB.get('equipmentTypes', id);
    if (!t) return;
    document.getElementById('equipmentTypeEditId').value = t.id;
    document.getElementById('selectEquipmentTypeUO').value = t.uoId;
    document.getElementById('inputEquipmentTypeName').value = t.name;
    document.getElementById('btnCancelEquipmentTypeEdit').style.display = 'inline-flex';
    document.getElementById('btnSubmitEquipmentType').textContent = 'Atualizar Tipo';
  },

  toggleEquipmentTypeActive: async function(id) {
    try {
      await App.Service.toggleEquipmentTypeActive(id);
      await this.renderEquipmentTypesTable();
    } catch (err) {
      this.showToast(err.message, 'danger');
    }
  },

  deleteEquipmentType: async function(id) {
    this.showConfirmModal('Excluir Tipo', 'Deseja realmente excluir este tipo de equipamento?', async () => {
      try {
        await App.Service.deleteEquipmentType(id);
        this.showToast('Tipo de equipamento excluído com sucesso.', 'info');
        await this.renderEquipmentTypesTable();
      } catch (err) {
        if (err.isDependencyError) {
          this.showDependencyModal('Tipo com Dependências', err.dependencies, async () => {
            await App.Service.toggleEquipmentTypeActive(id);
            this.showToast('Tipo inativado.', 'info');
            await this.renderEquipmentTypesTable();
          });
        } else {
          this.showToast(err.message, 'danger');
        }
      }
    });
  },

  editEquipmentTag: async function(id) {
    const t = await App.DB.get('equipmentTags', id);
    if (!t) return;
    document.getElementById('tagEditId').value = t.id;
    document.getElementById('selectTagUO').value = t.uoId;
    await this.loadEquipmentTypeOptions(t.uoId, 'selectTagType', t.equipmentTypeId);
    document.getElementById('inputTagCode').value = t.tag;
    document.getElementById('btnCancelTagEdit').style.display = 'inline-flex';
    document.getElementById('btnSubmitTag').textContent = 'Atualizar TAG';
  },

  toggleEquipmentTagActive: async function(id) {
    try {
      await App.Service.toggleEquipmentTagActive(id);
      await this.renderEquipmentTagsTable();
    } catch (err) {
      this.showToast(err.message, 'danger');
    }
  },

  deleteEquipmentTag: async function(id) {
    this.showConfirmModal('Excluir TAG', 'Deseja realmente excluir este TAG?', async () => {
      try {
        await App.Service.deleteEquipmentTag(id);
        this.showToast('TAG excluído com sucesso.', 'info');
        await this.renderEquipmentTagsTable();
      } catch (err) {
        if (err.isDependencyError) {
          this.showDependencyModal('TAG com Dependências', err.dependencies, async () => {
            await App.Service.toggleEquipmentTagActive(id);
            this.showToast('TAG inativado com sucesso.', 'info');
            await this.renderEquipmentTagsTable();
          });
        } else {
          this.showToast(err.message, 'danger');
        }
      }
    });
  },

  // --------------------------------------------------------------------------
  // RENDERIZAÇÃO: CONFIGURAÇÕES DE ALERTAS, LAYOUT E TEMA
  // --------------------------------------------------------------------------
  renderConfigAlerts: async function() {
    const settings = await App.Service.getSettings();
    document.getElementById('inputSettingsUserName').value = settings.localUserName || 'Usuário local';
    document.getElementById('inputDefaultLeadTime').value = settings.defaultLeadTimeMinutes || 15;
    document.getElementById('selectSoundType').value = settings.soundType || 'chime';
    document.getElementById('rangeSoundVolume').value = settings.soundVolume || 80;
    document.getElementById('labelVolumeValue').textContent = `${settings.soundVolume || 80}%`;

    const selViewMode = document.getElementById('selectSettingsViewMode');
    if (selViewMode) selViewMode.value = settings.responsiveLayoutMode || 'auto';

    const selTheme = document.getElementById('selectSettingsTheme');
    if (selTheme) selTheme.value = settings.theme || 'dark';

    document.getElementById('checkSettingSound').checked = settings.soundEnabled;
    document.getElementById('checkSettingVisualModal').checked = settings.visualAlertEnabled;
    document.getElementById('checkSettingHighlightCard').checked = settings.highlightCardEnabled;
    document.getElementById('checkSettingPulsing').checked = settings.pulsingEnabled;
    document.getElementById('checkSettingChangeTitle').checked = settings.changeTitleEnabled;
    document.getElementById('checkSettingNotification').checked = settings.notificationEnabled;
    document.getElementById('checkSettingRepeat').checked = settings.repeatAlarm;
    document.getElementById('inputSettingRepeatInterval').value = settings.repeatIntervalMinutes || 2;
    document.getElementById('inputSettingMaxRepeats').value = settings.maxRepeats || 5;

    const notifState = App.Notifications.getPermissionState();
    const btnReq = document.getElementById('btnRequestNotifText');
    if (btnReq) {
      btnReq.textContent = notifState === 'concedida' ? 'Permissão Concedida' : (notifState === 'negada' ? 'Permissão Negada' : 'Solicitar Permissão');
    }
  },

  // --------------------------------------------------------------------------
  // RENDERIZAÇÃO: CONFIGURAÇÕES DE FAIXAS DE CORES
  // --------------------------------------------------------------------------
  renderConfigColors: async function() {
    const ranges = await App.Service.getColorRanges();

    const previewBar = document.getElementById('colorPreviewBar');
    if (previewBar) {
      previewBar.innerHTML = ranges.map(r => {
        const label = r.maxMinutes > 1000 ? `${r.minMinutes}+ min` : `${r.minMinutes} - ${r.maxMinutes} min`;
        return `
          <div class="preview-segment" style="flex: ${r.maxMinutes > 1000 ? 1 : Math.max(1, (r.maxMinutes - r.minMinutes))}; background-color: ${r.color};" title="${r.name} (${label})">
            ${r.name} (${label})
          </div>
        `;
      }).join('');
    }

    const chainPreview = document.getElementById('colorChainPreview');
    if (chainPreview && ranges.length > 0) {
      const sorted = [...ranges].sort((a, b) => a.minMinutes - b.minMinutes);
      const stops = sorted.map(r => r.maxMinutes > 1000 ? `${r.name} (${r.minMinutes}+)` : `${r.minMinutes} ─ ${r.maxMinutes} (${r.name})`).join(' ─ ');
      chainPreview.textContent = `Encadeamento: ${stops}`;
    }

    const cardsContainer = document.getElementById('containerColorRangeCards');
    if (cardsContainer) {
      cardsContainer.innerHTML = ranges.map(r => {
        return `
          <div class="card" style="padding: 0.75rem; margin-bottom: 0.5rem; border-left: 4px solid ${r.color};">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
              <strong>${App.Utils.escapeHTML(r.name)}</strong>
              <code>${r.color}</code>
            </div>
            <div style="font-size: 0.78rem; color: var(--text-secondary); margin-bottom: 0.5rem;">
              Intervalo: <strong>${r.minMinutes} min</strong> até <strong>${r.maxMinutes > 1000 ? '60+ min' : r.maxMinutes + ' min'}</strong> &bull;
              Pulsar: ${r.blink ? 'Sim' : 'Não'} &bull; Som: ${r.sound ? 'Sim' : 'Não'}
            </div>
            <div style="display: flex; gap: 0.4rem;">
              <button class="btn btn-outline btn-sm" onclick="App.UI.editRange('${r.id}')">Editar</button>
              <button class="btn btn-outline btn-sm" onclick="App.UI.deleteRange('${r.id}')">&times;</button>
            </div>
          </div>
        `;
      }).join('');
    }

    const tbody = document.getElementById('tbodyColorRanges');
    if (tbody) {
      tbody.innerHTML = ranges.map(r => {
        return `
          <tr>
            <td><strong>${App.Utils.escapeHTML(r.name)}</strong></td>
            <td>
              <div style="display: flex; align-items: center; gap: 0.4rem;">
                <span style="display: inline-block; width: 18px; height: 18px; border-radius: 4px; background: ${r.color}; border: 1px solid rgba(0,0,0,0.2);"></span>
                <code>${r.color}</code>
              </div>
            </td>
            <td>${r.minMinutes} min</td>
            <td>${r.maxMinutes > 1000 ? 'Sem limite (60+)' : r.maxMinutes + ' min'}</td>
            <td>${r.blink ? 'Sim (Pulsar)' : 'Não'}</td>
            <td>${r.sound ? 'Sim' : 'Não'}</td>
            <td>${r.priority}</td>
            <td style="text-align: right; white-space: nowrap;">
              <button class="btn btn-outline btn-sm" onclick="App.UI.editRange('${r.id}')">Editar</button>
              <button class="btn btn-outline btn-sm" onclick="App.UI.deleteRange('${r.id}')">&times;</button>
            </td>
          </tr>
        `;
      }).join('');
    }
  },

  editRange: async function(id) {
    const r = await App.DB.get('colorRanges', id);
    if (!r) return;
    document.getElementById('rangeEditId').value = r.id;
    document.getElementById('inputRangeName').value = r.name;
    document.getElementById('inputRangeColor').value = r.color;
    document.getElementById('inputRangeColorText').value = r.color;
    document.getElementById('inputRangeMin').value = r.minMinutes;
    document.getElementById('inputRangeMax').value = r.maxMinutes;
    document.getElementById('inputRangePriority').value = r.priority || 1;
    document.getElementById('checkRangeBlink').checked = !!r.blink;
    document.getElementById('checkRangeSound').checked = !!r.sound;
    document.getElementById('btnCancelRangeEdit').style.display = 'inline-flex';
    document.getElementById('btnSubmitRange').textContent = 'Atualizar Faixa';
  },

  resetRangeForm: function() {
    document.getElementById('rangeEditId').value = '';
    document.getElementById('formColorRange').reset();
    document.getElementById('btnCancelRangeEdit').style.display = 'none';
    document.getElementById('btnSubmitRange').textContent = 'Salvar Faixa de Cor';
  },

  deleteRange: async function(id) {
    this.showConfirmModal('Excluir Faixa', 'Deseja realmente excluir esta faixa de classificação?', async () => {
      try {
        await App.Service.deleteColorRange(id);
        this.showToast('Faixa de cor excluída com sucesso.', 'info');
        await this.renderConfigColors();
      } catch (err) {
        this.showToast(err.message, 'danger');
      }
    });
  },

  // --------------------------------------------------------------------------
  // RENDERIZAÇÃO: DIAGNÓSTICO TÉCNICO
  // --------------------------------------------------------------------------
  renderDiagnostic: async function() {
    const stores = [
      { name: 'consoles', desc: 'Consoles Operacionais (C02-C16)' },
      { name: 'pipelines', desc: 'Dutos de Transporte' },
      { name: 'operationalUnits', desc: 'Unidades Operacionais (UOs)' },
      { name: 'pipelineOperationalUnits', desc: 'Associações Dutos e UOs (M:N)' },
      { name: 'equipmentTypes', desc: 'Tipos de Equipamentos por UO' },
      { name: 'equipmentTags', desc: 'TAGs de Equipamentos por UO' },
      { name: 'events', desc: 'Previsões Operacionais (Pendentes e Concluídas)' },
      { name: 'eventHistory', desc: 'Trilha de Auditoria e Rastreabilidade' },
      { name: 'colorRanges', desc: 'Faixas de Tempo e Cores Configuradas' },
      { name: 'settings', desc: 'Configurações Globais da Aplicação' },
      { name: 'errorLogs', desc: 'Registro de Erros e Diagnóstico Interno' }
    ];

    const tbodyColls = document.getElementById('tbodyDiagCollections');
    if (tbodyColls) {
      let rowsHtml = '';
      for (const s of stores) {
        const items = await App.DB.getAll(s.name);
        const activeCount = items.filter(i => i.active !== false).length;
        const inactiveCount = items.filter(i => i.active === false).length;
        rowsHtml += `
          <tr>
            <td><code>${s.name}</code></td>
            <td style="color: var(--text-secondary);">${s.desc}</td>
            <td><strong>${items.length}</strong></td>
            <td><span style="color: #4ade80;">${activeCount}</span></td>
            <td><span style="color: #94a3b8;">${inactiveCount}</span></td>
          </tr>
        `;
      }
      tbodyColls.innerHTML = rowsHtml;
    }

    document.getElementById('diagDBStatus').textContent = 'Online (Ativo)';
    document.getElementById('diagAudioStatus').textContent = App.Audio.isUnlocked ? 'Pronto (Ativo)' : 'Aguardando Interação';
    document.getElementById('diagNotifStatus').textContent = App.Notifications.getPermissionState();

    const errorLogs = await App.DB.getAll('errorLogs');
    const tbodyLogs = document.getElementById('tbodyDiagLogs');
    if (tbodyLogs) {
      if (errorLogs.length === 0) {
        tbodyLogs.innerHTML = `<tr><td colspan="4" style="text-align: center; color: var(--text-muted); padding: 1.5rem;">Nenhum erro registrado no sistema.</td></tr>`;
      } else {
        errorLogs.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
        tbodyLogs.innerHTML = errorLogs.slice(0, 50).map(l => `
          <tr>
            <td style="white-space: nowrap; font-size: 0.75rem;">${App.Utils.formatDateTime(l.timestamp)}</td>
            <td><strong>${App.Utils.escapeHTML(l.context)}</strong></td>
            <td style="color: #f87171;">${App.Utils.escapeHTML(l.message)}</td>
            <td><pre style="font-size: 0.7rem; max-width: 300px; overflow: hidden; text-overflow: ellipsis;">${App.Utils.escapeHTML(l.details)}</pre></td>
          </tr>
        `).join('');
      }
    }
  },

  getDiagnosticReport: async function() {
    const report = {
      app: 'Caderno de Previsões Operacionais em Dutos',
      version: 'v1.0.0',
      generatedAt: new Date().toISOString(),
      userAgent: navigator.userAgent,
      audioState: App.Audio.ctx ? App.Audio.ctx.state : 'uninitialized',
      audioUnlocked: App.Audio.isUnlocked,
      notificationPermission: App.Notifications.getPermissionState(),
      collections: {}
    };

    const storeNames = [
      'consoles', 'pipelines', 'operationalUnits', 'pipelineOperationalUnits',
      'equipmentTypes', 'equipmentTags', 'events', 'eventHistory', 'colorRanges', 'settings', 'errorLogs'
    ];

    for (const name of storeNames) {
      const items = await App.DB.getAll(name);
      report.collections[name] = items.length;
    }
    return report;
  },

  // --------------------------------------------------------------------------
  // MODAIS E DIÁLOGOS
  // --------------------------------------------------------------------------
  bindModalEvents: function() {
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        document.querySelectorAll('.modal-overlay.active').forEach(modal => {
          modal.classList.remove('active');
        });
      }
    });

    document.querySelectorAll('.modal-overlay').forEach(overlay => {
      overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
          overlay.classList.remove('active');
        }
      });
    });

    ['btnCloseAlarmModal', 'btnCloseSnoozeModal', 'btnCancelSnooze', 'btnCloseCompleteModal',
     'btnCancelCompleteModal', 'btnCloseReopenModal', 'btnCancelReopenModal', 'btnCloseDetailsModal',
     'btnCloseDetailsModalBtn', 'btnCloseConfirmModal', 'btnCancelConfirm', 'btnCloseDependencyModal',
     'btnCloseDependencyModalBtn', 'btnCloseImportSummaryModal', 'btnCancelImportSummary',
     'btnCloseActionSheet', 'btnCloseAppStatusModal', 'btnCloseAppStatusFooter'].forEach(id => {
      document.getElementById(id)?.addEventListener('click', () => {
        const modal = document.getElementById(id).closest('.modal-overlay');
        if (modal) modal.classList.remove('active');
      });
    });

    // Quick Snooze buttons
    document.querySelectorAll('.btn-quick-snooze').forEach(btn => {
      btn.addEventListener('click', () => {
        document.getElementById('inputSnoozeMinutes').value = btn.getAttribute('data-min');
      });
    });

    // Confirmar Snooze
    document.getElementById('btnConfirmSnooze')?.addEventListener('click', async () => {
      const mins = parseInt(document.getElementById('inputSnoozeMinutes').value, 10) || 5;
      if (this.selectedEventForAction) {
        await App.Service.snoozeAlarm(this.selectedEventForAction.id, mins);
        document.getElementById('modalSnooze').classList.remove('active');
        document.getElementById('modalAlarmTrigger').classList.remove('active');
        this.showToast(`Alarme adiado por ${mins} minutos.`, 'info');
        await this.renderPendingEvents();
        await this.renderDashboard();
      }
    });

    // Ações do Modal de Disparo de Alarme
    document.getElementById('btnAlarmAcknowledge')?.addEventListener('click', async () => {
      if (this.selectedEventForAction) {
        await App.Service.acknowledgeAlarm(this.selectedEventForAction.id);
        document.getElementById('modalAlarmTrigger').classList.remove('active');
        this.showToast('Alarme reconhecido com sucesso.', 'info');
        await this.renderPendingEvents();
        await this.renderDashboard();
      }
    });

    document.getElementById('btnAlarmSnoozePrompt')?.addEventListener('click', () => {
      document.getElementById('modalSnooze').classList.add('active');
    });

    document.getElementById('btnAlarmCompleteDirect')?.addEventListener('click', () => {
      document.getElementById('modalAlarmTrigger').classList.remove('active');
      if (this.selectedEventForAction) {
        this.showCompleteModal(this.selectedEventForAction.id);
      }
    });

    document.getElementById('btnAlarmOpenDetails')?.addEventListener('click', () => {
      document.getElementById('modalAlarmTrigger').classList.remove('active');
      if (this.selectedEventForAction) {
        this.showDetailsModal(this.selectedEventForAction.id);
      }
    });

    // Confirmar Conclusão
    document.getElementById('btnConfirmCompleteModal')?.addEventListener('click', async () => {
      if (this.selectedEventForAction) {
        const note = document.getElementById('inputCompleteNotes').value;
        await App.Service.completeEvent(this.selectedEventForAction.id, note);
        document.getElementById('modalCompleteEvent').classList.remove('active');
        this.showToast('Previsão operacional concluída com sucesso!', 'success');
        await this.renderPendingEvents();
        await this.renderDashboard();
        if (this.currentView === 'viewCompletedEvents') {
          await this.renderCompletedEvents();
        }
      }
    });

    // Confirmar Reabertura
    document.getElementById('btnConfirmReopenModal')?.addEventListener('click', async () => {
      if (this.selectedEventForAction) {
        const newD = document.getElementById('inputReopenDate').value;
        const newT = document.getElementById('inputReopenTime').value;
        await App.Service.reopenEvent(this.selectedEventForAction.id, newD, newT);
        document.getElementById('modalReopenEvent').classList.remove('active');
        this.showToast('Evento reaberto com sucesso e devolvido aos pendentes.', 'info');
        await this.renderCompletedEvents();
        await this.renderDashboard();
      }
    });
  },

  showAlarmModal: async function(event, isTest = false) {
    this.selectedEventForAction = event;
    const consoles = await App.DB.getAll('consoles');
    const pipelines = await App.DB.getAll('pipelines');
    const uos = await App.DB.getAll('operationalUnits');
    const tags = await App.DB.getAll('equipmentTags');

    const con = consoles.find(c => c.id === event.consoleId);
    const pipe = pipelines.find(p => p.id === event.pipelineId);
    const uo = uos.find(u => u.id === event.uoId);
    const tag = tags.find(t => t.id === event.tagId);

    const path = `${con ? con.name : 'Console'} | ${pipe ? pipe.name : 'Duto'} | ${uo ? uo.name : 'UO'} ${tag ? '| ' + tag.tag : ''}`;

    document.getElementById('alarmModalHierarchy').textContent = path;
    document.getElementById('alarmModalDescription').textContent = event.description;
    document.getElementById('alarmModalNotes').textContent = event.notes ? `Observações: ${event.notes}` : '';
    document.getElementById('alarmModalScheduledTime').textContent = App.Utils.formatDateTime(event.scheduledDate, event.scheduledTime);

    const timerInfo = App.Utils.formatTimeRemaining(new Date(event.scheduledAt).getTime());
    document.getElementById('alarmModalCountdown').textContent = isTest ? 'Alarme de Teste' : timerInfo.text;

    document.getElementById('modalAlarmTrigger').classList.add('active');
  },

  showSnoozeModal: function(eventId) {
    App.DB.get('events', eventId).then(ev => {
      if (!ev) return;
      this.selectedEventForAction = ev;
      document.getElementById('inputSnoozeMinutes').value = 5;
      document.getElementById('modalSnooze').classList.add('active');
    });
  },

  showCompleteModal: async function(eventId) {
    const event = await App.DB.get('events', eventId);
    if (!event) return;
    this.selectedEventForAction = event;

    const consoles = await App.DB.getAll('consoles');
    const pipelines = await App.DB.getAll('pipelines');
    const uos = await App.DB.getAll('operationalUnits');
    const tags = await App.DB.getAll('equipmentTags');

    const con = consoles.find(c => c.id === event.consoleId);
    const pipe = pipelines.find(p => p.id === event.pipelineId);
    const uo = uos.find(u => u.id === event.uoId);
    const tag = tags.find(t => t.id === event.tagId);

    document.getElementById('completeModalEventDesc').textContent = event.description;
    document.getElementById('completeModalHierarchy').textContent = `${con ? con.name : ''} • ${pipe ? pipe.name : ''} • ${uo ? uo.name : ''} ${tag ? '• ' + tag.tag : ''}`;

    const schedStr = App.Utils.formatDateTime(event.scheduledDate, event.scheduledTime);
    const now = new Date();
    const actualStr = App.Utils.formatDateTime(now.toISOString());
    const diffMins = (now.getTime() - new Date(event.scheduledAt).getTime()) / 60000;

    document.getElementById('completeModalScheduledTime').textContent = schedStr;
    document.getElementById('completeModalActualTime').textContent = actualStr;
    document.getElementById('completeModalTimeDiff').textContent = App.Utils.formatDiffMinutes(diffMins);
    document.getElementById('inputCompleteNotes').value = '';

    document.getElementById('modalCompleteEvent').classList.add('active');
  },

  showReopenModal: async function(eventId) {
    const event = await App.DB.get('events', eventId);
    if (!event) return;
    this.selectedEventForAction = event;

    const now = new Date();
    const isPast = new Date(event.scheduledAt).getTime() < now.getTime();
    const boxWarning = document.getElementById('boxReopenPastWarning');
    boxWarning.style.display = isPast ? 'flex' : 'none';

    if (isPast) {
      now.setHours(now.getHours() + 1);
      const y = now.getFullYear();
      const m = String(now.getMonth() + 1).padStart(2, '0');
      const d = String(now.getDate()).padStart(2, '0');
      const hh = String(now.getHours()).padStart(2, '0');
      const mm = String(now.getMinutes()).padStart(2, '0');
      document.getElementById('inputReopenDate').value = `${y}-${m}-${d}`;
      document.getElementById('inputReopenTime').value = `${hh}:${mm}`;
    } else {
      document.getElementById('inputReopenDate').value = event.scheduledDate;
      document.getElementById('inputReopenTime').value = event.scheduledTime;
    }

    document.getElementById('modalReopenEvent').classList.add('active');
  },

  showDetailsModal: async function(eventId) {
    const event = await App.DB.get('events', eventId);
    if (!event) return;

    const consoles = await App.DB.getAll('consoles');
    const pipelines = await App.DB.getAll('pipelines');
    const uos = await App.DB.getAll('operationalUnits');
    const types = await App.DB.getAll('equipmentTypes');
    const tags = await App.DB.getAll('equipmentTags');

    const con = consoles.find(c => c.id === event.consoleId);
    const pipe = pipelines.find(p => p.id === event.pipelineId);
    const uo = uos.find(u => u.id === event.uoId);
    const type = types.find(t => t.id === event.equipmentTypeId);
    const tag = tags.find(t => t.id === event.tagId);

    document.getElementById('detailsModalPath').textContent = `${con ? con.name : ''} / ${pipe ? pipe.name : ''} / ${uo ? uo.name : ''}`;
    document.getElementById('detailsModalEquipment').textContent = `${type ? type.name : 'Geral'} ${tag ? '(' + tag.tag + ')' : ''}`;
    document.getElementById('detailsModalSchedule').textContent = App.Utils.formatDateTime(event.scheduledDate, event.scheduledTime);
    document.getElementById('detailsModalStatus').textContent = event.status === 'concluido' ? 'Concluído' : 'Pendente';
    document.getElementById('detailsModalDescription').textContent = event.description;
    document.getElementById('detailsModalNotes').textContent = event.notes || 'Sem observações complementares.';

    // Exibir anotação gráfica / stylus unificada (Fix #10 da Seção 24)
    let drawingContainer = document.getElementById('detailsStylusContainer') || document.getElementById('detailsModalDrawingBox');
    if (!drawingContainer) {
      drawingContainer = document.createElement('div');
      drawingContainer.id = 'detailsStylusContainer';
      drawingContainer.style.marginTop = '1rem';
      document.getElementById('detailsModalNotes').parentNode.appendChild(drawingContainer);
    }

    if (event.stylusDrawing) {
      const existingImg = document.getElementById('detailsModalDrawingImg');
      if (existingImg) {
        existingImg.src = event.stylusDrawing;
      } else {
        drawingContainer.innerHTML = `
          <div style="font-size: 0.8rem; font-weight: 700; margin-bottom: 0.35rem; color: var(--accent);">
            &#x270E; Anotação Manual / Esboço Registrado:
          </div>
          <div style="background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); border-radius: var(--radius-sm); padding: 0.5rem; text-align: center;">
            <img id="detailsModalDrawingImg" src="${event.stylusDrawing}" alt="Esboço manual" style="max-width: 100%; height: auto; max-height: 240px; border-radius: 4px;">
          </div>
        `;
      }
      drawingContainer.style.display = 'block';
    } else {
      drawingContainer.style.display = 'none';
    }

    // Buscar histórico de auditoria
    const allHistory = await App.DB.getAll('eventHistory');
    const eventHist = allHistory.filter(h => h.eventId === eventId);
    eventHist.sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());

    const timeline = document.getElementById('detailsTimeline');
    if (eventHist.length === 0) {
      timeline.innerHTML = `<div style="color: var(--text-muted); font-size: 0.85rem;">Nenhum registro de auditoria encontrado.</div>`;
    } else {
      timeline.innerHTML = eventHist.map(h => {
        return `
          <div class="timeline-item">
            <div class="timeline-point"></div>
            <div class="timeline-content">
              <div class="timeline-meta">
                <span>${App.Utils.formatDateTime(h.timestamp)}</span>
                <span>Responsável: <strong>${App.Utils.escapeHTML(h.localUser)}</strong></span>
              </div>
              <div class="timeline-title">${App.Utils.escapeHTML(h.action.toUpperCase())}</div>
              <div class="timeline-desc">${App.Utils.escapeHTML(h.description)}</div>
            </div>
          </div>
        `;
      }).join('');
    }

    document.getElementById('modalEventDetails').classList.add('active');
  },

  showConfirmModal: function(title, message, onConfirm) {
    document.getElementById('modalConfirmTitle').textContent = title;
    document.getElementById('modalConfirmMessage').textContent = message;
    const btnAccept = document.getElementById('btnAcceptConfirm');

    const handler = () => {
      btnAccept.removeEventListener('click', handler);
      document.getElementById('modalConfirm').classList.remove('active');
      if (onConfirm) onConfirm();
    };

    btnAccept.addEventListener('click', handler);
    document.getElementById('modalConfirm').classList.add('active');
  },

  showDependencyModal: function(title, reasons, onInactivate) {
    document.getElementById('modalDependencyTitle').textContent = title;
    const list = document.getElementById('modalDependencyList');
    list.innerHTML = reasons.map(r => `<li>${App.Utils.escapeHTML(r)}</li>`).join('');

    const btnInact = document.getElementById('btnDependencyInactivate');
    const handler = () => {
      btnInact.removeEventListener('click', handler);
      document.getElementById('modalDependency').classList.remove('active');
      if (onInactivate) onInactivate();
    };
    btnInact.addEventListener('click', handler);

    document.getElementById('modalDependency').classList.add('active');
  },

  showImportSummaryModal: function(parsedBackup) {
    const data = parsedBackup.data;
    const summaryBox = document.getElementById('importSummaryCounts');
    summaryBox.innerHTML = `
      <div><strong>Versão do Esquema:</strong> ${parsedBackup.schemaVersion}</div>
      <div><strong>Data da Exportação:</strong> ${App.Utils.formatDateTime(parsedBackup.exportedAt)}</div>
      <div style="margin-top: 0.5rem; display: grid; grid-template-columns: 1fr 1fr; gap: 0.25rem;">
        <div>Consoles: ${(data.consoles || []).length}</div>
        <div>Dutos: ${(data.pipelines || []).length}</div>
        <div>UOs: ${(data.operationalUnits || []).length}</div>
        <div>Tipos: ${(data.equipmentTypes || []).length}</div>
        <div>TAGs: ${(data.equipmentTags || []).length}</div>
        <div>Eventos: ${(data.events || []).length}</div>
      </div>
    `;

    const btnConfirm = document.getElementById('btnConfirmImportSummary');
    const handler = async () => {
      btnConfirm.removeEventListener('click', handler);
      const mode = document.querySelector('input[name="importMode"]:checked').value;
      try {
        await App.Backup.importJSON(parsedBackup, mode);
        document.getElementById('modalImportSummary').classList.remove('active');
        this.showToast(`Backup importado com sucesso (Modo: ${mode === 'replace' ? 'Substituição' : 'Mesclagem'}).`, 'success');
        await this.initHeaderConsole();
        await this.renderDashboard();
      } catch (err) {
        this.showToast(err.message, 'danger');
      }
    };

    btnConfirm.addEventListener('click', handler);
    document.getElementById('modalImportSummary').classList.add('active');
  },

  showToast: function(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
      <div style="flex: 1;">${App.Utils.escapeHTML(message)}</div>
      <button style="background: none; border: none; color: inherit; cursor: pointer; font-size: 1.1rem; line-height: 1;">&times;</button>
    `;

    const closeBtn = toast.querySelector('button');
    closeBtn.addEventListener('click', () => {
      toast.remove();
    });

    container.appendChild(toast);
    setTimeout(() => {
      if (toast.parentNode) {
        toast.remove();
      }
    }, 4500);
  },

  acknowledgeAlarm: async function(eventId) {
    try {
      await App.Service.acknowledgeAlarm(eventId);
      this.showToast('Alarme reconhecido.', 'info');
      await this.renderPendingEvents();
      await this.renderDashboard();
    } catch (err) {
      this.showToast(err.message, 'danger');
    }
  },

  deleteEvent: function(eventId) {
    this.showConfirmModal('Excluir Previsão', 'Deseja realmente excluir esta previsão e seu histórico?', async () => {
      try {
        await App.Service.deleteEvent(eventId);
        this.showToast('Previsão excluída.', 'info');
        await this.renderPendingEvents();
        await this.renderDashboard();
        if (this.currentView === 'viewCompletedEvents') {
          await this.renderCompletedEvents();
        }
      } catch (err) {
        this.showToast(err.message, 'danger');
      }
    });
  },

  bindGlobalEvents: function() {
    const unlockAudio = () => {
      App.Audio.unlock();
      window.removeEventListener('click', unlockAudio);
      window.removeEventListener('keydown', unlockAudio);
    };
    window.addEventListener('click', unlockAudio, { once: true });
    window.addEventListener('keydown', unlockAudio, { once: true });

    const handleAudioClick = () => {
      App.Audio.unlock();
      App.Audio.play('chime');
      this.showToast('Áudio ativado com sucesso!', 'success');
    };

    document.getElementById('pillAudio')?.addEventListener('click', handleAudioClick);
    document.getElementById('chipHeaderAudioWarning')?.addEventListener('click', handleAudioClick);

    document.getElementById('pillNotif')?.addEventListener('click', async () => {
      await App.Notifications.requestPermission();
    });
  }
};

/* ==========================================================================
   10. INICIALIZAÇÃO DA APLICAÇÃO
   ========================================================================== */
window.addEventListener('DOMContentLoaded', async () => {
  try {
    await App.DB.open();
    await App.DB.initDefaults();
    await App.UI.init();
    console.log('Caderno de Previsões Operacionais em Dutos inicializado com sucesso.');
  } catch (err) {
    console.error('Falha crítica na inicialização da aplicação:', err);
    alert('Erro ao inicializar o banco de dados local da aplicação: ' + (err.message || err));
  }
});

  