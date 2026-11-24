import math
import streamlit as st


def show_microgrid_simulator():
    st.header('Interactive Microgrid Simulator — Cuba, New Mexico')
    st.caption('Educational planning model: adjustable illustrative assumptions, not a site-specific engineering design or vendor quote.')
    st.subheader('1. Define your electricity demand')
    watts = st.number_input('Desired usable power output (W)', min_value=1.0, value=10000.0, step=1000.0, key='mg_w')
    hours = st.slider('Operating hours per day', 1, 24, 24, key='mg_h')
    kw = watts / 1000
    daily = kw * hours
    annual = daily * 365
    st.write(f'Your load requires **{kw:,.2f} kW** while operating and **{daily:,.2f} kWh/day**.')
    st.subheader('2. Choose generation and storage')
    solar_share = st.slider('Solar share of daily generation (%)', 0, 100, 80, key='mg_share') / 100
    st.write(f'Wind share: {(1-solar_share)*100:.0f}%')
    a,b = st.columns(2)
    with a:
        sun = st.number_input('Peak sun hours per day', 0.1, 12.0, 5.5, 0.1, key='mg_sun')
        panel = st.number_input('Solar panel rating (W)', 1, 1000, 400, key='mg_panel')
        efficiency = st.slider('Generation-to-load efficiency (%)', 50, 100, 85, key='mg_eff') / 100
    with b:
        cf = st.slider('Wind capacity factor (%)', 1, 60, 20, key='mg_cf') / 100
        backup = st.slider('Battery backup hours at full load', 0, 72, 8, key='mg_backup')
        dod = st.slider('Usable battery capacity (%)', 10, 100, 80, key='mg_dod') / 100
        discharge = st.slider('Battery-to-load efficiency (%)', 50, 100, 90, key='mg_dis') / 100
    gross = daily / efficiency
    solar_kw_required = gross * solar_share / sun
    panels = math.ceil(solar_kw_required * 1000 / panel)
    solar_kw = panels * panel / 1000
    wind_kw = gross * (1-solar_share) / (24 * cf)
    battery_kwh = kw * backup / (dod * discharge)
    inverter_kw = kw * 1.25
    solar_energy = solar_kw * sun
    wind_energy = wind_kw * 24 * cf
    delivered = (solar_energy + wind_energy) * efficiency
    st.subheader('3. Estimated equipment and energy flow')
    a,b,c = st.columns(3)
    a.metric('Solar array', f'{solar_kw:,.2f} kW', f'{panels:,} panels', delta_color='off')
    b.metric('Wind capacity', f'{wind_kw:,.2f} kW')
    c.metric('Battery nameplate', f'{battery_kwh:,.2f} kWh')
    st.write(f'Indicative load-side inverter rating: **{inverter_kw:,.2f} kW** (25% headroom).')
    st.graphviz_chart(f'''digraph {{
      rankdir=TB;
      node [shape=box style="rounded"];
      solar [label="Solar panels\\n{solar_energy:,.1f} kWh/day"];
      wind [label="Wind turbines\\n{wind_energy:,.1f} kWh/day"];
      bus [label="Power conversion + controlled microgrid bus"];
      battery [label="Battery\\n{battery_kwh:,.1f} kWh nameplate"];
      load [label="Electrical load\\n{daily:,.1f} kWh/day required"];
      loss [label="Modeled conversion/system losses\\n{(solar_energy+wind_energy-delivered):,.1f} kWh/day"];
      solar -> bus; wind -> bus; bus -> battery [dir=both]; bus -> load; bus -> loss;
    }}''')
    st.bar_chart({'Solar generation (kWh/day)': [solar_energy], 'Wind generation (kWh/day)': [wind_energy]})
    st.write(f'Estimated gross generation: **{solar_energy+wind_energy:,.2f} kWh/day**. Estimated usable energy: **{delivered:,.2f} kWh/day** before curtailment; annual load requirement: **{annual:,.2f} kWh**.')
    with st.expander('How the microgrid works', expanded=True):
        st.markdown('''1. **Generation:** Solar panels convert sunlight into DC electricity. Wind turbines convert wind energy into electricity.\n2. **Conversion:** Inverters and converters condition electricity for the microgrid.\n3. **Control:** The controller balances generation, storage and demand.\n4. **Storage:** Batteries charge when surplus energy is available and discharge when generation is insufficient.\n5. **Distribution:** Switchgear and distribution lines deliver electricity to loads. Grid-connected systems may import or export electricity when permitted.\n6. **Protection:** Breakers, relays and islanding controls protect equipment and people.''')
    st.subheader('4. Estimate construction and operating costs')
    st.caption('All default prices are illustrative editable assumptions in US dollars, not verified local prices. Avoid double-counting equipment included in other unit costs.')
    a,b = st.columns(2)
    with a:
        solar_price = st.number_input('Solar array installed cost ($/kW)', 0.0, value=1800.0, key='mg_sp')
        wind_price = st.number_input('Wind installed cost ($/kW)', 0.0, value=3500.0, key='mg_wp')
        battery_price = st.number_input('Battery installed cost ($/kWh)', 0.0, value=500.0, key='mg_bp')
        inverter_price = st.number_input('Additional inverter cost ($/kW)', 0.0, value=300.0, key='mg_ip')
    with b:
        controls = st.number_input('Additional controls, protection and distribution ($)', 0.0, value=10000.0, key='mg_ctrl')
        contingency = st.slider('Contingency (%)', 0, 50, 15, key='mg_cont') / 100
        maintenance = st.slider('Annual O&M (% of capital cost)', 0.0, 10.0, 2.0, 0.1, key='mg_om') / 100
        years = st.slider('Cost evaluation period (years)', 1, 30, 20, key='mg_years')
        replacement = st.number_input('Total additional replacement costs over period ($)', 0.0, value=0.0, key='mg_rep')
    costs = {'Solar array': solar_kw*solar_price, 'Wind generation': wind_kw*wind_price, 'Battery storage': battery_kwh*battery_price, 'Additional inverter': inverter_kw*inverter_price, 'Controls and distribution': controls}
    costs['Contingency'] = sum(costs.values()) * contingency
    capital = sum(costs.values())
    om = capital * maintenance
    lifetime = capital + om * years + replacement
    st.table([{'Component': k, 'Estimated cost (USD)': f'${v:,.2f}'} for k,v in costs.items()])
    st.bar_chart(costs)
    a,b,c = st.columns(3)
    a.metric('Upfront cost', f'${capital:,.0f}')
    b.metric('Annual O&M', f'${om:,.0f}')
    c.metric('Monthly O&M', f'${om/12:,.0f}')
    st.write(f'**{years}-year undiscounted cost:** ${lifetime:,.2f}')
    st.write(f'**Illustrative cost per required kWh:** ${lifetime/(annual*years):,.3f}/kWh, assuming all demand is served.')
    st.subheader('5. What these results mean for Cuba')
    st.info('This model balances average daily energy, not hourly power. It does not guarantee continuous supply. Peak sun hours are not ordinary sunshine hours, and wind capacity factor cannot be inferred from average surface wind speed alone. Validate local irradiance, hub-height wind, turbine power curves, seasonal loads, terrain and interconnection before design.')
    st.caption('Battery charging availability, cycling losses beyond the selected aggregate efficiency, degradation, land, permits, financing, taxes, backup fuel and grid purchases are not separately modeled. Include relevant additional costs in the editable inputs. Actual turbine ratings must be selected from available equipment; inverter surge and charging requirements require separate engineering checks.')


if __name__ == '__main__':
    show_microgrid_simulator()
