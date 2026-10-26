"""Final evidence report; refuses to claim success with missing/red runs."""
from pathlib import Path
from collections import Counter
import csv,hashlib,html,json,re
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent
DATA=OUT/'resultados'
def read(path):return json.loads(path.read_text(encoding='utf-8'))
def esc(text):return html.escape(str(text),quote=True)

def main():
    suite=read(DATA/'suite_final.json');layout=read(DATA/'layout_completo.json');firefox=read(DATA/'firefox_resultado.json')
    gates=read(OUT/'decisoes_entrega.json')
    assert suite['failed']==0 and suite['errors']==0 and suite['skipped']==0 and suite['sources_stable'], 'Behavioral suite is not green/frozen'
    assert suite['distributed_html'], 'Final run must use generated index.html'
    assert layout['failed']==0 and layout['passed']==layout['cases'] and not layout['quick'], 'Full layout matrix is not green'
    assert firefox['failed']==0 and firefox['passed']==firefox['tests'], 'Native Firefox matrix is not green'
    for run in [layout,firefox]:
        assert run['distributed_html'] and run['sources_stable'] and not run['quick'], 'Final matrices must use frozen distributed HTML'
        assert run['source_hashes']==suite['source_hashes'], 'Matrices must test the same source revision'
    required_gates={'task1_review','task2_review','task3_review','whole_review','structural_checks','documented_scope'}
    assert required_gates.issubset(gates['checks']) and all(gates['checks'].values()), 'Delivery/review gates remain open'
    for name,digest in suite['source_hashes'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest, 'Source changed since behavioral run: '+name
    integrity=read(DATA/'integridade_referencias.json');artifact=read(DATA/'artefato_distribuido.json')
    assert integrity['failed']==0 and artifact['failed']==0, 'Reference or distribution integrity failed'
    assert artifact['index_sha256']==suite['source_hashes']['index.html'], 'Artifact verification is stale'
    integration=read(DATA/'validacao_integracao.json')
    assert integration['passed'] and integration['complete'] and integration['source_hashes']==suite['source_hashes'], 'Integrated delivery validation is incomplete/stale'
    source=(ROOT/'parts_js_core.py').read_text(encoding='utf-8')
    version=re.search(r"APP_VERSION:\s*'([^']+)'",source).group(1)
    cases=suite['tests']+layout['cases']+firefox['tests']
    summary={'version':version,'date':'2026-10-25','tests_total':cases,'tests_passed':cases,
             'behavioral':suite['tests'],'edge_layout':layout['cases'],'firefox':firefox['tests'],
             'failures':0,'errors':0,'skipped':0,'source_hashes':suite['source_hashes'],
             'scope':'100% dos cenários catalogados e executados nesta máquina; não é 100% de code coverage ou prova de ausência de todos os defeitos.',
             'physical_not_verified':gates['physical_not_verified']}
    (OUT/'resumo_final.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    resolutions=gates['resolutions'];assert len(resolutions)==40 and len({x['id'] for x in resolutions})==40
    assert all(x['status'] in ['corrigido','decisao_documentada'] for x in resolutions)
    with (OUT/'RESOLUCAO_ACHADOS.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['id','status','resolution','evidence'],delimiter=';');writer.writeheader();writer.writerows(resolutions)
    title='Correção integral — aplicação '+version
    paragraphs=[
        'A aplicação foi corrigida mantendo o arquivo HTML único, o funcionamento offline e a base IndexedDB. Os testes utilizaram origens/perfis temporários; os dados do usuário e os documentos de referência foram preservados.',
        'A composição usa navegação lateral em monitores, rail compacto no tablet em paisagem e topo móvel com relógio e aviso condicional de áudio. Editor e lousa ficam paralelos quando há largura útil. Campos e textos mantêm largura de leitura; a área adicional apresenta listas, detalhe selecionado e contexto real, sem dados inventados para preencher a tela.',
        'Os defeitos de integridade, alarmes, importação, cancelamento, identidade de diálogos, foco, filtros, resize, cache e desenho foram tratados e cobertos por regressões. Os registros abaixo identificam a resolução dos 40 grupos da auditoria.',
        summary['scope'],
        'Core e UI passaram por revisão independente e correções escopadas. O fallback de lease apenas reduz concorrência quando navigator.locks não está disponível; a exclusão de claims de alarmes e a preservação de conclusões são garantidas pelas transações IndexedDB.',
        'Estados sem registros mostram orientações e resumos compactos. Não se esticam cartões ou se inventam séries para preencher uma tela sem dados. Modos manuais respeitam a preferência; o automático distribui o contexto segundo a largura útil.',
        'A revisão integral confrontou os 321 requisitos documentais e os 22 elementos visuais; os registros seguintes resolvem os 40 agrupamentos da auditoria. Isso não significa que existam 321 novos testes individuais. A coexistência de métodos legados e overrides permanece como dívida de manutenção aceita, sem defeito operacional novo identificado; sua consolidação exige tarefa isolada com as regressões preservadas.',
    ]
    headings=['Bateria','Resultado','Evidência']
    rows=[['Comportamento no Edge',f"{suite['passed']}/{suite['tests']}",'resultados/suite_final.json'],
          ['Geometria, temas e modais no Edge',f"{layout['passed']}/{layout['cases']}",'resultados/layout_completo.json'],
          ['Compatibilidade e layout no Firefox instalado',f"{firefox['passed']}/{firefox['tests']}",'resultados/firefox_resultado.json']]
    md=['# '+title,'','25/10/2026 — Horário de Brasília','']
    md.extend(p+'\n' for p in paragraphs)
    md.extend(['| '+' | '.join(headings)+' |','| --- | --- | --- |'])
    md.extend('| '+' | '.join(r)+' |' for r in rows)
    md.extend(['','## Resolução dos achados',''])
    for x in resolutions:md.append(f"- **{x['id']} — {x['status']}:** {x['resolution']} Evidência: {x['evidence']}")
    md.extend(['','## Não verificado em aparelho físico',''])
    md.extend('- '+x for x in gates['physical_not_verified'])
    rulings=read(OUT/'decisoes_tecnicas.json')
    md.extend(['','## Decisões adotadas e custos caso estejam erradas',''])
    md.extend('- '+x['decision']+' Custo se incorreta: '+x['cost_if_wrong'] for x in rulings)
    md.extend(['','## Execução e rastreabilidade','','Consulte TESTES.md, os JSON/CSV de resultados, as revisões e os hashes de fontes. Os logs RED são históricos de reprodução, não falhas da versão final.'])
    (OUT/'RELATORIO_FINAL.md').write_text('\n'.join(md),encoding='utf-8')
    body=['<h1>'+esc(title)+'</h1><p>25/10/2026 — Horário de Brasília</p>']
    body.extend('<p>'+esc(x)+'</p>' for x in paragraphs)
    body.append('<div class="totals"><strong>'+str(cases)+' verificações aprovadas</strong><span>0 falhas · 0 erros · 0 testes ignorados</span></div>')
    body.append('<h2>Resultados executados</h2><table><thead><tr>'+''.join('<th>'+esc(x)+'</th>' for x in headings)+'</tr></thead><tbody>')
    body.extend('<tr><td>'+esc(a)+'</td><td>'+esc(b)+'</td><td><a href="'+esc(c)+'">JSON completo</a></td></tr>' for a,b,c in rows)
    body.append('</tbody></table><h2>Resolução dos 40 grupos</h2><label>Pesquisar achado<input id="search" type="search" placeholder="Ex.: alarme, GUI-10, layout"></label><div id="findings">')
    for x in resolutions:
        body.append('<article><h3>'+esc(x['id'])+' — '+esc(x['status'])+'</h3><p>'+esc(x['resolution'])+'</p><p class="evidence">'+esc(x['evidence'])+'</p></article>')
    body.append('</div><h2>Interfaces finais</h2><p>Capturas no Microsoft Edge. A validação do Firefox está registrada na matriz JSON. Clique na captura para abrir a resolução original.</p><div class="gallery">')
    extra_captures=read(DATA/'task4-captures.json')['screenshots']
    for path in sorted(DATA/name for name in set(layout['screenshots']+extra_captures)):
        assert path.is_file(), 'Final screenshot missing: '+path.name
        body.append('<details><summary>'+esc(path.name)+'</summary><a href="resultados/'+esc(path.name)+'"><img loading="lazy" src="resultados/'+esc(path.name)+'" alt="'+esc(path.stem)+'"></a></details>')
    body.append('</div><h2>Limites físicos</h2><ul>'+''.join('<li>'+esc(x)+'</li>' for x in gates['physical_not_verified'])+'</ul>')
    body.append('<h2>Decisões adotadas e custos caso estejam erradas</h2><ul>'+''.join('<li>'+esc(x['decision'])+' <strong>Custo se incorreta:</strong> '+esc(x['cost_if_wrong'])+'</li>' for x in rulings)+'</ul>')
    body.append('<h2>Rastreabilidade</h2><ul><li><a href="TESTES.md">Comandos dos testes</a></li><li><a href="RESOLUCAO_ACHADOS.csv">Resoluções em CSV</a></li><li><a href="resultados/suite_final.csv">Casos comportamentais em CSV</a></li><li><a href="../auditoria_interface/RELATORIO_INTERFACE.html">Auditoria original e referências</a></li><li><a href="../index.html">Abrir aplicação atualizada</a></li></ul>')
    css='body{margin:0;background:#f4f7fa;color:#192c3c;font:16px/1.55 system-ui,sans-serif}main{max-width:1200px;margin:auto;padding:24px}nav{background:#153d5d;padding:16px;color:white;display:flex;gap:20px;flex-wrap:wrap}nav a{color:white}h1,h2,h3{color:#123e60}h2{margin-top:2.4em}p{max-width:85ch}a{color:#075d98}.totals{background:#d7f1e5;border-left:5px solid #17653d;padding:20px;display:flex;gap:24px;flex-wrap:wrap}table{border-collapse:collapse;background:white;width:100%}td,th{border:1px solid #c5d3dd;padding:12px;text-align:left}article{padding:16px;background:white;border:1px solid #d2dde5;margin:12px 0}.evidence{font-size:14px;color:#445d70;overflow-wrap:anywhere}input{display:block;width:min(95%,650px);padding:12px;font:inherit;margin:12px 0}.gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px}details{background:white;padding:12px;overflow-wrap:anywhere;border:1px solid #d2dde5}img{max-width:100%}@media(max-width:600px){main{padding:16px}td,th{padding:8px;font-size:14px}}'
    js="document.getElementById('search').addEventListener('input',function(){let q=this.value.toLocaleLowerCase('pt-BR');document.querySelectorAll('#findings article').forEach(e=>e.hidden=!e.textContent.toLocaleLowerCase('pt-BR').includes(q))})"
    doc='<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(title)+'</title><style>'+css+'</style><nav><strong>Entrega da correção integral</strong><a href="../index.html">Aplicação</a><a href="RESOLUCAO_ACHADOS.csv">Resoluções</a></nav><main>'+''.join(body)+'</main><script>'+js+'</script></html>'
    (OUT/'RELATORIO_FINAL.html').write_text(doc,encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
