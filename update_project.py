from pathlib import Path
import urllib.request
import json

# Выполнять после create_project.py. Координаты меток — проценты ширины/высоты
# именно приложенной картинки, ориентировочные, а не географические координаты.
DATA = '''01,101|Республика Адыгея|Южный|7,61
02,102,702|Республика Башкортостан|Приволжский|28,53
03,103|Республика Бурятия|Дальневосточный|57,79
04,104|Республика Алтай|Сибирский|43,78
05,105|Республика Дагестан|Северо-Кавказский|8,68
06,106|Республика Ингушетия|Северо-Кавказский|8,65
07,107|Кабардино-Балкарская Республика|Северо-Кавказский|7,64
08,108|Республика Калмыкия|Южный|10,58
09,109|Карачаево-Черкесская Республика|Северо-Кавказский|6,63
10,110|Республика Карелия|Северо-Западный|21,31
11,111|Республика Коми|Северо-Западный|36,40
12,112|Республика Марий Эл|Приволжский|26,45
13,113|Республика Мордовия|Приволжский|21,46
14,114|Республика Саха — Якутия|Дальневосточный|71,43
15,115|Республика Северная Осетия — Алания|Северо-Кавказский|8,66
16,116,716|Республика Татарстан|Приволжский|26,49
17,117|Республика Тыва|Сибирский|51,80
18,118|Удмуртская Республика|Приволжский|28,47
19,119|Республика Хакасия|Сибирский|45,76
20,95,195|Чеченская Республика|Северо-Кавказский|9,65
21,121|Чувашская Республика|Приволжский|24,47
22,122,222|Алтайский край|Сибирский|40,73
23,93,123,193,323|Краснодарский край|Южный|6,57
24,84,88,124,224|Красноярский край|Сибирский|54,53
25,125,725|Приморский край|Дальневосточный|87,78
26,126|Ставропольский край|Северо-Кавказский|8,62
27,127|Хабаровский край|Дальневосточный|85,58
28,128|Амурская область|Дальневосточный|75,70
29,129|Архангельская область|Северо-Западный|29,33
30,130|Астраханская область|Южный|12,60
31,131|Белгородская область|Центральный|13,47
32,132|Брянская область|Центральный|12,43
33,133|Владимирская область|Центральный|21,42
34,134|Волгоградская область|Южный|14,52
35,135|Вологодская область|Северо-Западный|26,38
36,136|Воронежская область|Центральный|15,47
37,137|Ивановская область|Центральный|22,40
38,138|Иркутская область|Сибирский|57,70
39,91,139|Калининградская область|Северо-Западный|9,36
40,140|Калужская область|Центральный|15,42
41,141|Камчатский край|Дальневосточный|92,42
42,142|Кемеровская область — Кузбасс|Сибирский|43,71
43,143|Кировская область|Приволжский|28,44
44,144|Костромская область|Центральный|24,41
45,145|Курганская область|Уральский|32,58
46,146|Курская область|Центральный|13,45
47,147|Ленинградская область|Северо-Западный|17,34
48,148|Липецкая область|Центральный|17,46
49,149|Магаданская область|Дальневосточный|83,34
50,90,150,190,250,550,750,790|Московская область|Центральный|18,41
51,151|Мурманская область|Северо-Западный|26,27
52,152,252|Нижегородская область|Приволжский|24,44
53,153|Новгородская область|Северо-Западный|17,37
54,154,754|Новосибирская область|Сибирский|39,69
55,155|Омская область|Сибирский|36,64
56,156|Оренбургская область|Приволжский|24,55
57,157|Орловская область|Центральный|15,44
58,158|Пензенская область|Приволжский|20,48
59,159|Пермский край|Приволжский|31,47
60|Псковская область|Северо-Западный|14,37
61,161,761|Ростовская область|Южный|10,52
62,162|Рязанская область|Центральный|18,44
63,163,763|Самарская область|Приволжский|24,52
64,164|Саратовская область|Приволжский|20,52
65,165|Сахалинская область|Дальневосточный|90,64
66,96,166,196|Свердловская область|Уральский|33,52
67,167|Смоленская область|Центральный|14,40
68,168|Тамбовская область|Центральный|18,47
69,169|Тверская область|Центральный|18,38
70,170|Томская область|Сибирский|42,65
71,171|Тульская область|Центральный|17,43
72,172|Тюменская область|Уральский|35,59
73,173|Ульяновская область|Приволжский|23,49
74,174,774|Челябинская область|Уральский|29,57
75,175|Забайкальский край|Дальневосточный|64,79
76,176|Ярославская область|Центральный|21,39
77,97,99,177,197,199,277,299,777,797,799,977|Москва|Центральный|18,40
78,98,178,198,778|Санкт-Петербург|Северо-Западный|16,34
79,179|Еврейская автономная область|Дальневосточный|82,73
80,180|Донецкая Народная Республика|Южный|7,50
81,181|Луганская Народная Республика|Южный|9,49
82,182|Республика Крым|Южный|3,49
83,183|Ненецкий автономный округ|Северо-Западный|41,34
84,184|Херсонская область|Южный|3,46
85,185|Запорожская область|Южный|5,48
86,186|Ханты-Мансийский автономный округ — Югра|Уральский|40,52
87,187|Чукотский автономный округ|Дальневосточный|84,20
89,189|Ямало-Ненецкий автономный округ|Уральский|45,43
92,192|Севастополь|Южный|2,50'''
regions=[]
for line in DATA.splitlines():
    codes,name,district,point=line.split('|')
    x,y=map(float,point.split(','))
    regions.append(dict(codes=codes.split(','),name=name,district=district,x=x,y=y))

assets=Path('app/src/main/assets')
assets.mkdir(parents=True,exist_ok=True)
images={
    'map.jpg':'https://unlimbot.hb.ru-msk.vkcloud-storage.ru/uploads/faec385f22ba45689b97297bc63ac35fce260da4d2695b00.jpg',
    'marker.png':'https://unlimbot.hb.ru-msk.vkcloud-storage.ru/uploads/86c97b9bda2f439cbaf115491c17db94698439a063a0d11a.png'
}
for name,url in images.items():
    target=assets/name
    if not target.exists():
        print('Downloading',name)
        urllib.request.urlretrieve(url,target)

java='''package com.example.numberchecks;
import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.graphics.Color;

public class MainActivity extends Activity {
    private WebView web;
    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        getWindow().setStatusBarColor(Color.rgb(17,21,28));
        getWindow().setNavigationBarColor(Color.rgb(17,21,28));
        web = new WebView(this);
        web.setBackgroundColor(Color.rgb(17,21,28));
        web.getSettings().setJavaScriptEnabled(true);
        web.getSettings().setDomStorageEnabled(true);
        web.getSettings().setAllowFileAccess(true);
        web.setWebViewClient(new WebViewClient());
        web.setOnApplyWindowInsetsListener((v, insets) -> {
            v.setPadding(insets.getSystemWindowInsetLeft(),
                insets.getSystemWindowInsetTop(), insets.getSystemWindowInsetRight(),
                insets.getSystemWindowInsetBottom());
            return insets.consumeSystemWindowInsets();
        });
        setContentView(web);
        web.requestApplyInsets();
        web.loadUrl("file:///android_asset/index.html");
    }
    @Override public void onBackPressed() {
        web.evaluateJavascript("closeMap()", result -> {
            if (!"true".equals(result)) MainActivity.super.onBackPressed();
        });
    }
}
'''
Path('app/src/main/java/com/example/numberchecks/MainActivity.java').write_text(java,encoding='utf-8')
manifest=Path('app/src/main/AndroidManifest.xml')
manifest.write_text(manifest.read_text().replace('Theme.Material.Light.NoActionBar','Theme.Material.NoActionBar').replace('Числа 001–999','Коллекция номеров'),encoding='utf-8')
gradle=Path('app/build.gradle.kts')
gradle.write_text(gradle.read_text().replace('versionCode = 1','versionCode = 2').replace('versionName = "1.0"','versionName = "2.0"'),encoding='utf-8')

html='''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#11151c;color:#edf2fa;font:16px sans-serif}header{position:sticky;top:0;background:#11151c;z-index:2;padding:14px 12px 8px;border-bottom:1px solid #343d4a}h1{font-size:23px;margin:0 0 12px}nav{display:flex;gap:6px}button,input{font:inherit}button{color:inherit;background:#252e3c;border:0;border-radius:10px;padding:12px}nav button{flex:1;padding:12px 2px}nav button.active{background:#365fa0}#count{color:#aebbd0;margin:12px 0 8px;line-height:1.5}#search{width:100%;background:#202735;color:white;border:1px solid #445167;border-radius:10px;padding:11px}main{padding:12px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}h2{font-size:18px;margin:12px 0}label.tile{background:#202735;border:1px solid #354055;border-radius:12px;min-height:68px;display:flex;align-items:center;justify-content:space-between;padding:12px;font-size:23px;user-select:none;-webkit-user-select:none;-webkit-touch-callout:none}label.tile.selected{background:#243e62;border-color:#6d9edd}input[type=checkbox]{width:24px;height:24px;accent-color:#89b8ff;flex-shrink:0}.region{touch-action:pan-y}.empty,.hint{color:#aebbd0;font-size:14px;line-height:1.5}.info{font-size:16px;background:#35445c;border-radius:50%;padding:4px 9px;margin-left:auto;margin-right:8px}dialog{width:96vw;max-width:850px;max-height:94vh;overflow:auto;background:#18202b;color:#edf2fa;border:1px solid #51627a;border-radius:14px;padding:14px}dialog::backdrop{background:#000b}#mapviewport{overflow:auto;max-height:52vh;background:white;border-radius:8px}#canvas{position:relative;width:100%;line-height:0}#mapimage{width:100%;display:block}#pin{position:absolute;width:30px;height:30px;object-fit:contain;transform:translate(-50%,-95%);filter:drop-shadow(0 0 2px white);pointer-events:none}#regionTitle{font-size:20px;margin:0 0 10px}#regionDescription{line-height:1.5}#choices button{margin:3px}#zoom{width:100%}.dialogtop{display:flex;align-items:start;justify-content:space-between;gap:8px}footer{margin:20px 0;color:#aebbd0;font-size:13px;line-height:1.5}
</style></head><body>
<header><h1>Коллекция номеров</h1><nav><button data-tab="numbers">Числа</button><button data-tab="letters">Буквы</button><button data-tab="regions">Регионы</button></nav><div id="count"></div><input id="search" type="search" placeholder="Поиск" aria-label="Поиск"></header>
<main id="content"></main>
<dialog id="mapdialog"><div class="dialogtop"><h2 id="regionTitle"></h2><button onclick="closeMap()" aria-label="Закрыть">✕</button></div><p id="regionDescription"></p><div id="choices"></div><p class="hint">Метка приблизительная. Увеличь карту ползунком, затем перемещай её пальцем.</p><label>Масштаб <input id="zoom" type="range" min="100" max="500" value="100" step="25"></label><div id="mapviewport"><div id="canvas"><img id="mapimage" src="map.jpg" alt="Карта регионов"><img id="pin" src="marker.png" alt="Метка выбранного региона"></div></div><p class="hint">Использована предоставленная пользователем карта. Изображение границ не определяет международно-правовой статус территорий.</p></dialog>
<script>
const REGIONS=__REGIONS__;
const $=id=>document.getElementById(id);
let saved={};try{saved=JSON.parse(localStorage.getItem('collection-v2')||'{}')}catch(e){}
let tab=localStorage.getItem('tab')||'numbers';if(!['numbers','letters','regions'].includes(tab))tab='numbers';
const alphabet=Array.from('АВЕКМНОРСТУХ');
const numbers=Array.from({length:999},(_,i)=>String(i+1).padStart(3,'0'));
const combos=[];for(const a of alphabet)for(const b of alphabet)for(const c of alphabet)combos.push(a+b+c);
const byCode={};REGIONS.forEach(r=>r.codes.forEach(c=>(byCode[c]??=[]).push(r)));
const codes=Object.keys(byCode).sort((a,b)=>Number(a)-Number(b));
const checked=(kind,text)=>saved[kind+':'+text]===true;
function total(kind,arr){return arr.filter(t=>checked(kind,t)).length}
function updateCount(){
 $('count').textContent=tab==='numbers'?`Числа: ${total('n',numbers)} / 999`:tab==='letters'?`Буквы: ${total('l',alphabet)} / 12 · Сочетания: ${total('c',combos)} / 1728`:`Коды: ${total('r',codes)} / ${codes.length}`;
}
function save(){try{localStorage.setItem('collection-v2',JSON.stringify(saved))}catch(e){alert('Не удалось сохранить отметки: проверь свободное место на телефоне.')}}
function section(title,arr,kind){
 const q=$('search').value.trim().toUpperCase();
 const filtered=arr.filter(t=>t.includes(q)||(kind==='r'&&byCode[t].some(r=>r.name.toUpperCase().includes(q))));
 if(!filtered.length)return;
 const heading=document.createElement('h2');heading.textContent=title;$('content').append(heading);
 const grid=document.createElement('div');grid.className='grid';$('content').append(grid);
 const fragment=document.createDocumentFragment();
 filtered.forEach(text=>{
  const label=document.createElement('label');label.className='tile'+(kind==='r'?' region':'')+(checked(kind,text)?' selected':'');
  const span=document.createElement('span');span.textContent=text;label.append(span);
  const box=document.createElement('input');box.type='checkbox';box.checked=checked(kind,text);box.setAttribute('aria-label',text);
  box.addEventListener('change',()=>{saved[kind+':'+text]=box.checked;label.classList.toggle('selected',box.checked);save();updateCount()});
  if(kind==='r'){
   // Кнопка информации также доступна без длительного нажатия.
   const info=document.createElement('button');info.className='info';info.textContent='i';info.setAttribute('aria-label','Информация о коде '+text);info.onclick=e=>{e.preventDefault();e.stopPropagation();showRegion(text)};label.append(info);
   let timer=null,held=false,startX=0,startY=0;
   const cancel=()=>{clearTimeout(timer);timer=null};
   label.addEventListener('pointerdown',e=>{if(e.target===info)return;held=false;startX=e.clientX;startY=e.clientY;timer=setTimeout(()=>{held=true;showRegion(text)},550)});
   label.addEventListener('pointermove',e=>{if(Math.abs(e.clientX-startX)+Math.abs(e.clientY-startY)>12)cancel()});
   label.addEventListener('pointerup',cancel);label.addEventListener('pointercancel',cancel);
   label.addEventListener('click',e=>{if(held){e.preventDefault();e.stopPropagation();held=false}},true);
   label.addEventListener('contextmenu',e=>e.preventDefault());
  }
  label.append(box);fragment.append(label);
 });grid.append(fragment);
}
function render(){
 document.querySelectorAll('nav button').forEach(b=>b.classList.toggle('active',b.dataset.tab===tab));
 $('content').replaceChildren();updateCount();
 $('search').placeholder=tab==='numbers'?'Найти число':tab==='letters'?'Найти букву или сочетание':'Код или название региона';
 if(tab==='numbers')section('Числа',numbers,'n');
 if(tab==='letters'){section('Отдельные буквы',alphabet,'l');section('Сочетания из трёх букв',combos,'c')}
 if(tab==='regions'){
  const hint=document.createElement('p');hint.className='hint';hint.textContent='Нажатие — отметка. Удержание или кнопка i — регион и карта. Коды взяты из твоего справочника: включены исторические и не подтверждённые как действующие.';$('content').append(hint);
  section('Автомобильные коды',codes,'r');
 }
 if(!$('content').querySelector('.grid')){const p=document.createElement('p');p.textContent='Ничего не найдено';$('content').append(p)}
}
const positions={};
document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>{positions[tab]=window.scrollY;tab=b.dataset.tab;localStorage.setItem('tab',tab);$('search').value='';render();window.scrollTo(0,positions[tab]||0)});
let searchTimer;$('search').oninput=()=>{clearTimeout(searchTimer);searchTimer=setTimeout(render,180)};
let activeRegion=null;
function placeRegion(code,r){
 activeRegion=r;$('regionTitle').textContent=code+' — '+r.name;
 $('regionDescription').textContent='Федеральный округ по справочнику: '+r.district+'. Коды: '+r.codes.join(', ')+(code==='84'?' · Код 84 имеет историческое и современное назначения; выбери нужное ниже.':'');
 $('pin').style.left=r.x+'%';$('pin').style.top=r.y+'%';$('zoom').value=100;$('canvas').style.width='100%';$('mapviewport').scrollTo(0,0);
}
function showRegion(code){
 const list=byCode[code];$('choices').replaceChildren();
 if(list.length>1)list.forEach(r=>{const b=document.createElement('button');b.textContent=r.name+(r.name==='Красноярский край'?' (84: бывший Таймырский АО)':'');b.onclick=()=>placeRegion(code,r);$('choices').append(b)});
 placeRegion(code,list[list.length-1]);if(!$('mapdialog').open)$('mapdialog').showModal();
}
function closeMap(){if($('mapdialog').open){$('mapdialog').close();return true}return false}
$('zoom').oninput=()=>{
 $('canvas').style.width=$('zoom').value+'%';
 requestAnimationFrame(()=>{const v=$('mapviewport'),c=$('canvas');if(activeRegion)v.scrollTo(c.clientWidth*activeRegion.x/100-v.clientWidth/2,c.clientHeight*activeRegion.y/100-v.clientHeight/2)});
};
render();
</script></body></html>'''
(assets/'index.html').write_text(html.replace('__REGIONS__',json.dumps(regions,ensure_ascii=False)),encoding='utf-8')
print('Version 2 generated: dark theme, letters, combinations, regions and offline map.')
