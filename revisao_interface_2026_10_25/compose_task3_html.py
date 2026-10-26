from pathlib import Path
import sys,re
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'revisao_interface_2026_10_25/originais'))
from parts_html import HTML_CONTENT
s=BeautifulSoup(HTML_CONTENT,'html.parser')
def node(tag,**attrs):return s.new_tag(tag,attrs=attrs)
def by(id):return s.find(id=id)
def cls(e,name):e['class']=e.get('class',[])+[name];return e
def panel(id,title):
    e=node('aside',id=id,**{'class':'context-panel','aria-label':title});h=node('h2');h.string=title;e.append(h);return e
def wrap(e,tag='div',**attrs):
    w=node(tag,**attrs);e.wrap(w);return w
def group(nodes,title,tag='fieldset',classes=''):
    g=node(tag,**{'class':classes});h=node('legend' if tag=='fieldset' else 'h2');h.string=title;g.append(h)
    for n in nodes:g.append(n.extract())
    return g
# Static semantic source; JS remains the authority for state and visibility.
main=s.select_one('main');main['id']='mainContent';main['tabindex']='-1'
skip=node('a',href='#mainContent',**{'class':'skip-link'});skip.string='Ir para conteúdo';s.insert(0,skip)
nav=s.select_one('.app-nav');nav.attrs.pop('role',None);nav['aria-label']='Navegação principal'
for n in s.select('.nav-item'):n.attrs.pop('role',None)
for svg in s.select('svg'):svg['aria-hidden']='true';svg['focusable']='false'
newlabel=node('span');newlabel.string='Novo';by('fabAddEvent').append(newlabel)
for n in s.select('.metric-card[data-filter]'):n.name='button';n['type']='button'
for id in ['pillAudio','pillNotif','chipHeaderAudioWarning']:
    by(id).name='button';by(id)['type']='button'
for m in s.select('.modal-overlay'):
    h=m.select_one('.modal-header h3')
    if h:
        h['id']=h.get('id',m['id']+'Heading');m['role']='dialog';m['aria-modal']='true';m['aria-labelledby']=h['id']
        for b in m.select('.modal-close'):b['aria-label']='Fechar '+h.get_text(' ',strip=True)
# Remove inline typography, fixed minimum dimensions and grid tracks that defeated responsive rules.
for e in s.select('[style]'):
    keep=[]
    for decl in e['style'].split(';'):
        if ':' not in decl:continue
        k,v=decl.split(':',1);k=k.strip();v=v.strip()
        if k in ['font-size','font-family','min-width','max-width','min-height','max-height','grid-template-columns']:continue
        if k=='color' and not v.startswith('var('):continue
        if k in ['width','height'] and (v.endswith('px') or v=='auto'):continue
        keep.append(k+': '+v)
    if keep:e['style']='; '.join(keep)
    else:del e['style']
for d in s.select('div[style]'):
    if 'display: flex' in d.get('style','') and 'flex-wrap' not in d['style']:d['style']+='; flex-wrap: wrap'
desc=by('inputEventDescription');replacement=node('textarea',**{k:v for k,v in desc.attrs.items() if k!='type'});replacement['rows']='3';replacement.string='';desc.replace_with(replacement)
# Associate real nearby labels, with explicit contextual names for searches/aliases.
names={'inputConsoleName':'Nome do console','inputInlineNewUO':'Nova UO para o duto','inputImportBackupFile':'Arquivo de backup JSON','inputRangeColorText':'Código hexadecimal da cor','inputStylusStrokeColor':'Cor da caneta','selectStylusStrokeWidth':'Espessura da caneta','stylusColor':'Cor da caneta (compatibilidade)','stylusWidth':'Espessura da caneta (compatibilidade)'}
for e in s.select('input[id],select[id],textarea[id]'):
    if e.get('type')=='hidden' or e.find_parent('label') or s.find('label',attrs={'for':e['id']}):continue
    label=e.parent.find('label',recursive=False)
    if label and not label.get('for') and not label.find(['input','select','textarea']):label['for']=e['id'];continue
    name=names.get(e['id']) or e.get('placeholder') or e.get('aria-label')
    if not name:
        name={'filterActiveConsoles':'Situação dos consoles','filterActivePipelines':'Situação dos dutos','filterActiveUOs':'Situação das UOs','filterActiveEquipmentTypes':'Situação dos tipos','filterActiveTags':'Situação das TAGs','selectSortPending':'Ordenação dos eventos pendentes'}.get(e['id'])
    if not name:raise ValueError('Missing meaningful label: '+e['id'])
    label=node('label',**{'for':e['id'],'class':'control-label'});label.string=name;e.insert_before(label)
# Group event fields without cloning controls or changing IDs.
form=by('formEvent');grid=form.select_one('.form-grid');children=grid.find_all('div',recursive=False)
groups=[('Localização',children[:5]),('Programação',children[5:8]),('Atividade',children[8:10]),('Lousa',children[10:])]
for title,els in groups:
    g=group(els,title,classes='event-fieldset fieldset-'+title.lower().replace('ç','c').replace('ã','a'));grid.append(g)
grid['class']=['event-form-sections']
notes=by('inputEventNotes').parent;detail=node('details',**{'class':'optional-group'});summ=node('summary');summ.string='Observações e recomendações';detail.append(summ);notes.wrap(detail)
alarm=form.find('div',class_='card',recursive=False);alarm.name='fieldset';alarm['class']=['event-fieldset'];legend=node('legend');legend.string='Alarme';alarm.insert(0,legend)
footer=form.select_one('.form-sticky-submit-bar');footer.insert_before(by('checkKeepDutoUO').parent.extract());footer.insert_before(by('btnResetEventForm').extract());cls(by('btnResetEventForm'),'event-reset-action')
by('stylusDrawingCanvas')['width']='1200';by('stylusDrawingCanvas')['height']='440'
# Shared master region for both modalities.
master=node('div',**{'class':'pending-master'});by('containerPendingCards').wrap(master);master.append(by('containerPendingTable').extract())
by('viewPendingEvents').select_one('.pending-master-detail-grid').append(panel('pendingContextPanel','Contexto da seleção'))
# Dashboard: spotlight and alarms grouped, urgent list, selected detail, operational panorama.
dash=by('viewDashboard');dash.append(panel('dashboardSelectedDetail','Evento em foco'));dash.append(panel('dashboardContextPanel','Panorama do console'))
overview=node('div',id='dashboardOverview',**{'class':'dashboard-overview'});dash.append(overview);overview.append(dash.select_one('.dashboard-metrics').extract());overview.append(by('dashboardContextPanel').extract())
overview.insert(0,by('dashboardContextPanel').extract())
context=node('div',id='dashboardContextStack',**{'class':'dashboard-context-stack'});by('dashboardSelectedDetail').wrap(context);context.insert(0,overview.extract())
for id,title in [('eventDraftSummary','Prévia não salva'),('eventRelatedList','Previsões relacionadas')]:by('viewNewEvent').append(panel(id,title))
completed=node('div',**{'class':'completed-workspace'});by('containerCompletedCards').wrap(completed);completed.append(by('tableCompletedWrapper').extract());completed.append(by('completedEmptyMessage').extract());by('viewCompletedEvents').append(panel('completedContextPanel','Resumo dos concluídos'));by('viewCompletedEvents').append(panel('completedDetailPane','Conclusão selecionada'))
filters=by('viewCompletedEvents').select_one('.toolbar-filters');disclosure=node('details',id='completedFilters',**{'class':'completed-filters'});filters.wrap(disclosure);summary=node('summary');summary.string='Filtros';disclosure.insert(0,summary);scope=node('span',id='completedFiltersSummary',**{'class':'filter-scope'});scope.string='Todos os concluídos';summary.append(scope)
# Catalogs: each category has a genuine list and editor region. UI owns category visibility.
for e in s.select('[data-cat-item]'):
    cls(e,'catalog-category')
    f=e.find('form',recursive=False)
    if f:
        cls(f,'catalog-editor');others=[x for x in e.find_all('div',recursive=False) if 'hub-header' not in x.get('class',[])];
        if others:cls(others[-1],'catalog-list')
        b=node('button',type='button',**{'class':'btn btn-outline catalog-new','data-catalog-new':f['id']});b.string='Novo registro';(others[-1] if others else f).insert(0,b)
        back=node('button',type='button',**{'class':'btn btn-outline catalog-back','data-catalog-back':f['id']});back.string='Voltar à lista';f.insert(0,back);e['data-editor-open']='false'
by('viewCadastros').append(panel('cadastrosRelationsPanel','Vínculos do registro'))
# Alert preferences grouped into editable sections, with local test controls.
f=by('formAlertSettings') or by('formSettings');assert f is not None
grid=f.select_one('.form-grid');els=grid.find_all('div',recursive=False)
for title,ids in [('Antecedência e repetição',['inputDefaultLeadTime','inputSettingLeadTime','checkSettingRepeat']),('Som e volume',['selectSoundType','rangeSoundVolume']),('Aparência e layout',['selectSettingsViewMode','selectSettingsTheme']),('Canais de alerta',['checkSettingSound'])]:
    chosen=[]
    for e in els:
        if any(e.find(id=i) for i in ids):chosen.append(e)
    if not chosen:continue
    d=node('details',open='',**{'class':'settings-group'});summary=node('summary');summary.string=title;d.append(summary)
    for e in chosen:d.append(e.extract());els.remove(e)
    grid.append(d)
for e in list(els):
    d=node('details',open='',**{'class':'settings-group'});summary=node('summary');summary.string=e.find('label').get_text(' ',strip=True) if e.find('label') else 'Preferências';d.append(summary);d.append(e.extract());grid.append(d)
sound=by('selectSoundType').find_parent('details');sound.append(by('btnTestSound').extract())
channels=by('checkSettingSound').find_parent('details')
for id in ['btnTestVisual','btnRequestNotifPermission','btnTestNotif']:channels.append(by(id).extract())
rem=node('div',**{'class':'form-group'});label=node('label',**{'for':'inputBackupReminderDays'});label.string='Lembrar backup após (dias)';rem.append(label);rem.append(node('input',id='inputBackupReminderDays',type='number',min='1',max='3650',value='7'));grid.append(rem)
by('viewConfigAlerts').append(panel('settingsPreviewPanel','Prévia das preferências'))
# Color editor beside the saved list and explicit sample.
colors=by('viewConfigColors').select_one('.card');cls(colors,'color-workspace');editor=by('formColorRange').parent;cls(editor,'range-editor');colors.append(panel('rangeLivePreview','Exemplo de aparência'))
# Backup: separate export/import, local inventory, destructive maintenance.
backup=by('viewBackup').select_one('.card');cls(backup,'backup-workspace');op=by('btnExportJSON').parent.parent;cls(op,'backup-operations');backup.append(panel('backupContextPanel','Estado da base local'));cls(by('btnWipeAllData').parent.parent,'maintenance-panel')
op.attrs.pop('style',None)
filename=node('p',id='backupSelectedFileName',**{'class':'form-help','aria-live':'polite'});filename.string='Nenhum arquivo selecionado.';by('inputImportBackupFile').insert_after(filename)
# Diagnostic: three real regions with existing official outputs.
diag=by('viewDiagnostic').select_one('.card');cls(diag,'diagnostic-workspace');cls(diag.select_one('.form-grid'),'diagnostic-status');collections=by('tbodyDiagCollections').find_parent('div');heading=collections.find_previous_sibling('h4');reg=node('section',**{'class':'diagnostic-collections'});heading.wrap(reg);reg.append(collections.extract());logs=by('tbodyDiagLogs').find_parent('div');heading=logs.find_previous_sibling('div');reg=node('section',**{'class':'diagnostic-logs'});heading.wrap(reg);reg.append(logs.extract())
by('tbodyDiagCollections').parent['id']='tableDiagCollections';by('tbodyDiagLogs').parent['id']='tableDiagLogs'
table_names={'tableDashboardUrgent':'Eventos urgentes','tablePendingEvents':'Eventos pendentes','tableCompletedEvents':'Eventos concluídos','tableConsoles':'Consoles','tablePipelines':'Dutos','tableUOs':'Unidades operacionais','tableEquipmentTypes':'Tipos de equipamentos','tableEquipmentTags':'TAGs de equipamentos','tableColorRanges':'Faixas de tempo','tableDiagCollections':'Coleções locais','tableDiagLogs':'Logs de diagnóstico'}
for wrapper in s.select('.table-responsive,.hub-list-container'):
    table=wrapper.find('table')
    if not table:continue
    wrapper['tabindex']='0';wrapper['role']='region';wrapper['aria-label']=table_names[table['id']]+' — tabela com rolagem horizontal';wrapper['data-scroll-table']=''
    hint=node('p',**{'class':'table-scroll-hint','hidden':''});hint.string='Deslize a tabela ou use as setas do teclado para consultar as demais colunas.';wrapper.insert_before(hint)
recommendation=by('modalDependency').select_one('.notice-banner');text=node('p');
for child in list(recommendation.contents):text.append(child.extract())
recommendation.append(text)
for opt in by('selectSettingsViewMode').select('option'):
    if opt.get('value')=='conventional':opt.string='Monitor convencional (1200–1919 px)'
    elif opt.get('value')=='widescreen':opt.string='Widescreen (1920–2559 px)'
    elif opt.get('value')=='ultrawide':opt.string='Ultrawide (2560 px ou mais)'
# A concise title for every named view, kept out of the responsive panel grid.
titles=['Painel operacional','Nova previsão','Eventos pendentes','Eventos concluídos','Cadastros operacionais','Configurações de alertas','Faixas de tempo e cores','Backup e dados','Diagnóstico']
for view,title in zip(s.select('.view-section'),titles):
    h=node('h2',id=view['id']+'Heading',**{'class':'view-heading'});h.string=title;view.insert(0,h);view['aria-labelledby']=h['id']
for b in s.select('button'):
    if not b.get('type'):b['type']='button'
    if b.get_text(strip=True) in ['×','✕','&times;'] and not b.get('aria-label'):b['aria-label']='Fechar'
# Metadata is filled from the central runtime configuration, never a second version literal.
drawer_version=by('appMobileDrawer').select_one('.drawer-header').find(string=lambda t:t and 'v1.1.0' in t)
if drawer_version:
    parent=drawer_version.parent;parent.clear();parent.append(node('span',**{'data-app-version':''}));parent.append(' • Operação Offline')
by('diagAppVersion').string='—'
# A stable annotated source, no runtime parser or dependency.
(ROOT/'parts_html.py').write_text('# -*- coding: utf-8 -*-\nHTML_CONTENT = """\n'+s.prettify()+'\n"""\n',encoding='utf-8')
