/* Lumen — local interaction only. No requests, cookies or persistent storage. */
(() => {
  'use strict';
  const navToggle = document.querySelector('[data-menu-toggle]');
  const navMenu = document.querySelector('[data-nav-menu]');
  if (navToggle && navMenu) {
    function setMenu(open) { navToggle.setAttribute('aria-expanded', String(open)); navMenu.classList.toggle('is-open', open); navToggle.textContent = open ? 'Close ✕' : 'Menu ☰'; }
    navToggle.addEventListener('click', () => setMenu(navToggle.getAttribute('aria-expanded') !== 'true'));
    navMenu.addEventListener('click', event => { if (event.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', event => { if (event.key === 'Escape') setMenu(false); });
  }

  const atlas = document.querySelector('[data-atlas]');
  if (atlas) {
    const tabs = [...atlas.querySelectorAll('[data-atlas-tab]')];
    const kicker = atlas.querySelector('[data-atlas-kicker]');
    const title = atlas.querySelector('[data-atlas-title]');
    const desc = atlas.querySelector('[data-atlas-desc]');
    const svg = atlas.querySelector('.atlas-svg');
    const route = atlas.querySelector('[data-atlas-path]');
    const sets = [
      { kicker:'01 / DATA EXPLORATION', title:'Find the signal.', desc:'From raw data to useful patterns: cleaned, measured, explained.', path:'M24 194 C73 174 93 141 127 150 S198 90 234 101 S314 71 365 42' },
      { kicker:'02 / MODEL THINKING', title:'Measure the model.', desc:'Evaluation and clarity matter as much as any headline metric.', path:'M24 185 C68 187 95 159 127 158 S194 124 234 130 S301 55 365 68' },
      { kicker:'03 / DEVELOPER TOOLS', title:'Build the workflow.', desc:'Open tools for smoother, local-first coding and debugging.', path:'M24 200 C66 199 83 105 127 115 S179 166 234 101 S300 88 365 30' }
    ];
    function activate(i) {
      tabs.forEach((tab,j) => tab.setAttribute('aria-pressed',String(i===j)));
      svg.classList.add('is-shifting');
      kicker.textContent=sets[i].kicker; title.textContent=sets[i].title; desc.textContent=sets[i].desc;
      route.setAttribute('d',sets[i].path);
      window.setTimeout(() => svg.classList.remove('is-shifting'), 130);
    }
    tabs.forEach((tab,i) => tab.addEventListener('click', () => activate(i)));
  }

  const skills = document.querySelector('[data-skill-switcher]');
  if (skills) {
    const buttons = [...skills.querySelectorAll('[data-skill-button]')];
    const title = skills.querySelector('[data-skill-title]');
    const description = skills.querySelector('[data-skill-description]');
    const cloud = skills.querySelector('[data-skill-cloud]');
    const content = [
      {title:'Exploring and explaining data',description:'Structured analysis, decision-focused visualizations, and reproducible data workflows.',tags:['Python','Pandas','NumPy','SQL / MySQL','Power BI','DAX','Excel','ETL','Data cleaning']},
      {title:'Making models interpretable',description:'From classical machine learning to natural language and vision experiments, with evaluation in focus.',tags:['Scikit-learn','Classification','Regression','TensorFlow / Keras','NLP','TF-IDF','Model validation','Feature engineering']},
      {title:'Tools for people who build',description:'Open-source extensions and developer workflows for notebooks, execution, and debugging.',tags:['JavaScript','TypeScript','JupyterLab','Panic Nova','debugpy','Git / GitHub','Python','Notebook UX']},
      {title:'Thinking beyond the code',description:'Problem framing, careful communication, documentation, and transparent reasoning.',tags:['Root-cause analysis','Data storytelling','Business insights','Documentation','Stakeholder reporting','Privacy by design','Model evaluation']}
    ];
    const update = index => {
      buttons.forEach((button,j) => { button.setAttribute('aria-selected',String(index===j)); button.tabIndex=index===j?0:-1; });
      title.textContent = content[index].title; description.textContent = content[index].description;
      cloud.replaceChildren(...content[index].tags.map(tag => {const item=document.createElement('span');item.className='skill-chip';item.textContent=tag;return item;}));
    };
    buttons.forEach((button,i) => {
      button.addEventListener('click',() => update(i));
      button.addEventListener('keydown',e => { if(e.key!=='ArrowDown'&&e.key!=='ArrowRight'&&e.key!=='ArrowUp'&&e.key!=='ArrowLeft')return; e.preventDefault(); const dir=(e.key==='ArrowDown'||e.key==='ArrowRight')?1:-1;const next=(i+dir+buttons.length)%buttons.length;update(next);buttons[next].focus(); });
    });
  }

  const explorer = document.querySelector('[data-project-library]');
  if (explorer) {
    const filterButtons=[...explorer.querySelectorAll('[data-filter]')];
    const search=explorer.querySelector('[data-search]');
    const cards=[...explorer.querySelectorAll('[data-project-card]')];
    const status=explorer.querySelector('[data-result-count]');
    const empty=explorer.querySelector('[data-empty]');
    let active='All';
    function update() {
      const query=search.value.trim().toLocaleLowerCase();let count=0;
      cards.forEach(card => {const show=(active==='All'||card.dataset.group===active) && (!query||card.dataset.search.includes(query));card.hidden=!show;if(show) count++;});
      filterButtons.forEach(btn => btn.setAttribute('aria-pressed',String(btn.dataset.filter===active)));
      status.textContent=`${count} ${count===1?'project':'projects'} shown`;
      empty.style.display=count===0?'block':'none';
    }
    filterButtons.forEach(btn=>btn.addEventListener('click',()=>{active=btn.dataset.filter;update();}));
    search.addEventListener('input',update);
    update();
  }

  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const elements=[...document.querySelectorAll('.reveal')];
    if (elements.length) {
      const observer=new IntersectionObserver(entries => { entries.forEach(entry => { if(entry.isIntersecting) {entry.target.classList.add('show');observer.unobserve(entry.target);} }); },{threshold:.10});
      document.documentElement.classList.add('reveal-ready');
      elements.forEach(el=>observer.observe(el));
    }
  }
})();
