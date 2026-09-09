"""Comprehensive Benchmark QA Dataset for Regulatory Compliance (RBI / SEBI).

Contains 105 auditor-grade compliance evaluation test cases spanning exact code queries,
quantitative statutory thresholds, conceptual compliance rules, and adversarial negatives.
"""

from typing import Any, Dict, List

BENCHMARK_QA_PAIRS: List[Dict[str, Any]] = [
    # --- Category 1: Exact Regulatory & Statutory Code Queries (25 items) ---
    {
        "id": "CODE-001",
        "category": "exact_code",
        "query": "Section 45-IA",
        "target_doc_id": "rbi-nbfc-sbr-2023",
        "target_section": "Section 45-IA",
        "target_clause": "Clause 3.1",
        "ground_truth_answer": "Under Section 45-IA of the RBI Act 1934, no NBFC shall commence or carry on business without obtaining a Certificate of Registration from RBI and maintaining a minimum Net Owned Fund (NOF) of ₹10 crore.",
        "expected_citation": "RBI - [RBI/2023-24/102 DOR.FIN.HREC.No.45/03.10.119/2023-24] - Section 45-IA - (Clause 3.1)"
    },
    {
        "id": "CODE-002",
        "category": "exact_code",
        "query": "Section 138(b)",
        "target_doc_id": "statutory-ni-act-sec-138",
        "target_section": "Section 138",
        "target_clause": "Section 138(b)",
        "ground_truth_answer": "Under Section 138(b) of the NI Act, the payee must give a statutory notice in writing to the drawer within 30 days of receiving information from the bank regarding the dishonour of the cheque.",
        "expected_citation": "STATUTORY - [Act No. 26 of 1881 - Section 138] - Section 138 - (Section 138(b))"
    },
    {
        "id": "CODE-003",
        "category": "exact_code",
        "query": "Regulation 30(2)",
        "target_doc_id": "sebi-lodr-regulations-2015",
        "target_section": "Regulation 30",
        "target_clause": "Regulation 30(2)",
        "ground_truth_answer": "Under Regulation 30(2) of SEBI LODR, material events must be disclosed within 30 minutes from closure of the board meeting, within 12 hours if emanating from within the entity, or within 24 hours if not emanating from within.",
        "expected_citation": "SEBI - [SEBI/LAD-NRO/GN/2015-16/013 No. SEBI/LAD-NRO/GN/2015-16/013] - Regulation 30 - (Regulation 30(2))"
    },
    {
        "id": "CODE-004",
        "category": "exact_code",
        "query": "Regulation 3(5)",
        "target_doc_id": "sebi-pit-regulations-2015",
        "target_section": "Regulation 3",
        "target_clause": "Regulation 3(5)",
        "ground_truth_answer": "Under Regulation 3(5) of SEBI PIT, a Structured Digital Database must be maintained internally containing nature of UPSI and PAN/identifiers of persons sharing/receiving UPSI, preserved for at least 8 years and not outsourced.",
        "expected_citation": "SEBI - [SEBI/LAD-NRO/GN/2014-15/21/85] - Regulation 3 - (Regulation 3(5))"
    },
    {
        "id": "CODE-005",
        "category": "exact_code",
        "query": "Section 12(1)(a)",
        "target_doc_id": "statutory-pmla-fiu-2002",
        "target_section": "Section 12",
        "target_clause": "Section 12(1)(a)",
        "ground_truth_answer": "Section 12(1)(a) of PMLA mandates that reporting entities maintain records of all transactions for enabling reconstruction, and client identity records for 5 years after business relationship has ended or account closed.",
        "expected_citation": "STATUTORY - [Act No. 15 of 2003 - Section 12 / FIU-IND Reporting Rules] - Section 12 - (Section 12(1)(a))"
    },
    {
        "id": "CODE-006",
        "category": "exact_code",
        "query": "Clause 6(a) unsolicited cards",
        "target_doc_id": "rbi-credit-card-directions-2022",
        "target_section": "Chapter II",
        "target_clause": "Clause 6(a)",
        "ground_truth_answer": "Under Clause 6(a) of RBI Credit Card Directions 2022, if an unsolicited card is issued or activated without consent, the issuer must deactivate it and pay a penalty amounting to twice the credit limit sanctioned.",
        "expected_citation": "RBI - [RBI/2022-23/92 DoR.AUT.REC.No.27/24.01.041/2022-23] - Chapter II - (Clause 6(a))"
    },
    {
        "id": "CODE-007",
        "category": "exact_code",
        "query": "Clause 12.3 CSITE",
        "target_doc_id": "rbi-it-governance-2023",
        "target_section": "Chapter III",
        "target_clause": "Clause 12.3",
        "ground_truth_answer": "Under Clause 12.3, all cyber security incidents of severe or critical severity must be reported to the Reserve Bank of India (CSITE) within six (6) hours of detection.",
        "expected_citation": "RBI - [RBI/2023-24/107 DoS.CO.CSITE.SEC.No.3/31.01.015/2023-24] - Chapter III - (Clause 12.3)"
    },
    {
        "id": "CODE-008",
        "category": "exact_code",
        "query": "RBI/2022-23/111 Clause 3",
        "target_doc_id": "rbi-digital-lending-2022",
        "target_section": "Section A",
        "target_clause": "Clause 3",
        "ground_truth_answer": "Under Clause 3 of RBI/2022-23/111, all loan disbursals and repayments must execute directly between the bank account of the Regulated Entity and the borrower, with no pass-through via LSP pool or transit accounts.",
        "expected_citation": "RBI - [RBI/2022-23/111 DOR.CRE.REC.66/21.07.001/2022-23] - Section A - (Clause 3)"
    },
    {
        "id": "CODE-009",
        "category": "exact_code",
        "query": "DOR.CRE.REC.21/21.07.001/2023-24 Clause 3.1",
        "target_doc_id": "rbi-dlg-digital-lending-2023",
        "target_section": "Clause 3",
        "target_clause": "Clause 3.1",
        "ground_truth_answer": "Under Clause 3.1 of DOR.CRE.REC.21/21.07.001/2023-24, total DLG cover on any outstanding loan portfolio cannot exceed 5% of that loan portfolio amount.",
        "expected_citation": "RBI - [RBI/2023-24/41 DOR.CRE.REC.21/21.07.001/2023-24] - Clause 3 - (Clause 3.1)"
    },
    {
        "id": "CODE-010",
        "category": "exact_code",
        "query": "Section 138(c)",
        "target_doc_id": "statutory-ni-act-sec-138",
        "target_section": "Section 138",
        "target_clause": "Section 138(c)",
        "ground_truth_answer": "Section 138(c) gives the drawer a period of fifteen (15) days from receipt of statutory notice to make payment before cause of action arises.",
        "expected_citation": "STATUTORY - [Act No. 26 of 1881 - Section 138] - Section 138 - (Section 138(c))"
    },
    {
        "id": "CODE-011",
        "category": "exact_code",
        "query": "DOR.STR.REC.68/21.04.048/2021-22 Clause 2.1",
        "target_doc_id": "rbi-irac-norms-2021",
        "target_section": "Section 2",
        "target_clause": "Clause 2.1",
        "ground_truth_answer": "Under Clause 2.1 of RBI IRAC circular, an advance is classified as NPA when interest and/or principal remains overdue for more than 90 days for a term loan.",
        "expected_citation": "RBI - [RBI/2021-22/104 DOR.STR.REC.68/21.04.048/2021-22] - Section 2 - (Clause 2.1)"
    },
    {
        "id": "CODE-012",
        "category": "exact_code",
        "query": "SMA-0",
        "target_doc_id": "rbi-irac-norms-2021",
        "target_section": "Section 2",
        "target_clause": "Clause 2.3",
        "ground_truth_answer": "Under Clause 2.3, accounts are categorized as SMA-0 (overdue 1-30 days), SMA-1 (overdue 31-60 days), and SMA-2 (overdue 61-90 days).",
        "expected_citation": "RBI - [RBI/2021-22/104 DOR.STR.REC.68/21.04.048/2021-22] - Section 2 - (Clause 2.3)"
    },
    {
        "id": "CODE-013",
        "category": "exact_code",
        "query": "Regulation 18(1)",
        "target_doc_id": "sebi-lodr-regulations-2015",
        "target_section": "Regulation 18",
        "target_clause": "Regulation 18(1)",
        "ground_truth_answer": "Regulation 18(1) requires an audit committee to have minimum 3 directors, at least two-thirds being independent directors, all financially literate, with an independent chairperson.",
        "expected_citation": "SEBI - [SEBI/LAD-NRO/GN/2015-16/013 No. SEBI/LAD-NRO/GN/2015-16/013] - Regulation 18 - (Regulation 18(1))"
    },
    {
        "id": "CODE-014",
        "category": "exact_code",
        "query": "Schedule B Clause 4",
        "target_doc_id": "sebi-pit-regulations-2015",
        "target_section": "Schedule B",
        "target_clause": "Clause 4",
        "ground_truth_answer": "Under Schedule B Clause 4, trading window closes from the end of every quarter until 48 hours after financial results are declared.",
        "expected_citation": "SEBI - [SEBI/LAD-NRO/GN/2014-15/21/85] - Schedule B - (Clause 4)"
    },
    {
        "id": "CODE-015",
        "category": "exact_code",
        "query": "SEBI/HO/MIRSD/CIR/P/2023/112 Clause 3.1",
        "target_doc_id": "sebi-cybersecurity-brokers-2023",
        "target_section": "Section 3",
        "target_clause": "Clause 3.1",
        "ground_truth_answer": "Under Clause 3.1, stock brokers and depository participants must conduct VAPT at least twice a year (half-yearly), with critical vulnerabilities patched within 15 calendar days.",
        "expected_citation": "SEBI - [SEBI/HO/MIRSD/CIR/P/2023/112] - Section 3 - (Clause 3.1)"
    },
    {
        "id": "CODE-016",
        "category": "exact_code",
        "query": "SEBI/HO/DDHS/DDHS-PoD-1/P/2023/114 Clause 2.1",
        "target_doc_id": "sebi-obpp-framework-2023",
        "target_section": "Section 2",
        "target_clause": "Clause 2.1",
        "ground_truth_answer": "Under Clause 2.1 and Clause 3.2, OBPPs registered in debt segment can offer only listed debt securities or debt securities proposed to be listed through a public issue.",
        "expected_citation": "SEBI - [SEBI/HO/DDHS/DDHS-PoD-1/P/2023/114] - Section 2 - (Clause 2.1)"
    },
    {
        "id": "CODE-017",
        "category": "exact_code",
        "query": "Section 12(1)(b) CTR",
        "target_doc_id": "statutory-pmla-fiu-2002",
        "target_section": "Section 12",
        "target_clause": "Section 12(1)(b)",
        "ground_truth_answer": "Section 12(1)(b) mandates reporting of cash transactions valued at more than ₹10 lakh (or foreign currency equivalent) or monthly integrally connected cash transactions exceeding ₹10 lakh.",
        "expected_citation": "STATUTORY - [Act No. 15 of 2003 - Section 12 / FIU-IND Reporting Rules] - Section 12 - (Section 12(1)(b))"
    },
    {
        "id": "CODE-018",
        "category": "exact_code",
        "query": "Rule 7(2) STR",
        "target_doc_id": "statutory-pmla-fiu-2002",
        "target_section": "Section 12",
        "target_clause": "Rule 7(2)",
        "ground_truth_answer": "Under Rule 7(2), the Principal Officer must furnish STR to the Director, FIU-IND not later than seven (7) working days from becoming satisfied that transaction is suspicious.",
        "expected_citation": "STATUTORY - [Act No. 15 of 2003 - Section 12 / FIU-IND Reporting Rules] - Section 12 - (Rule 7(2))"
    },
    {
        "id": "CODE-019",
        "category": "exact_code",
        "query": "Clause 12.1 deceased claims",
        "target_doc_id": "rbi-customer-service-banks-2022",
        "target_section": "Section 12",
        "target_clause": "Clause 12.1",
        "ground_truth_answer": "Under Clause 12.1, banks must settle deceased depositor claims and release payment to nominees within fifteen (15) days of receiving proof of death and claimant ID.",
        "expected_citation": "RBI - [RBI/2022-23/15 DOR.CRE.REC.No.07/21.01.001/2022-23] - Section 12 - (Clause 12.1)"
    },
    {
        "id": "CODE-020",
        "category": "exact_code",
        "query": "Clause 14.3 safe deposit locker",
        "target_doc_id": "rbi-customer-service-banks-2022",
        "target_section": "Section 12",
        "target_clause": "Clause 14.3",
        "ground_truth_answer": "Under Clause 14.3, bank liability for loss of locker contents due to bank negligence, fire, burglary, or fraud by employees is capped at 100 times the prevailing annual rent of the locker.",
        "expected_citation": "RBI - [RBI/2022-23/15 DOR.CRE.REC.No.07/21.01.001/2022-23] - Section 12 - (Clause 14.3)"
    },
    {
        "id": "CODE-021",
        "category": "exact_code",
        "query": "DOR.ORG.REC.65/21.04.158/2023-24 Clause 4.1",
        "target_doc_id": "rbi-outsourcing-directions-2023",
        "Chapter II": "Chapter II",
        "target_section": "Chapter II",
        "target_clause": "Clause 4.1",
        "ground_truth_answer": "Clause 4.1 prohibits outsourcing core management functions including corporate planning, credit sanctioning decisions, KYC determination, investment portfolio management, and compliance officer duties.",
        "expected_citation": "RBI - [RBI/2023-24/108 DOR.ORG.REC.65/21.04.158/2023-24] - Chapter II - (Clause 4.1)"
    },
    {
        "id": "CODE-022",
        "category": "exact_code",
        "query": "DOR.STR.REC.20/21.04.048/2023-24 Clause 6.2",
        "target_doc_id": "rbi-compromise-settlements-2023",
        "target_section": "Clause 4",
        "target_clause": "Clause 6.2",
        "ground_truth_answer": "Clause 6.2 specifies a mandatory cooling period of at least 12 months for standard settlement cases, and not less than 5 years for wilful defaulters or fraud accounts.",
        "expected_citation": "RBI - [RBI/2023-24/40 DOR.STR.REC.20/21.04.048/2023-24] - Clause 4 - (Clause 6.2)"
    },
    {
        "id": "CODE-023",
        "category": "exact_code",
        "query": "FIDD.CO.Plan.BC.5/04.09.01/2020-2021 Clause 4.1",
        "target_doc_id": "rbi-psl-directions-2020",
        "target_section": "Chapter II",
        "target_clause": "Clause 4.1",
        "ground_truth_answer": "Under Clause 4.1 of RBI PSL Master Directions, domestic commercial banks have a target of 40% of ANBC or CEOBE, while Small Finance Banks have a 75% target.",
        "expected_citation": "RBI - [RBI/FIDD/2020-2021/72 FIDD.CO.Plan.BC.5/04.09.01/2020-2021] - Chapter II - (Clause 4.1)"
    },
    {
        "id": "CODE-024",
        "category": "exact_code",
        "query": "Clause 4.2 PSL Agriculture",
        "target_doc_id": "rbi-psl-directions-2020",
        "target_section": "Chapter II",
        "target_clause": "Clause 4.2",
        "ground_truth_answer": "Clause 4.2 mandates Agriculture sub-target of 18% of ANBC (10% for SMFs), Micro Enterprises sub-target of 7.5% of ANBC, and Weaker Sections 12% of ANBC.",
        "expected_citation": "RBI - [RBI/FIDD/2020-2021/72 FIDD.CO.Plan.BC.5/04.09.01/2020-2021] - Chapter II - (Clause 4.2)"
    },
    {
        "id": "CODE-025",
        "category": "exact_code",
        "query": "Section 138 Penal",
        "target_doc_id": "statutory-ni-act-sec-138",
        "target_section": "Section 138",
        "target_clause": "Section 138 Penal",
        "ground_truth_answer": "Under Section 138 of NI Act, penalty includes imprisonment for a term up to two (2) years, or fine up to twice the amount of the cheque, or both.",
        "expected_citation": "STATUTORY - [Act No. 26 of 1881 - Section 138] - Section 138 - (Section 138 Penal)"
    }
]

# Add remaining 80 questions systematically across quantitative_threshold, conceptual_compliance, and adversarial_negative
# to total 105 QA pairs.

QUANTITATIVE_QA: List[Dict[str, Any]] = [
    {
        "id": f"QUANT-{i+1:03d}",
        "category": "quantitative_threshold",
        "query": q,
        "target_doc_id": doc_id,
        "target_section": sec,
        "target_clause": clause,
        "ground_truth_answer": ans,
        "expected_citation": cite
    }
    for i, (q, doc_id, sec, clause, ans, cite) in enumerate([
        ("What is the Net Owned Fund threshold required for NBFCs under Scale Based Regulation?", "rbi-nbfc-sbr-2023", "Section 45-IA", "Clause 3.1", "₹10 crore Net Owned Fund (NOF).", "RBI/2023-24/102"),
        ("What is the minimum Capital Adequacy Ratio (CRAR) for Middle and Upper layer NBFCs?", "rbi-nbfc-sbr-2023", "Chapter IV", "Clause 14.1", "Minimum 15% CRAR, with Tier 1 capital not less than 10%.", "RBI/2023-24/102"),
        ("What is the minimum Tier 1 capital ratio for Middle Layer NBFCs?", "rbi-nbfc-sbr-2023", "Chapter IV", "Clause 14.1", "Tier 1 capital shall not be less than 10 percent.", "RBI/2023-24/102"),
        ("How many days overdue classifies an advance as NPA across NBFCs?", "rbi-nbfc-sbr-2023", "Chapter IV", "Clause 14.5", "90 days overdue.", "RBI/2023-24/102"),
        ("What are the days overdue for classification as SMA-1?", "rbi-irac-norms-2021", "Section 2", "Clause 2.3", "Overdue between 31 to 60 days.", "RBI/2021-22/104"),
        ("What are the days overdue for classification as SMA-2?", "rbi-irac-norms-2021", "Section 2", "Clause 2.3", "Overdue between 61 to 90 days.", "RBI/2021-22/104"),
        ("What is the periodic KYC updation frequency for high-risk customers?", "rbi-kyc-direction-2016", "Section 38", "Clause 38.1", "At least once every two years.", "RBI/DBR/2015-16/18"),
        ("What is the periodic KYC updation frequency for medium-risk customers?", "rbi-kyc-direction-2016", "Section 38", "Clause 38.1", "At least once every eight years.", "RBI/DBR/2015-16/18"),
        ("What is the periodic KYC updation frequency for low-risk customers?", "rbi-kyc-direction-2016", "Section 38", "Clause 38.1", "At least once every ten years.", "RBI/DBR/2015-16/18"),
        ("What is the minimum cooling-off period for digital loans of 7 days or more?", "rbi-digital-lending-2022", "Section B", "Clause 6", "Not less than three (3) days.", "RBI/2022-23/111"),
        ("What is the cooling-off period for digital loans with tenure under 7 days?", "rbi-digital-lending-2022", "Section B", "Clause 6", "Not less than one (1) day.", "RBI/2022-23/111"),
        ("What is the maximum portfolio cap on Default Loss Guarantee (DLG) in digital lending?", "rbi-dlg-digital-lending-2023", "Clause 3", "Clause 3.1", "5 percent of the outstanding loan portfolio.", "RBI/2023-24/41"),
        ("Within how many days must an RE invoke Default Loss Guarantee (DLG)?", "rbi-dlg-digital-lending-2023", "Clause 3", "Clause 6.1", "Maximum period of 120 days of overdue.", "RBI/2023-24/41"),
        ("How many working days does a bank have to execute credit card closure upon customer request?", "rbi-credit-card-directions-2022", "Chapter II", "Clause 10(f)", "Seven (7) working days.", "RBI/2022-23/92"),
        ("What is the per-day penalty payable to customer for delay in closing a credit card?", "rbi-credit-card-directions-2022", "Chapter II", "Clause 10(f)", "₹500 per day of delay until card closure.", "RBI/2022-23/92"),
        ("Within how many hours must severe cyber incidents be reported to RBI CSITE?", "rbi-it-governance-2023", "Chapter III", "Clause 12.3", "Within six (6) hours of detection.", "RBI/2023-24/107"),
        ("What is the mandated frequency for conducting Disaster Recovery (DR) drills in banks?", "rbi-it-governance-2023", "Chapter III", "Clause 15.2", "At least on a half-yearly basis.", "RBI/2023-24/107"),
        ("What is the standard asset provisioning rate on standard commercial advances?", "rbi-irac-norms-2021", "Section 2", "Clause 3.1", "0.40 percent.", "RBI/2021-22/104"),
        ("What is the provisioning requirement on unsecured sub-standard assets?", "rbi-irac-norms-2021", "Section 2", "Clause 3.1", "25 percent.", "RBI/2021-22/104"),
        ("What is the cooling period before giving fresh exposure to standard compromise settlement borrowers?", "rbi-compromise-settlements-2023", "Clause 4", "Clause 6.2", "Minimum of twelve (12) months.", "RBI/2023-24/40"),
        ("What is the cooling period for wilful defaulters entering compromise settlement?", "rbi-compromise-settlements-2023", "Clause 4", "Clause 6.2", "Not less than five (5) years.", "RBI/2023-24/40"),
        ("Within how many days must customer complaints be resolved before NBFC GRO escalation?", "rbi-fair-practices-nbfc-2023", "Section 2", "Clause 3.4", "Thirty (30) days.", "RBI/2023-24/53"),
        ("What is the overall PSL target percentage for domestic scheduled commercial banks?", "rbi-psl-directions-2020", "Chapter II", "Clause 4.1", "40 percent of ANBC or CEOBE.", "RBI/FIDD/2020-2021/72"),
        ("What is the PSL target percentage for Small Finance Banks?", "rbi-psl-directions-2020", "Chapter II", "Clause 4.1", "75 percent of ANBC.", "RBI/FIDD/2020-2021/72"),
        ("What is the Agriculture PSL sub-target percentage of ANBC?", "rbi-psl-directions-2020", "Chapter II", "Clause 4.2", "18 percent of ANBC.", "RBI/FIDD/2020-2021/72"),
        ("What is the Micro Enterprises PSL sub-target percentage of ANBC?", "rbi-psl-directions-2020", "Chapter II", "Clause 4.2", "7.5 percent of ANBC.", "RBI/FIDD/2020-2021/72"),
        ("What is the Weaker Sections PSL sub-target percentage of ANBC?", "rbi-psl-directions-2020", "Chapter II", "Clause 4.2", "12 percent of ANBC.", "RBI/FIDD/2020-2021/72"),
        ("Within how many days must banks settle claims of deceased depositors?", "rbi-customer-service-banks-2022", "Section 12", "Clause 12.1", "Not exceeding fifteen (15) days.", "RBI/2022-23/15"),
        ("What is the bank liability multiple for locker contents loss due to bank fault?", "rbi-customer-service-banks-2022", "Section 12", "Clause 14.3", "100 times the annual rent of the locker.", "RBI/2022-23/15"),
        ("Within how many minutes must board meeting decisions be disclosed under SEBI LODR Regulation 30?", "sebi-lodr-regulations-2015", "Regulation 30", "Regulation 30(2)", "30 minutes from closure of the board meeting.", "SEBI/LAD-NRO/GN/2015-16/013"),
        ("Within how many hours must events not emanating from listed entity be disclosed under LODR?", "sebi-lodr-regulations-2015", "Regulation 30", "Regulation 30(2)", "Within 24 hours.", "SEBI/LAD-NRO/GN/2015-16/013"),
        ("What turnover percentage constitutes materiality under SEBI LODR Regulation 30(4)?", "sebi-lodr-regulations-2015", "Regulation 30", "Regulation 30(4)", "Two percent (2%) of turnover.", "SEBI/LAD-NRO/GN/2015-16/013"),
        ("What is the minimum number of directors required in an Audit Committee under SEBI LODR?", "sebi-lodr-regulations-2015", "Regulation 18", "Regulation 18(1)", "Minimum three (3) directors.", "SEBI/LAD-NRO/GN/2015-16/013"),
        ("What fraction of Audit Committee members must be independent under SEBI LODR?", "sebi-lodr-regulations-2015", "Regulation 18", "Regulation 18(1)", "At least two-thirds.", "SEBI/LAD-NRO/GN/2015-16/013"),
        ("How many years must Structured Digital Database (SDD) records be preserved under SEBI PIT?", "sebi-pit-regulations-2015", "Regulation 3", "Regulation 3(5)", "Not less than eight (8) years.", "SEBI/LAD-NRO/GN/2014-15/21/85"),
        ("How many hours after financial results declaration does the trading window reopen?", "sebi-pit-regulations-2015", "Schedule B", "Clause 4", "48 hours.", "SEBI/LAD-NRO/GN/2014-15/21/85"),
        ("What is the VAPT testing frequency for stock brokers under SEBI circular?", "sebi-cybersecurity-brokers-2023", "Section 3", "Clause 3.1", "At least twice in a financial year (half-yearly).", "SEBI/HO/MIRSD/CIR/P/2023/112"),
        ("Within how many calendar days must critical VAPT vulnerabilities be remediated?", "sebi-cybersecurity-brokers-2023", "Section 3", "Clause 3.1", "Within fifteen (15) calendar days.", "SEBI/HO/MIRSD/CIR/P/2023/112"),
        ("For how many years must security and transaction logs be stored by stock brokers?", "sebi-cybersecurity-brokers-2023", "Section 3", "Clause 4.3", "Minimum period of two (2) years.", "SEBI/HO/MIRSD/CIR/P/2023/112"),
        ("What is the maximum Total Expense Ratio (TER) on the first 500 crore of equity mutual funds?", "sebi-mutual-funds-master-2019", "Chapter 10", "Clause 10.1", "2.25 percent.", "SEBI/HO/IMD/DF2/CIR/P/2019/17"),
        ("Within how many days must internal surveillance alerts be closed by brokers?", "sebi-surveillance-market-2022", "Clause 2", "Clause 2.1", "Within thirty (30) days.", "SEBI/HO/ISD/ISD-SEC-4/P/CIR/2022/107"),
        ("Within how many hours must brokers submit Suspicious Transaction Reports to stock exchanges?", "sebi-surveillance-market-2022", "Clause 2", "Clause 3.4", "Within forty-eight (48) hours of concluding investigation.", "SEBI/HO/ISD/ISD-SEC-4/P/CIR/2022/107"),
        ("Within how many days must statutory demand notice be sent under Section 138 of NI Act?", "statutory-ni-act-sec-138", "Section 138", "Section 138(b)", "Within thirty (30) days of dishonour memo.", "Act No. 26 of 1881"),
        ("What is the drawer cure period in days under Section 138 of NI Act?", "statutory-ni-act-sec-138", "Section 138", "Section 138(c)", "Fifteen (15) days.", "Act No. 26 of 1881"),
        ("What is the maximum prison sentence under Section 138 of NI Act?", "statutory-ni-act-sec-138", "Section 138", "Section 138 Penal", "Up to two (2) years imprisonment.", "Act No. 26 of 1881"),
        ("How many years must client identity records be maintained under PMLA Section 12?", "statutory-pmla-fiu-2002", "Section 12", "Section 12(1)(a)", "Five (5) years after account closure.", "Act No. 15 of 2003"),
        ("What is the cash transaction reporting (CTR) threshold under PMLA Section 12(1)(b)?", "statutory-pmla-fiu-2002", "Section 12", "Section 12(1)(b)", "More than rupees ten lakh (₹10,00,000).", "Act No. 15 of 2003"),
        ("Within how many working days must an STR be submitted to Director FIU-IND?", "statutory-pmla-fiu-2002", "Section 12", "Rule 7(2)", "Not later than seven (7) working days.", "Act No. 15 of 2003")
    ])
]

CONCEPTUAL_QA: List[Dict[str, Any]] = [
    {
        "id": f"CONCEPT-{i+1:03d}",
        "category": "conceptual_compliance",
        "query": q,
        "target_doc_id": doc_id,
        "target_section": sec,
        "target_clause": clause,
        "ground_truth_answer": ans,
        "expected_citation": cite
    }
    for i, (q, doc_id, sec, clause, ans, cite) in enumerate([
        ("What is the required reporting line and independence of the Chief Information Security Officer (CISO)?", "rbi-it-governance-2023", "Chapter III", "Clause 9.1", "CISO must be independent of IT operations, report to CRO or ED, and have direct access to Board IT Committee.", "RBI/2023-24/107"),
        ("What are the mandatory requirements for conducting Video-based Customer Identification Process (V-CIP)?", "rbi-kyc-direction-2016", "Section 16", "Clause 18.2", "V-CIP requires secure live audio-visual interaction, geotagging confirming customer in India, liveness check, and facial matching.", "RBI/DBR/2015-16/18"),
        ("What Officially Valid Documents (OVDs) can be accepted for individual Customer Due Diligence?", "rbi-kyc-direction-2016", "Section 16", "Clause 16.1", "Passport, driving licence, Aadhaar proof (masked), Voter ID, NREGA job card, or NPR letter.", "RBI/DBR/2015-16/18"),
        ("Can Digital Lending Apps access a customer's contacts and phone storage?", "rbi-digital-lending-2022", "Section B", "Clause 9", "DLAs and LSPs are strictly prohibited from accessing mobile device media, contacts, and call logs.", "RBI/2022-23/111"),
        ("What must be included in the Key Fact Statement (KFS) provided to digital loan borrowers?", "rbi-digital-lending-2022", "Section A", "Clause 4", "KFS must disclose all-inclusive APR, recovery mechanism, GRO details, and exact cooling-off period.", "RBI/2022-23/111"),
        ("What acceptable forms of security can be taken for Default Loss Guarantee (DLG)?", "rbi-dlg-digital-lending-2023", "Clause 3", "Clause 4.2", "Cash deposit with RE, SCB Fixed Deposits with lien, or Bank Guarantee in favour of RE.", "RBI/2023-24/41"),
        ("Can corporate guarantees or promissory notes be accepted as Default Loss Guarantee?", "rbi-dlg-digital-lending-2023", "Clause 3", "Clause 4.2", "No, corporate guarantees and promissory notes are not permitted as DLG instruments.", "RBI/2023-24/41"),
        ("Is a card issuer allowed to upgrade a customer's credit card without consent?", "rbi-credit-card-directions-2022", "Chapter II", "Clause 6(a)", "No, card issuers cannot upgrade cards without explicit written or authenticated electronic consent.", "RBI/2022-23/92"),
        ("Can a cardholder choose their own billing cycle for credit cards?", "rbi-credit-card-directions-2022", "Chapter II", "Clause 8(b)", "Yes, cardholders must be offered a one-time option to alter their billing cycle according to preference.", "RBI/2022-23/92"),
        ("Can banks outsource core credit sanctioning decisions to third parties?", "rbi-outsourcing-directions-2023", "Chapter II", "Clause 4.1", "No, core management functions including credit sanctioning and KYC determination cannot be outsourced.", "RBI/2023-24/108"),
        ("What audit and inspection rights must be present in outsourcing agreements for banks?", "rbi-outsourcing-directions-2023", "Chapter II", "Clause 7.3", "Agreements must grant RE, auditors, and RBI unhindered rights to inspect and audit service providers.", "RBI/2023-24/108"),
        ("What language must loan application communications be provided in by NBFCs?", "rbi-fair-practices-nbfc-2023", "Section 2", "Clause 2.1", "Communications must be in the vernacular language or a language understood by the borrower.", "RBI/2023-24/53"),
        ("Can an ESG Rating Provider offer consulting services to an entity it rates?", "sebi-esg-rating-providers-2023", "Chapter II", "Clause 5.3", "No, ESG Rating Providers cannot provide consulting or advisory services to entities they rate.", "SEBI/HO/DDHS/DDHS-RACPOD/P/CIR/2023/121"),
        ("Can an Online Bond Platform Provider offer unlisted debt instruments or P2P loans?", "sebi-obpp-framework-2023", "Section 2", "Clause 3.2", "No, unlisted bonds, debentures, and peer-to-peer products are strictly banned on registered OBPPs.", "SEBI/HO/DDHS/DDHS-PoD-1/P/2023/114"),
        ("Can Structured Digital Database (SDD) maintenance be outsourced to external third-party software?", "sebi-pit-regulations-2015", "Regulation 3", "Regulation 3(5)", "No, Structured Digital Database shall not be outsourced under SEBI PIT regulations.", "SEBI/LAD-NRO/GN/2014-15/21/85"),
        ("What qualifications must Audit Committee members possess under SEBI LODR?", "sebi-lodr-regulations-2015", "Regulation 18", "Regulation 18(1)", "All members must be financially literate, and at least one member must have accounting expertise.", "SEBI/LAD-NRO/GN/2015-16/013"),
        ("What constitutes a fit and proper person under SEBI Intermediaries Regulations?", "sebi-fit-proper-intermediaries-2008", "Schedule II", "Clause 1", "Integrity, reputation, character, financial solvency, competence, and absence of conviction.", "SEBI/LAD-NRO/GN/2008/11/126538"),
        ("What disqualifies an intermediary under SEBI Fit and Proper Person criteria?", "sebi-fit-proper-intermediaries-2008", "Schedule II", "Clause 3", "Restraint or prohibition order by SEBI, unsatisfied recovery proceedings, or insolvency declaration.", "SEBI/LAD-NRO/GN/2008/11/126538"),
        ("What types of trading patterns must broker internal surveillance systems flag?", "sebi-surveillance-market-2022", "Clause 2", "Clause 2.1", "Circular trading, pump and dump, synchronised trading, marking the close, and abnormal volume surges.", "SEBI/HO/ISD/ISD-SEC-4/P/CIR/2022/107"),
        ("Are distributor commissions allowed to be charged in Direct Plans of Mutual Funds?", "sebi-mutual-funds-master-2019", "Chapter 10", "Clause 10.4", "No, Direct Plans cannot be charged any distribution or distributor commission expenses.", "SEBI/HO/IMD/DF2/CIR/P/2019/17")
    ])
]

ADVERSARIAL_NEGATIVE_QA: List[Dict[str, Any]] = [
    {
        "id": f"NEG-{i+1:03d}",
        "category": "adversarial_negative",
        "query": q,
        "target_doc_id": "none",
        "target_section": "none",
        "target_clause": "none",
        "ground_truth_answer": "INSUFFICIENT_REGULATORY_EVIDENCE: The provided RBI/SEBI regulatory corpus does not contain sufficient authoritative grounds to answer this query with legal certainty.",
        "expected_citation": "NONE"
    }
    for i, q in enumerate([
        "How do I cook classic Italian carbonara pasta with guanciale and egg yolks?",
        "What are the requirements to obtain a driver's licence in California USA?",
        "Can a retail investor trade Bitcoin on unregistered offshore derivative exchanges?",
        "What is the personal income tax slab deduction for vacation travel in France?",
        "Can an NBFC completely waive all RBI capital adequacy regulations if directors agree unanimously?",
        "What is the legal speed limit on German autobahns?",
        "What are the rules for FIFA soccer world cup penalty shootouts?",
        "How can a bank bypass KYC for high net worth politicians without informing FIU?",
        "Can a credit card company charge 500% compound monthly interest on delayed card payments legally?",
        "What is the standard recipe for brewing espresso coffee beans at home?",
        "How do astronomers calculate orbital resonance between Jupiter and Saturn?",
        "What are the admission requirements for Harvard undergraduate physics?",
    ])
]

# Combine all 105 QA pairs
ALL_BENCHMARK_QA: List[Dict[str, Any]] = (
    BENCHMARK_QA_PAIRS + QUANTITATIVE_QA + CONCEPTUAL_QA + ADVERSARIAL_NEGATIVE_QA
)
