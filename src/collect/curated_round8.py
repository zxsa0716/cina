"""Round 8 — full Plano Clima 17 sectoral + PRIMAP-hist + UNFCCC AdCom + WB CCDR.

가장 큰 단일 batch — 데이터 완성도 95% → 99% 도약 목표.
"""
from __future__ import annotations

import logging
from pathlib import Path

from .base import CollectorBase

logger = logging.getLogger(__name__)


# Plano Clima Brasil — Estratégia Nacional + 16 Setoriais e Temáticos (총 17 PDFs)
PLANO_CLIMA_FULL = [
    ("https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/estrategia-nacional-de-adaptacao.pdf",
     "Brazil_PlanoClima_Estrategia_Nacional_Adaptacao", "BRA", "MAIN"),
    ("https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/plano-clima-adaptacao-sumario-executivo.pdf",
     "Brazil_PlanoClima_Sumario_Executivo_v2", "BRA", "MAIN"),
    # Sectoral Plans (9)
    ("https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/planosetorial-agriculturapecuaria.pdf",
     "Brazil_PlanoSetorial_Agricultura_Pecuaria", "BRA", "SECTORAL"),
    ("https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/planosetorial-agricultura-familiar.pdf",
     "Brazil_PlanoSetorial_Agricultura_Familiar", "BRA", "SECTORAL"),
    ("https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/planosetorial-cidades.pdf",
     "Brazil_PlanoSetorial_Cidades", "BRA", "SECTORAL"),
    ("https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/planosetorial-energia.pdf",
     "Brazil_PlanoSetorial_Energia", "BRA", "SECTORAL"),
    ("https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/planosetorial-reducao-gestao-riscos-desastres.pdf",
     "Brazil_PlanoSetorial_Riscos_Desastres", "BRA", "SECTORAL"),
    ("https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/planosetorial-saude.pdf",
     "Brazil_PlanoSetorial_Saude", "BRA", "SECTORAL"),
    ("https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/planosetorial-seguranca-alimentar-nutricional.pdf",
     "Brazil_PlanoSetorial_Seguranca_Alimentar", "BRA", "SECTORAL"),
    ("https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/planosetorial-transportes.pdf",
     "Brazil_PlanoSetorial_Transportes", "BRA", "SECTORAL"),
    ("https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/planosetorial-turismo.pdf",
     "Brazil_PlanoSetorial_Turismo", "BRA", "SECTORAL"),
    # Thematic Plans (6)
    ("https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/plano-tematico-biodiversidade.pdf",
     "Brazil_PlanoTematico_Biodiversidade", "BRA", "THEMATIC"),
    ("https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/planotematico-igualdade-racial-combate-racismo.pdf",
     "Brazil_PlanoTematico_Igualdade_Racial", "BRA", "THEMATIC"),
    ("https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/planotematico-oceano-zona-costeira.pdf",
     "Brazil_PlanoTematico_Oceano_Costeira", "BRA", "THEMATIC"),
    ("https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/planotematico-povos-comunidades-tradicionais.pdf",
     "Brazil_PlanoTematico_Comunidades_Tradicionais", "BRA", "THEMATIC"),
    ("https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/planotematico-povos-indigenas.pdf",
     "Brazil_PlanoTematico_Povos_Indigenas", "BRA", "THEMATIC"),
    ("https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/planotematico-recursos-hidricos.pdf",
     "Brazil_PlanoTematico_Recursos_Hidricos", "BRA", "THEMATIC"),
]

# PRIMAP-hist v2.6.1 — 1750-2023 GHG 시계열 (Stage 2 country features baseline)
PRIMAP_HIST = [
    ("https://zenodo.org/records/15016289/files/Guetschow_et_al_2025-PRIMAP-hist_v2.6.1_final_13-Mar-2025.csv?download=1",
     "PRIMAP_hist_v2_6_1_1750_2023", "Global", "BASELINE"),
]

# UNFCCC Adaptation Communications Registry — 직접 PDF 발견된 것
UNFCCC_ADAPTATION_COMMUNICATIONS = [
    ("https://unfccc.int/sites/default/files/ACR/2023-03/The%20Republic%20of%20Koreas%20Adaptation%20Communication.pdf",
     "Korea_Republic_Adaptation_Communication_2023", "KOR", "MULTI"),
]

# World Bank CCDR 추가 (BR 외 5국)
WB_CCDR_EXPANDED = [
    # World Bank Open Knowledge Repository 직접 패턴
    ("https://documents1.worldbank.org/curated/en/099051723150515371/pdf/P1781730a06ee30c70a8a30bbfd5c00ad24.pdf",
     "WB_CCDR_India_alt", "IND", "BASELINE"),
    ("https://documents1.worldbank.org/curated/en/099092122110587923/pdf/P1772370fad77a04609fd708f1e60bf9da7.pdf",
     "WB_CCDR_Indonesia", "IDN", "BASELINE"),
    # NDC Partnership 직접 패턴 (CCDR 인덱스)
    ("https://ndcpartnership.org/sites/default/files/2023-04/CCDR_2023_summary.pdf",
     "NDC_Partnership_CCDR_2023_summary", "Multiple", "BASELINE"),
]

# UNDRR / EM-DAT 풍부한 disaster 데이터 (Stage 2 vulnerability features)
DISASTER_DATA = [
    # UNDRR Sendai Framework Monitor — 시계열 disaster 통계
    ("https://www.undrr.org/media/91140/download?attachment",
     "UNDRR_Sendai_Framework_2023_status", "Global", "BASELINE"),
]

# IISD ENB 추가 — COP21-29 archives (Castro 재현 input 보강)
ENB_HISTORICAL_BACKFILL = [
    # COP21-25 cumulative
    ("https://enb.iisd.org/sites/default/files/2015-12/enb12660e.pdf", "enb12660e_COP21_pre", "Multiple", "COP21"),
    ("https://enb.iisd.org/sites/default/files/2018-12/enb12740e.pdf", "enb12740e_COP24_pre", "Multiple", "COP24"),
    # SBI/SBSTA 종합 보고
    ("https://enb.iisd.org/sites/default/files/2024-06/enb12858e.pdf", "enb12858e_SB60_2024", "Multiple", "SB60"),
    ("https://enb.iisd.org/sites/default/files/2025-06/enb12877e.pdf", "enb12877e_SB62_2025", "Multiple", "SB62"),
]


class CuratedRound8Collector(CollectorBase):
    source_system = "round8_curated"
    source_type = "round8_curated"
    license_str = "Mixed (gov.br Public / Zenodo CC BY-NC-SA / UN Open / WB CC BY-4.0)"
    license_attribution = "© Various (MMA Brazil / PRIMAP / UNFCCC / World Bank / IISD)"

    def collect(self) -> list[dict]:
        records = []
        all_targets = []
        all_targets += [(u, s, c, sess, "plano_clima_17") for u, s, c, sess in PLANO_CLIMA_FULL]
        all_targets += [(u, s, c, sess, "primap_hist_baseline") for u, s, c, sess in PRIMAP_HIST]
        all_targets += [(u, s, c, sess, "adaptation_communication") for u, s, c, sess in UNFCCC_ADAPTATION_COMMUNICATIONS]
        all_targets += [(u, s, c, sess, "wb_ccdr_expanded") for u, s, c, sess in WB_CCDR_EXPANDED]
        all_targets += [(u, s, c, sess, "disaster_data") for u, s, c, sess in DISASTER_DATA]
        all_targets += [(u, s, c, sess, "enb_historical_backfill") for u, s, c, sess in ENB_HISTORICAL_BACKFILL]

        for url, slug, country, sess, kind in all_targets:
            if "csv" in url.lower() or url.lower().endswith(".csv?download=1"):
                ext = ".csv"
            elif url.lower().endswith(".pdf") or "pdf" in url.lower():
                ext = ".pdf"
            else:
                ext = ".pdf"
            local = self.out_dir / kind / f"{slug}{ext}"
            try:
                dl = self.http.download(url, local)
            except Exception as exc:
                logger.warning("Round8 download failed for %s: %s", url, exc)
                continue

            extras = {
                "session": sess,
                "doc_kind": kind,
                "country_authors_initial": [country] if country and country != "Multiple" else [],
                "round_target": "round8_full_completion",
            }
            if kind == "plano_clima_17":
                extras["topic_tags_initial"] = ["adaptation", "brazil_plano_clima", "PNAC_2024"]
            elif kind == "primap_hist_baseline":
                extras["topic_tags_initial"] = ["GHG", "PRIMAP", "baseline_data", "1750-2023"]
                extras["doc_kind"] = "data_csv"
            elif kind == "adaptation_communication":
                extras["topic_tags_initial"] = ["adaptation_communication", "AdCom"]
            elif kind == "wb_ccdr_expanded":
                extras["topic_tags_initial"] = ["world_bank", "country_climate_development_report"]
            elif kind == "disaster_data":
                extras["topic_tags_initial"] = ["UNDRR", "Sendai_Framework", "disaster_baseline"]
            elif kind == "enb_historical_backfill":
                extras["topic_tags_initial"] = ["enb_summary", "historical", "castro_input"]

            rec = self.write_meta(
                local_path=local,
                url=url,
                sha256=dl["sha256"],
                size_bytes=dl["size_bytes"],
                extra=extras,
            )
            records.append(rec)
        return records
