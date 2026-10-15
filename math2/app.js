'use strict';
(() => {
  const $ = (s, p = document) => p.querySelector(s);
  const $$ = (s, p = document) => Array.from(p.querySelectorAll(s));
  const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const key = 'math2-topic-practice:v1';
  const typeNames = {single:'选择题',fill:'填空题',solution:'解答题'};
  const viewNames = {topics:'专题刷题',years:'年份真题',wrong:'错题本',favorites:'我的收藏',history:'学习记录'};
  const chapterOrder = ['函数、极限、连续','一元函数微分学','一元函数积分学','多元函数微积分学','常微分方程','行列式','矩阵','向量','线性方程组','矩阵的特征值和特征向量','二次型'];
  const chapterRank = name => chapterOrder.includes(name)?chapterOrder.indexOf(name):99;
  const weakDefinitions = [
    ['数列极限',/数列|递推/],['反常积分',/反常积分|广义积分/],['定积分应用',/定积分.*应用|物理应用|几何应用|旋转体|液体压力|功的计算/],
    ['条件极值',/条件极值|拉格朗日|约束极值/],['特征值',/特征值|特征向量/],['二次型',/二次型|正定|合同/],
    ['正交对角化',/正交对角化/],['同解与公共解',/同解|公共解/],['合同与正定性',/合同|正定/],['定积分物理应用',/物理应用|液体压力|功的计算|引力/]
  ];
  let questions = [], questionMap = new Map(), meta = {}, weakGroups = [], dataLoaded = false;
  let view = 'topics', listMode = false, page = 1, sort = 'new';
  let filters = {subject:'',chapter:'',topic:'',type:'',from:2007,to:2026,status:'',search:'',weak:''};
  let db = readDatabase(), activeId = null, queue = [], queueIndex = 0, readerReturnFocus = null;
  let answerChoice = '', checkedChoice = '', zoom = 100, timerRunning = false, timerStarted = 0, sessionSeconds = 0;
  let toastTimeout, noteTimeout;
  const dayKey = (date = new Date()) => `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;
  function blankDb() { return {version:1,records:{},days:{},activity:[],lastId:null}; }
  function readDatabase() {
    try {
      const text = localStorage.getItem(key);
      if (!text) return blankDb();
      const value = JSON.parse(text);
      if(value.version !== 1 || !value.records || typeof value.records !== 'object') return blankDb();
      return {...blankDb(),...value,activity:Array.isArray(value.activity)?value.activity:[],days:value.days && typeof value.days==='object'?value.days:{}};
    } catch { return blankDb(); }
  }
  function saveDatabase(silent = false) {
    try { localStorage.setItem(key,JSON.stringify(db)); return true; }
    catch { if(!silent) toast('此浏览器暂时无法保存，请导出备份以免丢失记录。'); return false; }
  }
  function record(id) {
    if(!Object.prototype.hasOwnProperty.call(db.records,id) || !db.records[id] || typeof db.records[id]!=='object') db.records[id] = {status:'unseen',favorite:false,everWrong:false,note:'',seconds:0,attempts:[]};
    const r = db.records[id];
    if(!Array.isArray(r.attempts)) r.attempts = [];
    if(!Number.isFinite(r.seconds)) r.seconds=0;
    return r;
  }
  function status(id) { return db.records[id]?.status || 'unseen'; }
  function attempted(id) { return !!db.records[id]?.attempts?.length; }
  function searchable(q) { return [q.subject,q.chapter,q.topic,...q.tags,q.year,q.id,`${q.year}年第${q.number}题`].join(' '); }
  function safeUrl(url) {
    try { const u = new URL(url); return ['http:','https:'].includes(u.protocol) ? u.href : ''; } catch { return ''; }
  }
  function safeAsset(path) {
    if(typeof path !== 'string' || !path) return '';
    if (/^(?:javascript|data|vbscript):/i.test(path)) return '';
    if (/^https?:\/\//i.test(path)) return safeUrl(path);
    return path;
  }
  function link(url,text,cls = '') { const href=safeUrl(url); return href?`<a href="${esc(href)}" target="_blank" rel="noopener noreferrer"${cls?` class="${esc(cls)}"`:''}>${esc(text)} ↗</a>`:''; }
  function toast(text) { clearTimeout(toastTimeout); $('#toast').textContent=text; $('#toast').classList.add('show'); toastTimeout=setTimeout(()=>$('#toast').classList.remove('show'),3300); }
  function unique(values) { return [...new Set(values)].filter(Boolean); }
  function qsByFilters(ignoreSubject = false) {
    const w = weakGroups.find(item=>item.name===filters.weak);
    return questions.filter(q => {
      if(view==='wrong' && !db.records[q.id]?.everWrong) return false;
      if(view==='favorites' && !db.records[q.id]?.favorite) return false;
      if(!ignoreSubject && filters.subject && q.subject!==filters.subject) return false;
      if(filters.chapter && q.chapter!==filters.chapter) return false;
      if(filters.topic && q.topic!==filters.topic) return false;
      if(filters.type && q.type!==filters.type) return false;
      if(q.year<filters.from || q.year>filters.to) return false;
      if(filters.status==='attempted' ? !attempted(q.id) : filters.status && status(q.id)!==filters.status) return false;
      if(w && !w.ids.has(q.id)) return false;
      return !filters.search || searchable(q).toLowerCase().includes(filters.search.toLowerCase().trim());
    });
  }
  function sorted(list) { return [...list].sort((a,b)=>sort==='old'?a.year-b.year||a.number-b.number:sort==='number'?a.number-b.number||b.year-a.year:b.year-a.year||a.number-b.number); }
  function option(value,label,selected) { return `<option value="${esc(value)}"${String(value)===String(selected)?' selected':''}>${esc(label)}</option>`; }
  function syncFilterControls() {
    const base = questions.filter(q=>!filters.subject || q.subject===filters.subject);
    const chapters=unique(base.map(q=>q.chapter)).sort((a,b)=>chapterRank(a)-chapterRank(b));
    $('#chapter-filter').innerHTML=option('','全部章节',filters.chapter)+chapters.map(v=>option(v,v,filters.chapter)).join('');
    const topics=unique(base.filter(q=>!filters.chapter||q.chapter===filters.chapter).map(q=>q.topic));
    $('#topic-filter').innerHTML=option('','全部专题',filters.topic)+topics.map(v=>option(v,v,filters.topic)).join('');
    $('#type-filter').value=filters.type;
    const years=unique(questions.map(q=>q.year)).sort((a,b)=>a-b);
    $('#year-from').innerHTML=years.map(y=>option(y,y,filters.from)).join('');
    $('#year-to').innerHTML=years.map(y=>option(y,y,filters.to)).join('');
    $('#status-filter').value=filters.status;
    if(document.activeElement!==$('#search-filter')) $('#search-filter').value=filters.search;
  }
  function renderStats() {
    const mastered=questions.filter(q=>status(q.id)==='mastered').length;
    $('#stat-total').textContent=questions.length;
    $('#stat-topics').textContent=unique(questions.map(q=>`${q.subject}/${q.chapter}/${q.topic}`)).length;
    $('#stat-years').textContent=unique(questions.map(q=>q.year)).length;
    $('#stat-mastered').textContent=mastered;
    $('#stat-percent').textContent=`${Math.round(mastered/questions.length*100)||0}%`;
    $('#nav-topic-count').textContent=$('#stat-topics').textContent;
    $('#nav-year-count').textContent=$('#stat-years').textContent;
    $('#nav-wrong-count').textContent=questions.filter(q=>db.records[q.id]?.everWrong).length;
    $('#nav-fav-count').textContent=questions.filter(q=>db.records[q.id]?.favorite).length;
  }
  function renderWeak() {
    $('#weak-chips').innerHTML=weakGroups.map(w=>`<button class="chip${filters.weak===w.name?' active':''}" data-weak="${esc(w.name)}">${esc(w.name)}<span>${w.ids.size} 题</span></button>`).join('');
  }
  function renderHeader() {
    $$('.nav-item').forEach(b=>{const selected=b.dataset.view===view;b.classList.toggle('active',selected);b.setAttribute('aria-current',selected?'page':'false');});
    $('#breadcrumb').textContent=viewNames[view];
    const titles={topics:['THE TOPIC WORKBOOK · 数学二','一道一道，<em>突破薄弱点。</em>','把历年真题按知识点重新排列。从一个专题开始，把一类题真正练透。'],years:['THE PAST PAPERS · 数学二','回到真题，<em>检验每一步。</em>','2007—2026 年真题按年收录。可以顺序练习，也可以回到专题，串联同一类考点。'],wrong:['THE REVIEW NOTEBOOK · 数学二','做错的题，<em>值得再做一遍。</em>','错题会保留在这里。即使已经掌握，也能通过筛选回顾，看看自己是怎样走过来的。'],favorites:['YOUR PERSONAL COLLECTION · 数学二','值得回看的题，<em>留在这里。</em>','收藏有启发的解法、值得二刷的题目。下一次复习，从自己的题单开始。'],history:['YOUR LEARNING JOURNEY · 数学二','看见积累，<em>继续向前。</em>','每一次作答、每一段思考，都是进步的依据。学习数据仅存储在当前浏览器。']};
    const h=titles[view];$('#eyebrow').textContent=h[0];$('#page-title').innerHTML=h[1];$('#page-description').textContent=h[2];
    $('#primary-action').innerHTML=view==='wrong'?'开始错题复习 <span>↗</span>':view==='favorites'?'练习收藏题目 <span>↗</span>':db.lastId&&questionMap.has(db.lastId)?'继续上次练习 <span>↗</span>':'开始专题练习 <span>↗</span>';
    $('#weak-section').hidden=view!=='topics';$('#library-section').hidden=view==='history';$('#history-section').hidden=view!=='history';
    $('#library-kicker').textContent={topics:'TOPIC LIBRARY',years:'YEAR BY YEAR',wrong:'REVIEW & REVISIT',favorites:'MY COLLECTION'}[view]||'TOPIC LIBRARY';
    const title={topics:listMode?(filters.topic||filters.weak||'专题题目'):'按专题，系统练习',years:listMode?`${filters.from===filters.to?filters.from+' 年':'历年'}数学二真题`:'二十年真题，逐年练习',wrong:'我的错题本',favorites:'我的收藏'}[view];
    const matched=qsByFilters();
    $('#library-title').innerHTML=`${esc(title||'专题题目')} <span>${matched.length} 题</span>`;
    $('#overview-button').hidden=!(listMode && ['topics','years'].includes(view));
    $('#overview-button').textContent=view==='years'?'← 返回年份':'← 返回专题';
  }
  function renderTabs() {
    const base=qsByFilters(true);
    $('#subject-tabs').innerHTML=['','高等数学','线性代数'].map(s=>`<button class="subject-tab${filters.subject===s?' active':''}" data-subject="${esc(s)}" aria-pressed="${filters.subject===s}">${s||'全部学科'}<span>${base.filter(q=>!s||q.subject===s).length}</span></button>`).join('');
  }
  function renderActiveFilters() {
    const labels=[];
    for(const [field,label] of [['subject','学科'],['chapter','章节'],['topic','专题'],['type','题型'],['status','状态'],['search','搜索'],['weak','重点']]){
      const value=filters[field];if(!value)continue;
      const text=field==='type'?typeNames[value]:field==='status'?{unseen:'尚未练习',review:'待复习',mastered:'已掌握',attempted:'已练习'}[value]:value;
      labels.push(`<button class="filter-pill" data-remove-filter="${field}" aria-label="移除${esc(label)}筛选">${esc(text)} <span>×</span></button>`);
    }
    const min=Math.min(...questions.map(q=>q.year)),max=Math.max(...questions.map(q=>q.year));
    if(filters.from!==min || filters.to!==max) labels.push(`<button class="filter-pill" data-remove-filter="years">${filters.from}—${filters.to}<span>×</span></button>`);
    $('#active-filters').hidden=!labels.length;$('#active-filters').innerHTML=labels.join('');
  }
  function counts(list) { return ['single','fill','solution'].map(t=>`${typeNames[t].replace('题','')} ${list.filter(q=>q.type===t).length}`).join(' · '); }
  function masteredCount(list) { return list.filter(q=>status(q.id)==='mastered').length; }
  function empty(title,description,action='reset-filters',button='重置筛选') { return `<div class="empty-state"><span>∅</span><h3>${esc(title)}</h3><p>${esc(description)}</p><button class="button outline" data-action="${action}">${esc(button)}</button></div>`; }
  function renderTopics(list) {
    const groups=new Map();
    list.forEach(q=>{const k=`${q.subject}/${q.chapter}`;if(!groups.has(k))groups.set(k,{subject:q.subject,chapter:q.chapter,questions:[]});groups.get(k).questions.push(q);});
    const symbols=['lim','ƒ′','∫','∂','y′','|A|','A','α','Ax','λ','Q'];
    $('#library-body').innerHTML=[...groups.values()].sort((a,b)=>(a.subject==='高等数学'?0:1)-(b.subject==='高等数学'?0:1)||chapterRank(a.chapter)-chapterRank(b.chapter)).map((g,index)=>{
      const topics=unique(g.questions.map(q=>q.topic));
      return `<section class="chapter-group"><div class="chapter-heading"><span class="chapter-index">${String(index+1).padStart(2,'0')}</span><h3>${esc(g.chapter)}</h3><span>${esc(g.subject)} · ${g.questions.length} 题</span></div><div class="topic-grid">${topics.map(topic=>{const items=g.questions.filter(q=>q.topic===topic),done=masteredCount(items);return `<button class="topic-card" data-topic="${esc(topic)}" data-chapter="${esc(g.chapter)}" data-subject="${esc(g.subject)}"><div class="topic-card-top"><span class="topic-symbol">${symbols[chapterRank(g.chapter)]||'ƒ'}</span><span>${items.length} 道真题</span></div><h3>${esc(topic)}</h3><p>${counts(items)}</p><div class="topic-card-bottom"><span>${done?`已掌握 ${done} / ${items.length}`:'尚未开始 · 从这里出发'}</span><b>↗</b></div><div class="mini-progress"><span style="width:${done/items.length*100}%"></span></div></button>`;}).join('')}</div></section>`;
    }).join('') || empty('还没有匹配的专题','试试减少筛选条件，或换一个关键词。');
  }
  function renderYears(list) {
    const years=unique(list.map(q=>q.year)).sort((a,b)=>b-a);
    $('#library-body').innerHTML=`<div class="year-grid">${years.map(year=>{const items=list.filter(q=>q.year===year),done=masteredCount(items);return `<button class="year-card" data-year="${year}"><h3>${year}<span style="font:10px var(--sans);margin-left:6px;color:#a5af9c">年</span></h3><p>数学二 · ${items.length} 道真题</p><div class="year-note"><span>${done?`已掌握 ${done} / ${items.length}`:'开始这一年'}</span><span>↗</span></div><div class="mini-progress"><span style="width:${done/items.length*100}%"></span></div></button>`;}).join('')}</div>`;
    if(!years.length)$('#library-body').innerHTML=empty('没有找到符合条件的年份','请调整年份范围或其他筛选条件。');
  }
  function rowMarkup(q) {
    const r=db.records[q.id]||{},label=r.status==='mastered'?'已掌握':r.status==='review'?'待复习':'未练习';
    return `<button class="question-row" data-question="${esc(q.id)}"><span class="question-number">${q.year}<small>第 ${String(q.number).padStart(2,'0')} 题 · ${typeNames[q.type]}</small></span><span><span class="question-title">${esc(q.topic)}</span><span class="question-subtitle">${esc(q.chapter)}${q.tags.length?' · '+esc(q.tags.slice(0,2).join(' / ')):''}</span></span><span class="row-status">${r.favorite?'<span class="badge favorite" aria-label="已收藏">★</span>':''}<span class="badge ${esc(r.status||'')}">${label}</span></span><span class="question-row-arrow">↗</span></button>`;
  }
  function renderList(list) {
    const sortedList=sorted(list),size=30,max=Math.max(1,Math.ceil(list.length/size));page=Math.min(page,max);
    let note=`共 ${list.length} 题 · 点击题目开始练习`;
    if(view==='wrong')note=`保留错题历史 · 待复习 ${list.filter(q=>status(q.id)!=='mastered').length} / 已掌握 ${masteredCount(list)}`;
    $('#library-body').innerHTML=`<div class="list-toolbar"><span>${note}</span><div><select id="sort-select" class="sort-select" aria-label="题目排序">${option('new','年份：由近到远',sort)}${option('old','年份：由远到近',sort)}${option('number','按原卷题号',sort)}</select><button class="button small outline" data-action="practice-list"${!list.length?' disabled':''}>顺序练习 ↗</button></div></div><div class="question-list">${sortedList.slice((page-1)*size,page*size).map(rowMarkup).join('')}</div>`;
    if(!list.length){const messages=view==='wrong'?['错题本暂时是空的','答错的题和标记“还需复习”的题会自动进入这里。已掌握的错题仍会保留。']:view==='favorites'?['还没有收藏题目','在练习页点击“收藏”，把值得再做的题留下来。']:['没有匹配的题目','试试清除一项筛选，或者换一个更简短的关键词。'];$('#library-body').innerHTML=empty(messages[0],messages[1],view==='wrong'||view==='favorites'?'go-topics':'reset-filters',view==='wrong'||view==='favorites'?'去专题刷题':'重置筛选');}
    $('#pagination').hidden=max<=1;
    $('#pagination').innerHTML=`<button class="button small outline" data-page="${page-1}"${page<=1?' disabled':''}>← 上一页</button><span>${page} / ${max}</span><button class="button small outline" data-page="${page+1}"${page>=max?' disabled':''}>下一页 →</button>`;
  }
  function renderHistory() {
    const now=new Date(),today=db.days[dayKey()]||{},allSeconds=questions.reduce((sum,q)=>sum+(db.records[q.id]?.seconds||0),0),done=questions.filter(q=>attempted(q.id)).length;
    const days=Array.from({length:7},(_,i)=>{const d=new Date(now);d.setDate(d.getDate()-(6-i));const k=dayKey(d);return {key:k,label:i===6?'今天':`${d.getMonth()+1}/${d.getDate()}`,count:db.days[k]?.attempts||0};}),max=Math.max(1,...days.map(d=>d.count));
    const recent=[...db.activity].filter(a=>questionMap.has(a.id)).reverse().slice(0,12);
    $('#history-section').innerHTML=`<div class="history-header"><span class="section-kicker">YOUR PROGRESS</span><h2>每一次练习，都算数。</h2><p>自动核对与自评均会记录；练习次数可以包含同一道题的多次作答。</p></div><div class="history-grid"><div class="history-stat"><span>今日练习次数</span><strong>${today.attempts||0}</strong><small>已作答与自评</small></div><div class="history-stat"><span>累计练习题目</span><strong>${done}</strong><small>去重后的题目数</small></div><div class="history-stat"><span>累计专注时间</span><strong>${Math.floor(allSeconds/60)}<span style="font:10px var(--sans)"> 分</span></strong><small>阅读器打开并计时的时长</small></div></div><div class="activity-chart" aria-label="最近七天练习次数">${days.map(d=>`<div class="activity-day"><span>${d.count||''}</span><div class="bar" style="height:${Math.max(2,d.count/max*80)}px"></div><small>${d.label}</small></div>`).join('')}</div><div class="recent-list"><h3>最近的练习</h3>${recent.length?recent.map(a=>{const q=questionMap.get(a.id),d=new Date(a.at);return `<button class="recent-row" data-question="${esc(q.id)}"><span>${q.year} 年 · 第 ${q.number} 题 · ${esc(q.topic)}<small>${a.kind==='correct'?'选择题答对':a.kind==='wrong'?'选择题答错':a.kind==='mastered'?'自评：已经掌握':a.kind==='choice'?'已记录所选选项':'记录：还需复习'}</small></span><small>${Number.isNaN(d.getTime())?'':`${d.getMonth()+1}/${d.getDate()} ${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`} ↗</small></button>`;}).join(''):empty('先从一道题开始','提交答案或进行自评后，你的练习足迹会显示在这里。','go-topics','开始专题练习')}</div><div class="history-backup"><p>记录仅保存在当前浏览器。换设备或清理浏览器前，记得导出备份。</p><button class="button small outline" data-action="backup">备份与恢复 ↗</button></div>`;
  }
  function render() {
    if(!dataLoaded)return;
    renderStats();renderHeader();renderWeak();syncFilterControls();renderTabs();renderActiveFilters();
    $('#pagination').hidden=true;
    if(view==='history'){renderHistory();return;}
    const list=qsByFilters();
    if(view==='topics'&&!listMode)renderTopics(list);else if(view==='years'&&!listMode)renderYears(list);else renderList(list);
  }
  function resetFilters() { filters={subject:'',chapter:'',topic:'',type:'',from:Math.min(...questions.map(q=>q.year)),to:Math.max(...questions.map(q=>q.year)),status:'',search:'',weak:''};page=1; }
  function setView(next) { if(!viewNames[next])return;view=next;listMode=['wrong','favorites'].includes(view);resetFilters();render();history.replaceState(null,'',`#${next}`);window.scrollTo({top:0,behavior:'smooth'}); }
  function openQuestion(id,list) {
    if(!questionMap.has(id))return;
    const wasOpen=$('#reader').open;
    if(wasOpen)flushTime();else{readerReturnFocus=document.activeElement;sessionSeconds=0;}
    if(list)queue=list.map(q=>typeof q==='string'?q:q.id);
    if(!queue.includes(id))queue=[id];
    queueIndex=queue.indexOf(id);activeId=id;db.lastId=id;
    const q=questionMap.get(id),r=record(id);r.lastViewed=new Date().toISOString();saveDatabase(true);
    answerChoice='';checkedChoice='';zoom=100;
    $('#reader-title').textContent=`${q.year} 年 · 第 ${q.number} 题`;
    $('#reader-position').textContent=`${typeNames[q.type]} · ${queueIndex+1} / ${queue.length}`;
    $('#reader-tags').innerHTML=[q.subject,q.chapter,q.topic,...q.tags].filter((x,i,a)=>a.indexOf(x)===i).map(t=>`<span>${esc(t)}</span>`).join('');
    const note=$('#question-note-correction');note.hidden=!q.questionNote;note.textContent=q.questionNote||'';
    const img=$('#question-image');$('#image-error').hidden=true;img.hidden=false;img.style.width='100%';img.alt=`${q.year}年考研数学二第${q.number}题，${q.topic}。完整题面包含在原题图片中。`;img.src=safeAsset(q.image);$('#zoom-label').textContent='100%';
    $('#question-image-wrap').scrollLeft=0;$('#choice-area').hidden=q.type!=='single';
    $('#choice-buttons').innerHTML=['A','B','C','D'].map(c=>`<button class="choice-button" data-choice="${c}" aria-pressed="false">${c}</button>`).join('');
    $('#check-answer').disabled=true;$('#check-answer').textContent=/^[ABCD]$/.test(String(q.answer||'').trim().toUpperCase())?'提交并核对':'记录选择';$('#choice-feedback').textContent='';$('#choice-feedback').classList.remove('wrong');
    $('#answer-details').open=false;
    let answer='';
    if(q.answer!==null&&q.answer!==undefined&&String(q.answer).trim())answer+=`<div class="reference-answer">参考答案：${esc(q.answer)}</div>`;
    if(q.answerImage&&safeAsset(q.answerImage))answer+=`<img class="answer-image" src="${esc(safeAsset(q.answerImage))}" alt="${q.year}年数学二第${q.number}题参考答案图" loading="lazy"><p class="answer-image-fallback" hidden>答案图未加载成功，请查看下方讲解或原卷来源。</p>`;
    if(!answer)answer=q.proof?'<p>这是一道证明题，请对照讲解核查推导过程，再进行自评。</p>':'<p>这道题暂未收录可直接显示的参考答案，请查看讲解或原卷来源，再进行自评。</p>';
    if(q.answerImage||q.answer)answer+='<p>这里用于核对参考结果。完整解题过程请通过下方讲解或原卷来源查看。</p>';
    if(q.answerDerivation)answer+=`<div class="derivation-note"><h3>解题提示</h3><p>${esc(q.answerDerivation)}</p></div>`;
    if(q.answerNote)answer+=`<p class="source-warning">${esc(q.answerNote)}</p>`;
    if(q.sourceCorrection)answer+=`<p class="source-warning"><strong>来源勘误：</strong>${esc(q.sourceCorrection)}</p>`;
    answer+=`<div class="question-sources">${link(q.analysisUrl,'看讲解')}${link(q.sourceUrl,'原卷来源')}</div>`;
    $('#answer-content').innerHTML=answer;
    const answerImage=$('.answer-image');if(answerImage)answerImage.onerror=()=>{answerImage.hidden=true;$('.answer-image-fallback').hidden=false;};
    $('#question-note').value=r.note||'';$('#note-save-status').textContent='输入后自动保存到此浏览器';
    $('#question-sources').innerHTML=link(q.sourceUrl,'原卷来源')+link(q.analysisUrl,'看讲解')+(safeAsset(q.image)?`<a href="${esc(safeAsset(q.image))}" target="_blank" rel="noopener noreferrer">打开原题图片 ↗</a>`:'')+(q.verification?`<p>${esc(q.verification)}</p>`:'');
    $('#prev-question').disabled=queueIndex===0;$('#next-question').disabled=queueIndex===queue.length-1;
    updateReaderRecord();$('#reader-scroll')?.scrollTo({top:0});$('.reader-scroll').scrollTop=0;
    if(!wasOpen){$('#reader').showModal();document.body.style.overflow='hidden';$('#close-reader').focus();}
    startTimer();
  }
  function updateReaderRecord() {
    if(!activeId)return;const r=record(activeId);
    $('#favorite-question').textContent=r.favorite?'★ 已收藏':'☆ 收藏';$('#favorite-question').classList.toggle('selected',!!r.favorite);$('#favorite-question').setAttribute('aria-pressed',String(!!r.favorite));
    $('#wrong-question').textContent=r.everWrong?'↻ 已在错题本':'＋ 加入错题';$('#wrong-question').classList.toggle('selected',!!r.everWrong);
    $$('[data-grade]').forEach(b=>{b.classList.toggle('selected',r.status===b.dataset.grade);b.setAttribute('aria-pressed',String(r.status===b.dataset.grade));});
    $('#eval-status').textContent=r.status==='mastered'?(r.everWrong?'已掌握 · 仍保留在错题本中，可筛选回顾。':'已掌握 · 已更新练习进度。'):r.status==='review'?'待复习 · 已加入错题本，下次再挑战。':'尚未标记掌握状态。';
    $('#question-total-time').textContent=formatDuration(r.seconds||0);
    $('#question-history').innerHTML=r.attempts.length?`<h3>最近作答记录</h3>${r.attempts.slice(-3).reverse().map(a=>`<p>${esc(String(a.at||'').slice(0,10))} · ${a.result==='correct'?'答对':a.result==='wrong'?'答错':a.result==='mastered'?'自评已掌握':a.result==='choice'?'已记录选项':'标记待复习'}${a.choice?' · '+esc(a.choice):''}</p>`).join('')}`:'';
  }
  function logAttempt(kind,choice='') {
    if(!activeId)return;const r=record(activeId),at=new Date().toISOString();
    r.attempts.push({at,result:kind,...(choice?{choice}: {})});r.attempts=r.attempts.slice(-100);
    r.lastAttempt=at;
    if(kind==='wrong'||kind==='review'){r.status='review';r.everWrong=true;}else if(kind==='correct'||kind==='mastered')r.status='mastered';
    db.activity.push({id:activeId,at,kind});db.activity=db.activity.slice(-1000);
    const today=dayKey();if(!db.days[today])db.days[today]={attempts:0,seconds:0};db.days[today].attempts=(db.days[today].attempts||0)+1;
    saveDatabase();updateReaderRecord();renderStats();
  }
  function checkAnswer() {
    if(!answerChoice||!activeId||checkedChoice===answerChoice)return;
    const q=questionMap.get(activeId),a=String(q.answer||'').trim().toUpperCase();checkedChoice=answerChoice;
    if(/^[ABCD]$/.test(a)){const ok=answerChoice===a;logAttempt(ok?'correct':'wrong',answerChoice);$('#choice-feedback').textContent=ok?'答对了。已记录为掌握，也可以继续对照讲解检查思路。':`你选择了 ${answerChoice}，参考答案为 ${a}。已加入错题本，复习时再试一次。`;$('#choice-feedback').classList.toggle('wrong',!ok);$$('.choice-button').forEach(b=>{b.classList.toggle('correct',b.dataset.choice===a);b.classList.toggle('incorrect',b.dataset.choice===answerChoice&&!ok);});}
    else {logAttempt('choice',answerChoice);$('#choice-feedback').textContent=`已记录你的选择 ${answerChoice}。本题没有可自动核对的答案，请查看参考资料并自行标记。`;}
    $('#check-answer').disabled=true;
  }
  function formatDuration(seconds){const s=Math.max(0,Math.floor(seconds));return s<60?`${s} 秒`:`${Math.floor(s/60)} 分 ${s%60} 秒`;}
  function drawTimer(){const n=sessionSeconds+(timerRunning?Math.floor((Date.now()-timerStarted)/1000):0);$('#timer-value').textContent=`${String(Math.floor(n/60)).padStart(2,'0')}:${String(n%60).padStart(2,'0')}`;}
  function flushTime(){if(!timerRunning||!activeId)return;const elapsed=Math.max(0,Math.floor((Date.now()-timerStarted)/1000));timerStarted+=elapsed*1000;if(!elapsed)return;sessionSeconds+=elapsed;record(activeId).seconds+=elapsed;const today=dayKey();if(!db.days[today])db.days[today]={attempts:0,seconds:0};db.days[today].seconds=(db.days[today].seconds||0)+elapsed;saveDatabase(true);$('#question-total-time').textContent=formatDuration(record(activeId).seconds);}
  function startTimer(){if(!timerRunning){timerRunning=true;timerStarted=Date.now();}$('#timer-icon').textContent='Ⅱ';$('#timer-button').setAttribute('aria-label','暂停计时');drawTimer();}
  function pauseTimer(){flushTime();timerRunning=false;$('#timer-icon').textContent='▶';$('#timer-button').setAttribute('aria-label','继续计时');drawTimer();}
  function closeReader(){pauseTimer();clearTimeout(noteTimeout);saveNote();$('#reader').close();document.body.style.overflow='';activeId=null;render();if(readerReturnFocus?.isConnected)readerReturnFocus.focus();}
  function saveNote(){if(!activeId)return;record(activeId).note=$('#question-note').value;const ok=saveDatabase();$('#note-save-status').textContent=ok?'已自动保存到此浏览器':'未能保存，请复制笔记或导出备份';}
  function changeQuestion(offset){const index=queueIndex+offset;if(index<0||index>=queue.length)return;saveNote();openQuestion(queue[index]);}
  function randomQuestion(list){if(!list.length){toast('当前筛选下没有可练习的题目。');return;}const eligible=list.length>1?list.filter(q=>q.id!==activeId):list;openQuestion(eligible[Math.floor(Math.random()*eligible.length)].id,list);}
  function openInfo(title,html){$('#info-title').textContent=title;$('#info-content').innerHTML=html;$('#info-dialog').showModal();$('#close-info').focus();}
  function showBackup(){openInfo('给学习记录留一份备份',`<p>收藏、错题、笔记和练习进度只保存在<strong>当前浏览器</strong>，不会自动同步到其他设备。清理浏览器数据或更换浏览器可能丢失记录。</p><p>可以导出 JSON 文件，在另一台设备打开本网站后导入。导入会替换当前记录，请先保留备份。</p><div class="backup-actions"><button class="button primary" data-action="export">导出学习记录 ↓</button><button class="button outline" data-action="import">导入备份 ↑</button></div><p>目前记录：${questions.filter(q=>attempted(q.id)).length} 道已练题目 · ${questions.filter(q=>db.records[q.id]?.favorite).length} 道收藏。</p><div class="danger-section"><h3>重新开始</h3><p>清空会删除此浏览器中的全部学习记录，不会删除题库。建议先导出备份。</p><button class="button small danger-button" data-action="clear-records">清空本地学习记录</button></div>`);}
  function exportData(){flushTime();const blob=new Blob([JSON.stringify({app:'数二逐题',exportedAt:new Date().toISOString(),...db},null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=`数二逐题_学习记录_${dayKey()}.json`;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),10000);toast('备份已生成，请保存下载的 JSON 文件。');}
  function cleanImport(input){
    if(!input||input.version!==1||!input.records||typeof input.records!=='object'||Array.isArray(input.records))throw new Error('这不是可识别的数二逐题备份文件。');
    const clean=blankDb();
    for(const [id,value] of Object.entries(input.records)){if(!questionMap.has(id)||!value||typeof value!=='object')continue;clean.records[id]={status:['unseen','review','mastered'].includes(value.status)?value.status:'unseen',favorite:value.favorite===true,everWrong:value.everWrong===true,note:typeof value.note==='string'?value.note.slice(0,100000):'',seconds:Number.isFinite(value.seconds)?Math.max(0,Math.min(value.seconds,315360000)):0,attempts:Array.isArray(value.attempts)?value.attempts.filter(a=>a&&typeof a.at==='string'&&['correct','wrong','review','mastered','choice'].includes(a.result)).slice(-100).map(a=>({at:a.at.slice(0,35),result:a.result,...(/^[ABCD]$/.test(a.choice)?{choice:a.choice}:{})})):[],...(typeof value.lastViewed==='string'?{lastViewed:value.lastViewed.slice(0,35)}:{}),...(typeof value.lastAttempt==='string'?{lastAttempt:value.lastAttempt.slice(0,35)}:{})};}
    if(input.days&&typeof input.days==='object')for(const [day,v]of Object.entries(input.days)){if(/^\d{4}-\d{2}-\d{2}$/.test(day)&&v&&typeof v==='object')clean.days[day]={attempts:Number.isFinite(v.attempts)?Math.max(0,Math.min(Math.floor(v.attempts),100000)):0,seconds:Number.isFinite(v.seconds)?Math.max(0,Math.min(v.seconds,864000)):0};}
    if(Array.isArray(input.activity))clean.activity=input.activity.filter(a=>a&&questionMap.has(a.id)&&typeof a.at==='string'&&['correct','wrong','review','mastered','choice'].includes(a.kind)).slice(-1000).map(a=>({id:a.id,at:a.at.slice(0,35),kind:a.kind}));
    clean.lastId=questionMap.has(input.lastId)?input.lastId:null;return clean;
  }
  async function importData(file){if(!file)return;try{if(file.size>15000000)throw new Error('文件过大，请选择正常导出的 JSON 备份。');const imported=cleanImport(JSON.parse(await file.text()));if(!confirm(`已读取 ${Object.keys(imported.records).length} 道题的记录。导入将替换当前浏览器全部学习记录，确定继续？`))return;db=imported;saveDatabase();$('#info-dialog').close();render();toast('学习记录已恢复。');}catch(error){toast(error instanceof SyntaxError?'文件不是有效的 JSON，请检查备份文件。':error.message);}finally{$('#import-file').value='';}}
  function showSources(){const years=unique(questions.map(q=>q.year)).sort((a,b)=>a-b),sources=Array.isArray(meta.sources)?meta.sources:[];openInfo('题库说明与来源',`<p>数学二 · ${years[0]}—${years[years.length-1]} 年 · ${questions.length} 道原题 · ${unique(questions.map(q=>q.topic)).length} 个知识专题。</p><p>原题图按年份和原卷题号对应。按主考点分类，综合题可以跨越多个知识点；重点补弱入口依据专题标签匹配实际题目。</p><h3>答案与讲解</h3><p>仅对具有明确 A / B / C / D 参考答案的选择题自动核对。填空、计算和证明题使用参考结果或来源讲解辅助自评。参考结果不等同于完整解题步骤。</p>${meta.description?`<p>${esc(meta.description)}</p>`:''}${meta.notes?`<p>${esc(Array.isArray(meta.notes)?meta.notes.join('；'):meta.notes)}</p>`:''}<h3>公开来源</h3>${sources.length?`<ul>${sources.map(s=>`<li>${link(s.url,s.title||'题库来源')}${s.years?`<span> · ${esc(Array.isArray(s.years)?s.years.join('、'):s.years)}</span>`:''}${s.description?`<p>${esc(s.description)}</p>`:''}</li>`).join('')}</ul>`:'<p>每道题的练习页面都提供对应原卷来源，便于回查。</p>'}<p>本页不提供未收录题目的虚构答案。若参考答案与原卷资料存在差异，请回查来源。</p>`);}
  function handleAction(action){
    if(!dataLoaded&&action!=='retry')return;
    if(action==='retry'){location.reload();return;}
    if(action==='go-topics'){setView('topics');return;}
    if(action==='overview'){listMode=false;filters.topic='';filters.chapter='';filters.weak='';if(view==='years'){filters.from=Math.min(...questions.map(q=>q.year));filters.to=Math.max(...questions.map(q=>q.year));}page=1;render();return;}
    if(action==='reset-filters'){resetFilters();render();return;}
    if(action==='backup'){showBackup();return;}
    if(action==='sources'){showSources();return;}
    if(action==='export'){exportData();return;}
    if(action==='import'){$('#import-file').click();return;}
    if(action==='clear-records'){if(confirm('将清空本浏览器全部收藏、错题、笔记和学习记录。此操作不能撤销。已导出备份并确认清空吗？')){db=blankDb();saveDatabase();$('#info-dialog').close();render();toast('本地学习记录已清空。');}return;}
    if(action==='random'){randomQuestion(qsByFilters());return;}
    if(action==='practice-list'){const list=sorted(qsByFilters());if(list.length)openQuestion(list[0].id,list);return;}
    if(action==='start'){const list=sorted(qsByFilters());if(!list.length){toast('这里还没有可练习的题目，先去专题库看看。');return;}const last=list.find(q=>q.id===db.lastId),next=list.find(q=>status(q.id)!=='mastered')||list[0];openQuestion((last||next).id,list);}
  }
  document.addEventListener('click',event=>{
    const b=event.target.closest('button');if(!b||b.disabled)return;
    if(b.dataset.action){handleAction(b.dataset.action);return;}
    if(b.dataset.view){setView(b.dataset.view);return;}
    if(b.hasAttribute('data-topic')){filters.subject=b.dataset.subject;filters.chapter=b.dataset.chapter;filters.topic=b.dataset.topic;listMode=true;page=1;render();$('#library-section').scrollIntoView({behavior:'smooth',block:'start'});return;}
    if(b.hasAttribute('data-subject')){filters.subject=b.dataset.subject;filters.chapter='';filters.topic='';page=1;render();return;}
    if(b.dataset.weak){if(view!=='topics')view='topics';resetFilters();filters.weak=b.dataset.weak;listMode=true;render();$('#library-section').scrollIntoView({behavior:'smooth',block:'start'});return;}
    if(b.dataset.year){filters.from=Number(b.dataset.year);filters.to=Number(b.dataset.year);listMode=true;page=1;render();$('#library-section').scrollIntoView({behavior:'smooth',block:'start'});return;}
    if(b.dataset.question){const list=view==='history'?sorted(questions):sorted(qsByFilters());openQuestion(b.dataset.question,list);return;}
    if(b.dataset.page){page=Number(b.dataset.page);render();$('#library-section').scrollIntoView({behavior:'smooth',block:'start'});return;}
    if(b.dataset.removeFilter){const field=b.dataset.removeFilter;if(field==='years'){filters.from=Math.min(...questions.map(q=>q.year));filters.to=Math.max(...questions.map(q=>q.year));}else{filters[field]='';if(field==='subject'){filters.chapter='';filters.topic='';}if(field==='chapter')filters.topic='';}page=1;render();return;}
    if(b.dataset.choice){answerChoice=b.dataset.choice;checkedChoice='';$$('.choice-button').forEach(btn=>{const selected=btn.dataset.choice===answerChoice;btn.classList.toggle('selected',selected);btn.setAttribute('aria-pressed',String(selected));btn.classList.remove('correct','incorrect');});$('#check-answer').disabled=false;$('#choice-feedback').textContent='';return;}
    if(b.dataset.grade){logAttempt(b.dataset.grade);toast(b.dataset.grade==='mastered'?'已标记掌握。':'已加入待复习错题。');}
  });
  $('#toggle-filters').addEventListener('click',()=>{const panel=$('#filter-panel');panel.hidden=!panel.hidden;$('#toggle-filters').setAttribute('aria-expanded',String(!panel.hidden));});
  [['chapter-filter','chapter'],['topic-filter','topic'],['type-filter','type'],['year-from','from'],['year-to','to'],['status-filter','status']].forEach(([id,field])=>$('#'+id).addEventListener('change',event=>{filters[field]=field==='from'||field==='to'?Number(event.target.value):event.target.value;if(field==='chapter')filters.topic='';if(field==='from'&&filters.from>filters.to)filters.to=filters.from;if(field==='to'&&filters.to<filters.from)filters.from=filters.to;if(field==='topic'&&filters.topic)listMode=true;page=1;render();}));
  $('#search-filter').addEventListener('input',event=>{filters.search=event.target.value;page=1;render();});
  document.addEventListener('change',event=>{if(event.target.id==='sort-select'){sort=event.target.value;page=1;render();}});
  $('#close-reader').addEventListener('click',closeReader);
  $('#reader').addEventListener('cancel',event=>{event.preventDefault();closeReader();});
  $('#reader').addEventListener('click',event=>{if(event.target===$('#reader')){const r=$('#reader').getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)closeReader();}});
  $('#close-info').addEventListener('click',()=>$('#info-dialog').close());
  $('#check-answer').addEventListener('click',checkAnswer);
  $('#prev-question').addEventListener('click',()=>changeQuestion(-1));$('#next-question').addEventListener('click',()=>changeQuestion(1));
  $('#reader-random').addEventListener('click',()=>{saveNote();randomQuestion(queue.map(id=>questionMap.get(id)));});
  $('#timer-button').addEventListener('click',()=>timerRunning?pauseTimer():startTimer());
  $('#favorite-question').addEventListener('click',()=>{if(!activeId)return;const r=record(activeId);r.favorite=!r.favorite;saveDatabase();updateReaderRecord();renderStats();toast(r.favorite?'已收藏这道题。':'已取消收藏。');});
  $('#wrong-question').addEventListener('click',()=>{if(!activeId)return;if(record(activeId).everWrong){toast('错题历史会保留，可以通过“已经掌握”更新复习状态。');return;}logAttempt('review');toast('已加入错题本。');});
  $('#question-note').addEventListener('input',()=>{if(!activeId)return;record(activeId).note=$('#question-note').value;$('#note-save-status').textContent='正在保存…';clearTimeout(noteTimeout);noteTimeout=setTimeout(saveNote,450);});
  $('#question-note').addEventListener('blur',saveNote);
  function setZoom(value){zoom=Math.max(70,Math.min(240,value));$('#question-image').style.width=zoom+'%';$('#zoom-label').textContent=zoom+'%';}
  $('#zoom-in').addEventListener('click',()=>setZoom(zoom+20));$('#zoom-out').addEventListener('click',()=>setZoom(zoom-20));$('#zoom-fit').addEventListener('click',()=>setZoom(100));
  $('#question-image').addEventListener('error',()=>{if(!activeId)return;$('#question-image').hidden=true;$('#image-error').hidden=false;});
  $('#import-file').addEventListener('change',event=>importData(event.target.files[0]));
  let pausedByVisibility=false;
  document.addEventListener('visibilitychange',()=>{if(document.hidden){pausedByVisibility=timerRunning;pauseTimer();saveDatabase(true);}else if(pausedByVisibility&&$('#reader').open){pausedByVisibility=false;startTimer();}});
  window.addEventListener('pagehide',()=>{flushTime();saveNote();saveDatabase(true);});
  window.addEventListener('hashchange',()=>{const next=location.hash.slice(1);if(viewNames[next]&&next!==view)setView(next);});
  setInterval(()=>{if($('#reader').open)drawTimer();},1000);setInterval(()=>{if(timerRunning)flushTime();},15000);
  async function init(){
    $('#today-label').textContent=new Intl.DateTimeFormat('zh-CN',{month:'long',day:'numeric',weekday:'short'}).format(new Date());
    try{
      const [dataResult,metaResult]=await Promise.allSettled([fetch('data/questions.json').then(r=>{if(!r.ok)throw new Error(`HTTP ${r.status}`);return r.json();}),fetch('data/meta.json').then(r=>r.ok?r.json():{})]);
      if(dataResult.status==='rejected')throw dataResult.reason;
      const raw=dataResult.value;const array=Array.isArray(raw)?raw:raw.questions;
      if(!Array.isArray(array)||!array.length)throw new Error('题库数据为空');
      const seen=new Set();questions=array.filter(q=>q&&typeof q.id==='string'&&Number.isFinite(Number(q.year))&&Number.isFinite(Number(q.number))&&!seen.has(q.id)&&(seen.add(q.id),true)).map(q=>({...q,year:Number(q.year),number:Number(q.number),subject:q.subject||'高等数学',chapter:q.chapter||'待归类',topic:q.topic||'综合题',type:typeNames[q.type]?q.type:'solution',tags:Array.isArray(q.tags)?q.tags.filter(t=>typeof t==='string'):[]}));
      if(!questions.length)throw new Error('未找到有效题目');
      questionMap=new Map(questions.map(q=>[q.id,q]));meta=metaResult.status==='fulfilled'&&metaResult.value&&typeof metaResult.value==='object'?metaResult.value:{};
      weakGroups=weakDefinitions.map(([name,regex])=>({name,ids:new Set(questions.filter(q=>regex.test(searchable(q))).map(q=>q.id))})).filter(w=>w.ids.size);
      db=cleanImport(db);dataLoaded=true;view=viewNames[location.hash.slice(1)]?location.hash.slice(1):'topics';listMode=['wrong','favorites'].includes(view);resetFilters();$('#initial-state').hidden=true;$('#app-content').hidden=false;render();
    }catch(error){$('#initial-state').innerHTML=`<h1>题库暂时没有载入</h1><p>请刷新页面重试；如果仍无法加载，请检查网络连接。</p><button class="button primary" data-action="retry" style="margin-top:22px">重新载入</button>`;console.error('Question bank loading failed:',error);}
  }
  init();
})();
