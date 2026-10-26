# -*- coding: utf-8 -*-
JS_PRESENTATION = r"""
/* Read-only operational composition. No storage writes, timers or UI method replacement. */
App.Presentation = {
  dashboardSelection: null,
  init() {
    if(this.initialized)return;
    this.initialized=true;
    for(const version of document.querySelectorAll('[data-app-version]'))version.textContent='v'+App.Config.APP_VERSION;
    for(const button of document.querySelectorAll('.app-nav .nav-item'))button.title=button.querySelector('span:not(.badge-count)')?.textContent.trim()||'';
    window.addEventListener('app-ui-update',e=>this.refresh(e.detail?.reason));
    document.addEventListener('input',e=>this.editing(e));
    document.addEventListener('change',e=>this.editing(e));
    document.addEventListener('click',e=>this.click(e));
    this.editorObserver=new MutationObserver(()=>{
      if(['viewCadastros','viewConfigColors'].includes(App.UI.currentView))this.refresh('editor');
    });
    for(const form of document.querySelectorAll('.catalog-editor,#formColorRange'))this.editorObserver.observe(form,{attributes:true,attributeFilter:['style'],subtree:true,childList:true});
    this.refresh('init');
  },
  el(tag,text,attrs={}) {
    const n=document.createElement(tag);
    if(text!==undefined&&text!==null)n.textContent=String(text);
    for(const [key,value] of Object.entries(attrs))n.setAttribute(key,String(value));
    return n;
  },
  panel(id,title) {
    const n=document.getElementById(id);if(!n)return null;
    n.replaceChildren(this.el('h2',title));return n;
  },
  name(store,id,fallback='Não informado') {
    const item=(this.state.snapshot[store]||[]).find(x=>x.id===id);
    return item?.name||item?.tag||fallback;
  },
  path(event) {
    return [this.name('consoles',event.consoleId),this.name('pipelines',event.pipelineId),this.name('operationalUnits',event.uoId)].join(' / ');
  },
  value(id) {return document.getElementById(id)?.value||'';},
  checked(id) {return !!document.getElementById(id)?.checked;},
  selectedText(id) {const e=document.getElementById(id);return e?.value?e.selectedOptions?.[0]?.textContent.trim()||e.value:'Não selecionado';},
  pairs(parent,entries) {
    const dl=this.el('dl');
    for(const [label,value] of entries){dl.append(this.el('dt',label),this.el('dd',value));}
    parent.append(dl);
  },
  action(parent,label,action,id,kind='outline') {
    const b=this.el('button',label,{type:'button',class:'btn btn-'+kind,'data-presentation-action':action});
    if(id)b.dataset.eventId=id;parent.append(b);return b;
  },
  eventList(parent,events,action='details',limit=8) {
    if(!events.length){parent.append(this.el('p','Nenhuma previsão neste contexto.',{class:'form-help'}));return;}
    const list=this.el('ul');
    for(const e of events.slice(0,limit)){
      const li=this.el('li'),b=this.el('button',e.description,{type:'button',class:'context-event','data-presentation-action':action,'data-event-id':e.id});
      b.append(this.el('small',this.path(e)+' · '+App.Utils.formatDateTime(e.scheduledAt)));
      if(action==='dashboard-select')b.setAttribute('aria-pressed',String(e.id===this.dashboardSelection));
      li.append(b);list.append(li);
    }
    parent.append(list);
    if(events.length>limit)parent.append(this.el('p',`${events.length-limit} outras previsões neste contexto.`,{class:'form-help'}));
  },
  history(parent,event) {
    parent.append(this.el('h3','Histórico registrado'));
    const entries=(this.state.snapshot.eventHistory||[]).filter(h=>h.eventId===event.id).slice().sort((a,b)=>new Date(b.timestamp)-new Date(a.timestamp));
    if(!entries.length){parent.append(this.el('p','Sem movimentações registradas.',{class:'form-help'}));return;}
    const list=this.el('ul');
    for(const h of entries.slice(0,5)){
      const li=this.el('li');li.append(this.el('strong',h.action),this.el('p',h.description),this.el('small',App.Utils.formatDateTime(h.timestamp)+' · '+(h.localUser||'Usuário não informado')));list.append(li);
    }
    parent.append(list);
    if(entries.length>5)this.action(parent,'Abrir histórico completo','details',event.id);
  },
  detail(parent,event,completed=false) {
    if(!event){parent.append(this.el('p','Selecione um evento para consultar seu contexto.',{class:'form-help'}));return;}
    const classification=this.state.classifyEvent(event);
    parent.append(this.el('p',this.path(event),{class:'form-help'}),this.el('h3',event.description));
    this.pairs(parent,[['Situação',completed?'Concluído':classification.name],['Previsto',App.Utils.formatDateTime(event.scheduledAt)],['Prioridade',event.priority||'Normal'],['Equipamento / TAG',[this.name('equipmentTypes',event.equipmentTypeId,'Geral da UO'),this.name('equipmentTags',event.tagId,'Sem TAG')].join(' / ')]]);
    if(completed)this.pairs(parent,[['Concluído em',App.Utils.formatDateTime(event.completedAt)],['Controlador',typeof event.completedBy==='string'&&event.completedBy.trim()?event.completedBy.trim():'Não informado'],['Diferença do previsto',Number.isFinite(event.completedTimeDiffMinutes)?`${Math.round(event.completedTimeDiffMinutes)} min`:'Não informada'],['Observação de conclusão',event.completionNote||'Sem observações']]);
    else {
      const p=this.el('p',App.UI.formatCountdown(new Date(event.scheduledAt).getTime()).text,{class:'event-countdown','data-timestamp':new Date(event.scheduledAt).getTime()});parent.append(p);
      this.pairs(parent,[['Alarme',event.alarmState==='triggered'?'Disparado · aguardando reconhecimento':event.hasAlarm?'Ativado':'Desativado']]);
    }
    if(event.notes)parent.append(this.el('p',event.notes));
    const actions=this.el('div',null,{class:'context-actions'});
    if(event.alarmState==='triggered'&&!completed)this.action(actions,'Reconhecer','acknowledge',event.id,'warning');
    if(!completed)this.action(actions,'Concluir','complete',event.id,'success');
    this.action(actions,'Detalhes e histórico','details',event.id);parent.append(actions);
    this.history(parent,event);
  },
  refresh(reason) {
    const focused=document.activeElement,action=focused?.dataset?.presentationAction,eventId=focused?.dataset?.eventId;
    this.state=App.UI.getPresentationState();if(!this.state.snapshot)return;
    this.syncCompletedFilters();
    for(const b of document.querySelectorAll('.nav-item,.mobile-nav-link,.bottom-nav-item,.bottom-nav-fab')){
      if((b.dataset.view||b.dataset.target)===this.state.view)b.setAttribute('aria-current','page');else b.removeAttribute('aria-current');
    }
    const view=this.state.view;
    if(view==='viewDashboard')this.dashboard();
    else if(view==='viewNewEvent')this.draft();
    else if(view==='viewPendingEvents')this.pending();
    else if(view==='viewCompletedEvents')this.completed();
    else if(view==='viewCadastros')this.catalog();
    else if(view==='viewConfigAlerts')this.settings();
    else if(view==='viewConfigColors')this.range();
    else if(view==='viewBackup')this.backup();
    this.decorateRenderedControls();
    this.syncScrollableTables();
    if(action&&!focused.isConnected){const replacement=[...document.querySelectorAll('[data-presentation-action]')].find(n=>n.dataset.presentationAction===action&&n.dataset.eventId===eventId);replacement?.focus({preventScroll:true});}
  },
  dashboard() {
    document.getElementById('viewDashboardHeading').textContent='Painel operacional · todos os consoles';
    const s=this.state,events=s.snapshot.events.filter(e=>e.active!==false&&e.status==='pendente'&&(!s.activeConsoleId||e.consoleId===s.activeConsoleId)).slice().sort((a,b)=>new Date(a.scheduledAt)-new Date(b.scheduledAt));
    const panorama=this.panel('dashboardContextPanel','Panorama do console');panorama.dataset.total=events.length;
    panorama.append(this.el('p',`${events.length} previsões pendentes · ${this.name('consoles',s.activeConsoleId,'Todos os consoles')}`,{class:'form-help'}));
    const columns=this.el('div',null,{class:'context-columns'}),states=this.el('section'),pipes=this.el('section');
    states.append(this.el('h3','Por faixa de tempo'));pipes.append(this.el('h3','Por duto'));
    const counts=new Map(),pipelines=new Map();
    for(const event of events){const c=s.classifyEvent(event);counts.set(c.name,(counts.get(c.name)||0)+1);const name=this.name('pipelines',event.pipelineId);pipelines.set(name,(pipelines.get(name)||0)+1);}
    for(const [parent,map] of [[states,counts],[pipes,pipelines]]){
      if(!map.size)parent.append(this.el('p','Sem previsões pendentes.',{class:'form-help'}));
      for(const [name,count] of map){const row=this.el('div',null,{class:'context-count-row'});row.append(this.el('span',name),this.el('strong',count));const meter=this.el('meter',null,{min:0,max:Math.max(events.length,1),value:count,'aria-label':name+': '+count});row.append(meter);parent.append(row);}
    }
    columns.append(states,pipes);panorama.append(columns);
    const dashboardEvents=s.snapshot.events.filter(e=>e.active!==false&&e.status==='pendente').slice().sort((a,b)=>new Date(a.scheduledAt)-new Date(b.scheduledAt));
    if(!dashboardEvents.some(e=>e.id===this.dashboardSelection))this.dashboardSelection=dashboardEvents[0]?.id||null;
    const detail=this.panel('dashboardSelectedDetail','Evento em foco');this.detail(detail,dashboardEvents.find(e=>e.id===this.dashboardSelection));
    // Map the already-rendered urgent rows to the same official chronological sequence.
    const urgent=dashboardEvents.filter(e=>(new Date(e.scheduledAt)-Date.now())/60000<=30);
    const rows=document.querySelectorAll('#tbodyDashboardUrgent tr');
    rows.forEach((row,i)=>{const ev=urgent[i];if(!ev)return;row.dataset.presentationEvent=ev.id;row.tabIndex=0;row.setAttribute('aria-label','Selecionar '+ev.description);row.onkeydown=e=>{if(e.target===row&&(e.key==='Enter'||e.key===' ')){e.preventDefault();this.dashboardSelection=ev.id;this.dashboard();}};row.classList.toggle('selected-master-card',ev.id===this.dashboardSelection);});
    document.querySelectorAll('#dashboardUrgentCards>.event-card').forEach((row,i)=>{if(urgent[i])row.dataset.presentationEvent=urgent[i].id;});
  },
  draft() {
    const summary=this.panel('eventDraftSummary','Prévia não salva');
    summary.append(this.el('p','A edição abaixo só será gravada ao salvar.',{class:'form-help'}));
    summary.append(this.el('h3',this.value('inputEventDescription')||'Descreva a atividade operacional'));
    const date=this.value('inputEventDate').split('-').reverse().join('/');
    this.pairs(summary,[['Console',this.selectedText('headerActiveConsole')],['Duto / UO',this.selectedText('selectEventPipeline')+' / '+this.selectedText('selectEventUO')],['Programação',[date,this.value('inputEventTime')].filter(Boolean).join(' · ')||'Não definida'],['Prioridade',this.selectedText('selectEventPriority')],['Alarme',this.checked('checkEventAlarmActive')?(this.checked('checkEventUseDefaultAlarm')?`Padrão: ${this.state.settings.defaultLeadTimeMinutes} min antes`:`${this.value('inputEventAlarmLeadTime')} min antes`):'Desativado']]);
    if(this.value('inputEventNotes'))summary.append(this.el('p',this.value('inputEventNotes')));
    const related=this.panel('eventRelatedList','Previsões relacionadas'),pipe=this.value('selectEventPipeline'),uo=this.value('selectEventUO');
    if(!pipe){related.append(this.el('p','Selecione um duto para consultar as previsões existentes.',{class:'form-help'}));return;}
    const events=this.state.snapshot.events.filter(e=>e.active!==false&&e.status==='pendente'&&e.pipelineId===pipe&&(!uo||e.uoId===uo)&&e.id!==this.value('eventEditId')).slice().sort((a,b)=>new Date(a.scheduledAt)-new Date(b.scheduledAt));
    related.append(this.el('p',`${events.length} pendentes no duto${uo?' e UO selecionados':' selecionado'}.`,{class:'form-help'}));this.eventList(related,events);
  },
  pending() {
    const p=this.panel('pendingContextPanel','Contexto da seleção'),s=this.state,list=s.pending||[],event=list.find(e=>e.id===s.selectedEventId);
    this.pairs(p,[['Resultado filtrado',`${list.length} previsões`],['Aguardando reconhecimento',list.filter(e=>e.alarmState==='triggered').length],['Atrasadas',list.filter(e=>s.classifyEvent(e).isOverdue).length]]);
    if(!event){p.append(this.el('p','Selecione uma previsão para consultar os vínculos e o histórico.',{class:'form-help'}));return;}
    p.append(this.el('h3','Mesmo duto · fora ou dentro do filtro'));
    const related=s.snapshot.events.filter(e=>e.active!==false&&e.status==='pendente'&&e.pipelineId===event.pipelineId&&e.id!==event.id).slice().sort((a,b)=>new Date(a.scheduledAt)-new Date(b.scheduledAt));
    this.eventList(p,related,'details',5);this.history(p,event);
  },
  completed() {
    const s=this.state,list=s.completed||[],p=this.panel('completedContextPanel','Resumo dos concluídos');
    const dates=list.map(e=>e.completedAt).filter(Boolean).sort();
    this.pairs(p,[['Resultado filtrado',`${list.length} eventos`],['Primeira conclusão',dates.length?App.Utils.formatDateTime(dates[0]):'Nenhuma'],['Última conclusão',dates.length?App.Utils.formatDateTime(dates[dates.length-1]):'Nenhuma']]);
    p.append(this.el('h3','Selecionar conclusão'));this.eventList(p,list,'completed-select',8);
    const selected=list.find(e=>e.id===s.selectedEventId)||list[0];this.completedSelection=selected?.id||null;
    this.detail(this.panel('completedDetailPane','Conclusão selecionada'),selected,true);
    const scope=[];
    for(const id of ['filterCompletedConsole','filterCompletedPipeline','filterCompletedUO','filterCompletedTiming'])if(this.value(id))scope.push(this.selectedText(id));
    for(const [id,label] of [['filterCompletedDateFrom','Previsto desde'],['filterCompletedDateTo','Previsto até']])if(this.value(id))scope.push(label+' '+this.value(id).split('-').reverse().join('/'));
    if(this.value('inputSearchCompleted'))scope.push('Busca: '+this.value('inputSearchCompleted'));
    const today=document.getElementById('btnClearCompletedScope');if(today&&!today.hidden)scope.push('Concluídos hoje');
    document.getElementById('completedFiltersSummary').textContent=(scope.join(' · ')||'Todos os concluídos')+` · ${list.length} resultado(s)`;
  },
  syncCompletedFilters() {
    const details=document.getElementById('completedFilters'),mobile=this.state.tier==='mobile'||innerWidth<768;
    if(details&&mobile!==this.completedFiltersMobile){
      if(!details.contains(document.activeElement))details.open=!mobile;
      this.completedFiltersMobile=mobile;
    }
  },
  syncScrollableTables() {
    for(const wrapper of document.querySelectorAll('.view-section.active [data-scroll-table]')){
      const hint=wrapper.previousElementSibling;if(!hint?.classList.contains('table-scroll-hint'))continue;
      const overflow=wrapper.getClientRects().length&&wrapper.scrollWidth>wrapper.clientWidth+2;
      hint.hidden=!overflow;
    }
  },
  catalog() {
    const p=this.panel('cadastrosRelationsPanel','Vínculos do registro'),s=App.UI.getPresentationState();this.state=s;
    const configs={consoles:['consoles','consoleEditId','inputConsoleName'],pipelines:['pipelines','pipelineEditId','inputPipelineName'],uos:['operationalUnits','uoEditId','inputUOName'],types:['equipmentTypes','equipmentTypeEditId','inputEquipmentTypeName'],tags:['equipmentTags','tagEditId','inputTagCode']};
    const config=configs[s.category];
    if(!config){this.pairs(p,Object.values(configs).map(([store])=>[store,(s.snapshot[store]||[]).length]));return;}
    const [store,edit,input]=config,id=this.value(edit),item=(s.snapshot[store]||[]).find(x=>x.id===id);
    this.pairs(p,[['Categoria',document.querySelector('.cadastros-category-btn.active')?.querySelector('span')?.textContent.trim()||s.category],['Registros',(s.snapshot[store]||[]).length],['Edição atual',item?.name||item?.tag||this.value(input)||'Novo registro']]);
    if(!item){p.append(this.el('p','Selecione Editar na lista para consultar os vínculos existentes. Os dados do formulário só são gravados ao salvar.',{class:'form-help'}));return;}
    const field={consoles:'consoleId',pipelines:'pipelineId',uos:'uoId',types:'equipmentTypeId',tags:'tagId'}[s.category];
    const events=s.snapshot.events.filter(e=>e.active!==false&&e[field]===id);
    this.pairs(p,[['Previsões pendentes',events.filter(e=>e.status==='pendente').length],['Previsões concluídas',events.filter(e=>e.status==='concluido').length]]);
    const links=s.snapshot.pipelineOperationalUnits||[];
    const linkedNames=(targetStore,ids)=>(s.snapshot[targetStore]||[]).filter(record=>ids.has(record.id)).map(record=>record.name+(record.active===false?' (inativo)':'')).join(', ');
    if(store==='pipelines')this.pairs(p,[['Console responsável',this.name('consoles',item.consoleId)],['UOs vinculadas',linkedNames('operationalUnits',new Set(links.filter(link=>link.pipelineId===id).map(link=>link.uoId)))||'Nenhuma']]);
    else if(store==='consoles')this.pairs(p,[['Dutos vinculados',s.snapshot.pipelines.filter(x=>x.consoleId===id).map(x=>x.name).join(', ')||'Nenhum']]);
    else if(store==='operationalUnits')this.pairs(p,[['Dutos vinculados',linkedNames('pipelines',new Set(links.filter(link=>link.uoId===id).map(link=>link.pipelineId)))||'Nenhum']]);
    else this.pairs(p,[['UO',this.name('operationalUnits',item.uoId)]]);
    this.eventList(p,events,'details',5);
  },
  settings() {
    const p=this.panel('settingsPreviewPanel','Prévia das preferências');p.append(this.el('p','Valores em edição. Use Salvar Configurações para aplicar.',{class:'form-help'}));
    this.pairs(p,[['Antecedência',`${this.value('inputDefaultLeadTime')} min`],['Som',this.checked('checkSettingSound')?this.selectedText('selectSoundType')+' · '+this.value('rangeSoundVolume')+'%':'Desativado'],['Alerta visual',this.checked('checkSettingVisualModal')?'Ativado':'Desativado'],['Notificação',this.checked('checkSettingNotification')?'Solicitada nas preferências':'Desativada'],['Repetição',this.checked('checkSettingRepeat')?`${this.value('inputSettingRepeatInterval')} min · até ${this.value('inputSettingMaxRepeats')} repetições`:'Desativada'],['Tema',this.selectedText('selectSettingsTheme')],['Visualização',this.selectedText('selectSettingsViewMode')],['Lembrete de backup',`${this.value('inputBackupReminderDays')} dias`]]);
    p.append(this.el('h3','Estado atual do navegador'));this.pairs(p,[['Notificações',typeof Notification==='undefined'?'Indisponíveis':Notification.permission],['Áudio',document.getElementById('pillAudio')?.textContent.trim()||'Não inicializado']]);
  },
  range() {
    const p=this.panel('rangeLivePreview','Exemplo de aparência');p.append(this.el('p','Prévia da faixa em edição; não representa um evento da base.',{class:'form-help'}));
    const color=this.value('inputRangeColor');if(/^#[0-9a-f]{6}$/i.test(color))p.style.setProperty('--draft-range-color',color);
    this.pairs(p,[['Nome',this.value('inputRangeName')||'Nova faixa'],['Intervalo',`${this.value('inputRangeMin')||'—'} a ${this.value('inputRangeMax')||'—'} minutos`],['Cor de destaque',this.value('inputRangeColorText')],['Pulsação',this.checked('checkRangeBlink')?'Solicitada (respeita redução de movimento)':'Desativada'],['Som',this.checked('checkRangeSound')?'Ativado na faixa':'Desativado']]);
    p.append(this.el('h3','Faixas salvas'));for(const range of this.state.ranges||[])p.append(this.el('p',`${range.name}: ${range.minMinutes}–${range.maxMinutes} min`,{class:'form-help'}));
  },
  backup() {
    const p=this.panel('backupContextPanel','Estado da base local'),s=this.state.snapshot;
    p.append(this.el('p',document.getElementById('labelLastBackupDate')?.textContent||'Último backup não informado',{class:'form-help'}));
    this.pairs(p,[['Consoles',s.consoles.length],['Dutos',s.pipelines.length],['UOs',s.operationalUnits.length],['Previsões pendentes',s.events.filter(e=>e.active!==false&&e.status==='pendente').length],['Previsões concluídas',s.events.filter(e=>e.active!==false&&e.status==='concluido').length],['Movimentações históricas',(s.eventHistory||[]).length]]);
    p.append(this.el('p','O JSON inclui os registros e históricos. O navegador inicia o download; confira o arquivo na pasta de downloads.',{class:'form-help'}));
    p.append(this.el('h3','Armazenamento neste dispositivo'));
    p.append(this.el('p','Os dados ficam neste dispositivo, navegador e perfil. Outro navegador ou perfil não vê esta base. Limpar os dados do navegador pode apagá-la. Não há sincronização automática; use o backup para transportar e preservar os registros.',{class:'form-help'}));
    const file=document.getElementById('inputImportBackupFile')?.files?.[0];document.getElementById('backupSelectedFileName').textContent=file?file.name:'Nenhum arquivo selecionado.';p.append(this.el('h3','Importação'));p.append(this.el('p',file?`${file.name} · aguardando validação pelo botão Validar Arquivo.`:'Selecione um arquivo para validar. O resumo seguro é apresentado antes da confirmação.',{class:'form-help'}));
  },
  editing(event) {
    if(!this.state?.snapshot)return;
    if(event.target.closest('#formEvent'))this.draft();
    else if(event.target.closest('#formAlertSettings'))this.settings();
    else if(event.target.closest('#formColorRange'))this.range();
    else if(event.target.closest('#viewCadastros'))this.catalog();
    else if(event.target.id==='inputImportBackupFile')this.backup();
  },
  click(event) {
    const target=event.target.closest('[data-presentation-action]');
    if(target){
      const id=target.dataset.eventId,action=target.dataset.presentationAction;
      if(action==='dashboard-select'){this.dashboardSelection=id;this.dashboard();}
      else if(action==='completed-select'){App.UI.selectCompletedEvent(id);}
      else if(action==='details')App.UI.showDetailsModal(id);
      else if(action==='complete')App.UI.showCompleteModal(id);
      else if(action==='acknowledge')App.UI.acknowledgeAlarm(id);
      return;
    }
    const row=event.target.closest('[data-presentation-event]');if(row&&!event.target.closest('button')){this.dashboardSelection=row.dataset.presentationEvent;this.dashboard();}
    if(event.target.closest('#viewCadastros')){
      const group=event.target.closest('.catalog-category');
      const back=event.target.closest('[data-catalog-back]');
      if(back&&group){group.dataset.editorOpen='false';group.querySelector('[data-catalog-new]')?.focus();return;}
      const add=event.target.closest('[data-catalog-new]');
      if(add){const form=document.getElementById(add.dataset.catalogNew);const cancel=form.querySelector('[id^=btnCancel]');if(cancel)cancel.click();else form.reset();if(group)group.dataset.editorOpen='true';form.querySelector('input:not([type=hidden]),select')?.focus();}
      else if(group&&event.target.closest('button[onclick*=".edit"]'))group.dataset.editorOpen='true';
      // Catalog edits use asynchronous UI lookups. Observe form values after that task yields.
      queueMicrotask(()=>this.refresh('catalog-selection'));
    }
  },
  decorateRenderedControls() {
    // Normalize generated presentation only; preserve listeners and the UI's visibility contract.
    for(const b of document.querySelectorAll('.view-section.active button')){
      const text=b.textContent.trim();
      if(!b.hasAttribute('aria-label')&&['×','⋯','✕'].includes(text))b.setAttribute('aria-label',text==='⋯'?'Mais ações da previsão':'Excluir registro');
    }
    for(const svg of document.querySelectorAll('.view-section.active svg'))svg.setAttribute('aria-hidden','true');
    for(const element of document.querySelectorAll('.view-section.active [style]')){
      const font=element.style.fontSize;
      if(font && ((font.endsWith('rem')&&parseFloat(font)<.875)||(font.endsWith('px')&&parseFloat(font)<14)))element.style.fontSize='.875rem';
      if(element.style.color && !element.style.color.startsWith('var('))element.style.color='var(--text-main)';
      if(element.style.display==='flex'&&element.style.flexWrap!=='wrap')element.style.flexWrap='wrap';
    }
    for(const segment of document.querySelectorAll('.preview-segment')){
      const color=segment.style.backgroundColor;if(color && !color.startsWith('var(')){segment.style.borderTop='6px solid '+color;segment.style.backgroundColor='var(--bg-surface-active)';segment.style.color='var(--text-main)';}
    }
  }
};
"""
