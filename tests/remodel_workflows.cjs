/* Behavioral and rendered-accessibility regression checks, isolated from user data. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'C:/Users/upseg/AppData/Roaming/npm/node_modules/@playwright/cli/node_modules/playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');
const root=path.resolve(__dirname,'..'),out=path.join(root,'output/playwright/remodel-20261026');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const context=await browser.newContext({viewport:{width:1440,height:1000},timezoneId:'America/Sao_Paulo'}),page=await context.newPage(),records=[],errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 const check=async(name,fn)=>{try{await fn();records.push({name,passed:true});}catch(e){records.push({name,passed:false,error:e.stack});}console.log(name,records.at(-1).passed?'PASS':'FAIL');};
 await page.goto(pathToFileURL(path.join(root,'index.html')).href);
 await page.waitForFunction(()=>window.App?.DB.db&&App.AlarmEngine.intervalId!==null);
 await page.evaluate(async()=>{App.AlarmEngine.stop();await App.Service.loadDemoData();await App.UI.renderDashboard();});
 await check('create / complete / reopen / duplicate with history',async()=>{
  await page.evaluate(()=>App.UI.navigateTo('viewNewEvent'));
  const ids=await page.evaluate(async()=>({pipeline:(await App.DB.getAll('pipelines')).find(e=>e.name==='OSCAN').id,uo:(await App.DB.getAll('operationalUnits')).find(e=>e.name==='REFAP').id}));
  await page.locator('#selectEventPipeline').selectOption(ids.pipeline);await page.locator('#selectEventUO').selectOption(ids.uo);
  await page.locator('#inputEventDescription').fill('Verificação da remodelação');await page.locator('#btnSubmitEvent').click();
  await page.waitForFunction(async()=>(await App.DB.getAll('events')).some(e=>e.description==='Verificação da remodelação'));
  const id=await page.evaluate(async()=>(await App.DB.getAll('events')).find(e=>e.description==='Verificação da remodelação').id);
  await page.evaluate(id=>App.UI.showCompleteModal(id),id);await page.locator('#inputCompleteNotes').fill('Teste isolado');await page.locator('#btnConfirmCompleteModal').click();
  await page.waitForFunction(async id=>(await App.DB.get('events',id)).status==='concluido',id);
  await page.evaluate(id=>App.UI.showReopenModal(id),id);await page.locator('#btnConfirmReopenModal').click();
  await page.waitForFunction(async id=>(await App.DB.get('events',id)).status==='pendente',id);
  await page.evaluate(id=>App.UI.duplicateEvent(id),id);await page.locator('#inputEventDescription').fill('Cópia de verificação');await page.locator('#btnSubmitEvent').click();
  await page.waitForFunction(async()=>(await App.DB.getAll('events')).some(e=>e.description==='Cópia de verificação'));
  const history=await page.evaluate(async id=>(await App.DB.getAll('eventHistory')).filter(e=>e.eventId===id).map(e=>e.action),id);
  for(const action of ['criacao','conclusao','reabertura'])assert(history.includes(action));
 });
 await check('JSON backup and three CSV downloads',async()=>{
  await page.evaluate(()=>App.UI.navigateTo('viewBackup'));
  for(const id of ['btnExportJSON','btnExportCSVAllPending','btnExportCSVAllCompleted','btnExportCSVCadastros']){
   const promise=page.waitForEvent('download');await page.locator('#'+id).click();const download=await promise;assert.equal(await download.failure(),null);
  }
 });
 await check('pending search and clear filters',async()=>{
  await page.evaluate(()=>App.UI.navigateTo('viewPendingEvents'));await page.locator('#inputSearchPending').fill('PIG');await page.waitForTimeout(200);
  const items=await page.evaluate(()=>App.UI.activePendingEvents.map(e=>e.description));assert(items.length&&items.every(x=>x.includes('PIG')));
  await page.locator('#btnClearFilters').click();await page.waitForTimeout(200);assert((await page.evaluate(()=>App.UI.activePendingEvents.length))>items.length);
 });
 const views=['viewDashboard','viewNewEvent','viewPendingEvents','viewCompletedEvents','viewCadastros','viewConfigAlerts','viewConfigColors','viewBackup','viewDiagnostic'];
 let contrastSamples=0;
 for(const theme of ['dark','light','industrial'])await check('rendered contrast / '+theme,async()=>{
  await page.evaluate(t=>App.UI.applyTheme(t),theme);await page.waitForTimeout(200);
  const failures=[];
  for(const v of views){await page.evaluate(v=>App.UI.navigateTo(v),v);await page.waitForTimeout(200);
   const samples=await page.evaluate(()=>{
    const rgb=s=>(s.match(/[\d.]+/g)||[]).map(Number),lum=a=>a.slice(0,3).map(x=>(x/=255)<=.04045?x/12.92:((x+.055)/1.055)**2.4).reduce((s,x,i)=>s+x*[.2126,.7152,.0722][i],0);
    return [...document.querySelectorAll('.card-subtitle,.form-help,.metric-label,.nav-item,.btn-primary,.event-countdown,.view-heading,.context-panel dt,.context-panel dd')].filter(e=>e.getClientRects().length&&!e.disabled).flatMap(e=>{
     let node=e,bg;while(node){const s=getComputedStyle(node),a=rgb(s.backgroundColor);if(s.backgroundImage!=='none')return [];if(a.length===3||a[3]===1){bg=a;break;}node=node.parentElement;}
     if(!bg)return [];const s=getComputedStyle(e),a=lum(rgb(s.color)),b=lum(bg),minimum=parseFloat(s.fontSize)>=24||parseFloat(s.fontSize)>=18.66&&parseInt(s.fontWeight)>=700?3:4.5;
     return [{text:e.textContent.trim().slice(0,50),ratio:(Math.max(a,b)+.05)/(Math.min(a,b)+.05),minimum}];
    });
   });contrastSamples+=samples.length;failures.push(...samples.filter(x=>x.ratio+.02<x.minimum).map(x=>({view:v,...x})));
  }assert.deepEqual(failures,[]);
  await page.evaluate(()=>App.UI.navigateTo('viewDashboard'));await page.screenshot({path:path.join(out,`theme-${theme}.png`)});
 });
 await check('200% text scaling / keyboard focus / reduced motion',async()=>{
  await page.evaluate(()=>{App.UI.applyTheme('dark');document.documentElement.style.fontSize='32px';});
  for(const v of views){await page.evaluate(v=>App.UI.navigateTo(v),v);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),v);}
  await page.evaluate(()=>{document.documentElement.style.fontSize='';App.UI.navigateTo('viewDashboard');});
  await page.locator('.metric-card[data-filter=overdue]').focus();await page.keyboard.press('Enter');await page.waitForTimeout(200);assert.equal(await page.evaluate(()=>App.UI.currentView),'viewPendingEvents');
  await page.emulateMedia({reducedMotion:'reduce'});assert(await page.evaluate(()=>[...document.querySelectorAll('.pulsing-card,.pulsing-badge')].every(e=>parseFloat(getComputedStyle(e).animationDuration)===0)));
 });
 await check('touch / portrait and landscape / form state retained',async()=>{
  const mobile=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,deviceScaleFactor:2});const p=await mobile.newPage();await p.goto(pathToFileURL(path.join(root,'index.html')).href);await p.waitForFunction(()=>window.App?.DB.db&&App.AlarmEngine.intervalId!==null);
  await p.evaluate(()=>{App.AlarmEngine.stop();App.UI.navigateTo('viewNewEvent');});await p.locator('#inputEventDescription').fill('Preservar ao girar');
  for(const id of ['inputEventDescription','selectEventPipeline','btnSubmitEvent']){const r=await p.locator('#'+id).boundingBox();assert(r.height>=44);}
  await p.setViewportSize({width:844,height:390});await p.waitForTimeout(200);assert.equal(await p.locator('#inputEventDescription').inputValue(),'Preservar ao girar');assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));await mobile.close();
 });
 await check('offline reload retains events',async()=>{
  const count=await page.evaluate(async()=>(await App.DB.getAll('events')).length);await context.setOffline(true);await page.reload();await page.waitForFunction(()=>window.App?.DB.db&&App.AlarmEngine.intervalId!==null);await page.evaluate(()=>App.AlarmEngine.stop());assert.equal(await page.evaluate(async()=>(await App.DB.getAll('events')).length),count);
 });
 await check('no runtime exceptions',async()=>assert.deepEqual(errors,[]));
 fs.writeFileSync(path.join(out,'workflows.json'),JSON.stringify({records,contrastSamples,errors},null,2));await browser.close();if(records.some(r=>!r.passed))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
