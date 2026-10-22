/* Pure functions shared by the desktop and Node's test runner. No network. */
export const STOP = new Set('a an and are as at be by can do does for from has have how i in is it of on or that the their this to was what when where which why will with you your'.split(' '));
export function terms(s) { return (s.toLowerCase().match(/[a-z0-9]+/g)||[]).filter(t=>t.length>1&&!STOP.has(t)); }
export function makeIndex(documents) {
  const chunks=[];
  for (const d of documents) for(let i=0;i<d.lines.length;i+=11){
    const text=d.lines.slice(i,i+14).join('\n'); const ts=terms(text), freq={};
    ts.forEach(t=>freq[t]=(freq[t]||0)+1);
    chunks.push({doc:d.id,revision:d.commit,path:d.path,text,start:i+1,end:Math.min(i+14,d.lines.length),freq,length:ts.length});
  }
  const df={};chunks.forEach(c=>Object.keys(c.freq).forEach(t=>df[t]=(df[t]||0)+1));
  return {chunks,df,avg:chunks.reduce((s,c)=>s+c.length,0)/Math.max(1,chunks.length)};
}
export function search(index,query,limit=5){
  const ts=[...new Set(terms(query))];if(!ts.length)return [];
  return index.chunks.map(c=>{let score=0,hits=0;for(const t of ts){const tf=c.freq[t]||0;if(tf){hits++;score+=Math.log(1+(index.chunks.length-(index.df[t]||0)+.5)/((index.df[t]||0)+.5))*tf*2.2/(tf+1.2*(.25+.75*c.length/Math.max(1,index.avg)));}}
    return {...c,score,coverage:hits/ts.length};}).filter(c=>c.score>0).sort((a,b)=>b.score-a.score||a.doc.localeCompare(b.doc)||a.start-b.start).slice(0,limit);
}
export function inspectCitation(c,documents){const d=documents.find(x=>x.id===c.doc);return !!d&&c.revision===d.commit&&Number.isInteger(c.start)&&c.start>0&&c.end>=c.start&&c.end<=d.lines.length&&d.lines.slice(c.start-1,c.end).join('\n')===c.text;}
export function criticize(hits,documents){
  const revisions=new Set(hits.map(x=>x.revision));
  return [
    {ok:hits.length>0,text:hits.length?'Source passages found in the pinned corpus.':'No source passage found. Abstain from an asserted answer.'},
    {ok:hits.length>0&&hits.every(c=>inspectCitation(c,documents)),text:'Check exact revision, line range, and quoted bytes.'},
    {ok:null,text:revisions.size>1?'Multiple revisions retrieved. A person must check whether they actually contradict.':'A single retrieved revision cannot establish agreement across all versions.'},
    {ok:null,text:'Keyword relevance is not entailment. Read the passages before accepting a claim.'},
    {ok:null,text:'This deterministic review does not measure the model critic in DEV2-001.'}
  ];
}
export function normalize(weights){if(!weights.length||weights.some(x=>!Number.isFinite(x)||x<0))throw Error('Weights must be finite and nonnegative.');const z=weights.reduce((a,b)=>a+b,0);if(!Number.isFinite(z)||z===0)return null;return weights.map(x=>x/z);}
export function posterior(weights,likelihoods){normalize(weights);if(weights.length!==likelihoods.length||likelihoods.some(x=>!Number.isFinite(x)||x<0||x>1))throw Error('One likelihood in [0,1] is needed for each possibility.');return normalize(weights.map((x,i)=>x*likelihoods[i]));}
export function entropy(p){return p===null?null:-p.reduce((s,x)=>s+(x>0?x*Math.log2(x):0),0);}
export function pairedSummary(bothFalse,improves,worsens,neither){
  const ns=[bothFalse,improves,worsens,neither];if(ns.some(x=>!Number.isInteger(x)||x<0)||ns.reduce((a,b)=>a+b,0)<2)throw Error('Use nonnegative integer counts and at least two paired items.');
  const n=ns.reduce((a,b)=>a+b,0),effect=(improves-worsens)/n;
  const variance=((improves+worsens)/n-effect*effect)*n/(n-1);
  const half=1.96*Math.sqrt(Math.max(0,variance)/n);
  return {n,effect,a:(bothFalse+improves)/n,c:(bothFalse+worsens)/n,interval:[Math.max(-1,effect-half),Math.min(1,effect+half)]};
}
export function budget(stages){if(stages.some(s=>!Number.isInteger(s.input)||!Number.isInteger(s.output)||s.input<0||s.output<0))throw Error('Token counts must be nonnegative integers.');return stages.reduce((s,x)=>({input:s.input+x.input,output:s.output+x.output,total:s.total+x.input+x.output}),{input:0,output:0,total:0});}
export function validateNotebook(obj){if(!obj||obj.format!=='devs2-notebook-v1'||!Array.isArray(obj.notes)||obj.notes.length>200)throw Error('Not a Devs 2.0 notebook (maximum 200 notes).');return obj.notes.map(n=>{if(!n||typeof n.text!=='string'||n.text.length>20000||typeof n.title!=='string'||n.title.length>300||typeof n.date!=='string')throw Error('Invalid note.');return {title:n.title,text:n.text,date:n.date};});}
