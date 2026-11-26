/* Metricmind — bandeau cookies custom + Consent Mode v2 (partagé par toutes les pages).
   Les défauts consent + GTM sont déclarés inline dans le <head> de chaque page. */
(function(){
  var MAX_AGE=60*60*24*182; // ~6 mois
  var css='.cc-ov{position:fixed;inset:0;z-index:199;background:rgba(0,0,0,.62);backdrop-filter:blur(3px);-webkit-backdrop-filter:blur(3px);display:none}'
  +'.cc-ov.show{display:block}'
  +'.cc{position:fixed;left:50%;top:50%;transform:translate(-50%,-50%);z-index:200;width:min(480px,calc(100% - 2rem));background:#F2EFE9;border-radius:16px;padding:1.6rem 1.6rem 1.4rem;box-shadow:0 24px 80px rgba(0,0,0,.6);display:none;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#111827}'
  +'.cc.show{display:block}.cc-t{font-family:Georgia,serif;font-size:1.25rem;margin-bottom:.6rem;color:#080808}'
  +'.cc-d{font-size:.84rem;color:#4B4F58;line-height:1.6;margin:0 0 1.1rem}.cc-d a{color:#2F5FD0}'
  +'.cc-btns{display:flex;gap:.6rem;flex-wrap:wrap}'
  +'.cc-btn{flex:1 1 40%;font:700 .82rem -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;padding:.75rem 1rem;border-radius:100px;cursor:pointer;border:1px solid #080808;background:#080808;color:#F2EFE9}'
  +'.cc-btn:hover{background:#262626}.cc-btn:focus-visible{outline:2px solid #5B8DF8;outline-offset:3px}'
  +'.cc-btn.link{flex:1 1 100%;background:none;border-color:transparent;color:#4B4F58;text-decoration:underline;padding:.4rem}'
  +'.cc-btn.link:hover{background:none;color:#080808}'
  +'.cc-prefs{display:none;margin:0 0 1rem;border-top:1px solid #D9D5CC;padding-top:.8rem}.cc.custom .cc-prefs{display:block}'
  +'.cc-opt{display:flex;justify-content:space-between;gap:1rem;align-items:flex-start;padding:.55rem 0;font-size:.82rem;color:#4B4F58;cursor:pointer}'
  +'.cc-opt strong{display:block;color:#080808;font-size:.86rem}.cc-opt input{margin-top:.2rem;width:18px;height:18px;accent-color:#2F5FD0;flex-shrink:0}'
  +'.cc-save{display:none}.cc.custom .cc-save{display:block;flex:1 1 100%}.cc.custom .cc-custom-btn{display:none}'
  +'body.cc-open{overflow:hidden}body.cc-open .float-cta{display:none!important}'
  +'@media(max-width:600px){.cc{left:0;right:0;top:auto;bottom:0;transform:none;width:auto;border-radius:18px 18px 0 0;padding:1.5rem 1.3rem calc(1.3rem + env(safe-area-inset-bottom))}}';
  var html='<div class="cc-t" id="cc-title">Vos choix de cookies</div>'
  +'<p class="cc-d" id="cc-desc">J\'utilise des cookies de mesure d\'audience pour comprendre comment le site est utilisé et l\'améliorer. Rien n\'est déposé sans votre accord, et vous pouvez changer d\'avis à tout moment. <a href="/mentions-legales.html#cookies">Détails</a></p>'
  +'<div class="cc-prefs">'
  +'<label class="cc-opt"><span><strong>Mesure d\'audience</strong>Statistiques de visite et d\'usage (Google Analytics, Microsoft Clarity).</span><input type="checkbox" id="cc-a"></label>'
  +'<label class="cc-opt"><span><strong>Marketing</strong>Mesure des campagnes publicitaires (Google Ads, LinkedIn).</span><input type="checkbox" id="cc-m"></label>'
  +'</div><div class="cc-btns">'
  +'<button type="button" class="cc-btn" data-cc="refuse">Tout refuser</button>'
  +'<button type="button" class="cc-btn" data-cc="accept">Tout accepter</button>'
  +'<button type="button" class="cc-btn cc-save" data-cc="save">Enregistrer</button>'
  +'<button type="button" class="cc-btn link cc-custom-btn" data-cc="custom">Personnaliser</button>'
  +'</div>';
  function init(){
    var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
    var ov=document.createElement('div');ov.className='cc-ov';ov.setAttribute('aria-hidden','true');document.body.appendChild(ov);
    var cc=document.createElement('div');cc.className='cc';cc.id='cc';cc.setAttribute('aria-modal','true');
    cc.setAttribute('role','dialog');cc.setAttribute('aria-labelledby','cc-title');cc.setAttribute('aria-describedby','cc-desc');
    cc.innerHTML=html;document.body.appendChild(cc);
    var ca=cc.querySelector('#cc-a'),cm=cc.querySelector('#cc-m');
    function open(custom){
      var s=window.mmConsentSaved;ca.checked=!!(s&&s.a);cm.checked=!!(s&&s.m);
      cc.classList.toggle('custom',!!custom);cc.classList.add('show');ov.classList.add('show');document.body.classList.add('cc-open');
      if(custom)ca.focus({preventScroll:true});
    }
    function close(){cc.classList.remove('show','custom');ov.classList.remove('show');document.body.classList.remove('cc-open');}
    function apply(a,m){
      var v={a:!!a,m:!!m,v:1,ts:Date.now()};
      document.cookie='mm_consent='+encodeURIComponent(JSON.stringify(v))+';max-age='+MAX_AGE+';path=/;SameSite=Lax'+(location.protocol==='https:'?';Secure':'');
      window.mmConsentSaved=v;
      var mk=m?'granted':'denied';
      window.gtag('consent','update',{analytics_storage:a?'granted':'denied',ad_storage:mk,ad_user_data:mk,ad_personalization:mk});
      window.dataLayer.push({event:'consent_update',consent_analytics:a?'granted':'denied',consent_marketing:mk});
      close();
    }
    cc.addEventListener('click',function(e){
      var act=e.target.getAttribute&&e.target.getAttribute('data-cc');if(!act)return;
      if(act==='accept')apply(true,true);else if(act==='refuse')apply(false,false);
      else if(act==='save')apply(ca.checked,cm.checked);else if(act==='custom')open(true);
    });
    document.querySelectorAll('[data-cc-open]').forEach(function(b){b.addEventListener('click',function(e){e.preventDefault();open(true);});});
    window.mmOpenConsent=function(){open(true);};
    if(!window.mmConsentSaved)open(false);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
