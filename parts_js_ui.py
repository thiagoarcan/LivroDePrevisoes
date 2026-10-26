# -*- coding: utf-8 -*-
JS_UI = """
/* ==========================================================================
   9. CAMADA DE INTERFACE COM O USUÁRIO (UI CONTROLLER)
   ========================================================================== */
App.UI = {
  modalStack: [],
  modalActions: new Map(),
  modalBusy: new Set(),
  modalRequests: new Map(),
  pageSize: 50,
  pages: {pending: 1, completed: 1},
  renderedListModalities: {},
  expandedCompletedIds: new Set(),
  getListModality: function(kind) {
    if(kind==='pending')return this.viewMode;
    return this.getEffectiveViewportTier()==='mobile' || window.innerWidth<768 ? 'cards' : 'table';
  },
  syncActiveListModality: function() {
    if(this._listModalityTask)return this._listModalityTask;
    const update=async()=>{
      while(true){
        const view=this.currentView,kind=view==='viewCompletedEvents'?'completed':view==='viewPendingEvents'?'pending':null;
        if(!kind || this.renderedListModalities[kind]===this.getListModality(kind))return;
        const scroll={x:window.scrollX,y:window.scrollY};
        const positions=[...document.querySelectorAll(kind==='completed'?'#containerCompletedCards,#tableCompletedWrapper':'#containerPendingCards,#containerPendingTable')].map(element=>({element,top:element.scrollTop,left:element.scrollLeft}));
        await this[kind==='completed'?'renderCompletedEvents':'renderPendingEvents']();
        if(this.currentView===view){for(const p of positions){p.element.scrollTop=p.top;p.element.scrollLeft=p.left;}window.scrollTo(scroll.x,scroll.y);}
      }
    };
    this._listModalityTask=update().finally(()=>{this._listModalityTask=null;});
    return this._listModalityTask;
  },
  localDate: function(value = Date.now()) {
    const d = new Date(value);
    return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
  },
  isSafeDrawing: function(value) {
    return typeof value === 'string' && value.length <= 3000000 && value.startsWith('data:image/png;base64,iVBORw0KGgo');
  },
  formatCountdown: function(timestamp) {
    const diff=Number(timestamp)-Date.now(),seconds=Math.floor(Math.abs(diff)/1000);
    const hours=Math.floor(seconds/3600),minutes=Math.floor(seconds%3600/60),remaining=seconds%60;
    const text=(hours?`${hours}h `:'')+`${String(minutes).padStart(2,'0')}min ${String(remaining).padStart(2,'0')}s`;
    return {text:(diff<0?'Atrasado há ':'Faltam ')+text,isOverdue:diff<0};
  },
  notifyPresentation: function(reason, eventId) {
    window.dispatchEvent(new CustomEvent('app-ui-update', {detail:{reason,view:this.currentView,eventId}}));
  },
  refreshPresentationCache: async function() {
    this._snapshot = await App.DB.snapshot();
    this._settings = this._snapshot.settings.find(x=>x.key === 'app_settings')?.value || {...App.Config.DEFAULT_SETTINGS};
    this._ranges = this._snapshot.colorRanges.filter(x=>x.active !== false);
    this._temporalSignature = this.temporalSignature();
    this.applyVisualPreferences();
  },
  publishCatalogChange: async function() {
    await this.refreshPresentationCache();
    this.populateFilterDropdowns(this._snapshot.consoles,this._snapshot.pipelines,this._snapshot.operationalUnits);
    this.notifyPresentation('catalog');
  },
  getPresentationState: function() {
    return {snapshot:this._snapshot,settings:this._settings,ranges:this._ranges,view:this.currentView,
      activeConsoleId:this.activeConsoleId,pending:this.activePendingEvents,completed:this.activeCompletedEvents || [],
      selectedEventId:this.currentView==='viewCompletedEvents'?this.selectedCompletedEventId:this.currentView==='viewDashboard'?this.spotlightEventId:this.selectedDetailEventId,
      selections:{pending:this.selectedDetailEventId,completed:this.selectedCompletedEventId,dashboard:this.spotlightEventId},spotlightEventId:this.spotlightEventId,
      category:this.currentCadastrosCategory,tier:this.getEffectiveViewportTier(),metricFilter:this.metricFilter,
      filters:Object.fromEntries([...document.querySelectorAll('#filterDrawer input,#filterDrawer select')].map(e=>[e.id,e.type==='checkbox'?e.checked:e.value])),
      classifyEvent:event=>App.Service.classifyEvent(event,this._ranges || [])};
  },
  temporalSignature: function() {
    return (this._snapshot?.events || []).filter(e=>e.active!==false && e.status==='pendente').map(e=>{
      const minutes=(new Date(e.scheduledAt).getTime()-Date.now())/60000;
      const window=minutes<0?'overdue':minutes<=15?'15min':minutes<=30?'30min':minutes<=60?'60min':'later';
      return e.id+':'+App.Service.classifyEvent(e,this._ranges||[]).key+':'+window+':'+e.alarmState;
    }).join('|')+'|'+this.localDate();
  },
  applyVisualPreferences: function() {
    const settings=this._settings || {};
    document.body.classList.toggle('disable-pulsing',settings.pulsingEnabled===false);
    document.body.classList.toggle('disable-highlight',settings.highlightCardEnabled===false);
    if(settings.pulsingEnabled===false || matchMedia('(prefers-reduced-motion: reduce)').matches)
      document.querySelectorAll('.pulsing-card,.pulsing-badge').forEach(e=>e.classList.remove('pulsing-card','pulsing-badge'));
    if(settings.highlightCardEnabled===false) document.getElementById('spotlightCard')?.classList.remove('highlight-card','alarm-triggered');
  },
  reloadPreferences: async function() {
    const settings=await App.Service.getSettings();this._settings=settings;
    this.activeConsoleId=settings.activeConsoleId || null;
    this.applyTheme(settings.theme || 'dark');
    this.viewMode=['cards','table'].includes(settings.viewMode)?settings.viewMode:'cards';this.updateViewModeUI();
    await this.applyResponsiveLayoutMode(settings.responsiveLayoutMode || 'auto',false);
    document.getElementById('headerUserName').textContent=settings.localUserName;
    const drawerUser=document.getElementById('labelDrawerUser');if(drawerUser)drawerUser.textContent='Usuário: '+settings.localUserName;
    const user=document.getElementById('inputSettingsUserName');if(user)user.value=settings.localUserName;
    this.updateBackupPill(settings.lastBackupAt);
    await this.initHeaderConsole();await this.refreshAllMasterDataDropdowns();await this.refreshPresentationCache();
    this.populateFilterDropdowns(this._snapshot.consoles,this._snapshot.pipelines,this._snapshot.operationalUnits);
    await this.renderConfigAlerts();this.notifyPresentation('import');
  },
  clearPendingFilters: function() {
    for(const id of ['inputSearchPending','filterConsole','filterPipeline','filterUO','filterStatus','filterAlarm','filterPriority','filterDateFrom','filterDateTo']){
      const e=document.getElementById(id);if(e)e.value='';
    }
    this.metricFilter=null;this.pages.pending=1;
  },
  applyMetricFilter: function(events) {
    const filter=this.metricFilter;
    return events.filter(e=>{const minutes=(new Date(e.scheduledAt).getTime()-Date.now())/60000;
      if(filter==='overdue')return minutes<0;if(filter==='unacknowledged')return e.alarmState==='triggered';
      if(filter==='15min')return minutes>=0 && minutes<=15;if(filter==='30min')return minutes>15 && minutes<=30;
      if(filter==='60min')return minutes>30 && minutes<=60;return true;});
  },
  paginateEvents: function(kind,events) {
    const key=events.map(e=>e.id).join('|');
    this._pageKeys ||= {};
    if(this._pageKeys[kind]!==key){this.pages[kind]=1;this._pageKeys[kind]=key;}
    const count=Math.max(1,Math.ceil(events.length/this.pageSize));
    this.pages[kind]=Math.min(count,Math.max(1,this.pages[kind]||1));
    const id=kind+'Pagination';let nav=document.getElementById(id);
    if(!nav){nav=document.createElement('nav');nav.id=id;nav.className='events-pagination';nav.setAttribute('aria-label',kind==='pending'?'Páginas de previsões pendentes':'Páginas de previsões concluídas');document.getElementById(kind==='pending'?'pendingEmptyMessage':'completedEmptyMessage').before(nav);}
    nav.replaceChildren();
    const label=document.createElement('span');label.textContent=`${events.length} resultado(s) • Página ${this.pages[kind]} de ${count}`;
    for(const [text,delta] of [['Anterior',-1],['Próxima',1]]){
      const button=document.createElement('button');button.type='button';button.className='btn btn-outline btn-sm';button.textContent=text;
      button.disabled=delta<0?this.pages[kind]<=1:this.pages[kind]>=count;
      button.onclick=()=>{this.pages[kind]+=delta;this[kind==='pending'?'renderPendingEvents':'renderCompletedEvents']();};nav.append(button);
    }
    nav.prepend(label);
    return events.slice((this.pages[kind]-1)*this.pageSize,this.pages[kind]*this.pageSize);
  },
  toggleCompletedCard: function(card) {
    const expanded=card.classList.toggle('expanded');card.setAttribute('aria-expanded',String(expanded));
    if(expanded)this.expandedCompletedIds.add(card.dataset.eventId);else this.expandedCompletedIds.delete(card.dataset.eventId);
    const details=card.querySelector('.completed-card-details');details.hidden=!expanded;details.style.display=expanded?'block':'none';
    this.selectedCompletedEventId=card.dataset.eventId;this.notifyPresentation('selection',card.dataset.eventId);
  },
  movePendingSelection: function(direction) {
    const index=this.activePendingEvents.findIndex(e=>e.id===this.selectedDetailEventId);
    const event=this.activePendingEvents[index+direction];if(event)this.selectPendingDetailEvent(event.id);
  },
  selectCompletedEvent: function(eventId) {
    this.selectedCompletedEventId=eventId;this.notifyPresentation('selection',eventId);
  },
  focusable: function(root) {
    return [...root.querySelectorAll('button,a[href],input,select,textarea,[tabindex]')].filter(e=>!e.disabled && e.tabIndex>=0 && !e.closest('[inert]') && e.getClientRects().length);
  },
  syncModalInert: function() {
    for(const e of this._inerted || []) e.inert=false;
    this._inerted=[];
    const top=this.modalStack.at(-1)?.element;
    if(top){let node=top;while(node.parentElement && node.parentElement!==document.documentElement){for(const sibling of node.parentElement.children){if(sibling!==node && !['SCRIPT','STYLE'].includes(sibling.tagName) && sibling.id!=='toastContainer'){if(!sibling.inert){sibling.inert=true;this._inerted.push(sibling);}}}node=node.parentElement;}}
    const drawer=document.getElementById('appMobileDrawer');if(drawer && top!==drawer && !drawer.classList.contains('open'))drawer.inert=true;
    for(const entry of this.modalStack)if(entry.element!==top){entry.element.inert=true;this._inerted.push(entry.element);}
  },
  beginModalRequest: function(id, eventId) {
    if(this.modalBusy.has(id))return null;
    const generation=(this.modalRequests.get(id)||0)+1;
    this.modalRequests.set(id,generation);
    return {id,eventId,generation,returnFocus:document.activeElement};
  },
  isModalRequestCurrent: function(request) {
    return Boolean(request && this.modalRequests.get(request.id)===request.generation && !this.modalBusy.has(request.id));
  },
  openModal: function(id, event = null, request = null) {
    if(this.modalBusy.has(id) || (request && !this.isModalRequestCurrent(request)))return false;
    const element=document.getElementById(id);if(!element)return;
    const current=this.modalStack.find(e=>e.element===element);
    if(!current)this.modalStack.push({element,returnFocus:request?.returnFocus || document.activeElement,event});
    else current.event=event;
    if(event)this.selectedEventForAction=event;
    element.inert=false;element.hidden=false;element.classList.add('active');element.setAttribute('role','dialog');element.setAttribute('aria-modal','true');element.tabIndex=-1;
    if(!element.getAttribute('aria-label')&&!element.getAttribute('aria-labelledby'))element.setAttribute('aria-label',element.querySelector('.modal-header,h2,h3')?.textContent.trim() || 'Diálogo');
    element.setAttribute('aria-hidden','false');this.syncModalInert();
    (this.focusable(element)[0] || element).focus();
  },
  closeModal: function(id, force=false) {
    if(this.modalBusy.has(id)&&!force)return false;
    this.modalRequests.set(id,(this.modalRequests.get(id)||0)+1);
    const index=this.modalStack.findIndex(x=>x.element.id===id),entry=this.modalStack[index];
    const element=document.getElementById(id);this.modalActions.delete(id);
    if(element){element.classList.remove('active','open','active-sheet');element.setAttribute('aria-hidden','true');element.removeAttribute('aria-modal');}
    if(id==='appMobileDrawer'){document.getElementById('mobileDrawerOverlay')?.classList.remove('open','active');document.getElementById('btnToggleMobileMenu')?.setAttribute('aria-expanded','false');if(element)element.inert=true;}
    if(id==='filterDrawer'){element.style.display='none';document.getElementById('btnToggleFilters')?.setAttribute('aria-expanded','false');}
    if(id==='boxStylusCanvas'){
      element.classList.remove('fullscreen-lousa');
      const button=document.getElementById('btnFullscreenStylusCanvas');button.textContent='⛶ Tela Cheia';button.classList.remove('btn-primary');button.classList.add('btn-outline');
    }
    if(entry)this.modalStack.splice(index,1);
    this.syncModalInert();
    const top=this.modalStack.at(-1);if(top)this.selectedEventForAction=top.event;
    if(entry?.returnFocus?.isConnected && !entry.returnFocus.closest('[inert]'))entry.returnFocus.focus();
    else if(top)(this.focusable(top.element)[0]||top.element).focus();
    return true;
  },
  setModalAction: function(id,buttonId,action) {
    this.modalActions.set(id,action);
    const button=document.getElementById(buttonId);button.disabled=false;
    button.onclick=()=>{
      if(this.modalBusy.has(id))return;
      const callback=this.modalActions.get(id);if(!callback)return;
      this.modalActions.delete(id);this.modalBusy.add(id);button.disabled=true;
      let result;
      try{result=callback();}catch(error){result=Promise.reject(error);}
      Promise.resolve(result).then(value=>{if(value!==false)this.closeModal(id,true);else if(this.modalStack.some(x=>x.element.id===id))this.modalActions.set(id,callback);})
      .catch(error=>{this.showToast(error.message,'danger');App.DB.logError(error,'Interface: '+id);if(this.modalStack.some(x=>x.element.id===id))this.modalActions.set(id,callback);})
      .finally(()=>{this.modalBusy.delete(id);button.disabled=false;});
    };
  },
  updateKeyboardState: function() {
    const viewport=window.visualViewport,focused=document.activeElement;
    const editable=Boolean(focused && !focused.disabled && !focused.readOnly && (focused.isContentEditable || focused.tagName==='TEXTAREA' || focused.tagName==='INPUT' && ['text','search','email','url','tel','number','password','date','time','datetime-local'].includes(focused.type)));
    // Pinch changes visual height and scale together; normalize them before
    // comparing to the layout viewport. Height alone is not a keyboard signal.
    const available=viewport ? viewport.height*(viewport.scale || 1) : window.innerHeight;
    document.body.classList.toggle('keyboard-open',editable && available<window.innerHeight*.7);
  },
  initUIController: function() {
    if(!this._settings.firstMobileNoticeShown && this.getEffectiveViewportTier()==='mobile'){
      const notice=document.createElement('aside');notice.id='appRuntimeNotice';notice.className='runtime-notice';notice.setAttribute('role','note');
      const text=document.createElement('p');text.textContent='Mantenha esta aplicação aberta e o áudio ativado. O navegador pode suspender alarmes em segundo plano ou com a tela bloqueada. Exporte backups dos dados locais.';
      const dismiss=document.createElement('button');dismiss.type='button';dismiss.className='btn btn-outline btn-sm';dismiss.textContent='Entendi';dismiss.onclick=async()=>{const settings=await App.Service.getSettings();settings.firstMobileNoticeShown=true;await App.Service.saveSettings(settings);notice.remove();};
      notice.append(text,dismiss);document.querySelector('.app-main')?.prepend(notice);
    }
    document.querySelectorAll('[role=dialog],.modal-overlay').forEach(e=>{
      if(!e.getAttribute('aria-label')&&!e.getAttribute('aria-labelledby'))e.setAttribute('aria-label',e.querySelector('h2,h3,.modal-header')?.textContent.trim() || 'Diálogo');
    });
    document.querySelectorAll('.metric-card[data-filter]').forEach(e=>{e.setAttribute('role','button');e.tabIndex=0;e.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();e.click();}});});
    const header=document.querySelector('.app-header');
    if(header && window.ResizeObserver)new ResizeObserver(()=>document.documentElement.style.setProperty('--app-header-height',header.getBoundingClientRect().height+'px')).observe(header);
    window.addEventListener('alarm-engine-tick',async e=>{
      const ids=(e.detail.triggeredIds || []).slice().sort().join('|');
      if(ids!==this._triggeredIds){this._triggeredIds=ids;await this.refreshPresentationCache();await this.renderDashboard();if(this.currentView==='viewPendingEvents')await this.renderPendingEvents();}
      await this.updateLiveTimers();
    });
    if(window.visualViewport)visualViewport.addEventListener('resize',()=>this.updateKeyboardState());
    document.addEventListener('focusin',()=>this.updateKeyboardState());
    document.addEventListener('focusout',()=>this.updateKeyboardState());
    this.notifyPresentation('init');
  },
  currentView: 'viewDashboard',
  viewMode: 'cards', // 'cards' ou 'table' para lista de pendentes
  responsiveLayoutMode: 'auto', // 'auto', 'compact', 'mobile', 'tablet', 'conventional', 'widescreen', 'ultrawide'
  activePendingEvents: [],
  selectedEventForAction: null,
  selectedDetailEventId: null,
  selectedDetailTab: 'detalhes',
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
    const alertsForm=document.getElementById('formAlertSettings');
    if(alertsForm && !document.getElementById('inputBackupReminderDays')){
      const group=document.createElement('div');group.className='form-group';
      const label=document.createElement('label');label.htmlFor='inputBackupReminderDays';label.textContent='Lembrar backup após (dias)';
      const input=document.createElement('input');input.id='inputBackupReminderDays';input.type='number';input.min='1';input.max='3650';input.required=true;input.value='7';
      group.append(label,input);alertsForm.querySelector('.form-grid')?.append(group);
    }
    this.bindGlobalEvents();
    this.bindNavEvents();
    this.bindFormEvents();
    this.bindFilterEvents();
    this.bindModalEvents();

    // Carregar preferências e estado inicial
    const settings = await App.Service.getSettings();
    this.applyTheme(settings.theme || 'dark');

    // Modo de visualização da lista (cards vs table)
    this._settings = settings;
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
    document.getElementById('labelDrawerUser').textContent = 'Usuário: ' + (settings.localUserName || 'Usuário local');
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
    this.initUIController();
    await this.refreshPresentationCache();
    if (App.Presentation) await App.Presentation.init();
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
    if (w < 1920) return 'conventional';
    if (w < 2560) return 'widescreen';
    return 'ultrawide';
  },

  applyResponsiveLayoutMode: async function(mode, persist = true) {
    const validModes = ['auto', 'compact', 'mobile', 'tablet', 'conventional', 'widescreen', 'ultrawide'];
    const cleanMode = validModes.includes(mode) ? mode : 'auto';
    this.responsiveLayoutMode = cleanMode;

    document.body.classList.toggle('density-compact', cleanMode === 'compact');
    document.body.dataset.layoutMode = this.getEffectiveViewportTier(cleanMode);
    document.body.classList.toggle('layout-narrow', window.innerWidth < 768);

    // Sincronizar todos os seletores de modo de exibição
    ['selectHeaderViewMode', 'selectDrawerViewMode', 'selectSettingsViewMode'].forEach(id => {
      const sel = document.getElementById(id);
      if (sel && sel.value !== cleanMode) sel.value = cleanMode;
    });

    this.checkViewModeUsabilityWarning();

    this.switchCadastrosCategory(this.currentCadastrosCategory || 'consoles');

    if (persist) {
      const settings = await App.Service.getSettings();
      settings.responsiveLayoutMode = cleanMode;
      await App.Service.saveSettings(settings);
      this._settings=settings;await this.refreshPresentationCache();this.notifyPresentation('settings');
    }

    await this.syncActiveListModality();
    this.notifyPresentation('layout');
  },

  checkViewModeUsabilityWarning: function() {
    const banner = document.getElementById('viewModeWarningBanner');
    const textEl = document.getElementById('bannerViewModeText') || document.getElementById('viewModeWarningText');
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

  handleViewportResize: async function() {
    document.body.dataset.layoutMode = this.getEffectiveViewportTier(this.responsiveLayoutMode);
    document.body.classList.toggle('layout-narrow', window.innerWidth < 768);
    this.checkViewModeUsabilityWarning();
    await this.syncActiveListModality();
    this.notifyPresentation('layout');
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
      this._settings=settings;await this.refreshPresentationCache();this.notifyPresentation('settings');
    this.applyTheme(nextTheme);
    const names = { dark: 'Controle Escuro', light: 'Profissional Claro', industrial: 'Industrial Alto Contraste' };
    this.showToast(`Tema visual alterado para: ${names[nextTheme]}`, 'info');
  },

  updateBackupPill: function(lastBackupAt) {
    const pill = document.getElementById('pillBackup');
    const labelDate = document.getElementById('labelLastBackupDate');
    const statusModalBackup = document.getElementById('statusModalLastBackup');
    const overdueBanner = document.getElementById('backupOverdueBanner');
    const overdueText = document.getElementById('bannerBackupOverdueText') || document.getElementById('backupOverdueText');

    if (lastBackupAt) {
      const dt = App.Utils.formatDateTime(lastBackupAt);
      const daysDiff = Math.floor((Date.now() - new Date(lastBackupAt).getTime()) / (1000 * 60 * 60 * 24));
      if (pill) {
        pill.className = daysDiff >= (this._settings?.backupReminderDays ?? 7) ? 'status-pill warn' : 'status-pill ok';
        pill.innerHTML = `<span class="indicator-dot">&bull;</span> Backup: ${App.Utils.formatDate(lastBackupAt)}`;
      }
      if (labelDate) labelDate.textContent = `Último backup: ${dt}`;
      if (statusModalBackup) statusModalBackup.textContent = `${dt} (${daysDiff === 0 ? 'Hoje' : 'há ' + daysDiff + ' dia(s)'})`;

      if (overdueBanner) {
        if (daysDiff >= (this._settings?.backupReminderDays ?? 7)) {
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
      this._settings=settings;await this.refreshPresentationCache();this.notifyPresentation('settings');

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
    this.notifyPresentation('console');
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
      drawer?.classList.add('open');
      overlay?.classList.add('open', 'active');
      btnOpen?.setAttribute('aria-expanded','true');
      this.openModal('appMobileDrawer');
    };

    const closeDrawer = () => {
      this.closeModal('appMobileDrawer');
    };

    if(drawer)drawer.inert=true;
    btnOpen?.setAttribute('aria-expanded','false');
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
    this.openModal('modalAppStatus');
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
    canvas.width=1200;canvas.height=440;
    canvas.style.width='100%';canvas.style.height='auto';canvas.style.aspectRatio='1200 / 440';
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
      if(this.stylusIsDrawing)return;
      this.stylusActivePointerId=e.pointerId;
      canvas.style.touchAction='none';e.preventDefault();
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
      if (!this.stylusIsDrawing || e.pointerId!==this.stylusActivePointerId) return;
      if (this.stylusActivePointerType === 'pen' && e.pointerType === 'touch') return;
      const pos = getPos(e);
      this.stylusCtx.lineTo(pos.x, pos.y);
      this.stylusCtx.stroke();
    });

    const stopDrawing = (e) => {
      if (this.stylusIsDrawing && e.pointerId===this.stylusActivePointerId) {
        this.stylusIsDrawing = false;
        this.stylusActivePointerType = null;
        this.stylusActivePointerId=null;canvas.style.touchAction='pan-y';
        try { canvas.releasePointerCapture(e.pointerId); } catch(err) {}
        this.stylusDrawingData = canvas.toDataURL('image/png');
      }
    };

    canvas.addEventListener('pointerup', stopDrawing);
    canvas.addEventListener('pointercancel', stopDrawing);
    canvas.style.touchAction='pan-y';
    canvas.addEventListener('touchstart',e=>{if(this.stylusIsDrawing)e.preventDefault();},{passive:false});
    canvas.addEventListener('touchmove',e=>{if(this.stylusIsDrawing)e.preventDefault();},{passive:false});

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
      if(isFull)this.openModal('boxStylusCanvas');else this.closeModal('boxStylusCanvas');
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
    if(this.modalStack.some(x=>x.element.id==='boxStylusCanvas'))this.closeModal('boxStylusCanvas',true);
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
    await this.refreshPresentationCache();this.notifyPresentation('catalog');
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

    // Botões dos Banners Persistentes (Alarme Ativo, Backup Vencido e Modo de Visualização)
    document.getElementById('btnBannerResetAuto')?.addEventListener('click', () => {
      this.applyResponsiveLayoutMode('auto', true);
      this.showToast('Modo de exibição restaurado para Automático.', 'info');
    });

    document.getElementById('btnBannerBackupNow')?.addEventListener('click', () => {
      App.Backup.exportJSON();
    });

    document.getElementById('btnBannerViewAlarms')?.addEventListener('click', () => {
      this.clearPendingFilters();this.metricFilter='unacknowledged';
      document.getElementById('checkFilterOnlyActiveConsole').checked=false;
      this.navigateTo('viewPendingEvents');
    });

    document.getElementById('btnBannerAckAll')?.addEventListener('click', async () => {
      const allEvents = await App.DB.getAll('events');
      const triggered = allEvents.filter(e => e.status === 'pendente' && e.active !== false && e.alarmState === 'triggered');
      for (const ev of triggered) {
        await App.Service.acknowledgeAlarm(ev.id);
      }
      this.showToast('Alarmes ativos reconhecidos com sucesso.', 'info');
      await this.renderDashboard();
      if (this.currentView === 'viewPendingEvents') await this.renderPendingEvents();
    });

    document.getElementById('btnDrawerCloseBottom')?.addEventListener('click', () => {
      this.closeModal('appMobileDrawer');
    });

    // Seletor de Tema Visual nas Configurações
    document.getElementById('selectSettingsTheme')?.addEventListener('change', async (e) => {
      const newTheme = e.target.value;
      const settings = await App.Service.getSettings();
      settings.theme = newTheme;
      await App.Service.saveSettings(settings);
      this._settings=settings;await this.refreshPresentationCache();this.notifyPresentation('settings');
      this.applyTheme(newTheme);
    });

    // Sino de Alarmes no Header Mobile/Tablet
    document.getElementById('btnHeaderAlarmBell')?.addEventListener('click', () => {
      this.clearPendingFilters();this.metricFilter='unacknowledged';
      document.getElementById('checkFilterOnlyActiveConsole').checked=false;
      this.navigateTo('viewPendingEvents');
    });

    // Mudar usuário local (Header e Gaveta)
    const promptUserChange = async () => {
      const settings = await App.Service.getSettings();
      const currentName = settings.localUserName || 'Usuário local';
      const newName = prompt('Informe o nome do controlador neste dispositivo:', currentName);
      if (newName !== null) {
        settings.localUserName = newName.trim() || 'Usuário local';
        await App.Service.saveSettings(settings);
      this._settings=settings;await this.refreshPresentationCache();this.notifyPresentation('settings');
        document.getElementById('headerUserName').textContent = settings.localUserName;
        const lblDrawerUser = document.getElementById('labelDrawerUser');
        if (lblDrawerUser) lblDrawerUser.textContent = `👤 Usuário: ${settings.localUserName}`;
        const inpUser = document.getElementById('inputSettingsUserName');
        if (inpUser) inpUser.value = settings.localUserName;
        this.showToast(`Identificação atualizada: ${settings.localUserName}`, 'info');
      }
    };
    document.getElementById('btnControllerBadge')?.addEventListener('click', promptUserChange);
    document.getElementById('btnDrawerUser')?.addEventListener('click', promptUserChange);

    // Alternar Tema (Cicla entre os 3 Temas: Escuro -> Claro -> Industrial Alto Contraste)
    document.getElementById('btnToggleTheme')?.addEventListener('click', () => {
      this.cycleTheme();
    });

    // Métrica cards clicáveis no dashboard
    document.querySelectorAll('.dashboard-metrics .metric-card').forEach(card => {
      card.addEventListener('click', () => {
        const filter = card.getAttribute('data-filter');
        if (filter === 'completed') {
          for(const id of ['inputSearchCompleted','filterCompletedConsole','filterCompletedPipeline','filterCompletedUO','filterCompletedTiming','filterCompletedDateFrom','filterCompletedDateTo'])document.getElementById(id).value='';
          this.completedTodayOnly = true;
          this.navigateTo('viewCompletedEvents');
        } else {
          this.clearPendingFilters();
          this.metricFilter = filter === 'all' ? null : filter;
          this.activePendingEvents=this.applyMetricFilter((this._snapshot?.events||[]).filter(e=>e.active!==false && e.status==='pendente'));
          document.getElementById('checkFilterOnlyActiveConsole').checked = false;
          this.navigateTo('viewPendingEvents');
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

    if (callback) await callback();
    this.notifyPresentation('navigation');
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
        await this.refreshPresentationCache();this.notifyPresentation('crud');

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
        settings.backupReminderDays=Number(document.getElementById('inputBackupReminderDays').value);
        settings.defaultLeadTimeMinutes = Number(document.getElementById('inputDefaultLeadTime').value);
        settings.soundType = document.getElementById('selectSoundType').value;
        settings.soundVolume = Number(document.getElementById('rangeSoundVolume').value);
        settings.soundEnabled = document.getElementById('checkSettingSound').checked;
        settings.visualAlertEnabled = document.getElementById('checkSettingVisualModal').checked;
        settings.highlightCardEnabled = document.getElementById('checkSettingHighlightCard').checked;
        settings.pulsingEnabled = document.getElementById('checkSettingPulsing').checked;
        settings.changeTitleEnabled = document.getElementById('checkSettingChangeTitle').checked;
        settings.notificationEnabled = document.getElementById('checkSettingNotification').checked;
        settings.repeatAlarm = document.getElementById('checkSettingRepeat').checked;
        settings.repeatIntervalMinutes = Number(document.getElementById('inputSettingRepeatInterval').value);
        settings.maxRepeats = Number(document.getElementById('inputSettingMaxRepeats').value);

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
      this._settings=settings;await this.refreshPresentationCache();this.notifyPresentation('settings');
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
        scheduledDate: this.localDate(),
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
        'Esta ação substituirá todos os dados locais por exemplos de demonstração. Um backup preventivo será exportado antes de apagar a base. Deseja continuar?',
        async () => {
          await App.Backup.exportJSON({preventive:true});
          await App.Service.clearAllData();
          await App.Service.loadDemoData();
          await this.reloadPreferences();
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
          await this.reloadPreferences();
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

    document.getElementById('inputEventAlarmLeadTime').value = event.alarmMinutesBefore ?? 15;
    document.getElementById('checkEventAlertSound').checked = event.alarmAudio !== false;
    document.getElementById('checkEventAlertVisual').checked = event.alarmVisual !== false;
    document.getElementById('checkEventAlertNotif').checked = !!event.alarmNotification;
    document.getElementById('checkEventAlertRepeat').checked = !!event.alarmRepeat;
    document.getElementById('inputEventAlertRepeatInterval').value = event.alarmRepeatInterval ?? 2;
    document.getElementById('inputEventAlertMaxRepeats').value = event.alarmMaxRepeats ?? 5;

    document.getElementById('boxCustomAlarmSettings').style.display = (!event.hasAlarm || event.useDefaultAlarmSettings) ? 'none' : 'grid';
    document.getElementById('wrapperUseDefaultAlarm').style.display = event.hasAlarm ? 'flex' : 'none';

    const safeDrawing = this.isSafeDrawing(event.stylusDrawing);
    const outerDrawing = document.getElementById('detailsModalDrawingBox');
    if (outerDrawing) outerDrawing.style.display = safeDrawing ? 'block' : 'none';
    if (safeDrawing) {
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

      document.getElementById('inputEventAlarmLeadTime').value = clone.alarmMinutesBefore ?? 15;
      document.getElementById('checkEventAlertSound').checked = clone.alarmAudio !== false;
      document.getElementById('checkEventAlertVisual').checked = clone.alarmVisual !== false;
      document.getElementById('checkEventAlertNotif').checked = !!clone.alarmNotification;
      document.getElementById('checkEventAlertRepeat').checked = !!clone.alarmRepeat;
      document.getElementById('inputEventAlertRepeatInterval').value = clone.alarmRepeatInterval ?? 2;
      document.getElementById('inputEventAlertMaxRepeats').value = clone.alarmMaxRepeats ?? 5;

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
      if(isVisible){this.closeModal('filterDrawer');return;}
      filterDrawer.style.display='grid';btnToggle.setAttribute('aria-expanded','true');
      if(window.innerWidth<768 || this.getEffectiveViewportTier()==='mobile'){filterDrawer.classList.add('active-sheet');this.openModal('filterDrawer');}
    });

    document.getElementById('btnCloseFilterSheet')?.addEventListener('click', () => {
      this.closeModal('filterDrawer');
      btnToggle?.classList.remove('btn-secondary');
    });

    document.getElementById('btnSheetApplyFilters')?.addEventListener('click', () => {
      this.closeModal('filterDrawer');
      btnToggle?.classList.remove('btn-secondary');
      this.renderPendingEvents();
    });

    document.getElementById('btnSheetClearFilters')?.addEventListener('click', () => {
      btnClear?.click();
      this.closeModal('filterDrawer');
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
      this.metricFilter = null;
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
      await this.renderPendingEvents();
      const settings = await App.Service.getSettings();
      settings.viewMode = 'cards';
      await App.Service.saveSettings(settings);
      this._settings=settings;await this.refreshPresentationCache();this.notifyPresentation('settings');
    });

    document.getElementById('btnViewTable')?.addEventListener('click', async () => {
      this.viewMode = 'table';
      this.updateViewModeUI();
      await this.renderPendingEvents();
      const settings = await App.Service.getSettings();
      settings.viewMode = 'table';
      await App.Service.saveSettings(settings);
      this._settings=settings;await this.refreshPresentationCache();this.notifyPresentation('settings');
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
    await this.refreshPresentationCache();
    try {
    const allEvents = this._snapshot.events;
    const colorRanges = this._ranges;
    const consoles = this._snapshot.consoles;
    const pipelines = this._snapshot.pipelines;
    const uos = this._snapshot.operationalUnits;
    const tags = this._snapshot.equipmentTags;

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
    const todayStr = this.localDate();
    const completedTodayCount = completed.filter(e => e.completedAt && this.localDate(e.completedAt) === todayStr).length;

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
    const mobileAlarmsText = document.getElementById('bannerActiveAlarmsText') || document.getElementById('mobileActiveAlarmsText');
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
    const badgeTabletAlarms = document.getElementById('tabletAlarmsCount') || document.getElementById('badgeTabletAlarmsCount');
    const activeAlarmEvents = pending.filter(e => e.alarmState === 'triggered');
    if (badgeTabletAlarms) badgeTabletAlarms.textContent = activeAlarmEvents.length;
    if (tabletAlarmsList) {
      if (activeAlarmEvents.length === 0) {
        tabletAlarmsList.innerHTML = `<div style="color: var(--text-muted); font-size: 0.82rem; text-align: center; padding: 1rem;">Nenhum alarme crítico disparado no momento.</div>`;
      } else {
        tabletAlarmsList.innerHTML = activeAlarmEvents.slice(0, 4).map(ev => {
          const cl = App.Service.classifyEvent(ev, colorRanges);
          const tInfo = this.formatCountdown(new Date(ev.scheduledAt).getTime());
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
    this.spotlightEventId = spotlightTarget?.id || null;

    const spDesc = document.getElementById('spotlightDescription');
    const spPath = document.getElementById('spotlightHierarchy');
    const spBadge = document.getElementById('spotlightBadgeState');
    const spTimeLeft = document.getElementById('spotlightTimeLeft');
    const spSched = document.getElementById('spotlightScheduledAt');
    const spActions = document.getElementById('spotlightActions');
    const spNotes = document.getElementById('spotlightNotes');

    if (spotlightTarget) {
      const classification = App.Service.classifyEvent(spotlightTarget, colorRanges);
      const timerInfo = this.formatCountdown(new Date(spotlightTarget.scheduledAt).getTime());

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

      spTimeLeft.dataset.timestamp = new Date(spotlightTarget.scheduledAt).getTime();
      spTimeLeft.textContent = timerInfo.text;
      spTimeLeft.style.setProperty('--event-color',classification.color);
      spTimeLeft.style.removeProperty('color');
      spSched.textContent = `Previsto: ${App.Utils.formatDateTime(spotlightTarget.scheduledDate, spotlightTarget.scheduledTime)}`;

      spActions.innerHTML = `
        ${spotlightTarget.alarmState === 'triggered' ? `<button class="btn btn-warning btn-sm" onclick="App.UI.acknowledgeAlarm('${spotlightTarget.id}')">Reconhecer Alarme</button><button class="btn btn-secondary btn-sm" onclick="App.UI.showSnoozeModal('${spotlightTarget.id}')">Adiar</button>` : ''}
        <button class="btn btn-success btn-sm" onclick="App.UI.showCompleteModal('${spotlightTarget.id}')">Concluir</button>
        <button class="btn btn-secondary btn-sm event-action-secondary" onclick="App.UI.editEvent('${spotlightTarget.id}')">Editar</button>
        <button class="btn btn-outline btn-sm event-action-secondary" onclick="App.UI.duplicateEvent('${spotlightTarget.id}')">+ Duplicar</button>
        <button class="btn btn-outline btn-sm event-action-secondary" onclick="App.UI.showDetailsModal('${spotlightTarget.id}')">Detalhes</button>
        <button class="btn btn-outline btn-sm" onclick="App.UI.openEventActionSheet('${spotlightTarget.id}')" title="Mais ações">&#x22EF; Mais</button>
      `;
    } else {
      spDesc.textContent = 'Nenhuma previsão operacional pendente no momento.';
      spNotes.textContent = '';
      spPath.textContent = 'Console • Duto • UO';
      spBadge.className = 'status-badge normal';
      spBadge.textContent = '● Sem Pendências';
      delete spTimeLeft.dataset.timestamp;
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
          const timerInfo = this.formatCountdown(new Date(ev.scheduledAt).getTime());
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
                <span class="event-countdown" style="--event-color: ${cl.color};" data-timestamp="${new Date(ev.scheduledAt).getTime()}">${timerInfo.text}</span>
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
      tbodyUrgent.innerHTML = urgentEvents.slice(0,50).map(ev => {
        const classification = App.Service.classifyEvent(ev, colorRanges);
        const timerInfo = this.formatCountdown(new Date(ev.scheduledAt).getTime());
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
    } finally { this.applyVisualPreferences(); this.notifyPresentation('dashboard'); }
  },

  // --------------------------------------------------------------------------
  // RENDERIZAÇÃO: EVENTOS PENDENTES (CARDS, TABELA E MASTER-DETAIL TABLET)
  // --------------------------------------------------------------------------
  renderPendingEvents: async function() {
    await this.refreshPresentationCache();
    try {
    const allEvents = this._snapshot.events;
    const colorRanges = this._ranges;
    const consoles = this._snapshot.consoles;
    const pipelines = this._snapshot.pipelines;
    const uos = this._snapshot.operationalUnits;
    const types = this._snapshot.equipmentTypes;
    const tags = this._snapshot.equipmentTags;

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
    const activeFiltersCount = [fConsole, fPipe, fUO, fStatus, fAlarm, fPriority, fDateFrom, fDateTo].filter(Boolean).length + (chkConsoleOnly ? 1 : 0) + (this.metricFilter ? 1 : 0);
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

    events = this.applyMetricFilter(events);
    this.activePendingEvents = events;
    const pageEvents = this.paginateEvents('pending', events);
    this.renderedListModalities.pending=this.getListModality('pending');
    this.updateViewModeUI();

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
    cardsContainer.innerHTML = (this.viewMode === 'cards' ? pageEvents : []).map(ev => {
      const cl = App.Service.classifyEvent(ev, colorRanges);
      const timerInfo = this.formatCountdown(new Date(ev.scheduledAt).getTime());
      const conName = consoleMap.get(ev.consoleId) || '';
      const pipeName = pipeMap.get(ev.pipelineId) || '';
      const uoName = uoMap.get(ev.uoId) || '';
      const tagName = tagMap.get(ev.tagId) || '';

      const isFiring = ev.alarmState === 'triggered';
      const isSnoozed = ev.alarmState === 'snoozed';
      const isAck = ev.alarmState === 'acknowledged';
      const isSelected = ev.id === this.selectedDetailEventId;

      return `
        <div tabindex="0" role="button" aria-label="${App.Utils.escapeHTML(ev.description)}" onkeydown="if(event.target===this && (event.key==='Enter'||event.key===' ')){event.preventDefault();App.UI.selectPendingDetailEvent('${ev.id}')}" class="event-card ${cl.blink || isFiring ? 'pulsing-card' : ''} ${isSelected ? 'selected-master-card' : ''}" data-event-id="${ev.id}" style="border-left-color: ${cl.color}; cursor: pointer;" onclick="if(!event.target.closest('button')) App.UI.selectPendingDetailEvent('${ev.id}')">
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
                  <button class="btn btn-outline btn-sm event-action-secondary" style="font-size: 0.72rem; padding: 0.2rem 0.5rem;" onclick="App.UI.showDetailsModal('${ev.id}')">
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
              <div class="event-countdown" style="--event-color: ${cl.color};" data-timestamp="${new Date(ev.scheduledAt).getTime()}">
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
              <button class="btn btn-secondary btn-sm event-action-secondary" onclick="App.UI.editEvent('${ev.id}')" title="Editar evento">Editar</button>
              <button class="btn btn-outline btn-sm event-action-secondary" onclick="App.UI.duplicateEvent('${ev.id}')" title="Duplicar evento para outro horário">+ Duplicar</button>
              <button class="btn btn-outline btn-sm event-action-secondary" onclick="App.UI.showDetailsModal('${ev.id}')" title="Ver detalhes e histórico">Detalhes</button>
              <button class="btn btn-outline btn-sm event-action-secondary" onclick="App.UI.deleteEvent('${ev.id}')" title="Excluir evento">&times;</button>
              <button class="btn btn-outline btn-sm btn-card-more-actions" onclick="App.UI.openEventActionSheet('${ev.id}')" title="Mais ações">&#x22EF;</button>
            </div>
          </div>
        </div>
      `;
    }).join('');

    // Renderizar Tabela Compacta
    tbodyTable.innerHTML = (this.viewMode === 'table' ? pageEvents : []).map(ev => {
      const cl = App.Service.classifyEvent(ev, colorRanges);
      const timerInfo = this.formatCountdown(new Date(ev.scheduledAt).getTime());
      const conName = consoleMap.get(ev.consoleId) || '';
      const pipeName = pipeMap.get(ev.pipelineId) || '';
      const uoName = uoMap.get(ev.uoId) || '';
      const tagName = tagMap.get(ev.tagId) || '-';

      return `
        <tr class="${cl.isOverdue ? 'row-overdue' : ''}" data-event-id="${ev.id}" tabindex="0" onclick="if(!event.target.closest('button')) App.UI.selectPendingDetailEvent('${ev.id}')" onkeydown="if(event.target===this && event.key==='Enter')App.UI.selectPendingDetailEvent('${ev.id}')">
          <td style="white-space: nowrap;"><strong>${App.Utils.formatDateTime(ev.scheduledDate, ev.scheduledTime)}</strong></td>
          <td style="white-space: nowrap;"><span class="event-countdown" style="--event-color: ${cl.color}; font-weight: 700;" data-timestamp="${new Date(ev.scheduledAt).getTime()}">${timerInfo.text}</span></td>
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
    } finally { this.applyVisualPreferences(); this.notifyPresentation('filters'); }
  },

  selectPendingDetailEvent: async function(eventId, tab = 'detalhes') {
    this.selectedDetailEventId = eventId;
    this.selectedDetailTab = tab;
    document.querySelectorAll('#containerPendingCards .event-card').forEach(card => {
      card.classList.toggle('selected-master-card', card.getAttribute('data-event-id') === eventId);
    });
    await this.renderPendingDetailPane(eventId, tab);
    this.notifyPresentation('selection', eventId);
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
    const timerInfo = this.formatCountdown(new Date(ev.scheduledAt).getTime());

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
            <div style="font-weight: 700;">${ev.priority} &bull; ${ev.hasAlarm ? ((ev.useDefaultAlarmSettings ? (await App.Service.getSettings()).defaultLeadTimeMinutes : ev.alarmMinutesBefore) + ' min antes') : 'Sem alarme'}</div>
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
      tabContentHtml = this.isSafeDrawing(ev.stylusDrawing) ? `
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

    const selectedIndex=this.activePendingEvents.findIndex(e=>e.id===ev.id);
    pane.innerHTML = `
      <nav class="detail-navigation" aria-label="Navegar nas previsões filtradas">
        <button type="button" class="btn btn-outline btn-sm" ${selectedIndex<=0?'disabled':''} onclick="App.UI.movePendingSelection(-1)">Anterior</button>
        <span>${selectedIndex+1} de ${this.activePendingEvents.length}</span>
        <button type="button" class="btn btn-outline btn-sm" ${selectedIndex<0 || selectedIndex>=this.activePendingEvents.length-1?'disabled':''} onclick="App.UI.movePendingSelection(1)">Próxima</button>
      </nav>
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 0.65rem; margin-bottom: 0.75rem;">
        <span class="status-badge ${cl.key}">${cl.icon || ''} ${cl.name}</span>
        <span class="event-countdown" style="--event-color: ${cl.color}; font-weight: 800; font-size: 1rem;" data-timestamp="${new Date(ev.scheduledAt).getTime()}">${timerInfo.text}</span>
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
    const request=this.beginModalRequest('modalEventActionSheet',eventId);
    if(!request)return;
    const ev = await App.DB.get('events', eventId);
    if (!ev) return;
    const snapshot=await App.DB.snapshot();
    if(!this.isModalRequestCurrent(request))return;

    const titleEl = document.getElementById('actionSheetEventTitle');
    const container = document.getElementById('actionSheetButtonsContainer');
    const modal = document.getElementById('modalEventActionSheet');
    if (!container || !modal) return;

    if (titleEl) titleEl.textContent = ev.description;
    const names = [['consoles', ev.consoleId], ['pipelines', ev.pipelineId], ['operationalUnits', ev.uoId]].map(([store,id]) => snapshot[store].find(x=>x.id===id)?.name || '');
    document.getElementById('actionSheetEventSubtitle').textContent = names.join(' / ') + ' • ' + App.Utils.formatDateTime(ev.scheduledAt);

    const closeSheet = "App.UI.closeModal('modalEventActionSheet');";
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
      <section class="action-sheet-destructive" aria-labelledby="actionSheetDestructiveTitle">
        <h4 id="actionSheetDestructiveTitle">Ação destrutiva</h4>
        <button class="btn btn-danger" style="width: 100%; justify-content: flex-start;" onclick="${closeSheet} App.UI.deleteEvent('${ev.id}')">&times; Excluir Previsão</button>
      </section>
    `;

    this.openModal(modal.id,ev,request);
  },

  updateLiveTimers: async function() {
    for(const element of document.querySelectorAll('.event-countdown[data-timestamp],#spotlightTimeLeft[data-timestamp],#alarmModalCountdown[data-timestamp]')){
      const timestamp=Number(element.dataset.timestamp);if(timestamp)element.textContent=this.formatCountdown(timestamp).text;
    }
    const signature=this.temporalSignature();
    if(this._snapshot && signature!==this._temporalSignature && !this._temporalRefresh){
      this._temporalSignature=signature;this._temporalRefresh=true;
      try{await this.renderDashboard();if(this.currentView==='viewPendingEvents')await this.renderPendingEvents();if(this.currentView==='viewCompletedEvents')await this.renderCompletedEvents();this.notifyPresentation('time');}
      finally{this._temporalRefresh=false;}
    }
  },

  populateFilterDropdowns: function(consoles, pipelines, uos) {
    const fill = (id, list) => {
      const sel = document.getElementById(id);
      if (!sel) return;
      const previous = sel.value, placeholder = sel.options[0]?.textContent || 'Todos';
      sel.replaceChildren(new Option(placeholder, ''), ...list.map(x => new Option(x.name + (x.active === false ? ' (Inativo)' : ''), x.id)));
      if (list.some(x => x.id === previous)) sel.value = previous;
    };
    for (const prefix of ['filter', 'filterCompleted']) {
      fill(prefix+'Console', consoles); fill(prefix+'Pipeline', pipelines); fill(prefix+'UO', uos);
    }
  },

  // --------------------------------------------------------------------------
  // RENDERIZAÇÃO: EVENTOS CONCLUÍDOS (9 COLUNAS + CARDS EXPANSÍVEIS MOBILE)
  // --------------------------------------------------------------------------
  renderCompletedEvents: async function() {
    await this.refreshPresentationCache();
    try {
    const allEvents = this._snapshot.events;
    const consoles = this._snapshot.consoles;
    const pipelines = this._snapshot.pipelines;
    const uos = this._snapshot.operationalUnits;
    const types = this._snapshot.equipmentTypes;
    const tags = this._snapshot.equipmentTags;

    const consoleMap = new Map(consoles.map(c => [c.id, c.name]));
    const pipeMap = new Map(pipelines.map(p => [p.id, p.name]));
    const uoMap = new Map(uos.map(u => [u.id, u.name]));
    const tagMap = new Map(tags.map(t => [t.id, t.tag]));

    let completed = allEvents.filter(e => e.status === 'concluido' && e.active !== false);

    this.populateFilterDropdowns(consoles, pipelines, uos);
    let scope=document.getElementById('btnClearCompletedScope');
    if(!scope){scope=document.createElement('button');scope.id='btnClearCompletedScope';scope.type='button';scope.className='btn btn-outline btn-sm';scope.textContent='Concluídos hoje • Remover filtro';scope.onclick=()=>{this.completedTodayOnly=false;this.renderCompletedEvents();};document.getElementById('inputSearchCompleted').parentElement.after(scope);}
    scope.hidden=!this.completedTodayOnly;
    if (this.completedTodayOnly) completed = completed.filter(e => e.completedAt && this.localDate(e.completedAt) === this.localDate());
    this.activeCompletedEvents = completed;
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

    this.activeCompletedEvents = completed;
    const pageCompleted = this.paginateEvents('completed', completed);
    if(!completed.some(e=>e.id===this.selectedCompletedEventId))this.selectedCompletedEventId=completed[0]?.id || null;
    const mobileCompleted = this.getListModality('completed')==='cards';
    this.renderedListModalities.completed=mobileCompleted?'cards':'table';
    const tbody = document.getElementById('tbodyCompletedEvents');
    const cardsContainer = document.getElementById('containerCompletedCards');
    const emptyMsg = document.getElementById('completedEmptyMessage');
    cardsContainer.style.display=mobileCompleted?'flex':'none';
    document.getElementById('tableCompletedWrapper').style.display=mobileCompleted?'none':'block';

    if (completed.length === 0) {
      if (tbody) tbody.innerHTML = '';
      if (cardsContainer) cardsContainer.innerHTML = '';
      if (emptyMsg) emptyMsg.style.display = 'block';
      return;
    }
    if (emptyMsg) emptyMsg.style.display = 'none';

    // Renderizar Cards Expansíveis para Mobile (Seção 12.6 / Fix #11)
    if (cardsContainer) {
      cardsContainer.innerHTML = (mobileCompleted ? pageCompleted : []).map(ev => {
        const expanded=this.expandedCompletedIds.has(ev.id);
        const conName = consoleMap.get(ev.consoleId) || '';
        const pipeName = pipeMap.get(ev.pipelineId) || '';
        const uoName = uoMap.get(ev.uoId) || '';
        const tagName = tagMap.get(ev.tagId) || '-';
        const schedStr = App.Utils.formatDateTime(ev.scheduledDate, ev.scheduledTime);
        const compStr = App.Utils.formatDateTime(ev.completedAt);
        const diffStr = App.Utils.formatDiffMinutes(ev.completedTimeDiffMinutes);
        const controllerName = typeof ev.completedBy === 'string' && ev.completedBy.trim() ? ev.completedBy : 'Não informado';
        const alarmSummary = ev.alarmTriggerCount ? `${ev.alarmTriggerCount} disparo(s)` : (ev.hasAlarm ? 'Ativo (0 disparos)' : 'Sem alarme');

        return `
          <div class="completed-event-card${expanded?' expanded':''}" data-event-id="${ev.id}" tabindex="0" role="button" aria-expanded="${expanded}" onclick="if(!event.target.closest('button')) App.UI.toggleCompletedCard(this)" onkeydown="if(event.target===this && (event.key==='Enter'||event.key===' ')){event.preventDefault();App.UI.toggleCompletedCard(this)}">
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
            <div class="completed-card-details" ${expanded?'':'hidden'} style="display:${expanded?'block':'none'};">
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
    tbody.innerHTML = (mobileCompleted ? [] : pageCompleted).map(ev => {
      const conName = consoleMap.get(ev.consoleId) || '';
      const pipeName = pipeMap.get(ev.pipelineId) || '';
      const uoName = uoMap.get(ev.uoId) || '';
      const tagName = tagMap.get(ev.tagId) || '-';

      const schedStr = App.Utils.formatDateTime(ev.scheduledDate, ev.scheduledTime);
      const compStr = App.Utils.formatDateTime(ev.completedAt);
      const diffStr = App.Utils.formatDiffMinutes(ev.completedTimeDiffMinutes);
      const controllerName = typeof ev.completedBy === 'string' && ev.completedBy.trim() ? ev.completedBy : 'Não informado';
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
    } finally { this.applyVisualPreferences(); this.notifyPresentation('completed'); }
  },

  // --------------------------------------------------------------------------
  // RENDERIZAÇÃO: HUB UNIFICADO DE CADASTROS (SEM ESPAÇO MORTO + DRILL-DOWN)
  // --------------------------------------------------------------------------
  renderCadastros: async function() {
    await this.refreshPresentationCache();
    try {
    await this.refreshAllMasterDataDropdowns();
    await this.renderConsolesTable();
    await this.renderPipelinesTable();
    await this.renderUOsTable();
    await this.renderEquipmentTypesTable();
    await this.renderEquipmentTagsTable();
    } finally { this.applyVisualPreferences(); this.notifyPresentation('catalog'); }
  },

  switchCadastrosCategory: function(category) {
    this.currentCadastrosCategory = category;
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
        await this.publishCatalogChange();
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
        await this.publishCatalogChange();
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
        await this.publishCatalogChange();
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
          await this.publishCatalogChange();
          this.showToast('UO atualizada com sucesso!', 'success');
        } else {
          // Criação (suporta lote por vírgula, ex: REFAP, TEDEP)
          const result = await App.Service.saveUOBatch(nameVal);
          await this.publishCatalogChange();
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
        await this.publishCatalogChange();
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
        await this.publishCatalogChange();
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
      await this.publishCatalogChange();
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
        await this.publishCatalogChange();
        this.showToast('Console excluído com sucesso.', 'info');
        await this.initHeaderConsole();
        await this.renderConsolesTable();
      } catch (err) {
        if (err.isDependencyError) {
          this.showDependencyModal('Console com Dependências', err.dependencies, async () => {
            await App.Service.toggleConsoleActive(id);
            await this.publishCatalogChange();
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
      await this.publishCatalogChange();
      await this.renderPipelinesTable();
    } catch (err) {
      this.showToast(err.message, 'danger');
    }
  },

  deletePipeline: async function(id) {
    this.showConfirmModal('Excluir Duto', 'Deseja realmente excluir este duto?', async () => {
      try {
        await App.Service.deletePipeline(id);
        await this.publishCatalogChange();
        this.showToast('Duto excluído com sucesso.', 'info');
        await this.renderPipelinesTable();
      } catch (err) {
        if (err.isDependencyError) {
          this.showDependencyModal('Duto com Dependências', err.dependencies, async () => {
            await App.Service.togglePipelineActive(id);
            await this.publishCatalogChange();
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
      await this.publishCatalogChange();
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
        await this.publishCatalogChange();
        this.showToast('UO excluída com sucesso.', 'info');
        await this.refreshAllMasterDataDropdowns();
        await this.renderUOsTable();
      } catch (err) {
        if (err.isDependencyError) {
          this.showDependencyModal('UO com Dependências', err.dependencies, async () => {
            await App.Service.toggleUOActive(id);
            await this.publishCatalogChange();
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
      await this.publishCatalogChange();
      await this.renderEquipmentTypesTable();
    } catch (err) {
      this.showToast(err.message, 'danger');
    }
  },

  deleteEquipmentType: async function(id) {
    this.showConfirmModal('Excluir Tipo', 'Deseja realmente excluir este tipo de equipamento?', async () => {
      try {
        await App.Service.deleteEquipmentType(id);
        await this.publishCatalogChange();
        this.showToast('Tipo de equipamento excluído com sucesso.', 'info');
        await this.renderEquipmentTypesTable();
      } catch (err) {
        if (err.isDependencyError) {
          this.showDependencyModal('Tipo com Dependências', err.dependencies, async () => {
            await App.Service.toggleEquipmentTypeActive(id);
            await this.publishCatalogChange();
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
      await this.publishCatalogChange();
      await this.renderEquipmentTagsTable();
    } catch (err) {
      this.showToast(err.message, 'danger');
    }
  },

  deleteEquipmentTag: async function(id) {
    this.showConfirmModal('Excluir TAG', 'Deseja realmente excluir este TAG?', async () => {
      try {
        await App.Service.deleteEquipmentTag(id);
        await this.publishCatalogChange();
        this.showToast('TAG excluído com sucesso.', 'info');
        await this.renderEquipmentTagsTable();
      } catch (err) {
        if (err.isDependencyError) {
          this.showDependencyModal('TAG com Dependências', err.dependencies, async () => {
            await App.Service.toggleEquipmentTagActive(id);
            await this.publishCatalogChange();
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
    await this.refreshPresentationCache();
    try {
    const settings = await App.Service.getSettings();
    document.getElementById('inputSettingsUserName').value = settings.localUserName || 'Usuário local';
    document.getElementById('inputDefaultLeadTime').value = settings.defaultLeadTimeMinutes ?? 15;
    document.getElementById('inputBackupReminderDays').value=settings.backupReminderDays ?? 7;
    document.getElementById('selectSoundType').value = settings.soundType || 'chime';
    document.getElementById('rangeSoundVolume').value = settings.soundVolume ?? 80;
    document.getElementById('labelVolumeValue').textContent = `${settings.soundVolume ?? 80}%`;

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
    document.getElementById('inputSettingRepeatInterval').value = settings.repeatIntervalMinutes ?? 2;
    document.getElementById('inputSettingMaxRepeats').value = settings.maxRepeats ?? 5;

    const notifState = App.Notifications.getPermissionState();
    const btnReq = document.getElementById('btnRequestNotifText');
    if (btnReq) {
      btnReq.textContent = notifState === 'concedida' ? 'Permissão Concedida' : (notifState === 'negada' ? 'Permissão Negada' : 'Solicitar Permissão');
    }
    } finally { this.applyVisualPreferences(); this.notifyPresentation('settings'); }
  },

  // --------------------------------------------------------------------------
  // RENDERIZAÇÃO: CONFIGURAÇÕES DE FAIXAS DE CORES
  // --------------------------------------------------------------------------
  renderConfigColors: async function() {
    await this.refreshPresentationCache();
    try {
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
    } finally { this.applyVisualPreferences(); this.notifyPresentation('ranges'); }
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
    await this.refreshPresentationCache();
    try {
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

    document.getElementById('diagAppVersion').textContent = App.Config.APP_VERSION;
    document.getElementById('diagDBStatus').textContent = App.DB.db ? 'Local (IndexedDB ativo)' : 'Indisponível';
    document.getElementById('diagAudioStatus').textContent = App.Audio.isUnlocked ? 'Pronto (Ativo)' : 'Aguardando Interação';
    document.getElementById('diagNotifStatus').textContent = App.Notifications.getPermissionState();

    const errorLogs = await App.DB.getAll('errorLogs');
    this._snapshot.errorLogs=errorLogs;
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
    } finally { this.applyVisualPreferences(); this.notifyPresentation('diagnostic'); }
  },

  getDiagnosticReport: async function() {
    const report = {
      app: 'Caderno de Previsões Operacionais em Dutos',
      version: App.Config.APP_VERSION,
      errors: await App.DB.getAll('errorLogs'),
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
    document.addEventListener('keydown',event=>{
      const top=this.modalStack.at(-1);if(!top)return;
      if(event.key==='Escape'){event.preventDefault();event.stopPropagation();this.closeModal(top.element.id);return;}
      if(event.key==='Tab'){
        const list=this.focusable(top.element),first=list[0],last=list.at(-1);
        if(!first){event.preventDefault();top.element.focus();}
        else if(event.shiftKey && (document.activeElement===first || !top.element.contains(document.activeElement))){event.preventDefault();last.focus();}
        else if(!event.shiftKey && (document.activeElement===last || !top.element.contains(document.activeElement))){event.preventDefault();first.focus();}
      }
    });
    document.querySelectorAll('.modal-overlay').forEach(overlay=>overlay.addEventListener('click',event=>{if(event.target===overlay && this.modalStack.at(-1)?.element===overlay)this.closeModal(overlay.id);}));
    for(const id of ['btnCloseAlarmModal','btnCloseSnoozeModal','btnCancelSnooze','btnCloseCompleteModal','btnCancelCompleteModal','btnCloseReopenModal','btnCancelReopenModal','btnCloseDetailsModal','btnCloseDetailsModalBtn','btnCloseConfirmModal','btnCancelConfirm','btnCloseDependencyModal','btnCloseDependencyModalBtn','btnCloseImportSummaryModal','btnCancelImportSummary','btnCloseActionSheet','btnCloseAppStatusModal','btnCloseAppStatusFooter']){
      document.getElementById(id)?.addEventListener('click',event=>{const modal=event.currentTarget.closest('.modal-overlay');if(modal)this.closeModal(modal.id);});
    }
    document.querySelectorAll('.btn-quick-snooze').forEach(button=>button.addEventListener('click',()=>document.getElementById('inputSnoozeMinutes').value=button.dataset.min));
    const bindCritical=(buttonId,modalId,callback)=>{
      const button=document.getElementById(buttonId);if(!button)return;
      button.addEventListener('click',async()=>{
        if(this.modalBusy.has(modalId))return;
        const selected=this.modalStack.find(x=>x.element.id===modalId)?.event;if(!selected)return;
        this.modalBusy.add(modalId);button.disabled=true;
        try{await callback(selected);this.closeModal(modalId,true);await this.renderDashboard();if(this.currentView==='viewPendingEvents')await this.renderPendingEvents();if(this.currentView==='viewCompletedEvents')await this.renderCompletedEvents();}
        catch(error){this.showToast(error.message,'danger');await App.DB.logError(error,'Interface: '+modalId);}
        finally{button.disabled=false;this.modalBusy.delete(modalId);}
      });
    };
    bindCritical('btnConfirmSnooze','modalSnooze',async selected=>{
      const mins=Number(document.getElementById('inputSnoozeMinutes').value);
      if(!Number.isInteger(mins)||mins<1||mins>1440)throw new Error('Informe um adiamento de 1 a 1440 minutos.');
      await App.Service.snoozeAlarm(selected.id,mins);this.closeModal('modalAlarmTrigger',true);this.showToast(`Alarme adiado por ${mins} minutos.`,'info');
    });
    bindCritical('btnAlarmAcknowledge','modalAlarmTrigger',async selected=>{await App.Service.acknowledgeAlarm(selected.id);this.showToast('Alarme reconhecido.','info');});
    bindCritical('btnConfirmCompleteModal','modalCompleteEvent',async selected=>{await App.Service.completeEvent(selected.id,document.getElementById('inputCompleteNotes').value);this.showToast('Previsão operacional concluída.','success');});
    bindCritical('btnConfirmReopenModal','modalReopenEvent',async selected=>{await App.Service.reopenEvent(selected.id,document.getElementById('inputReopenDate').value,document.getElementById('inputReopenTime').value);this.showToast('Previsão reaberta.','success');});
    document.getElementById('btnAlarmSnoozePrompt')?.addEventListener('click',()=>{const event=this.modalStack.find(x=>x.element.id==='modalAlarmTrigger')?.event;if(event)this.showSnoozeModal(event.id,event);});
    document.getElementById('btnAlarmCompleteDirect')?.addEventListener('click',()=>{const id=this.modalStack.find(x=>x.element.id==='modalAlarmTrigger')?.event?.id;this.closeModal('modalAlarmTrigger');if(id)this.showCompleteModal(id);});
    document.getElementById('btnAlarmOpenDetails')?.addEventListener('click',()=>{const id=this.modalStack.find(x=>x.element.id==='modalAlarmTrigger')?.event?.id;this.closeModal('modalAlarmTrigger');if(id)this.showDetailsModal(id);});
  },

  showAlarmModal: async function(event, isTest = false) {
    const request=this.beginModalRequest('modalAlarmTrigger',event.id);
    if(!request)return;
    event={...event};
    const consoles = await App.DB.getAll('consoles');
    const pipelines = await App.DB.getAll('pipelines');
    const uos = await App.DB.getAll('operationalUnits');
    const tags = await App.DB.getAll('equipmentTags');
    if(!this.isModalRequestCurrent(request))return;

    const con = consoles.find(c => c.id === event.consoleId);
    const pipe = pipelines.find(p => p.id === event.pipelineId);
    const uo = uos.find(u => u.id === event.uoId);
    const tag = tags.find(t => t.id === event.tagId);

    const path = `${con ? con.name : 'Console'} | ${pipe ? pipe.name : 'Duto'} | ${uo ? uo.name : 'UO'} ${tag ? '| ' + tag.tag : ''}`;

    document.getElementById('alarmModalHierarchy').textContent = path;
    document.getElementById('alarmModalDescription').textContent = event.description;
    document.getElementById('alarmModalNotes').textContent = event.notes ? `Observações: ${event.notes}` : '';
    document.getElementById('alarmModalScheduledTime').textContent = App.Utils.formatDateTime(event.scheduledDate, event.scheduledTime);

    const timerInfo = this.formatCountdown(new Date(event.scheduledAt).getTime());
    document.getElementById('alarmModalCountdown').textContent = isTest ? 'Alarme de Teste' : timerInfo.text;
    document.getElementById('alarmModalCountdown').dataset.timestamp = isTest ? '' : new Date(event.scheduledAt).getTime();
    this.alarmEventId = event.id;

    this.openModal('modalAlarmTrigger',event,request);
  },

  showSnoozeModal: async function(eventId, currentAlarm = null) {
    const request=this.beginModalRequest('modalSnooze',eventId);
    if(!request)return;
    const event=currentAlarm?.id===request.eventId ? {...currentAlarm} : await App.DB.get('events',request.eventId);
    if(!event || !this.isModalRequestCurrent(request))return;
    document.getElementById('inputSnoozeMinutes').value=5;
    this.openModal('modalSnooze',event,request);
  },

  showCompleteModal: async function(eventId) {
    const request=this.beginModalRequest('modalCompleteEvent',eventId);
    if(!request)return;
    const event = await App.DB.get('events', eventId);
    if (!event) return;

    const consoles = await App.DB.getAll('consoles');
    const pipelines = await App.DB.getAll('pipelines');
    const uos = await App.DB.getAll('operationalUnits');
    const tags = await App.DB.getAll('equipmentTags');
    if(!this.isModalRequestCurrent(request))return;

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

    this.openModal('modalCompleteEvent',event,request);
  },

  showReopenModal: async function(eventId) {
    const request=this.beginModalRequest('modalReopenEvent',eventId);
    if(!request)return;
    const event = await App.DB.get('events', eventId);
    if (!event || !this.isModalRequestCurrent(request)) return;

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

    this.openModal('modalReopenEvent',event,request);
  },

  showDetailsModal: async function(eventId) {
    const request=this.beginModalRequest('modalEventDetails',eventId);
    if(!request)return;
    const event = await App.DB.get('events', eventId);
    if (!event) return;

    const consoles = await App.DB.getAll('consoles');
    const pipelines = await App.DB.getAll('pipelines');
    const uos = await App.DB.getAll('operationalUnits');
    const types = await App.DB.getAll('equipmentTypes');
    const tags = await App.DB.getAll('equipmentTags');
    const allHistory = await App.DB.getAll('eventHistory');
    if(!this.isModalRequestCurrent(request))return;

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

    const safeDrawing = this.isSafeDrawing(event.stylusDrawing);
    const outerDrawing = document.getElementById('detailsModalDrawingBox');
    if (outerDrawing) outerDrawing.style.display = safeDrawing ? 'block' : 'none';
    if (safeDrawing) {
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
      document.getElementById('detailsModalDrawingImg')?.removeAttribute('src');
    }

    // Buscar histórico de auditoria
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

    this.openModal('modalEventDetails',event,request);
  },

  showConfirmModal: function(title, message, onConfirm) {
    if(this.modalBusy.has('modalConfirm'))return;
    document.getElementById('modalConfirmTitle').textContent=title;
    document.getElementById('modalConfirmMessage').textContent=message;
    this.setModalAction('modalConfirm','btnAcceptConfirm',onConfirm || (()=>{}));this.openModal('modalConfirm');
  },

  showDependencyModal: function(title, reasons, onInactivate) {
    if(this.modalBusy.has('modalDependency'))return;
    document.getElementById('modalDependencyTitle').textContent=title;
    document.getElementById('modalDependencyList').innerHTML=reasons.map(r=>`<li>${App.Utils.escapeHTML(r)}</li>`).join('');
    this.setModalAction('modalDependency','btnDependencyInactivate',onInactivate || (()=>{}));this.openModal('modalDependency');
  },

  showImportSummaryModal: function(parsedBackup) {
    if(this.modalBusy.has('modalImportSummary'))return;
    let validated;
    try{validated=App.Backup.validateBackupData(parsedBackup);}catch(error){this.showToast(error.message,'danger');return;}
    const box=document.getElementById('importSummaryCounts');box.replaceChildren();
    const heading=document.createElement('p');heading.textContent=`Esquema ${validated.schemaVersion} • Exportado em ${App.Utils.formatDateTime(validated.exportedAt)}`;box.append(heading);
    for(const [name,rows] of Object.entries(validated.data)){const line=document.createElement('div');line.textContent=`${name}: ${rows.length}`;box.append(line);}
    this.setModalAction('modalImportSummary','btnConfirmImportSummary',async()=>{
      const mode=document.querySelector('input[name="importMode"]:checked')?.value || 'merge';
      const result=await App.Backup.importJSON(validated,mode);this.importResult=result;
      const message=document.createElement('p');message.className='import-result';message.setAttribute('role','status');
      message.textContent=`${result.applied?'Importação aplicada':'Importação não aplicada'}: ${result.inserted} inserido(s), ${result.updated} atualizado(s), ${result.skipped} ignorado(s).`;
      box.append(message);
      for(const conflict of result.conflicts || []){const line=document.createElement('p');line.textContent=`${conflict.store} / ${conflict.id}: ${conflict.reason}`;box.append(line);}
      if(!result.applied){this.showToast('A importação não foi aplicada. Revise os conflitos.','warning');this.notifyPresentation('import');return false;}
      await this.reloadPreferences();await this.renderDashboard();
      if(this.currentView==='viewPendingEvents')await this.renderPendingEvents();
      if(this.currentView==='viewCompletedEvents')await this.renderCompletedEvents();
      this.showToast(message.textContent,'success');
    });
    this.openModal('modalImportSummary');
  },

  showToast: function(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.setAttribute('role',type==='danger'?'alert':'status');
    toast.innerHTML = `
      <div style="flex: 1;">${App.Utils.escapeHTML(message)}</div>
      <button aria-label="Fechar mensagem" style="background: none; border: none; color: inherit; cursor: pointer; font-size: 1.1rem; line-height: 1;">&times;</button>
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
    this.showConfirmModal('Excluir Previsão', 'Excluir esta previsão da lista ativa? O histórico de auditoria será preservado.', async () => {
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
"""

from parts_js_presentation import JS_PRESENTATION
JS_UI += JS_PRESENTATION

