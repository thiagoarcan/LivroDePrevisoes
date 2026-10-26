/* Local, isolated browser audit. Uses the already-installed Playwright CLI runtime. */
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'C:/Users/upseg/AppData/Roaming/npm/node_modules/@playwright/cli/node_modules/playwright');
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const root=path.resolve(__dirname,'..'), phase=process.argv[2]||'after';
const out=path.join(root,'output/playwright/remodel-20261026');fs.mkdirSync(out,{recursive:true});
const views=['viewDashboard','viewNewEvent','viewPendingEvents','viewCompletedEvents','viewCadastros','viewConfigAlerts','viewConfigColors','viewBackup','viewDiagnostic'];
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const context=await browser.newContext({viewport:{width:1440,height:1000},timezoneId:'America/Sao_Paulo'});
 const page=await context.newPage(), errors=[], results=[];
 page.on('pageerror',e=>errors.push(e.message));
 let source=path.join(root,'index.html');
 if(phase==='before'){source=path.join(out,'baseline.html');fs.writeFileSync(source,require('node:child_process').execFileSync('git',['show','7fc610408dfca1d49c245216613f4355236ec268:index.html'],{cwd:root}));}
 await page.goto(pathToFileURL(source).href);
 await page.waitForFunction(()=>window.App?.DB.db&&App.AlarmEngine.intervalId!==null);
 await page.evaluate(async()=>{App.AlarmEngine.stop();await App.AlarmEngine.tick();await App.Service.loadDemoData();await App.UI.renderDashboard();});
 const timing=await page.evaluate(()=>performance.getEntriesByType('navigation')[0].toJSON());
 for(const [width,height] of [[320,740],[360,800],[390,844],[768,1024],[844,390],[1024,768],[1280,800],[1280,1024],[1440,900],[1920,1080],[2560,1080],[3440,1440],[3840,2160],[5120,1440]]){
  await page.setViewportSize({width,height});
  await page.evaluate(()=>App.UI.applyResponsiveLayoutMode('auto',false));
  for(const view of views){
   await page.evaluate(v=>App.UI.navigateTo(v),view);await page.waitForTimeout(60);
   results.push(await page.evaluate(({view,width,height})=>({view,width,height,tier:document.body.dataset.layoutMode,overflow:document.documentElement.scrollWidth>innerWidth+1,heading:!!document.querySelector('#'+view+' .view-heading')?.getClientRects().length}),{view,width,height}));
   if([320,390,1440,3440].includes(width))await page.screenshot({path:path.join(out,`${phase}-${view}-${width}.png`),fullPage:false});
  }
 }
 fs.writeFileSync(path.join(out,`${phase}.json`),JSON.stringify({timing,errors,results},null,2));
 console.log(JSON.stringify({phase,checks:results.length,overflow:results.filter(x=>x.overflow),errors}));
 await browser.close();
})().catch(e=>{console.error(e);process.exitCode=1});
