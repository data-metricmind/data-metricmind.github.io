/* Metricmind — bandeau cookies custom + Consent Mode v2 (partagé par toutes les pages).
   Les défauts consent + GTM sont déclarés inline dans le <head> de chaque page. */
(function(){
  var MAX_AGE=60*60*24*182; // ~6 mois
  var css='.cc{position:fixed;left:1.2rem;bottom:1.2rem;z-index:200;max-width:440px;background:#161616;border:1px solid #323232;border-radius:14px;padding:1.4rem 1.5rem;box-shadow:0 16px 48px rgba(0,0,0,.55);display:none;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#F2EFE9}'
  +'.cc.show{display:block}.cc-t{font-family:Georgia,serif;font-size:1.05rem;margin-bottom:.5rem}'
  +'.cc-d{font-size:.8rem;color:#B8B3AA;line-height:1.6;margin:0 0 1rem}.cc-d a{color:#F2EFE9}'
  +'.cc-btns{display:flex;gap:.6rem;flex-wrap:wrap}'
  +'.cc-btn{flex:1 1 auto;font:700 .78rem -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;padding:.6rem 1rem;border-radius:100px;cursor:pointer;border:1px solid #323232;background:#101010;color:#F2EFE9}'
  +'.cc-btn:hover{border-color:#928E87}.cc-btn:focus-visible{outline:2px solid #5B8DF8;outline-offset:3px}'
  +'.cc-btn.link{flex:0 0 auto;background:none;border-color:transparent;color:#B8B3AA;text-decoration:underline;padding-left:.4rem;padding-right:.4rem}'
  +'.cc-prefs{display:none;margin:0 0 1rem;border-top:1px solid #272727;padding-top:.8rem}.cc.custom .cc-prefs{display:block}'
  +'.cc-opt{display:flex;justify-content:space-between;gap:1rem;align-items:flex-start;padding:.55rem 0;font-size:.8rem;color:#B8B3AA;cursor:pointer}'
  +'.cc-opt strong{display:block;color:#F2EFE9;font-size:.82rem}.cc-opt input{margin-top:.2rem;width:18px;height:18px;accent-color:#5B8DF8;flex-shrink:0}'
  +'.cc-save{display:none}.cc.custom .cc-save{display:block}.cc.custom .cc-custom-btn{display:none}'
  +'body.cc-open .float-cta{display:none!important}'
  +'@media(max-width:900px){.cc{left:.8rem;right:.8rem;bottom:.8rem;max-width:none}}';
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
    var cc=document.createElement('div');cc.className='cc';cc.id='cc';
    cc.setAttribute('role','dialog');cc.setAttribute('aria-labelledby','cc-title');cc.setAttribute('aria-describedby','cc-desc');
    cc.innerHTML=html;document.body.appendChild(cc);
    var ca=cc.querySelector('#cc-a'),cm=cc.querySelector('#cc-m');
    function open(custom){
      var s=window.mmConsentSaved;ca.checked=!!(s&&s.a);cm.checked=!!(s&&s.m);
      cc.classList.toggle('custom',!!custom);cc.classList.add('show');document.body.classList.add('cc-open');
      if(custom)ca.focus({preventScroll:true});
    }
    function close(){cc.classList.remove('show','custom');document.body.classList.remove('cc-open');}
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
