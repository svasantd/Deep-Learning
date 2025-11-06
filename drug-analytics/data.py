"""
Mock data for specialty drug portfolio analytics
"""

PORTFOLIO_DATA = {
    "payers": [
        {
            "id": "UHC",
            "name": "UnitedHealthcare",
            "sgp": 12300000,
            "yoy_change": 0.08,
            "margin": 0.24,
            "contracts": [
                {
                    "id": "UHC_ONC",
                    "name": "Oncology Portfolio",
                    "discount": 0.18,
                    "expires_days": 45,
                    "sgp": 4200000,
                    "yoy_change": -0.05,
                    "drugs": [
                        {
                            "id": "DRUG_A",
                            "name": "Drug A",
                            "sgp": 4200000,
                            "yoy_change": 0.12,
                            "margin": 0.28,
                            "margin_2024": 0.26,
                            "volume_impact": 250000,
                            "price_impact": -80000,
                            "cost_impact": -340000
                        },
                        {
                            "id": "DRUG_B",
                            "name": "Drug B",
                            "sgp": 3100000,
                            "yoy_change": -0.08,
                            "margin": 0.15,
                            "margin_2024": 0.20,
                            "volume_impact": 90000,
                            "price_impact": -120000,
                            "cost_impact": -340000
                        }
                    ]
                },
                {
                    "id": "UHC_RARE",
                    "name": "Rare Disease",
                    "discount": 0.22,
                    "expires_days": 120,
                    "sgp": 3100000,
                    "yoy_change": 0.12,
                    "drugs": [
                        {
                            "id": "DRUG_C",
                            "name": "Drug C",
                            "sgp": 2800000,
                            "yoy_change": 0.05,
                            "margin": 0.22,
                            "margin_2024": 0.22,
                            "volume_impact": 150000,
                            "price_impact": 50000,
                            "cost_impact": -100000
                        }
                    ]
                },
                {
                    "id": "UHC_AUTO",
                    "name": "Auto-Immune",
                    "discount": 0.15,
                    "expires_days": 90,
                    "sgp": 5000000,
                    "yoy_change": 0.20,
                    "drugs": [
                        {
                            "id": "DRUG_F",
                            "name": "Drug F",
                            "sgp": 5000000,
                            "yoy_change": 0.20,
                            "margin": 0.30,
                            "margin_2024": 0.28,
                            "volume_impact": 500000,
                            "price_impact": 100000,
                            "cost_impact": -200000
                        }
                    ]
                }
            ]
        },
        {
            "id": "ANTHEM",
            "name": "Anthem",
            "sgp": 8900000,
            "yoy_change": -0.03,
            "margin": 0.22,
            "contracts": [
                {
                    "id": "ANTHEM_IMM",
                    "name": "Immunology",
                    "discount": 0.20,
                    "expires_days": 180,
                    "sgp": 8900000,
                    "yoy_change": -0.03,
                    "drugs": [
                        {
                            "id": "DRUG_D",
                            "name": "Drug D",
                            "sgp": 5200000,
                            "yoy_change": -0.10,
                            "margin": 0.18,
                            "margin_2024": 0.23,
                            "volume_impact": -200000,
                            "price_impact": -150000,
                            "cost_impact": -180000
                        },
                        {
                            "id": "DRUG_G",
                            "name": "Drug G",
                            "sgp": 3700000,
                            "yoy_change": 0.05,
                            "margin": 0.25,
                            "margin_2024": 0.24,
                            "volume_impact": 150000,
                            "price_impact": 50000,
                            "cost_impact": -80000
                        }
                    ]
                }
            ]
        },
        {
            "id": "AETNA",
            "name": "Aetna",
            "sgp": 7200000,
            "yoy_change": 0.15,
            "margin": 0.26,
            "contracts": [
                {
                    "id": "AETNA_ONC",
                    "name": "Oncology",
                    "discount": 0.16,
                    "expires_days": 200,
                    "sgp": 7200000,
                    "yoy_change": 0.15,
                    "drugs": [
                        {
                            "id": "DRUG_E",
                            "name": "Drug E",
                            "sgp": 7200000,
                            "yoy_change": 0.15,
                            "margin": 0.26,
                            "margin_2024": 0.24,
                            "volume_impact": 400000,
                            "price_impact": 200000,
                            "cost_impact": -100000
                        }
                    ]
                }
            ]
        },
        {
            "id": "CIGNA",
            "name": "Cigna",
            "sgp": 6500000,
            "yoy_change": -0.12,
            "margin": 0.19,
            "contracts": [
                {
                    "id": "CIGNA_RARE",
                    "name": "Rare Disease",
                    "discount": 0.24,
                    "expires_days": 30,
                    "sgp": 6500000,
                    "yoy_change": -0.12,
                    "drugs": [
                        {
                            "id": "DRUG_H",
                            "name": "Drug H",
                            "sgp": 4000000,
                            "yoy_change": -0.15,
                            "margin": 0.16,
                            "margin_2024": 0.22,
                            "volume_impact": -300000,
                            "price_impact": -200000,
                            "cost_impact": -150000
                        },
                        {
                            "id": "DRUG_I",
                            "name": "Drug I",
                            "sgp": 2500000,
                            "yoy_change": -0.08,
                            "margin": 0.23,
                            "margin_2024": 0.25,
                            "volume_impact": -100000,
                            "price_impact": -50000,
                            "cost_impact": -80000
                        }
                    ]
                }
            ]
        }
    ]
}


def get_portfolio_totals():
    """Calculate portfolio-level totals"""
    total_sgp = sum(payer["sgp"] for payer in PORTFOLIO_DATA["payers"])
    weighted_yoy = sum(payer["sgp"] * payer["yoy_change"] for payer in PORTFOLIO_DATA["payers"]) / total_sgp
    weighted_margin = sum(payer["sgp"] * payer["margin"] for payer in PORTFOLIO_DATA["payers"]) / total_sgp

    return {
        "total_sgp": total_sgp,
        "yoy_change": weighted_yoy,
        "margin": weighted_margin
    }


def get_payer_by_id(payer_id):
    """Get payer object by ID"""
    for payer in PORTFOLIO_DATA["payers"]:
        if payer["id"] == payer_id:
            return payer
    return None


def get_contract_by_id(payer_id, contract_id):
    """Get contract object by payer and contract ID"""
    payer = get_payer_by_id(payer_id)
    if not payer:
        return None

    for contract in payer["contracts"]:
        if contract["id"] == contract_id:
            return contract
    return None


def get_drug_by_id(payer_id, contract_id, drug_id):
    """Get drug object by payer, contract, and drug ID"""
    contract = get_contract_by_id(payer_id, contract_id)
    if not contract:
        return None

    for drug in contract["drugs"]:
        if drug["id"] == drug_id:
            return drug
    return None


def get_urgent_alerts():
    """Generate urgent alerts from data"""
    alerts = []

    # Check for expiring contracts
    expiring_contracts = []
    total_at_risk = 0

    for payer in PORTFOLIO_DATA["payers"]:
        for contract in payer["contracts"]:
            if contract["expires_days"] < 60:
                expiring_contracts.append((payer["name"], contract["name"], contract["expires_days"], contract["sgp"]))
                total_at_risk += contract["sgp"]

    if expiring_contracts:
        alerts.append({
            "level": "critical",
            "message": f"{len(expiring_contracts)} contracts expire <60d (${total_at_risk/1000000:.1f}M at risk)",
            "type": "expiring_contracts",
            "data": expiring_contracts
        })

    # Check for margin drops
    for payer in PORTFOLIO_DATA["payers"]:
        for contract in payer["contracts"]:
            for drug in contract["drugs"]:
                margin_drop = drug["margin_2024"] - drug["margin"]
                if margin_drop >= 0.05:  # 5pp drop
                    alerts.append({
                        "level": "critical",
                        "message": f"{drug['name']} margin dropped {margin_drop*100:.0f}pp (investigate)",
                        "type": "margin_drop",
                        "payer_id": payer["id"],
                        "contract_id": contract["id"],
                        "drug_id": drug["id"]
                    })

    # Check for outperformers
    for payer in PORTFOLIO_DATA["payers"]:
        for contract in payer["contracts"]:
            for drug in contract["drugs"]:
                if drug["yoy_change"] > 0.15:  # >15% growth
                    alerts.append({
                        "level": "medium",
                        "message": f"{drug['name']} exceeding plan by {drug['yoy_change']*100:.0f}%",
                        "type": "outperformer",
                        "payer_id": payer["id"],
                        "contract_id": contract["id"],
                        "drug_id": drug["id"]
                    })

    return alerts


def get_all_drugs():
    """Get all drugs across all payers and contracts"""
    drugs = []
    for payer in PORTFOLIO_DATA["payers"]:
        for contract in payer["contracts"]:
            for drug in contract["drugs"]:
                drugs.append({
                    **drug,
                    "payer_id": payer["id"],
                    "payer_name": payer["name"],
                    "contract_id": contract["id"],
                    "contract_name": contract["name"]
                })
    return drugs
