// Optional local browser QA: requires Playwright and its Chromium headless shell.
// Serve the built site at http://127.0.0.1:8765 before running this script.
const {chromium}=require('playwright');
const fs=require('fs');
const dest=require('path').resolve(process.argv[2] || 'review/metal-cutting');
fs.mkdirSync(dest,{recursive:true});
(async()=>{
const browser=await chromium.launch({headless:true});let report={};
for(const [name,width,height] of [['desktop',1440,1000],['mobile',390,844]]){
const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1});const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto('http://127.0.0.1:8765/projects/metal-cutting/',{waitUntil:'networkidle'});
await page.evaluate(()=>{document.querySelectorAll('img').forEach(i=>i.loading='eager')});
await page.evaluate(()=>Promise.all(Array.from(document.images).map(i=>i.decode().catch(()=>{}))));

await page.screenshot({path:`${dest}/${name}-top.png`});
const data=await page.evaluate(()=>({title:document.title,canonical:document.querySelector('link[rel=canonical]')?.href,description:document.querySelector('meta[name=description]')?.content,overflow:document.documentElement.scrollWidth>innerWidth,images:[...document.querySelectorAll('article img')].map(i=>({src:i.getAttribute('src'),ok:i.complete&&i.naturalWidth>0,alt:!!i.alt})),videos:[...document.querySelectorAll('video')].map(v=>({src:v.currentSrc,width:v.videoWidth,duration:v.duration,controls:v.controls,muted:v.muted,autoplay:v.autoplay,error:v.error?.message})),math:document.querySelectorAll('[role=math]').length}));
await page.locator('.cutting-media-grid').scrollIntoViewIfNeeded();
for(const video of await page.locator('video').all()) {
  await video.scrollIntoViewIfNeeded();
  await video.evaluate(async v=>{await v.play();await new Promise(r=>v.requestVideoFrameCallback(()=>v.requestVideoFrameCallback(r)));v.pause();});
}
await page.reload({waitUntil:'networkidle'});
await page.locator('video').first().scrollIntoViewIfNeeded();
await page.evaluate(()=>Promise.all([...document.querySelectorAll('video')].map(v=>{let i=new Image();i.src=v.poster;return i.decode()})));
await page.waitForFunction(()=>[...document.querySelectorAll('video')].every(v=>v.readyState>=2&&!v.seeking));
await page.waitForTimeout(1200);
await page.locator('video').first().evaluate(v=>{v.scrollIntoView({block:'start'});window.scrollBy(0,-85)});
await page.mouse.move(0,0);
await page.waitForTimeout(600);
await page.screenshot({path:`${dest}/${name}-media.png`});
await page.goto('http://127.0.0.1:8765/projects/',{waitUntil:'networkidle'});await page.locator('article a[href="metal-cutting/"]').click();data.catalogNavigates=page.url().endsWith('/projects/metal-cutting/');
await page.goto('http://127.0.0.1:8765/projects/metal-cutting/');await page.keyboard.press('Tab');data.keyboardFocus=await page.evaluate(()=>document.activeElement.tagName);report[name]={...data,errors};await page.close();
}
fs.writeFileSync(`${dest}/browser-checks.json`,JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));await browser.close();
if(Object.values(report).some(x=>x.overflow||x.errors.length||x.images.some(i=>!i.ok||!i.alt)||x.videos.some(v=>v.error||!v.width||!v.controls||!v.muted||v.autoplay)))process.exitCode=1;
})().catch(e=>{console.error(e);process.exit(1)});
