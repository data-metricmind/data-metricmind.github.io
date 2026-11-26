function toggleCas(el,ev){
  if(ev&&ev.target&&ev.target.closest&&ev.target.closest('a'))return;
  const isOpen=el.classList.contains('open');
  document.querySelectorAll('.cas-card').forEach(c=>{
    c.classList.remove('open');
    c.setAttribute('aria-expanded','false');
    const body=c.querySelector('.cas-body');
    if(body) body.setAttribute('aria-hidden','true');
  });
  if(!isOpen){
    el.classList.add('open');
    el.setAttribute('aria-expanded','true');
    const body=el.querySelector('.cas-body');
    if(body) body.setAttribute('aria-hidden','false');
  }
}

// Float CTA: show only after scrolling past hero
const floatCta=document.querySelector('.float-cta');
const heroSection=document.getElementById('hero');
const secs=document.querySelectorAll('section[id]');
const links=document.querySelectorAll('.nav-links a');

window.addEventListener('scroll',()=>{
  // Float CTA visibility
  const heroBottom=heroSection.offsetTop+heroSection.offsetHeight;
  const contactTop=document.getElementById('contact').offsetTop;
  if(window.scrollY>heroBottom-200&&window.scrollY+window.innerHeight<contactTop+200){
    floatCta.classList.add('visible');
  }else{
    floatCta.classList.remove('visible');
  }
  // Nav active section
  let cur='';
  secs.forEach(s=>{if(window.scrollY>=s.offsetTop-80)cur=s.id});
  links.forEach(a=>{
    a.classList.remove('active');
    if(a.getAttribute('href')==='#'+cur)a.classList.add('active');
  });
},{passive:true});

document.getElementById('year').textContent=new Date().getFullYear();

/* ---------- SUIVI DES CONTACTS ---------- */
document.getElementById('calendly-link').addEventListener('click',function(){
  dataLayer.push({event:'generate_lead',lead_method:'calendly'});
});
document.querySelectorAll('[data-contact]').forEach(function(a){
  a.addEventListener('click',function(){dataLayer.push({event:'contact_click',contact_method:a.getAttribute('data-contact')});});
});
/* Pré-sélection du sujet depuis un CTA */
document.querySelectorAll('[data-subject]').forEach(function(a){
  a.addEventListener('click',function(){var s=document.getElementById('f-subject');if(s)s.value=a.getAttribute('data-subject');});
});

(function(){var q=new URLSearchParams(location.search).get('sujet'),sel=document.getElementById('f-subject');
  if(q&&sel){for(var i=0;i<sel.options.length;i++){if(sel.options[i].text.toLowerCase().indexOf(q.toLowerCase())===0){sel.selectedIndex=i;break;}}}})();

/* ---------- FORMULAIRE (Web3Forms) ---------- */
(function(){
  var f=document.getElementById('contact-form'),err=document.getElementById('form-error'),ok=document.getElementById('form-success');
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
