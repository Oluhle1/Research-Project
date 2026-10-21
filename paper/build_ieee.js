// Build the review manuscript from portable, editable sources. No analysis is run.
const fs = require('fs');
const path = require('path');
const {Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
    AlignmentType, HeadingLevel, BorderStyle, WidthType, VerticalAlign,
    ImageRun, SectionType, TableLayoutType, LineRuleType} = require('docx');
const ROOT = __dirname;
const source = fs.readFileSync(path.join(ROOT, 'manuscript.md'), 'utf8');
const references = JSON.parse(fs.readFileSync(path.join(ROOT, 'references.json'), 'utf8'));
const FONT = 'Times New Roman';
const COLUMN = 5040;
const PAGE = {size:{width:12240,height:15840}, margin:{top:1080,bottom:1440,left:900,right:900}};
const ids=[];
// Source IDs remain stable across detailed working sections; output is IEEE first-use order.
const expanded = source.replace(/\[(\d+)\][–-]\[(\d+)\]/g, (_,a,b) => {
    const from=Number(a), to=Number(b);
    if(to<from) throw new Error('Reversed citation range');
    return Array.from({length:to-from+1},(_,i)=>`[${from+i}]`).join(', ');
});
for(const match of expanded.matchAll(/\[(\d+)\]/g)) {
    const id=Number(match[1]);
    if(!references[id]) throw new Error(`Missing reference ${id}`);
    if(!ids.includes(id)) ids.push(id);
}
const remapped=expanded.replace(/\[(\d+)\]/g,(_,id)=>`[${ids.indexOf(Number(id))+1}]`)
    .replace(/\[\d+\](?:, \[\d+\])+/g, group =>
      [...group.matchAll(/\d+/g)].map(m=>Number(m[0])).sort((a,b)=>a-b).map(n=>`[${n}]`).join(', '));
const lines=remapped.trim().split('\n');
function run(text, options={}){return new TextRun({text,font:FONT,size:20,...options});}
function paragraph(text,options={}){
    return new Paragraph({alignment:AlignmentType.JUSTIFIED,
      spacing:{before:0,after:60,line:230},...options,
      children:[run(text,options.run||{})]});
}
function heading(text,level){return paragraph(text,{
    heading:level===1?HeadingLevel.HEADING_1:HeadingLevel.HEADING_2,
    keepNext:true,alignment:level===1?AlignmentType.CENTER:AlignmentType.LEFT,
    spacing:{before:140,after:60,line:230},run:{size:20,bold:level===1,italics:level===2}});}
const rule={style:BorderStyle.SINGLE,size:4,color:'808080'};
function grid(headers,rows){
    const n=headers.length;
    const conceptual=headers[0]==='Predictor'&&headers[1]==='Theoretical role';
    const none={style:BorderStyle.NONE,size:0,color:'000000'};
    const horizontal={style:BorderStyle.SINGLE,size:6,color:'000000'};
    const widths = n===7?[540,760,650,650,700,900,840]:
                   n===6?[1040,850,700,700,900,850]:
                   headers[0]==='Predictor'?[900,1800,2340]:
                   headers[0]==='Study'?[1150,1570,2320]:
                   headers[0]==='Characteristic'?[2120,1460,1460]:
                   headers[0]==='Metric'?[2200,1200,1640]:
                   headers[0]==='Data concept'?[1450,1670,1920]:
                   headers[0]==='Evidence'?[1460,1480,2100]:[2940,1050,1050];
    if(widths.reduce((a,b)=>a+b,0)!==COLUMN) throw new Error('Bad table widths');
    return new Table({width:{size:COLUMN,type:WidthType.DXA},columnWidths:widths,
      layout:TableLayoutType.FIXED,
      ...(conceptual?{borders:{top:none,bottom:none,left:none,right:none,insideHorizontal:none,insideVertical:none}}:{}),
      rows:[headers,...rows].map((row,i)=>new TableRow({cantSplit:true,tableHeader:i===0,
        children:row.map((value,j)=>new TableCell({
          width:{size:widths[j],type:WidthType.DXA},verticalAlign:conceptual?VerticalAlign.TOP:VerticalAlign.CENTER,
          margins:{top:conceptual?50:40,bottom:conceptual?50:40,left:45,right:45},
          borders:conceptual?{top:i===0?horizontal:none,bottom:i===0||i===rows.length?horizontal:none,left:none,right:none}:
            {top:rule,bottom:rule,left:rule,right:rule},
          children:[paragraph(value,{keepNext:i<rows.length,alignment:j===0||n===3?AlignmentType.LEFT:AlignmentType.CENTER,
            spacing:{before:0,after:0,line:240,lineRule:LineRuleType.AUTO},run:{size:18,bold:i===0}})]}))}))});
}
const titleEnd=lines.findIndex(line=>line.startsWith('## '));
const title=[];
for(const line of lines.slice(0,titleEnd)){
    if(!line.trim()) continue;
    if(line.startsWith('# ')) title.push(paragraph(line.slice(2),{alignment:AlignmentType.CENTER,
      spacing:{before:0,after:160,line:260,lineRule:LineRuleType.AUTO},run:{size:48}}));
    else if(line.startsWith('Abstract—')||line.startsWith('Keywords—'))title.push(paragraph(line,{
      spacing:{before:80,after:80,line:220},run:{size:18}}));
    else title.push(paragraph(line,{alignment:AlignmentType.CENTER,
      spacing:{before:0,after:30,line:230},run:{size:line==='Oluhle Jawe'?22:18}}));
}
const body=[];
for(let i=titleEnd;i<lines.length;i++){
    const line=lines[i];if(!line.trim())continue;
    if(line.startsWith('## ')){body.push(heading(line.slice(3),1));continue;}
    if(line.startsWith('### ')){body.push(heading(line.slice(4),2));continue;}
    if(line.startsWith('TABLE: ')){
      body.push(paragraph(line.slice(7),{keepNext:true,alignment:AlignmentType.CENTER,
        spacing:{before:100,after:50,line:190},run:{size:16}}));
      const tableLines=[];
      while(i+1<lines.length&&lines[i+1].startsWith('|'))tableLines.push(lines[++i]);
      const cells=tableLines.map(s=>s.split('|').slice(1,-1).map(v=>v.trim()));
      if(!cells[1]||!cells[1].every(c=>/^:?-+:?$/.test(c.replace(/\s/g,''))))throw new Error('Table separator');
      body.push(grid(cells[0],cells.slice(2)));continue;
    }
    if(line.startsWith('FIGURE: ')){
      const [file,caption]=line.slice(8).split(' | ');
      body.push(new Paragraph({alignment:AlignmentType.CENTER,keepNext:true,
        spacing:{before:80,after:30,line:240,lineRule:LineRuleType.AUTO},children:[new ImageRun({type:'png',
          data:fs.readFileSync(path.join(ROOT,file)),
          transformation:{width:336,height:(()=>{
            const data=fs.readFileSync(path.join(ROOT,file));
            if(data.toString('ascii',1,4)!=='PNG')throw new Error('Figure must be PNG');
            return Math.round(336*data.readUInt32BE(20)/data.readUInt32BE(16));
          })()},
          altText:{name:caption,title:caption,description:caption}})]}));
      body.push(paragraph(caption,{spacing:{before:0,after:80,line:190},run:{size:16}}));continue;
    }
    if(line.startsWith('NOTE: ')){
      body.push(paragraph(line.slice(6),{spacing:{before:30,after:80,line:190},run:{size:16,italics:true}}));continue;
    }
    body.push(paragraph(line));
}
body.push(heading('References',1));
for(const [i,id] of ids.entries())body.push(paragraph(`[${i+1}] ${references[id]}`,{
    keepLines:true,alignment:AlignmentType.LEFT,indent:{left:260,hanging:260},spacing:{before:0,after:0,line:160},run:{size:16}}));
const doc=new Document({title:lines[0].slice(2),creator:'Oluhle Jawe',description:'Submission 2 revised research manuscript',
  styles:{default:{document:{run:{font:FONT,size:20},paragraph:{spacing:{line:230,lineRule:LineRuleType.AUTO}}}},
    paragraphStyles:[{id:'Heading1',name:'Heading 1',basedOn:'Normal',next:'Normal',run:{font:FONT,color:'000000',size:20},paragraph:{keepNext:true}},
      {id:'Heading2',name:'Heading 2',basedOn:'Normal',next:'Normal',run:{font:FONT,color:'000000',size:20},paragraph:{keepNext:true}}]},
  sections:[{properties:{page:PAGE},children:title},
    {properties:{type:SectionType.CONTINUOUS,column:{count:2,space:360,equalWidth:true},page:PAGE},children:body},
    // A final continuous section balances the final reference columns in Word/Writer.
    {properties:{type:SectionType.CONTINUOUS,page:PAGE},children:[new Paragraph({spacing:{before:0,after:0,line:20,lineRule:LineRuleType.EXACT},children:[]})]}]});
async function main(){
    const output=path.join(ROOT,'Jawe_OPG_nonreceipt_KZN.docx');
    fs.writeFileSync(output,await Packer.toBuffer(doc));
    fs.writeFileSync(path.join(ROOT,'manuscript_numbered.md'),remapped+'\n\n## References\n\n'+ids.map((id,i)=>`[${i+1}] ${references[id]}`).join('\n\n')+'\n');
    fs.writeFileSync(path.join(ROOT,'citation_map.json'),JSON.stringify({source:'references.json',
      order:'first appearance in manuscript',source_to_published:Object.fromEntries(ids.map((id,i)=>[id,i+1])),
      unused_source_ids:Object.keys(references).map(Number).filter(id=>!ids.includes(id))},null,2)+'\n');
    console.log(`Wrote ${output}; ${ids.length} references in first-use order.`);
}
main().catch(error=>{console.error(error);process.exitCode=1;});
