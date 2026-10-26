# -*- coding: utf-8 -*-
JS_SERVICE = """
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
    const rawNames = namesString.split(/[,;\\n\\r]+/).map(s => s.trim()).filter(Boolean);
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
        body: `${pathStr}\\nHorário: ${App.Utils.formatDateTime(event.scheduledDate, event.scheduledTime)}`,
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
    const BOM = '\\uFEFF';
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
        : allEvents.filter(e => e.active !== false && (normType === 'pending' ? e.status === 'pendente' : e.status === 'concluido'));

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

    const csvContent = BOM + csvRows.join('\\r\\n');
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
"""


# Integrity rules shared by services, import preview and transactional merge.
JS_SERVICE += r"""
(() => {
  const stores=App.DB.DATA_STORES, S=App.Service, U=App.Utils;
  const fail=message=>{throw new Error(message);};
  const integer=(value,min,max,label)=>{
    if ((typeof value!=='number' && typeof value!=='string') || value==='' || !Number.isInteger(Number(value)) || Number(value)<min || Number(value)>max) fail(`${label}: número inteiro entre ${min} e ${max}.`);
    return Number(value);
  };
  const iso=value=>typeof value==='string' && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$/.test(value) && Number.isFinite(Date.parse(value)) && (()=>{try{U.localDateTime(value.slice(0,10),value.slice(11,16));return true;}catch(_){return false;}})();
  const text=(value,label)=>{if(typeof value!=='string'||!value.trim())fail(`${label} obrigatório.`);return value.trim();};
  const drawing=value=>{if(value!=null && value!=='' && (typeof value!=='string'||value.length>3000000||!/^data:image\/png;base64,iVBORw0KGgo[A-Za-z0-9+/]*={0,2}$/.test(value)))fail('Desenho deve ser uma imagem PNG segura.');};
  // These fields were written by the legacy v1 exporter. Actor/drawing additions,
  // range units and metadata on settings/colorRanges remain optional for old files.
  const catalogueFields=['id','name','active','createdAt','updatedAt','version','synchronizationStatus'];
  const requiredFields={
    consoles:catalogueFields,
    operationalUnits:catalogueFields,
    pipelines:[...catalogueFields,'consoleId'],
    pipelineOperationalUnits:['id','pipelineId','uoId','createdAt','version','synchronizationStatus'],
    equipmentTypes:[...catalogueFields,'uoId'],
    equipmentTags:['id','tag','uoId','equipmentTypeId','active','createdAt','updatedAt','version','synchronizationStatus'],
    events:['id','consoleId','pipelineId','uoId','equipmentTypeId','tagId','scheduledDate','scheduledTime','scheduledAt','description','notes','priority','status','hasAlarm','useDefaultAlarmSettings','alarmMinutesBefore','alarmAudio','alarmVisual','alarmNotification','alarmRepeat','alarmRepeatInterval','alarmMaxRepeats','alarmState','alarmSnoozedUntil','alarmTriggerCount','lastAlarmTriggeredAt','completedAt','completedTimeDiffMinutes','completionNote','active','createdAt','updatedAt','version','synchronizationStatus'],
    eventHistory:['id','eventId','action','timestamp','description','previousValue','newValue','localUser'],
    colorRanges:['id','name','color','minMinutes','maxMinutes','priority','blink','sound','active'],
    settings:['key','value']
  };
  const nullableFields={events:new Set(['equipmentTypeId','tagId','alarmSnoozedUntil','lastAlarmTriggeredAt','completedAt','completedTimeDiffMinutes']),eventHistory:new Set(['previousValue','newValue'])};
  const settingsValid=value=>{
    if(!value || typeof value!=='object'||Array.isArray(value))fail('Configurações inválidas.');
    for(const key of ['localUserName','soundEnabled','soundType','soundVolume','visualAlertEnabled','notificationEnabled','repeatAlarm','repeatIntervalMinutes','maxRepeats','defaultLeadTimeMinutes'])if(!Object.hasOwn(value,key)||value[key]==null)fail(`Configuração obrigatória ausente: ${key}.`);
    const enums={soundType:['chime','beep','siren','blip'],theme:['dark','light','industrial'],viewMode:['cards','table'],responsiveLayoutMode:['auto','compact','mobile','tablet','conventional','widescreen','ultrawide']};
    for(const [key,list] of Object.entries(enums))if(value[key]!==undefined&&!list.includes(value[key]))fail(`Configuração ${key} inválida.`);
    for(const [key,min,max] of [['soundVolume',0,100],['defaultLeadTimeMinutes',0,525600],['repeatIntervalMinutes',1,1440],['maxRepeats',0,1000],['backupReminderDays',1,3650]])if(value[key]!==undefined){if(typeof value[key]!=='number')fail(`Configuração ${key} deve ser numérica.`);integer(value[key],min,max,key);}
    for(const [key,def] of Object.entries(App.Config.DEFAULT_SETTINGS))if(typeof def==='boolean'&&value[key]!==undefined&&typeof value[key]!=='boolean')fail(`Configuração ${key} inválida.`);
    if(value.localUserName!==undefined)text(value.localUserName,'Nome do usuário');
    if(value.lastBackupAt!=null&&!iso(value.lastBackupAt))fail('Data de backup inválida.');
  };
  const rangesValid=rows=>{
    if(!rows.length)fail('Pelo menos uma faixa é obrigatória.');
    const ordered=[...rows].sort((a,b)=>a.minMinutes-b.minMinutes);let end=0;
    for(const r of ordered){text(r.name,'Faixa');if(!/^#[0-9a-f]{6}$/i.test(r.color))fail('Cor inválida.');integer(r.minMinutes,0,999999999,'Limite inicial');integer(r.maxMinutes,1,999999999,'Limite final');integer(r.priority,0,1000,'Prioridade');if(r.minMinutes!==end||r.maxMinutes<=r.minMinutes)fail('Faixas com lacuna, sobreposição ou limite inválido.');end=r.maxMinutes;}
    return ordered;
  };
  const uniqueKey=(store,row)=>{
    const key=U.cleanStr(row.name||row.tag);
    switch(store){case 'consoles':case 'operationalUnits':case 'colorRanges':return key;case 'pipelines':return row.consoleId+'|'+key;case 'equipmentTypes':return row.uoId+'|'+key;case 'equipmentTags':return U.cleanStr(row.tag);case 'pipelineOperationalUnits':return row.pipelineId+'|'+row.uoId;default:return null;}
  };
  const validateData=(data)=>{
    if(!data||typeof data!=='object'||Array.isArray(data)||Object.keys(data).some(key=>!stores.includes(key)))fail('Coleção desconhecida ou seção de dados inválida.');
    const maps={};
    for(const store of stores){
      if(!Array.isArray(data[store]))fail(`Coleção obrigatória ausente: ${store}.`);
      maps[store]=new Map();const business=new Set();
      for(const row of data[store]){
        if(!row||typeof row!=='object'||Array.isArray(row))fail(`Linha inválida em ${store}.`);
        for(const key of requiredFields[store])if(!Object.hasOwn(row,key)||row[key]===undefined||(row[key]===null&&!nullableFields[store]?.has(key)))fail(`Campo obrigatório ausente: ${store}.${key}.`);
        const id=store==='settings'?row.key:row.id;
        if(typeof id!=='string'||!/^[A-Za-z0-9_-]{1,128}$/.test(id)||['__proto__','constructor','prototype'].includes(id))fail(`ID inválido em ${store}.`);
        if(maps[store].has(id))fail(`ID duplicado em ${store}: ${id}.`);maps[store].set(id,row);
        const businessKey=uniqueKey(store,row);if(businessKey!==null){if(!businessKey||business.has(businessKey))fail(`Duplicidade cadastral em ${store}.`);business.add(businessKey);}
        if(row.version!==undefined){if(typeof row.version!=='number')fail('Versão deve ser numérica.');integer(row.version,1,Number.MAX_SAFE_INTEGER,'Versão');}
        for(const key of ['createdAt','updatedAt','timestamp','completedAt','lastAlarmTriggeredAt'])if(row[key]!=null&&!iso(row[key]))fail(`Data ${key} inválida em ${store}.`);
        for(const [key,value] of Object.entries(row)){
          if((['alarmMinutesBefore','alarmRepeatInterval','alarmMaxRepeats','alarmTriggerCount','minMinutes','maxMinutes'].includes(key)||(store==='colorRanges'&&key==='priority'))&&typeof value!=='number')fail(`Número ${key} inválido.`);
          if(['notes','completionNote','createdBy','completedBy','localUser','description','previousValue','newValue','synchronizationStatus'].includes(key)&&value!=null&&typeof value!=='string')fail(`Texto ${key} inválido.`);
          if(['active','hasAlarm','useDefaultAlarmSettings','alarmAudio','alarmVisual','alarmNotification','alarmRepeat','blink','sound'].includes(key)&&typeof value!=='boolean')fail(`Booleano ${key} inválido.`);
          if(/^(?:url|link|href|externalUrl)$/i.test(key)&&value!=null&&value!==''&&(typeof value!=='string'||!/^https?:\/\//i.test(value)))fail('Link inválido.');
        }
        drawing(row.stylusDrawing);
      }
    }
    const ref=(store,id)=>{if(!maps[store].has(id))fail(`Referência ausente em ${store}: ${id}.`);return maps[store].get(id);};
    for(const row of data.consoles)text(row.name,'Console');
    for(const row of data.operationalUnits)text(row.name,'UO');
    for(const row of data.pipelineOperationalUnits){ref('pipelines',row.pipelineId);ref('operationalUnits',row.uoId);}
    for(const row of data.pipelines){text(row.name,'Duto');ref('consoles',row.consoleId);if(new Set(data.pipelineOperationalUnits.filter(l=>l.pipelineId===row.id).map(l=>l.uoId)).size<2)fail('Duto exige duas UOs distintas.');}
    for(const row of data.equipmentTypes){text(row.name,'Tipo');ref('operationalUnits',row.uoId);}
    for(const row of data.equipmentTags){text(row.tag,'TAG');ref('operationalUnits',row.uoId);if(ref('equipmentTypes',row.equipmentTypeId).uoId!==row.uoId)fail('Tipo e TAG possuem UOs incompatíveis.');}
    for(const row of data.events){
      text(row.description,'Descrição');ref('consoles',row.consoleId);const p=ref('pipelines',row.pipelineId);ref('operationalUnits',row.uoId);
      if(p.consoleId!==row.consoleId||!data.pipelineOperationalUnits.some(l=>l.pipelineId===row.pipelineId&&l.uoId===row.uoId))fail('Console, duto e UO incompatíveis.');
      if(row.equipmentTypeId&&ref('equipmentTypes',row.equipmentTypeId).uoId!==row.uoId)fail('Tipo incompatível com UO.');
      if(row.tagId){const t=ref('equipmentTags',row.tagId);if(t.uoId!==row.uoId||t.equipmentTypeId!==row.equipmentTypeId)fail('TAG incompatível com tipo ou UO.');}
      const date=U.localDateTime(row.scheduledDate,row.scheduledTime);
      if(!iso(row.scheduledAt)||Date.parse(row.scheduledAt)!==date.getTime())fail('Horário previsto inconsistente.');
      if(!['pendente','concluido'].includes(row.status)||!['idle','triggered','snoozed','acknowledged'].includes(row.alarmState))fail('Situação do evento inválida.');
      if(row.priority!==undefined&&!['Baixa','Normal','Alta','Crítica','Urgente'].includes(row.priority))fail('Prioridade inválida.');
      for(const [key,min,max] of [['alarmMinutesBefore',0,525600],['alarmRepeatInterval',1,1440],['alarmMaxRepeats',0,1000],['alarmTriggerCount',0,Number.MAX_SAFE_INTEGER]])if(row[key]!==undefined)integer(row[key],min,max,key);
      if(row.alarmSnoozedUntil!=null&&(!Number.isFinite(row.alarmSnoozedUntil)||row.alarmSnoozedUntil<0))fail('Adiamento inválido.');
      if(row.completedTimeDiffMinutes!=null&&!Number.isFinite(row.completedTimeDiffMinutes))fail('Diferença de conclusão inválida.');
      if(row.status==='concluido'&&!iso(row.completedAt))fail('Conclusão sem data válida.');
    }
    for(const h of data.eventHistory){ref('events',h.eventId);text(h.action,'Ação do histórico');if(!iso(h.timestamp))fail('Data de histórico inválida.');}
    rangesValid(data.colorRanges);
    for(const row of data.settings){if(row.key!=='app_settings')fail('Chave de configuração desconhecida.');settingsValid(row.value);if(row.value.activeConsoleId!=null)ref('consoles',row.value.activeConsoleId);}
    if(data.settings.length!==1)fail('Configuração principal obrigatória.');
    return data;
  };
  App.Validation={validateData,settings:settingsValid,ranges:rangesValid,integer,isISO:iso};
  const stamp=(current,values)=>({...current,...values,updatedAt:new Date().toISOString(),version:(current?.version??0)+1,...(!current?{id:U.uuid(),active:true,createdAt:new Date().toISOString(),synchronizationStatus:'local-only'}:{})});
  const config=d=>({...App.Config.DEFAULT_SETTINGS,...d.settings.find(x=>x.key==='app_settings')?.value});
  const actor=d=>config(d).localUserName;
  const history=(d,e,action,description,previous=null)=>d.eventHistory.push({id:U.uuid(),eventId:e.id,action,description,timestamp:new Date().toISOString(),previousValue:previous,newValue:JSON.stringify(e),localUser:actor(d)});
  const change=callback=>App.DB.atomic(stores,d=>{const result=callback(d);validateData(d);return result;});
  const get=(d,store,id)=>d[store].find(x=>x.id===id)||fail('Registro não encontrado.');
  const activeRef=(d,store,id,oldId)=>{const r=get(d,store,id);if(r.active===false&&id!==oldId)fail('Não é permitido selecionar cadastro inativo.');return r;};
  S.getSettings=async()=>({...App.Config.DEFAULT_SETTINGS,...(await App.DB.get('settings','app_settings'))?.value});
  S.saveSettings=async value=>change(d=>{settingsValid(value);const old=d.settings[0];d.settings=[{...old,key:'app_settings',value:{...App.Config.DEFAULT_SETTINGS,...value},updatedAt:new Date().toISOString(),version:(old?.version??0)+1}];return d.settings[0].value;});
  const masterSave=(store,data)=>change(d=>{
    const old=data.id?get(d,store,data.id):null;const values={};
    for(const key of (store==='equipmentTags'?['tag']:['name']))values[key]=text(data[key],key);
    if(store==='pipelines'){values.consoleId=data.consoleId;activeRef(d,'consoles',data.consoleId,old?.consoleId);const ids=data.uoIds;if(!Array.isArray(ids)||new Set(ids).size!==ids.length||ids.length<2)fail('Duto exige duas UOs distintas.');for(const id of ids)activeRef(d,'operationalUnits',id,d.pipelineOperationalUnits.some(l=>l.pipelineId===old?.id&&l.uoId===id)?id:null);}
    if(['equipmentTypes','equipmentTags'].includes(store)){values.uoId=data.uoId;activeRef(d,'operationalUnits',data.uoId,old?.uoId);}
    if(store==='equipmentTags'){values.equipmentTypeId=data.equipmentTypeId;activeRef(d,'equipmentTypes',data.equipmentTypeId,old?.equipmentTypeId);}
    const row=stamp(old,values);d[store]=d[store].filter(x=>x.id!==row.id).concat(row);
    if(store==='pipelines'){const prior=d.pipelineOperationalUnits.filter(l=>l.pipelineId===row.id);d.pipelineOperationalUnits=d.pipelineOperationalUnits.filter(l=>l.pipelineId!==row.id);for(const id of data.uoIds)d.pipelineOperationalUnits.push(prior.find(l=>l.uoId===id)||{id:U.uuid(),pipelineId:row.id,uoId:id,createdAt:new Date().toISOString(),version:1,synchronizationStatus:'local-only'});}
    return row;
  });
  for(const [name,store] of [['Console','consoles'],['Pipeline','pipelines'],['UO','operationalUnits'],['EquipmentType','equipmentTypes'],['EquipmentTag','equipmentTags']]){
    S['save'+name]=data=>masterSave(store,data);
    S['toggle'+name+'Active']=id=>change(d=>{const row=get(d,store,id);Object.assign(row,stamp(row,{active:!row.active}));return row;});
    S['delete'+name]=id=>change(d=>{get(d,store,id);d[store]=d[store].filter(x=>x.id!==id);if(store==='pipelines')d.pipelineOperationalUnits=d.pipelineOperationalUnits.filter(l=>l.pipelineId!==id);try{validateData(d);}catch(err){err.isDependencyError=true;err.dependencies=['Referências vinculadas preservadas'];err.targetStore=store;err.targetId=id;throw err;}return true;});
  }
  S.saveUOBatch=names=>change(d=>{const created=[],existing=[];for(const name of [...new Set(text(names,'UOs').split(/[,;\n\r]+/).map(x=>x.trim()).filter(Boolean))]){let row=d.operationalUnits.find(u=>U.cleanStr(u.name)===U.cleanStr(name));if(row){if(!row.active)Object.assign(row,stamp(row,{active:true}));existing.push(row);}else{row=stamp(null,{name});d.operationalUnits.push(row);created.push(row);}}return{created,existing,all:[...created,...existing]};});
  S.saveEvent=data=>change(d=>{
    const old=data.id?get(d,'events',data.id):null;
    for(const [field,store] of [['consoleId','consoles'],['pipelineId','pipelines'],['uoId','operationalUnits'],['equipmentTypeId','equipmentTypes'],['tagId','equipmentTags']])if(data[field])activeRef(d,store,data[field],old?.[field]);
    const date=U.localDateTime(data.scheduledDate,data.scheduledTime), scheduledAt=date.toISOString();
    for(const field of ['hasAlarm','useDefaultAlarmSettings','alarmAudio','alarmVisual','alarmNotification','alarmRepeat'])if(data[field]!==undefined&&typeof data[field]!=='boolean')fail(`Booleano ${field} inválido.`);
    const row=stamp(old,{consoleId:data.consoleId,pipelineId:data.pipelineId,uoId:data.uoId,equipmentTypeId:data.equipmentTypeId||null,tagId:data.tagId||null,scheduledDate:data.scheduledDate,scheduledTime:data.scheduledTime,scheduledAt,description:text(data.description,'Descrição'),notes:data.notes??'',priority:data.priority??'Normal',stylusDrawing:data.stylusDrawing===undefined?old?.stylusDrawing??null:data.stylusDrawing,hasAlarm:data.hasAlarm??false,useDefaultAlarmSettings:data.useDefaultAlarmSettings??false,alarmMinutesBefore:integer(data.alarmMinutesBefore??0,0,525600,'Antecedência'),alarmAudio:data.alarmAudio??true,alarmVisual:data.alarmVisual??true,alarmNotification:data.alarmNotification??false,alarmRepeat:data.alarmRepeat??false,alarmRepeatInterval:integer(data.alarmRepeatInterval??2,1,1440,'Intervalo'),alarmMaxRepeats:integer(data.alarmMaxRepeats??5,0,1000,'Repetições')});
    if(!old)Object.assign(row,{status:'pendente',alarmState:'idle',alarmSnoozedUntil:null,alarmTriggerCount:0,lastAlarmTriggeredAt:null,completedAt:null,completedTimeDiffMinutes:null,completionNote:'',createdBy:actor(d)});
    if(old&&(old.scheduledAt!==scheduledAt||old.hasAlarm!==row.hasAlarm))Object.assign(row,{alarmState:'idle',alarmSnoozedUntil:null,alarmTriggerCount:0,lastAlarmTriggeredAt:null});
    d.events=d.events.filter(x=>x.id!==row.id).concat(row);history(d,row,old?'edicao':'criacao',old?'Evento atualizado':'Previsão criada',old?JSON.stringify(old):null);return row;
  });
  const transition=(id,action,fn)=>change(d=>{const row=get(d,'events',id);if(row.active===false)fail('Evento excluído.');const previous=JSON.stringify(row);fn(row,d);Object.assign(row,stamp(row,{}));history(d,row,action,action,previous);return row;});
  S.completeEvent=(id,note='')=>transition(id,'conclusao',(e,d)=>{if(e.status!=='pendente')fail('Evento já concluído.');Object.assign(e,{status:'concluido',completedAt:new Date().toISOString(),completedBy:actor(d),completedTimeDiffMinutes:(Date.now()-Date.parse(e.scheduledAt))/60000,completionNote:String(note).trim(),alarmState:'acknowledged',alarmSnoozedUntil:null});});
  S.reopenEvent=(id,date,time)=>transition(id,'reabertura',e=>{if((date&&!time)||(!date&&time))fail('Informe data e hora.');if(date){e.scheduledAt=U.localDateTime(date,time).toISOString();e.scheduledDate=date;e.scheduledTime=time;}Object.assign(e,{status:'pendente',completedAt:null,completedBy:null,completedTimeDiffMinutes:null,completionNote:'',alarmState:'idle',alarmSnoozedUntil:null,alarmTriggerCount:0,lastAlarmTriggeredAt:null});});
  S.snoozeAlarm=(id,minutes)=>{const count=integer(minutes,1,1440,'Adiamento');return transition(id,'adiamento',e=>{if(e.status!=='pendente'||!e.hasAlarm)fail('Alarme indisponível.');e.alarmState='snoozed';e.alarmSnoozedUntil=Date.now()+count*60000;});};
  S.acknowledgeAlarm=id=>transition(id,'reconhecimento',e=>{if(e.status!=='pendente')fail('Evento concluído.');e.alarmState='acknowledged';e.alarmSnoozedUntil=null;});
  S.deleteEvent=async id=>{await transition(id,'exclusao',e=>{e.active=false;e.alarmState='acknowledged';e.alarmSnoozedUntil=null;});return true;};
  S.validateColorRanges=rangesValid;
  S.saveColorRange=data=>change(d=>{const old=data.id?get(d,'colorRanges',data.id):null;const row=stamp(old,{name:text(data.name,'Faixa'),color:data.color,minMinutes:integer(data.minMinutes,0,999999999,'Início'),maxMinutes:integer(data.maxMinutes,1,999999999,'Fim'),priority:integer(data.priority??1,0,1000,'Prioridade'),blink:!!data.blink,sound:!!data.sound,active:true});d.colorRanges=d.colorRanges.filter(r=>r.id!==row.id).concat(row);return true;});
  S.deleteColorRange=id=>change(d=>{get(d,'colorRanges',id);d.colorRanges=d.colorRanges.filter(r=>r.id!==id);return true;});
  S.resetColorRanges=()=>change(d=>{d.colorRanges=structuredClone(App.Config.DEFAULT_COLOR_RANGES);return true;});
  // Explicit full reset includes history, errors, settings and catalogues together.
  S.clearAllData=()=>App.DB.atomic([...stores,'errorLogs'],d=>{for(const s of [...stores,'errorLogs'])d[s]=[];d.consoles=App.Config.INITIAL_CONSOLES.map(name=>stamp(null,{name}));d.colorRanges=structuredClone(App.Config.DEFAULT_COLOR_RANGES);d.settings=[{key:'app_settings',value:{...App.Config.DEFAULT_SETTINGS,activeConsoleId:d.consoles.find(c=>c.name==='C04').id}}];return true;});
  // Preserve the six original demonstration scenarios. Mixing with operational
  // catalogues is refused; UI can explicitly back up/reset before loading them.
  S.loadDemoData=()=>change(d=>{
    if(d.events.length||d.pipelines.length||d.operationalUnits.length)fail('Demonstração requer base operacional vazia. Exporte um backup antes de limpar os dados.');
    const consoles={};
    for(const name of ['C04','C08','C10']){let c=d.consoles.find(c=>U.cleanStr(c.name)===U.cleanStr(name));if(c?.active===false)fail('Console demonstrativo inativo.');if(!c){c=stamp(null,{name});d.consoles.push(c);}consoles[name]=c;}
    const units={};for(const name of ['REFAP','TEDEP','REPLAN','TEBAR']){const row=stamp(null,{name});units[name]=row;d.operationalUnits.push(row);}
    const pipelines={};for(const [name,consoleName,unitNames] of [['OSCAN','C04',['REFAP','TEDEP']],['OSBRA','C08',['REPLAN','TEBAR']],['DTCS','C10',['REPLAN','TEDEP']]]){const row=stamp(null,{name,consoleId:consoles[consoleName].id});pipelines[name]=row;d.pipelines.push(row);for(const unitName of unitNames)d.pipelineOperationalUnits.push({id:U.uuid(),pipelineId:row.id,uoId:units[unitName].id,version:1,createdAt:new Date().toISOString(),synchronizationStatus:'local-only'});}
    const equipment={};for(const [name,unitName,tag] of [['Tanque','REFAP','TQ-804'],['Bomba','REFAP','BB-101A'],['Esfera','REPLAN','ES-201'],['Válvula de Controle','TEDEP','PCV-301']]){const type=stamp(null,{name,uoId:units[unitName].id}),row=stamp(null,{tag,uoId:units[unitName].id,equipmentTypeId:type.id});d.equipmentTypes.push(type);d.equipmentTags.push(row);equipment[tag]=row;}
    const examples=[
      [-12,'C04','OSCAN','REFAP','BB-101A','Verificar alinhamento e término de partida da bomba BB-101A','Confirmar pressão de sucção e vazão nominal.','Crítica',15],
      [8,'C04','OSCAN','REFAP','TQ-804','Verificar o término do recebimento de MGO no TQ-804','Monitorar nível máximo seguro de 85% e preparar fechamento de válvula.','Alta',15],
      [22,'C08','OSBRA','REPLAN','ES-201','Acompanhar transferência de GLP para a esfera ES-201','Vazão prevista de 180 m³/h.','Normal',15],
      [50,'C10','DTCS','TEDEP','PCV-301','Ajuste de controle de contrapressão na PCV-301','Ajuste fino de setpoint para amortecimento de transiente.','Normal',15],
      [150,'C04','OSCAN','TEDEP',null,'Chegada estimada de PIG raspador no recebedor de TEDEP','Aviso prévio à equipe de manutenção para abertura de câmara.','Baixa',30],
      [-40,'C08','OSBRA','TEBAR',null,'Abertura de manifold de recebimento de Diesel S10','Operação concluída conforme procedimento operacional padrão.','Normal',15]
    ];
    for(const [offset,consoleName,pipelineName,unitName,tag,description,notes,priority,lead] of examples){
      const date=new Date(Date.now()+offset*60000),ds=`${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`,ts=`${String(date.getHours()).padStart(2,'0')}:${String(date.getMinutes()).padStart(2,'0')}`;
      const e=stamp(null,{consoleId:consoles[consoleName].id,pipelineId:pipelines[pipelineName].id,uoId:units[unitName].id,equipmentTypeId:tag?equipment[tag].equipmentTypeId:null,tagId:tag?equipment[tag].id:null,description,notes,priority,stylusDrawing:null,scheduledDate:ds,scheduledTime:ts,scheduledAt:U.localDateTime(ds,ts).toISOString(),status:'pendente',hasAlarm:true,useDefaultAlarmSettings:false,alarmMinutesBefore:lead,alarmAudio:true,alarmVisual:true,alarmNotification:false,alarmRepeat:false,alarmRepeatInterval:2,alarmMaxRepeats:5,alarmState:'idle',alarmTriggerCount:0,lastAlarmTriggeredAt:null,alarmSnoozedUntil:null,createdBy:actor(d),completedAt:null,completedTimeDiffMinutes:null,completionNote:''});
      d.events.push(e);history(d,e,'criacao','Demonstração criada');
      if(offset===-40){Object.assign(e,{status:'concluido',completedAt:new Date().toISOString(),completedBy:actor(d),completedTimeDiffMinutes:(Date.now()-Date.parse(e.scheduledAt))/60000,completionNote:'Manifold aberto e estanqueidade confirmada sem anomalias.',alarmState:'acknowledged',version:2});history(d,e,'conclusao','Demonstração concluída');}
    }
    return true;
  });
  const B=App.Backup;
  B.validateBackupData=function(input){let parsed;try{parsed=typeof input==='string'?JSON.parse(input):structuredClone(input);}catch(_){fail('Backup JSON inválido.');}if(!parsed||!['1',1].includes(parsed.schemaVersion)||!iso(parsed.exportedAt))fail('Versão ou data de exportação inválida.');validateData(parsed.data||{});return parsed;};
  B.createSnapshot=async()=>({application:'Controle de Previsões em Dutos',schemaVersion:1,exportedAt:new Date().toISOString(),data:await App.DB.snapshot()});
  B.exportJSON=async function(options={}){
    const b=await this.createSnapshot();
    await this.downloadBlob(new Blob([JSON.stringify(b,null,2)],{type:'application/json;charset=utf-8'}),`backup_previsoes_dutos_${new Date().toISOString().replace(/[:.]/g,'-')}.json`);
    // Preventive export must not mutate lastBackupAt or any other persisted value:
    // a failed export/download must leave the complete pre-import database intact.
    if(options.preventive===true)return b;
    const conf=await S.getSettings();conf.lastBackupAt=new Date().toISOString();await S.saveSettings(conf);
    await App.UI.updateBackupPill?.(conf.lastBackupAt);await App.UI.showToast?.('Backup JSON exportado com sucesso!','success');return b;
  };
  // Merge conflicts leave the ENTIRE database unchanged. UI must display conflicts.
  B.importJSON=async function(input,mode='merge'){
    if(!['merge','replace'].includes(mode))fail('Modo de importação inválido.');const backup=this.validateBackupData(input);
    if(mode==='replace')await this.exportJSON({preventive:true});
    return App.DB.atomic(stores,d=>{
      const result={mode,inserted:0,updated:0,skipped:0,conflicts:[],applied:false};
      const candidate=structuredClone(d);
      for(const store of stores){
        if(mode==='replace'){candidate[store]=structuredClone(backup.data[store]);result.inserted+=candidate[store].length;continue;}
        const key=r=>store==='settings'?r.key:r.id;
        for(const incoming of backup.data[store]){
          const current=candidate[store].find(x=>key(x)===key(incoming));
          if(!current){const business=uniqueKey(store,incoming);if(business!==null&&candidate[store].some(x=>uniqueKey(store,x)===business)){result.conflicts.push({store,id:key(incoming),reason:'duplicate-business-key'});continue;}candidate[store].push(structuredClone(incoming));result.inserted++;continue;}
          if(JSON.stringify(current)===JSON.stringify(incoming)){result.skipped++;continue;}
          const cv=current.version??0,nv=incoming.version??0,ct=Date.parse(current.updatedAt||current.createdAt||current.timestamp||'')||0,nt=Date.parse(incoming.updatedAt||incoming.createdAt||incoming.timestamp||'')||0;
          if(nv<cv||nt<ct){result.skipped++;continue;}
          if(nv===cv&&nt===ct){result.conflicts.push({store,id:key(incoming),reason:'same-revision-different-content'});continue;}
          if((nv>cv&&nt<ct)||(nv<cv&&nt>ct)){result.conflicts.push({store,id:key(incoming),reason:'divergent-revision'});continue;}
          Object.assign(current,structuredClone(incoming));result.updated++;
        }
      }
      if(result.conflicts.length){result.inserted=0;result.updated=0;return result;}
      try{validateData(candidate);}catch(err){if(mode==='replace')throw err;result.conflicts.push({store:'data',id:null,reason:err.message});result.inserted=0;result.updated=0;return result;}
      for(const store of stores)d[store]=candidate[store];result.applied=true;return result;
    });
  };
})();
"""

JS_SERVICE += r"""
(() => {
  const E=App.AlarmEngine;
  E._owner=App.Utils.uuid();E._tickPromise=null;E.onTick=null;
  E.channels=function(event,settings){const defaults=event.useDefaultAlarmSettings,volume=Number(settings.soundVolume??80);return {audio:!!((defaults?settings.soundEnabled:event.alarmAudio)&&Number.isFinite(volume)&&volume>0&&App.Audio.isUnlocked&&App.Audio.ctx?.state==='running'),visual:!!((defaults?settings.visualAlertEnabled:event.alarmVisual)&&typeof App.UI?.showAlarmModal==='function'),notification:!!((defaults?settings.notificationEnabled:event.alarmNotification)&&App.Notifications.getPermissionState()==='concedida')};};
  E.due=function(event,settings,now=Date.now()){
    if(!event||event.active===false||event.status!=='pendente'||!event.hasAlarm||event.alarmState==='acknowledged')return false;
    const defaults=event.useDefaultAlarmSettings,lead=defaults?(settings.defaultLeadTimeMinutes??15):(event.alarmMinutesBefore??0);
    if(now<Date.parse(event.scheduledAt)-lead*60000||event.alarmSnoozedUntil&&now<event.alarmSnoozedUntil)return false;
    if(event.alarmState==='snoozed'&&event.alarmSnoozedUntil&&now>=event.alarmSnoozedUntil)return true;
    if(!event.lastAlarmTriggeredAt)return true;
    // maxRepeats counts additional firings AFTER the initial alarm. Zero disables repeats.
    const repeat=defaults?settings.repeatAlarm:event.alarmRepeat,limit=defaults?(settings.maxRepeats??5):(event.alarmMaxRepeats??5),interval=defaults?(settings.repeatIntervalMinutes??2):(event.alarmRepeatInterval??2);
    return !!repeat&&(event.alarmTriggerCount??0)<1+limit&&now-Date.parse(event.lastAlarmTriggeredAt)>=interval*60000;
  };
  E.withLock=async function(callback){
    if(navigator.locks?.request)return navigator.locks.request('livro-previsoes-alarm-engine',{mode:'exclusive',ifAvailable:true},lock=>lock?callback():false);
    // localStorage lease is advisory, not a mutex. Only navigator.locks excludes
    // callbacks; IndexedDB's final transactional due check excludes duplicate claims.
    const key='livro-previsoes-alarm-lease',owner=this._owner;let lease;
    try{lease=JSON.parse(localStorage.getItem(key)||'null');if(lease&&lease.expires>Date.now()&&lease.owner!==owner)return false;localStorage.setItem(key,JSON.stringify({owner,expires:Date.now()+15000}));if(JSON.parse(localStorage.getItem(key)||'null')?.owner!==owner)return false;}catch(err){await App.DB.logError(err,'AlarmEngine lease');return false;}
    const renew=setInterval(()=>{try{const current=JSON.parse(localStorage.getItem(key)||'null');if(current?.owner===owner)localStorage.setItem(key,JSON.stringify({owner,expires:Date.now()+15000}));}catch(_){}},5000);
    try{return await callback();}finally{clearInterval(renew);try{if(JSON.parse(localStorage.getItem(key)||'null')?.owner===owner)localStorage.removeItem(key);}catch(_){}}
  };
  E.fireAlarm=async function(staleEvent){
    const claimed=await App.DB.atomic(['events','eventHistory','settings'],d=>{
      const current=d.events.find(e=>e.id===staleEvent.id),settings={...App.Config.DEFAULT_SETTINGS,...d.settings.find(s=>s.key==='app_settings')?.value};
      if(!this.due(current,settings))return null;
      const previous=JSON.stringify(current),now=new Date().toISOString();
      Object.assign(current,{alarmState:'triggered',lastAlarmTriggeredAt:now,alarmTriggerCount:(current.alarmTriggerCount??0)+1,alarmSnoozedUntil:null,updatedAt:now,version:(current.version??0)+1});
      const record={id:App.Utils.uuid(),eventId:current.id,action:'disparo_alarme',timestamp:now,description:'Alarme disparado. Canais acionados: nenhum.',channels:[],previousValue:previous,newValue:JSON.stringify(current),localUser:'Sistema de Alarme'};
      d.eventHistory.push(record);return{event:current,record,settings};
    });
    if(!claimed)return false;
    const {event,record,settings}=claimed,available=this.channels(event,settings),actual=[];
    for(const [channel,callback] of [['audio',()=>App.Audio.play(settings.soundType??'chime',settings.soundVolume??80)],['visual',()=>App.UI.showAlarmModal(event)],['notification',()=>App.Notifications.send(`Previsão Operacional: ${event.description}`,{body:App.Utils.formatDateTime(event.scheduledDate,event.scheduledTime),tag:`alarm-${event.id}`})]]){
      if(!available[channel])continue;
      // A concurrent completion or acknowledgement invalidates visual delivery as well.
      const latest=await App.DB.get('events',event.id);if(latest?.status!=='pendente'||latest.active===false||latest.alarmState!=='triggered')break;
      try{const result=await callback();if(channel!=='notification'||result)actual.push(channel);}catch(err){await App.DB.logError(err,'AlarmEngine '+channel);}
    }
    await App.DB.atomic(['eventHistory'],d=>{const h=d.eventHistory.find(x=>x.id===record.id);if(h){h.channels=actual;h.description=`Alarme disparado (${event.alarmTriggerCount===1?'Inicial':'Repetição '+(event.alarmTriggerCount-1)}). Canais acionados: ${actual.length?actual.join(', '):'nenhum disponível'}.`;}});
    return true;
  };
  E.tick=function(){
    if(this._tickPromise)return this._tickPromise;
    this._tickPromise=(async()=>{
      try{
        const clock=document.getElementById('liveClock');if(clock)clock.textContent=new Date().toLocaleString('pt-BR');
        await App.UI?.updateLiveTimers?.();
        await this.withLock(async()=>{
          const snapshot=await App.DB.snapshot(['events','settings']),settings={...App.Config.DEFAULT_SETTINGS,...snapshot.settings.find(s=>s.key==='app_settings')?.value};
          for(const event of snapshot.events.filter(event=>this.due(event,settings)))await this.fireAlarm(event);
        });
        const data=await App.DB.snapshot(['events','settings']),settings={...App.Config.DEFAULT_SETTINGS,...data.settings.find(s=>s.key==='app_settings')?.value};
        const triggered=data.events.filter(e=>e.active!==false&&e.status==='pendente'&&e.alarmState==='triggered');
        if(triggered.length&&settings.changeTitleEnabled){this.titleBlinkState=!this.titleBlinkState;document.title=this.titleBlinkState?'⚠ ALARME OPERACIONAL!':'ALARME — Caderno de Previsões';}else document.title=this.originalTitle;
        const state={now:Date.now(),triggeredIds:triggered.map(e=>e.id),channels:this.channels({useDefaultAlarmSettings:true},settings)};
        App.Audio.updateStatusPill();App.Notifications.updateStatusPill();
        if(this.onTick)await this.onTick(state);
        window.dispatchEvent(new CustomEvent('alarm-engine-tick',{detail:state}));
        return state;
      }catch(err){console.error('Erro no ciclo do AlarmEngine:',err);await App.DB.logError(err,'AlarmEngine tick');return null;}
      finally{this._tickPromise=null;}
    })();return this._tickPromise;
  };
})();
"""
