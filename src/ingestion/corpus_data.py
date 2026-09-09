"""Official corpus data definitions for RBI, SEBI, and Statutory compliance texts."""

from typing import Any, Dict, List

REGULATORY_DOCUMENTS: List[Dict[str, Any]] = [
    {
        "doc_id": "rbi-nbfc-sbr-2023",
        "regulator": "RBI",
        "title": "Master Direction â€“ Reserve Bank of India (Non-Banking Financial Company â€“ Scale Based Regulation) Directions, 2023",
        "circular_number": "RBI/2023-24/102 DOR.FIN.HREC.No.45/03.10.119/2023-24",
        "issue_date": "2023-10-19",
        "subject": "Regulatory Framework for NBFCs under Scale Based Regulation (Base, Middle, Upper, and Top Layers)",
        "sections": [
            {
                "section_number": "Section 45-IA",
                "section_title": "Requirement of Registration and Net Owned Fund (NOF)",
                "clauses": [
                    {
                        "clause_number": "Clause 3.1",
                        "clause_title": "Certificate of Registration Mandatory Requirement",
                        "text": "In terms of Section 45-IA of the Reserve Bank of India Act, 1934, no non-banking financial company shall commence or carry on the business of a non-banking financial institution without obtaining a certificate of registration (CoR) issued by the Reserve Bank and having a Net Owned Fund (NOF) of not less than ten crore rupees (â‚¹10 crore). Existing NBFCs-ICC, NBFC-MFI, and IDF-NBFC with NOF below â‚¹10 crore shall achieve â‚¹10 crore by March 31, 2027 in a phased trajectory."
                    },
                    {
                        "clause_number": "Clause 3.2",
                        "clause_title": "Net Owned Fund Computation",
                        "text": "Net Owned Fund (NOF) shall be calculated in accordance with the explanation provided under Section 45-IA of the RBI Act, 1934. The computation deducts from the aggregate of paid-up equity capital and free reserves: (i) accumulated balance of loss, (ii) deferred revenue expenditure, and (iii) other intangible assets, further adjusted for investments in subsidiaries and group companies exceeding 10% of owned funds."
                    }
                ]
            },
            {
                "section_number": "Chapter IV",
                "section_title": "Capital Adequacy and Prudential Norms for Middle and Upper Layers",
                "clauses": [
                    {
                        "clause_number": "Clause 14.1",
                        "clause_title": "Minimum Capital Ratio (CRAR)",
                        "text": "Every NBFC in Middle and Upper Layers shall maintain a minimum capital ratio consisting of Tier 1 and Tier 2 capital which shall not be less than 15 percent of its aggregate risk weighted assets on-balance sheet and of risk adjusted value of off-balance sheet items. Tier 1 capital shall not be less than 10 percent at any point in time."
                    },
                    {
                        "clause_number": "Clause 14.5",
                        "clause_title": "Asset Classification & 90-day NPA Norm",
                        "text": "The norm for asset classification as Non-Performing Asset (NPA) shall be 90 days of overdue across all categories of NBFCs. NBFCs shall classify accounts as Special Mention Accounts (SMA): SMA-0 (principal or interest payment overdue between 1 to 30 days), SMA-1 (overdue between 31 to 60 days), and SMA-2 (overdue between 61 to 90 days). Upgradation of accounts classified as NPAs shall only be permitted after the borrower settles all arrears of interest and principal in full."
                    }
                ]
            }
        ]
    },
    {
        "doc_id": "rbi-kyc-direction-2016",
        "regulator": "RBI",
        "title": "Master Direction â€“ Know Your Customer (KYC) Direction, 2016 (Updated 2024)",
        "circular_number": "RBI/DBR/2015-16/18 Master Direction DBR.AML.BC.No.81/14.01.001/2015-16",
        "issue_date": "2016-02-25",
        "subject": "Customer Acceptance Policy, Customer Identification Procedures, and Monitoring of Transactions",
        "sections": [
            {
                "section_number": "Section 16",
                "section_title": "Customer Due Diligence (CDD) and Officially Valid Documents (OVD)",
                "clauses": [
                    {
                        "clause_number": "Clause 16.1",
                        "clause_title": "Officially Valid Document (OVD) Definition",
                        "text": "For undertaking Customer Due Diligence (CDD) of individual customers, Regulated Entities (REs) shall obtain: (a) passport, (b) driving licence, (c) proof of possession of Aadhaar number, (d) Voter's Identity Card issued by Election Commission of India, (e) job card issued by NREGA duly signed by an officer of the State Government, or (f) letter issued by the National Population Register containing details of name and address. Where customer submits proof of possession of Aadhaar, redaction or masking of the first 8 digits is mandatory."
                    },
                    {
                        "clause_number": "Clause 18.2",
                        "clause_title": "Video-based Customer Identification Process (V-CIP)",
                        "text": "Regulated Entities may undertake Customer Due Diligence through Video-based Customer Identification Process (V-CIP). V-CIP must be carried out on an authorized, secure live audio-visual interaction by a trained official of the RE. Geo-tagging and live liveness check are mandatory. The video recording must confirm customer presence within India at the time of onboarding. Spoofing detection and facial match scores against the official ID must be verified before account activation."
                    }
                ]
            },
            {
                "section_number": "Section 38",
                "section_title": "Periodic Updation of KYC",
                "clauses": [
                    {
                        "clause_number": "Clause 38.1",
                        "clause_title": "Periodic Updation Timeframes by Risk Categorization",
                        "text": "Periodic KYC updation shall be carried out at least once every two years for high-risk customers, once every eight years for medium-risk customers, and once every ten years for low-risk customers from the date of opening of the account or last KYC verification. In case of no change in KYC information of low and medium risk customers, self-declaration through non-face-to-face digital channels or registered email shall suffice."
                    }
                ]
            }
        ]
    },
    {
        "doc_id": "rbi-digital-lending-2022",
        "regulator": "RBI",
        "title": "Guidelines on Digital Lending (Master Direction)",
        "circular_number": "RBI/2022-23/111 DOR.CRE.REC.66/21.07.001/2022-23",
        "issue_date": "2022-09-02",
        "subject": "Direct Disbursal, Key Fact Statement, Cooling-Off Period, and LSP Data Privacy Governance",
        "sections": [
            {
                "section_number": "Section A",
                "section_title": "Loan Disbursal, Servicing and Repayment Architecture",
                "clauses": [
                    {
                        "clause_number": "Clause 3",
                        "clause_title": "Direct Account-to-Account Fund Flow",
                        "text": "All loan disbursals and repayments must be executed directly between the bank account of the Regulated Entity (RE) and the bank account of the borrower. Under no circumstances shall loan disbursal or servicing pass through any pool, escrow, or transit account of a Lending Service Provider (LSP) or third party, except for statutory deductions or corporate co-lending frameworks explicitly approved."
                    },
                    {
                        "clause_number": "Clause 4",
                        "clause_title": "Key Fact Statement (KFS) Requirement",
                        "text": "REs shall provide a standardized Key Fact Statement (KFS) to the borrower before the execution of the loan contract. The KFS must transparently disclose: (a) Annual Percentage Rate (APR) inclusive of all processing fees, verification charges, and third-party fees, (b) recovery mechanism, (c) details of the Grievance Redressal Officer, and (d) the exact cooling-off / look-up period. Any fee not mentioned in the KFS cannot be charged to the borrower."
                    }
                ]
            },
            {
                "section_number": "Section B",
                "section_title": "Cooling-Off Period and Borrower Rights",
                "clauses": [
                    {
                        "clause_number": "Clause 6",
                        "clause_title": "Mandatory Cooling-Off / Look-Up Window",
                        "text": "A cooling-off / look-up period shall be provided to borrowers during which they can exit the digital loan without any penalty by repaying the principal and proportionate APR. The cooling-off period shall be not less than three (3) days for loans having a tenure of seven (7) days or more, and not less than one (1) day for loans having a tenure of less than seven days."
                    },
                    {
                        "clause_number": "Clause 9",
                        "clause_title": "Data Privacy and Storage Restrictions",
                        "text": "Lending Service Providers (LSPs) and Digital Lending Apps (DLAs) are prohibited from accessing mobile device media, contacts list, call logs, and external storage. One-time access may be taken solely for camera, microphone, and location required for onboarding and KYC. All customer data must be stored on servers located within the territorial borders of India."
                    }
                ]
            }
        ]
    },
    {
        "doc_id": "rbi-dlg-digital-lending-2023",
        "regulator": "RBI",
        "title": "Guidelines on Default Loss Guarantee (DLG) in Digital Lending",
        "circular_number": "RBI/2023-24/41 DOR.CRE.REC.21/21.07.001/2023-24",
        "issue_date": "2023-06-08",
        "subject": "First Loss Default Guarantee (FLDG) Structures, Portfolio Caps, and Capital Requirements",
        "sections": [
            {
                "section_number": "Clause 3",
                "section_title": "Eligibility and Structure of Default Loss Guarantee (DLG)",
                "clauses": [
                    {
                        "clause_number": "Clause 3.1",
                        "clause_title": "5% Portfolio Cap on DLG",
                        "text": "Regulated Entities (REs) entering into Default Loss Guarantee (DLG) arrangements with Lending Service Providers (LSPs) shall ensure that the total amount of DLG cover on any outstanding loan portfolio does not exceed five percent (5%) of the amount of that loan portfolio. Any contractual structure that provides credit enhancement exceeding 5% is strictly prohibited and shall be treated as synthetic securitisation."
                    },
                    {
                        "clause_number": "Clause 4.2",
                        "clause_title": "Form of DLG Security Deposit",
                        "text": "REs shall accept DLG only in one or more of the following forms: (a) Cash deposit maintained with the RE, (b) Fixed Deposits maintained with a Scheduled Commercial Bank with lien marked in favour of the RE, or (c) Bank Guarantee in favour of the RE. Corporate guarantees or promissory notes are not permitted as acceptable DLG instruments."
                    },
                    {
                        "clause_number": "Clause 6.1",
                        "clause_title": "Invocation and Maximum Tenor of Invocation",
                        "text": "The RE shall invoke DLG within a maximum period of 120 days of overdue, unless the borrower settles the outstanding amount beforehand. DLG arrangements shall not relieve the RE of asset classification norms; recognition of NPA and provisioning shall be governed by IRAC norms irrespective of DLG availability."
                    }
                ]
            }
        ]
    },
    {
        "doc_id": "rbi-credit-card-directions-2022",
        "regulator": "RBI",
        "title": "Master Direction â€“ Credit Card and Debit Card â€“ Issuance and Conduct Directions, 2022",
        "circular_number": "RBI/2022-23/92 DoR.AUT.REC.No.27/24.01.041/2022-23",
        "issue_date": "2022-04-21",
        "subject": "Customer Protection, Billing Cycle Choice, Unsolicited Cards Penalties, and Account Closure",
        "sections": [
            {
                "section_number": "Chapter II",
                "section_title": "Credit Cards Governance and Issuance Rules",
                "clauses": [
                    {
                        "clause_number": "Clause 6(a)",
                        "clause_title": "Unsolicited Credit Cards and Penalty",
                        "text": "Card-issuers shall not issue unsolicited credit cards or upgrade existing cards without explicit written or authenticated electronic consent of the customer. In case an unsolicited card is issued or activated without consent, the card-issuer shall immediately deactivate the card and pay a penalty to the recipient amounting to twice the credit limit sanctioned on the card, without prejudice to other regulatory sanctions."
                    },
                    {
                        "clause_number": "Clause 8(b)",
                        "clause_title": "Flexibility in Billing Cycle",
                        "text": "Card-issuers shall offer a one-time option to cardholders to alter the billing cycle of the credit card at least once, according to the cardholder's preference, instead of compelling adherence to a pre-fixed standard billing date."
                    },
                    {
                        "clause_number": "Clause 10(f)",
                        "clause_title": "Seven-Day Mandatory Closure Rule",
                        "text": "Any request for closure of a credit card shall be honoured within seven (7) working days by the card-issuer, subject to payment of all outstanding dues. Failure to close the card within 7 working days shall render the card-issuer liable to pay a penalty of â‚¹500 per day of delay to the customer until the card is closed, provided there are no unpaid dues."
                    }
                ]
            }
        ]
    },
    {
        "doc_id": "rbi-it-governance-2023",
        "regulator": "RBI",
        "title": "Master Direction on Information Technology Governance, Risk, Controls and Regulatory Reporting, 2023",
        "circular_number": "RBI/2023-24/107 DoS.CO.CSITE.SEC.No.3/31.01.015/2023-24",
        "issue_date": "2023-11-07",
        "subject": "IT Committee, CISO Independence, Cyber Incident Escalation within 6 Hours, and DR Drills",
        "sections": [
            {
                "section_number": "Chapter III",
                "section_title": "IT Governance and CISO Appointment",
                "clauses": [
                    {
                        "clause_number": "Clause 9.1",
                        "clause_title": "Appointment and Role of CISO",
                        "text": "The Regulated Entity shall designate a senior officer as Chief Information Security Officer (CISO) who shall be independent of IT operations and business functions. The CISO shall report directly to the Chief Risk Officer (CRO) or Executive Director and shall have direct communication access to the Board IT Committee. The CISO cannot hold operational duties related to software development or infrastructure administration."
                    },
                    {
                        "clause_number": "Clause 12.3",
                        "clause_title": "Mandatory 6-Hour Cyber Incident Reporting",
                        "text": "All cyber security incidents of severe or critical severity (including ransomware infections, unauthorized data exfiltration, DDoS attacks causing disruption, or core banking compromise) must be reported to the Reserve Bank of India (CSITE) within six (6) hours of detection by the RE."
                    },
                    {
                        "clause_number": "Clause 15.2",
                        "clause_title": "Disaster Recovery (DR) and Business Continuity Drills",
                        "text": "REs shall establish a Disaster Recovery (DR) site located in a different seismic zone from the Primary Data Centre. DR drills for critical applications shall be conducted at least on a half-yearly basis, and failover simulations must demonstrate Recovery Time Objective (RTO) under two hours and Recovery Point Objective (RPO) near zero for core transaction systems."
                    }
                ]
            }
        ]
    },
    {
        "doc_id": "rbi-irac-norms-2021",
        "regulator": "RBI",
        "title": "Master Circular â€“ Prudential Norms on Income Recognition, Asset Classification and Provisioning pertaining to Advances (IRAC)",
        "circular_number": "RBI/2021-22/104 DOR.STR.REC.68/21.04.048/2021-22",
        "issue_date": "2021-10-01",
        "subject": "Classification of NPAs, Special Mention Accounts (SMA), and Provisioning Rates",
        "sections": [
            {
                "section_number": "Section 2",
                "section_title": "Asset Classification Framework",
                "clauses": [
                    {
                        "clause_number": "Clause 2.1",
                        "clause_title": "Definition of Non-Performing Asset (NPA)",
                        "text": "An asset, including a lease asset, becomes non-performing when it ceases to generate income for the bank. An advance is classified as an NPA where: (a) interest and/or instalment of principal remains overdue for a period of more than 90 days in respect of a term loan, (b) the account remains 'out of order' in respect of an Overdraft/Cash Credit (OD/CC), or (c) the bill remains overdue for more than 90 days in the case of bills purchased and discounted."
                    },
                    {
                        "clause_number": "Clause 2.3",
                        "clause_title": "Special Mention Account (SMA) Sub-Categories",
                        "text": "Lenders shall classify borrower accounts into Special Mention Account (SMA) sub-categories upon default on due dates: SMA-0 where principal or interest payment is overdue between 1 to 30 days; SMA-1 where payment is overdue between 31 to 60 days; and SMA-2 where payment is overdue between 61 to 90 days. Day-end process automation is mandatory across all core banking software."
                    },
                    {
                        "clause_number": "Clause 3.1",
                        "clause_title": "Standard Asset and Sub-Standard Provisioning Requirements",
                        "text": "Banks shall maintain general provisioning on standard advances: 0.40% on standard commercial advances, 0.25% on direct agricultural advances and SMEs, and 1.00% on commercial real estate advances. For sub-standard assets (NPA for up to 12 months), a general provision of 15% shall be made on secured portions and 25% on unsecured portions. For doubtful assets, provisioning increases from 25% (D1: up to 1 yr) to 40% (D2: 1 to 3 yrs) and 100% (D3: > 3 yrs)."
                    }
                ]
            }
        ]
    },
    {
        "doc_id": "rbi-compromise-settlements-2023",
        "regulator": "RBI",
        "title": "Framework for Compromise Settlements and Technical Write-offs",
        "circular_number": "RBI/2023-24/40 DOR.STR.REC.20/21.04.048/2023-24",
        "issue_date": "2023-06-08",
        "subject": "Board Approved Policy for Compromise Settlements, Wilful Defaulters, and Mandatory Cooling Period",
        "sections": [
            {
                "section_number": "Clause 4",
                "section_title": "Board Approved Policy and Approval Thresholds",
                "clauses": [
                    {
                        "clause_number": "Clause 4.1",
                        "clause_title": "Comprehensive Policy Framework",
                        "text": "Regulated Entities shall put in place Board-approved policies for undertaking compromise settlements and technical write-offs. The policy shall delineate delegation of powers, prudential floor on sacrifice, methodology for valuation of security, and permissible concessions. Settlements involving concessions above â‚¹50 lakh shall be approved by an executive committee headed by the Managing Director or equivalent."
                    },
                    {
                        "clause_number": "Clause 6.2",
                        "clause_title": "Cooling Period for Fresh Borrowing",
                        "text": "In respect of borrowers who have entered into compromise settlement, there shall be a mandatory cooling period before the RE can consider fresh exposure to such borrowers. The cooling period shall be a minimum of twelve (12) months for standard settlement cases. For wilful defaulters or fraud accounts subjected to compromise settlements without prejudice to ongoing criminal action, the cooling period shall not be less than five (5) years."
                    }
                ]
            }
        ]
    },
    {
        "doc_id": "rbi-outsourcing-directions-2023",
        "regulator": "RBI",
        "title": "Master Direction â€“ Reserve Bank of India (Outsourcing of Financial Services) Directions",
        "circular_number": "RBI/2023-24/108 DOR.ORG.REC.65/21.04.158/2023-24",
        "issue_date": "2023-11-15",
        "subject": "Core Management Functions Non-Delegable, Risk Assessment, and Vendor Audit Rights",
        "sections": [
            {
                "section_number": "Chapter II",
                "section_title": "Core Functions and Outsourcing Restrictions",
                "clauses": [
                    {
                        "clause_number": "Clause 4.1",
                        "clause_title": "Core Management Functions Prohibition",
                        "text": "Regulated Entities shall not outsource core management functions including corporate planning, decision-making on credit sanctioning, KYC compliance determination, management of investment portfolio, and compliance officer responsibilities. Outsourcing does not diminish the ultimate responsibility of the Board and senior management of the RE."
                    },
                    {
                        "clause_number": "Clause 7.3",
                        "clause_title": "Regulatory Inspection and Audit Rights",
                        "text": "Every outsourcing agreement shall contain clear clauses granting the RE, its internal/external auditors, and the Reserve Bank of India or its authorized representatives unhindered rights to inspect, audit, and examine the books, systems, and premises of the third-party service provider, including sub-contractors."
                    }
                ]
            }
        ]
    },
    {
        "doc_id": "rbi-fair-practices-nbfc-2023",
        "regulator": "RBI",
        "title": "Master Direction â€“ Fair Practices Code for Non-Banking Financial Companies",
        "circular_number": "RBI/2023-24/53 DOR.FIN.REC.No.29/03.10.119/2023-24",
        "issue_date": "2023-07-21",
        "subject": "Loan Sanction Disclosures, Vernacular Language Terms, and Grievance Redressal Officer",
        "sections": [
            {
                "section_number": "Section 2",
                "section_title": "Loan Applications and Processing Disclosures",
                "clauses": [
                    {
                        "clause_number": "Clause 2.1",
                        "clause_title": "Language and Acknowledgement of Loan Applications",
                        "text": "All communications to the borrower shall be in the vernacular language or a language understood by the borrower. Loan application forms shall include necessary information which affects the interest of the borrower so that a meaningful comparison with the terms offered by other NBFCs can be made. NBFCs shall devise a system of giving an acknowledgement for receipt of all loan applications."
                    },
                    {
                        "clause_number": "Clause 3.4",
                        "clause_title": "Grievance Redressal Mechanism & GRO Escalation",
                        "text": "At each branch and website, NBFCs shall prominently display the name, designation, telephone number, and email address of the Grievance Redressal Officer (GRO). If the customer complaint is not resolved within thirty (30) days, the customer may appeal to the Officer-in-Charge of the Regional Office of DNBS, RBI or the RBI Integrated Ombudsman."
                    }
                ]
            }
        ]
    },
    {
        "doc_id": "rbi-psl-directions-2020",
        "regulator": "RBI",
        "title": "Master Directions â€“ Priority Sector Lending (PSL) â€“ Targets and Classification",
        "circular_number": "RBI/FIDD/2020-2021/72 FIDD.CO.Plan.BC.5/04.09.01/2020-2021",
        "issue_date": "2020-09-04",
        "subject": "Mandatory Lending Targets for Agriculture, Micro-Enterprises, and Weaker Sections",
        "sections": [
            {
                "section_number": "Chapter II",
                "section_title": "Targets and Sub-Targets for Priority Sector",
                "clauses": [
                    {
                        "clause_number": "Clause 4.1",
                        "clause_title": "Overall Priority Sector Lending Targets",
                        "text": "Domestic scheduled commercial banks and foreign banks with 20 branches and above shall achieve an overall Priority Sector Lending target of 40 percent of Adjusted Net Bank Credit (ANBC) or Credit Equivalent of Off-Balance Sheet Exposure (CEOBE), whichever is higher. Small Finance Banks (SFBs) shall achieve an overall target of 75 percent of ANBC."
                    },
                    {
                        "clause_number": "Clause 4.2",
                        "clause_title": "Sub-targets for Agriculture and Weaker Sections",
                        "text": "Within the overall 40% PSL target for commercial banks, sub-targets are: (a) Agriculture: 18 percent of ANBC, with 10 percent earmarked for Small and Marginal Farmers (SMFs), (b) Micro Enterprises: 7.5 percent of ANBC, and (c) Advances to Weaker Sections: 12 percent of ANBC. Non-achievement of PSL targets requires shortfall deposit into Rural Infrastructure Development Fund (RIDF) with NABARD."
                    }
                ]
            }
        ]
    },
    {
        "doc_id": "rbi-customer-service-banks-2022",
        "regulator": "RBI",
        "title": "Master Circular â€“ Customer Service in Banks",
        "circular_number": "RBI/2022-23/15 DOR.CRE.REC.No.07/21.01.001/2022-23",
        "issue_date": "2022-04-01",
        "subject": "Deceased Depositors Settlement, Doorstep Banking, and Locker Allocation",
        "sections": [
            {
                "section_number": "Section 12",
                "section_title": "Settlement of Claims in Respect of Deceased Depositors",
                "clauses": [
                    {
                        "clause_number": "Clause 12.1",
                        "clause_title": "15-Day Time Limit for Claim Settlement",
                        "text": "Banks shall settle the claims in respect of deceased depositors and release payments to survivor(s)/nominee within a period not exceeding fifteen (15) days from the date of receipt of the claim subject to the production of proof of death and suitable identification of the claimant, without asking for succession certificate or letters of administration in accounts with nomination."
                    },
                    {
                        "clause_number": "Clause 14.3",
                        "clause_title": "Locker Compensation for Loss Due to Fire, Theft, or Fraud",
                        "text": "In instances where loss of contents of the locker occurs due to bank's negligence, fire, burglary, or fraudulent acts by its employees, the bank's liability shall be for an amount equivalent to one hundred (100) times the prevailing annual rent of the safe deposit locker."
                    }
                ]
            }
        ]
    },
    {
        "doc_id": "sebi-lodr-regulations-2015",
        "regulator": "SEBI",
        "title": "Securities and Exchange Board of India (Listing Obligations and Disclosure Requirements) Regulations, 2015",
        "circular_number": "SEBI/LAD-NRO/GN/2015-16/013 No. SEBI/LAD-NRO/GN/2015-16/013",
        "issue_date": "2015-09-02",
        "subject": "Regulation 30 Material Disclosures, Regulation 17 Board Composition, and Regulation 18 Audit Committee",
        "sections": [
            {
                "section_number": "Regulation 30",
                "section_title": "Disclosure of Events or Information",
                "clauses": [
                    {
                        "clause_number": "Regulation 30(2)",
                        "clause_title": "Mandatory Material Disclosures Timelines",
                        "text": "The listed entity shall disclose to the stock exchange(s) all events or information which are material as soon as reasonably possible and not later than: (i) thirty (30) minutes from the closure of the meeting of the board of directors in which the decision or event occurred; (ii) twelve (12) hours from the occurrence of the event or information if emanating from within the listed entity; and (iii) twenty-four (24) hours from the occurrence of the event or information if not emanating from within the listed entity."
                    },
                    {
                        "clause_number": "Regulation 30(4)",
                        "clause_title": "Materiality Threshold Criteria",
                        "text": "An event or information shall be deemed material if the omission or impact exceeds: (a) two percent (2%) of turnover as per the last audited consolidated financial statements; (b) two percent (2%) of net worth; or (c) five percent (5%) of the average of absolute value of profit or loss after tax for the last three pre-audited financial years."
                    }
                ]
            },
            {
                "section_number": "Regulation 18",
                "section_title": "Constitution of Audit Committee",
                "clauses": [
                    {
                        "clause_number": "Regulation 18(1)",
                        "clause_title": "Audit Committee Composition & Independence",
                        "text": "Every listed entity shall constitute a qualified and independent audit committee. The audit committee shall have minimum three (3) directors as members, of which at least two-thirds of the members shall be independent directors. All members of audit committee shall be financially literate and at least one member shall have accounting or related financial management expertise. The chairperson shall be an independent director."
                    }
                ]
            }
        ]
    },
    {
        "doc_id": "sebi-pit-regulations-2015",
        "regulator": "SEBI",
        "title": "Securities and Exchange Board of India (Prohibition of Insider Trading) Regulations, 2015",
        "circular_number": "SEBI/LAD-NRO/GN/2014-15/21/85",
        "issue_date": "2015-01-15",
        "subject": "UPSI Handling, Structured Digital Database (SDD), and Trading Window Restrictions",
        "sections": [
            {
                "section_number": "Regulation 3",
                "section_title": "Communication or Procurement of Unpublished Price Sensitive Information (UPSI)",
                "clauses": [
                    {
                        "clause_number": "Regulation 3(5)",
                        "clause_title": "Structured Digital Database (SDD) Mandatory Maintenance",
                        "text": "The board of directors or head(s) of the organisation of every person required to handle Unpublished Price Sensitive Information (UPSI) shall ensure that a Structured Digital Database (SDD) is maintained containing the nature of UPSI, the names of such persons who have shared the information and the names of such persons with whom such information is shared, along with the Permanent Account Number (PAN) or any other identifier authorized by law. Such database shall not be outsourced and shall be preserved for a period of not less than eight (8) years."
                    }
                ]
            },
            {
                "section_number": "Schedule B",
                "section_title": "Minimum Standards for Code of Conduct to Regulate, Monitor and Report Trading",
                "clauses": [
                    {
                        "clause_number": "Clause 4",
                        "clause_title": "Trading Window Closure Mandate",
                        "text": "Designated persons may execute trades subject to compliance with these regulations. The trading window shall be closed when the compliance officer determines that a designated person can reasonably be expected to have possession of UPSI. Trading restriction period shall mandatorily commence from the end of every quarter till forty-eight (48) hours after the declaration of financial results."
                    }
                ]
            }
        ]
    },
    {
        "doc_id": "sebi-cybersecurity-brokers-2023",
        "regulator": "SEBI",
        "title": "Cybersecurity and Cyber Resilience Framework for Stock Brokers & Depository Participants",
        "circular_number": "SEBI/HO/MIRSD/CIR/P/2023/112",
        "issue_date": "2023-07-06",
        "subject": "SOC Operations, Half-Yearly VAPT, Cyber Audit, and Critical Incident Escalation",
        "sections": [
            {
                "section_number": "Section 3",
                "section_title": "Vulnerability Assessment and Penetration Testing (VAPT)",
                "clauses": [
                    {
                        "clause_number": "Clause 3.1",
                        "clause_title": "Mandatory Half-Yearly VAPT",
                        "text": "All stock brokers and depository participants (DPs) shall conduct Vulnerability Assessment and Penetration Testing (VAPT) at least twice in a financial year (half-yearly). For Qualified Stock Brokers (QSBs), VAPT shall be carried out only by CERT-In empaneled organizations. Any high or critical vulnerability identified during VAPT must be remediated within fifteen (15) calendar days from the date of submission of the VAPT report."
                    },
                    {
                        "clause_number": "Clause 4.3",
                        "clause_title": "Security Operations Centre (SOC) & Log Retention",
                        "text": "Brokers and DPs shall establish or subscribe to a 24x7x365 Security Operations Centre (SOC) for continuous monitoring of security events. All perimeter, authentication, database, and transaction logs must be stored and securely archived for a minimum period of two (2) years, with baseline logs kept accessible online for immediate forensic scrutiny for at least ninety (90) days."
                    }
                ]
            }
        ]
    },
    {
        "doc_id": "sebi-mutual-funds-master-2019",
        "regulator": "SEBI",
        "title": "Master Circular for Mutual Funds",
        "circular_number": "SEBI/HO/IMD/DF2/CIR/P/2019/17",
        "issue_date": "2019-06-05",
        "subject": "Total Expense Ratio (TER) Limits, Scheme Categorization, and Risk-o-meter",
        "sections": [
            {
                "section_number": "Chapter 10",
                "section_title": "Total Expense Ratio (TER) Slabs",
                "clauses": [
                    {
                        "clause_number": "Clause 10.1",
                        "clause_title": "TER Limits for Equity and Debt Schemes",
                        "text": "The maximum permissible Total Expense Ratio (TER) on daily net assets for open-ended equity-oriented schemes shall be: 2.25% on the first â‚¹500 crore of daily net assets, reducing to 2.00% on the next â‚¹250 crore, 1.75% on the next â‚¹1,250 crore, 1.60% on the next â‚¹3,000 crore, 1.50% on the next â‚¹5,000 crore, and decreasing further as AUM expands. All fees and expenses charged to the scheme under any head must be contained within the permissible TER."
                    },
                    {
                        "clause_number": "Clause 10.4",
                        "clause_title": "Direct Plan Cost Differentiation",
                        "text": "Mutual fund schemes shall have separate Total Expense Ratios for Direct Plans and Regular Plans. The Direct Plan shall not be charged any distribution expenses, marketing costs, or distributor commission, and the TER of the Direct Plan must reflect a reduction equivalent to the entire commission payout."
                    }
                ]
            }
        ]
    },
    {
        "doc_id": "sebi-obpp-framework-2023",
        "regulator": "SEBI",
        "title": "Framework for Online Bond Platform Providers (OBPPs)",
        "circular_number": "SEBI/HO/DDHS/DDHS-PoD-1/P/2023/114",
        "issue_date": "2023-07-21",
        "subject": "Registration as Stock Broker in Debt Segment, Permissible Securities, and Settlement Mechanism",
        "sections": [
            {
                "section_number": "Section 2",
                "section_title": "Eligibility and Registration of OBPPs",
                "clauses": [
                    {
                        "clause_number": "Clause 2.1",
                        "clause_title": "Stock Broker Registration Requirement",
                        "text": "No person shall act as an Online Bond Platform Provider (OBPP) without obtaining registration as a stock broker in the debt segment under SEBI (Stock Brokers) Regulations, 1992. OBPPs shall offer only listed debt securities or debt securities proposed to be listed through a public issue on their platforms."
                    },
                    {
                        "clause_number": "Clause 3.2",
                        "clause_title": "Prohibition of Unlisted and Non-Debt Products",
                        "text": "An OBPP shall not offer on its online platform or any website/app linked thereto any unlisted bonds, unlisted debentures, products or securities other than debt securities. Disinvestment products and peer-to-peer debt instruments are strictly banned on registered OBPP domains."
                    }
                ]
            }
        ]
    },
    {
        "doc_id": "sebi-esg-rating-providers-2023",
        "regulator": "SEBI",
        "title": "Regulatory Framework for ESG Rating Providers (ERPs)",
        "circular_number": "SEBI/HO/DDHS/DDHS-RACPOD/P/CIR/2023/121",
        "issue_date": "2023-07-12",
        "subject": "Registration of ERPs, Transparency in Rating Methodologies, and BRSR Core Assurance",
        "sections": [
            {
                "section_number": "Chapter II",
                "section_title": "Registration and Methodology Standards",
                "clauses": [
                    {
                        "clause_number": "Clause 4.1",
                        "clause_title": "Mandatory Registration under CRA Regulations",
                        "text": "Entities providing Environmental, Social and Governance (ESG) ratings for Indian listed entities or in Indian securities markets shall obtain registration from SEBI under the SEBI (Credit Rating Agencies) Regulations, 1999. ERPs must ensure that their rating methodology incorporates parameters defined under Business Responsibility and Sustainability Reporting (BRSR) Core."
                    },
                    {
                        "clause_number": "Clause 5.3",
                        "clause_title": "Conflict of Interest and Independence",
                        "text": "An ESG Rating Provider shall not provide consulting or advisory services to any corporate entity that it rates. Analysts engaged in the ESG evaluation process shall not participate in commercial or fee negotiations with the target corporate entity."
                    }
                ]
            }
        ]
    },
    {
        "doc_id": "sebi-surveillance-market-2022",
        "regulator": "SEBI",
        "title": "Surveillance of Securities Market & Trade Execution Directives",
        "circular_number": "SEBI/HO/ISD/ISD-SEC-4/P/CIR/2022/107",
        "issue_date": "2022-08-08",
        "subject": "Trade Surveillance Alerts, Suspicious Activity Escalation, and Pump-and-Dump Prevention",
        "sections": [
            {
                "section_number": "Clause 2",
                "section_title": "Broker Internal Surveillance Systems",
                "clauses": [
                    {
                        "clause_number": "Clause 2.1",
                        "clause_title": "Mandatory Surveillance Alerts Processing",
                        "text": "Trading members and depository participants shall maintain an automated internal surveillance system generating transactional alerts covering: (a) circular trading, (b) pump and dump patterns, (c) synchronised trading, (d) marking the close, and (e) sudden volume surges unsupported by fundamentals. All alerts must be analyzed and closed within thirty (30) days."
                    },
                    {
                        "clause_number": "Clause 3.4",
                        "clause_title": "Reporting of Suspicious Transactions to Exchanges and SEBI",
                        "text": "Where internal analysis indicates market manipulation, fraudulent trades, or misuse of client accounts, the intermediary shall submit a detailed Suspicious Transaction Report to the Stock Exchanges within forty-eight (48) hours of concluding the internal investigation."
                    }
                ]
            }
        ]
    },
    {
        "doc_id": "sebi-fit-proper-intermediaries-2008",
        "regulator": "SEBI",
        "title": "SEBI (Intermediaries) Regulations, 2008 â€“ Criteria for Fit and Proper Person",
        "circular_number": "SEBI/LAD-NRO/GN/2008/11/126538 Schedule II",
        "issue_date": "2008-05-26",
        "subject": "Integrity, Solvency, Disqualification Conditions for Market Intermediaries",
        "sections": [
            {
                "section_number": "Schedule II",
                "section_title": "Criteria for Determining Fit and Proper Person",
                "clauses": [
                    {
                        "clause_number": "Clause 1",
                        "clause_title": "Fundamental Competence and Integrity Criteria",
                        "text": "For the purpose of determining whether an applicant or an intermediary is a 'fit and proper person', the Board may take into account any consideration as it deems fit, including: (a) integrity, reputation and character; (b) absence of conviction and restraint orders; (c) competence including financial solvency and net worth; (d) absence of categorization as a wilful defaulter."
                    },
                    {
                        "clause_number": "Clause 3",
                        "clause_title": "Disqualification Events",
                        "text": "A person shall not be considered 'fit and proper' if: (a) an order of restraint, prohibition or debarment has been passed by SEBI or any other regulatory authority against the applicant or its whole-time directors; (b) a recovery proceeding has been initiated by SEBI and remains unsatisfied; or (c) the entity is declared insolvent or is facing winding up proceedings."
                    }
                ]
            }
        ]
    },
    {
        "doc_id": "statutory-ni-act-sec-138",
        "regulator": "STATUTORY",
        "title": "Section 138 of the Negotiable Instruments Act, 1881",
        "circular_number": "Act No. 26 of 1881 - Section 138",
        "issue_date": "1881-12-09",
        "subject": "Dishonour of Cheque for Insufficiency of Funds, Statutory Demand Notice, and Criminal Liability",
        "sections": [
            {
                "section_number": "Section 138",
                "section_title": "Dishonour of Cheque for Insufficiency, etc., of Funds in the Account",
                "clauses": [
                    {
                        "clause_number": "Section 138(a)",
                        "clause_title": "Presentation within Validity Period",
                        "text": "Where any cheque drawn by a person on an account maintained by him with a banker for payment of any amount of money to another person from out of that account for the discharge, in whole or in part, of any debt or other liability, is returned by the bank unpaid, either because of the amount of money standing to the credit of that account is insufficient to honour the cheque or that it exceeds the amount arranged to be paid from that account by an agreement made with that bank, such person shall be deemed to have committed an offence. Condition (a): the cheque has been presented to the bank within a period of three months from the date on which it is drawn or within the period of its validity, whichever is earlier."
                    },
                    {
                        "clause_number": "Section 138(b)",
                        "clause_title": "Statutory Demand Notice within 30 Days",
                        "text": "Condition (b) under Section 138 of NI Act: the payee or the holder in due course of the cheque, as the case may be, makes a demand for the payment of the said amount of money by giving a notice in writing, to the drawer of the cheque, within thirty (30) days of the receipt of information by him from the bank regarding the return of the cheque as unpaid."
                    },
                    {
                        "clause_number": "Section 138(c)",
                        "clause_title": "15-Day Cure Period for Drawer and Cause of Action",
                        "text": "Condition (c) under Section 138 of NI Act: the drawer of such cheque fails to make the payment of the said amount of money to the payee or, as the case may be, to the holder in due course of the cheque, within fifteen (15) days of the receipt of the said notice. The cause of action arises on the 16th day following the expiry of the 15-day period, and a complaint must be filed before the competent Judicial Magistrate within one month thereafter under Section 142."
                    },
                    {
                        "clause_number": "Section 138 Penal",
                        "clause_title": "Criminal Penalty and Imprisonment",
                        "text": "Any person committing an offence under Section 138 shall be punished with imprisonment for a term which may be extended to two (2) years, or with fine which may extend to twice the amount of the cheque, or with both."
                    }
                ]
            }
        ]
    },
    {
        "doc_id": "statutory-pmla-fiu-2002",
        "regulator": "STATUTORY",
        "title": "Prevention of Money Laundering Act, 2002 (PMLA) & FIU-IND Reporting Directives",
        "circular_number": "Act No. 15 of 2003 - Section 12 / FIU-IND Reporting Rules",
        "issue_date": "2003-01-17",
        "subject": "Maintenance of Transaction Records, CTR Thresholds, and Suspicious Transaction Reporting (STR)",
        "sections": [
            {
                "section_number": "Section 12",
                "section_title": "Reporting Entity to Maintain Records",
                "clauses": [
                    {
                        "clause_number": "Section 12(1)(a)",
                        "clause_title": "Mandatory Maintenance of Records for Five Years",
                        "text": "Every reporting entity (including banking companies, financial institutions, intermediaries, and persons carrying on designated businesses) shall maintain a record of all transactions, the series of which have taken place within a month, in such manner as to enable it to reconstruct individual transactions. Records of identity of clients and beneficial owners shall be maintained for five (5) years after the business relationship has ended or the account has been closed."
                    },
                    {
                        "clause_number": "Section 12(1)(b)",
                        "clause_title": "Cash Transaction Reports (CTR) Threshold",
                        "text": "Reporting entities shall furnish to the Director, Financial Intelligence Unit - India (FIU-IND) information relating to all cash transactions of the value of more than rupees ten lakh (â‚¹10,00,000) or its equivalent in foreign currency, or a series of cash transactions integrally connected to each other which have taken place within a month where the aggregate value exceeds rupees ten lakh."
                    },
                    {
                        "clause_number": "Rule 7(2)",
                        "clause_title": "Suspicious Transaction Report (STR) Seven-Day Timeline",
                        "text": "The Principal Officer of a reporting entity shall furnish information regarding any Suspicious Transaction (STR) to the Director, FIU-IND not later than seven (7) working days on being satisfied that the transaction is suspicious. A transaction is suspicious where it gives rise to reasonable ground of suspicion that it may involve proceeds of crime, appears to have no economic rationale or bona fide purpose, or gives rise to suspicion of terrorist financing."
                    }
                ]
            }
        ]
    }
]

