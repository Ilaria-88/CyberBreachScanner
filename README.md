# CyberBreachScanner - Threat Intelligence Tool

CyberBreachScanner is a threat intelligence prototype designed to help organizations monitor Shadow IT activity and assess potential data breach exposure for corporate domains.

The tool provides a clear, high-level view of external cyber risk by combining domain-focused checks with risk scoring and data visualization, enabling security teams to quickly identify priorities.

> **Disclaimer**: This prototype uses mock data for demonstration purposes.

## Table of Contents

- [Overview](#overview)
- [How it works](#how-it-works)
- [Installation](#installation)
- [Author](#author)

## Overview

CyberBreachScanner is built to support early-stage threat intelligence workflows by:

- Detecting potential Shadow IT indicators linked to company domains
- Simulating exposure signals related to known breach scenarios
- Translating technical findings into actionable risk levels
- Presenting results in a concise and readable format

This project is intended as a practical prototype for demos, internal validation, and future extension into real-world security pipelines.

## How it works

CyberBreachScanner follows a simple analysis pipeline:

1. **Data intake**  
   The tool processes domain-related inputs and simulated threat intelligence signals.

2. **Risk analysis**  
   Each domain is evaluated through weighted factors (for example: exposure indicators, breach relevance, and suspicious activity context).  
   These factors are aggregated into a risk score that supports prioritization.

3. **Data visualization**  
   Results are presented through structured output so analysts can quickly compare entities, understand relative severity, and focus on high-risk targets first.

This approach helps transform raw security indicators into decision-ready intelligence.

## Installation

### Prerequisites

- Python 3.9+ recommended
- `pip` available in your environment

### Setup

```bash
pip install -r requirements.txt
```

If you prefer manual package installation:

```bash
pip install flask requests
```

### Run

```bash
python app.py
```

## Author

**Ilaria**

