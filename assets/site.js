/* Metricmind - scripts partagés */
(function(){
  var y=document.getElementById('year');if(y)y.textContent=new Date().getFullYear();

  /* Menu mobile */
  var nav=document.querySelector('nav'),burger=document.querySelector('.nav-burger');
  if(burger)burger.addEventListener('click',function(){
    var o=nav.classList.toggle('open');burger.setAttribute('aria-expanded',o?'true':'false');
  });

  /* Lien actif */
  var path=location.pathname.replace(/\.html$/,'').replace(/\/$/,'')||'/';
  document.querySelectorAll('.nav-links a').forEach(function(a){
    var h=a.getAttribute('href').replace(/\.html$/,'').replace(/\/$/,'')||'/';
    if(h!=='/'&&path.indexOf(h)===0)a.classList.add('active');
  });

  /* CTA flottant : visible après 500px, masqué près du pied de page */
  var fc=document.querySelector('.float-cta'),foot=document.querySelector('footer');
  if(fc)window.addEventListener('scroll',function(){
    var nearEnd=foot&&(window.scrollY+window.innerHeight>foot.offsetTop-300);
    fc.classList.toggle('visible',window.scrollY>500&&!nearEnd);
  },{passive:true});

  /* Cartes études de cas */
  window.toggleCas=function(el,ev){
    if(ev&&ev.target&&ev.target.closest&&ev.target.closest('a'))return;
    var isOpen=el.classList.contains('open');
    document.querySelectorAll('.cas-card').forEach(function(c){
      c.classList.remove('open');c.setAttribute('aria-expanded','false');
      var b=c.querySelector('.cas-body');if(b)b.setAttribute('aria-hidden','true');
    });
    if(!isOpen){el.classList.add('open');el.setAttribute('aria-expanded','true');
      var b=el.querySelector('.cas-body');if(b)b.setAttribute('aria-hidden','false');}
  };

  /* Suivi des contacts */
  var cal=document.getElementById('calendly-link');
  if(cal)cal.addEventListener('click',function(){dataLayer.push({event:'generate_lead',lead_method:'calendly'});});
  document.querySelectorAll('[data-contact]').forEach(function(a){
    a.addEventListener('click',function(){dataLayer.push({event:'contact_click',contact_method:a.getAttribute('data-contact')});});
  });
  document.querySelectorAll('[data-lead]').forEach(function(a){
    a.addEventListener('click',function(){dataLayer.push({event:'cta_click',cta_location:a.getAttribute('data-lead')});});
  });

  /* Présélection du sujet via ?sujet= */
  var q=new URLSearchParams(location.search).get('sujet'),sel=document.getElementById('f-subject');
  if(q&&sel){for(var i=0;i<sel.options.length;i++){if(sel.options[i].text.toLowerCase().indexOf(q.toLowerCase())===0){sel.selectedIndex=i;break;}}}
})();

/* ---------- FORMULAIRE (Web3Forms) ---------- */
(function(){
  var f=document.getElementById('contact-form');if(!f)return;var _f=f,err=document.getElementById('form-error'),ok=document.getElementById('form-success');
  var btn=f.querySelector('button[type=submit]');
  function showErr(html){err.innerHTML=html;err.style.display='block';}
  var fallback=' Vous pouvez aussi m\'écrire directement à <a href="mailto:contact@metricmind.fr">contact@metricmind.fr</a>.';
  f.addEventListener('submit',function(e){
    e.preventDefault();err.style.display='none';
    if(!f.checkValidity()){showErr('Merci de renseigner votre nom, un email valide et votre message.');return;}
    if(f.botcheck.checked)return;
    if(f.access_key.value==='WEB3FORMS_ACCESS_KEY'){showErr('Le formulaire n\'est pas encore activé.'+fallback);return;}
    btn.disabled=true;btn.textContent='Envoi…';
    var data=Object.fromEntries(new FormData(f));
    data.subject='[metricmind.fr] '+data.subject;
    fetch(f.action,{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify(data)})
      .then(function(r){return r.text().then(function(t){var j;try{j=JSON.parse(t);}catch(e){j={success:false,message:'HTTP '+r.status};}return j;});})
      .then(function(j){
        if(!j.success)throw new Error(j.message||'erreur inconnue');
        dataLayer.push({event:'generate_lead',lead_method:'form',form_subject:f.subject.value});
        f.querySelectorAll('.form-row,.form-group,.form-note,button[type=submit]').forEach(function(n){n.style.display='none';});
        ok.style.display='block';
      })
      .catch(function(err){console.warn('[form] Web3Forms:',err&&err.message);showErr('L\'envoi n\'a pas abouti'+(err&&err.message?' ('+String(err.message).replace(/[<>&]/g,'')+')':'')+'.'+fallback);btn.disabled=false;btn.textContent='Envoyer le message →';});
  });
})();
