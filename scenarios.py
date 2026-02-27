"""
Pakistan T20 WC 2026 - Qualification Scenarios
Generates a clean HTML page with the scenarios
"""

import webbrowser
import os

# Current Pakistan stats BEFORE the Sri Lanka game
pak_runs_for = 164
pak_overs_for = 20.0
pak_runs_against = 166
pak_overs_against = 19.1

# New Zealand NRR to beat
nz_nrr = 1.390

def overs_to_decimal(overs):
    whole = int(overs)
    balls = round((overs - whole) * 10)
    return whole + balls / 6.0

def balls_to_overs_display(balls):
    overs = balls // 6
    remaining = balls % 6
    return f"{overs}.{remaining}"

def calc_nrr(runs_for, overs_for, runs_against, overs_against):
    dec_for = overs_to_decimal(overs_for)
    dec_against = overs_to_decimal(overs_against)
    return (runs_for / dec_for) - (runs_against / dec_against)


# ============ CALCULATE SCENARIO 1 ============
scenario1_rows = []
for pak_score in range(100, 261, 10):
    found = False
    for sl_score in range(pak_score - 1, -1, -1):
        total_for = pak_runs_for + pak_score
        total_overs_for = 20.0 + 20.0
        total_against = pak_runs_against + sl_score
        total_overs_against = 19.1 + 20.0

        nrr = calc_nrr(total_for, total_overs_for, total_against, total_overs_against)

        if nrr > nz_nrr:
            margin = pak_score - sl_score
            scenario1_rows.append({
                'pak': pak_score,
                'sl': sl_score,
                'margin': margin,
                'nrr': nrr
            })
            found = True
            break

    if not found:
        scenario1_rows.append({
            'pak': pak_score,
            'sl': '-',
            'margin': 'IMPOSSIBLE',
            'nrr': 0
        })


# ============ CALCULATE SCENARIO 2 ============
scenario2_rows = []
for sl_score in range(80, 221, 10):
    found = False
    pak_chase = sl_score + 1

    for chase_balls in range(120, 0, -1):
        chase_overs_display = balls_to_overs_display(chase_balls)
        chase_overs_raw = float(chase_overs_display)

        total_for = pak_runs_for + pak_chase
        total_overs_for = 20.0 + chase_overs_raw
        total_against = pak_runs_against + sl_score
        total_overs_against = 19.1 + 20.0

        nrr = calc_nrr(total_for, total_overs_for, total_against, total_overs_against)

        if nrr > nz_nrr:
            scenario2_rows.append({
                'sl': sl_score,
                'pak': pak_chase,
                'overs': chase_overs_display,
                'nrr': nrr
            })
            found = True
            break

    if not found:
        for extra in range(2, 100):
            pak_big_chase = sl_score + extra
            for chase_balls in range(120, 0, -1):
                chase_overs_display = balls_to_overs_display(chase_balls)
                chase_overs_raw = float(chase_overs_display)

                total_for = pak_runs_for + pak_big_chase
                total_overs_for = 20.0 + chase_overs_raw
                total_against = pak_runs_against + sl_score
                total_overs_against = 19.1 + 20.0

                nrr = calc_nrr(total_for, total_overs_for, total_against, total_overs_against)

                if nrr > nz_nrr:
                    scenario2_rows.append({
                        'sl': sl_score,
                        'pak': pak_big_chase,
                        'overs': chase_overs_display,
                        'nrr': nrr
                    })
                    found = True
                    break
            if found:
                break

        if not found:
            scenario2_rows.append({
                'sl': sl_score,
                'pak': '-',
                'overs': 'IMPOSSIBLE',
                'nrr': 0
            })


# ============ BUILD HTML ============
html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pakistan T20 WC 2026 - Qualification Scenarios</title>
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    body {
        background: #0a1628;
        color: #e0e0e0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        padding: 20px;
    }
    .container {
        max-width: 900px;
        margin: 0 auto;
    }
    .header {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, #01411C, #1B5E20);
        border-radius: 16px;
        margin-bottom: 30px;
    }
    .header h1 {
        font-size: 28px;
        color: #fff;
        margin-bottom: 8px;
    }
    .header .subtitle {
        color: #a5d6a7;
        font-size: 16px;
    }
    .header .nrr-target {
        margin-top: 16px;
        background: rgba(255,255,255,0.1);
        display: inline-block;
        padding: 8px 20px;
        border-radius: 8px;
        font-size: 14px;
        color: #fff;
    }
    .stats-row {
        display: flex;
        gap: 12px;
        margin-bottom: 30px;
    }
    .stat-card {
        flex: 1;
        background: #1a2332;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        border: 1px solid #2a3a4a;
    }
    .stat-card .label {
        font-size: 12px;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stat-card .value {
        font-size: 22px;
        font-weight: bold;
        margin-top: 4px;
    }
    .stat-card .value.negative { color: #ef5350; }
    .stat-card .value.positive { color: #66bb6a; }
    .stat-card .value.neutral { color: #fff; }
    .scenario {
        background: #1a2332;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        border: 1px solid #2a3a4a;
    }
    .scenario h2 {
        font-size: 20px;
        margin-bottom: 4px;
        color: #fff;
    }
    .scenario .desc {
        font-size: 14px;
        color: #888;
        margin-bottom: 20px;
    }
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th {
        background: #0d2137;
        color: #66bb6a;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 12px 16px;
        text-align: left;
        border-bottom: 2px solid #2a3a4a;
    }
    td {
        padding: 10px 16px;
        border-bottom: 1px solid #1e2d3d;
        font-size: 15px;
    }
    tr:hover {
        background: rgba(102, 187, 106, 0.05);
    }
    .impossible {
        color: #ef5350;
        font-weight: bold;
    }
    .nrr-cell {
        color: #66bb6a;
        font-weight: bold;
    }
    .highlight-row {
        background: rgba(102, 187, 106, 0.08);
    }
    .pak-flag { 
        font-size: 24px; 
        margin-right: 8px; 
    }
    .footer {
        text-align: center;
        padding: 20px;
        color: #555;
        font-size: 13px;
    }
</style>
</head>
<body>
<div class="container">

    <div class="header">
        <h1>🇵🇰 Pakistan Qualification Scenarios</h1>
        <div class="subtitle">ICC T20 World Cup 2026 - Group 2</div>
        <div class="nrr-target">Must beat New Zealand NRR of <strong>+1.390</strong></div>
    </div>

    <div class="stats-row">
        <div class="stat-card">
            <div class="label">Current NRR</div>
            <div class="value negative">""" + f"{calc_nrr(pak_runs_for, pak_overs_for, pak_runs_against, pak_overs_against):+.3f}" + """</div>
        </div>
        <div class="stat-card">
            <div class="label">Target NRR</div>
            <div class="value positive">+1.390</div>
        </div>
        <div class="stat-card">
            <div class="label">Runs For</div>
            <div class="value neutral">""" + f"{pak_runs_for}/{pak_overs_for}" + """</div>
        </div>
        <div class="stat-card">
            <div class="label">Runs Against</div>
            <div class="value neutral">""" + f"{pak_runs_against}/{pak_overs_against}" + """</div>
        </div>
    </div>

    <div class="scenario">
        <h2>🏏 Scenario 1: Pakistan Bats First</h2>
        <div class="desc">Pakistan posts a total, then restricts Sri Lanka below the required score (assuming SL bats full 20 overs)</div>
        <table>
            <thead>
                <tr>
                    <th>PAK Score</th>
                    <th>SL Must Be Under</th>
                    <th>Win Margin</th>
                    <th>NRR</th>
                </tr>
            </thead>
            <tbody>"""

for row in scenario1_rows:
    if row['margin'] == 'IMPOSSIBLE':
        html += f"""
                <tr>
                    <td>{row['pak']}</td>
                    <td class="impossible">IMPOSSIBLE</td>
                    <td class="impossible">-</td>
                    <td>-</td>
                </tr>"""
    else:
        html += f"""
                <tr>
                    <td><strong>{row['pak']}</strong></td>
                    <td>{row['sl']}</td>
                    <td>{row['margin']} runs</td>
                    <td class="nrr-cell">+{row['nrr']:.3f}</td>
                </tr>"""

html += """
            </tbody>
        </table>
    </div>

    <div class="scenario">
        <h2>🏏 Scenario 2: Pakistan Chases</h2>
        <div class="desc">Sri Lanka bats first and posts a total, Pakistan must chase it within the required overs</div>
        <table>
            <thead>
                <tr>
                    <th>SL Score</th>
                    <th>PAK Must Score</th>
                    <th>Chase Within</th>
                    <th>NRR</th>
                </tr>
            </thead>
            <tbody>"""

for row in scenario2_rows:
    if row['overs'] == 'IMPOSSIBLE':
        html += f"""
                <tr>
                    <td>{row['sl']}</td>
                    <td class="impossible">-</td>
                    <td class="impossible">IMPOSSIBLE</td>
                    <td>-</td>
                </tr>"""
    else:
        html += f"""
                <tr>
                    <td><strong>{row['sl']}</strong></td>
                    <td>{row['pak']}</td>
                    <td>{row['overs']} overs</td>
                    <td class="nrr-cell">+{row['nrr']:.3f}</td>
                </tr>"""

html += """
            </tbody>
        </table>
    </div>

    <div class="footer">
        Pakistan must WIN and finish with NRR above +1.390 to qualify ahead of New Zealand
    </div>

</div>
</body>
</html>"""


# ============ SAVE AND OPEN ============
output_path = os.path.join(os.path.dirname(__file__), 'scenarios.html')
with open(output_path, 'w') as f:
    f.write(html)

print(f"Saved to {output_path}")
webbrowser.open('file://' + os.path.abspath(output_path))