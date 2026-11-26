---
# ! Alteração de IA - Revisar: verbete da biblioteca base da Fase 2-B (mecanismo de falha).
# ! Motivo: o cobaia tem um injetor de falhas de propósito; documentar o efeito exato de
# cada modo no fio é o que permite ao modelo reconhecer "um campo só, o resto íntegro".
id: modos-de-injecao
titulo: Injeção de falhas da CobaiaAPI
sistema: CobaiaAPI
entidade_principal: Infraestrutura
tipo: funcionamento
status: ativo
arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaAPI/app/routers/admin_fault.py, Programacao/CobaiaAPI/.env.example]
endpoints: [GET /api/admin/fault-mode, POST /api/admin/fault-mode]
sintomas: [um campo alterado e o resto integro, 500 com fault injection, atraso fixo de 2 s, corpo cortado]
palavras_chave: [fault, injecao, falha, modo, error_500, latency, type_drift, field_missing, field_renamed, malformed_json, target_field, probability, X-Admin-Token]
causas_relacionadas: [erro_interno_do_servidor, tempo_de_resposta_excedido, tipo_divergente, campo_ausente, campo_renomeado, resposta_truncada]
---
## Resumo
Injetor com 7 modos: error_500, latency (2 s), type_drift (campo-alvo vira texto), field_missing (remove), field_renamed (vira <campo>_v2), malformed_json (corpo cortado) e normal.

## Sinais
- só um campo alterado, resto íntegro: modo com campo-alvo
- detail "fault injection: error_500 em produto"

## Causa
Ligado por FAULT_MODE/FAULT_TARGET_FIELD no .env ou POST /api/admin/fault-mode com X-Admin-Token; probability < 1 dá intermitência.
